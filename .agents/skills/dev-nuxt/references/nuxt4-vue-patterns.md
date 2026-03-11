# Nuxt 4 + Vue Patterns

## Purpose

Apply Nuxt 4-native architecture with modern Vue Composition API and explicit server/client boundaries.

## Workflow

1. Detect project mode and modules from `package.json`, `nuxt.config.*`, and lockfiles.
2. Confirm Nuxt 4 structure assumptions:
   - app source is under `app/`
   - runtime roots (`server/`, `shared/`, `public/`, `modules/`) remain in project root
   - `srcDir` / `dir.app` overrides are intentional and understood
3. Choose rendering strategy first: SSR, SSG/prerender, or hybrid.
4. Place code in the right runtime boundary:
   - `server/api/*` and `server/routes/*` for backend HTTP behavior.
   - shared composables/types in `shared/*` when needed by both app and server.
   - client-only logic behind runtime checks when required.
5. Implement data flows with Nuxt primitives before introducing custom abstractions.
6. Verify route-level behavior, payload shape, async-data state transitions, and hydration assumptions.

## Modern Nuxt Defaults

- Prefer `<script setup lang="ts">` in Vue SFCs.
- Prefer `useAsyncData`/`useFetch` for route and page data loading.
- Prefer Nitro server routes for API endpoints instead of separate ad-hoc servers.
- Prefer route rules/config over custom runtime branching where possible.
- Prefer composables for reuse instead of global mutable helpers.
- Prefer app aliases that match Nuxt 4 defaults (`~`/`@` map to the app source directory).

## Nuxt 4 Async Data and Fetch Semantics

These defaults and behaviors are mandatory guardrails for generated/reviewed code:

- `deep` defaults to `false` for `useAsyncData` and `useFetch` (shallow refs by default).
  - implication: do not assume deep reactivity for nested object mutation; prefer immutable updates or set `deep: true` intentionally.
- `dedupe` defaults to `cancel`.
  - implication: repeated requests with same key can cancel in-flight requests; set `dedupe: 'defer'` only when queueing behavior is required.
- `pendingWhenIdle` is disabled by default in Nuxt 4 behavior.
  - implication: with `immediate: false`, `pending` stays `false` until first execution; use `status` (`idle` / `pending` / `success` / `error`) for UI state logic.
- Keyed async data calls share refs (`data`, `error`, `status`, `pending`) and require option consistency.
  - options that must remain consistent for a shared key include handler, `deep`, `transform`, `pick`, `getCachedData`, and `default`.
- `sharedPrerenderData` is enabled by default.
  - implication: keys must uniquely encode payload identity (for example route params) to prevent incorrect cache reuse across prerendered pages.
- `getCachedData` should return a value to skip fetch; `null` or `undefined` should be treated as a cache miss that triggers fetch.
  - implication: custom cache functions must use explicit miss semantics and avoid ambiguous return shapes.

## Anti-Regression Checks for Async Data

- Reject code that assumes `data`/`error` are `null` by default; handle `undefined` safely.
- Reject UI loading logic based only on `!pending`; prefer explicit `status` checks.
- Reject keyless `useAsyncData` in dynamic routes when payload identity depends on params/query.
- Reject mixed option sets for repeated keyed calls across components.
- Reject deep mutation assumptions when `deep` is not explicitly `true`.

## Server, Client, and Hydration Rules

- Keep browser-only APIs in client-safe branches.
- Keep secrets and privileged logic in server runtime only.
- Avoid hydration mismatch by making server and client initial state deterministic.
- Keep payloads minimal and typed.

## State and Data

- Keep state ownership local and explicit.
- Use typed stores/composables when shared state is needed.
- Normalize API response types at the server boundary.
- Model async states explicitly (`idle`, `loading`, `success`, `error`) for UI clarity.

## Routing and Navigation

- Use file-based routing defaults.
- Use typed route params/query parsing before business logic.
- Keep route middleware focused and side-effect minimal.

## Testing Focus

- Validate critical server routes and composables first.
- Add component tests for rendering branches driven by async/state conditions.
- Keep E2E for user-critical flows and route transitions.

## Anti-Patterns to Avoid

- Vue 2 era APIs in new code (`mixins`, filters, class-style components).
- Options API for net-new implementation unless required by surrounding constraints.
- Framework bypasses that duplicate existing Nuxt capabilities.
- Hidden global side effects in plugins/composables.
- Root-level v3 app directories (`pages/`, `components/`, `layouts/`, `middleware/`, `plugins/`) when generating Nuxt 4 file placements.
