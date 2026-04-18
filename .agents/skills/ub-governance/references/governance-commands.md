# Governance Commands

Stable governance entrypoints (Pass 2 baseline):

1. `python .agents/skills/ub-governance/scripts/build_adr_registry.py`
2. `python .agents/skills/ub-governance/scripts/check_adr_gate.py`
3. `python .agents/skills/ub-governance/scripts/check_claim_register.py`
4. `python .agents/skills/ub-governance/scripts/check_test_signal.py`
5. `python .agents/skills/ub-governance/scripts/check_skill_integrity.py`

These entrypoints execute the canonical Python implementations directly for cross-platform portability.

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

## Usage Examples

```bash
python .agents/skills/ub-governance/scripts/build_adr_registry.py --strict --output docs/adr/registry.json
python .agents/skills/ub-governance/scripts/check_adr_gate.py --gate merge --changed-files-file artifacts/decision-governance/changed-files.txt --output artifacts/decision-governance/adr-gate.json
python .agents/skills/ub-governance/scripts/check_claim_register.py --claim-register docs/adr/claim-register.json --output artifacts/decision-governance/claim-gate.json
python .agents/skills/ub-governance/scripts/check_test_signal.py --path .agents/skills/ub-governance/tests --language auto --strict
python .agents/skills/ub-governance/scripts/check_skill_integrity.py
```
