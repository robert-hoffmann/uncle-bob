# UB Quality

Source: `.agents/skills/ub-quality/SKILL.md`

`ub-quality` is the companion baseline for clear, reviewable agent work. It
pushes the agent to explain choices, preserve scope, format touched content
consistently, and validate what changed.

## When To Use It

Use it whenever the task involves code, docs, review, planning, refactoring, or
structured explanation. In this skill set, it is the always-on quality layer
that travels with other skills.

## What It Changes

- asks for real tradeoffs instead of one unexamined answer
- keeps edits scoped to the touched logical area
- applies documentation and readability rules to user-facing output
- enforces alignment and formatting rules in touched eligible blocks
- distinguishes repository policy from portable defaults

## Common Prompts

- “Use `ub-quality` to review this plan for missing tradeoffs.”
- “Apply `ub-quality` while cleaning up this documentation.”
- “Check whether this refactor is too broad for the requested scope.”

## Boundaries

Do not use `ub-quality` as the owner of language, framework, or runtime
decisions. Pair it with the domain skill that owns the work.

## Tradeoffs

Strength: makes agent output more consistent and easier to review.

Cost: strict formatting and documentation rules can feel heavy for tiny edits.
