# TypeScript 5.9.3 Legacy Replacements

## Purpose

Map legacy TypeScript patterns to modern 5.9.3 alternatives and define bounded migration exception policy.

## Replacement Map

| Legacy pattern | Modern replacement | Why replace |
|---|---|---|
| Implicit type-only imports | `import type` and `export type` with `verbatimModuleSyntax` | Avoid runtime import confusion and preserve emit intent. |
| Loose module detection | `moduleDetection: force` in module-based repos | Prevent accidental script-mode behavior and phantom globals. |
| Broad assertion chains (`as any as ...`) | Narrowing with guards, discriminated unions, and `unknown` boundaries | Improve soundness and reviewability. |
| Inference hacks for generic APIs | Built-in `NoInfer` and clearer generic parameter design | Reduce surprising inference outcomes. |
| Widened config object literals | `satisfies` plus optional `as const` where needed | Preserve literals while validating shape. |
| Namespace-heavy architecture | ES modules with explicit exports | Align with modern tooling and runtime semantics. |
| Legacy decorator mode for new code | Standard decorators where supported and explicitly configured | Keep semantics aligned with modern ECMAScript direction. |

## Explicit Bans For New Code

- Do not create new `namespace`-centric architecture.
- Do not use implicit type-only imports.
- Do not introduce assertion-heavy shortcuts where narrowing is feasible.
- Do not rely on legacy decorator patterns for newly authored modules.
- Do not add ambiguous ESM and CJS interop hacks without runtime-driven justification.

## Migration Exception Format

Allow temporary retention only when all fields are captured:

1. `retained_pattern`: exact legacy construct being kept.
2. `scope`: file or module boundary where it remains.
3. `constraint`: concrete compatibility reason.
4. `fallback_evaluated`: modern option considered and why deferred.
5. `retirement_trigger`: condition that allows removal.
6. `follow_up_change`: concrete modernization task.

## Example Exception Record

```md
retained_pattern: experimental decorator usage in auth module
scope: src/auth/decorators.ts
constraint: framework plugin currently depends on legacy metadata flow
fallback_evaluated: standard decorators tested, plugin rejects metadata shape
retirement_trigger: plugin vNext with standards-compliant decorator metadata
follow_up_change: migrate decorators and remove legacy compiler flags
```

## Review Checklist

1. Confirm legacy usage is pre-existing, not newly introduced.
2. Confirm modern replacement was evaluated.
3. Confirm exception scope is narrowly bounded.
4. Confirm follow-up task is concrete and testable.
5. Confirm no additional legacy surface area was added.

## Practical Migration Strategy

1. Harden module and import hygiene first.
2. Replace assertion-heavy typing with boundary validation and unions.
3. Migrate shared utilities to modern generic and literal-preserving patterns.
4. Remove retained exceptions as soon as constraints clear.
