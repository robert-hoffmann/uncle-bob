# Nuxt 3 to Nuxt 4 Deltas

## Purpose

Provide a single source of truth for high-impact Nuxt 3 -> Nuxt 4 changes that affect scaffolding, code review, and migration guidance.

## Migration Matrix (v3 Pattern -> v4 Pattern -> Why It Matters)

| v3 pattern | v4 pattern | Why it matters |
| --- | --- | --- |
| Root app dirs like `pages/`, `components/`, `layouts/`, `middleware/`, `plugins/` | Put app source in `app/pages`, `app/components`, `app/layouts`, `app/middleware`, `app/plugins` | Nuxt 4 defaults to an `app/` source directory; generating v3 paths causes drift and confusion. |
| Root `app.vue` and root `app.config.ts` | `app/app.vue` and `app/app.config.ts` | Aligns with Nuxt 4 source boundaries and app auto-discovery rules. |
| `~` / `@` commonly resolve to project root (when app source lived there) | `~` / `@` resolve to app source directory (default `app/`); use `~~` / `@@` for project root | Import paths can silently break after migration if root-vs-app aliases are confused. |
| Async data often assumed deep reactivity by default | `useAsyncData`/`useFetch` default to `deep: false` | Nested mutation assumptions become fragile unless `deep: true` is explicitly required. |
| Idle/loading logic often keyed off historical `pending` assumptions | Nuxt 4 behavior aligns on explicit status flow; `pendingWhenIdle` is disabled by default | Prevents stale loading UX by preferring `status`-driven UI states. |
| Async dedupe assumptions from older defaults | `dedupe` defaults to `cancel` | Repeated keyed requests can cancel in-flight runs; code must choose `defer` intentionally. |
| Prerender payload sharing often opt-in | `sharedPrerenderData` enabled by default | Keys must be uniquely tied to route identity to avoid payload reuse bugs. |
| `data`/`error` often treated as `null` default | `data`/`error` may be `undefined`; `getCachedData` `null`/`undefined` means cache miss | Null-only checks and custom cache logic must be updated to explicit miss semantics. |

## Official Upgrade and Codemod Path

1. Start from the official Nuxt upgrade guide for current migration constraints and behavior notes.
2. Run the official migration recipe codemod:

```bash
npx codemod@latest nuxt/4/migration-recipe
```

1. Reconcile imports and paths after codemod, especially alias usage and app-vs-root placements.
2. Typecheck and run app tests to catch behavior-level changes in async data and rendering.

## Compatibility Caveats

- For staged migrations on Nuxt 3, use Nuxt's compatibility settings to pre-align with Nuxt 4 behavior before full upgrade.
- Treat `future.compatibilityVersion` as a detection and reporting checkpoint in reviews.
- Reject mixed guidance that partially applies v3 folder conventions and partially applies v4 runtime behavior.

## Module and Layer Caveats

- Layers should follow Nuxt 4 structure as well (app source under each layer's `app/` boundary).
- Avoid hard-coded root alias assumptions in modules and templates (`~`/`@` may point to app source, not project root).
- When generating imports in modules, prefer explicit root aliases (`~~`/`@@`) only when root resolution is truly required.
- Verify auto-import outcomes after migration by checking generated Nuxt type artifacts (for example, imports and app typings) rather than assuming v3 scan roots.

## Agent Output Expectations

- Always emit Nuxt 4 file paths by default.
- Always call out async data defaults when discussing fetch/data state behavior.
- Always document alias intent when adding or changing imports across app, server, and shared boundaries.
