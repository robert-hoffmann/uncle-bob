---
name: dev-nuxt
description: Build, review, migrate, and debug Nuxt 4 applications with typed composables, SSR/SSG/hybrid rendering, runtime config, Nitro/server routes, and app-directory semantics. Use when tasks mention nuxt.config.*, Nuxt modules, middleware/plugins, server APIs, deployment/runtime mode, or Nuxt 3 to 4 migration, especially when framework/runtime behavior is the primary concern.
---

# Dev Nuxt

## Overview

Use this skill to keep Nuxt work current-version aligned, type-safe, and framework-native. This skill is hard Nuxt 4-only: enforce the `app/`-first source layout, Nuxt 4 runtime defaults, and current Vue + TypeScript patterns while rejecting v3-era directory guidance.

## Load References On Demand

- Read `references/nuxt4-vue-patterns.md` for architecture, data-fetching, routing, server, and rendering guidance.
- Read `references/typescript-modern.md` for strict TypeScript defaults, typing patterns, and anti-pattern checks.
- Read `references/ecosystem-preferences.md` for modern package preferences, VueUse-first heuristics, and replacement matrix.
- Read `references/nuxt3-to-nuxt4-deltas.md` for migration deltas, codemod mapping, and compatibility caveats.

## Core Workflow

1. Detect Nuxt generation and active toolchain from `package.json`, `nuxt.config.*`, lockfiles, and modules. Always inspect `srcDir`, `future.compatibilityVersion`, and `app/` directory presence.
2. Decide rendering/runtime mode first (SSR, SSG, hybrid, edge/server) before writing code.
3. Implement features with Composition API, `<script setup lang="ts">`, typed composables, and server/client separation.
4. Prefer VueUse and modern ecosystem defaults from `references/ecosystem-preferences.md`.
5. Apply Nuxt 4 runtime semantics from `references/nuxt4-vue-patterns.md` and migration deltas from `references/nuxt3-to-nuxt4-deltas.md`.
6. Reject legacy Nuxt/Vue patterns and replace them with current equivalents.
7. Validate types, lint/build output, and framework-specific constraints after edits.

## Nuxt 4 Structure Contract (Hard Requirement)

- Place all app source in `app/`:
  - `app/pages`, `app/components`, `app/layouts`, `app/middleware`, `app/plugins`
  - `app/app.vue`, `app/app.config.ts`
- Keep runtime and project roots at repository root:
  - `server/`, `shared/`, `public/`, `modules/`, `nuxt.config.ts`
- Respect `srcDir` if explicitly configured, but still apply Nuxt 4 structure semantics within that source root.
- Treat `future.compatibilityVersion` as a required detection signal:
  - if present and below `4`, call out mismatch and provide Nuxt 4 correction guidance.
- Do not scaffold or recommend v3-era root app directories:
  - `pages/`, `components/`, `layouts/`, `middleware/`, `plugins/` at repository root.

## Implementation Rules

### Nuxt and Vue

- Use Nuxt-native primitives (`useAsyncData`, `useFetch`, Nitro server routes, plugins, runtime config) instead of custom framework bypasses.
- Use Composition API and composables for reuse; avoid Options API for new work unless explicitly required.
- Keep data ownership clear across server routes, server composables, and client composables.
- Prefer auto-imported Nuxt utilities and composables where they improve consistency.
- Enforce Nuxt 4 directory and runtime defaults when generating or reviewing code; do not emit Nuxt 3 directory placements.

### TypeScript

- Enable strict TypeScript behavior and avoid `any` in application code.
- Type runtime config, API responses, composable contracts, and emits/props explicitly.
- Prefer inferred types where stable; add explicit exported/public types at boundaries.
- Use modern TypeScript features that improve correctness (satisfies, const assertions, template literal types, discriminated unions).

### Ecosystem and Package Selection

- Prefer VueUse before introducing utility packages for reactivity, browser APIs, sensors, lifecycle wrappers, and async helpers.
- Choose Nuxt ecosystem modules and actively maintained libraries with strong TypeScript support.
- Keep dependencies minimal; remove redundant packages when Nuxt/VueUse/standard platform APIs already solve the need.
- Defer deep Tailwind guidance to `.agents/skills/dev-tailwind/SKILL.md`; keep only integration-level Tailwind notes in Nuxt tasks.

## Legacy-Avoidance Guardrails

- Do not scaffold or recommend legacy Nuxt directory conventions that conflict with Nuxt 4 defaults.
- Do not introduce Vue 2-era patterns (`mixins`, filters, class-style component decorators) for new implementation.
- Do not default to ad-hoc global stores or plugin side effects when composables or typed stores are clearer.
- Do not use old router/data-fetching idioms when Nuxt-native patterns are available.
- Do not generate app source files in root-level `pages/`, `components/`, `layouts/`, `middleware/`, or `plugins/`.

## Output Requirements

When generating or reviewing code, always include:

1. A short environment detection note (Nuxt generation, Vue version family, TS strictness state).
2. A Nuxt 4 structure compliance note (`app/` placement, root runtime dirs, `srcDir` handling, `future.compatibilityVersion` status).
3. The selected rendering/runtime strategy and why it fits.
4. The package selection rationale when adding dependencies (especially VueUse vs alternatives).
5. A concise list of legacy patterns removed or avoided.
6. Validation actions performed (typecheck/build/test/lint as available).

## Completion Checklist

- Nuxt mode and toolchain are identified before edits.
- Nuxt 4 structure contract is satisfied (`app/` app source; root runtime dirs).
- Composition-first and Nuxt-native patterns are used throughout.
- TypeScript boundary types are explicit and `any` is avoided.
- VueUse-first preference is applied for utility/reactive helpers.
- Added dependencies are modern, maintained, and justified.
- Tailwind details are delegated to `dev-tailwind` when needed.
- Legacy patterns are replaced, not carried forward.
