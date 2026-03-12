# Version De-Pinning — dev-nuxt

## SKILL.md Changes

- Frontmatter `description`: "Nuxt 4" → "Nuxt (latest stable)"
- Overview: "hard Nuxt 4-only" → "latest stable Nuxt"
- "Nuxt 4 Structure Contract" → "Nuxt Modern Structure Contract"
- "Nuxt 4" references → "modern Nuxt" / "current stable Nuxt"
- "v3-era" → "legacy"
- `future.compatibilityVersion` references: keep as detection signal, remove version-specific values
- "Load References On Demand": update file paths to new names

## Reference File Renames

- `nuxt4-vue-patterns.md` → `nuxt-vue-patterns.md`
- `nuxt3-to-nuxt4-deltas.md` → `nuxt-legacy-to-modern-migration.md`

## nuxt-vue-patterns.md Content Changes

- Title: "Nuxt 4 + Vue Patterns" → "Nuxt + Vue Patterns (Latest Stable)"
- All "Nuxt 4" → "modern Nuxt" / "current stable"
- Keep `app/` directory rules but frame as current conventions
- Add header note: verify against latest official Nuxt docs

## nuxt-legacy-to-modern-migration.md Content Changes

- Title: "Nuxt 3 to Nuxt 4 Deltas" → "Nuxt Legacy-to-Modern Migration"
- "v3 → v4" table headers → "legacy → modern"
- Keep codemod commands, note to verify latest versions
- Add header note: verify migration paths via web search

## ecosystem-preferences.md Content Changes

- Remove "Tailwind v4" → "Tailwind (latest stable)"
- Remove "Nuxt 4" → "modern Nuxt"
- Keep content otherwise neutral

## typescript-modern.md — No Changes

Already version-neutral.
