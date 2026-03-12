# Modern CSS Source (Web Applications)

Quick reference for modern CSS authoring across HTML pages, Vue/Nuxt/Quasar SFC styles, and Tailwind pipelines.

## DTCG Token Contract (Canonical -> Runtime)

Use DTCG-style JSON as the canonical token source, then map to runtime CSS variables.

```json
{
  "color": {
    "brand": {
      "primary": {
        "$type": "color",
        "$value": "oklch(62% 0.2 256)",
        "$description": "Primary brand accent"
      }
    }
  },
  "space": {
    "4": { "$type": "dimension", "$value": "1rem" }
  }
}
```

```css
:root {
    --color-brand-primary : oklch(62% 0.2 256);
    --space-4             : 1rem;
}
```

## Tailwind Bridge (`@theme`)

Keep Tailwind theme variables aligned with runtime CSS variable naming so utilities and raw CSS stay in sync.

```css
@import "tailwindcss";

@theme {
    --color-brand-primary : oklch(62% 0.2 256);
    --spacing-4           : 1rem;
    --radius-md           : 0.5rem;
}
```

## Vue / Nuxt / Quasar SFC Style Usage

Use CSS vars directly; reserve `v-bind()` for reactive component values.

```vue
<style scoped>
.card {
    padding       : var(--space-4);
    border-radius : var(--radius-md);
    background    : var(--color-surface-default);
    color         : var(--color-text-default);
}

.card[data-tone="brand"] {
    border-color : var(--color-brand-primary);
}

.card[data-progress] {
    --progress : v-bind(progressPercent);
    inline-size : calc(var(--progress) * 1%);
}
</style>
```

## Cascade Strategy (`@layer`)

Use layers to make override order explicit and avoid specificity arms races.

```css
@layer reset, vendor, tokens, base, components, utilities, overrides;
@import url("vendor.css") layer(vendor);

@layer tokens {
    :root { --space-4: 1rem; }
}

@layer components {
    .card { padding: var(--space-4); }
}
```

## Nesting + Container Queries

```css
.card-shell {
    container : card / inline-size;
}

.card {
    display : grid;
    gap     : var(--space-4);

    &:hover {
        box-shadow : var(--shadow-sm);
    }

    @container card (min-width: 30rem) {
        grid-template-columns : 12rem 1fr;
    }
}
```

## Progressive Enhancement Pattern

```css
.form-group {
    border-inline-start : 2px solid transparent;
}

@supports selector(:has(*)) {
    .form-group:has(.is-invalid) {
        border-inline-start-color : var(--color-danger);
    }
}
```

```css
.hero {
    min-block-size : 100vh;  /* fallback */
    min-block-size : 100dvh; /* modern viewport behavior */
}
```

## Feature Use Notes

- Safe defaults: nesting, container size queries, `:has()`, `@layer`, logical properties, `aspect-ratio`.
- Enhancement tier: `light-dark()`, `@scope`, anchor positioning, scroll-driven animation, style queries.
- Limited tier: container scroll-state queries, CSS `if()`, grid lanes/masonry.

## Primary Standards And Docs

- DTCG home: <https://www.designtokens.org/>
- DTCG 2025.10 technical reports: <https://www.designtokens.org/tr/2025.10/>
- DTCG editor drafts (including format): <https://www.designtokens.org/tr/drafts/>
- Tailwind CSS configuration and theme variables: <https://tailwindcss.com/docs/configuration>
- Vue SFC CSS features (`v-bind()` in style): <https://vuejs.org/api/sfc-css-features>
