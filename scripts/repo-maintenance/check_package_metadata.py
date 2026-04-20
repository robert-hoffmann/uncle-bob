#!/usr/bin/env python3
"""Validate repository package metadata consistency and inventory-like claims."""

from __future__ import annotations

import argparse
import importlib.util
import json
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
collect_agent_names = REPO_INTEGRITY.collect_agent_names
collect_skill_names = REPO_INTEGRITY.collect_skill_names
parse_marketplace_count_claim = REPO_INTEGRITY.parse_marketplace_count_claim
parse_pyproject_version = REPO_INTEGRITY.parse_pyproject_version
write_payload = REPO_INTEGRITY.write_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--output")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[2]
    errors: list[str] = []

    plugin_path = repo_root / "plugin.json"
    marketplace_path = repo_root / ".github" / "plugin" / "marketplace.json"
    pyproject_path = repo_root / "pyproject.toml"

    disk_skill_count = len(collect_skill_names(repo_root))
    disk_agent_count = len(collect_agent_names(repo_root))

    try:
        plugin_json = json.loads(plugin_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append("Missing plugin.json")
        plugin_json = {}
    try:
        marketplace_json = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append("Missing .github/plugin/marketplace.json")
        marketplace_json = {}

    pyproject_version = parse_pyproject_version(pyproject_path)
    if pyproject_version is None:
        errors.append("Unable to parse project version from pyproject.toml")

    plugin_version = str(plugin_json.get("version", "")).strip()
    metadata_version = str(marketplace_json.get("metadata", {}).get("version", "")).strip()
    plugin_entry = marketplace_json.get("plugins", [{}])
    marketplace_version = str(plugin_entry[0].get("version", "")).strip() if plugin_entry else ""

    versions = {
        "pyproject": pyproject_version,
        "plugin.json": plugin_version,
        "marketplace.metadata": metadata_version,
        "marketplace.plugin": marketplace_version,
    }
    normalized_versions = {key: value for key, value in versions.items() if value}
    if len(set(normalized_versions.values())) > 1:
        errors.append(f"Version mismatch across package metadata surfaces: {normalized_versions}")

    description = str(plugin_entry[0].get("description", "")) if plugin_entry else ""
    count_claim = parse_marketplace_count_claim(description)
    if count_claim is None:
        errors.append("Marketplace plugin description must include skill and custom agent count claims")
    else:
        claimed_skill_count, claimed_agent_count = count_claim
        if claimed_skill_count != disk_skill_count:
            errors.append(
                f"Marketplace description claims {claimed_skill_count} skills but disk has {disk_skill_count}"
            )
        if claimed_agent_count != disk_agent_count:
            errors.append(
                f"Marketplace description claims {claimed_agent_count} custom agents but disk has {disk_agent_count}"
            )

    payload = {
        "status": "fail" if errors else "pass",
        "repoRoot": repo_root.as_posix(),
        "versions": versions,
        "diskCounts": {"skills": disk_skill_count, "customAgents": disk_agent_count},
        "errors": errors,
        "warnings": [],
    }
    write_payload(payload, args.output)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
