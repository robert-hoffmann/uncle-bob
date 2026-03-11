# Vue 3.5 Modern Patterns (Stable Baseline)

Use this reference for modern Vue core patterns in Vue 3.5.x with strict TypeScript.

## Script Setup and TypeScript Baseline

- Default to SFC + `script setup` + `lang="ts"`.
- Keep component contracts explicit with typed props, emits, models, and slots when needed.
- Prefer inferred types internally; keep exported and boundary types explicit.

```vue
<script setup lang="ts">
const props = defineProps<{
  title: string
  count?: number
}>()
</script>
```

## Reactive Props Destructure

Reactive props destructure is modern in Vue 3.5+ and supports inline defaults.

```ts
const { page = 1, pageSize = 25 } = defineProps<{
  page?: number
  pageSize?: number
}>()
```

Important caveat: destructured values are reactive reads, not watch sources by value.

```ts
watch(() => pageSize, (next) => {
  console.log(next)
})
```

## Modern Component v-model with defineModel

Prefer `defineModel()` for new `v-model` component contracts.

```vue
<script setup lang="ts">
const model = defineModel<string>({ default: "" })
</script>

<template>
  <input v-model="model" />
</template>
```

Use manual `modelValue` and `update:modelValue` only for bounded compatibility scenarios.

## Template Refs with useTemplateRef

Prefer `useTemplateRef()` for string refs.

```vue
<script setup lang="ts">
import { onMounted, useTemplateRef } from "vue"

const inputEl = useTemplateRef<HTMLInputElement>("search")

onMounted(() => inputEl.value?.focus())
</script>

<template>
  <input ref="search" />
</template>
```

## Watchers and Cleanup

Register cleanup synchronously with `onWatcherCleanup()` before any async boundary.

```ts
watch(query, async (next) => {
  const controller = new AbortController()
  onWatcherCleanup(() => controller.abort())

  await fetch(`/api/search?q=${encodeURIComponent(next)}`, {
    signal: controller.signal,
  })
})
```

For deep watch, prefer precise getters first. If deep watching is required, use numeric depth conservatively.

```ts
watch(
  () => state.filters,
  () => {
    // ...
  },
  { deep: 1 },
)
```

## Composables: Accept Value, Ref, or Getter

Use `MaybeRefOrGetter<T>` and `toValue()` to keep call sites ergonomic and compatible with destructured props.

```ts
import { computed, toValue } from "vue"
import type { MaybeRefOrGetter } from "vue"

export function useNormalizedQuery(input: MaybeRefOrGetter<string>) {
  return computed(() => toValue(input).trim())
}
```

## SSR and Hydration Primitives

- Use `useId()` for SSR-safe unique IDs.
- Use lazy hydration strategies for async components when practical.
- Use `data-allow-mismatch` only for known unavoidable mismatches, with narrow scope.
- Use `Teleport defer` when targets render later.

```ts
const HeavyWidget = defineAsyncComponent({
  loader: () => import("./HeavyWidget.vue"),
  hydrate: hydrateOnVisible({ rootMargin: "200px" }),
})
```

## Performance and Compile-Time Guardrails

- Favor stable props and split large UI regions into async boundaries.
- Use virtualization for large lists.
- Use shallow reactivity APIs for very large immutable-like structures.
- Keep compile-time flags intentional and explicit:
  - `__VUE_OPTIONS_API__`
  - `__VUE_PROD_DEVTOOLS__`
  - `__VUE_PROD_HYDRATION_MISMATCH_DETAILS__`

## Stable vs Beta Policy

- Baseline: Vue 3.5.x stable behavior.
- Beta features: do not generate by default. Require explicit user request before introducing 3.6 beta-only behavior.
