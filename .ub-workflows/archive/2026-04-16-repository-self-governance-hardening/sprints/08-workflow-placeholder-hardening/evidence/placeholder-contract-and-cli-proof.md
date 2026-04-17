# Sprint 08 Evidence

## Placeholder Contract

Sprint 08 defined the generated-output placeholder contract in
`./.agents/skills/ub-workflow/references/placeholder-contract.md`.

Contract summary:

1. Validation scope is generated initiative output, not canonical internal
   templates.
2. `REPLACE_*` tokens are always required in generated initiative output.
3. Plain-language `Replace with ...` prompts are required in `roadmap.md` and
   `sprints/*/sprint.md`.
4. Plain-language `Replace with ...` prompts are advisory in `prd.md` and
   generated `closeout.md` files.
5. `PENDING_HANDOFF:` markers are advisory.
6. Fenced-code examples and quoted prose about placeholder strings are not
   treated as unresolved generated-output placeholders.

## Implemented Surfaces

Sprint 08 added or updated these workflow surfaces:

1. `./.agents/skills/ub-workflow/scripts/check_scaffold_placeholders.py`
2. `./.agents/skills/ub-workflow/scripts/scaffold_initiative.py`
3. `./.agents/skills/ub-workflow/tests/test_scaffold_initiative.py`
4. `./.agents/skills/ub-workflow/references/placeholder-contract.md`
5. `./.agents/skills/ub-workflow/references/scaffold-helper.md`
6. `./.agents/skills/ub-workflow/references/scaffold-adaptation.md`
7. `./.agents/skills/ub-workflow/SKILL.md`

## Disposable CLI Proof

Sprint 08 validated three direct CLI behaviors against disposable initiative
roots:

1. `create` prints a generated-output placeholder summary immediately after
   scaffolding.
2. `check_scaffold_placeholders.py --strict` fails for placeholder-only sprint
   shells created by `init-sprints` before roadmap-derived sprint preparation.
3. `prepare-sprints --strict-placeholders` passes once the sprint PRDs are
   rendered and only advisory findings remain.

Observed proof points:

1. Create-state scan reported required roadmap placeholders plus advisory PRD
   prompts, making the incomplete generated output visible without blocking by
   default.
2. Strict init-state scan exited non-zero with unresolved `REPLACE_SPRINT_*`
   findings in the generated `sprint.md` shell.
3. Strict prepare-state scan completed successfully with `0 required` findings
   and only advisory PRD prompts, generated closeout prompts, and
   `PENDING_HANDOFF:` markers remaining.

## Live Initiative Scan

Direct command:

1. `uv run python .agents/skills/ub-workflow/scripts/check_scaffold_placeholders.py ./.ub-workflows/initiatives/2026-04-16-repository-self-governance-hardening --format json`

Result:

1. `status: pass`
2. `requiredCount: 0`
3. `advisoryCount: 32`

The advisory findings are expected `PENDING_HANDOFF:` reminders in the Sprint 08
closeout plus future-closeout authoring prompts in Sprint 09 through Sprint 11.
No blocking generated-output placeholder findings remain in the active
initiative state.

## Regression Coverage

Workflow regression coverage now proves:

1. create-time placeholder visibility
2. strict failure on placeholder-only sprint shells
3. strict success after prepared sprint rendering when only advisory findings
   remain
4. ignored code examples and quoted prose about placeholder strings
