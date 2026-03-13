# Governance Commands

Stable governance entrypoints (Pass 2 baseline):

1. `python .agents/skills/ub-governance/scripts/build_adr_registry.py`
2. `python .agents/skills/ub-governance/scripts/check_adr_gate.py`
3. `python .agents/skills/ub-governance/scripts/check_claim_register.py`
4. `python .agents/skills/ub-governance/scripts/check_test_signal.py`
5. `python .agents/skills/ub-governance/scripts/check_skill_integrity.py`

These entrypoints execute the canonical Python implementations directly for cross-platform portability.

## Usage Examples

```bash
python .agents/skills/ub-governance/scripts/build_adr_registry.py --strict --output docs/adr/registry.json
python .agents/skills/ub-governance/scripts/check_adr_gate.py --gate merge --changed-files-file artifacts/decision-governance/changed-files.txt --output artifacts/decision-governance/adr-gate.json
python .agents/skills/ub-governance/scripts/check_claim_register.py --claim-register docs/adr/claim-register.json --output artifacts/decision-governance/claim-gate.json
python .agents/skills/ub-governance/scripts/check_test_signal.py --path .agents/skills/ub-governance/tests --language auto --strict
python .agents/skills/ub-governance/scripts/check_skill_integrity.py
```
