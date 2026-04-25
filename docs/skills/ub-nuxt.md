# UB Nuxt

Source: `.agents/skills/ub-nuxt/SKILL.md`

`ub-nuxt` guides Nuxt runtime, app structure, rendering, data fetching, Nitro,
server routes, modules, and deployment-mode decisions.

## When To Use It

Use it for `nuxt.config.*`, Nuxt modules, app-directory structure, middleware,
plugins, server routes, runtime config, SSR, SSG, hybrid rendering, or Nuxt
migration.

## What It Changes

- chooses rendering and runtime mode before implementation
- keeps Nuxt app structure modern and explicit
- separates server, client, and shared data ownership
- coordinates Nuxt, Vue, and TypeScript decisions

## Common Prompts

- “Use `ub-nuxt` to design this server route.”
- “Review this Nuxt app structure for legacy patterns.”
- “Choose the rendering mode for this page.”

## Boundaries

Do not use it for framework-agnostic Vue component logic unless Nuxt runtime
behavior is also involved.

## Tradeoffs

Strength: prevents legacy Nuxt structure and runtime ambiguity.

Cost: can be too broad for a small Vue-only component change.
