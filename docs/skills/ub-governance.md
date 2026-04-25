# UB Governance

Source: `.agents/skills/ub-governance/SKILL.md`

`ub-governance` is the control skill. It helps decide how much evidence,
testing scrutiny, exception handling, ADR alignment, or release discipline a
change needs.

## When To Use It

Use it when the question is about risk, validation quality, governance gates,
test signal, exceptions, evidence, or whether a decision needs a durable
record.

## What It Changes

- defaults to the lean profile for ordinary work
- escalates to advanced controls only with explicit rationale
- separates workflow gates from governance gates
- treats bounded exceptions as structured records
- keeps ADR and claim machinery for durable or high-risk decisions

## Common Prompts

- “Use `ub-governance` to decide whether this needs an ADR.”
- “Review this test plan for low-signal testing patterns.”
- “Check whether this exception is bounded enough.”
- “Explain the lean versus advanced governance choice.”

## Boundaries

Do not use it as a general workflow planner. Use `ub-workflow` to choose
delivery lanes and sprint flow.

## Tradeoffs

Strength: keeps ordinary work lightweight while preserving escalation paths.

Cost: advanced governance adds overhead and should be activated deliberately.

## Deep Dive

See [UB Governance deep dive](/deep-dives/ub-governance).
