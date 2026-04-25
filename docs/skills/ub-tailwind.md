# UB Tailwind

Source: `.agents/skills/ub-tailwind/SKILL.md`

`ub-tailwind` guides Tailwind setup, migration, framework integration,
CSS-first configuration, design tokens, and utility-first styling.

## Core Principles

- Detect the target environment before choosing a Tailwind recipe.
- Prefer modern CSS entrypoints and CSS-first configuration patterns.
- Keep setup minimal and framework-native.
- Centralize design tokens where Tailwind and raw CSS can stay aligned.
- Treat JavaScript config and legacy directives as compatibility paths, not
  new defaults.
- Use migration references when replacing legacy syntax or setup patterns.
- Coordinate with `ub-css` when token architecture or raw CSS layers matter.

## Behavior In Practice

- Detects the environment before writing setup instructions: standalone HTML,
  Vue plus Vite, Nuxt, CSS entrypoint location, build plugins, and existing
  dependencies all change the correct recipe.
- Defaults to modern CSS-first Tailwind usage with `@import "tailwindcss"`
  and CSS directives such as `@theme`, `@utility`, `@variant`,
  `@custom-variant`, `@source`, and `@reference` where they apply.
- Uses the official Vite plugin path for Vue plus Vite projects and the Nuxt
  framework recipe through Nuxt config rather than inventing a separate
  Vue-only Vite setup for Nuxt.
- Treats PostCSS, `@config`, `@plugin`, and JavaScript config files as
  compatibility paths, not fresh defaults.
- Centralizes design tokens in `@theme` so utility classes and raw CSS consume
  the same semantic values.
- Uses `@reference` in component-scoped styles when utilities or variants need
  access to the main stylesheet context without duplicating imported CSS.
- Applies migration guidance to replace deprecated directives, legacy
  utilities, and stale setup advice with bounded compatibility notes when old
  behavior must temporarily remain.

## Reference Highlights

- `.agents/skills/ub-tailwind/references/tailwind-guardrails.md`: current
  setup guardrails, CSS-first directives, deprecated syntax traps,
  environment validation, Nuxt/Vite differences, component-style rules, and
  compatibility exception format.
- `.agents/skills/ub-tailwind/references/framework-recipes.md`: standalone
  HTML, Vue plus Vite, Nuxt setup paths, component-scoped style notes, and
  quick environment detection.
- `.agents/skills/ub-tailwind/references/tailwind-legacy-to-modern-migration.md`:
  migration matrix, directive replacements, representative utility changes,
  removed defaults, and compatibility caveats.

## Progressive Disclosure

The main skill decides whether Tailwind owns the task. Load framework recipes
only after the target environment is known. Load migration guidance only when
legacy Tailwind syntax or upgrade work is present.

## Common Invocation Examples

- “Use `ub-tailwind` to set up Tailwind for this Nuxt app.”
- “Review this migration away from legacy directives.”
- “Bridge these design tokens into Tailwind utilities.”
- “Choose the right Tailwind setup path for Vue plus Vite.”

## Boundaries

Do not use it when the task is plain CSS architecture without Tailwind as the
primary surface. Use `ub-css` for that.

## Tradeoffs

Strength: keeps Tailwind setup current, framework-native, and aligned with CSS
architecture.

Cost: environment detection is required; guessing the setup path creates
drift.
