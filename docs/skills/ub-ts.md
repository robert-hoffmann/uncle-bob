# UB TypeScript

Source: `.agents/skills/ub-ts/SKILL.md`

`ub-ts` guides TypeScript typing, compiler configuration, module strategy,
boundary design, and modernization.

## When To Use It

Use it for `tsconfig`, module resolution, emitted types, strict compiler flags,
TypeScript API boundaries, Node TypeScript, bundler projects, Vue, or Nuxt.

## What It Changes

- detects runtime and project archetype before choosing config
- keeps module settings faithful to runtime behavior
- prefers strict typing and explicit trust boundaries
- avoids legacy TypeScript patterns in new code
- surfaces version or official-guidance conflicts when they matter

## Common Prompts

- “Use `ub-ts` to choose the right module settings.”
- “Review this TypeScript API boundary.”
- “Modernize this config without breaking runtime behavior.”

## Boundaries

Do not use it for Vue or Nuxt runtime decisions by itself. Pair it with
`ub-vuejs` or `ub-nuxt` when framework behavior is central.

## Tradeoffs

Strength: reduces type and module ambiguity.

Cost: strict baselines may require staged migration in older projects.
