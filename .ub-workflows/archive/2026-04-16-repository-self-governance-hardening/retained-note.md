# Retained Note

Status: complete

## Outcome

Repository self-governance hardening completed with a green final validation
baseline and explicit archive-ready status.

## What Shipped

Shipped capabilities:

1. corrected and regression-protected `ub-workflow` lifecycle and scaffold behavior
2. aligned inventory, metadata, and `AGENTS.md` registry truth
3. deterministic repository-integrity validators with local-to-CI parity
4. generated-output placeholder checking and strict-mode readiness support
5. explicit packaging policy with `agents/openai.yaml` marked optional
6. warning-only freshness policy and explicit policy-versus-default boundaries

## Preserve These Decisions

Preserve these decisions:

1. `task check` is the closest local CI mirror and the blocking validation baseline
2. generated-output placeholder enforcement distinguishes required findings
   from advisory authoring prompts and handoff markers
3. `agents/openai.yaml` is optional, not a required skill-package surface
4. freshness review for high-volatility skills is advisory-only by default
5. archive remains an explicit human decision after final audit, not an
   automatic side effect of green tests

## Useful Future Notes

Useful future notes:

1. packaging, freshness, and placeholder policies now exist as explicit docs,
   so future work should update those contracts rather than relying on implied conventions
2. the repository's Python baseline is `uv`, Ruff, direct script execution,
   and stdlib `unittest`, not repository-wired mypy or pytest gates
3. built-in `Explore` references may remain inside local agent implementation
   details, but the published repository agent inventory is 4 custom agents

## Deferred Items

No intentional deferred items were recorded during the final audit.

## Governance Bridge Summary

Governance bridge level: `Level 1`

Profile: `lean`

No active exceptions or ADR waivers remained open at final audit.

If governance coordination was active, also record the profile, exception
references, and ADR references that shaped the final decision.

## Follow-Up Decisions

No additional follow-up audits or refactors were requested.

## Validation Baseline

Final validation commands and outcomes:

1. `task check` — pass
2. `uv run python .agents/skills/ub-workflow/scripts/check_scaffold_placeholders.py ./.ub-workflows/initiatives/2026-04-16-repository-self-governance-hardening --strict` — pass
3. `uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive ./.ub-workflows/initiatives/2026-04-16-repository-self-governance-hardening --dry-run` — pass

Evidence pointer:

1. `./sprints/11-final-audit/evidence/final-audit-summary.md`

Documentation synchronization confirmation:

1. `README.md`, `roadmap.md`, and this retained note were synchronized during
   the final audit.
