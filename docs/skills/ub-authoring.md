# UB Authoring

Source: `.agents/skills/ub-authoring/SKILL.md`

`ub-authoring` helps create and improve reusable skill guidance. It treats
descriptions as routing metadata, not marketing copy.

## When To Use It

Use it when changing skill instructions, shared skill references, routing
boundaries, naming, or portable authoring conventions.

## What It Changes

- makes “when to use this skill” concrete
- adds “do not use for” boundaries where misrouting is likely
- keeps reusable guidance portable across installed skill payloads
- moves deeper detail into references instead of overloading `SKILL.md`

## Common Prompts

- “Use `ub-authoring` to improve this skill description.”
- “Check whether this guidance belongs in the skill or in repo docs.”
- “Add non-use boundaries so this skill does not trigger for normal code work.”

## Boundaries

Do not use it for ordinary app implementation. Use `ub-customizations` when the
task is building a full skill, hook, MCP config, or bundle.

## Tradeoffs

Strength: improves skill activation quality and portability.

Cost: can expose ambiguity between reusable guidance and local documentation.
