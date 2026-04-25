# UB Nuxt

Source: `.agents/skills/ub-nuxt/SKILL.md`

`ub-nuxt` guides Nuxt runtime, app structure, rendering, data fetching, Nitro,
server routes, modules, ecosystem choices, and migration decisions.

## Core Principles

- Detect Nuxt generation, app structure, modules, and runtime targets before
  changing code.
- Use Nuxt-native primitives for data fetching, server routes, plugins,
  middleware, runtime config, and rendering decisions.
- Keep server, client, and shared data ownership clear.
- Coordinate Vue and TypeScript choices without letting them override Nuxt
  runtime truth.
- Prefer modern directory and runtime conventions for new work.
- Treat ecosystem preferences as strong defaults, not universal requirements.
- Use migration references when legacy Nuxt structure or old data patterns are
  present.

## Behavior In Practice

- Inspects `package.json`, lockfiles, `nuxt.config.*`, configured `srcDir`,
  modules, compatibility flags, and app directory layout before changing code.
- Chooses rendering and runtime strategy first: SSR, SSG, hybrid, edge, or
  server mode shape the data, server, and deployment choices.
- Enforces modern Nuxt structure for new guidance: app source under `app/`,
  runtime roots such as `server/`, `shared/`, `public/`, and `modules/` at the
  project root, with configured `srcDir` respected.
- Prefers Nuxt-native primitives: `useAsyncData`, `useFetch`, Nitro server
  routes, plugins, middleware, runtime config, route rules, and auto-imported
  composables when they match the work.
- Keeps server-only secrets and privileged logic out of client code, and keeps
  payloads typed, minimal, and deterministic to avoid hydration problems.
- Uses TypeScript and Vue guidance without letting component concerns override
  Nuxt runtime truth.
- Applies VueUse-first and maintained-module heuristics before adding utility
  dependencies or bespoke runtime helpers.
- Rejects legacy root app directories, old data-fetching idioms, ad-hoc
  global stores, and plugin side effects unless a bounded migration constraint
  requires temporary retention.

## Reference Highlights

- `.agents/skills/ub-nuxt/references/nuxt-vue-patterns.md`: architecture,
  async data semantics, server/client rules, routing, state ownership,
  hydration checks, testing focus, and anti-patterns.
- `.agents/skills/ub-nuxt/references/typescript-modern.md`: TypeScript
  baseline, boundary typing priorities, Vue-specific typing, strict compiler
  expectations, and quality gates.
- `.agents/skills/ub-nuxt/references/ecosystem-preferences.md`: VueUse-first
  heuristics, package selection, dependency replacement matrix, and package
  justification rules.
- `.agents/skills/ub-nuxt/references/nuxt-legacy-to-modern-migration.md`:
  root-directory migration deltas, codemod path, compatibility caveats,
  module/layer caveats, and modern app-structure expectations.

## Progressive Disclosure

The main skill handles Nuxt routing and runtime ownership. Load Nuxt/Vue
patterns for architecture and data work, TypeScript guidance for boundary
typing, ecosystem preferences for package choices, and migration guidance only
when legacy patterns are actually in scope.

## Common Invocation Examples

- “Use `ub-nuxt` to design this server route.”
- “Review this Nuxt app structure for legacy patterns.”
- “Choose the rendering mode for this page.”
- “Decide whether this belongs in a server route, plugin, or composable.”

## Boundaries

Do not use it for framework-agnostic Vue component logic unless Nuxt runtime
behavior is also involved. Do not use it as the primary styling owner when the
problem is plain CSS or Tailwind integration.

## Tradeoffs

Strength: prevents legacy Nuxt structure and runtime ambiguity.

Cost: can be too broad for a small Vue-only component change.
