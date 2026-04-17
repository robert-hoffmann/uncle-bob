# Sprint PRD

## Summary

Expand `ub-workflow` regression coverage so the corrected lifecycle is enforced
mechanically and the discovered rich-roadmap but empty-sprint failure mode
cannot silently reappear. This sprint turns the redesign work from Sprints 01
through 03 into scenario-based tests that cover gating, sprint preparation,
session-reset resume order, and final review pauses.

## Scope

1. Extend `test_scaffold_initiative.py` with cases for roadmap approval gating,
 sprint-content preparation, and refusal to progress when required readiness
 checkpoints are missing.
2. Add direct regression coverage for the rich-roadmap but empty-sprint failure
 mode that the current initiative exposed.
3. Add at least one session-reset resume scenario for a later sprint, proving
 that roadmap plus prior closeout plus active sprint PRD are sufficient to
 regain context unless the PRD is genuinely needed.
4. Add final-audit pause and explicit archive-readiness coverage so the review
 checkpoint before archive is mechanically protected.

## Dependencies

1. Sprint 03 must complete first so the helper and template behaviors under
 test are already defined.
2. Use the current initiative's original empty-sprint failure mode and the
 redesigned helper behavior as the primary scenario inputs.
3. Reuse and extend `./.agents/skills/ub-workflow/tests/test_scaffold_initiative.py`
 before creating any second workflow test suite.

## Repository Truth At Sprint Start

1. The existing workflow regression suite currently covers `create`,
 `init-sprints`, and `archive`, but it does not yet protect the new
 sprint-preparation lifecycle or session-reset resume semantics.
2. The discovered failure mode is concrete and reproducible: the roadmap can be
 detailed while sprint PRDs are still placeholder-only.
3. The workflow redesign is not complete until those behaviors are protected by
 tests and can fail loudly when they regress.

## Chosen Path

Extend the existing workflow test module with scenario-style cases that map
directly to the corrected lifecycle. That keeps regression logic discoverable
and ties the new behavior to the same helper entrypoints and initiative surfaces
already used in the repository.

## Rejected Alternative

Rely on manual smoke testing of the redesigned workflow without expanding the
automated regression suite.

Pros:

1. Lower short-term implementation effort.
2. Fewer fixtures to maintain.

Cons:

1. Leaves the exact discovered failure mode free to regress.
2. Makes session-reset resume behavior a matter of operator memory.
3. Weakens trust in the workflow redesign because the critical behaviors would
 still be enforced socially rather than mechanically.

## Affected Areas

1. `./.agents/skills/ub-workflow/tests/test_scaffold_initiative.py`
2. Any small workflow fixture inputs needed to model prepared sprint packs,
 pending handoff markers, or final-audit states
3. Potentially `./Taskfile.yml` or workflow test wiring only if the new tests
 require an updated invocation path

## Validation Plan

1. Run `uv run python -m unittest discover -s .agents/skills/ub-workflow/tests
 -p 'test_*.py' -v` and record the final output in `./evidence/`.
2. Confirm at least one new regression test would have failed on the original
 placeholder-only sprint behavior before the redesign.
3. Confirm at least one resume scenario exercises a later sprint after a
 session reset and documents the expected read order.
4. Run `npx --yes markdownlint-cli2` on any touched workflow test-facing docs
 or fixtures if they are Markdown-based.
5. For the Level 1 `lean` governance bridge, record the final test coverage map
 for lifecycle, placeholder, and archive-review behavior.

## Exit Criteria

1. The corrected workflow lifecycle is protected by automated regression tests.
2. The exact discovered failure mode is covered by at least one deterministic
 regression case.
3. Sprint closeout gives Sprint 05 an implementation-ready workflow baseline so
 the original repository-hardening work can begin under the corrected
 orchestration model.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 05 should read this sprint's `closeout.md` first, then verify the final
workflow contract, helper behavior, and regression outputs. Its first task is
to begin the original hardening work by aligning the public inventory and
metadata surfaces under the now-corrected `ub-workflow` lifecycle.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
