#!/usr/bin/env python3
"""Validate skill frontmatter shape and local runtime-facing references."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def load_repo_integrity_module():
    spec = importlib.util.spec_from_file_location("ub_governance_repo_integrity", SCRIPT_DIR / "_repo_integrity.py")
    if spec is None or spec.loader is None:
        raise ImportError("Unable to load _repo_integrity.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REPO_INTEGRITY = load_repo_integrity_module()
collect_skill_names = REPO_INTEGRITY.collect_skill_names
parse_frontmatter = REPO_INTEGRITY.parse_frontmatter
unresolved_local_reference_targets = REPO_INTEGRITY.unresolved_local_reference_targets
write_payload = REPO_INTEGRITY.write_payload


REQUIRED_FRONTMATTER_FIELDS = ("name", "description")
BOOLEAN_FIELDS = ("user-invocable", "disable-model-invocation")
STRING_FIELDS = ("argument-hint",)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--output")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[2]
    skills_root = repo_root / ".agents" / "skills"
    errors: list[str] = []
    checked_skills: list[str] = []

    for skill_name in collect_skill_names(repo_root):
        checked_skills.append(skill_name)
        skill_dir = skills_root / skill_name
        skill_path = skill_dir / "SKILL.md"
        frontmatter, body = parse_frontmatter(skill_path)
        if frontmatter is None:
            errors.append(f"{skill_name}: SKILL.md must start with valid YAML frontmatter")
            continue

        for field in REQUIRED_FRONTMATTER_FIELDS:
            value = frontmatter.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{skill_name}: frontmatter field '{field}' must be a non-empty string")

        if str(frontmatter.get("name", "")).strip() != skill_name:
            errors.append(f"{skill_name}: frontmatter name must match the skill directory name")

        errors.extend(
            f"{skill_name}: frontmatter field '{field}' must be a boolean when present"
            for field in BOOLEAN_FIELDS
            if field in frontmatter and not isinstance(frontmatter[field], bool)
        )

        errors.extend(
            f"{skill_name}: frontmatter field '{field}' must be a string when present"
            for field in STRING_FIELDS
            if field in frontmatter and not isinstance(frontmatter[field], str)
        )

        unresolved = unresolved_local_reference_targets(skill_dir, body)
        errors.extend(f"{skill_name}: unresolved local reference '{target}'" for target in unresolved)

    payload = {
        "status": "fail" if errors else "pass",
        "repoRoot": repo_root.as_posix(),
        "checkedSkills": checked_skills,
        "ignoredScope": ["tmp/", "fixture-like content outside .agents/skills/"],
        "errors": errors,
        "warnings": [],
    }
    write_payload(payload, args.output)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
