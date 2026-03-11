---
name: dev-tailwind
description: Set up, migrate, debug, and review Tailwind CSS v4 integrations across standalone HTML, Vue + Vite, and Nuxt projects. Use when tasks mention Tailwind directives/utilities, @import "tailwindcss", @theme tokens, v3-to-v4 migration, plugin wiring, or framework-specific Tailwind build issues, especially when utility-class workflow is the primary change surface.
---

# Dev Tailwind

## Overview

Use this skill to keep Tailwind usage v4-correct across different environments and avoid outdated patterns. This skill is hard Tailwind v4-first: enforce CSS-first setup, apply official framework recipes, and replace legacy/v3-era defaults in generated guidance.

## Load References On Demand

- Read `references/tailwind-v4-guardrails.md` for strict do/don't rules, deprecated syntax traps, and review checklists.
- Read `references/framework-recipes.md` for environment-specific setup paths (standalone HTML/CDN, Vue + Vite, Nuxt).
- Read `references/tailwind-v3-to-v4-deltas.md` for migration matrix, upgrade replacements, and compatibility caveats.

## Core Workflow

1. Identify the target environment before writing any Tailwind setup.
2. Run required detection checks: `nuxt.config.*`, `vite.config.*`, `package.json` dependencies, CSS entrypoints, and Nuxt app stylesheet placement (for Nuxt v4-style docs, expect `app/assets/css/main.css`).
3. Choose the matching recipe from `references/framework-recipes.md`.
4. Apply Tailwind v4 CSS-first rules from `references/tailwind-v4-guardrails.md`.
5. Apply upgrade-safe replacements from `references/tailwind-v3-to-v4-deltas.md`.
6. Run the environment-specific validation checklist.
7. Reject and replace deprecated or legacy syntax.

## Environment Selection

- Use the **Standalone HTML/CDN** recipe for plain HTML pages without a build tool.
- Use the **Vue + Vite** recipe for Vue projects with Vite bundling.
- Use the **Nuxt** recipe for Nuxt apps where integration details differ from plain Vite.
- For Nuxt, default to the official setup path (`@tailwindcss/vite` wired in `nuxt.config.*`), not legacy module defaults.

If the environment is unclear, inspect project markers first (`package.json`, framework config, build plugins) and do not guess.

## Non-Negotiable Guardrails

### Tailwind Version and Syntax

- Use Tailwind v4-first patterns and current docs semantics.
- Prefer CSS entrypoint `@import "tailwindcss"`.
- Prefer CSS directives like `@theme`, `@utility`, `@variant`, `@custom-variant`, `@source`, and `@reference` as needed.
- Treat `@config` and `@plugin` as legacy paths unless explicitly required for compatibility.
- Prefer compatibility only as a bounded layer with a documented migration back to CSS-first defaults.

### Build Strategy

- Do not assume PostCSS is required for Tailwind v4.
- Use Vite plugin integration where applicable (`@tailwindcss/vite`) for Vue + Vite workflows.
- For Nuxt, use the official Nuxt framework-guide flow and configure the Vite plugin under Nuxt config instead of creating Vue-only `vite.config.*` instructions.
- Keep setup minimal and environment-native.

### Vue/Nuxt Style Context

- For Vue/Nuxt component-scoped styles using `@apply` or `@variant`, include `@reference` to the main stylesheet or app stylesheet context.
- Avoid duplicating imported CSS just to expose theme values in component-local styles.

### Design Tokens

- Keep Tailwind tokens centralized in `@theme`.
- Reuse existing token primitives and avoid ad-hoc hardcoded drift.

### Do Not Generate

- Do not generate `@tailwind base;`, `@tailwind components;`, `@tailwind utilities;` as the default modern entrypoint.
- Do not assume PostCSS setup is mandatory for Tailwind v4.
- Do not default to `@nuxtjs/tailwindcss` as the first-line setup for fresh Nuxt guidance.

## Output Requirements

When generating or modifying code, always provide:

1. A short environment detection note.
2. The selected setup path (CDN, Vue + Vite, or Nuxt).
3. Exact deprecated-to-modern replacements applied (syntax/tooling/utility changes).
4. A quick validation checklist confirming v4-safe setup.
5. Compatibility notes when legacy directives (`@config`/`@plugin`) are retained.

## Completion Checklist

- Environment explicitly identified before setup.
- Tailwind entrypoint and directives align with v4 guidance.
- No deprecated/legacy syntax remains without explicit compatibility reason.
- Framework-specific differences are handled (CDN vs Vite vs Nuxt).
- Nuxt guidance uses the official framework path and does not drift into Vue-only `vite.config.*` steps.
- Token usage is centralized and consistent.
- Generated instructions are concise, deterministic, and current-version oriented.
