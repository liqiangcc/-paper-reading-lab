#!/usr/bin/env python3
"""Validate paper-reading-lab's lightweight repository governance invariants.

This intentionally checks deterministic repository structure only. It does not
score prose quality, replace reading-mcp identity checks, or validate live
GitHub Issue state.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
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

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
IMAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
INVARIANT_RE = re.compile(r"^###\s+(I-\d{2})\b", re.MULTILINE)


def read_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def markdown_files() -> list[Path]:
    ignored_parts = {".git", ".venv", "node_modules"}
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in ignored_parts for part in path.parts)
    )


def normalize_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    # Markdown allows an optional quoted title after the URL.
    if " \"" in target:
        target = target.split(" \"", 1)[0].strip()
    elif " '" in target:
        target = target.split(" '", 1)[0].strip()
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target)


def is_external_or_anchor(target: str) -> bool:
    lowered = target.lower()
    return (
        not target
        or target.startswith("#")
        or lowered.startswith(("http://", "https://", "mailto:", "tel:", "data:"))
        or target.startswith("//")
    )


def validate_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def validate_markdown_links(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        targets = MARKDOWN_LINK_RE.findall(text) + IMAGE_LINK_RE.findall(text)
        for raw in targets:
            target = normalize_link_target(raw)
            if is_external_or_anchor(target):
                continue
            # Skip templates or shell-like placeholders, which are not links.
            if any(marker in target for marker in ("${", "{{", "<owner>", "<repo>")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"local link escapes repository: {path.relative_to(ROOT)} -> {raw}"
                )
                continue
            if not resolved.exists():
                errors.append(
                    f"broken local link: {path.relative_to(ROOT)} -> {raw}"
                )


def parse_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
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
    ids = INVARIANT_RE.findall(path.read_text(encoding="utf-8"))
    seen: set[str] = set()
    for invariant_id in ids:
        if invariant_id in seen:
            errors.append(f"{relative}: duplicate invariant id {invariant_id}")
        seen.add(invariant_id)
    required = {"I-01", "I-05", "I-11", "I-21", "I-30", "I-40", "I-44", "I-55", "I-58", "I-59"}
    missing = sorted(required.difference(seen))
    if missing:
        errors.append(f"{relative}: missing expected invariant ids: {', '.join(missing)}")


def validate_navigation(errors: list[str]) -> None:
    relative = "docs/README.md"
    path = ROOT / relative
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for entry in CANONICAL_NAV_ENTRIES:
        if entry not in text:
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
        if text.count("```") % 2:
            errors.append(f"{relative}: unbalanced fenced code blocks")


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
