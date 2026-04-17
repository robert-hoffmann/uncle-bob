# Placeholder Contract

This contract defines how `ub-workflow` treats unresolved placeholders in
generated initiative artifacts.

## Scope

Default placeholder validation applies to generated initiative output only.

Covered artifact paths:

1. `README.md`
2. `roadmap.md`
3. `prd.md`
4. `retained-note.md`
5. `sprints/*/sprint.md`
6. `sprints/*/closeout.md`

Default placeholder validation does not treat the canonical internal templates
under `assets/initiative-template/` or `assets/operations-root/` as failures.

## Placeholder Classes

### Required

Required unresolved placeholders block strict-mode success.

Rules:

1. Any `REPLACE_*` token in a generated artifact is required.
2. Any plain-language `Replace with ...` prompt in `roadmap.md` is required.
3. Any plain-language `Replace with ...` prompt in `sprints/*/sprint.md` is
   required.

### Advisory

Advisory unresolved placeholders stay visible in reports but do not fail
strict mode.

Rules:

1. Plain-language `Replace with ...` prompts in `prd.md` are advisory because
   PRD authoring can still be in progress.
2. Plain-language `Replace with ...` prompts in `sprints/*/closeout.md` are
   advisory because closeout completion happens after execution, not before it.
3. `PENDING_HANDOFF:` markers in prepared sprint PRDs are advisory because they
   are explicit carry-forward reminders, not machine placeholders.

## Generated-Output Behavior

The scaffold helper and standalone checker should:

1. print deterministic placeholder summaries for generated initiative output
2. distinguish required versus advisory findings explicitly
3. support strict-mode failure when required findings remain
4. keep canonical internal templates outside the default validation scope

## Intended Use

Use strict mode when you need a generated initiative artifact set to be ready
for the next workflow phase.

Examples:

1. `init-sprints --strict-placeholders` should fail if the generated sprint
   shells still contain `REPLACE_*` machine placeholders.
2. `prepare-sprints --strict-placeholders` should pass when roadmap-derived
   sprint PRDs are rendered and only advisory closeout or handoff prompts
   remain.
3. `check_scaffold_placeholders.py --strict` should fail only on required
   generated-output findings.
