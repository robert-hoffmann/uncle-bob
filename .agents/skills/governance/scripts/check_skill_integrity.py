#!/usr/bin/env python3
"""Validate unified governance skill integrity after hard cutover."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(slots=True)
class Violation:
    message: str


REPO_ROOT = Path(__file__).resolve().parents[4]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "governance"

REQUIRED_PATHS = (
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "agents" / "openai.yaml",
    SKILL_DIR / "references" / "exception-contract.md",
    SKILL_DIR / "references" / "gate-and-report-contract.md",
    SKILL_DIR / "references" / "profile-model.md",
    SKILL_DIR / "references" / "governance-commands.md",
    SKILL_DIR / "scripts" / "build_adr_registry.py",
    SKILL_DIR / "scripts" / "check_adr_gate.py",
    SKILL_DIR / "scripts" / "check_claim_register.py",
    SKILL_DIR / "scripts" / "check_test_signal.py",
    SKILL_DIR / "scripts" / "check_skill_integrity.py",
    SKILL_DIR / "tests" / "governance_scripts" / "test_governance_scripts.py",
)

LEGACY_SUFFIXES = ("core", "repository", "testing", "evidence")
PATH_REF_PATTERN = re.compile(r"\.agents/skills/governance-[a-z]+")
EXCEPTION_TEMPLATE_PATTERN = re.compile(r"^(governance_exception:|tdd_exception:|adr_waiver_exception:)")
READ_REF_PATTERN = re.compile(r"- Read `([^`]+)`")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def iter_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return [item for item in path.rglob("*") if item.is_file()]
    return []


def check_required_paths(violations: list[Violation]) -> None:
    for required in REQUIRED_PATHS:
        if not required.exists():
            violations.append(Violation(f"Missing required governance asset: {required.as_posix()}"))


def check_legacy_dirs(violations: list[Violation]) -> None:
    for suffix in LEGACY_SUFFIXES:
        legacy_dir = REPO_ROOT / ".agents" / "skills" / f"governance-{suffix}"
        if legacy_dir.exists():
            violations.append(Violation(f"Legacy governance directory still exists: {legacy_dir.as_posix()}"))


def check_stale_refs(violations: list[Violation]) -> None:
    scan_roots = (
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / ".github" / "workflows",
        REPO_ROOT / "docs",
    )

    for root in scan_roots:
        for path in iter_files(root):
            text = read_text(path)
            if text is None:
                continue

            for line_no, line in enumerate(text.splitlines(), start=1):
                if PATH_REF_PATTERN.search(line):
                    violations.append(
                        Violation(
                            f"Stale governance-* path reference in {path.as_posix()}:{line_no}: {line.strip()}"
                        )
                    )


def check_exception_templates(violations: list[Violation]) -> None:
    allowed_file = SKILL_DIR / "references" / "exception-contract.md"
    matches = 0

    for path in SKILL_DIR.rglob("*"):
        if not path.is_file():
            continue
        text = read_text(path)
        if text is None:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            if EXCEPTION_TEMPLATE_PATTERN.search(line):
                matches += 1
                if path != allowed_file:
                    violations.append(
                        Violation(
                            "Exception template schema definitions must exist only in "
                            f"{allowed_file.as_posix()} (found {path.as_posix()}:{line_no})"
                        )
                    )

    if matches == 0:
        violations.append(
            Violation(f"No exception-template schema definitions found in {SKILL_DIR.as_posix()}")
        )


def check_skill_read_refs(violations: list[Violation]) -> None:
    skill_md = SKILL_DIR / "SKILL.md"
    text = read_text(skill_md)
    if text is None:
        violations.append(Violation(f"Unable to read {skill_md.as_posix()} as UTF-8"))
        return

    for match in READ_REF_PATTERN.finditer(text):
        ref = match.group(1)
        candidate = SKILL_DIR / ref
        resolved = (SKILL_DIR / ref).resolve()
        if candidate.is_file() or resolved.is_file():
            continue
        violations.append(Violation(f"Missing reference path in {skill_md.as_posix()}: {ref}"))


def main() -> int:
    violations: list[Violation] = []
    check_required_paths(violations)
    check_legacy_dirs(violations)
    check_stale_refs(violations)
    check_exception_templates(violations)
    check_skill_read_refs(violations)

    if violations:
        for violation in violations:
            print(violation.message)
        return 1

    print("Unified governance skill integrity checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
