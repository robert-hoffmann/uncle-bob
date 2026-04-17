---
name: ub-ts
description: Design, review, migrate, and debug TypeScript (latest stable) codebases and tsconfig strategy for Node, bundlers, and libraries. Use when tasks center on typing, module/moduleResolution, compiler flags, type errors, project-wide TS modernization, or tsconfig architecture, especially when framework-specific behavior is secondary.
---

# UB TS

## Overview

Use this skill to enforce latest stable TypeScript modern defaults and patterns across app and library codebases. Generate modern-only output for new code, and allow legacy retention only as a bounded migration exception.

## Load References On Demand

- Read `references/ts-modern-patterns.md` for archetype selection, tsconfig baselines, and modern typing patterns.
- Read `references/ts-legacy-to-modern-migration.md` for old-to-new migrations, banned patterns, and exception handling.

## Core Workflow

1. Detect the project archetype from `package.json`, lockfiles, runtime targets, build tooling, and existing `tsconfig*.json` files.
2. Choose module strategy that matches runtime truth:
   - Node runtime: `module` as `node20` or `nodenext`
   - Bundler runtime: `moduleResolution` as `bundler` with `module` as `esnext`
   - Library publishing: prefer Node-faithful resolution for compatibility checks
   - Type-stripping runtime: enforce erasable TypeScript subset
3. Apply strict safety baseline and module hygiene defaults from `references/ts-modern-patterns.md`.
4. Implement modern type patterns first (`satisfies`, `const` type parameters, `NoInfer`, discriminated unions, explicit boundary typing).
5. Reject legacy output for new code and apply migration mapping from `references/ts-legacy-to-modern-migration.md` when touching existing code.
6. Validate with available typecheck, lint, tests, and build commands in the target project.

## Version & Research Policy

- Target the latest stable release of TypeScript.
- Detect the project's actual TypeScript version from `package.json` and lockfiles.
- Use web search to verify current best practices, API availability, and migration guidance against official TypeScript documentation.
- Do not emit beta-only syntax unless the user explicitly requests it.
- When the project's installed version is behind latest stable, note the version gap and recommend an upgrade path.
- Refer to AGENTS.md for centralized version policy and default tooling.
- Do not hardcode version numbers in generated guidance — keep recommendations evergreen.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: TypeScript release changes, compiler-flag behavior shifts, new module-resolution guidance, or runtime-platform updates that affect tsconfig strategy.
- Enforcement: advisory only; freshness should inform review priority, not become a blocking requirement by itself.
- Stable core: runtime-faithful module strategy, strict typing, and explicit boundary modeling remain the durable guidance even when compiler defaults evolve.

## Implementation Rules

### Project Archetype and Modules

- Decide archetype before changing compiler options.
- Keep module settings runtime-faithful, not preference-driven.
- Keep `moduleDetection` as `force` unless a known compatibility constraint requires otherwise.

### Import and Export Hygiene

- Keep `verbatimModuleSyntax` enabled.
- Use `import type` and `export type` for type-only symbols.
- Keep side-effect imports explicit and resolvable.

### Type System Patterns

- Prefer `satisfies` to validate shapes without widening literals.
- Prefer `const` type parameters in reusable APIs that benefit from literal preservation.
- Use built-in `NoInfer` when inference must be constrained.
- Model state with discriminated unions when behavior depends on variants.
- Use `unknown` at trust boundaries, then narrow with validation.

### Compiler Baseline

- Keep `strict: true`.
- Keep `noUncheckedIndexedAccess: true`.
- Keep `exactOptionalPropertyTypes: true`.
- Enable `isolatedModules` in toolchain-mixed repos.
- Enable `isolatedDeclarations` for declaration-heavy library workflows.
- Use `noUncheckedSideEffectImports` when side-effect imports are present.

### Tradeoff Handling

- Always propose at least two implementation paths for major TypeScript decisions.
- State concise pros and cons for each option (correctness, compatibility, DX, and migration cost).
- Default to the safest modern option unless user constraints indicate otherwise.

## Legacy-Avoidance Guardrails

- Do not generate legacy experimental decorator patterns for new code.
- Do not generate `namespace`-centric architecture for new code.
- Do not rely on implicit type-only import elision.
- Do not use assertion-heavy shortcuts (`as any`, chained assertions) where narrowing is possible.
- Do not introduce legacy module ambiguity between ESM and CJS.

Migration-aware exception policy:

- Allow temporary legacy retention only for explicit compatibility constraints in existing code.
- Document exactly what is retained, why it is retained, and the concrete follow-up modernization step.
- Scope each exception narrowly and avoid introducing new dependency on retained legacy behavior.

## Output Requirements

When generating or reviewing code, include:

1. Environment note: detected archetype, runtime target, and toolchain context.
2. Version note: TypeScript baseline and any intentional deviations.
3. Decision note: chosen module and compiler strategy with one alternative.
4. Tradeoff note: concise pros and cons for chosen path and rejected option.
5. Legacy note: removed legacy patterns or bounded exceptions with rationale.
6. Validation note: what checks were run and outcomes.

## Completion Checklist

- Latest stable TypeScript modern baseline is enforced.
- Project archetype was detected before config or code changes.
- Module strategy matches runtime behavior.
- Strict safety flags are enabled intentionally.
- New code avoids legacy patterns.
- Any retained legacy pattern is documented with a migration path.
- Typecheck and relevant project validations were executed when available.
