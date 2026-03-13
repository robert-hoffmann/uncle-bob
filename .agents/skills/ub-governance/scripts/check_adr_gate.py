#!/usr/bin/env python3
"""Evaluate ADR governance gate status for changed files."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
from pathlib import Path
import subprocess
from typing import Any

BLOCKED_EXIT = 2


def _normalize(path: str) -> str:
    value = path.strip().replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value.strip("/")


def load_changed_files(changed_file_args: list[str], changed_file_list: str | None) -> list[str]:
    files: list[str] = []

    for value in changed_file_args:
        norm = _normalize(value)
        if norm:
            files.append(norm)

    if changed_file_list:
        list_path = Path(changed_file_list)
        if list_path.exists():
            for line in list_path.read_text(encoding="utf-8").splitlines():
                norm = _normalize(line)
                if norm:
                    files.append(norm)

    unique = sorted(set(files))
    return unique


def load_changed_files_from_git(base_ref: str, head_ref: str) -> list[str]:
    cmd = ["git", "diff", "--name-only", f"{base_ref}...{head_ref}"]
    output = subprocess.check_output(cmd, text=True)
    items = [_normalize(line) for line in output.splitlines() if line.strip()]
    return sorted(set(items))


def load_high_risk_patterns(path: Path) -> list[str]:
    if not path.exists():
        return []

    patterns: list[str] = []
    in_block = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("high_risk_paths:"):
            in_block = True
            continue
        if in_block and stripped.startswith("-"):
            pattern = stripped[1:].strip().strip("\"").strip("'")
            if pattern:
                patterns.append(pattern)
        elif in_block and not raw_line.startswith(" "):
            break

    return patterns


def path_matches_pattern(path: str, pattern: str) -> bool:
    if fnmatch.fnmatch(path, pattern):
        return True

    if pattern.endswith("/"):
        return path.startswith(pattern)

    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path.startswith(prefix)

    return False


def collect_high_risk_files(changed_files: list[str], patterns: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    matched: dict[str, list[str]] = {}

    for file_path in changed_files:
        for pattern in patterns:
            if path_matches_pattern(file_path, pattern):
                matched.setdefault(pattern, []).append(file_path)

    high_risk_files = sorted({item for values in matched.values() for item in values})
    return high_risk_files, matched


def load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schemaVersion": "0", "generatedAt": None, "entries": []}
    return json.loads(path.read_text(encoding="utf-8"))


def entry_matches_file(entry: dict[str, Any], file_path: str) -> bool:
    for pattern in entry.get("paths", []):
        if not isinstance(pattern, str):
            continue
        pattern = _normalize(pattern)
        if not pattern:
            continue
        if fnmatch.fnmatch(file_path, pattern):
            return True
        if pattern.endswith("/") and file_path.startswith(pattern):
            return True
        if file_path.startswith(pattern.rstrip("/") + "/"):
            return True
    return False


def load_waivers(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        waivers = payload.get("waivers", [])
        if isinstance(waivers, list):
            return [item for item in waivers if isinstance(item, dict)]
    return []


def waiver_applies(waiver: dict[str, Any], changed_files: list[str], today: dt.date) -> tuple[bool, str]:
    owner = str(waiver.get("owner", "")).strip()
    follow_up = str(waiver.get("followUp") or waiver.get("follow_up") or "").strip()
    expires_raw = str(waiver.get("expiresAt") or waiver.get("expires_at") or "").strip()
    waiver_id = str(waiver.get("id", "")).strip() or "unknown-waiver"

    if not owner or not follow_up or not expires_raw:
        return False, f"Waiver {waiver_id} missing owner/follow-up/expiry"

    try:
        expires_at = dt.date.fromisoformat(expires_raw)
    except ValueError:
        return False, f"Waiver {waiver_id} has invalid expiresAt: {expires_raw}"

    if expires_at < today:
        return False, f"Waiver {waiver_id} expired on {expires_at.isoformat()}"

    affected = waiver.get("affectedPaths") or waiver.get("affected_paths") or []
    patterns = [item for item in affected if isinstance(item, str)]

    if not patterns:
        return True, waiver_id

    for changed in changed_files:
        for pattern in patterns:
            if path_matches_pattern(changed, _normalize(pattern)):
                return True, waiver_id
    return False, waiver_id


def write_output(path: Path | None, payload: dict[str, Any]) -> None:
    content = json.dumps(payload, indent=2) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(content, end="")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", choices=["merge", "confidence", "release"], default="merge")
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--changed-files-file")
    parser.add_argument("--base-ref")
    parser.add_argument("--head-ref")
    parser.add_argument(
        "--high-risk-config",
        default=".agents/skills/ub-governance/references/high-risk-paths.yaml",
    )
    parser.add_argument("--adr-registry", default="docs/adr/registry.json")
    parser.add_argument("--waivers", default="docs/adr/waivers.json")
    parser.add_argument("--output")
    parser.add_argument("--today", help="Override ISO date for deterministic tests")
    args = parser.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    changed_files = load_changed_files(args.changed_file, args.changed_files_file)
    if not changed_files and args.base_ref and args.head_ref:
        changed_files = load_changed_files_from_git(args.base_ref, args.head_ref)

    patterns = load_high_risk_patterns(Path(args.high_risk_config))
    high_risk_files, matched_patterns = collect_high_risk_files(changed_files, patterns)

    registry_path = Path(args.adr_registry)
    waivers_path = Path(args.waivers)
    registry = load_registry(registry_path)
    entries = [entry for entry in registry.get("entries", []) if isinstance(entry, dict)]

    adr_markdown_changes = [
        item
        for item in changed_files
        if item.startswith("docs/adr/") and item.endswith(".md")
    ]
    registry_has_changed_adr = {
        entry.get("adrPath")
        for entry in entries
        if isinstance(entry.get("adrPath"), str) and entry.get("adrPath") in adr_markdown_changes
    }

    structural_matches: dict[str, list[str]] = {}
    for changed in high_risk_files:
        ids: list[str] = []
        for entry in entries:
            if entry_matches_file(entry, changed):
                ids.append(str(entry.get("id", "")))
        if ids:
            structural_matches[changed] = sorted(set(ids))

    waivers = load_waivers(waivers_path)
    active_waivers: list[str] = []
    waiver_notes: list[str] = []
    for waiver in waivers:
        applies, detail = waiver_applies(waiver, high_risk_files, today)
        if applies:
            active_waivers.append(detail)
        elif detail and detail not in waiver_notes:
            waiver_notes.append(detail)

    status = "pass"
    reasons: list[str] = []

    if not changed_files:
        reasons.append("No changed files were provided; ADR gate treated as pass.")
    elif not high_risk_files:
        reasons.append("No high-risk paths touched; ADR gate not required.")
    else:
        if args.gate == "merge":
            has_aligned_adr_change = bool(registry_has_changed_adr)
            has_valid_waiver = bool(active_waivers)
            if has_aligned_adr_change:
                reasons.append("High-risk changes include ADR markdown updates registered in docs/adr/registry.json.")
            elif has_valid_waiver:
                status = "pass"
                reasons.append("High-risk changes allowed by active ADR waiver.")
            else:
                status = "blocked"
                reasons.append(
                    "High-risk paths changed without ADR markdown update registered in docs/adr/registry.json and without an active waiver."
                )
        else:
            if active_waivers:
                status = "blocked"
                reasons.append("Confidence/release gate cannot pass with active ADR waivers.")
            if not structural_matches:
                status = "blocked"
                reasons.append("No accepted ADR entries matched changed high-risk paths.")

    payload = {
        "status": status,
        "gate": args.gate,
        "changedFiles": changed_files,
        "highRiskFiles": high_risk_files,
        "matchedPatterns": matched_patterns,
        "registry": {
            "path": registry_path.as_posix(),
            "entryCount": len(entries),
            "changedAdrFiles": adr_markdown_changes,
            "changedAdrRegistered": sorted(registry_has_changed_adr),
            "structuralMatches": structural_matches,
        },
        "waivers": {
            "path": waivers_path.as_posix(),
            "active": sorted(set(active_waivers)),
            "notes": waiver_notes,
        },
        "reasons": reasons,
        "generatedAt": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }

    output_path = Path(args.output) if args.output else None
    write_output(output_path, payload)

    if status == "pass":
        return 0
    if status == "blocked":
        return BLOCKED_EXIT
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

