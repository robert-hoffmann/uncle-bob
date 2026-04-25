# UB Customizations

Source: `.agents/skills/ub-customizations/SKILL.md`

`ub-customizations` helps choose and build reusable agent customization
artifacts: skills, hooks, MCP configs, and bundles.

## When To Use It

Use it when the user wants to create, update, review, or package a reusable
agent customization rather than simply implement application code.

## What It Changes

- classifies the artifact before generating it
- chooses the smallest sufficient customization surface
- distinguishes soft guidance from deterministic automation
- keeps validation and packaging concerns visible

## Common Prompts

- “Use `ub-customizations` to decide whether this should be a skill or hook.”
- “Create a skill for this reusable workflow.”
- “Review this MCP config and companion skill design.”

## Boundaries

Do not use it for general code implementation or governance-only decisions.
Use `ub-authoring` when the work is only reusable wording or routing quality.

## Tradeoffs

Strength: prevents overbuilding customization systems.

Cost: artifact classification can require an interview before implementation.
