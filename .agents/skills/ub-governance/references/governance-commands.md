# Governance Commands

Stable governance entrypoints (Pass 2 baseline):

1. `uv run python .agents/skills/ub-governance/scripts/build_adr_registry.py`
2. `uv run python .agents/skills/ub-governance/scripts/check_adr_gate.py`
3. `uv run python .agents/skills/ub-governance/scripts/check_claim_register.py`
4. `uv run python .agents/skills/ub-governance/scripts/check_test_signal.py`

These entrypoints execute the canonical Python implementations through `uv`
when available so the command uses the host project's intended environment.

Host repository note:

1. Prefer host-defined wrappers when the repository exposes them.
2. Prefer `uv run python ...` when `uv` is available or the host repository
   uses `uv`.
3. Replace `uv run python` with the configured local Python runner, such as
   `python`, when `uv` is unavailable or inappropriate for the host.

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

Host-repository wrappers:

1. A host repository may expose an integrity-baseline wrapper through its own
   task runner.
2. A host repository may expose a governance-regression wrapper through its own
   task runner.

Repo-local maintenance note:

1. Repo-maintenance wrappers belong to the host repository's own documented
   maintenance/check surface.
2. That surface is intentionally separate from the distributable governance
   command set carried by this skill.

## Usage Examples

Portable script-surface examples:

```bash
uv run python .agents/skills/ub-governance/scripts/build_adr_registry.py --strict --output docs/adr/registry.json
uv run python .agents/skills/ub-governance/scripts/check_adr_gate.py --gate merge --changed-files-file artifacts/decision-governance/changed-files.txt --output artifacts/decision-governance/adr-gate.json
uv run python .agents/skills/ub-governance/scripts/check_claim_register.py --claim-register docs/adr/claim-register.json --output artifacts/decision-governance/claim-gate.json
uv run python .agents/skills/ub-governance/scripts/check_test_signal.py --path .agents/skills/ub-governance/tests --language auto --strict
```
