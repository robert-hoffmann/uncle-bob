# Sprint PRD

## Summary

Propagate the new `ub-workflow` lifecycle across every workflow-facing
reference and guide so the system has one coherent story. This sprint makes the
skill, companion agent, artifact contract, validation rules, scaffold
adaptation guidance, scaffold-helper guidance, and user guide all describe the
same sprint-preparation-first workflow instead of leaving the phase model
partially implicit.

## Scope

1. Update the artifact contract so `sprint.md` is explicitly an execution-ready
 sprint PRD rather than a starter shell.
2. Update the validation and completion contract so `research_ready`,
 `sprint_content_ready`, optional `sprint_start_ready`, and final archive
 review semantics become explicit readiness checks.
3. Update scaffold-adaptation and scaffold-helper guidance so sprint
 preparation is described as a separate phase before sprint materialization or
 execution.
4. Update the user guide and broader agent wording so the user-facing story
 matches the corrected lifecycle without requiring literal slash commands.

## Dependencies

1. Sprint 01 must complete first so the lifecycle and gate model are already
 stable before this sprint propagates them.
2. Use the finalized Sprint 01 contract, gate glossary, and session-reset rules
 as the authoritative inputs for these documentation and guide changes.
3. Reuse the current `ub-workflow` references and user guide rather than
 inventing parallel docs.

## Repository Truth At Sprint Start

1. The artifact contract currently says each sprint must stand alone, but the
 sprint template and helper behavior have historically allowed placeholder
 sprint shells.
2. The validation contract currently treats sprint initialization as the last
 planning barrier before execution and does not name a separate
 sprint-content-ready phase.
3. Scaffold-adaptation and scaffold-helper guidance currently route users from
 roadmap approval to `init-sprints` without a distinct sprint-preparation
 step.
4. The user guide still teaches roadmap approval followed by sprint-set
 initialization as the immediate path into execution.

## Chosen Path

Update the contracts and guides in place so there is one canonical explanation
of the new lifecycle. This keeps the workflow teachable and prevents later
helper or template work from silently redefining behavior that the docs still
describe incorrectly.

## Rejected Alternative

Leave the documentation surfaces mostly unchanged and rely on helper behavior
alone to teach the new workflow.

Pros:

1. Reduces immediate documentation churn.
2. Keeps the redesign concentrated in scripts.

Cons:

1. Leaves contradictory user guidance across the workflow surfaces.
2. Makes the workflow harder to resume correctly after a session reset.
3. Undermines trust because the docs would still teach the old path.

## Affected Areas

1. `./.agents/skills/ub-workflow/references/artifact-contracts.md`
2. `./.agents/skills/ub-workflow/references/validation-and-completion.md`
3. `./.agents/skills/ub-workflow/references/scaffold-adaptation.md`
4. `./.agents/skills/ub-workflow/references/scaffold-helper.md`
5. `./.agents/skills/ub-workflow/docs/user-guide.md`
6. `./.github/agents/ub-workflow.agent.md` for the broader wording cleanup

## Validation Plan

1. Run `npx --yes markdownlint-cli2` on every touched `ub-workflow` reference,
 guide, and agent file.
2. Re-read the touched files in sequence to confirm none of them still imply
 that roadmap approval followed by `init-sprints` is sufficient for
 execution.
3. Record one normalized lifecycle summary and one user-facing resume order in
 `./evidence/` so Sprint 03 can treat those documents as the new reference
 surfaces.
4. Record any intentionally deferred wording cleanup in the sprint closeout so
 Sprint 03 does not accidentally re-open contract decisions.
5. For the Level 1 `lean` governance bridge, note which workflow requirements
 remain guidance versus enforced behavior pending helper changes in Sprint 03.

## Exit Criteria

1. All `ub-workflow` contracts and guides describe the same lifecycle,
 including sprint preparation before execution.
2. No touched reference or guide still teaches placeholder-only sprint shells
 as an acceptable execution state.
3. Sprint closeout gives Sprint 03 a stable documentation and contract baseline
 for helper and template redesign.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 03 should read this sprint's `closeout.md` first, then re-open the final
artifact and validation contracts. Its first task is to redesign the helper and
sprint template so the lifecycle described in the docs can actually be enforced
in generated initiative output.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
