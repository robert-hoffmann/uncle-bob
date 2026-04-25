# UB Tailwind

Source: `.agents/skills/ub-tailwind/SKILL.md`

`ub-tailwind` guides Tailwind setup, migration, framework integration,
CSS-first configuration, and utility-first styling.

## When To Use It

Use it for Tailwind directives, utility workflow, `@import "tailwindcss"`,
`@theme`, plugin wiring, Vue plus Vite setup, Nuxt setup, or migration from
legacy Tailwind patterns.

## What It Changes

- detects the environment before choosing a setup recipe
- prefers current CSS-first Tailwind patterns
- avoids legacy defaults unless compatibility requires them
- bridges Tailwind tokens with raw CSS architecture

## Common Prompts

- “Use `ub-tailwind` to set up Tailwind for this Nuxt app.”
- “Review this migration away from legacy directives.”
- “Bridge these design tokens into Tailwind utilities.”

## Boundaries

Do not use it when the task is plain CSS architecture without Tailwind as the
primary surface. Use `ub-css` for that.

## Tradeoffs

Strength: keeps Tailwind setup current and framework-native.

Cost: environment detection is required; guessing the setup path creates drift.
