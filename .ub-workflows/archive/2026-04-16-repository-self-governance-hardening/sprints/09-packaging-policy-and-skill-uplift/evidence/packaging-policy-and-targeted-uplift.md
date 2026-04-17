# Sprint 09 Evidence

## Packaging Policy Decision

Sprint 09 added the canonical packaging policy document at
`./docs/packaging-policy.md`.

Key contract decisions:

1. a skill package only requires `SKILL.md`
2. `references/`, `assets/`, `agents/`, `docs/`, `scripts/`, and `tests/` are
   optional support surfaces
3. custom-agent registry truth remains the `.github/agents/*.agent.md` files
4. plugin metadata synchronization remains anchored to `pyproject.toml`,
   `plugin.json`, and `.github/plugin/marketplace.json`

## `agents/openai.yaml` Decision

Status: optional

Reasoning:

1. the repository currently mixes skills with and without `agents/openai.yaml`
2. the active integrity baseline does not require it for package validity
3. making it required would add ceremony without improving the core inventory
   or governance contract

Operational outcome:

1. keep `agents/openai.yaml` when a skill needs provider-specific interface
   metadata
2. do not add it merely for symmetry
3. do not treat its absence as package drift

## `ub-python` Uplift

Sprint 09 deepened `ub-python` in two targeted ways:

1. `SKILL.md` now loads a repository-specific Python workflow reference
2. `references/repository-python-workflows.md` records the real repository
   Python baseline: `uv`, `ruff`, stdlib `unittest`, direct script execution,
   and the absence of repository-wired mypy/pytest gates

This closes the mismatch where `ub-python` previously described a more generic
Python toolchain than this repository actually enforces.

## Structural Consistency Fixes

Sprint 09 normalized only two high-value documentation inconsistencies:

1. `ub-css` now includes an explicit `Output Requirements` section
2. `ub-customizations` now includes an explicit `Completion Checklist`

The sprint intentionally avoided repo-wide skill normalization beyond those
high-value gaps.

## Validation Proof

Passed commands:

1. `npx --yes markdownlint-cli2 docs/packaging-policy.md .agents/skills/ub-python/SKILL.md .agents/skills/ub-python/references/repository-python-workflows.md .agents/skills/ub-css/SKILL.md .agents/skills/ub-customizations/SKILL.md`
2. `uv run python .agents/skills/ub-governance/scripts/check_skill_schema.py`
3. `task check`
