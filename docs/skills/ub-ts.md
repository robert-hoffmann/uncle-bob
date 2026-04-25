# UB TypeScript

Source: `.agents/skills/ub-ts/SKILL.md`

`ub-ts` guides TypeScript typing, compiler configuration, module strategy,
boundary design, emitted types, and legacy-to-modern migration.

## Core Principles

- Detect the project archetype before choosing TypeScript settings.
- Keep module configuration faithful to runtime behavior.
- Prefer strict compiler posture and explicit trust-boundary narrowing.
- Use type-only imports and exports where they clarify emitted code.
- Preserve literal intent with modern type patterns when they improve safety.
- Avoid assertion-heavy shortcuts when narrowing or validation is practical.
- Modernize legacy configs incrementally and document compatibility exceptions.

## Behavior In Practice

- Detects the project archetype before touching config: Node runtime, bundler
  app, library publishing flow, Vue/Nuxt project, or type-stripping runtime.
- Makes module settings match runtime behavior instead of personal preference.
  Node-like, bundler-like, and library outputs have different resolution and
  declaration pressures.
- Treats strictness as a safety baseline: strict type checking, checked index
  access, exact optional properties, isolated modules where tooling mixes, and
  declaration checks where published types matter.
- Uses modern type patterns to preserve intent: `satisfies`, discriminated
  unions, type-only imports and exports, constrained inference, literal
  preservation, and explicit boundary types.
- Uses `unknown` at trust boundaries, then narrows with validation or
  discriminants before application code consumes the data.
- Replaces legacy shortcuts when touching code: namespace-centric structure,
  ambiguous CJS/ESM modules, implicit type-only import elision, assertion
  chains, and new experimental-decorator patterns.
- Scaffolds starter configs only when the repository lacks active TypeScript
  config and explicitly wants the Uncle Bob house baseline.

## Reference Highlights

- `.agents/skills/ub-ts/references/ts-modern-patterns.md`: archetype matrix,
  strict baseline, config starting points, module strategies, boundary typing,
  and modern type patterns.
- `.agents/skills/ub-ts/references/ts-config-resolution.md`: how to inspect
  local TypeScript config, package metadata, lockfiles, runtime markers,
  optional ESLint support, and starter scaffold choices.
- `.agents/skills/ub-ts/references/ts-legacy-to-modern-migration.md`: banned
  patterns, replacement map, module migration concerns, and compatibility
  exception format.
- `.agents/skills/ub-ts/references/task-bundle.md`: optional task automation
  bundle for repositories that want repeatable typecheck, lint, build, and
  test entrypoints.
- `.agents/skills/ub-ts/assets/tsconfig-template/`: starter configs for common
  archetypes when a repository explicitly wants them and does not already have
  active local config.

## Progressive Disclosure

The main skill handles TypeScript routing and high-level workflow. References
load when the task depends on config resolution, modern typing patterns,
legacy migration, or optional automation. This prevents a simple type review
from becoming a full compiler-baseline migration.

## Common Invocation Examples

- “Use `ub-ts` to choose the right module settings.”
- “Review this TypeScript API boundary.”
- “Modernize this config without breaking runtime behavior.”
- “Replace this unsafe assertion with real narrowing.”

## Boundaries

Do not use it for Vue or Nuxt runtime decisions by itself. Pair it with
`ub-vuejs` or `ub-nuxt` when framework behavior is central.

## Tradeoffs

Strength: reduces type and module ambiguity by tying compiler choices to the
project's actual runtime model.

Cost: strict baselines may require staged migration in older projects.
