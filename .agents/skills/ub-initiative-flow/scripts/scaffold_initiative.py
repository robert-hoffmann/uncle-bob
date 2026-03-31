#!/usr/bin/env python3
"""Copy the canonical initiative scaffold into a target directory."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from pathlib import Path
import shutil

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE_ROOT = SKILL_ROOT / "assets" / "initiative-template"
TEXT_FILE_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
}


def derive_initiative_name(target_root: Path) -> str:
    """Derive a readable initiative name from the target directory name."""

    parts = [part for part in target_root.name.split("-") if part]
    if len(parts) >= 4 and all(part.isdigit() for part in parts[:3]):
        parts = parts[3:]
    if not parts:
        return target_root.name
    return " ".join(parts).replace("_", " ").title()


def ensure_target_is_safe(target_root: Path) -> None:
    """Reject reruns against populated targets to avoid clobbering work."""

    if not target_root.exists():
        return
    if not target_root.is_dir():
        raise ValueError(f"Target path exists and is not a directory: {target_root.as_posix()}")
    if any(target_root.iterdir()):
        raise ValueError(
            "Target directory already contains files. "
            "Choose a new target or move the existing initiative first: "
            f"{target_root.as_posix()}"
        )


def normalize_path(value: Path) -> str:
    """Return a stable slash-based path string for generated files."""

    current_root = Path.cwd().resolve()
    try:
        return value.relative_to(current_root).as_posix()
    except ValueError:
        return value.as_posix()


def build_placeholder_map(args: argparse.Namespace, target_root: Path) -> dict[str, str]:
    """Build the placeholder replacements for the copied scaffold."""

    initiative_name = args.initiative_name or derive_initiative_name(target_root)

    values = {
        "REPLACE_INITIATIVE_NAME"    : initiative_name,
        "REPLACE_INITIATIVE_ROOT"    : normalize_path(target_root),
        "REPLACE_PHASE"              : args.phase,
        "REPLACE_GATE_STATE"         : args.gate_state,
        "REPLACE_ROADMAP_STATUS"     : args.roadmap_status,
        "REPLACE_CURRENT_STEP"       : args.current_step,
        "REPLACE_NEXT_ACTION"        : args.next_action,
        "REPLACE_OWNER"              : args.owner,
        "REPLACE_VALIDATION_COMMANDS": args.validation_commands,
        "REPLACE_EVIDENCE_POINTERS"  : args.evidence_pointers,
    }

    return {key: value for key, value in values.items() if value is not None}


def should_render(path: Path) -> bool:
    """Restrict rendering to known text artifacts in the scaffold."""

    return path.suffix in TEXT_FILE_SUFFIXES or path.name == "AGENTS.md"


def render_placeholders(root: Path, replacements: Mapping[str, str]) -> None:
    """Render placeholders in copied text files while preserving unknown tokens."""

    for path in sorted(root.rglob("*")):
        if not path.is_file() or not should_render(path):
            continue
        text = path.read_text(encoding="utf-8")
        updated = text
        for placeholder, value in replacements.items():
            updated = updated.replace(placeholder, value)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def copy_scaffold(template_root: Path, target_root: Path) -> None:
    """Copy the initiative scaffold to the requested target directory."""

    shutil.copytree(template_root, target_root, dirs_exist_ok=target_root.exists())


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for the scaffold helper."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target_root", help="Path for the new initiative root")
    parser.add_argument(
        "--template-root",
        default=str(DEFAULT_TEMPLATE_ROOT),
        help="Template directory to copy from",
    )
    parser.add_argument("--initiative-name", help="Display name written into the scaffold")
    parser.add_argument("--owner", help="Initiative owner")
    parser.add_argument(
        "--phase",
        default="discovery-and-research",
        help="Initial initiative phase",
    )
    parser.add_argument(
        "--gate-state",
        default="blocked",
        choices=["pass", "fail", "blocked"],
        help="Initial initiative gate state",
    )
    parser.add_argument(
        "--roadmap-status",
        default="template-copied-roadmap-not-yet-adapted",
        help="Initial roadmap status string",
    )
    parser.add_argument(
        "--validation-commands",
        help="Repository-specific validation commands to inject into README.md",
    )
    parser.add_argument(
        "--evidence-pointers",
        help="Repository-specific evidence path notes to inject into README.md",
    )
    parser.add_argument(
        "--current-step",
        default="adapt-the-scaffold-and-replace-the-prd-placeholders",
        help="Initial roadmap current step",
    )
    parser.add_argument(
        "--next-action",
        default="replace-prd-placeholders-then-generate-the-final-roadmap-and-sprint-set",
        help="Initial roadmap next action",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and report what would happen without writing files",
    )
    return parser


def main() -> int:
    """Execute the scaffold helper."""

    parser = build_parser()
    args = parser.parse_args()

    template_root = Path(args.template_root).resolve()
    target_root = Path(args.target_root).resolve()

    if not template_root.exists() or not template_root.is_dir():
        parser.error(f"Template root does not exist: {template_root.as_posix()}")

    try:
        ensure_target_is_safe(target_root)
    except ValueError as exc:
        parser.exit(1, f"{exc}\n")

    replacements = build_placeholder_map(args, target_root)

    if args.dry_run:
        print(f"dry-run: scaffold would be copied from {template_root.as_posix()}")
        print(f"dry-run: target root would be {target_root.as_posix()}")
        print(f"dry-run: {len(replacements)} placeholders would be rendered")
        return 0

    copy_scaffold(template_root, target_root)
    render_placeholders(target_root, replacements)

    print(f"scaffolded initiative at {target_root.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())