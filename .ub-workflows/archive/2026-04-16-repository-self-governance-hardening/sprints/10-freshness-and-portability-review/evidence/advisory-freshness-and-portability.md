# Sprint 10 Evidence

## Advisory Freshness Design

Sprint 10 added the canonical advisory freshness policy document at
`./docs/freshness-policy.md`.

Key decisions:

1. freshness remains warning-only by default
2. high-volatility skills use lightweight documentation markers rather than a
   new metadata registry
3. freshness markers are review signals, not blocking integrity or CI gates
4. the advisory layer must not weaken the existing packaging or integrity
   baseline

## High-Volatility Skill Markers

Sprint 10 added `Freshness Review` sections to these skills:

1. `ub-tailwind`
2. `ub-nuxt`
3. `ub-vuejs`
4. `ub-ts`
5. `ub-python`
6. `ub-customizations`

Each marker records:

1. volatility level
2. review recommendation
3. trigger signals
4. advisory-only enforcement status
5. stable core guidance that should survive recipe churn

## Policy Versus Defaults Clarification

Sprint 10 clarified portability boundaries in the core quality surfaces:

1. `AGENTS.md` now distinguishes repository policy from strong defaults
2. `ub-quality` now points to a dedicated freshness-and-portability reference
3. `ub-quality` explicitly states that alignment and required-reference loading
   are repository policy in this repo, while many sibling-skill setup patterns
   remain strong defaults rather than universal rules

## No New Blocking Layer

Sprint 10 intentionally did not add:

1. a freshness checker
2. a CI freshness job
3. a new task in `Taskfile.yml`
4. a metadata file that the integrity baseline must parse

That restraint is part of the shipped behavior, not missing work.

## Validation Proof

Passed commands:

1. `npx --yes markdownlint-cli2 docs/freshness-policy.md AGENTS.md .agents/skills/ub-quality/SKILL.md .agents/skills/ub-quality/references/freshness-portability.md .agents/skills/ub-tailwind/SKILL.md .agents/skills/ub-nuxt/SKILL.md .agents/skills/ub-vuejs/SKILL.md .agents/skills/ub-ts/SKILL.md .agents/skills/ub-python/SKILL.md .agents/skills/ub-customizations/SKILL.md`
2. `uv run python .agents/skills/ub-governance/scripts/check_skill_schema.py`
3. `task check`
