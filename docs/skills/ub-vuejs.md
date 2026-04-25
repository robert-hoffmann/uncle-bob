# UB Vue

Source: `.agents/skills/ub-vuejs/SKILL.md`

`ub-vuejs` guides Vue component and composable authoring with modern Vue and
strict TypeScript patterns.

## When To Use It

Use it for Vue SFCs, Composition API, reactivity, watchers, props, emits,
template refs, SSR or hydration primitives, and Vue composables.

## What It Changes

- defaults new SFC work to `script setup` with TypeScript
- keeps props, emits, and model contracts explicit
- applies modern reactivity and watcher patterns
- separates Vue component logic from Nuxt runtime concerns

## Common Prompts

- “Use `ub-vuejs` to design this component contract.”
- “Review this watcher for correctness and cleanup.”
- “Refactor this composable with strict TypeScript boundaries.”

## Boundaries

Do not use it as the owner for Nuxt routing, Nitro, runtime config, or app
structure. Use `ub-nuxt` for those.

## Tradeoffs

Strength: improves component contracts and reactivity safety.

Cost: may be unnecessary for purely presentational Markdown or CSS changes.
