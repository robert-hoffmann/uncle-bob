# Tailwind v3 to v4 Deltas

## Purpose

Capture high-impact Tailwind v3 -> v4 differences so generated guidance consistently produces modern, upgrade-safe output.

## Migration Matrix (v3 pattern -> v4 pattern -> why it matters -> canonical replacement)

| v3 pattern | v4 pattern | Why it matters | Canonical replacement |
| --- | --- | --- | --- |
| `@tailwind base; @tailwind components; @tailwind utilities;` | `@import "tailwindcss";` | v4 is CSS-first and no longer uses directive triplets as the default entrypoint. | Replace old directives with a single `@import "tailwindcss";` in the main stylesheet. |
| PostCSS plugin `tailwindcss` | PostCSS plugin package `@tailwindcss/postcss` | v4 moved PostCSS integration to a dedicated package. | Install/use `@tailwindcss/postcss` in PostCSS config when PostCSS is required. |
| CLI via `tailwindcss` package/binary | CLI via `@tailwindcss/cli` | v4 moved CLI into a dedicated package. | Use `npx @tailwindcss/cli ...` for CLI workflows. |
| Prefix in class token (`tw-bg-red-500`) | Prefix as variant (`tw:bg-red-500`) | Class name generation/consumption changes in v4. | Migrate prefixed classes to `tw:*` variant style. |
| Right-to-left variant stacking assumptions | Left-to-right variant stacking | Variant order semantics changed and can alter selector output. | Reorder stacked variants to match left-to-right behavior. |
| Arbitrary variable shorthand `bg-[--brand-color]` | Arbitrary variable shorthand `bg-(--brand-color)` | Bracket shorthand syntax changed for CSS variable values. | Replace bracket variable shorthand with parenthesis form. |
| Safelist-only workflow in JS config | `@source inline()` in CSS when explicit include is needed | v4 CSS-first source controls replace many safelist-only use cases. | Add `@source inline()` for explicit generation targets. |
| Scoped Vue/Nuxt styles use `@apply` without shared theme context | Scoped styles using `@apply`/`@variant` require `@reference` | Theme variables/utilities are not automatically in scope in local style blocks. | Add `@reference` to the app/main stylesheet from the component style block. |
| Fresh Nuxt setups defaulting to legacy module guidance | Official Nuxt flow uses `@tailwindcss/vite` in `nuxt.config.*` and CSS registration | Keeps Nuxt instructions aligned with current Tailwind docs. | Use Nuxt framework guide path: install module, configure `vite.plugins`, register `~/assets/css/main.css`, and `@import "tailwindcss";`. |

## Representative Utility Renames and Defaults to Catch

- `shadow-sm` -> `shadow-xs`
- `shadow` -> `shadow-sm`
- `blur-sm` -> `blur-xs`
- `blur` -> `blur-sm`
- `rounded-sm` -> `rounded-xs`
- `rounded` -> `rounded-sm`
- `outline-none` -> `outline-hidden`
- Default `ring` width changed to `1px` (`ring-3` for prior default-like thickness)
- Default `ring` color changed to `currentColor` (explicit color utilities may be needed)

## JavaScript Config Compatibility Caveat

- `@config` and `@plugin` can be used as compatibility directives when a full migration is not yet possible.
- Treat this as a bounded fallback: keep compatibility scope minimal and prefer migrating tokens/utilities/variants into CSS-first directives (`@theme`, `@utility`, `@variant`).
- Do not assume every legacy JavaScript config behavior maps 1:1 in v4.

## Upgrade Command

Use the official upgrade tool first when modernizing existing projects:

```bash
npx @tailwindcss/upgrade
```
