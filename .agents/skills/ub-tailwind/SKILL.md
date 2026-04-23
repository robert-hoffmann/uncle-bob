---
name: ub-tailwind
description: Use this skill for Tailwind setup, migration, integration, and utility-first styling. Apply it when the task mentions Tailwind directives or utilities, @import "tailwindcss", @theme, plugin wiring, legacy-to-modern migration, token bridging with CSS variables, or framework-specific Tailwind build issues.
---

# UB Tailwind

## Overview

Use this skill to keep Tailwind usage current and correct across different environments and avoid outdated patterns. This skill targets the latest stable Tailwind CSS: enforce CSS-first setup, apply official framework recipes, and replace legacy defaults in generated guidance.

Implement against the detected project and tooling truth, but bias setup and
migration guidance toward modern CSS-first Tailwind rather than retaining
legacy configuration habits or compatibility layers by default.

## Load References On Demand

- Read `../ub-authoring/references/authoring-conventions.md` when adjusting routing
  guidance or cross-skill authoring conventions.
- Read `references/tailwind-guardrails.md` for strict do/don't rules, deprecated syntax traps, and review checklists.
- Read `references/framework-recipes.md` for environment-specific setup paths (standalone HTML/CDN, Vue + Vite, Nuxt).
- Read `references/tailwind-legacy-to-modern-migration.md` for migration matrix, upgrade replacements, and compatibility caveats.

## When Not To Use

- Do not use this skill when the task is plain CSS architecture, selector
  strategy, or token-driven styling without Tailwind as the primary surface;
  co-load or defer to `ub-css` when Tailwind and CSS architecture overlap.
- Do not use this skill when the main issue is framework runtime behavior
  rather than Tailwind integration or utility-class authoring.

## Core Workflow

1. Identify the target environment before writing any Tailwind setup.
2. Run required detection checks: `nuxt.config.*`, `vite.config.*`, `package.json` dependencies, CSS entrypoints, and Nuxt app stylesheet placement (for modern Nuxt, expect `app/assets/css/main.css`).
3. Choose the matching recipe from `references/framework-recipes.md`.
4. Compare official guidance, repo truth, and observed code reality for
   non-trivial or version-sensitive recommendations.
5. Surface `OFFICIAL_CONFLICT` when authoritative sources, repo truth, or live
   code reality materially disagree on a non-trivial recommendation.
6. Surface `UNVERIFIED` when a non-trivial claim could not be confirmed in
   official sources after targeted research.
7. Apply modern Tailwind CSS-first rules from `references/tailwind-guardrails.md`.
8. Apply upgrade-safe replacements from `references/tailwind-legacy-to-modern-migration.md`.
9. Run the environment-specific validation checklist.
10. Reject and replace deprecated or legacy syntax.

## Environment Selection

- Use the **Standalone HTML/CDN** recipe for plain HTML pages without a build tool.
- Use the **Vue + Vite** recipe for Vue projects with Vite bundling.
- Use the **Nuxt** recipe for Nuxt apps where integration details differ from plain Vite.
- For Nuxt, default to the official setup path (`@tailwindcss/vite` wired in `nuxt.config.*`), not legacy module defaults.

If the environment is unclear, inspect project markers first (`package.json`, framework config, build plugins) and do not guess.

## Non-Negotiable Guardrails

### Tailwind Version and Syntax

- Use modern Tailwind CSS-first patterns and current docs semantics.
- Prefer CSS entrypoint `@import "tailwindcss"`.
- Prefer CSS directives like `@theme`, `@utility`, `@variant`, `@custom-variant`, `@source`, and `@reference` as needed.
- Treat `@config` and `@plugin` as legacy paths unless explicitly required for compatibility.
- Prefer compatibility only as a bounded layer with a documented migration back to CSS-first defaults.

### Build Strategy

- Do not assume PostCSS is required for modern Tailwind.
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
- Do not assume PostCSS setup is mandatory for modern Tailwind.
- Do not default to `@nuxtjs/tailwindcss` as the first-line setup for fresh Nuxt guidance.

## Output Requirements

When generating or modifying code, always provide:

1. A short environment detection note.
2. A source truth note: detected project version, environment markers, and any
   material gap versus latest stable guidance.
3. The selected setup path (CDN, Vue + Vite, or Nuxt).
4. Exact deprecated-to-modern replacements applied (syntax/tooling/utility changes).
5. A quick validation checklist confirming modern Tailwind setup.
6. Compatibility notes when legacy directives (`@config`/`@plugin`) are retained.
7. Conflict note when relevant: `OFFICIAL_CONFLICT` or `UNVERIFIED` with a
   concise explanation and the implementation consequence.

## Version & Research Policy

- Target the latest stable release of Tailwind CSS.
- Detect the project's actual Tailwind version from `package.json` and lockfiles.
- Use web search to verify current best practices, directive availability, and migration guidance against official Tailwind CSS documentation.
- Treat repo truth as the gold implementation standard when deciding what can
  actually ship safely in the current project.
- Treat official Tailwind docs as the preferred guidance baseline for
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
- Inspect the host repository's `AGENTS.md` or equivalent instructions when
  present for project-specific version policy and tooling; do not assume it
  contains this catalog's defaults.
- Do not hardcode version numbers in generated guidance — keep recommendations evergreen.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: official migration changes, deprecated directives, major Tailwind releases, or repo toolchain changes that affect setup recipes.
- Enforcement: advisory only; stale Tailwind guidance is a review signal, not a blocking gate by itself.
- Stable core: environment detection, official recipe selection, and deprecated-syntax avoidance should remain useful even when exact setup details evolve.

## Completion Checklist

- Environment explicitly identified before setup.
- Tailwind entrypoint and directives align with modern guidance.
- No deprecated/legacy syntax remains without explicit compatibility reason.
- Framework-specific differences are handled (CDN vs Vite vs Nuxt).
- Nuxt guidance uses the official framework path and does not drift into Vue-only `vite.config.*` steps.
- Token usage is centralized and consistent.
- Generated instructions are concise, deterministic, and current-version oriented.
- Any material official-source conflict or unverified non-trivial guidance is
  disclosed explicitly when relevant.
