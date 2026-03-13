#!/usr/bin/env python3
"""Build a machine-readable ADR registry from docs/adr markdown files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
from typing import Any

ADR_FILE_RE = re.compile(r"^(?P<num>[0-9]{4})-.*\.md$")


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_scalar_or_list(value: str) -> Any:
    value = value.strip()
    if value == "":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_strip_quotes(part.strip()) for part in inner.split(",") if part.strip()]
    return _strip_quotes(value)


def parse_front_matter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}

    data: dict[str, Any] = {}
    current_key: str | None = None

    for raw_line in lines[1:]:
        line = raw_line.rstrip()
        if line.strip() == "---":
            break
        if not line.strip() or line.strip().startswith("#"):
            continue

        stripped = line.lstrip()
        if stripped.startswith("- ") and current_key:
            item = _strip_quotes(stripped[2:].strip())
            bucket = data.setdefault(current_key, [])
            if isinstance(bucket, list):
                bucket.append(item)
            continue

        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = parse_scalar_or_list(raw_value)

        data[key] = value
        current_key = key if isinstance(value, list) else None

    for list_key in (
        "supersedes",
        "tags",
        "paths",
        "constraints_refs",
        "source_claims",
    ):
        if list_key not in data:
            data[list_key] = []
        elif not isinstance(data[list_key], list):
            data[list_key] = [str(data[list_key])]

    return data


def infer_title(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title
    return None


def normalize_path(path: Path, repo_root: Path) -> str:
    resolved_path = path.resolve()
    resolved_root = repo_root.resolve()
    try:
        return resolved_path.relative_to(resolved_root).as_posix()
    except ValueError:
        return resolved_path.as_posix()


def build_entry(path: Path, repo_root: Path, strict: bool) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    metadata = parse_front_matter(text)

    match = ADR_FILE_RE.match(path.name)
    if not match:
        return None, [f"Invalid ADR filename format: {path.as_posix()}"]

    numeric_id = match.group("num")
    fallback_id = f"ADR-{numeric_id}"
    adr_id = str(metadata.get("id") or fallback_id)

    title = metadata.get("title") or infer_title(text)
    if isinstance(title, str) and title.startswith("ADR-") and ":" in title:
        title = title.split(":", 1)[1].strip()

    status = str(metadata.get("status") or "proposed")
    date_value = str(metadata.get("date") or "")
    review_by = str(metadata.get("review_by") or "")

    if strict:
        if not metadata.get("id"):
            errors.append(f"Missing front matter field 'id' in {path.as_posix()}")
        if not metadata.get("title"):
            errors.append(f"Missing front matter field 'title' in {path.as_posix()}")
        if not metadata.get("status"):
            errors.append(f"Missing front matter field 'status' in {path.as_posix()}")
        if not metadata.get("date"):
            errors.append(f"Missing front matter field 'date' in {path.as_posix()}")
        if not metadata.get("review_by"):
            errors.append(f"Missing front matter field 'review_by' in {path.as_posix()}")

    if not title:
        errors.append(f"Unable to infer title for {path.as_posix()}")

    if date_value:
        try:
            dt.date.fromisoformat(date_value)
        except ValueError:
            errors.append(f"Invalid ISO date for 'date' in {path.as_posix()}: {date_value}")

    if review_by:
        try:
            dt.date.fromisoformat(review_by)
        except ValueError:
            errors.append(f"Invalid ISO date for 'review_by' in {path.as_posix()}: {review_by}")

    entry = {
        "id": adr_id,
        "title": str(title) if title else "",
        "status": status,
        "date": date_value,
        "supersedes": list(metadata.get("supersedes", [])),
        "tags": list(metadata.get("tags", [])),
        "paths": list(metadata.get("paths", [])),
        "constraintsRefs": list(metadata.get("constraints_refs", [])),
        "sourceClaims": list(metadata.get("source_claims", [])),
        "reviewBy": review_by,
        "adrPath": normalize_path(path, repo_root),
    }

    if strict:
        if not entry["tags"]:
            errors.append(f"No tags set for {path.as_posix()}")
        if not entry["paths"]:
            errors.append(f"No paths set for {path.as_posix()}")
        if not entry["constraintsRefs"]:
            errors.append(f"No constraints_refs set for {path.as_posix()}")

    if errors:
        return None, errors
    return entry, []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--adr-dir", default="docs/adr", help="ADR directory path")
    parser.add_argument("--output", default="docs/adr/registry.json", help="Registry output path")
    parser.add_argument("--strict", action="store_true", help="Fail on missing required metadata")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    adr_dir = (repo_root / args.adr_dir).resolve()
    output_path = (repo_root / args.output).resolve()

    if not adr_dir.exists():
        payload = {
            "status": "fail",
            "error": f"ADR directory not found: {adr_dir.as_posix()}",
        }
        print(json.dumps(payload, indent=2))
        return 1

    entries: list[dict[str, Any]] = []
    errors: list[str] = []

    for path in sorted(adr_dir.glob("[0-9][0-9][0-9][0-9]-*.md")):
        entry, entry_errors = build_entry(path, repo_root, args.strict)
        errors.extend(entry_errors)
        if entry:
            entries.append(entry)

    if errors:
        payload = {
            "status": "fail",
            "errors": errors,
            "entryCount": len(entries),
        }
        print(json.dumps(payload, indent=2))
        return 1

    entries.sort(key=lambda item: item["id"])
    registry = {
        "schemaVersion": "1",
        "generatedAt": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "entries": entries,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    payload = {
        "status": "pass",
        "output": normalize_path(output_path, repo_root),
        "entryCount": len(entries),
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
