# Sprint PRD

## Summary

Redesign `ub-workflow`'s lifecycle and gate model so the initiative can be run
under a workflow that preserves resumability after session resets instead of
relying on placeholder sprint shells. This sprint establishes the explicit
phase model, gate vocabulary, stop-resume discipline, and pause-before-next-step
behavior that the later workflow-correction sprints and the original
repository-hardening sprints will depend on.

## Scope

1. Redefine the canonical lifecycle for `ub-workflow` so it explicitly covers
 research and discovery, PRD readiness, initiative scaffold, roadmap
 generation and approval, sprint-content preparation, sprint materialization,
 optional context refresh before execution, one-sprint execution, sprint
 closeout and review pause, final audit pause, and explicit archive review.
2. Define the gate vocabulary needed to enforce that lifecycle, including
 `research_ready`, `prd_ready`, `roadmap_ready`, `sprint_content_ready`,
 optional `sprint_start_ready`, `sprint_closeout`, `archive_ready`, and
 `initiative_complete`.
3. Decide which checkpoints are human-owned approvals versus machine-enforced
 blockers so the workflow remains rigorous without becoming bureaucratic.
4. Make the session-reset assumption explicit: written artifacts are the system
 of record, not chat history.

## Dependencies

1. This sprint has no prior sprint dependency.
2. Use the current `ub-workflow` contract surfaces in
 `./.agents/skills/ub-workflow/` and `./.github/agents/ub-workflow.agent.md`
 as the concrete baseline for redesign.
3. Use the discovered workflow gap in the current initiative's placeholder-only
 sprint generation as the motivating failure mode this sprint must correct.

## Repository Truth At Sprint Start

1. `./.agents/skills/ub-workflow/references/workflow-contract.md` currently
 compresses the lifecycle to discovery, PRD, roadmap, sprint initialization,
 sprint execution, final audit, and retained note.
2. `./.agents/skills/ub-workflow/SKILL.md` currently treats sprint
 initialization as the last planning step before execution, even though the
 current initiative proved that initialized sprint folders can still contain
 empty placeholder sprint PRDs.
3. `./.github/agents/ub-workflow.agent.md` currently routes users from roadmap
 generation to sprint initialization without a distinct sprint-preparation
 phase.
4. The current initiative already exposed the operational failure mode: the
 roadmap was rich, but the generated sprint PRDs were not execution-ready.

## Chosen Path

Rewrite the workflow contract first, then make the skill and companion agent
follow it. That keeps the lifecycle authority in one place and avoids helper,
template, or guide changes being built on top of unclear phase semantics.

## Rejected Alternative

Jump directly to helper and template changes before redefining the lifecycle
contract.

Pros:

1. Could make the current sprint-generation failure disappear quickly.
2. Produces visible artifact changes early.

Cons:

1. Leaves the underlying phase and gate semantics ambiguous.
2. Risks the helper, skill, and agent drifting in different directions.
3. Makes later test and documentation work unstable because the contract would
 still be moving.

## Affected Areas

1. `./.agents/skills/ub-workflow/references/workflow-contract.md`
2. `./.agents/skills/ub-workflow/SKILL.md`
3. `./.github/agents/ub-workflow.agent.md`
4. The current initiative roadmap and sprint pack only as downstream consumers
 of the corrected contract, not as primary implementation surfaces in this
 sprint

## Validation Plan

1. Re-read the updated workflow contract, skill, and agent together to confirm
 they all describe the same lifecycle order and the same gate vocabulary.
2. Run `npx --yes markdownlint-cli2` on the three touched workflow surfaces.
3. Record one before/after lifecycle summary and one gate glossary in
 `./evidence/` so Sprint 02 can treat the new contract as authoritative.
4. Record the explicit session-reset rule and the smallest required resume file
 set in the sprint closeout.
5. For the Level 1 `lean` governance bridge, note which checkpoints are
 deliberately human-owned approvals rather than mechanical blockers.

## Exit Criteria

1. The workflow contract, skill, and companion agent share one explicit
 lifecycle and gate model.
2. The contract explicitly covers a sprint-preparation phase before execution,
 a review pause after every sprint, and a final pause before archive.
3. Sprint closeout gives Sprint 02 a stable lifecycle contract to propagate
 across the rest of the `ub-workflow` documentation surface.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 02 should read this sprint's `closeout.md` first, then re-open the final
workflow contract, skill, and agent. Its first task is to propagate the new
lifecycle into the artifact contract, validation contract, scaffold guidance,
and user-facing workflow guide without re-opening the Sprint 01 design
decisions.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
