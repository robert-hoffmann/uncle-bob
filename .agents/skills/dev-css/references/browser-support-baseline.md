# Browser Support Baseline

> This snapshot was last validated in February 2026. Always verify current browser support data via web search (caniuse.com) before making fallback decisions.

Use this baseline for initial fallback decisions. Re-check support for high-risk deliverables or strict enterprise browser matrices.

## Tier Matrix

| Tier | Feature | Global usage snapshot | Notes |
| ---- | ------- | --------------------: | ----- |
| Safe default | CSS nesting | 90.71% | Mature in modern engines |
| Safe default | Container queries (size) | 93.47% | Baseline for component responsiveness |
| Safe default | `:has()` | 93.71% | Prefer targeted relationships for performance |
| Safe default | `@property` | 94.57% | Enables typed, animatable custom properties |
| Safe default | `content-visibility` | 93.07% | Strong performance upside in long pages |
| Safe default | `scrollbar-gutter` | 93.05% | Prevents scrollbar-induced layout shift |
| Safe default | `aspect-ratio` | 95.26% | Replace padding hacks |
| Safe default | Logical properties | 96.46% | Prefer for RTL/writing mode resilience |
| Safe default | `color-mix()` | 91.26% | Useful for derived token variants |
| Enhancement | `text-wrap: balance` | 87.18% | Great for headings and display text |
| Enhancement | `light-dark()` | 84.93% | Pair with `color-scheme` |
| Enhancement | `@scope` | 86.22% | Valuable, still newer in many stacks |
| Enhancement | Anchor positioning | 76.65% | Require fallback for menus/tooltips |
| Enhancement | Scroll-driven animations | 78.18% | Not supported in Firefox (Feb 2026) |
| Enhancement | Container style queries | 87.86% | Partial; not supported in Firefox |
| Limited | Container scroll-state queries | 69.31% | Not supported in Safari/Firefox |
| Limited | CSS `if()` | 66.86% | Chromium-oriented at this date |
| Limited | Grid lanes / masonry | 0% | Not available in stable browsers |

## Recommended Policy

1. Use safe-default features by default.
2. For enhancement features, require `@supports` plus graceful fallback.
3. For limited features, require explicit justification, clear fallback, and easy rollback.

## Primary Sources

- <https://caniuse.com/css-nesting>
- <https://caniuse.com/css-container-queries>
- <https://caniuse.com/css-has>
- <https://caniuse.com/mdn-css_at-rules_property>
- <https://caniuse.com/css-content-visibility>
- <https://caniuse.com/mdn-css_properties_scrollbar-gutter>
- <https://caniuse.com/mdn-css_properties_aspect-ratio>
- <https://caniuse.com/css-logical-props>
- <https://caniuse.com/mdn-css_types_color_color-mix>
- <https://caniuse.com/css-text-wrap-balance>
- <https://caniuse.com/wf-light-dark>
- <https://caniuse.com/mdn-css_at-rules_scope>
- <https://caniuse.com/css-anchor-positioning>
- <https://caniuse.com/wf-scroll-driven-animations>
- <https://caniuse.com/css-container-queries-style>
- <https://caniuse.com/wf-container-scroll-state-queries>
- <https://caniuse.com/css-if>
- <https://caniuse.com/css-grid-lanes>
