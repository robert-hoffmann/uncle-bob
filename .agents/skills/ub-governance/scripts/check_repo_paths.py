#!/usr/bin/env python3
"""Validate exact canonical repository paths and case-sensitive naming."""

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
exact_case_path_exists = REPO_INTEGRITY.exact_case_path_exists
write_payload = REPO_INTEGRITY.write_payload


CANONICAL_PATHS = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "Taskfile.yml",
    "plugin.json",
    "pyproject.toml",
    ".agents/skills",
    ".github/agents",
    ".github/plugin/marketplace.json",
)

LEGACY_PATHS = (
    "AGENTS.MD",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--output")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[4]
    errors: list[str] = []

    errors.extend(
        f"Canonical path missing or mis-cased: {relative_path}"
        for relative_path in CANONICAL_PATHS
        if not exact_case_path_exists(repo_root, relative_path)
    )
    errors.extend(
        f"Legacy path must not exist: {relative_path}"
        for relative_path in LEGACY_PATHS
        if exact_case_path_exists(repo_root, relative_path)
    )

    payload = {
        "status": "fail" if errors else "pass",
        "repoRoot": repo_root.as_posix(),
        "canonicalPaths": list(CANONICAL_PATHS),
        "ignoredScope": ["tmp/", "fixture-like content outside canonical surfaces"],
        "errors": errors,
        "warnings": [],
    }
    write_payload(payload, args.output)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
