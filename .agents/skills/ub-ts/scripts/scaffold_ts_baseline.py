#!/usr/bin/env python3
"""Scaffold the UB TypeScript starter baseline into a target repository."""

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
        description="Copy the UB TypeScript starter baseline into a target repository."
    )
    parser.add_argument(
        "target_root",
        help="Target repository root that should receive TypeScript starter files.",
    )
    parser.add_argument(
        "--archetype",
        choices=("node", "bundler", "library"),
        required=True,
        help="TypeScript project archetype to scaffold.",
    )
    parser.add_argument(
        "--with-eslint",
        action="store_true",
        help="Also scaffold the optional ESLint flat-config starter.",
    )
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    assets_root = script_path.parent.parent / "assets"
    target_root = Path(args.target_root).resolve()

    if not target_root.exists() or not target_root.is_dir():
        raise SystemExit(
            f"Target root does not exist or is not a directory: {target_root}"
        )

    results = [
        copy_if_missing(
            assets_root / "tsconfig-template" / args.archetype / "tsconfig.json",
            target_root / "tsconfig.json",
        )
    ]

    if args.with_eslint:
        results.append(
            copy_if_missing(
                assets_root / "eslint-template" / "eslint.config.mjs",
                target_root / "eslint.config.mjs",
            )
        )

    for line in results:
        print(line)

    print()
    print("Next steps:")
    print(f"1. Adapt tsconfig.json for the '{args.archetype}' repo structure.")
    if args.with_eslint:
        print("2. Install eslint, @eslint/js, typescript, and typescript-eslint.")
        print("3. Run: npx eslint .")
        print("4. Optional Task adoption bundle: see references/task-bundle.md")
    else:
        print("2. Run: npx tsc --noEmit")
        print("3. Optional Task adoption bundle: see references/task-bundle.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
