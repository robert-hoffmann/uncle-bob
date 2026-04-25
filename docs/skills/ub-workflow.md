# UB Workflow

Source: `.agents/skills/ub-workflow/SKILL.md`

`ub-workflow` is the planning and delivery skill. It decides whether work can
stay direct, needs a lightweight spec, or should become a full initiative with
roadmap, prepared sprints, closeouts, final audit, and retained notes.

For the detailed lane and mode model, read the
[UB Workflow deep dive](/deep-dives/ub-workflow).

## Core Principles

- Choose the smallest safe planning lane before opening durable artifacts.
- Promote out of chat-only state when assumptions, options, validation, or
  staged execution need to survive handoff.
- Treat lightweight specs as a real lane, not a weak initiative.
- Treat initiative roadmaps as the durable post-plan artifact.
- Do not start sprint execution from placeholder-only sprint shells.
- In reviewed mode, preview before execution and wait for explicit approval.
- End initiatives with final audit, retained note, and human review before
  archive.

## Behavior In Practice

- Makes the lane choice visible: direct bounded work, lightweight spec, or
  initiative. It promotes out of direct work when planning, assumptions,
  options, validation, or handoff state need a durable record.
- Uses lightweight specs for bounded work that still needs a written contract.
  A spec is not treated as a failed initiative; it is the right lane for
  medium planning that should remain small.
- Uses initiatives when the work needs PRD-level decomposition, roadmap
  sequencing, resumable sprint execution, final audit, and retained memory.
- Keeps `prd.md` self-contained before generating `roadmap.md`, then treats
  `roadmap.md` as the durable progress surface for resume.
- Separates preparation from execution. Sprint folders or placeholder shells
  are not enough; each sprint needs standalone content before it can start.
- Preserves human control in `reviewed` mode: next-sprint requests open a
  preview first, and execution waits for one explicit start approval.
- Tracks mode differences without weakening gates: `flow` reduces pre-work
  ceremony, `auto` advances unless interrupted, and `continuous` or `yolo`
  removes routine pause points while still requiring internal artifact updates.
- Ends with a final audit, retained note, and archive decision instead of
  leaving the last sprint as the only memory of the initiative.

## Reference Highlights

- `.agents/skills/ub-workflow/references/workflow-contract.md`: lifecycle,
  lane promotion, interaction modes, reviewed-mode checkpoints, execution
  rules, pause behavior, and resume order.
- `.agents/skills/ub-workflow/references/artifact-contracts.md`: required
  contents for initiative roots, lightweight specs, sprint PRDs, decision
  logs, closeouts, rollups, retained notes, and archive-ready state.
- `.agents/skills/ub-workflow/references/validation-and-completion.md`: gate
  readiness, closeout evidence, final-audit expectations, and completion
  criteria.
- `.agents/skills/ub-workflow/references/scaffold-helper.md`: deterministic
  scaffold helper behavior, operation-root bootstrapping, safe rerun rules,
  and placeholder handling.
- `.agents/skills/ub-workflow/references/governance-bridge.md`: how workflow
  artifacts coordinate with governance evidence only when explicit escalation
  is in scope.

## Progressive Disclosure

The main skill is enough for lane choice and ordinary workflow routing. The
references load when the task reaches a specific phase: artifact creation,
roadmap readiness, sprint closeout, helper use, placeholder validation, or
explicit governance alignment.

This keeps small bounded work light while giving large initiatives a durable
operating system.

## Common Invocation Examples

- “Use `ub-workflow` to turn this idea into the right planning surface.”
- “Create a lightweight spec for this bounded change.”
- “Scaffold an initiative from this PRD.”
- “Prepare the next sprint, but do not start execution yet.”
- “Explain the difference between reviewed mode and yolo mode.”

## Boundaries

Do not use it for governance-only evidence decisions. Use `ub-governance` for
gate semantics, evidence depth, testing posture, and ADR escalation.

## Tradeoffs

Strength: prevents large work from living only in chat history and gives later
operators a reliable resume path.

Cost: initiatives add process and should be reserved for work that benefits
from staged execution.

## Deep Dive

See [UB Workflow deep dive](/deep-dives/ub-workflow) for lane choice,
interaction modes, initiative lifecycle, and approval checkpoints.
