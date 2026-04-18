# Governance Commands

Stable governance entrypoints (Pass 2 baseline):

1. `python .agents/skills/ub-governance/scripts/build_adr_registry.py`
2. `python .agents/skills/ub-governance/scripts/check_adr_gate.py`
3. `python .agents/skills/ub-governance/scripts/check_claim_register.py`
4. `python .agents/skills/ub-governance/scripts/check_test_signal.py`
5. `python .agents/skills/ub-governance/scripts/check_skill_integrity.py`

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

Common repo-local wrappers:

1. `task test-integrity` for repository integrity baseline checks
2. `task test-governance` for governance regression tests

## Usage Examples

Portable script-surface examples:

```bash
python .agents/skills/ub-governance/scripts/build_adr_registry.py --strict --output docs/adr/registry.json
python .agents/skills/ub-governance/scripts/check_adr_gate.py --gate merge --changed-files-file artifacts/decision-governance/changed-files.txt --output artifacts/decision-governance/adr-gate.json
python .agents/skills/ub-governance/scripts/check_claim_register.py --claim-register docs/adr/claim-register.json --output artifacts/decision-governance/claim-gate.json
python .agents/skills/ub-governance/scripts/check_test_signal.py --path .agents/skills/ub-governance/tests --language auto --strict
python .agents/skills/ub-governance/scripts/check_skill_integrity.py
```

Repo-local direct invocation examples:

```bash
uv run python .agents/skills/ub-governance/scripts/build_adr_registry.py --strict --output docs/adr/registry.json
uv run python .agents/skills/ub-governance/scripts/check_adr_gate.py --gate merge --changed-files-file artifacts/decision-governance/changed-files.txt --output artifacts/decision-governance/adr-gate.json
uv run python .agents/skills/ub-governance/scripts/check_claim_register.py --claim-register docs/adr/claim-register.json --output artifacts/decision-governance/claim-gate.json
uv run python .agents/skills/ub-governance/scripts/check_test_signal.py --path .agents/skills/ub-governance/tests --language auto --strict
uv run python .agents/skills/ub-governance/scripts/check_skill_integrity.py
```
