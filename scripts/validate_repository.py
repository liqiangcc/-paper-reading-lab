#!/usr/bin/env python3
"""Validate paper-reading-lab's lightweight repository governance invariants.

This intentionally checks deterministic repository structure only. It does not
score prose quality, replace reading-mcp identity checks, or validate live
GitHub Issue state.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "scripts/validate_repository.py",
    "tests/test_validate_repository.py",
    ".github/workflows/repository-consistency.yml",
    "README.md",
    "AGENTS.md",
    ".agents/skills/source-first-reading/SKILL.md",
    "docs/README.md",
    "docs/architecture/boundaries.md",
    "docs/domain/model.md",
    "docs/integrations/reading-mcp.md",
    "docs/source/source-policy.md",
    "docs/learning/source-first-sentence-reading.md",
    "docs/learning/incremental-explanation-profile.md",
    "docs/learning/reading-sessions.md",
    "docs/workflows/issue-driven-workflow.md",
    "docs/workflows/paper-reading-lifecycle.md",
    "docs/workflows/conversation-bootstrap.md",
    "docs/validation/invariants.md",
    "docs/pilot/first-pilot.md",
    "docs/pilot/first-pilot-closure.md",
    "docs/audits/2026-09-repository-audit.md",
)

CANONICAL_NAV_ENTRIES = (
    "../AGENTS.md",
    "architecture/boundaries.md",
    "domain/model.md",
    "integrations/reading-mcp.md",
    "source/source-policy.md",
    "learning/source-first-sentence-reading.md",
    "learning/incremental-explanation-profile.md",
    "learning/reading-sessions.md",
    "workflows/issue-driven-workflow.md",
    "workflows/paper-reading-lifecycle.md",
    "workflows/conversation-bootstrap.md",
    "validation/invariants.md",
    "pilot/first-pilot.md",
    "pilot/first-pilot-closure.md",
    "audits/2026-09-repository-audit.md",
)

STABLE_DOCS = ("README.md", "docs/README.md")
FORBIDDEN_STALE_LITERALS = (
    "当前执行入口：Raft 2014",
    "waiting for Codex Source acquisition",
    "Issue #1\n→ reading-mcp 打开 Raft",
)

# This is a bounded repository check, not a complete CommonMark renderer.
# Supported syntax and deliberately unverified cases are documented in
# docs/validation/repository-checks.md.
MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]\n]*\]\(\s*"
    r"(<[^>\n]*>|(?:\\.|[^()\s]|\([^()\n]*\))+)"
    r"(?:[ \t]+(?:\"[^\"]*\"|'[^']*'))?[ \t]*\)"
)
INVARIANT_RE = re.compile(r"^###\s+(I-\d{2})\b", re.MULTILINE)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", re.DOTALL)
HEADING_RE = re.compile(r"^ {0,3}#{1,6}[ \t]+(.+?)\s*$", re.MULTILINE)
EXPLICIT_ANCHOR_RE = re.compile(
    r"<(?:a|[hH][1-6])\b[^>]*\b(?:id|name)=[\"']([^\"']+)[\"']", re.I
)


def mask_text(text: str) -> str:
    """Keep newlines and offsets while hiding non-prose examples."""
    return "".join("\n" if char == "\n" else " " for char in text)


def visible_markdown(text: str, *, mask_inline: bool = True) -> tuple[str, list[int]]:
    """Mask top-level fences; report unclosed opener line numbers.

    A closer must have the same character and at least the opener's length.
    Backticks inside tilde fences, or shorter markers, are ordinary content.
    """
    visible: list[str] = []
    opened: tuple[str, int, int] | None = None
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        marker = FENCE_RE.match(line.rstrip("\r\n"))
        if opened is not None:
            if (marker and marker[1][0] == opened[0]
                    and len(marker[1]) >= opened[1] and not marker[2].strip()):
                opened = None
            visible.append(mask_text(line))
        elif marker and not (marker[1][0] == "`" and "`" in marker[2]):
            opened = (marker[1][0], len(marker[1]), number)
            visible.append(mask_text(line))
        else:
            visible.append(line)
    result = "".join(visible)
    # Complete HTML comments in prose do not supply navigation or headings.
    result = re.sub(r"<!--.*?-->", lambda m: mask_text(m[0]), result, flags=re.DOTALL)
    if mask_inline:
        result = INLINE_CODE_RE.sub(lambda m: mask_text(m[0]), result)
    return result, [opened[2]] if opened else []


def link_targets(text: str) -> list[str]:
    visible, _ = visible_markdown(text)
    return MARKDOWN_LINK_RE.findall(visible)


def heading_anchors(text: str) -> set[str]:
    """IDs for ordinary ATX headings, duplicate suffixes and explicit anchors.

    This covers the repo's current heading syntax; complex HTML/Setext and
    renderer-specific extensions are not presented as fully validated.
    """
    visible, _ = visible_markdown(text, mask_inline=False)
    prose, _ = visible_markdown(text)
    anchors: set[str] = set()
    generated: set[str] = set()
    for match in HEADING_RE.finditer(visible):
        if not HEADING_RE.match(prose, match.start()):
            continue
        title = re.sub(r"[ \t]+#+[ \t]*$", "", match[1])
        title = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", title)
        title = re.sub(r"<[^>]+>", "", title)
        title = html.unescape(title).replace("`", "").replace("*", "").replace("~", "")
        title = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"\1", title)
        slug = re.sub(r"[^\w -]", "", title.lower()).replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in generated:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        generated.add(candidate)
    anchors.update(generated)
    anchors.update(EXPLICIT_ANCHOR_RE.findall(prose))
    return anchors


def markdown_files() -> list[Path]:
    ignored_parts = {".git", ".venv", "node_modules"}
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in ignored_parts for part in path.parts)
    )


def normalize_link_target(raw: str) -> str:
    """Remove destination wrappers without discarding fragment identity."""
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return re.sub(r"\\([\\()\[\] ])", r"\1", target)


def is_external(target: str) -> bool:
    # External schemes are not fetched by this offline validator.
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)) or target.startswith("//")


def validate_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def validate_markdown_links(errors: list[str]) -> None:
    root = ROOT.resolve()
    anchor_cache: dict[Path, set[str]] = {}
    for path in markdown_files():
        for raw in link_targets(path.read_text(encoding="utf-8")):
            target = normalize_link_target(raw)
            if is_external(target):
                continue
            # Templates belong in code examples, not live navigation links.
            if any(marker in target for marker in ("${", "{{", "<owner>", "<repo>")):
                errors.append(f"unresolved link template: {path.relative_to(ROOT)} -> {raw}")
                continue
            location, _, fragment = target.partition("#")
            location = unquote(location.split("?", 1)[0])
            fragment = unquote(fragment)
            resolved = (path.parent / location).resolve() if location else path.resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"local link escapes repository: {path.relative_to(ROOT)} -> {raw}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link: {path.relative_to(ROOT)} -> {raw}")
                continue
            if fragment and resolved.is_file() and resolved.suffix.lower() == ".md":
                if resolved not in anchor_cache:
                    anchor_cache[resolved] = heading_anchors(resolved.read_text(encoding="utf-8"))
                if fragment not in anchor_cache[resolved]:
                    errors.append(f"broken local anchor: {path.relative_to(ROOT)} -> {raw}")


def parse_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(
            index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"
        )
    except StopIteration:
        return {}

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def validate_skill(errors: list[str]) -> None:
    relative = ".agents/skills/source-first-reading/SKILL.md"
    path = ROOT / relative
    if not path.is_file():
        return
    front_matter = parse_front_matter(path.read_text(encoding="utf-8"))
    if front_matter.get("name") != "source-first-reading":
        errors.append(f"{relative}: front matter name must be source-first-reading")
    if not front_matter.get("description"):
        errors.append(f"{relative}: front matter description is required")


def validate_invariant_ids(errors: list[str]) -> None:
    relative = "docs/validation/invariants.md"
    path = ROOT / relative
    if not path.is_file():
        return
    visible, _ = visible_markdown(path.read_text(encoding="utf-8"))
    ids = INVARIANT_RE.findall(visible)
    seen: set[str] = set()
    for invariant_id in ids:
        if invariant_id in seen:
            errors.append(f"{relative}: duplicate invariant id {invariant_id}")
        seen.add(invariant_id)

    required = {
        "I-01",
        "I-05",
        "I-11",
        "I-15",
        "I-21",
        "I-28",
        "I-30",
        "I-40",
        "I-44",
        "I-49",
        "I-55",
        "I-58",
        "I-59",
        "I-90",
        "I-91",
        "I-92",
        "I-93",
        "I-94",
    }
    missing = sorted(required.difference(seen))
    if missing:
        errors.append(f"{relative}: missing expected invariant ids: {', '.join(missing)}")


def validate_navigation(errors: list[str]) -> None:
    relative = "docs/README.md"
    path = ROOT / relative
    if not path.is_file():
        return
    targets = {normalize_link_target(raw).split("#", 1)[0]
               for raw in link_targets(path.read_text(encoding="utf-8"))}
    for entry in CANONICAL_NAV_ENTRIES:
        if entry not in targets:
            errors.append(f"{relative}: missing canonical navigation entry {entry}")


def validate_stable_docs(errors: list[str]) -> None:
    for relative in STABLE_DOCS:
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for literal in FORBIDDEN_STALE_LITERALS:
            if literal in text:
                errors.append(f"{relative}: stale live-state literal found: {literal!r}")


def validate_formatting(errors: list[str]) -> None:
    for path in markdown_files():
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.endswith((" ", "\t")):
                errors.append(f"{relative}:{line_number}: trailing whitespace")
            if "\t" in line:
                errors.append(f"{relative}:{line_number}: tab character")
        _, unclosed = visible_markdown(text)
        for line_number in unclosed:
            errors.append(f"{relative}:{line_number}: unclosed fenced code block")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_markdown_links(errors)
    validate_skill(errors)
    validate_invariant_ids(errors)
    validate_navigation(errors)
    validate_stable_docs(errors)
    validate_formatting(errors)

    if errors:
        print("repository consistency validation: FAIL", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1

    print("repository consistency validation: PASS")
    print(f"checked {len(markdown_files())} Markdown files")
    print(f"checked {len(REQUIRED_FILES)} required files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
