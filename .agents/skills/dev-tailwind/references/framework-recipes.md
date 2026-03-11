# Framework Recipes

Use this document to choose the correct Tailwind v4 setup path for the target runtime.

## 1) Standalone HTML (CDN)

Use this path for plain HTML files without a build pipeline.

### Pattern

- Load Tailwind using the current CDN script pattern.
- Keep customization minimal and page-local.
- Avoid build-plugin instructions in this mode.

### Use When

- The user asks for a quick prototype.
- The project has no `package.json`, Vite, or Nuxt markers.

### Guardrails

- Do not inject Vite/Nuxt setup steps into CDN-only projects.
- Keep examples simple and avoid migration-heavy build guidance.

## 2) Vue + Vite

Use this path for Vue projects using Vite bundling.

### Pattern

- Add the Tailwind v4 Vite plugin (`@tailwindcss/vite`).
- Register the plugin in the Vite config plugin list.
- Create or update a main stylesheet with `@import "tailwindcss"`.
- Import that stylesheet from the app entry point.
- Keep design tokens in `@theme` for maintainability.

### Component-Scoped Styles

If a Vue SFC style block uses `@apply` or `@variant`, add `@reference` to the main stylesheet context.

### Guardrails

- Do not add PostCSS as a default requirement.
- Do not introduce legacy `@config` or `@plugin` unless compatibility is explicitly required.

## 3) Nuxt

Use this path for Nuxt applications.

### Pattern

Use this exact official sequence for modern Nuxt setup:

1. Install Tailwind module via Nuxt tooling:

```bash
npx nuxi@latest module add tailwindcss
```

2. Wire the Tailwind Vite plugin in `nuxt.config.ts`:

```ts
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  css: ["~/assets/css/main.css"],
  vite: {
    plugins: [tailwindcss()],
  },
});
```

3. Create `app/assets/css/main.css` with:

```css
@import "tailwindcss";
```

4. Keep token and utility extensions in CSS-first v4 style (`@theme`, `@utility`, `@variant`, `@custom-variant`).

### Known Differences vs Vue + Vite

- Nuxt wiring belongs in `nuxt.config.*`, not a standalone Vue `vite.config.*` file.
- Global CSS registration is done through Nuxt `css` config.
- Nuxt apps should use app-source stylesheet placement (`app/assets/css/main.css`) with `~/assets/css/main.css` registration.

### Guardrails

- Do not scaffold Vue-only `vite.config.*` plugin wiring for Nuxt projects.
- Do not present `@nuxtjs/tailwindcss` as the default path for new Tailwind v4 Nuxt setup.
- Do not mix Nuxt and Vue+Vite setup instructions in the same recipe unless compatibility constraints are explicitly requested.

## Quick Environment Detection

Use this order before writing setup instructions:

1. Check project markers (`nuxt.config.*`, `vite.config.*`, `package.json`).
2. Check existing CSS entrypoints and how global styles are loaded.
3. Confirm whether the user wants quick prototype mode (CDN) or production app wiring.
4. For Nuxt, confirm stylesheet placement and registration pair (`app/assets/css/main.css` + `~/assets/css/main.css`).

If signals conflict, ask for clarification instead of merging incompatible setup paths.
