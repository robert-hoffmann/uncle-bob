# Sprint PRD

## Summary

Redesign the workflow helper and sprint template so the corrected lifecycle can
produce execution-ready sprint PRDs instead of generic placeholder shells. This
sprint should keep deterministic scaffold operations conservative, but add an
explicit sprint-preparation phase and the richer roadmap parsing needed to turn
the roadmap into real sprint artifacts before execution starts.

## Scope

1. Redesign `roadmap_sprint_entries()` so the helper can extract title, path,
 goal, dependencies, validation focus, subtasks, and evidence folder from
 the roadmap.
2. Add or model an explicit `prepare-sprints` phase so sprint content can be
 authored before execution without hiding deep planning inside
 `init-sprints`.
3. Redesign the sprint template so roadmap-derived sections and
 human-authored-reasoning sections are clearly separated.
4. Update helper readiness and placeholder logic so blocking machine
 placeholders and allowed pending handoff markers are not treated as the same
 thing.

## Dependencies

1. Sprint 02 must complete first so the helper and template redesign can follow
 a stable documented lifecycle and contract surface.
2. Use the current initiative's roadmap and sprint pack as the concrete example
 of the failure mode the new helper behavior must solve.
3. Reuse the existing deterministic helper entrypoints where possible instead
 of inventing a second workflow system.

## Repository Truth At Sprint Start

1. `./.agents/skills/ub-workflow/scripts/scaffold_initiative.py` currently
 supports `create`, `init-sprints`, and `archive`, but no explicit
 sprint-content-preparation step.
2. The current helper parser extracts only sprint title and path from the
 roadmap, not the richer metadata already present in the Sprint Sequence
 entries.
3. The current sprint template is a generic placeholder shell rather than a
 pre-execution sprint PRD.
4. The current initiative originally proved that rich roadmap data does not, by
 itself, guarantee useful sprint PRDs unless the helper or workflow turns
 that data into written sprint content.

## Chosen Path

Keep deterministic scaffold operations explicit and conservative, but add an
equally explicit sprint-preparation step that authors sprint PRDs from the PRD,
roadmap, and initiative state before execution begins. That preserves review
clarity and makes session-reset recovery depend on written artifacts rather
than regenerated chat reasoning.

## Rejected Alternative

Hide deep sprint authoring inside `init-sprints` so one command both creates
directories and silently generates sprint content.

Pros:

1. Fewer visible commands.
2. Faster path from roadmap approval to generated sprint pack.

Cons:

1. Blurs the boundary between deterministic scaffold operations and model-led
 planning.
2. Makes it harder for users to review sprint PRDs before execution.
3. Increases the chance that helper behavior and documented lifecycle will drift
 again.

## Affected Areas

1. `./.agents/skills/ub-workflow/scripts/scaffold_initiative.py`
2. `./.agents/skills/ub-workflow/assets/initiative-template/sprint-template/sprint.md`
3. Potentially `./.agents/skills/ub-workflow/references/scaffold-helper.md` and
 adjacent references where helper behavior must be described precisely
4. The current initiative roadmap and sprint pack as smoke-test targets for the
 redesigned helper behavior

## Validation Plan

1. Use targeted helper dry runs and controlled generated initiative fixtures to
 prove the richer roadmap parser extracts the expected sprint metadata.
2. Run `npx --yes markdownlint-cli2` on the touched template and helper-facing
 docs.
3. Record at least one before/after sprint example in `./evidence/` showing a
 placeholder-only sprint PRD transformed into an execution-ready one.
4. Record the precise behavior of pending handoff markers so Sprint 04 can turn
 it into regression coverage.
5. For the Level 1 `lean` governance bridge, record which parts of the helper
 change are deterministic versus model-authored and why that boundary was
 chosen.

## Exit Criteria

1. The helper and template design support real sprint-content preparation before
 execution.
2. The roadmap parser can consume the richer Sprint Sequence metadata already
 present in the initiative roadmap.
3. Sprint closeout gives Sprint 04 the exact behaviors that now need
 regression-test protection.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 04 should read this sprint's `closeout.md` first, then inspect the final
helper behavior and template semantics. Its first task is to convert the newly
defined lifecycle, parser, and placeholder behaviors into deterministic
regression and session-reset resume scenarios.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
