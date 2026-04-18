#!/usr/bin/env python3
"""Manage the repository initiative workflow under ./.ub-workflows."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil

# region Constants

SKILL_ROOT                    = Path(__file__).resolve().parents[1]
DEFAULT_INITIATIVE_TEMPLATE_ROOT = SKILL_ROOT / "assets" / "initiative-template"
CANONICAL_SPRINT_TEMPLATE_ROOT   = DEFAULT_INITIATIVE_TEMPLATE_ROOT / "sprint-template"
DEFAULT_OPERATIONS_TEMPLATE_ROOT = SKILL_ROOT / "assets" / "operations-root"
DEFAULT_SPEC_TEMPLATE_ROOT       = SKILL_ROOT / "assets" / "lightweight-spec-template"
DEFAULT_OPS_ROOT                 = Path(".ub-workflows")
TEXT_FILE_SUFFIXES               = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
}
KNOWN_COMMANDS            = {"create", "create-spec", "prepare-sprints", "init-sprints", "archive"}
ACTIVE_INITIATIVE_HEADING = "## Active Initiative Roots"
ACTIVE_SPEC_HEADING       = "## Active Lightweight Specs"
OPERATIONS_INDEX_FILES    = {"AGENTS.md", "README.md", "operation-guide.md", "user-guide.md"}
SPRINT_ENTRY_PATTERN      = re.compile(r"^-\s+\[[ xX]\]\s+(.+?)\s*$")
SPRINT_SUBTASK_PATTERN    = re.compile(r"^\s+-\s+\[[ xX]\]\s+(.+?)\s*$")
SPRINT_PATH_PATTERN       = re.compile(r"^\s+-\s+Path:\s+`?(.+?sprint\.md)`?\s*$")
SPRINT_GOAL_PATTERN       = re.compile(r"^\s+-\s+Goal:\s+(.+?)\s*$")
SPRINT_DEPENDS_PATTERN    = re.compile(r"^\s+-\s+Depends on:\s+(.+?)\s*$")
SPRINT_VALIDATION_PATTERN = re.compile(r"^\s+-\s+Validation focus:\s+(.+?)\s*$")
SPRINT_EVIDENCE_PATTERN   = re.compile(r"^\s+-\s+Evidence folder:\s+`?(.+?)`?\s*$")
PENDING_HANDOFF_PREFIX    = "PENDING_HANDOFF:"
LEGACY_SPRINT_INIT_UNCHECKED = "- [ ] All sprint folders initialized under `./sprints/` from `./sprint-template/`"
LEGACY_SPRINT_INIT_CHECKED   = "- [x] All sprint folders initialized under `./sprints/` from `./sprint-template/`"
SPRINT_INIT_UNCHECKED        = (
    "- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template"
)
SPRINT_INIT_CHECKED          = (
    "- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template"
)

# endregion Constants


@dataclass(frozen=True)
class RoadmapSprintEntry:
    """Structured sprint metadata extracted from roadmap.md."""

    title: str
    sprint_root: Path
    sprint_file: Path
    goal: str
    depends_on: str
    validation_focus: str
    evidence_folder: str
    subtasks: tuple[str, ...]


@dataclass(frozen=True)
class PlaceholderFinding:
    """One unresolved generated-artifact placeholder finding."""

    initiative_root: Path
    file_path: Path
    line_number: int
    category: str
    severity: str
    marker: str
    line_text: str


# region Path And Text Helpers

MACHINE_PLACEHOLDER_PATTERN = re.compile(r"\bREPLACE_[A-Z0-9_]+\b")
HUMAN_PLACEHOLDER_PATTERN = re.compile(r"Replace with\b")
HUMAN_PLACEHOLDER_PROMPT_PATTERN = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)?(?:\[[ xX]\]\s+)?Replace with\b")
CODE_FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")


def generated_artifact_role(initiative_root: Path, path: Path) -> str | None:
    """Classify one generated workflow artifact path."""

    try:
        relative = path.resolve().relative_to(initiative_root.resolve())
    except ValueError:
        return None

    if relative == Path("README.md"):
        return "readme"
    if relative == Path("roadmap.md"):
        return "roadmap"
    if relative == Path("spec.md"):
        return "lightweight-spec"
    if relative == Path("prd.md"):
        return "prd"
    if relative == Path("rollup.md"):
        return "rollup"
    if relative == Path("retained-note.md"):
        return "retained-note"
    if len(relative.parts) == 3 and relative.parts[0] == "sprints" and relative.parts[2] == "sprint.md":
        return "sprint"
    if len(relative.parts) == 3 and relative.parts[0] == "sprints" and relative.parts[2] == "decision-log.md":
        return "decision-log"
    if len(relative.parts) == 3 and relative.parts[0] == "sprints" and relative.parts[2] == "closeout.md":
        return "closeout"
    return None


def generated_artifact_paths(initiative_root: Path) -> list[Path]:
    """Return the generated workflow artifacts covered by placeholder checks."""

    spec_path = initiative_root / "spec.md"
    if spec_path.exists() and spec_path.is_file():
        return [spec_path]

    candidates = [
        initiative_root / "README.md",
        initiative_root / "roadmap.md",
        initiative_root / "prd.md",
        initiative_root / "rollup.md",
        initiative_root / "retained-note.md",
    ]
    sprints_root = initiative_root / "sprints"
    if sprints_root.exists():
        for sprint_root in sorted(path for path in sprints_root.iterdir() if path.is_dir()):
            candidates.append(sprint_root / "sprint.md")
            candidates.append(sprint_root / "decision-log.md")
            candidates.append(sprint_root / "closeout.md")
    return [path for path in candidates if path.exists() and path.is_file()]


def human_placeholder_is_required(initiative_root: Path, path: Path) -> bool:
    """Return True when a plain-language placeholder blocks this generated artifact."""

    return generated_artifact_role(initiative_root, path) in {"roadmap", "sprint", "lightweight-spec"}


def required_placeholder_markers(text: str, path: Path, initiative_root: Path) -> tuple[str, ...]:
    """Return required placeholder markers for one generated artifact."""

    markers = list(dict.fromkeys(MACHINE_PLACEHOLDER_PATTERN.findall(text)))
    if human_placeholder_is_required(initiative_root, path) and HUMAN_PLACEHOLDER_PATTERN.search(text):
        markers.append("Replace with")
    return tuple(markers)


def collect_placeholder_findings(initiative_root: Path) -> list[PlaceholderFinding]:
    """Collect required and advisory placeholder findings for one initiative root."""

    findings: list[PlaceholderFinding] = []
    for path in generated_artifact_paths(initiative_root):
        text = path.read_text(encoding="utf-8")
        is_required_human_prompt = human_placeholder_is_required(initiative_root, path)
        in_code_fence = False
        for line_number, line in enumerate(text.splitlines(), start=1):
            if CODE_FENCE_PATTERN.match(line):
                in_code_fence = not in_code_fence
                continue
            if in_code_fence:
                continue
            findings.extend(
                PlaceholderFinding(
                    initiative_root=initiative_root,
                    file_path=path,
                    line_number=line_number,
                    category="machine-token",
                    severity="required",
                    marker=marker,
                    line_text=line.strip(),
                )
                for marker in MACHINE_PLACEHOLDER_PATTERN.findall(line)
            )
            if HUMAN_PLACEHOLDER_PROMPT_PATTERN.search(line):
                findings.append(
                    PlaceholderFinding(
                        initiative_root=initiative_root,
                        file_path=path,
                        line_number=line_number,
                        category="human-prompt",
                        severity=("required" if is_required_human_prompt else "advisory"),
                        marker="Replace with",
                        line_text=line.strip(),
                    )
                )
            if PENDING_HANDOFF_PREFIX in line:
                findings.append(
                    PlaceholderFinding(
                        initiative_root=initiative_root,
                        file_path=path,
                        line_number=line_number,
                        category="pending-handoff",
                        severity="advisory",
                        marker=PENDING_HANDOFF_PREFIX,
                        line_text=line.strip(),
                    )
                )
    return findings


def format_placeholder_summary(initiative_root: Path, findings: Sequence[PlaceholderFinding]) -> str:
    """Return a deterministic text summary for generated-output placeholder findings."""

    required_count = sum(1 for finding in findings if finding.severity == "required")
    advisory_count = len(findings) - required_count
    if not findings:
        return f"placeholder summary: no unresolved generated-artifact placeholders under {initiative_root.as_posix()}"

    lines = [
        (
            "placeholder summary: "
            f"{required_count} required, {advisory_count} advisory finding(s) under {initiative_root.as_posix()}"
        )
    ]
    for finding in findings:
        relative = finding.file_path.resolve().relative_to(initiative_root.resolve()).as_posix()
        lines.append(
            f"- {finding.severity} {finding.category}: {relative}:{finding.line_number} -> {finding.marker}"
        )
    return "\n".join(lines)


def report_generated_placeholder_state(initiative_root: Path, *, strict: bool) -> None:
    """Print generated-output placeholder findings and optionally fail on required ones."""

    findings = collect_placeholder_findings(initiative_root)
    summary = format_placeholder_summary(initiative_root, findings)
    print(summary)
    if strict and any(finding.severity == "required" for finding in findings):
        raise ValueError(
            "Generated workflow output still contains required unresolved placeholders:\n"
            f"{summary}"
        )


def generated_roots_in_directory(root: Path) -> list[Path]:
    """Return sorted generated workflow roots inside one container directory."""

    if not root.exists() or not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir())


def discover_generated_roots_for_placeholder_scan(scan_root: Path) -> list[Path]:
    """Resolve one or more generated workflow roots from a scan target."""

    resolved = scan_root.resolve()
    if (resolved / "spec.md").exists():
        return [resolved]
    if (resolved / "README.md").exists() and (resolved / "roadmap.md").exists():
        return [resolved]
    if resolved.name == "initiatives" and resolved.is_dir():
        return generated_roots_in_directory(resolved)
    if resolved.name == "specs" and resolved.is_dir():
        return generated_roots_in_directory(resolved)
    if resolved.name == ".ub-workflows" and resolved.is_dir():
        return sorted(
            [
                *generated_roots_in_directory(resolved / "initiatives"),
                *generated_roots_in_directory(resolved / "specs"),
            ]
        )
    if (resolved / ".ub-workflows").is_dir():
        return discover_generated_roots_for_placeholder_scan(resolved / ".ub-workflows")
    raise ValueError(
        "Placeholder scan target must be a workflow root, an initiatives directory, "
        "a specs directory, a .ub-workflows root, or a repository root containing "
        "./.ub-workflows/initiatives/ or ./.ub-workflows/specs/."
    )


def discover_initiative_roots_for_placeholder_scan(scan_root: Path) -> list[Path]:
    """Backward-compatible alias for generated workflow root discovery."""

    return discover_generated_roots_for_placeholder_scan(scan_root)

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


def strip_wrapping_backticks(value: str) -> str:
    """Return a field value without surrounding Markdown code ticks."""

    stripped = value.strip()
    if stripped.startswith("`") and stripped.endswith("`") and len(stripped) >= 2:
        return stripped[1:-1].strip()
    return stripped


def replace_markdown_section(text: str, heading: str, body: str) -> str:
    """Replace or append a Markdown section body under a heading."""

    pattern = re.compile(rf"(?ms)^({re.escape(heading)}\n\n)(.*?)(?=^##\s|\Z)")
    if pattern.search(text):
        return pattern.sub(lambda match: f"{match.group(1)}{body}\n\n", text)
    suffix = "" if text.endswith("\n") else "\n"
    return f"{text}{suffix}\n{heading}\n\n{body}\n"


def update_markdown_table_value(text: str, field: str, value: str) -> str:
    """Update a single Markdown table or bullet-list status row by field name."""

    lines = text.splitlines()
    updated_lines: list[str] = []
    for line in lines:
        match = re.match(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", line)
        if match and match.group(1).strip() == field:
            updated_lines.append(f"| {field:<21} | {value} |")
            continue
        bullet_match = re.match(r"^-\s+(.+?):\s+(.+?)\s*$", line)
        if bullet_match and bullet_match.group(1).strip() == field:
            updated_lines.append(f"- {field}: {value}")
            continue
        updated_lines.append(line)
    return "\n".join(updated_lines) + ("\n" if text.endswith("\n") else "")


def read_markdown_table_value(text: str, field: str) -> str | None:
    """Return a Markdown table or bullet-list value by field name when present."""

    for line in text.splitlines():
        match = re.match(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", line)
        if match and match.group(1).strip() == field:
            return match.group(2).strip()
        bullet_match = re.match(r"^-\s+(.+?):\s+(.+?)\s*$", line)
        if bullet_match and bullet_match.group(1).strip() == field:
            return bullet_match.group(2).strip()
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


def render_text_placeholders(text: str, replacements: Mapping[str, str]) -> str:
    """Render a placeholder map against an in-memory template string."""

    updated = text
    for placeholder, value in replacements.items():
        updated = updated.replace(placeholder, value)
    return updated


def find_blocking_placeholders(text: str) -> tuple[str, ...]:
    """Return placeholder markers that still block execution readiness."""

    markers: list[str] = []
    markers.extend(dict.fromkeys(MACHINE_PLACEHOLDER_PATTERN.findall(text)))
    if HUMAN_PLACEHOLDER_PATTERN.search(text):
        markers.append("Replace with")
    return tuple(markers)


def find_pending_handoff_markers(text: str) -> tuple[str, ...]:
    """Return allowed pending handoff markers from generated sprint text."""

    return tuple(
        line.strip()
        for line in text.splitlines()
        if PENDING_HANDOFF_PREFIX in line
    )


def sprint_document_has_blocking_placeholders(path: Path) -> bool:
    """Return True when a sprint document still contains blocking placeholders."""

    initiative_root = path.parents[2]
    text = path.read_text(encoding="utf-8")
    return bool(required_placeholder_markers(text, path, initiative_root))

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


def copy_initiative_template(source: Path, destination: Path) -> None:
    """Copy initiative control files while keeping sprint seeding internal."""

    destination.mkdir(parents=True, exist_ok=True)
    for child in sorted(source.iterdir()):
        if child.name == "sprint-template":
            continue
        target = destination / child.name
        if child.is_dir():
            copy_tree(child, target)
            continue
        shutil.copy2(child, target)


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


def determine_spec_target_root(args: argparse.Namespace) -> Path:
    """Resolve the new lightweight spec root from a slug or explicit path."""

    if args.target:
        raw_target = args.target.strip()
        candidate = Path(raw_target)
        if candidate.is_absolute() or len(candidate.parts) > 1 or raw_target.startswith("."):
            return candidate.resolve()
        directory_name = dated_directory_name(raw_target, args.date)
        return (Path(args.ops_root).resolve() / "specs" / directory_name).resolve()

    if not args.spec_name:
        raise ValueError("Provide either a target slug/path or --spec-name.")
    directory_name = dated_directory_name(args.spec_name, args.date)
    return (Path(args.ops_root).resolve() / "specs" / directory_name).resolve()


def build_active_root_list(ops_root: Path, root_name: str) -> str:
    """Return one numbered active-root list for the operations root README."""

    active_root = ops_root / root_name
    active_items = sorted(
        path.name for path in active_root.iterdir() if path.is_dir()
    ) if active_root.exists() else []
    if not active_items:
        return "1. `none`"
    return "\n".join(
        f"{index}. `{root_name}/{name}`"
        for index, name in enumerate(active_items, start=1)
    )


def sync_ops_root_readme(ops_root: Path, template_root: Path) -> None:
    """Synchronize the active workflow listings in the operations root README."""

    readme_path = ops_root / "initiatives" / "README.md"
    template_path = template_root / "README.md"
    active_initiatives = build_active_root_list(ops_root, "initiatives")
    active_specs = build_active_root_list(ops_root, "specs")
    if readme_path.exists():
        text = readme_path.read_text(encoding="utf-8")
    else:
        text = template_path.read_text(encoding="utf-8")
    updated = text.replace("REPLACE_ACTIVE_INITIATIVE_ROOTS", active_initiatives)
    updated = text.replace("REPLACE_ACTIVE_LIGHTWEIGHT_SPECS", active_specs)
    updated = replace_markdown_section(updated, ACTIVE_INITIATIVE_HEADING, active_initiatives)
    updated = replace_markdown_section(updated, ACTIVE_SPEC_HEADING, active_specs)
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
    specs_root = ops_root / "specs"
    specs_root.mkdir(parents=True, exist_ok=True)
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
            "The master PRD is imported and ready for roadmap planning. Generate the full ordered roadmap next, review it, and set `roadmap_ready: pass` before running `prepare-sprints` or `init-sprints`."
            if args.prd_imported
            else "This initiative has been scaffolded but `./prd.md` still needs the real master PRD before roadmap generation can begin."
        )
    )
    next_action = (
        "Review or refine `./prd.md`, then generate `roadmap.md`. Do not initialize sprint directories until `roadmap_ready: pass`."
        if has_prd_source and not args.prd_imported
        else (
            "Generate `roadmap.md` from `./prd.md`, review it, and set `roadmap_ready: pass` before preparing or initializing any sprint artifacts under `./sprints/`."
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
    copy_initiative_template(initiative_template_root, target_root)
    render_placeholders(target_root, build_initiative_placeholder_map(args, target_root, prd_source))
    if prd_source is not None:
        shutil.copy2(prd_source, target_root / "prd.md")
    sync_ops_root_readme(ops_root, operations_template_root)

    print(f"scaffolded initiative at {target_root.as_posix()}")
    report_generated_placeholder_state(target_root, strict=args.strict_placeholders)
    return 0

# endregion Create Initiative


# region Create Lightweight Spec

def build_spec_placeholder_map(args: argparse.Namespace, target_root: Path) -> dict[str, str]:
    """Build replacements for a newly created lightweight spec root."""

    spec_name = args.spec_name or derive_initiative_name(target_root)
    status = args.status if args.status.startswith("`") else f"`{args.status}`"
    next_action = (
        args.next_action
        or "Review `./spec.md`, resolve the remaining placeholders, then decide whether to execute it directly or promote it into a full initiative."
    )
    return {
        "REPLACE_SPEC_NAME"   : spec_name,
        "REPLACE_SPEC_ROOT"   : normalize_path(target_root),
        "REPLACE_CREATED_ON"  : args.date,
        "REPLACE_OWNER"       : args.owner or "unassigned",
        "REPLACE_SPEC_STATUS" : status,
        "REPLACE_NEXT_ACTION" : next_action,
    }


def command_create_spec(args: argparse.Namespace) -> int:
    """Create a new lightweight spec root under the repository operations tree."""

    spec_template_root = Path(args.template_root).resolve()
    operations_template_root = Path(args.operations_template_root).resolve()
    ops_root = Path(args.ops_root).resolve()
    target_root = determine_spec_target_root(args)

    if not spec_template_root.exists() or not spec_template_root.is_dir():
        raise ValueError(f"Lightweight spec template root does not exist: {spec_template_root.as_posix()}")
    if not operations_template_root.exists() or not operations_template_root.is_dir():
        raise ValueError(f"Operations template root does not exist: {operations_template_root.as_posix()}")

    if args.dry_run:
        print(f"dry-run: operations root would be {ops_root.as_posix()}")
        print(f"dry-run: lightweight spec root would be {target_root.as_posix()}")
        print("dry-run: operations root bootstrap and README sync would run if needed")
        return 0

    ensure_operations_root(ops_root, operations_template_root, DEFAULT_INITIATIVE_TEMPLATE_ROOT)
    ensure_directory_is_safe(target_root)
    copy_tree(spec_template_root, target_root)
    render_placeholders(target_root, build_spec_placeholder_map(args, target_root))
    sync_ops_root_readme(ops_root, operations_template_root)

    print(f"scaffolded lightweight spec at {target_root.as_posix()}")
    report_generated_placeholder_state(target_root, strict=args.strict_placeholders)
    return 0

# endregion Create Lightweight Spec


# region Initialize Sprints

def roadmap_sprint_entries(roadmap_path: Path) -> list[RoadmapSprintEntry]:
    """Extract structured sprint metadata from a roadmap document."""

    text = roadmap_path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^## Sprint Sequence\n\n(.*?)(?=^##\s|\Z)", text)
    if not match:
        raise ValueError("roadmap.md is missing the Sprint Sequence section.")

    current_title: str | None = None
    current_data: dict[str, object] = {}
    in_subtasks = False
    active_field: str | None = None
    entries: list[RoadmapSprintEntry] = []

    def finalize_current() -> None:
        nonlocal current_title, current_data, in_subtasks, active_field
        if current_title is None:
            return

        sprint_root = current_data.get("sprint_root")
        if not isinstance(sprint_root, Path):
            raise ValueError(f"Roadmap sprint entry is missing a valid path: {current_title}")

        goal = str(current_data.get("goal", "No explicit roadmap goal recorded.")).strip()
        depends_on = str(current_data.get("depends_on", "`none`")).strip()
        validation_focus = str(
            current_data.get("validation_focus", "No explicit validation focus recorded.")
        ).strip()
        evidence_folder = str(
            current_data.get("evidence_folder", f"./{(sprint_root / 'evidence').as_posix()}")
        ).strip()
        subtasks = tuple(current_data.get("subtasks", []))
        if not subtasks:
            subtasks = ("No subtasks were listed in roadmap.md.",)

        entries.append(
            RoadmapSprintEntry(
                title=current_title,
                sprint_root=sprint_root,
                sprint_file=sprint_root / "sprint.md",
                goal=strip_wrapping_backticks(goal),
                depends_on=strip_wrapping_backticks(depends_on),
                validation_focus=strip_wrapping_backticks(validation_focus),
                evidence_folder=strip_wrapping_backticks(evidence_folder),
                subtasks=tuple(strip_wrapping_backticks(item) for item in subtasks),
            )
        )
        current_title = None
        current_data = {}
        in_subtasks = False
        active_field = None

    for line in match.group(1).splitlines():
        title_match = SPRINT_ENTRY_PATTERN.match(line)
        if title_match:
            finalize_current()
            current_title = title_match.group(1).strip()
            current_data = {"subtasks": []}
            in_subtasks = False
            active_field = None
            continue

        if current_title is None:
            continue

        stripped = line.strip()
        if not stripped:
            continue

        path_match = SPRINT_PATH_PATTERN.match(line)
        if path_match:
            raw_path = strip_wrapping_backticks(path_match.group(1))
            relative = raw_path.removeprefix("./")
            sprint_file = Path(relative)
            if sprint_file.name == "sprint.md" and sprint_file.parts and sprint_file.parts[0] == "sprints":
                current_data["sprint_root"] = Path(*sprint_file.parts[:-1])
            in_subtasks = False
            active_field = None
            continue

        goal_match = SPRINT_GOAL_PATTERN.match(line)
        if goal_match:
            current_data["goal"] = goal_match.group(1)
            in_subtasks = False
            active_field = "goal"
            continue

        depends_match = SPRINT_DEPENDS_PATTERN.match(line)
        if depends_match:
            current_data["depends_on"] = depends_match.group(1)
            in_subtasks = False
            active_field = "depends_on"
            continue

        validation_match = SPRINT_VALIDATION_PATTERN.match(line)
        if validation_match:
            current_data["validation_focus"] = validation_match.group(1)
            in_subtasks = False
            active_field = "validation_focus"
            continue

        evidence_match = SPRINT_EVIDENCE_PATTERN.match(line)
        if evidence_match:
            current_data["evidence_folder"] = evidence_match.group(1)
            in_subtasks = False
            active_field = "evidence_folder"
            continue

        if stripped == "- Subtasks:":
            in_subtasks = True
            active_field = None
            continue

        if in_subtasks:
            subtask_match = SPRINT_SUBTASK_PATTERN.match(line)
            if subtask_match:
                current_data.setdefault("subtasks", []).append(subtask_match.group(1).strip())
                continue
            subtasks = current_data.get("subtasks", [])
            if isinstance(subtasks, list) and subtasks and not stripped.startswith("-"):
                subtasks[-1] = f"{subtasks[-1]} {stripped}".strip()
                continue
            in_subtasks = False

        if active_field is not None and not stripped.startswith("-"):
            existing = str(current_data.get(active_field, "")).strip()
            current_data[active_field] = f"{existing} {stripped}".strip()
            continue

        active_field = None

    finalize_current()

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
        synced = False
        for template_child in sorted(template_root.iterdir()):
            destination = sprint_root / template_child.name
            if destination.exists():
                continue
            if template_child.is_dir():
                copy_tree(template_child, destination)
            else:
                shutil.copy2(template_child, destination)
            synced = True
        return "synced" if synced else "existing"
    missing = ", ".join(sorted(required - present))
    raise ValueError(
        "Sprint directory already exists but is incomplete. "
        f"Add the missing template files or clean the directory first: {sprint_root.as_posix()} ({missing})"
    )


def resolve_canonical_sprint_template_root() -> Path:
    """Return the canonical sprint template root or raise a clear helper error."""

    template_root = CANONICAL_SPRINT_TEMPLATE_ROOT
    required_entries = {"sprint.md", "closeout.md", "decision-log.md", "evidence"}
    if not template_root.exists() or not template_root.is_dir():
        raise ValueError(
            "Canonical `ub-workflow` sprint template is missing or invalid: "
            f"{template_root.as_posix()}"
        )

    present_entries = {path.name for path in template_root.iterdir()}
    missing_entries = sorted(required_entries - present_entries)
    if missing_entries:
        raise ValueError(
            "Canonical `ub-workflow` sprint template is missing required entries at "
            f"{template_root.as_posix()}: {', '.join(missing_entries)}"
        )
    return template_root


def ensure_initiative_rollup(initiative_root: Path) -> bool:
    """Backfill rollup.md into existing initiative roots when missing."""

    rollup_path = initiative_root / "rollup.md"
    if rollup_path.exists():
        if not rollup_path.is_file():
            raise ValueError(f"Initiative rollup path exists and is not a file: {rollup_path.as_posix()}")
        return False

    template_path = DEFAULT_INITIATIVE_TEMPLATE_ROOT / "rollup.md"
    if not template_path.exists() or not template_path.is_file():
        raise ValueError(f"Canonical initiative rollup template is missing: {template_path.as_posix()}")

    shutil.copy2(template_path, rollup_path)
    return True


def format_checkbox_items(items: Sequence[str]) -> str:
    """Return roadmap subtasks as Markdown checklist items."""

    if not items:
        return "- [ ] No roadmap subtasks were listed."
    return "\n".join(f"- [ ] {item}" for item in items)


def format_scope_items(entry: RoadmapSprintEntry) -> str:
    """Return numbered scope items derived from the roadmap goal and subtasks."""

    lines = [f"1. Deliver the roadmap goal: {entry.goal}."]
    for index, subtask in enumerate(entry.subtasks, start=2):
        lines.append(f"{index}. Complete roadmap subtask: {subtask}.")
    lines.append(f"{len(lines) + 1}. Record any sprint-specific exclusions or constraints before execution begins.")
    return "\n".join(lines)


def format_execution_slices(entry: RoadmapSprintEntry) -> str:
    """Return execution-slice prompts derived from roadmap subtasks."""

    if not entry.subtasks:
        return (
            "1. Slice 01\n"
            "   - Objective: Replace with the first execution slice objective.\n"
            "   - Acceptance: Replace with how this slice will be considered done.\n"
            "   - Verification: Replace with the check, command, or review step for this slice.\n"
            "   - Dependencies: Replace with blocking inputs or `none`.\n"
            "   - Likely touched areas: Replace with the files, modules, or docs most likely to change."
        )

    lines: list[str] = []
    for index, subtask in enumerate(entry.subtasks, start=1):
        label = f"Slice {index:02d}"
        lines.extend(
            [
                f"{index}. {label}",
                f"   - Objective: {subtask}",
                "   - Acceptance: Replace with the concrete done condition for this slice.",
                "   - Verification: Replace with the check, command, or review step for this slice.",
                "   - Dependencies: Replace with prior slices, external prerequisites, or `none`.",
                "   - Likely touched areas: Replace with the most likely files, modules, systems, or docs.",
            ]
        )
    return "\n".join(lines)


def previous_handoff_note(entry: RoadmapSprintEntry) -> str:
    """Return the generated previous-sprint handoff note for a sprint."""

    if entry.depends_on.lower() == "none":
        return "No prior sprint closeout is required before this sprint begins."
    return (
        f"{PENDING_HANDOFF_PREFIX} Review `{entry.depends_on}` closeout and carry forward any blockers, "
        "validation changes, or repository-truth updates before execution begins."
    )


def next_handoff_note(next_entry: RoadmapSprintEntry | None) -> str:
    """Return the generated next-sprint handoff note for a sprint."""

    if next_entry is None:
        return (
            "No next implementation sprint is planned after this one. Replace this line with final-audit "
            "or archive-readiness carry-forward notes when this sprint closes."
        )
    return (
        f"Roadmap next sprint: `{next_entry.title}` at `./{next_entry.sprint_file.as_posix()}`. "
        "Replace this line with concrete carry-forward notes when this sprint closes."
    )


def build_prepare_sprint_placeholder_map(
    entry: RoadmapSprintEntry,
    next_entry: RoadmapSprintEntry | None,
) -> dict[str, str]:
    """Build the machine-derived placeholder map for one sprint PRD."""

    return {
        "REPLACE_SPRINT_TITLE": entry.title,
        "REPLACE_SPRINT_GOAL": entry.goal,
        "REPLACE_SPRINT_DEPENDS_ON": entry.depends_on,
        "REPLACE_SPRINT_VALIDATION_FOCUS": entry.validation_focus,
        "REPLACE_SPRINT_EVIDENCE_FOLDER": entry.evidence_folder,
        "REPLACE_SPRINT_SUBTASKS": format_checkbox_items(entry.subtasks),
        "REPLACE_SPRINT_SCOPE_ITEMS": format_scope_items(entry),
        "REPLACE_SPRINT_EXECUTION_SLICES": format_execution_slices(entry),
        "REPLACE_PREVIOUS_HANDOFF_NOTE": previous_handoff_note(entry),
        "REPLACE_NEXT_HANDOFF_NOTE": next_handoff_note(next_entry),
    }


def render_prepared_sprint(
    template_path: Path,
    entry: RoadmapSprintEntry,
    next_entry: RoadmapSprintEntry | None,
) -> str:
    """Render one prepared sprint PRD from the template and roadmap entry."""

    template_text = template_path.read_text(encoding="utf-8")
    return render_text_placeholders(
        template_text,
        build_prepare_sprint_placeholder_map(entry, next_entry),
    )


def refresh_initiative_readme_for_sprints(
    readme_path: Path,
    first_sprint_title: str,
    first_sprint_path: Path,
    *,
    phase: str,
    gate: str,
    validation_baseline: str,
    documentation_status: str,
) -> None:
    """Update the initiative README after sprint preparation or initialization."""

    text = readme_path.read_text(encoding="utf-8")
    updates = {
        "Current phase"        : phase,
        "Current gate"         : gate,
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
        f"- Validation baseline: {validation_baseline}\n- Documentation sync status: {documentation_status}\n- Exception records: `none`",
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
    for candidate in (SPRINT_INIT_UNCHECKED, LEGACY_SPRINT_INIT_UNCHECKED, LEGACY_SPRINT_INIT_CHECKED):
        if candidate in text:
            text = text.replace(candidate, SPRINT_INIT_CHECKED, 1)
            break
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
    if normalized_gate != "roadmap_ready: pass" and not roadmap_approval_recorded(roadmap_path):
        errors.append(
            "README.md or roadmap.md must preserve evidence that `roadmap_ready: pass` was approved before sprint preparation or initialization can start."
        )
    if unresolved_placeholder_found(roadmap_path):
        errors.append("roadmap.md still contains unresolved scaffold placeholders.")
    return errors


def resolve_resume_target(initiative_root: Path, roadmap_path: Path) -> Path | None:
    """Resolve the active or next sprint path from roadmap.md when available."""

    roadmap_text = roadmap_path.read_text(encoding="utf-8")
    resume_from = read_markdown_table_value(roadmap_text, "Resume from")
    if not resume_from:
        return None
    normalized = strip_wrapping_backticks(resume_from)
    if normalized in {"none", "review or generate roadmap from ./prd.md"}:
        return None
    relative = normalized.removeprefix("./")
    return initiative_root / Path(relative)


def previous_closeout_for_sprint(initiative_root: Path, sprint_path: Path) -> Path | None:
    """Return the previous sprint closeout path for a given sprint when one exists."""

    roadmap_path = initiative_root / "roadmap.md"
    entries = roadmap_sprint_entries(roadmap_path)
    try:
        relative = sprint_path.resolve().relative_to(initiative_root.resolve())
    except ValueError:
        relative = sprint_path
    for index, entry in enumerate(entries):
        if entry.sprint_file == relative:
            if index == 0:
                return None
            previous = initiative_root / entries[index - 1].sprint_root / "closeout.md"
            return previous if previous.exists() else None
    return None


def resolve_resume_file_order(initiative_root: Path, sprint_path: Path | None = None) -> list[Path]:
    """Return the minimal file order needed to resume an initiative safely."""

    roadmap_path = initiative_root / "roadmap.md"
    readme_path = initiative_root / "README.md"
    prd_path = initiative_root / "prd.md"
    target_sprint = sprint_path or resolve_resume_target(initiative_root, roadmap_path)

    ordered: list[Path] = [roadmap_path]
    previous_closeout: Path | None = None
    if target_sprint is not None:
        previous_closeout = previous_closeout_for_sprint(initiative_root, target_sprint)
        if previous_closeout is not None:
            ordered.append(previous_closeout)
        if target_sprint.exists():
            ordered.append(target_sprint)
    ordered.append(readme_path)
    if (
        prd_path.exists()
        and (
            target_sprint is None
            or not target_sprint.exists()
            or (
                sprint_document_has_blocking_placeholders(target_sprint)
                and previous_closeout is None
            )
        )
    ):
        ordered.append(prd_path)
    return ordered


def command_init_sprints(args: argparse.Namespace) -> int:
    """Create the full sprint set from roadmap path entries."""

    initiative_root = Path(args.initiative_root).resolve()
    roadmap_path = initiative_root / "roadmap.md"
    sprint_template_root = resolve_canonical_sprint_template_root()
    if not roadmap_path.exists():
        raise ValueError(f"Initiative roadmap does not exist: {roadmap_path.as_posix()}")

    readiness_errors = validate_roadmap_ready(initiative_root, roadmap_path)
    if readiness_errors:
        message = "Sprint initialization blocked because the roadmap is not ready:\n- " + "\n- ".join(readiness_errors)
        raise ValueError(message)

    entries = roadmap_sprint_entries(roadmap_path)
    if args.dry_run:
        print(f"dry-run: {len(entries)} sprint directories would be initialized under {initiative_root.as_posix()}")
        return 0

    created = 0
    synced = 0
    rollup_created = ensure_initiative_rollup(initiative_root)
    first_entry = entries[0]
    for entry in entries:
        status = ensure_sprint_directory(sprint_template_root, initiative_root / entry.sprint_root)
        if status == "created":
            created += 1
        elif status == "synced":
            synced += 1

    readme_text = (initiative_root / "README.md").read_text(encoding="utf-8")
    current_gate = read_markdown_table_value(readme_text, "Current gate")
    normalized_gate = current_gate.strip("`") if current_gate else ""
    phase = "Roadmap approved, sprint initialization complete"
    gate = "`roadmap_ready: pass`"
    validation_baseline = "The master PRD, full ordered roadmap, and all planned sprint folders are now in place."
    documentation_status = "No sprint-specific documentation updates are required yet because execution has not started."
    if normalized_gate == "sprint_content_ready: pass":
        phase = "Sprint set initialized, sprint pack ready for execution review"
        gate = "`sprint_content_ready: pass`"
        validation_baseline = "The sprint pack is prepared and all planned sprint folders are now in place."
        documentation_status = "Sprint PRDs are prepared and execution has not started yet."

    refresh_initiative_readme_for_sprints(
        initiative_root / "README.md",
        first_entry.title,
        initiative_root / first_entry.sprint_file,
        phase=phase,
        gate=gate,
        validation_baseline=validation_baseline,
        documentation_status=documentation_status,
    )
    refresh_roadmap_after_sprint_init(
        roadmap_path,
        first_entry.title,
        initiative_root / first_entry.sprint_file,
    )

    print(
        f"initialized {len(entries)} sprint directories "
        f"({created} newly created, {synced} additive template syncs, "
        f"{1 if rollup_created else 0} rollup backfilled)"
    )
    report_generated_placeholder_state(initiative_root, strict=args.strict_placeholders)
    return 0


def command_prepare_sprints(args: argparse.Namespace) -> int:
    """Prepare sprint PRDs from roadmap metadata before execution begins."""

    initiative_root = Path(args.initiative_root).resolve()
    roadmap_path = initiative_root / "roadmap.md"
    sprint_template_root = resolve_canonical_sprint_template_root()
    sprint_template_path = sprint_template_root / "sprint.md"
    if not roadmap_path.exists():
        raise ValueError(f"Initiative roadmap does not exist: {roadmap_path.as_posix()}")

    readiness_errors = validate_roadmap_ready(initiative_root, roadmap_path)
    if readiness_errors:
        message = "Sprint preparation blocked because the roadmap is not ready:\n- " + "\n- ".join(readiness_errors)
        raise ValueError(message)

    entries = roadmap_sprint_entries(roadmap_path)
    if args.dry_run:
        print(f"dry-run: {len(entries)} sprint PRDs would be prepared under {initiative_root.as_posix()}")
        for entry in entries:
            print(
                "dry-run: "
                f"{entry.title} | goal={entry.goal} | depends_on={entry.depends_on} | "
                f"validation_focus={entry.validation_focus} | subtasks={len(entry.subtasks)} | "
                f"evidence={entry.evidence_folder}"
            )
        return 0

    created = 0
    synced = 0
    rendered = 0
    preserved = 0
    rollup_created = ensure_initiative_rollup(initiative_root)
    first_entry = entries[0]
    for index, entry in enumerate(entries):
        sprint_root = initiative_root / entry.sprint_root
        status = ensure_sprint_directory(sprint_template_root, sprint_root)
        if status == "created":
            created += 1
        elif status == "synced":
            synced += 1

        sprint_path = initiative_root / entry.sprint_file
        if sprint_path.exists() and not sprint_document_has_blocking_placeholders(sprint_path):
            preserved += 1
            continue

        next_entry = entries[index + 1] if index + 1 < len(entries) else None
        sprint_path.write_text(
            render_prepared_sprint(sprint_template_path, entry, next_entry),
            encoding="utf-8",
        )
        rendered += 1

    refresh_initiative_readme_for_sprints(
        initiative_root / "README.md",
        first_entry.title,
        initiative_root / first_entry.sprint_file,
        phase="Sprint pack prepared, awaiting Sprint 01 execution",
        gate="`sprint_content_ready: pass`",
        validation_baseline="The sprint pack now contains roadmap-derived sprint PRDs with explicit handoff markers and machine-derived context.",
        documentation_status="Sprint PRDs are prepared for review before execution. Helper and template semantics should be validated before relying on them for new initiatives.",
    )
    refresh_roadmap_after_sprint_init(
        roadmap_path,
        first_entry.title,
        initiative_root / first_entry.sprint_file,
    )

    print(
        f"prepared {len(entries)} sprint PRDs "
        f"({created} directories created, {synced} additive template syncs, "
        f"{rendered} rendered, {preserved} preserved, "
        f"{1 if rollup_created else 0} rollup backfilled)"
    )
    report_generated_placeholder_state(initiative_root, strict=args.strict_placeholders)
    return 0

# endregion Initialize Sprints


# region Archive Initiative

def unresolved_placeholder_found(path: Path) -> bool:
    """Return True when a control file still contains obvious scaffold placeholders."""

    text = path.read_text(encoding="utf-8")
    initiative_root = (
        path.parent
        if path.name in {"README.md", "roadmap.md", "prd.md", "rollup.md", "retained-note.md"}
        else path.parents[2]
    )
    return bool(required_placeholder_markers(text, path, initiative_root))


def overall_checklist_is_complete(roadmap_path: Path) -> bool:
    """Return True when the roadmap overall checklist has no unchecked items."""

    text = roadmap_path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^## Overall Checklist\n\n(.*?)(?=^##\s|\Z)", text)
    if not match:
        return False
    return "- [ ]" not in match.group(1)


def roadmap_approval_recorded(roadmap_path: Path) -> bool:
    """Return True when roadmap approval is visibly recorded in roadmap.md."""

    text = roadmap_path.read_text(encoding="utf-8")
    return "- [x] Roadmap reviewed and approved with `roadmap_ready: pass`" in text


def validate_archive_readiness(initiative_root: Path) -> list[str]:
    """Return validation errors that block archive-on-request."""

    errors: list[str] = []
    readme_path = initiative_root / "README.md"
    roadmap_path = initiative_root / "roadmap.md"
    rollup_path = initiative_root / "rollup.md"
    retained_note_path = initiative_root / "retained-note.md"
    if not readme_path.exists():
        errors.append("README.md is missing.")
    if not roadmap_path.exists():
        errors.append("roadmap.md is missing.")
    if not rollup_path.exists():
        errors.append("rollup.md is missing.")
    if not retained_note_path.exists():
        errors.append("retained-note.md is missing.")
    if errors:
        return errors

    readme_text = readme_path.read_text(encoding="utf-8")
    current_gate = read_markdown_table_value(readme_text, "Current gate")
    normalized_gate = current_gate.strip("`") if current_gate else None
    if normalized_gate not in {"archive_ready: pass", "initiative_complete: pass"}:
        errors.append(
            "README.md must record `archive_ready: pass` or `initiative_complete: pass` before archive can start."
        )

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
        help="Initiative control-file template directory to copy from",
    )
    create_parser.add_argument(
        "--operations-template-root",
        default=str(DEFAULT_OPERATIONS_TEMPLATE_ROOT),
        help="Operations-root template directory to copy from",
    )
    create_parser.add_argument("--initiative-name", help="Display name written into the scaffold")
    create_parser.add_argument("--owner", help="Initiative owner")
    create_parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).date().isoformat(),
        help="Date stamp used in generated paths and README state",
    )
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
    create_parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Fail after create when generated output still has required unresolved placeholders",
    )
    create_parser.add_argument("--dry-run", action="store_true", help="Report the resolved create operation without writing files")

    create_spec_parser = subparsers.add_parser("create-spec", help="Create a new lightweight spec root")
    create_spec_parser.add_argument("target", nargs="?", help="Lightweight spec slug or explicit target path")
    create_spec_parser.add_argument("--ops-root", default=str(DEFAULT_OPS_ROOT), help="Operations root to bootstrap and use")
    create_spec_parser.add_argument(
        "--template-root",
        default=str(DEFAULT_SPEC_TEMPLATE_ROOT),
        help="Lightweight spec template directory to copy from",
    )
    create_spec_parser.add_argument(
        "--operations-template-root",
        default=str(DEFAULT_OPERATIONS_TEMPLATE_ROOT),
        help="Operations-root template directory to copy from",
    )
    create_spec_parser.add_argument("--spec-name", help="Display name written into the lightweight spec scaffold")
    create_spec_parser.add_argument("--owner", help="Lightweight spec owner")
    create_spec_parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).date().isoformat(),
        help="Date stamp used in generated paths and spec state",
    )
    create_spec_parser.add_argument("--status", default="draft", help="Initial lightweight spec status string")
    create_spec_parser.add_argument("--next-action", help="Initial next-action value written into spec.md")
    create_spec_parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Fail after create-spec when generated output still has required unresolved placeholders",
    )
    create_spec_parser.add_argument("--dry-run", action="store_true", help="Report the resolved create-spec operation without writing files")

    prepare_parser = subparsers.add_parser(
        "prepare-sprints",
        help="Prepare sprint PRDs from roadmap metadata before execution begins",
    )
    prepare_parser.add_argument("initiative_root", help="Initiative root containing roadmap.md")
    prepare_parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Fail after sprint preparation when generated output still has required unresolved placeholders",
    )
    prepare_parser.add_argument("--dry-run", action="store_true", help="Report sprint preparation without writing files")

    init_parser = subparsers.add_parser("init-sprints", help="Initialize sprint directories from roadmap paths")
    init_parser.add_argument("initiative_root", help="Initiative root containing roadmap.md")
    init_parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Fail after sprint initialization when generated output still has required unresolved placeholders",
    )
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
        if args.command == "create-spec":
            return command_create_spec(args)
        if args.command == "prepare-sprints":
            return command_prepare_sprints(args)
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
