#!/usr/bin/env python3
"""Manage the repository initiative workflow under ./.ub-workflows."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path
import re
import shutil

# region Constants

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INITIATIVE_TEMPLATE_ROOT = SKILL_ROOT / "assets" / "initiative-template"
DEFAULT_OPERATIONS_TEMPLATE_ROOT = SKILL_ROOT / "assets" / "operations-root"
DEFAULT_OPS_ROOT = Path(".ub-workflows")
TEXT_FILE_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
}
KNOWN_COMMANDS           = {"create", "init-sprints", "archive"}
ACTIVE_INITIATIVE_HEADING = "## Active Initiative Roots"
OPERATIONS_INDEX_FILES   = {"AGENTS.md", "README.md", "operation-guide.md", "user-guide.md"}
SPRINT_PATH_PATTERN      = re.compile(r"^\s*-\s+Path:\s+`?(.+?sprint\.md)`?\s*$")
SPRINT_ENTRY_PATTERN     = re.compile(r"^\s*-\s+\[[ xX]\]\s+(.+?)\s*$")

# endregion Constants


# region Path And Text Helpers

def derive_initiative_name(target_root: Path) -> str:
    """Derive a readable initiative name from a dated or plain directory name."""

    parts = [part for part in target_root.name.split("-") if part]
    if len(parts) >= 4 and all(part.isdigit() for part in parts[:3]):
        parts = parts[3:]
    if not parts:
        return target_root.name
    return " ".join(parts).replace("_", " ").title()


def normalize_path(value: Path) -> str:
    """Return a stable slash-based path string for generated files."""

    current_root = Path.cwd().resolve()
    try:
        return value.resolve().relative_to(current_root).as_posix()
    except ValueError:
        return value.resolve().as_posix()


def slugify(value: str) -> str:
    """Convert freeform text into a stable initiative slug."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = slug.strip("-")
    return slug or "initiative"


def dated_directory_name(raw_value: str, stamp: str) -> str:
    """Return a dated initiative directory name from a slug or dated slug."""

    candidate = raw_value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}-.+", candidate):
        return slugify(candidate[:10]) + "-" + slugify(candidate[11:])
    return f"{stamp}-{slugify(candidate)}"


def slug_source_name(source_path: Path) -> str:
    """Return a slug basis derived from a source PRD filename."""

    return source_path.stem


def replace_markdown_section(text: str, heading: str, body: str) -> str:
    """Replace or append a Markdown section body under a heading."""

    pattern = re.compile(rf"(?ms)^({re.escape(heading)}\n\n)(.*?)(?=^##\s|\Z)")
    if pattern.search(text):
        return pattern.sub(lambda match: f"{match.group(1)}{body}\n\n", text)
    suffix = "" if text.endswith("\n") else "\n"
    return f"{text}{suffix}\n{heading}\n\n{body}\n"


def update_markdown_table_value(text: str, field: str, value: str) -> str:
    """Update a single Markdown table row by field name."""

    lines = text.splitlines()
    updated_lines: list[str] = []
    for line in lines:
        match = re.match(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", line)
        if match and match.group(1).strip() == field:
            updated_lines.append(f"| {field:<21} | {value} |")
            continue
        updated_lines.append(line)
    return "\n".join(updated_lines) + ("\n" if text.endswith("\n") else "")


def read_markdown_table_value(text: str, field: str) -> str | None:
    """Return a Markdown table value by field name when present."""

    for line in text.splitlines():
        match = re.match(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", line)
        if match and match.group(1).strip() == field:
            return match.group(2).strip()
    return None


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

# endregion Path And Text Helpers


# region Filesystem Helpers

def ensure_directory_is_safe(target_root: Path) -> None:
    """Reject writes against populated directories to avoid clobbering work."""

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


def copy_tree(source: Path, destination: Path) -> None:
    """Copy a template tree into the destination directory."""

    shutil.copytree(source, destination, dirs_exist_ok=destination.exists())


def determine_target_root(args: argparse.Namespace) -> Path:
    """Resolve the new initiative root from a slug or explicit path."""

    if args.target:
        raw_target = args.target.strip()
        candidate = Path(raw_target)
        if candidate.is_absolute() or len(candidate.parts) > 1 or raw_target.startswith("."):
            return candidate.resolve()
        directory_name = dated_directory_name(raw_target, args.date)
        return (Path(args.ops_root).resolve() / "initiatives" / directory_name).resolve()

    if not args.initiative_name:
        if not args.prd_source:
            raise ValueError("Provide either a target slug/path, --initiative-name, or --prd-source.")
        directory_name = dated_directory_name(slug_source_name(Path(args.prd_source)), args.date)
        return (Path(args.ops_root).resolve() / "initiatives" / directory_name).resolve()
    directory_name = dated_directory_name(args.initiative_name, args.date)
    return (Path(args.ops_root).resolve() / "initiatives" / directory_name).resolve()


def build_active_initiative_list(ops_root: Path) -> str:
    """Return the numbered active-initiative list for the operations root README."""

    initiatives_root = ops_root / "initiatives"
    initiatives = sorted(
        path.name for path in initiatives_root.iterdir() if path.is_dir()
    ) if initiatives_root.exists() else []
    if not initiatives:
        return "1. `none`"
    return "\n".join(
        f"{index}. `initiatives/{name}`"
        for index, name in enumerate(initiatives, start=1)
    )


def sync_ops_root_readme(ops_root: Path, template_root: Path) -> None:
    """Synchronize the active initiative listing in the operations root README."""

    readme_path = ops_root / "initiatives" / "README.md"
    template_path = template_root / "README.md"
    active_list = build_active_initiative_list(ops_root)
    if readme_path.exists():
        text = readme_path.read_text(encoding="utf-8")
    else:
        text = template_path.read_text(encoding="utf-8")
    updated = text.replace("REPLACE_ACTIVE_INITIATIVE_ROOTS", active_list)
    updated = replace_markdown_section(updated, ACTIVE_INITIATIVE_HEADING, active_list)
    readme_path.write_text(updated, encoding="utf-8")


def ensure_operations_root(
    ops_root: Path,
    operations_template_root: Path,
    initiative_template_root: Path,
) -> None:
    """Bootstrap the repository operations root when it is missing or partial."""

    ops_root.mkdir(parents=True, exist_ok=True)
    initiatives_root = ops_root / "initiatives"
    initiatives_root.mkdir(parents=True, exist_ok=True)
    for child in operations_template_root.iterdir():
        if child.name == "template-copy-helper.md":
            continue
        destination_root = initiatives_root if child.name in OPERATIONS_INDEX_FILES else ops_root
        destination = destination_root / child.name
        if destination.exists():
            continue
        if child.is_dir():
            copy_tree(child, destination)
            continue
        shutil.copy2(child, destination)

    (ops_root / "archive").mkdir(parents=True, exist_ok=True)

    sync_ops_root_readme(ops_root, operations_template_root)

# endregion Filesystem Helpers


# region Create Initiative

def build_initiative_placeholder_map(
    args: argparse.Namespace,
    target_root: Path,
    prd_source: Path | None,
) -> dict[str, str]:
    """Build replacements for a newly created initiative root."""

    initiative_name = args.initiative_name or derive_initiative_name(target_root)
    gate_state = args.gate_state
    if args.prd_imported and gate_state == "blocked":
        gate_state = "pass"
    has_prd_source = prd_source is not None
    validation_note = (
        "The source PRD was copied into `./prd.md` as-is. Review or refine it until `prd_ready: pass`, then generate a durable `roadmap.md` before any sprint directories are initialized."
        if has_prd_source and not args.prd_imported
        else (
            "The master PRD is imported and ready for roadmap planning. Generate the full ordered roadmap next, review it, and set `roadmap_ready: pass` before running `init-sprints`."
            if args.prd_imported
            else "This initiative has been scaffolded but `./prd.md` still needs the real master PRD before roadmap generation can begin."
        )
    )
    next_action = (
        "Review or refine `./prd.md`, then generate `roadmap.md`. Do not initialize sprint directories until `roadmap_ready: pass`."
        if has_prd_source and not args.prd_imported
        else (
            "Generate `roadmap.md` from `./prd.md`, review it, and set `roadmap_ready: pass` before initializing any sprint directories under `./sprints/`."
            if args.prd_imported
            else "Import the master PRD into `./prd.md`, then generate and approve `roadmap.md` before initializing any sprint directories under `./sprints/`."
        )
    )

    return {
        "REPLACE_INITIATIVE_NAME" : initiative_name,
        "REPLACE_INITIATIVE_ROOT" : normalize_path(target_root),
        "REPLACE_IMPORTED_ON"     : args.date,
        "REPLACE_GOVERNANCE_BRIDGE": "`Level 0`",
        "REPLACE_GOVERNANCE_PROFILE": "`not applicable`",
        "REPLACE_PHASE"           : (
            args.phase
            or (
                "PRD imported, awaiting roadmap planning"
                if args.prd_imported
                else (
                    "PRD copied, awaiting review and roadmap planning"
                    if has_prd_source
                    else "Template scaffolded, awaiting PRD import"
                )
            )
        ),
        "REPLACE_GATE_STATE"      : (
            f"`prd_ready: {gate_state}`"
            if ":" not in gate_state
            else gate_state
        ),
        "REPLACE_ROADMAP_STATUS"  : f"`{args.roadmap_status}`",
        "REPLACE_NEXT_ACTION"     : args.next_action or next_action,
        "REPLACE_OWNER"           : args.owner or "unassigned",
        "REPLACE_VALIDATION_BASELINE": validation_note,
        "REPLACE_DOCUMENTATION_STATUS": "To be confirmed during roadmap planning, sprint execution, and final audit.",
        "REPLACE_EXCEPTION_POINTERS": "`none`",
        "REPLACE_CURRENT_SPRINT"  : "`none`",
        "REPLACE_LAST_COMPLETED"  : "`none`",
        "REPLACE_BLOCKERS"        : "`none`",
        "REPLACE_CURRENT_STATUS"  : "not started",
        "REPLACE_NEXT_SPRINT"     : "`define after roadmap approval`",
        "REPLACE_RESUME_FROM"     : "`review or generate roadmap from ./prd.md`",
    }


def resolve_prd_source(prd_source: str | None) -> Path | None:
    """Resolve and validate an optional source PRD path."""

    if not prd_source:
        return None
    source_path = Path(prd_source).resolve()
    if not source_path.exists() or not source_path.is_file():
        raise ValueError(f"Source PRD does not exist: {source_path.as_posix()}")
    return source_path


def command_create(args: argparse.Namespace) -> int:
    """Create a new initiative root under the repository operations tree."""

    initiative_template_root = Path(args.template_root).resolve()
    operations_template_root = Path(args.operations_template_root).resolve()
    ops_root = Path(args.ops_root).resolve()
    prd_source = resolve_prd_source(args.prd_source)
    target_root = determine_target_root(args)

    if not initiative_template_root.exists() or not initiative_template_root.is_dir():
        raise ValueError(f"Initiative template root does not exist: {initiative_template_root.as_posix()}")
    if not operations_template_root.exists() or not operations_template_root.is_dir():
        raise ValueError(f"Operations template root does not exist: {operations_template_root.as_posix()}")

    if args.dry_run:
        print(f"dry-run: operations root would be {ops_root.as_posix()}")
        print(f"dry-run: initiative root would be {target_root.as_posix()}")
        if prd_source is not None:
            print(f"dry-run: source PRD would be copied from {prd_source.as_posix()} to {(target_root / 'prd.md').as_posix()}")
        print("dry-run: operations root bootstrap and README sync would run if needed")
        return 0

    ensure_operations_root(ops_root, operations_template_root, initiative_template_root)
    ensure_directory_is_safe(target_root)
    copy_tree(initiative_template_root, target_root)
    render_placeholders(target_root, build_initiative_placeholder_map(args, target_root, prd_source))
    if prd_source is not None:
        shutil.copy2(prd_source, target_root / "prd.md")
    sync_ops_root_readme(ops_root, operations_template_root)

    print(f"scaffolded initiative at {target_root.as_posix()}")
    return 0

# endregion Create Initiative


# region Initialize Sprints

def roadmap_sprint_entries(roadmap_path: Path) -> list[tuple[str, Path]]:
    """Extract sprint titles and folder paths from a roadmap document."""

    text = roadmap_path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^## Sprint Sequence\n\n(.*?)(?=^##\s|\Z)", text)
    if not match:
        raise ValueError("roadmap.md is missing the Sprint Sequence section.")

    current_title: str | None = None
    entries: list[tuple[str, Path]] = []
    for line in match.group(1).splitlines():
        title_match = SPRINT_ENTRY_PATTERN.match(line)
        if title_match:
            current_title = title_match.group(1).strip()
            continue

        path_match = SPRINT_PATH_PATTERN.match(line)
        if not path_match or current_title is None:
            continue

        raw_path = path_match.group(1).strip().strip("`")
        relative = raw_path[2:] if raw_path.startswith("./") else raw_path
        sprint_file = Path(relative)
        if sprint_file.name != "sprint.md" or not sprint_file.parts or sprint_file.parts[0] != "sprints":
            continue
        entries.append((current_title, Path(*sprint_file.parts[:-1])))
        current_title = None

    if not entries:
        raise ValueError(
            "No sprint paths were found in roadmap.md. Generate the full roadmap before initializing sprints."
        )
    return entries


def ensure_sprint_directory(template_root: Path, sprint_root: Path) -> str:
    """Create or validate one sprint directory from the canonical sprint template."""

    if not sprint_root.exists():
        copy_tree(template_root, sprint_root)
        return "created"
    if not sprint_root.is_dir():
        raise ValueError(f"Sprint path exists and is not a directory: {sprint_root.as_posix()}")
    entries = list(sprint_root.iterdir())
    if not entries:
        copy_tree(template_root, sprint_root)
        return "created"

    required = {"sprint.md", "closeout.md", "evidence"}
    present = {path.name for path in entries}
    if required.issubset(present):
        return "existing"
    missing = ", ".join(sorted(required - present))
    raise ValueError(
        "Sprint directory already exists but is incomplete. "
        f"Add the missing template files or clean the directory first: {sprint_root.as_posix()} ({missing})"
    )


def refresh_initiative_readme_for_sprints(readme_path: Path, first_sprint_title: str, first_sprint_path: Path) -> None:
    """Update the initiative README after the sprint set is initialized."""

    text = readme_path.read_text(encoding="utf-8")
    updates = {
        "Current phase"        : "Roadmap approved, sprint initialization complete",
        "Current gate"         : "`roadmap_ready: pass`",
        "Roadmap status"       : "`generated`",
        "Next step"            : (
            f"Start {first_sprint_title} by opening `{normalize_path(first_sprint_path)}` and creating the first evidence and closeout entries as execution begins"
        ),
        "Active sprint"        : "`none`",
        "Last completed sprint": "`none`",
        "Blockers"             : "`none`",
    }
    for field, value in updates.items():
        text = update_markdown_table_value(text, field, value)
    text = replace_markdown_section(
        text,
        "## Validation Pointers",
        "- Validation baseline: The master PRD, full ordered roadmap, and all planned sprint folders are now in place.\n- Documentation sync status: No sprint-specific documentation updates are required yet because execution has not started.\n- Exception records: `none`",
    )
    readme_path.write_text(text, encoding="utf-8")


def replace_pattern_once(text: str, pattern: str, replacement: str) -> str:
    """Replace the first regex match or append the replacement if no match exists."""

    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count:
        return updated
    suffix = "" if text.endswith("\n") else "\n"
    return f"{text}{suffix}{replacement}\n"


def refresh_roadmap_after_sprint_init(roadmap_path: Path, first_sprint_title: str, first_sprint_path: Path) -> None:
    """Update roadmap state after all sprint directories have been initialized."""

    text = roadmap_path.read_text(encoding="utf-8")
    text = replace_pattern_once(text, r"^Status:\s+.+$", "Status: generated")
    text = text.replace(
        "- [ ] All sprint folders initialized under `./sprints/` from `./sprint-template/`",
        "- [x] All sprint folders initialized under `./sprints/` from `./sprint-template/`",
        1,
    )
    text = replace_pattern_once(text, r"^- Next sprint:\s+.+$", f"- Next sprint: `{first_sprint_title}`")
    text = replace_pattern_once(text, r"^- Resume from:\s+.+$", f"- Resume from: `{normalize_path(first_sprint_path)}`")
    roadmap_path.write_text(text, encoding="utf-8")


def validate_roadmap_ready(initiative_root: Path, roadmap_path: Path) -> list[str]:
    """Return validation errors that block sprint initialization."""

    errors: list[str] = []
    readme_path = initiative_root / "README.md"
    if not readme_path.exists():
        errors.append("README.md is missing.")
        return errors

    readme_text = readme_path.read_text(encoding="utf-8")
    current_gate = read_markdown_table_value(readme_text, "Current gate")
    normalized_gate = current_gate.strip("`") if current_gate else None
    if normalized_gate != "roadmap_ready: pass":
        errors.append("README.md must record `roadmap_ready: pass` before sprint initialization can start.")
    if unresolved_placeholder_found(roadmap_path):
        errors.append("roadmap.md still contains unresolved scaffold placeholders.")
    return errors


def command_init_sprints(args: argparse.Namespace) -> int:
    """Create the full sprint set from roadmap path entries."""

    initiative_root = Path(args.initiative_root).resolve()
    roadmap_path = initiative_root / "roadmap.md"
    sprint_template_root = initiative_root / "sprint-template"
    if not roadmap_path.exists():
        raise ValueError(f"Initiative roadmap does not exist: {roadmap_path.as_posix()}")
    if not sprint_template_root.exists():
        raise ValueError(f"Sprint template does not exist: {sprint_template_root.as_posix()}")

    readiness_errors = validate_roadmap_ready(initiative_root, roadmap_path)
    if readiness_errors:
        message = "Sprint initialization blocked because the roadmap is not ready:\n- " + "\n- ".join(readiness_errors)
        raise ValueError(message)

    entries = roadmap_sprint_entries(roadmap_path)
    if args.dry_run:
        print(f"dry-run: {len(entries)} sprint directories would be initialized under {initiative_root.as_posix()}")
        return 0

    created = 0
    first_title, first_relative = entries[0]
    for _, sprint_relative in entries:
        status = ensure_sprint_directory(sprint_template_root, initiative_root / sprint_relative)
        if status == "created":
            created += 1

    refresh_initiative_readme_for_sprints(
        initiative_root / "README.md",
        first_title,
        initiative_root / first_relative / "sprint.md",
    )
    refresh_roadmap_after_sprint_init(
        roadmap_path,
        first_title,
        initiative_root / first_relative / "sprint.md",
    )

    print(f"initialized {len(entries)} sprint directories ({created} newly created)")
    return 0

# endregion Initialize Sprints


# region Archive Initiative

def unresolved_placeholder_found(path: Path) -> bool:
    """Return True when a control file still contains obvious scaffold placeholders."""

    text = path.read_text(encoding="utf-8")
    return "REPLACE_" in text or "Replace with" in text


def overall_checklist_is_complete(roadmap_path: Path) -> bool:
    """Return True when the roadmap overall checklist has no unchecked items."""

    text = roadmap_path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^## Overall Checklist\n\n(.*?)(?=^##\s|\Z)", text)
    if not match:
        return False
    return "- [ ]" not in match.group(1)


def validate_archive_readiness(initiative_root: Path) -> list[str]:
    """Return validation errors that block archive-on-request."""

    errors: list[str] = []
    readme_path = initiative_root / "README.md"
    roadmap_path = initiative_root / "roadmap.md"
    retained_note_path = initiative_root / "retained-note.md"
    if not readme_path.exists():
        errors.append("README.md is missing.")
    if not roadmap_path.exists():
        errors.append("roadmap.md is missing.")
    if not retained_note_path.exists():
        errors.append("retained-note.md is missing.")
    if errors:
        return errors

    if not overall_checklist_is_complete(roadmap_path):
        errors.append("roadmap.md still has unchecked items in the Overall Checklist section.")
    if unresolved_placeholder_found(readme_path):
        errors.append("README.md still contains unresolved scaffold placeholders.")
    if unresolved_placeholder_found(retained_note_path):
        errors.append("retained-note.md still contains unresolved scaffold placeholders.")
    return errors


def discover_ops_root(initiative_root: Path, explicit_ops_root: str | None) -> Path:
    """Resolve the owning operations root for an initiative."""

    if explicit_ops_root:
        return Path(explicit_ops_root).resolve()
    parent = initiative_root.parent
    if parent.name != "initiatives":
        raise ValueError("Provide --ops-root when archiving an initiative outside ./initiatives/.")
    return parent.parent.resolve()


def command_archive(args: argparse.Namespace) -> int:
    """Archive a completed initiative only when explicitly requested."""

    initiative_root = Path(args.initiative_root).resolve()
    if not initiative_root.exists() or not initiative_root.is_dir():
        raise ValueError(f"Initiative root does not exist: {initiative_root.as_posix()}")

    errors = validate_archive_readiness(initiative_root)
    if errors:
        message = "Archive blocked because the initiative is not complete:\n- " + "\n- ".join(errors)
        raise ValueError(message)

    ops_root = discover_ops_root(initiative_root, args.ops_root)
    archive_root = ops_root / "archive" / initiative_root.name
    if archive_root.exists():
        raise ValueError(f"Archive destination already exists: {archive_root.as_posix()}")

    if args.dry_run:
        print(f"dry-run: initiative would be moved to {archive_root.as_posix()}")
        return 0

    archive_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(initiative_root.as_posix(), archive_root.as_posix())
    sync_ops_root_readme(ops_root, Path(args.operations_template_root).resolve())

    print(f"archived initiative to {archive_root.as_posix()}")
    return 0

# endregion Archive Initiative


# region Argument Parsing

def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for the initiative workflow helper."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a new initiative root")
    create_parser.add_argument("target", nargs="?", help="Initiative slug or explicit target path")
    create_parser.add_argument("--ops-root", default=str(DEFAULT_OPS_ROOT), help="Operations root to bootstrap and use")
    create_parser.add_argument(
        "--template-root",
        default=str(DEFAULT_INITIATIVE_TEMPLATE_ROOT),
        help="Initiative template directory to copy from",
    )
    create_parser.add_argument(
        "--operations-template-root",
        default=str(DEFAULT_OPERATIONS_TEMPLATE_ROOT),
        help="Operations-root template directory to copy from",
    )
    create_parser.add_argument("--initiative-name", help="Display name written into the scaffold")
    create_parser.add_argument("--owner", help="Initiative owner")
    create_parser.add_argument("--date", default=date.today().isoformat(), help="Date stamp used in generated paths and README state")
    create_parser.add_argument("--phase", help="Initial initiative phase")
    create_parser.add_argument(
        "--gate-state",
        default="blocked",
        help="Initial initiative gate state; plain values are wrapped as `prd_ready: <state>`",
    )
    create_parser.add_argument("--roadmap-status", default="not started", help="Initial roadmap status string")
    create_parser.add_argument("--next-action", help="Initial next-action value written into README.md")
    create_parser.add_argument(
        "--prd-source",
        help="Source PRD file to copy into the initiative root as ./prd.md",
    )
    create_parser.add_argument(
        "--prd-imported",
        action="store_true",
        help="Mark the PRD as already execution-ready after copy/import",
    )
    create_parser.add_argument("--dry-run", action="store_true", help="Report the resolved create operation without writing files")

    init_parser = subparsers.add_parser("init-sprints", help="Initialize sprint directories from roadmap paths")
    init_parser.add_argument("initiative_root", help="Initiative root containing roadmap.md and sprint-template/")
    init_parser.add_argument("--dry-run", action="store_true", help="Report sprint initialization without writing files")

    archive_parser = subparsers.add_parser("archive", help="Archive a completed initiative root")
    archive_parser.add_argument("initiative_root", help="Initiative root to archive")
    archive_parser.add_argument("--ops-root", help="Override the owning operations root")
    archive_parser.add_argument(
        "--operations-template-root",
        default=str(DEFAULT_OPERATIONS_TEMPLATE_ROOT),
        help="Operations-root template directory used to sync README.md after archive",
    )
    archive_parser.add_argument("--dry-run", action="store_true", help="Report the archive move without writing files")

    return parser


def rewrite_legacy_arguments(argv: Sequence[str]) -> list[str]:
    """Keep the original single-argument create invocation working."""

    if len(argv) < 2:
        return list(argv)
    command = argv[1]
    if command in KNOWN_COMMANDS or command.startswith("-"):
        return list(argv)
    return [argv[0], "create", *argv[1:]]


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the initiative workflow helper."""

    raw_argv = list(argv) if argv is not None else None
    adjusted_argv = rewrite_legacy_arguments(raw_argv or __import__("sys").argv)
    parser = build_parser()
    args = parser.parse_args(adjusted_argv[1:])

    try:
        if args.command == "create":
            return command_create(args)
        if args.command == "init-sprints":
            return command_init_sprints(args)
        if args.command == "archive":
            return command_archive(args)
    except ValueError as exc:
        parser.exit(1, f"{exc}\n")

    parser.print_help()
    return 1

# endregion Argument Parsing


if __name__ == "__main__":
    raise SystemExit(main())
