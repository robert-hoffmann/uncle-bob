# UB Vue

Source: `.agents/skills/ub-vuejs/SKILL.md`

`ub-vuejs` guides Vue component and composable authoring with modern Vue,
Composition API, reactivity, watcher, SSR, hydration, and TypeScript patterns.

## Core Principles

- Detect Vue version family and tooling before prescribing patterns.
- Prefer `script setup`, Composition API, and explicit component contracts for
  new work.
- Keep props, emits, models, and composables typed at their boundaries.
- Use precise reactivity and watcher sources instead of broad or stale
  subscriptions.
- Treat SSR IDs, hydration behavior, and mismatch exceptions deliberately.
- Migrate away from Options API, class-style components, filters, and mixins
  unless compatibility requires them.

## Behavior In Practice

- Detects Vue version family, Vite or framework tooling, TypeScript state, and
  existing component style before prescribing a pattern.
- Generates new SFC code with `<script setup lang="ts">`, Composition API, and
  compiler macros instead of Options API or `this`-centric logic.
- Treats props, emits, `v-model`, template refs, and composables as contracts.
  It prefers typed boundaries and modern helpers over loosely shaped objects.
- Uses precise reactivity: getter watch sources for destructured props,
  `MaybeRefOrGetter` and `toValue()` for flexible composables, and synchronous
  watcher cleanup before any async boundary.
- Handles SSR and hydration deliberately with stable IDs, lazy hydration where
  appropriate, narrow mismatch allowances, and documented exceptions.
- Considers VueUse before hand-rolling generic browser API, timer, storage,
  sensor, event, or async-state composables.
- Replaces legacy patterns incrementally when touching existing code, with a
  named compatibility reason and follow-up path when legacy must remain.

## Reference Highlights

- `.agents/skills/ub-vuejs/references/vue-modern-patterns.md`: script setup,
  reactive props, component models, template refs, watcher cleanup,
  composable input normalization, SSR-safe IDs, hydration controls, and
  performance guardrails.
- `.agents/skills/ub-vuejs/references/vue-legacy-to-modern-migration.md`:
  Options API, class components, filters, mixins, manual model boilerplate,
  template-ref patterns, compatibility exceptions, and incremental migration
  sequence.

## Progressive Disclosure

The main skill is enough for component routing and high-level Vue guidance.
Load the modern-patterns reference for concrete component and composable
recipes. Load the migration reference only when touching legacy Vue patterns or
planning an upgrade path.

## Common Invocation Examples

- “Use `ub-vuejs` to design this component contract.”
- “Review this watcher for correctness and cleanup.”
- “Refactor this composable with strict TypeScript boundaries.”
- “Explain whether this should be Vue logic or Nuxt runtime logic.”

## Boundaries

Do not use it as the owner for Nuxt routing, Nitro, runtime config, or app
structure. Use `ub-nuxt` for those. Use `ub-css` or `ub-tailwind` when styling
is the primary problem.

## Tradeoffs

Strength: improves component contracts, reactivity safety, and SSR/hydration
discipline.

Cost: it can be unnecessary for purely presentational Markdown or CSS-only
changes.
