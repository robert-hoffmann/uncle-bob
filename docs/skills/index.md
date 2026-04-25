# Skill Catalog

Use these pages to understand what each Uncle Bob skill brings to an installed
agent. The source of truth remains each skill's `SKILL.md`; these docs explain
the principles, references, examples, boundaries, and tradeoffs behind the
portable skill system.

Each skill page now includes a `Behavior In Practice` section. That section is
where the page surfaces the practical ideas hidden in the skill references:
KISS/DRY/YAGNI for quality, modern Python typing and boundary validation,
TDD and evidence rules for governance, app-structure rules for Nuxt, and so
on.

## Core Operating Skills

- [UB Quality](./ub-quality): design principles, scope discipline,
  readability, formatting, documentation standards, and portability.
- [UB Workflow](./ub-workflow): direct work, lightweight specs, initiatives,
  sprints, reviewed mode, and stop-resume flow. See the
  [UB Workflow deep dive](/deep-dives/ub-workflow).
- [UB Governance](./ub-governance): lean governance, evidence escalation,
  ADRs, claims, TDD red/green/refactor, test-signal review, gate semantics,
  and bounded exceptions. See the [UB Governance deep dive](/deep-dives/ub-governance).
- [UB Authoring](./ub-authoring): reusable skill guidance, routing metadata,
  naming, non-use boundaries, and progressive disclosure.
- [UB Customizations](./ub-customizations): skills, hooks, MCP configs,
  bundles, artifact selection, and validation.

## Implementation Specialists

- [UB Python](./ub-python): modern Python, typing, boundary validation,
  dataclasses, Pydantic v2, structured errors, tests, tooling, and
  repository-truth validation.
- [UB TypeScript](./ub-ts): strict compiler posture, module-faithful config,
  trust-boundary narrowing, and legacy-to-modern migration.
- [UB Vue](./ub-vuejs): Vue SFCs, Composition API, reactivity, props, emits,
  composables, SSR, and hydration.
- [UB Nuxt](./ub-nuxt): Nuxt runtime, app structure, rendering, Nitro, server
  routes, ecosystem choices, and migration boundaries.
- [UB CSS](./ub-css): token-first CSS, cascade layers, modern selectors,
  container queries, accessibility, and progressive enhancement.
- [UB Tailwind](./ub-tailwind): Tailwind setup, CSS-first configuration,
  framework recipes, tokens, and migration guardrails.

## References And Progressive Disclosure

Most skills keep the top-level contract compact and move deeper detail into
skill-owned references. Public skill pages now highlight those references so
you can see where deeper guidance lives without reading every operational file
up front.

Start with [References And Progressive Disclosure](/guide/references-progressive-disclosure)
when you want to understand how the skill catalog stays both lean and deep.

## How To Choose

Start with the problem, not the technology.

1. If the problem is planning or resumable delivery, use `ub-workflow`.
2. If the problem is evidence, risk, testing posture, or gates, use
   `ub-governance`.
3. If the problem is reusable agent guidance, use `ub-authoring` or
   `ub-customizations`.
4. If the problem is implementation in a specific stack, add the matching
   specialist.
5. Use progressive disclosure inside the active skill when deeper references
   are relevant.
