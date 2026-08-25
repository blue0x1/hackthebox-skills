#!/usr/bin/env python3
"""Validate the public Hack The Box skill packages without network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("hackthebox-claude", "hackthebox-codex")
REQUIRED_FILES = (
    "SKILL.md",
    "references/service-enumeration.md",
    "references/core-methodology.md",
    "references/machine-playbooks.md",
    "references/challenge-playbooks.md",
    "references/sherlock-playbooks.md",
    "references/pivoting-and-ssh.md",
    "references/ad-and-windows.md",
    "references/web-application.md",
    "references/privilege-escalation.md",
    "references/forensics-and-malware.md",
    "references/nimux-usage.md",
    "references/nimux-command-surface.txt",
    "references/source-map.md",
    "references/exploit-review.md",
    "references/tooling-and-output.md",
    "references/study-roadmap.md",
    "templates/engagement-notes.md",
    "templates/htb-report.md",
    "templates/machine-report.md",
    "templates/challenge-report.md",
    "templates/sherlock-report.md",
    "templates/prolab-report.md",
    "templates/hypothesis-log.md",
    "templates/command-log.md",
)
MAX_SKILL_LINES = 500

SECRET_PATTERNS = (
    re.compile(r"BEGIN (?:RSA|OPENSSH|EC|DSA|PGP) PRIVATE KEY"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOCAL_LINK_PREFIXES = ("http://", "https://", "mailto:", "#")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def link_target_exists(base_dir: Path, target: str) -> bool:
    path_part = target.split("#", 1)[0].strip()
    if not path_part or path_part.startswith(LOCAL_LINK_PREFIXES):
        return True
    if path_part.startswith("<") and path_part.endswith(">"):
        path_part = path_part[1:-1]
    return (base_dir / path_part).exists()


def validate_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        contents = path.read_text(encoding="utf-8", errors="replace")
        for match in MARKDOWN_LINK.finditer(contents):
            target = match.group(1)
            if not link_target_exists(path.parent, target):
                fail(errors, f"broken local Markdown link in {path.relative_to(root)}: {target}")
    return errors


def validate_shared_skill_files() -> list[str]:
    errors: list[str] = []
    baseline = ROOT / "skills" / SKILLS[0]
    comparison = ROOT / "skills" / SKILLS[1]

    for relative_path in REQUIRED_FILES:
        if relative_path == "SKILL.md":
            continue
        baseline_path = baseline / relative_path
        comparison_path = comparison / relative_path
        if not baseline_path.is_file() or not comparison_path.is_file():
            continue
        baseline_text = baseline_path.read_text(encoding="utf-8", errors="replace")
        comparison_text = comparison_path.read_text(encoding="utf-8", errors="replace")
        if baseline_text != comparison_text:
            fail(errors, f"shared skill file differs between packages: {relative_path}")

    return errors


def validate_skill(skill_name: str) -> list[str]:
    errors: list[str] = []
    skill_dir = ROOT / "skills" / skill_name

    if not skill_dir.is_dir():
        fail(errors, f"missing skill directory: {skill_dir}")
        return errors

    for relative_path in REQUIRED_FILES:
        path = skill_dir / relative_path
        if not path.is_file():
            fail(errors, f"{skill_name}: missing required file {relative_path}")

    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return errors

    text = skill_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) >= MAX_SKILL_LINES:
        fail(errors, f"{skill_name}: SKILL.md has {len(lines)} lines; limit is under {MAX_SKILL_LINES}")

    if not text.startswith("---\n"):
        fail(errors, f"{skill_name}: SKILL.md is missing YAML frontmatter")
    else:
        closing = text.find("\n---\n", 4)
        if closing == -1:
            fail(errors, f"{skill_name}: YAML frontmatter is not closed")
        else:
            frontmatter = text[4:closing]
            if not re.search(r"^name:\s*\S+", frontmatter, re.MULTILINE):
                fail(errors, f"{skill_name}: frontmatter is missing name")
            if not re.search(r"^description:\s*\S+", frontmatter, re.MULTILINE):
                fail(errors, f"{skill_name}: frontmatter is missing description")

    for relative_path in REQUIRED_FILES:
        if relative_path == "SKILL.md":
            continue
        if relative_path not in text:
            fail(errors, f"{skill_name}: SKILL.md does not mention required resource {relative_path}")

    all_files = [path for path in skill_dir.rglob("*") if path.is_file()]
    for path in all_files:
        contents = path.read_text(encoding="utf-8", errors="replace")
        if "\x00" in contents:
            fail(errors, f"{skill_name}: NUL byte found in {path.relative_to(skill_dir)}")
        if "\ufffd" in contents:
            fail(errors, f"{skill_name}: replacement character found in {path.relative_to(skill_dir)}")
        if re.search(r"\[TODO|TODO:\s*", contents, re.IGNORECASE):
            fail(errors, f"{skill_name}: placeholder TODO found in {path.relative_to(skill_dir)}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(contents):
                fail(errors, f"{skill_name}: possible secret pattern found in {path.relative_to(skill_dir)}")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_markdown_links(ROOT))
    errors.extend(validate_shared_skill_files())
    for skill_name in SKILLS:
        errors.extend(validate_skill(skill_name))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(SKILLS)} skills successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
