---
name: dev-vuejs
description: Build, review, migrate, and debug Vue 3.5.x application code with strict TypeScript, focusing on SFCs, composables, reactivity, watchers, SSR/hydration primitives, and component contracts. Use when tasks are Vue core/component architecture in Vite or framework-agnostic Vue apps, especially when Nuxt runtime or app-directory policy is not the main concern.
---

# Dev VueJS

## Overview

Use this skill to enforce Vue 3.5.x core best practices with strict TypeScript and migration-aware legacy handling. Generate only modern patterns for new code and refactor existing legacy patterns incrementally.

## Load References On Demand

- Read `references/vue-3-5-modern-patterns.md` for the canonical Vue 3.5+ recipes and API usage patterns.
- Read `references/vue-3-legacy-replacements.md` for migration mapping, compatibility exceptions, and modernization sequence.

## Core Workflow

1. Detect Vue version family and tooling from `package.json`, lockfiles, `vite.config.*`, `vue.config.*`, and TypeScript config.
2. Confirm the task is Vue core scope (SFCs, reactivity, watchers, SSR and hydration, component contracts). If the task is Nuxt-specific, defer framework rules to `.agents/skills/dev-nuxt/SKILL.md`.
3. Implement with strict TypeScript and SFC default `script setup` plus `lang="ts"`.
4. Apply Vue 3.5 patterns from `references/vue-3-5-modern-patterns.md`.
5. Reject legacy output and apply migration mapping from `references/vue-3-legacy-replacements.md` when updating existing code.
6. Validate behavior with typecheck, lint, and tests available in the target project.

## Version Contract

- Treat Vue `3.5.x` stable as the default baseline.
- Treat Vue `3.6` beta features as non-default and do not generate them unless the user explicitly requests beta usage.
- Keep guidance compatible with Vue 3.5 patch-level updates, including current bugfix behavior.

## Implementation Rules

### Core Vue and SFC

- Require TypeScript in generated code.
- Default to `script setup` plus `lang="ts"` for SFC authoring.
- Use Composition API and compiler macros for new code.
- Prefer `defineModel()` for component `v-model` contracts in new code.
- Prefer `useTemplateRef()` for string-based template refs.

### Reactivity and Watchers

- Use reactive props destructure in script setup where it improves clarity.
- Watch destructured props with getter sources, never pass the value directly as a watch source.
- Use `MaybeRefOrGetter<T>` and `toValue()` for composables that accept value, ref, or getter inputs.
- Consider `VueUse` (`vueuse.org`, especially `@vueuse/core`) before writing
	bespoke generic composables for browser APIs, events, timers, storage,
	sensors, or async state helpers.
- Register `onWatcherCleanup()` synchronously before any `await` boundary in watcher callbacks.
- Prefer precise getters for watch sources; use numeric `deep` only when necessary.

### SSR and Hydration

- Use `useId()` for SSR-safe ID generation.
- Use lazy hydration strategies for async components when rendering heavy below-the-fold islands.
- Use `data-allow-mismatch` narrowly and document justification for each mismatch type.
- Use `Teleport defer` when the target is created later in the same render tick.

### Performance and Build Hygiene

- Prioritize high-leverage optimizations: stable props, code splitting, large-list virtualization, and controlled deep reactivity.
- Keep compile-time flags intentional and explicit in build configuration.
- Avoid premature micro-optimizations that are not backed by measurements.

## Legacy-Avoidance Guardrails

- Do not generate Options API for new code.
- Do not generate class-style components, mixins, filters, or `this`-centric component logic for new code.
- Do not generate manual `modelValue` and `update:modelValue` boilerplate when `defineModel()` is viable.
- Do not generate `ref(null)` template-ref patterns when `useTemplateRef()` is available and suitable.
- Do not generate watcher code that registers cleanup after an async boundary.

Migration-aware exception policy:
- Allow temporary legacy retention only when required for bounded compatibility in existing codebases.
- Document each retained legacy pattern, why it is retained, and the exact follow-up modernization path.

Non-goals:
- Do not encode Nuxt-specific directory/runtime policy in this skill; defer to `dev-nuxt`.
- Do not provide deep Tailwind implementation guidance in this skill; defer to `dev-tailwind`.

## Output Requirements

When generating or reviewing code, always include:

1. Environment note: Vue version family, TypeScript state, and key tooling detected.
2. Version note: baseline 3.5.x used, and whether any beta-only behavior is intentionally excluded.
3. Pattern note: which modern APIs were selected and why.
4. Legacy note: what legacy patterns were removed or intentionally retained with compatibility rationale.
5. Validation note: what checks were run (typecheck, lint, tests, build) and outcomes.

## Completion Checklist

- Vue 3.5.x baseline and TypeScript requirement are enforced.
- New code uses Composition API and script setup with lang ts.
- `defineModel`, `useTemplateRef`, and modern watcher patterns are used where relevant.
- SSR and hydration primitives are used correctly when SSR is in scope.
- No new legacy output is introduced.
- Any retained legacy is explicitly justified with an incremental migration path.
- Nuxt and Tailwind concerns are delegated to their dedicated skills when applicable.
