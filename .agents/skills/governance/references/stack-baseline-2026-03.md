# Stack Baseline 2026-03

Last verified: **2026-03-04 (US)**

This baseline defines lean testing defaults and acceptable alternatives.

## 1) Lean Default Matrix

| Area | Default | Alternatives | Pros | Cons |
| ---- | ------- | ------------ | ---- | ---- |
| TS/Vite/Vue unit tests | Vitest + Vue Test Utils/Testing Library | Jest | Vite-native speed and TS ergonomics | migration cost from legacy stacks |
| Nuxt tests | `@nuxt/test-utils` + Vitest projects | Playwright-heavy integration only | Nuxt-aware runtime behavior coverage | fixture discipline required |
| Web E2E | Playwright Test | Cypress, WebdriverIO | cross-browser coverage + traces | setup overhead |
| Node backend tests | Vitest (TS-first) | `node:test` (lean JS) | unified tooling in TS repos | fewer ergonomics in bare runner |
| Python backend tests | pytest + pytest-xdist | unittest (legacy) | mature ecosystem | fixture hygiene required |

## 2) Governance Defaults

1. keep layers explicit: unit, integration, contract, e2e
2. keep e2e compact/high-value
3. treat retries as flake diagnostics, not correctness proof
4. prioritize deterministic commands and artifacts

## 3) Sources

- <https://nuxt.com/docs/4.x/getting-started/testing>
- <https://vitest.dev/guide/>
- <https://playwright.dev/docs/best-practices>
- <https://nodejs.org/api/test.html>
- <https://docs.pytest.org/en/stable/>
- <https://pytest-xdist.readthedocs.io/en/stable/>
