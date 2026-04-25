# UB Workflow

Source: `.agents/skills/ub-workflow/SKILL.md`

`ub-workflow` is the planning and delivery skill. It decides whether work can
stay direct, needs a lightweight spec, or should become a full initiative with
roadmap, prepared sprints, closeout, final audit, and retained notes.

## When To Use It

Use it when work is ambiguous, planning-heavy, multi-step, risky,
cross-cutting, or likely to continue across sessions.

## What It Changes

- chooses the smallest safe planning lane
- promotes work out of chat-only state when durable context is needed
- uses gates before initiative work advances
- makes reviewed-mode checkpoints explicit
- keeps stop-resume handoffs recoverable

## Common Prompts

- “Use `ub-workflow` to turn this idea into the right planning surface.”
- “Create a lightweight spec for this bounded change.”
- “Scaffold an initiative from this PRD.”
- “Prepare the next sprint, but do not start execution yet.”

## Boundaries

Do not use it for governance-only evidence decisions. Use `ub-governance` for
gate semantics, evidence depth, testing posture, and ADR escalation.

## Tradeoffs

Strength: prevents large work from living only in chat history.

Cost: initiatives add process and should be reserved for work that benefits
from staged execution.

## Deep Dive

See [UB Workflow deep dive](/deep-dives/ub-workflow).
