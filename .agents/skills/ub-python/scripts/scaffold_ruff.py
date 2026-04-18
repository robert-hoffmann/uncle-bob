#!/usr/bin/env python3
"""Scaffold the UB Python Ruff starter into a target repository."""

from __future__ import annotations

import argparse
from pathlib import Path


def copy_if_missing(source: Path, target: Path) -> str:
    if target.exists():
        return f"skip  {target}"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return f"write {target}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy the UB Python Ruff starter into a target repository."
    )
    parser.add_argument(
        "target_root",
        help="Target repository root that should receive Ruff starter files.",
    )
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    template_root = script_path.parent.parent / "assets" / "ruff-template"
    target_root = Path(args.target_root).resolve()

    if not target_root.exists() or not target_root.is_dir():
        raise SystemExit(
            f"Target root does not exist or is not a directory: {target_root}"
        )

    results = [
        copy_if_missing(template_root / "ruff.toml", target_root / "ruff.toml")
    ]

    for line in results:
        print(line)

    print()
    print("Next steps:")
    print("1. Adapt target-version, include/exclude, and known-first-party settings.")
    print("2. Ensure Ruff is installed or declared in the target repository.")
    print("3. Run: ruff check .")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
