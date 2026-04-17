#!/usr/bin/env python3
"""Validate repository catalog integrity across disk, registry, and README."""

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
collect_agent_names = REPO_INTEGRITY.collect_agent_names
collect_skill_names = REPO_INTEGRITY.collect_skill_names
parse_markdown_table_names = REPO_INTEGRITY.parse_markdown_table_names
read_text = REPO_INTEGRITY.read_text
write_payload = REPO_INTEGRITY.write_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--output")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[4]
    errors: list[str] = []
    warnings: list[str] = []

    agents_md = repo_root / "AGENTS.md"
    readme_md = repo_root / "README.md"
    plugin_json = repo_root / "plugin.json"

    errors.extend(
        f"Missing required repository surface: {required_path.relative_to(repo_root).as_posix()}"
        for required_path in (agents_md, readme_md, plugin_json)
        if not required_path.exists()
    )

    disk_skills = collect_skill_names(repo_root)
    disk_agents = collect_agent_names(repo_root)
    registry_skills = parse_markdown_table_names(agents_md, "Skills") if agents_md.exists() else []
    registry_agents = parse_markdown_table_names(agents_md, "Agents") if agents_md.exists() else []
    readme_skills = parse_markdown_table_names(readme_md, "What's Included") if readme_md.exists() else []
    readme_agents = parse_markdown_table_names(readme_md, "What's Included")[-len(disk_agents) :] if readme_md.exists() and disk_agents else []

    if sorted(registry_skills) != disk_skills:
        errors.append(f"AGENTS.md skills table does not match disk skills: expected {disk_skills}, found {registry_skills}")
    if sorted(registry_agents) != disk_agents:
        errors.append(f"AGENTS.md agents table does not match disk agents: expected {disk_agents}, found {registry_agents}")
    if sorted(readme_skills[: len(disk_skills)]) != disk_skills:
        errors.append(f"README.md skills table does not match disk skills: expected {disk_skills}, found {readme_skills[: len(disk_skills)]}")
    if sorted(readme_agents) != disk_agents:
        errors.append(f"README.md agents table does not match disk agents: expected {disk_agents}, found {readme_agents}")

    if plugin_json.exists():
        plugin_text = read_text(plugin_json)
        if '"skills": ".agents/skills/"' not in plugin_text:
            errors.append('plugin.json must point "skills" to ".agents/skills/"')
        if '"agents": ".github/agents/"' not in plugin_text:
            errors.append('plugin.json must point "agents" to ".github/agents/"')

    payload = {
        "status": "fail" if errors else "pass",
        "repoRoot": repo_root.as_posix(),
        "ignoredScope": ["tmp/", "fixture-like test content outside authoritative roots"],
        "skills": {
            "disk": disk_skills,
            "agentsMd": registry_skills,
            "readme": readme_skills[: len(disk_skills)],
        },
        "agents": {
            "disk": disk_agents,
            "agentsMd": registry_agents,
            "readme": readme_agents,
        },
        "errors": errors,
        "warnings": warnings,
    }
    write_payload(payload, args.output)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
