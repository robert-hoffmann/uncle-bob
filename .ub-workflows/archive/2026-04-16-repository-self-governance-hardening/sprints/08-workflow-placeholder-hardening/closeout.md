# Sprint Closeout

## environment_note

Executed in the local macOS workspace at
`/Users/itechnology/Dev/itech-agents`. Sprint 08 changed the ub-workflow
helper, added a direct placeholder-check CLI, expanded the workflow regression
suite, and updated the ub-workflow references to define the generated-output
placeholder contract explicitly.

## scope_note

This sprint defined the placeholder token contract for generated initiative
artifacts, added `check_scaffold_placeholders.py`, integrated deterministic
placeholder reporting and optional strict enforcement into
`scaffold_initiative.py`, and extended ub-workflow regression coverage for
required-versus-advisory behavior. It did not change repository packaging
policy or skill-surface uplift work; that remains Sprint 09. Governance bridge:
`Level 1`, profile `lean`.

## decision_note

Chosen path: classify generated-output placeholders explicitly, scan only the
generated initiative artifact surface by default, and separate required
blocking findings from advisory authoring prompts so strict mode can be useful
without treating canonical templates or prose examples as failures.

Rejected alternative: treat any `Replace with...` or `REPLACE_` string anywhere
in the repository as an unconditional failure.

Pros of the rejected alternative:

1. Very small implementation surface.
2. Fast to explain.

Cons of the rejected alternative:

1. It confuses canonical templates and generated output.
2. It flags prose examples and code fences instead of only unresolved output.
3. It creates enough false positives to weaken trust in strict mode.

## gate_note

sprint_closeout: pass

Sprint 08 completed the generated-output placeholder contract, the direct CLI
checker, the scaffold-helper integration, and the workflow regression coverage.
The live initiative now scans with `0 required` placeholder findings and only
advisory future-closeout prompts.

confidence: pass

When governance is active, also record the governance gate type and result as
`merge|confidence|release: pass|fail|blocked`.

## exception_note

none

When governance is active, reference exception records that use the canonical
governance exception metadata.

## validation_note

Validation commands and outcomes:

1. `uv run ruff check .agents/skills/ub-workflow/scripts .agents/skills/ub-workflow/tests/test_scaffold_initiative.py`

   Result: pass.

2. `uv run python -m unittest discover -s .agents/skills/ub-workflow/tests -p 'test_*.py' -v`

   Result: pass with 20 workflow regression tests, including the new
   placeholder visibility, strict-failure, strict-success, and false-positive
   avoidance cases.

3. `uv run python .agents/skills/ub-workflow/scripts/check_scaffold_placeholders.py ./.ub-workflows/initiatives/2026-04-16-repository-self-governance-hardening --format json`

   Result: pass with `requiredCount: 0` and `advisoryCount: 32`; the live
   initiative only retains advisory Sprint 08 handoff reminders plus future
   closeout authoring prompts.

4. Disposable initiative CLI proof:

   Result: confirmed create-time placeholder visibility, strict failure on
   placeholder-only sprint shells after `init-sprints`, and strict success
   after `prepare-sprints --strict-placeholders` when only advisory findings
   remained.

5. `task check`

   Result: pass after the ub-workflow placeholder checker, helper changes, and
   references were added.

Documentation and synchronized-artifact validation:

1. `references/placeholder-contract.md` records the canonical required versus
   advisory contract.
2. `references/scaffold-helper.md` documents the new checker and the
   `--strict-placeholders` helper flags.
3. `references/scaffold-adaptation.md` now points to the explicit enforcement
   rules for generated initiative output.
4. `SKILL.md` now tells operators when to load the placeholder contract.

TG001-TG005 note:

1. No separate TG001-TG005 product test run was required. This sprint changed
   workflow helper behavior and workflow regressions, and the updated
   ub-workflow test suite passed.

Governance-level validation note:

1. Profile: `lean`
2. Evidence path: `./evidence/placeholder-contract-and-cli-proof.md`
3. Advisory-only classes retained by design: `prd.md` authoring prompts,
   generated `closeout.md` prompts, and `PENDING_HANDOFF:` markers

Also record any documentation or synchronized-artifact validation that was required for this sprint.

When tests changed, record whether TG001-TG005 checks were run and what they
reported.

When governance is active, record governance-level validation commands, profile,
ADR references, and evidence paths that informed the gate decision.

## done_verification_note

Sprint 08 definition of done is satisfied.

1. Planned functionality implemented: yes
2. Known in-scope errors still open: none
3. Required quality gates green: yes
4. Relevant docs and synchronized artifacts updated or explicitly unchanged:
   updated
5. Validation evidence recorded: yes

Minimum questions to answer:

1. Is the planned functionality implemented?
2. Are there any known in-scope errors still open?
3. Are the required project quality gates green, including TG001-TG005 checks
   when tests changed?
4. Are the relevant docs and synchronized artifacts updated or explicitly unchanged?
5. Is the validation evidence recorded?

## handoff_note

1. Finished: ub-workflow now has an explicit placeholder contract, a direct
   generated-output checker, scaffold-helper summary reporting, strict
   placeholder enforcement hooks, and regression coverage for both blocking and
   advisory classes.
2. Open: repository packaging policy and targeted skill-surface uplift remain
   for Sprint 09.
3. Next recommended action: start Sprint 09 - Packaging Policy And Targeted
   Skill Uplift.
4. The next sprint should read this closeout first, then inspect
   `references/placeholder-contract.md`,
   `scripts/check_scaffold_placeholders.py`,
   `scripts/scaffold_initiative.py`, and the updated ub-workflow tests.

## follow_up_note

No additional follow-up work was requested during Sprint 08 beyond the planned
Sprint 09 packaging and skill-uplift work. The placeholder contract now leaves
`prd.md`, generated `closeout.md`, and `PENDING_HANDOFF:` findings advisory by
design; later sprints can tighten those classes only if the workflow model
changes deliberately.

For the final audit sprint, answer at minimum:

1. Was the user asked whether they want follow-up audits or refactors?
2. Which follow-up items were requested, if any?
3. Which follow-up items were explicitly declined, if any?
4. Did the final validation and documentation synchronization checks pass?
5. Are any governance exceptions, ADR waivers, or follow-up validation items
   still open?
