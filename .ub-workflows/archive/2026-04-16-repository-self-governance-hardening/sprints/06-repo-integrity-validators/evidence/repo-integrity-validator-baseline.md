# Sprint 06 Evidence

## Added Validator Entry Points

Sprint 06 added these focused CLI validators under
`./.agents/skills/ub-governance/scripts/`:

1. `check_repo_catalog.py`
2. `check_package_metadata.py`
3. `check_repo_paths.py`
4. `check_skill_schema.py`

Shared helper surface introduced for low-duplication repo walking and parsing:

1. `._repo_integrity.py`

The existing governance integrity checker now treats the 4 new validator
scripts as required governance assets.

## Authoritative Surface Baseline

Sprint 06 encodes this authoritative default repository baseline:

1. root registry: `./AGENTS.md`
2. public overview: `./README.md`
3. package metadata: `./plugin.json`
4. marketplace metadata: `./.github/plugin/marketplace.json`
5. Python package metadata: `./pyproject.toml`
6. custom agent root: `./.github/agents/`
7. skill root: `./.agents/skills/`

Low-noise default ignore scope:

1. `./tmp/`
2. fixture-like test content outside the canonical authoritative roots above

## Direct CLI Proof

These commands passed against the live repository:

1. `uv run python .agents/skills/ub-governance/scripts/check_repo_catalog.py`
2. `uv run python .agents/skills/ub-governance/scripts/check_package_metadata.py`
3. `uv run python .agents/skills/ub-governance/scripts/check_repo_paths.py`
4. `uv run python .agents/skills/ub-governance/scripts/check_skill_schema.py`
5. `uv run python .agents/skills/ub-governance/scripts/check_skill_integrity.py`

Observed pass-state highlights:

1. `check_repo_catalog.py` confirmed 10 tracked skills and 4 tracked custom
   agents across disk, `AGENTS.md`, and `README.md` while allowing curated
   table ordering.
2. `check_package_metadata.py` confirmed version `1.0.0` across
   `pyproject.toml`, `plugin.json`, and `.github/plugin/marketplace.json`, and
   confirmed the marketplace description claim of 10 skills and 4 custom
   agents.
3. `check_repo_paths.py` confirmed exact-case canonical paths, including the
   root `AGENTS.md` rename.
4. `check_skill_schema.py` confirmed valid frontmatter and local reference
   resolution across the 10 tracked skills.

## Regression Coverage Map

`test_governance_scripts.py` now covers pass and fail behavior for each new
validator:

1. catalog pass with `tmp/` noise ignored
2. catalog fail on README inventory drift
3. package-metadata pass with aligned versions and count claims
4. package-metadata fail with version and count drift
5. path pass with exact case and `tmp/` noise ignored
6. path fail with legacy `AGENTS.MD`
7. skill-schema pass with valid frontmatter and references
8. skill-schema fail with invalid frontmatter and missing local references

## Sprint 07 Wiring Targets

Sprint 07 should wire these stable commands into `Taskfile.yml` and CI:

1. `uv run python .agents/skills/ub-governance/scripts/check_repo_catalog.py`
2. `uv run python .agents/skills/ub-governance/scripts/check_package_metadata.py`
3. `uv run python .agents/skills/ub-governance/scripts/check_repo_paths.py`
4. `uv run python .agents/skills/ub-governance/scripts/check_skill_schema.py`
5. `uv run python -m unittest discover -s .agents/skills/ub-governance/tests/governance_scripts -p 'test_*.py' -v`
