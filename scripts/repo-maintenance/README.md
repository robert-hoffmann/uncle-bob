# Repo Maintenance Commands

This directory contains the development repository's local maintenance checks.

These scripts validate catalog, packaging, path, and skill-surface integrity
for this repository itself. They are intentionally separate from the
distributable governance scripts that live under `.agents/skills/ub-governance/`.

## Script Inventory

| Script | Purpose | Task Wrapper |
| ------ | ------- | ------------ |
| `check_repo_catalog.py` | Validate `AGENTS.md`, `README.md`, disk inventory, and plugin path alignment. | `task test-repo-catalog` |
| `check_package_metadata.py` | Validate versions and skill/agent count claims across `plugin.json`, `pyproject.toml`, and marketplace metadata. | `task test-package-metadata` |
| `check_repo_paths.py` | Validate canonical root paths and case-sensitive naming. | `task test-repo-paths` |
| `check_skill_schema.py` | Validate skill frontmatter shape and local reference targets. | `task test-skill-schema` |
| `check_skill_integrity.py` | Validate the governance-surface integrity contract after the repo-maintenance split. | `task test-governance-integrity` |

Aggregate wrappers:

1. `task test-integrity` runs the five baseline integrity checks above.
2. `task test-repo-maintenance` runs the extracted regression suite under
   `tests/repo_maintenance/`.

## Direct Invocation

In this repository, prefer the Taskfile wrappers when they fit.
When direct invocation is useful, prefer `uv run python ...`.

Examples:

```bash
uv run python scripts/repo-maintenance/check_repo_catalog.py
uv run python scripts/repo-maintenance/check_package_metadata.py
uv run python scripts/repo-maintenance/check_repo_paths.py
uv run python scripts/repo-maintenance/check_skill_schema.py
uv run python scripts/repo-maintenance/check_skill_integrity.py
```

All five scripts accept `--repo-root`.
The JSON-emitting checks also accept `--output`.

## Boundary

Use these scripts when maintaining this repository's skill catalog and
packaging surfaces.

Do not treat them as the normal governance path for downstream workspaces that
only receive `.agents/skills/`.
