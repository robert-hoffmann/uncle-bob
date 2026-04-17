# Sprint PRD

## Summary

Harden `ub-workflow` so generated initiative output makes unresolved
placeholders visible and can optionally fail in strict mode when required
placeholder tokens remain unresolved. This sprint turns the current manual
placeholder discipline into a deterministic generated-artifact check without
treating the canonical internal templates as if they were themselves
violations.

## Scope

1. Define the placeholder token contract for generated initiative artifacts so
 the checker validates an explicit rule instead of ad hoc assumptions.
2. Add `check_scaffold_placeholders.py` under
 `./.agents/skills/ub-workflow/scripts/`.
3. Integrate generated-output placeholder scanning into
 `./.agents/skills/ub-workflow/scripts/scaffold_initiative.py` where it adds
 deterministic visibility or strict-mode enforcement.
4. Extend workflow regression tests with required-versus-optional placeholder
 cases and generated-artifact scope rules.

## Dependencies

1. Sprint 07 must complete first so workflow tests and CI parity are already
 in place before placeholder-hardening logic expands the workflow surface.
2. Use `./prd.md` section 11.5, section 17 phase 3, section 18 action 5, and
 the current generated sprint pack as the functional contract for this work.
3. Reuse the existing `scaffold_initiative.py` helper rather than creating a
 second competing scaffold path.

## Repository Truth At Sprint Start

1. `./.agents/skills/ub-workflow/scripts/scaffold_initiative.py` currently
 supports `create`, `init-sprints`, and `archive`, but no dedicated generated
 placeholder completeness check.
2. `unresolved_placeholder_found()` currently uses a broad string test and is
 only applied to selected control files rather than to generated initiative
 output as a first-class product surface.
3. The current initiative under
 `./.ub-workflows/initiatives/2026-04-16-repository-self-governance-hardening/`
 began with placeholder-only sprint PRDs, which is the concrete failure mode
 this sprint must make visible or prevent.
4. Placeholder validation must apply to generated initiative artifacts, not to
 canonical internal templates by default.

## Chosen Path

Add an explicit generated-output placeholder checker and integrate it
conservatively with the scaffold helper. The checker should classify required
versus optional unresolved placeholders, print deterministic summaries, and
support strict-mode failure for required tokens while leaving canonical
template files outside the default validation scope.

## Rejected Alternative

Treat any `Replace with...` or `REPLACE_` string anywhere in the repository as
an unconditional failure.

Pros:

1. Easy to implement.
2. Would catch unresolved generated placeholders quickly.

Cons:

1. Confuses canonical templates with generated initiative outputs.
2. Creates noisy failures that weaken trust in the checker.
3. Breaks the PRD's explicit scope rule for placeholder validation.

## Affected Areas

1. `./.agents/skills/ub-workflow/scripts/scaffold_initiative.py`
2. `./.agents/skills/ub-workflow/scripts/check_scaffold_placeholders.py`
3. `./.agents/skills/ub-workflow/tests/`
4. `./.agents/skills/ub-workflow/references/scaffold-helper.md`
5. `./.agents/skills/ub-workflow/references/scaffold-adaptation.md`
6. Generated initiative outputs under `./.ub-workflows/initiatives/` as test
 fixtures or smoke-test targets

## Validation Plan

1. Run the new placeholder checker directly with `uv run python` against
 generated initiative fixtures that include both required and optional
 unresolved placeholders.
2. Re-run `uv run python -m unittest discover -s .agents/skills/ub-workflow/tests
 -p 'test_*.py' -v` after adding generated-output placeholder cases.
3. Verify that canonical template files do not trigger default failures and
 record that scope decision in `./evidence/`.
4. Record one deterministic summary example and one strict-mode failure example
 under `./evidence/` so later audits can confirm the behavior remained
 explicit.
5. For the Level 1 `lean` governance bridge, record whether any placeholder
 classes remain advisory rather than blocking and why.

## Exit Criteria

1. `ub-workflow` has deterministic generated-output placeholder reporting and
 optional strict-mode failure for required unresolved placeholders.
2. Workflow regression tests cover required-versus-optional placeholder cases
 and generated-output scope discipline.
3. Sprint closeout records the placeholder contract and the exact files or
 commands Sprint 05 should treat as the new workflow baseline.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 09 should read this sprint's `closeout.md` first, then inspect the final
placeholder contract and updated workflow references. Its first task is to
document the repository packaging policy, decide the status of
`agents/openai.yaml`, and make targeted quality improvements to the most
inconsistent skill surfaces without broad churn.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
