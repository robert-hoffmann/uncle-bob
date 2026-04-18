---
name: ub-nuxt
description: Build, review, migrate, and debug Nuxt (latest stable) applications with typed composables, SSR/SSG/hybrid rendering, runtime config, Nitro/server routes, and app-directory semantics. Use when tasks mention nuxt.config.*, Nuxt modules, middleware/plugins, server APIs, deployment/runtime mode, or Nuxt migration, especially when framework/runtime behavior is the primary concern.
---

# UB Nuxt

## Overview

Use this skill to keep Nuxt work current-version aligned, type-safe, and framework-native. This skill targets the latest stable Nuxt: enforce the `app/`-first source layout, modern Nuxt runtime defaults, and current Vue + TypeScript patterns while rejecting legacy directory guidance.

Implement against the detected project and runtime truth, but bias framework
guidance toward forward-compatible migration rather than preserving legacy
layouts, outdated recipes, or compatibility-layer drift by default.

## Load References On Demand

- Read `../references/authoring-conventions.md` when adjusting routing
  guidance or cross-skill authoring conventions.
- Read `references/nuxt-vue-patterns.md` for architecture, data-fetching, routing, server, and rendering guidance.
- Read `references/typescript-modern.md` for strict TypeScript defaults, typing patterns, and anti-pattern checks.
- Read `references/ecosystem-preferences.md` for modern package preferences, VueUse-first heuristics, and replacement matrix.
- Read `references/nuxt-legacy-to-modern-migration.md` for migration deltas, codemod mapping, and compatibility caveats.

## When Not To Use

- Do not use this skill when the task is framework-agnostic Vue component or
  composable logic without Nuxt runtime, app-directory, or Nitro concerns;
  defer that to `ub-vuejs`.
- Do not use this skill when the primary change surface is pure CSS or
  Tailwind integration rather than Nuxt framework behavior.

## Core Workflow

1. Detect Nuxt generation and active toolchain from `package.json`, `nuxt.config.*`, lockfiles, and modules. Always inspect `srcDir`, `future.compatibilityVersion`, and `app/` directory presence.
2. Decide rendering/runtime mode first (SSR, SSG, hybrid, edge/server) before writing code.
3. Compare official guidance, repo truth, and observed code reality for
   non-trivial or version-sensitive recommendations.
4. Surface `OFFICIAL_CONFLICT` when authoritative sources, repo truth, or live
   code reality materially disagree on a non-trivial recommendation.
5. Surface `UNVERIFIED` when a non-trivial claim could not be confirmed in
   official sources after targeted research.
6. Implement features with Composition API, `<script setup lang="ts">`, typed composables, and server/client separation.
7. Prefer VueUse and modern ecosystem defaults from `references/ecosystem-preferences.md`.
8. Apply modern Nuxt runtime semantics from `references/nuxt-vue-patterns.md` and migration deltas from `references/nuxt-legacy-to-modern-migration.md`.
9. Reject legacy Nuxt/Vue patterns and replace them with current equivalents.
10. Validate types, lint/build output, and framework-specific constraints after edits.

## Nuxt Modern Structure Contract (Hard Requirement)

- Place all app source in `app/`:
  - `app/pages`, `app/components`, `app/layouts`, `app/middleware`, `app/plugins`
  - `app/app.vue`, `app/app.config.ts`
- Keep runtime and project roots at repository root:
  - `server/`, `shared/`, `public/`, `modules/`, `nuxt.config.ts`
- Respect `srcDir` if explicitly configured, but still apply modern Nuxt structure semantics within that source root.
- Treat `future.compatibilityVersion` as a required detection signal:
  - if present and below the current stable version, call out mismatch and provide correction guidance.
- Do not scaffold or recommend legacy root app directories:
  - `pages/`, `components/`, `layouts/`, `middleware/`, `plugins/` at repository root.

## Implementation Rules

### Nuxt and Vue

- Use Nuxt-native primitives (`useAsyncData`, `useFetch`, Nitro server routes, plugins, runtime config) instead of custom framework bypasses.
- Use Composition API and composables for reuse; avoid Options API for new work unless explicitly required.
- Keep data ownership clear across server routes, server composables, and client composables.
- Prefer auto-imported Nuxt utilities and composables where they improve consistency.
- Enforce modern Nuxt directory and runtime defaults when generating or reviewing code; do not emit legacy directory placements.

### TypeScript

- Enable strict TypeScript behavior and avoid `any` in application code.
- Type runtime config, API responses, composable contracts, and emits/props explicitly.
- Prefer inferred types where stable; add explicit exported/public types at boundaries.
- Use modern TypeScript features that improve correctness (satisfies, const assertions, template literal types, discriminated unions).

### Ecosystem and Package Selection

- Prefer VueUse before introducing utility packages for reactivity, browser APIs, sensors, lifecycle wrappers, and async helpers.
- Choose Nuxt ecosystem modules and actively maintained libraries with strong TypeScript support.
- Keep dependencies minimal; remove redundant packages when Nuxt/VueUse/standard platform APIs already solve the need.
- Defer deep Tailwind guidance to `.agents/skills/ub-tailwind/SKILL.md`; keep only integration-level Tailwind notes in Nuxt tasks.

## Legacy-Avoidance Guardrails

- Do not scaffold or recommend legacy Nuxt directory conventions that conflict with modern Nuxt defaults.
- Do not introduce Vue 2-era patterns (`mixins`, filters, class-style component decorators) for new implementation.
- Do not default to ad-hoc global stores or plugin side effects when composables or typed stores are clearer.
- Do not use old router/data-fetching idioms when Nuxt-native patterns are available.
- Do not generate app source files in root-level `pages/`, `components/`, `layouts/`, `middleware/`, or `plugins/`.

## Version & Research Policy

- Target the latest stable release of Nuxt.
- Detect the project's actual Nuxt version from `package.json`, `nuxt.config.*`, and lockfiles.
- Use web search to verify current best practices, API availability, and migration guidance against official Nuxt documentation.
- Treat repo truth as the gold implementation standard when deciding what can
  actually ship safely in the current project.
- Treat official Nuxt docs as the preferred guidance baseline for
  forward-looking design and migration-ready patterns.
- If official guidance and repo truth diverge materially on a non-trivial
  recommendation, surface `OFFICIAL_CONFLICT`, implement the repo-safe path,
  and explain the migration path.
- If official sources disagree with each other on a non-trivial
  recommendation, also surface `OFFICIAL_CONFLICT` instead of silently
  collapsing the disagreement.
- If a non-trivial claim cannot be confirmed in official sources after
  targeted research, mark it `UNVERIFIED` or avoid presenting it as settled
  guidance.
- Keep conflict and uncertainty disclosure scoped to non-trivial,
  version-sensitive, or contested guidance rather than trivial edits.
- When the project's installed version is behind latest stable, note the version gap and recommend an upgrade path.
- Refer to AGENTS.md for centralized version policy and default tooling.
- Do not hardcode version numbers in generated guidance — keep recommendations evergreen.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: Nuxt release-cycle changes, updated framework migration guides, runtime defaults shifts, or ecosystem-module guidance changes.
- Enforcement: advisory only; freshness markers should prioritize review, not block unrelated Nuxt work automatically.
- Stable core: Nuxt-native primitives, clear server/client boundaries, and app-source versus runtime-root separation remain the stable principles even when recipes evolve.

## Output Requirements

When generating or reviewing code, always include:

1. A short environment detection note (Nuxt generation, Vue version family, TS strictness state).
2. A source truth note: detected project version, runtime layout, and any
   material gap versus latest stable guidance.
3. A modern Nuxt structure compliance note (`app/` placement, root runtime dirs, `srcDir` handling, `future.compatibilityVersion` status).
4. The selected rendering/runtime strategy and why it fits.
5. The package selection rationale when adding dependencies (especially VueUse vs alternatives).
6. A concise list of legacy patterns removed or avoided.
7. Validation actions performed (typecheck/build/test/lint as available).
8. Conflict note when relevant: `OFFICIAL_CONFLICT` or `UNVERIFIED` with a
   concise explanation and the implementation consequence.

## Completion Checklist

- Nuxt mode and toolchain are identified before edits.
- Modern Nuxt structure contract is satisfied (`app/` app source; root runtime dirs).
- Composition-first and Nuxt-native patterns are used throughout.
- TypeScript boundary types are explicit and `any` is avoided.
- VueUse-first preference is applied for utility/reactive helpers.
- Added dependencies are modern, maintained, and justified.
- Tailwind details are delegated to `ub-tailwind` when needed.
- Legacy patterns are replaced, not carried forward.
- Any material official-source conflict or unverified non-trivial guidance is
  disclosed explicitly when relevant.
