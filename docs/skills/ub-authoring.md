# UB Authoring

Source: `.agents/skills/ub-authoring/SKILL.md`

`ub-authoring` shapes reusable, installable skill guidance. It treats skill
descriptions as routing metadata, keeps reusable guidance portable, and moves
deeper detail into references instead of bloating the main skill file.

## Core Principles

- Write descriptions for routing, not marketing.
- Make non-use boundaries explicit when misrouting is likely or costly.
- Prefer concrete examples and acceptance boundaries over vague advice.
- Keep `SKILL.md` lean and move deeper reusable guidance into references.
- Keep shared conventions portable across installed skill payloads.
- Use shared choice-question UX where path selection matters.

## Behavior In Practice

- Rewrites descriptions so they behave like activation rules: concrete task
  triggers, clear owned surfaces, and explicit exclusions when another skill
  should win.
- Adds "when not to use" guidance where misrouting would be expensive, such
  as confusing reusable skill authoring with normal app implementation.
- Moves deep reusable guidance into targeted references, but keeps the main
  skill strong enough to work without loading the whole catalog.
- Favors concrete examples, output expectations, and acceptance boundaries
  over vague words like "improve" or "handle better".
- Normalizes naming so skill ids, file names, and generated surfaces are
  predictable for both humans and routing systems.
- Reuses the shared choice-question contract for prompts that affect path
  selection, so users see a short, comparable set of options instead of an
  open-ended interview.
- Keeps optional adoption bundles and config-aware scaffolding separate from
  the core skill contract so installed skills stay portable.

## Reference Highlights

- `.agents/skills/ub-authoring/references/authoring-conventions.md`: routing
  descriptions, non-use boundaries, output expectations, concrete examples,
  naming, anti-pattern notes, progressive disclosure, config-aware
  scaffolding, optional adoption bundles, and shared choice-question behavior.

## Progressive Disclosure

Most authoring tasks only need the main skill. The authoring conventions
reference becomes important when the work changes shared patterns such as
description style, routing quality, naming, reusable references, or
multiple-choice user prompts.

## Common Invocation Examples

- “Use `ub-authoring` to improve this skill description.”
- “Check whether this guidance belongs in the skill or in repo docs.”
- “Add non-use boundaries so this skill does not trigger for normal code work.”
- “Make this reusable reference portable for installed skill users.”

## Boundaries

Do not use it for ordinary app implementation. Use `ub-customizations` when the
task is building a full skill, hook, MCP config, or bundle.

## Tradeoffs

Strength: improves skill activation quality and keeps reusable guidance
portable.

Cost: it can expose ambiguity between reusable skill guidance and local
repository documentation, which may require a deliberate placement decision.
