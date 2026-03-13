# Modern TypeScript for Nuxt + Vue

## Goal

Keep Nuxt/Vue code strongly typed with modern TypeScript features and clear boundary contracts.

## Baseline

- Run with strict TypeScript settings.
- Keep module resolution/framework settings aligned with Nuxt defaults.
- Treat type errors as actionable defects, not noise.

## Boundary Typing Priorities

1. Type runtime config shape.
2. Type API input/output contracts at server routes.
3. Type composable return signatures.
4. Type component props/emits/slots where contracts are non-trivial.
5. Type store state/actions/getters if a store solution is used.

## Modern TypeScript Features to Prefer

- `satisfies` for validating object conformance without widening.
- `as const` for stable literal inference.
- Discriminated unions for UI/data state machines.
- Template literal types for constrained string patterns.
- Generic helper types for reusable composable contracts.

## Practical Rules

- Avoid `any`; prefer `unknown` + narrowing when needed.
- Keep exported/public API types explicit.
- Prefer inference for local implementation details.
- Avoid type assertions unless narrowing is impossible.
- Centralize shared domain types; avoid duplicate ad-hoc type copies.

## Vue-Specific Typing

- Type `defineProps`/`defineEmits` explicitly when contracts matter.
- Type computed/composable outputs that cross component boundaries.
- Type async data and server response payloads at call sites and shared helpers.

## Error Handling and Results

- Use typed error/result envelopes at server boundaries.
- Map transport errors into stable domain-level error types.
- Keep nullable and optional behavior explicit in types.

## Quality Gates

- Run type checking before finalizing code changes.
- Reject code that compiles only through broad assertions.
- Ensure generated code remains compatible with strict mode.
