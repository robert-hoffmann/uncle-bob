# UB CSS

Source: `.agents/skills/ub-css/SKILL.md`

`ub-css` guides plain CSS architecture, Vue/Nuxt style blocks, design tokens,
cascade control, layout, theming, accessibility styling, and progressive
enhancement.

## When To Use It

Use it for `.css` files, style blocks, selectors, specificity, cascade layers,
tokens, layout, browser-support fallback policy, and CSS architecture.

## What It Changes

- treats tokens as a system contract
- uses cascade layers to avoid specificity escalation
- favors platform CSS and progressive enhancement
- keeps accessibility, motion, and fallback behavior visible

## Common Prompts

- “Use `ub-css` to structure these design tokens.”
- “Review this selector strategy for maintainability.”
- “Add a fallback for this modern CSS feature.”

## Boundaries

Do not use it as the primary owner for Tailwind setup or utility workflow.
Pair with `ub-tailwind` when both CSS architecture and Tailwind matter.

## Tradeoffs

Strength: keeps styling maintainable without unnecessary abstraction.

Cost: token and cascade discipline can feel heavy for a one-off style tweak.
