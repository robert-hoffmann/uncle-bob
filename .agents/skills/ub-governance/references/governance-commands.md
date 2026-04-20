# Governance Commands

Stable governance entrypoints (Pass 2 baseline):

1. `python .agents/skills/ub-governance/scripts/build_adr_registry.py`
2. `python .agents/skills/ub-governance/scripts/check_adr_gate.py`
3. `python .agents/skills/ub-governance/scripts/check_claim_register.py`
4. `python .agents/skills/ub-governance/scripts/check_test_signal.py`

These entrypoints execute the canonical Python implementations directly for cross-platform portability.

Repository note:

1. in this repository, prefer `task` wrappers when they exist
2. use `uv run python ...` for direct repository Python invocation when no task
   wrapper fits
3. the `python ...` commands below describe the portable script surface, not
   the only valid local wrapper

Use them as explicit governance tools, not as the default workflow path for
every change.

Operator intent:

1. `check_test_signal.py` commonly supports testing governance during ordinary
   implementation work.
2. `build_adr_registry.py`, `check_adr_gate.py`, and `check_claim_register.py`
   are primarily for Level 2 or explicit repository-governance runs where ADR
   alignment, claims, or high-risk gate checks were intentionally activated.
3. Workflow-backed Level 1 initiatives normally keep their operational record
   in `prd.md`, `roadmap.md`, `sprint.md`, `closeout.md`, sprint `evidence/`,
   and bounded initiative `exceptions/` instead of invoking ADR machinery by
   default.
4. Repository-catalog, package-metadata, and skill-surface integrity scripts
   are repo-maintenance tooling, not default governance commands.

Common repo-local wrappers:

1. `task test-integrity` for repository integrity baseline checks
2. `task test-governance` for governance regression tests

Repo-local maintenance note:

1. In this development repository, the extracted repo-maintenance command
   surface is documented alongside the scripts in `scripts/repo-maintenance/`.
2. That surface is intentionally separate from the distributable governance
   command set carried under `.agents/skills/ub-governance/`.

## Usage Examples

Portable script-surface examples:

```bash
python .agents/skills/ub-governance/scripts/build_adr_registry.py --strict --output docs/adr/registry.json
python .agents/skills/ub-governance/scripts/check_adr_gate.py --gate merge --changed-files-file artifacts/decision-governance/changed-files.txt --output artifacts/decision-governance/adr-gate.json
python .agents/skills/ub-governance/scripts/check_claim_register.py --claim-register docs/adr/claim-register.json --output artifacts/decision-governance/claim-gate.json
python .agents/skills/ub-governance/scripts/check_test_signal.py --path .agents/skills/ub-governance/tests --language auto --strict
```

Repo-local direct invocation examples:

```bash
uv run python .agents/skills/ub-governance/scripts/build_adr_registry.py --strict --output docs/adr/registry.json
uv run python .agents/skills/ub-governance/scripts/check_adr_gate.py --gate merge --changed-files-file artifacts/decision-governance/changed-files.txt --output artifacts/decision-governance/adr-gate.json
uv run python .agents/skills/ub-governance/scripts/check_claim_register.py --claim-register docs/adr/claim-register.json --output artifacts/decision-governance/claim-gate.json
uv run python .agents/skills/ub-governance/scripts/check_test_signal.py --path .agents/skills/ub-governance/tests --language auto --strict
```

## Repo-Maintenance In This Repository

These commands are for maintaining this development repository's catalog and
skill surfaces. They are not part of the normal governance command path that
gets copied into downstream workspaces.

Task wrappers:

1. `task test-repo-catalog`
2. `task test-package-metadata`
3. `task test-repo-paths`
4. `task test-skill-schema`
5. `task test-governance-integrity`
6. `task test-integrity`
7. `task test-repo-maintenance`
