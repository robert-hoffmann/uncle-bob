# Vue 3 Legacy Replacements and Migration Guardrails

Use this reference when modernizing existing codebases. Never emit legacy patterns for new code.

## Legacy to Modern Replacement Matrix

| Legacy pattern | Modern replacement | Notes |
| -------------- | ------------------ | ----- |
| Options API for new features | Composition API with script setup and TypeScript | Keep Options API only as temporary compatibility in existing modules |
| `modelValue` + `update:modelValue` boilerplate | `defineModel()` | Prefer macro-based model contracts in Vue 3.4+ |
| `const el = ref(null)` for string template refs | `useTemplateRef()` | Prefer explicit template-ref helper in Vue 3.5+ |
| Watching destructured props directly | Watch getter (`() => prop`) | Destructured props are reactive reads, not direct watch sources |
| Cleanup after `await` in watcher | Register `onWatcherCleanup()` before `await` | Cleanup must be synchronous with active watcher context |
| Deep watch with `deep: true` everywhere | Narrow getter watch, or numeric `deep` | Use depth limits only where required |
| Mixins for shared logic | Typed composables | Keep shared behavior explicit, testable, and typed |
| Class-style component decorators | Composition API and macros | Avoid class-based Vue patterns in new code |
| Template filters | Computed values and plain functions | Filters are legacy and less explicit |

## Do Not Generate Checklist

- Do not generate new Options API components.
- Do not generate mixins, filters, or class-style decorator patterns.
- Do not generate new code that relies on `this` for component state logic.
- Do not generate manual model boilerplate where `defineModel()` is available.
- Do not generate watch sources that pass destructured props by value.
- Do not generate watcher cleanup registration after async boundaries.

## Allowed Compatibility Exceptions

Allow temporary retention only if all conditions are true:

1. The legacy code already exists and is in active use.
2. Immediate full migration would create unacceptable delivery risk.
3. The retained area is clearly scoped and documented.
4. A concrete follow-up plan exists with sequence and expected completion scope.

When retaining compatibility code, annotate:

- why compatibility is needed,
- what breaks if removed now,
- what replacement is planned next,
- when/where migration will continue.

## Incremental Migration Sequence

1. Introduce TypeScript boundaries first:
   - type props, emits, API payloads, and composable contracts.
2. Migrate stateful logic from Options API sections to composables:
   - move `data`, `computed`, and `methods` progressively.
3. Replace `v-model` boilerplate with `defineModel()` where compatibility allows.
4. Replace template ref patterns with `useTemplateRef()` in touched components.
5. Normalize watcher behavior:
   - convert watch sources to getters,
   - move cleanup to synchronous `onWatcherCleanup()`,
   - reduce broad deep watchers.
6. Apply SSR and hydration fixes in SSR-enabled apps:
   - `useId()` for IDs,
   - targeted mismatch suppression,
   - lazy hydration for expensive islands.
7. Remove remaining compatibility shims once tests and downstream usage confirm parity.

## Review Prompts for Migration PRs

- Is this PR adding any new legacy pattern? If yes, block or request rewrite.
- Is retained legacy explicitly justified and bounded?
- Is there a clear next step that reduces legacy surface area?
- Are watcher, model, and template-ref patterns aligned with Vue 3.5 guidance?
