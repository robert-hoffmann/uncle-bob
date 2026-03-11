# Tailwind v4 Guardrails

Use this document as the hard guardrails layer when generating or reviewing Tailwind output.

## Core Principle

Apply Tailwind v4 CSS-first patterns and reject legacy syntax by default.

## Do

- Use `@import "tailwindcss"` as the standard CSS entrypoint.
- Use v4 directives when needed: `@theme`, `@utility`, `@variant`, `@custom-variant`, `@source`, `@reference`, `@apply`.
- Keep tokens in `@theme` and reuse them consistently.
- Use `@source` only when automatic source detection misses files.
- Use `@source inline()` when an explicit safelist-like include is required.
- In Vue/Nuxt component-local styles that use `@apply` or `@variant`, add `@reference` to make theme/context available.
- If PostCSS integration is required, use `@tailwindcss/postcss` (not the old `tailwindcss` PostCSS plugin entry).
- If CLI integration is required, use `@tailwindcss/cli`.

## Do Not

- Do not introduce `@config` unless explicit legacy compatibility is required.
- Do not introduce `@plugin` unless explicit legacy compatibility is required.
- Do not assume Tailwind v4 requires PostCSS setup.
- Do not copy obsolete v3-era setup snippets when v4-native patterns exist.
- Do not mix multiple setup styles (for example CDN plus build-time plugin) in the same app unless the user explicitly asks.
- Do not use `@tailwind base`, `@tailwind components`, `@tailwind utilities` as the default modern entrypoint.
- Do not emit `tw-` prefix syntax in v4 projects; prefix is variant-like (for example `tw:flex`).
- Do not assume right-to-left variant stacking behavior from v3.

## High-Impact Upgrade Traps

Treat these changes as mandatory migration checks:

- Prefix format changed from prefix-as-token (for example `tw-bg-red-500`) to prefix-as-variant (for example `tw:bg-red-500`).
- Variant stacking order is left-to-right in v4.
- Arbitrary CSS variable shorthand changed from bracket form to parenthesis form:
  - v3 style: `bg-[--brand-color]`
  - v4 style: `bg-(--brand-color)`
- `@source inline()` replaces many legacy safelist-only use cases.

## Legacy Trap Detection

Treat these as red flags during review:

- JavaScript config-first setup where CSS-first setup is sufficient.
- Instructions that require PostCSS as a default prerequisite.
- Missing `@reference` in component-scoped styles using `@apply`/`@variant`.
- Deprecated directives presented as standard flow.
- Prefix migration not applied (`tw-` style classes still emitted for v4).
- Variant behavior explanations that assume right-to-left stacking.
- Arbitrary variable syntax left in pre-v4 bracket shorthand.

## Environment-Specific Validation

After generating code, verify:

1. The setup matches the actual environment (CDN, Vite, Nuxt).
2. The entrypoint and directives are Tailwind v4-compatible.
3. Legacy directives are absent, or clearly justified by compatibility constraints.
4. Token definitions are centralized and reused.
5. Build/tooling assumptions are minimal and current.
6. Nuxt guidance (if applicable) follows the official framework guide path.
7. Prefix/variant/arbitrary-value syntax reflects v4 behavior.

## Compatibility Exception Rule

If legacy syntax is unavoidable:

1. State why compatibility requires it.
2. Isolate the compatibility layer to the smallest possible scope.
3. Offer a migration path back to v4-native patterns.
4. Document limitations when using `@config`/`@plugin` as compatibility directives (not all JavaScript-config features map 1:1 to CSS-first v4 behavior).
