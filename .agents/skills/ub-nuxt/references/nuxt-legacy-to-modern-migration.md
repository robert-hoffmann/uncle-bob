# Nuxt Legacy-to-Modern Migration

> Verify migration paths against the latest official Nuxt documentation via web search.

## Purpose

Provide a single source of truth for high-impact legacy-to-modern Nuxt changes that affect scaffolding, code review, and migration guidance.

## Migration Matrix (Legacy Pattern → Modern Pattern → Why It Matters)

| Legacy pattern | Modern pattern | Why it matters |
| --- | --- | --- |
| Root app dirs like `pages/`, `components/`, `layouts/`, `middleware/`, `plugins/` | Put app source in `app/pages`, `app/components`, `app/layouts`, `app/middleware`, `app/plugins` | Modern Nuxt defaults to an `app/` source directory; generating legacy paths causes drift and confusion. |
| Root `app.vue` and root `app.config.ts` | `app/app.vue` and `app/app.config.ts` | Aligns with modern Nuxt source boundaries and app auto-discovery rules. |
| `~` / `@` commonly resolve to project root (when app source lived there) | `~` / `@` resolve to app source directory (default `app/`); use `~~` / `@@` for project root | Import paths can silently break after migration if root-vs-app aliases are confused. |

## Official Upgrade and Codemod Path

1. Start from the official Nuxt upgrade guide for current migration constraints and behavior notes.
2. Run the official migration recipe codemod:

```bash
npx codemod@latest nuxt/4/migration-recipe
```

1. Reconcile imports and paths after codemod, especially alias usage and app-vs-root placements.
2. Typecheck and run app tests to catch behavior-level changes in async data and rendering.

## Compatibility Caveats

- For staged migrations, use Nuxt's compatibility settings to pre-align with modern behavior before full upgrade.
- Treat `future.compatibilityVersion` as a detection and reporting checkpoint in reviews.
- Reject mixed guidance that partially applies legacy folder conventions and partially applies modern runtime behavior.

## Module and Layer Caveats

- Layers should follow modern Nuxt structure as well (app source under each layer's `app/` boundary).
- Avoid hard-coded root alias assumptions in modules and templates (`~`/`@` may point to app source, not project root).
- When generating imports in modules, prefer explicit root aliases (`~~`/`@@`) only when root resolution is truly required.
- Verify auto-import outcomes after migration by checking generated Nuxt type artifacts (for example, imports and app typings) rather than assuming legacy scan roots.

## Agent Output Expectations

- Always emit modern Nuxt file paths by default.
- Always call out async data defaults when discussing fetch/data state behavior.
- Always document alias intent when adding or changing imports across app, server, and shared boundaries.
