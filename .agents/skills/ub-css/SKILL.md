---
name: ub-css
description: Use this skill for plain CSS and style-block architecture. Apply it when the task involves .css files, selectors, specificity, cascade layers, tokens, layout or theming, accessibility styling, browser-support fallbacks, or CSS architecture in Vue, Nuxt, or Tailwind-bearing projects.
---

# UB CSS

## Overview

Apply modern CSS platform features with predictable cascade control, token-driven styling, and progressive enhancement. Treat design tokens as a system contract, keep selectors and specificity maintainable, and prefer native CSS features over legacy Sass-era workarounds.

## Load References On Demand

- Read `../ub-authoring/references/authoring-conventions.md` when adjusting routing
  guidance or cross-skill authoring conventions.
- Read `references/modern-css-source.md` for copy-ready patterns and framework bridges (Vue/Nuxt/Quasar/Tailwind).
- Read `references/browser-support-baseline.md` when deciding fallback policy or feature gating.

## When Not To Use

- Do not use this skill when Tailwind utility workflow, Tailwind setup, or
  Tailwind migration is the primary change surface; co-load or defer to
  `ub-tailwind` depending on whether CSS architecture remains a first-class
  concern.
- Do not use this skill when the main problem is Nuxt runtime behavior, app
  structure, or Nitro/server concerns; defer that to `ub-nuxt`.
- Do not use this skill for general Vue component logic when CSS is secondary
  to component architecture.

## Core Workflow

1. Confirm token source of truth (DTCG JSON or existing token registry).
2. Map tokens to runtime CSS custom properties and semantic aliases.
3. Define cascade order with `@layer` and isolate vendor CSS in a vendor layer.
4. Implement component styles with native nesting, modern selectors, and container queries.
5. Add fluid sizing, logical properties, and modern color/theming primitives.
6. Gate partial-support features with `@supports` and explicit fallback behavior.
7. Review accessibility, motion preferences, and performance-oriented CSS features.

## Modern CSS Rules

### 1. Use Design Tokens As The Source Of Truth (DTCG-First)

- Prefer DTCG token format for canonical token data (`$value`, `$type`, `$description`, alias references).
- Map canonical tokens to CSS custom properties in global and semantic scopes.
- Keep semantic token names stable; allow value churn behind them.
- Avoid hard-coded values in components unless a one-off value is intentional and documented.

```json
{
  "color": {
    "brand": {
      "primary": { "$type": "color", "$value": "oklch(62% 0.2 256)" }
    },
    "surface": {
      "default": { "$type": "color", "$value": "#ffffff" }
    }
  }
}
```

```css
:root {
    --color-brand-primary   : oklch(62% 0.2 256);
    --color-surface-default : #ffffff;
    --space-4               : 1rem;
    --radius-md             : 0.5rem;
}
```

### 2. Bridge Tokens Into Framework CSS Pipelines

- Vue/Nuxt/Quasar: consume CSS vars directly in SFC style blocks; use `v-bind()` only for component-reactive values.
- Tailwind (latest stable): keep tokens in `@theme` and align naming with CSS vars so utilities and raw CSS share the same source values.
- Keep token mapping deterministic so design, app CSS, and utility classes stay synchronized.

```css
@theme {
    --color-brand-primary : oklch(62% 0.2 256);
    --spacing-4           : 1rem;
    --radius-md           : 0.5rem;
}
```

### 3. Control Cascade Predictably With `@layer`

- Declare global layer order once.
- Import third-party CSS into a dedicated vendor layer.
- Use layers to avoid specificity escalation.

```css
@layer reset, vendor, tokens, base, components, utilities, overrides;
@import url("vendor.css") layer(vendor);
```

### 4. Use Native Nesting, But Keep It Shallow

- Use native nesting for state selectors, local descendants, and colocated queries.
- Keep depth at `<= 3` levels.
- Avoid deep DOM-coupled selectors.

### 5. Use Container Queries For Component Responsiveness

- Set `container: <name> / inline-size` (or `container-type` + `container-name`) at component boundaries.
- Prefer container queries for component internals; keep viewport media queries for page shell layout.
- Use container query units (`cqw`, `cqh`, `cqi`, `cqmin`, `cqmax`) when sizing should track container width/height.

### 6. Use Modern Selectors Deliberately

- Use `:has()` for parent/state-driven styling where it simplifies markup/JS.
- Use `:is()` to group selector variants with normal specificity.
- Use `:where()` for zero-specificity defaults.
- Always include accessible keyboard focus states with `:focus-visible`.

### 7. Prefer Modern Layout, Sizing, and Internationalization Primitives

- Use Grid/Flex with `gap` instead of margin-based spacing hacks.
- Use `clamp()`, `min()`, `max()`, and `calc()` for fluid sizing.
- Prefer logical properties (`padding-inline`, `border-inline-start`, `inset-block`) over physical left/right properties.
- Use `aspect-ratio` instead of padding-box ratio hacks.

### 8. Use Modern Color and Theming Primitives

- Prefer perceptual color spaces (`oklch`) for token values.
- Derive variants with `color-mix()` instead of manually duplicating palettes.
- Use `color-scheme` and `light-dark()` when dual-theme behavior is needed.
- Treat `accent-color` as enhancement, not correctness-critical styling.

### 9. Handle Motion, Interaction, and Performance Intentionally

- Respect user preferences (`prefers-reduced-motion`, contrast and forced-color modes where relevant).
- Use `@starting-style`, `transition-behavior: allow-discrete`, and popover hooks as enhancement patterns.
- Use `content-visibility` and containment for long lists and heavy offscreen content.
- Use `scrollbar-gutter: stable` to reduce layout shift during scrollbar appearance.

## Progressive Enhancement Policy (Tiered Modern-First)

- Safe default: use broadly supported modern features by default.
- Enhancement tier: require `@supports` guard plus acceptable fallback behavior.
- Limited/experimental tier: use only with explicit justification and easy rollback.

## Documentation, Organization, And Formatting

### Organization

- Split styles by role when codebase size justifies it:
  - `styles/tokens.css`
  - `styles/base.css`
  - `styles/components/*.css`
  - `styles/utilities.css`
- Keep component styles close to components when practical.
- Centralize global token definitions to reduce drift.

### Documentation

- Add short comments for non-obvious intent, fallback rationale, or compatibility constraints.
- Document why partial-support features are used.
- Keep comments focused on `why`, not `what`.

### Formatting

- Keep property ordering logical:
  1. Layout (`display`, `position`, grid/flex, `z-index`)
  2. Box model (`inline-size/block-size`, `margin`, `padding`, `border`)
  3. Typography (`font-*`, `line-height`, `text-*`)
  4. Visual (`background`, `color`, `box-shadow`, `opacity`, `filter`)
  5. Motion (`transform`, `transition`, `animation`)
- Use consistent spacing and alignment.
- Prefer small, single-purpose selector blocks.

## Completion Checklist

- Token model is defined and mapped cleanly into CSS custom properties.
- Hard-coded values are minimized and justified when present.
- Layer order is explicit and vendor CSS is isolated.
- Nesting is shallow and readable.
- Container queries and modern selectors are used where they simplify code.
- Accessibility states include `:focus-visible` and motion preferences are respected.
- Enhancement and limited features are gated with fallbacks.
- Comments are concise and intent-focused.

## Version & Research Policy

- Use web search to verify current browser support data before recommending or gating CSS features.
- Inspect the host repository's `AGENTS.md` or equivalent instructions when
  present for project-specific version policy and tooling; do not assume it
  contains this catalog's defaults.
- Do not hardcode snapshot dates or version numbers in generated guidance — keep recommendations evergreen.

## Output Requirements

When generating or reviewing CSS guidance, include:

1. Token note: source of truth for tokens and how they map into runtime CSS.
2. Cascade note: layer order and selector-specificity strategy.
3. Enhancement note: which features are baseline versus gated by `@supports`.
4. Accessibility note: focus, motion, contrast, and forced-color considerations.
5. Validation note: lint, build, browser-support, or manual verification steps actually used.
