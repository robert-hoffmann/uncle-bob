# Initiative Rollup

Status: not started

## Purpose

Use this file as the readable cross-sprint summary for the initiative.

Keep raw sprint proof in each sprint's `./evidence/` folder, keep sprint
execution intent in each `./sprint.md`, keep running sprint decisions in each
`./decision-log.md`, and use this file to summarize the parts a future reader
should not have to reconstruct by opening every sprint directory in order.

## Current Snapshot

- Read `./README.md` for the live phase, gate, and next-step state.
- Read `./roadmap.md` for the ordered sprint checklist and dependency chain.
- Update this file whenever a sprint materially changes later-sprint
  assumptions, direction, or validation posture.

## Major Decisions

- Record the cross-sprint decisions that later work should preserve.
- Summarize why the decision mattered and point to the owning sprint artifact
  when that adds useful detail.

## Sprint Highlights

- Summarize each active or completed sprint in a few lines.
- Point to the relevant sprint `decision-log.md`, `closeout.md`, and
  `evidence/` folder when a later reader needs deeper traceability.

## Cross-Sprint Risks And Deferrals

- Record risks, deferrals, or follow-up conditions that span more than one
  sprint.
- Keep sprint-local issues in the owning sprint unless they materially affect
  later work.

## Validation And Evidence Rollup

- Summarize the major initiative-level validation signals and where they live.
- Point to the owning sprint `evidence/` folders instead of copying raw logs
  into this file.

## Research And Exceptions Pointers

- Use `./research/` only for supportive discovery worth retaining across
  sprints.
- Use `./exceptions/` only for explicit bounded exception records.
- Keep routine sprint reasoning out of those folders; put it in sprint
  `decision-log.md` files and this `rollup.md` instead.
