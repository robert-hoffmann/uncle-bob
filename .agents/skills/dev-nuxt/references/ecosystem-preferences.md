# Ecosystem Preferences (Nuxt + Vue)

## Decision Heuristic

1. Prefer Nuxt-native capability first.
2. Prefer VueUse second for client/runtime utility behavior.
3. Add third-party libraries only when they deliver clear capability beyond Nuxt/VueUse.
4. Prefer actively maintained packages with strong TypeScript support.

## VueUse-First Areas

Prefer VueUse for:

- Browser API wrappers (storage, media query, clipboard, device/sensors).
- Reactive timing/control helpers (debounce/throttle, interval/timeout wrappers).
- Async utility composables.
- Lifecycle and event composables.

## Common Package Choices (Modern)

- Validation: `zod` for schema-first runtime + TypeScript alignment.
- Forms: `vee-validate` (+ `zod` resolver where appropriate) for complex form workflows.
- Data tables/UI primitives: prefer headless, actively maintained Vue-first options.
- State management (when needed): typed modern store approaches with explicit contracts.
- Date/time: lightweight modern libraries with timezone support only when required.
- i18n: official Nuxt/Vue i18n integrations where localization is needed.

## Selection Guardrails

- Reject libraries that duplicate Nuxt core features.
- Reject packages with stale maintenance signals.
- Reject dependencies without TypeScript support or clear typing story.
- Prefer composable and tree-shakeable APIs.
- Reject workaround packages introduced only to preserve Nuxt 3 conventions when Nuxt 4 native structure/runtime behavior already covers the use case.

## Tailwind Handling

For Tailwind v4 setup and migration details, defer to:

- `.agents/skills/dev-tailwind/SKILL.md`
- `.agents/skills/dev-tailwind/references/tailwind-v4-guardrails.md`
- `.agents/skills/dev-tailwind/references/framework-recipes.md`

Keep Nuxt skill guidance focused on integration decisions, not Tailwind implementation internals.

## Legacy Replacement Matrix

- Generic utility package for browser/reactive helpers -> VueUse composables.
- Custom fetch wrapper without Nuxt integration -> `useFetch`/`useAsyncData` + typed helpers.
- Untyped validation helpers -> schema-first typed validation.
- Broad global singleton patterns -> focused composables or typed stores.
- Alias/path workaround plugin for root-vs-app confusion -> explicit Nuxt 4 aliases (`~`, `@`, `~~`, `@@`) and `app/`-first structure.
