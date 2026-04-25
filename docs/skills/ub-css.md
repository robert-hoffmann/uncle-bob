# UB CSS

Source: `.agents/skills/ub-css/SKILL.md`

`ub-css` guides plain CSS architecture, Vue/Nuxt style blocks, design tokens,
cascade control, selectors, layout, theming, accessibility styling, browser
support, and progressive enhancement.

## Core Principles

- Treat design tokens as a system contract.
- Use cascade layers to avoid specificity escalation.
- Prefer platform CSS before adding extra styling dependencies.
- Keep nesting shallow and selectors maintainable.
- Use container queries and modern layout primitives where they match the
  component boundary.
- Apply progressive enhancement when modern features need fallback policy.
- Respect accessibility states, motion preferences, and performance-oriented
  CSS features.

## Behavior In Practice

- Starts with the token source of truth, ideally DTCG-shaped token data, then
  maps canonical values into CSS custom properties and semantic aliases.
- Uses CSS variables as the runtime contract and bridges them into Tailwind
  `@theme` or framework style blocks so utility classes and raw CSS do not
  drift.
- Defines cascade order with `@layer`, including vendor isolation, instead of
  fighting specificity with longer selectors.
- Uses native nesting for local state and descendant relationships, but keeps
  depth shallow so selectors stay readable and portable.
- Chooses container queries for component-internal responsiveness and viewport
  media queries for page-shell layout.
- Uses modern selectors like `:has()`, `:is()`, and `:where()` when they
  simplify markup or specificity, while preserving accessible `:focus-visible`
  states.
- Prefers modern layout, sizing, color, and internationalization primitives:
  Grid/Flex gaps, logical properties, `aspect-ratio`, `clamp()`, `oklch`,
  `color-mix()`, and theme-aware color behavior.
- Gates partial-support features with `@supports` and documents fallback
  behavior instead of pretending every browser has identical capability.

## Reference Highlights

- `.agents/skills/ub-css/references/modern-css-source.md`: DTCG token
  contract, CSS-variable mapping, Tailwind `@theme` bridge, SFC style usage,
  cascade layers, native nesting, container queries, modern selectors,
  progressive enhancement, and source-backed feature notes.
- `.agents/skills/ub-css/references/browser-support-baseline.md`: browser
  support tiers, broadly safe defaults, enhancement-tier features, limited or
  experimental features, and fallback policy.

## Progressive Disclosure

The main skill handles CSS architecture and styling ownership. Load the modern
CSS source when the task needs patterns or framework bridges. Load browser
support guidance when fallback policy or feature gating affects the result.

## Common Invocation Examples

- “Use `ub-css` to structure these design tokens.”
- “Review this selector strategy for maintainability.”
- “Add a fallback for this modern CSS feature.”
- “Decide whether this should be a token, utility, or component style.”

## Boundaries

Do not use it as the primary owner for Tailwind setup or utility workflow. Pair
with `ub-tailwind` when both CSS architecture and Tailwind matter.

## Tradeoffs

Strength: keeps styling maintainable without unnecessary abstraction.

Cost: token and cascade discipline can feel heavy for a one-off style tweak.
