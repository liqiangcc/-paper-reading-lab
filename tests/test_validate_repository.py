"""Positive and negative checks; all mutation fixtures are isolated/offline."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", REPO / "scripts/validate_repository.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class RepositoryChecks(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        root_patch = patch.object(validator, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def write(self, name: str, content: str) -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def check(self, name: str) -> list[str]:
        errors: list[str] = []
        getattr(validator, name)(errors)
        return errors

    def links(self, content: str) -> list[str]:
        self.write("README.md", content)
        return self.check("validate_markdown_links")

    def test_missing_live_link_is_rejected(self) -> None:
        self.assertIn("broken local link", self.links("[x](missing.md)\n")[0])

    def test_fenced_examples_are_not_links(self) -> None:
        for marker in ("```", "~~~", "````", "~~~~"):
            with self.subTest(marker=marker):
                self.assertEqual([], self.links(f"{marker}markdown\n[x](missing.md)\n{marker}\n"))

    def test_inline_examples_are_not_links(self) -> None:
        for example in ("`[x](missing.md)`", "``[x](missing.md) `literal` ``"):
            with self.subTest(example=example):
                self.assertEqual([], self.links(f"Use {example}.\n"))

    def test_unmatched_inline_backtick_does_not_hide_links(self) -> None:
        self.assertIn("broken local link", self.links("` [x](missing.md)\n")[0])

    def test_live_link_after_fence_is_checked(self) -> None:
        self.assertEqual(1, len(self.links("~~~\n[x](example.md)\n~~~\n[x](missing.md)\n")))

    def test_prose_comments_do_not_supply_links(self) -> None:
        self.assertEqual([], self.links("<!-- [x](missing.md) -->\n"))

    def test_matching_fences_allow_longer_closers(self) -> None:
        for content in ("````md\n```\n````\n", "~~~text\n```\n~~~~\n"):
            with self.subTest(content=content):
                self.write("README.md", content)
                self.assertEqual([], self.check("validate_formatting"))

    def test_unclosed_tilde_is_rejected(self) -> None:
        self.write("README.md", "~~~text\nnot closed\n")
        self.assertIn(":1: unclosed", self.check("validate_formatting")[0])

    def test_short_fence_cannot_close_long_fence(self) -> None:
        self.write("README.md", "````text\nvalue\n```\n")
        self.assertIn("unclosed", self.check("validate_formatting")[0])

    def test_wrong_fence_character_cannot_close(self) -> None:
        self.write("README.md", "```text\nvalue\n~~~\n")
        self.assertIn("unclosed", self.check("validate_formatting")[0])

    def test_closer_with_nonspace_suffix_is_content(self) -> None:
        self.write("README.md", "```text\nx\n```not-a-closer\n")
        self.assertIn("unclosed", self.check("validate_formatting")[0])

    def test_missing_local_heading_is_rejected(self) -> None:
        self.assertIn("broken local anchor", self.links("# Existing\n\n[x](#missing)\n")[0])

    def test_existing_heading_same_file(self) -> None:
        self.assertEqual([], self.links("# Existing\n\n[x](#existing)\n"))

    def test_cross_file_unicode_heading_and_encoded_space(self) -> None:
        self.write("docs/a b.md", "# 中文标题\n")
        self.assertEqual([], self.links('[x](docs/a%20b.md#%E4%B8%AD%E6%96%87%E6%A0%87%E9%A2%98 "title")\n'))

    def test_angle_wrapped_path_with_title(self) -> None:
        self.write("docs/a b.md", "# Example\n")
        self.assertEqual([], self.links('[x](<docs/a b.md#example> "title")\n'))

    def test_filename_with_parentheses(self) -> None:
        self.write("a(b).md", "# Example\n")
        for target in ("a(b).md", r"a\(b\).md"):
            with self.subTest(target=target):
                self.assertEqual([], self.links(f"[x]({target}#example)\n"))

    def test_repeated_heading_suffixes(self) -> None:
        text = "# Same\n# Same\n# Same-1\n# Same\n"
        self.assertEqual({"same", "same-1", "same-1-1", "same-2"}, validator.heading_anchors(text))

    def test_fenced_heading_does_not_create_anchor(self) -> None:
        self.assertIn("broken local anchor", self.links("```\n# Example\n```\n[x](#example)\n")[0])

    def test_formatted_heading_keeps_inline_code_content(self) -> None:
        self.assertEqual({"api--planned_scope"}, validator.heading_anchors("## **API** / `planned_scope`\n"))

    def test_explicit_anchor(self) -> None:
        self.assertEqual([], self.links('<a id="custom"></a>\n[x](#custom)\n'))

    def test_inline_anchor_example_is_not_an_anchor(self) -> None:
        self.assertIn("broken local anchor", self.links('Use `<a id="fake"></a>`.\n[x](#fake)\n')[0])

    def test_heading_in_multiline_inline_code_is_not_an_anchor(self) -> None:
        self.assertIn("broken local anchor", self.links('Use `example\n# Fake\nend`.\n[x](#fake)\n')[0])

    def test_external_links_are_not_fetched(self) -> None:
        self.assertEqual([], self.links("[x](https://invalid.example/no#heading)\n[x](mailto:x@y.test)\n"))

    def test_images_are_checked(self) -> None:
        self.assertIn("broken local link", self.links("![x](missing.png)\n")[0])

    def test_path_escape_is_rejected(self) -> None:
        for target in ("../outside.md", "%2E%2E/outside.md", "/etc/passwd"):
            with self.subTest(target=target):
                self.assertIn("escapes repository", self.links(f"[x]({target})\n")[0])

    def test_unresolved_live_templates_are_rejected(self) -> None:
        self.assertIn("unresolved link template", self.links("[x](docs/${name}.md)\n")[0])

    def test_gate_and_tests_are_required(self) -> None:
        for path in validator.REQUIRED_FILES:
            self.write(path, "placeholder\n")
        self.assertEqual([], self.check("validate_required_files"))
        for name in (".github/workflows/repository-consistency.yml", "scripts/validate_repository.py", "tests/test_validate_repository.py"):
            with self.subTest(name=name):
                (self.root / name).unlink()
                self.assertIn(f"missing required file: {name}", self.check("validate_required_files"))
                self.write(name, "placeholder\n")

    def test_skill_minimum_front_matter(self) -> None:
        path = ".agents/skills/source-first-reading/SKILL.md"
        self.write(path, "---\nname: source-first-reading\ndescription: Test\n---\n")
        self.assertEqual([], self.check("validate_skill"))
        self.write(path, "---\nname: wrong\ndescription:\n---\n")
        self.assertEqual(2, len(self.check("validate_skill")))

    def test_navigation_requires_links_not_path_mentions(self) -> None:
        text = "\n".join(f"`{name}`" for name in validator.CANONICAL_NAV_ENTRIES)
        self.write("docs/README.md", text)
        self.assertEqual(len(validator.CANONICAL_NAV_ENTRIES), len(self.check("validate_navigation")))
        self.write("docs/README.md", "\n".join(f"[x]({name})" for name in validator.CANONICAL_NAV_ENTRIES))
        self.assertEqual([], self.check("validate_navigation"))

    def test_duplicate_invariants_and_code_examples(self) -> None:
        self.write("docs/validation/invariants.md", "### I-01 Real\n```md\n### I-01 Example\n```\n")
        self.assertFalse(any("duplicate" in e for e in self.check("validate_invariant_ids")))
        self.write("docs/validation/invariants.md", "### I-01 Real\n### I-01 Duplicate\n")
        self.assertTrue(any("duplicate" in e for e in self.check("validate_invariant_ids")))

    def test_repository_and_mutation_exit_codes(self) -> None:
        shutil.copytree(REPO, self.root, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(0, validator.main())
            self.write("negative-probe.md", "[x](missing.md)\n")
            self.assertEqual(1, validator.main())
            (self.root / "negative-probe.md").unlink()
            self.assertEqual(0, validator.main())


if __name__ == "__main__":
    unittest.main()
