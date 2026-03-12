# Version De-Pinning — dev-tailwind

## SKILL.md Changes

- Frontmatter `description`: "Tailwind CSS v4" → "Tailwind CSS (latest stable)"
- Overview: "hard Tailwind v4-first" → "latest stable Tailwind"
- All "v4"/"v3" references → "modern"/"legacy"
- "Tailwind v4" → "modern Tailwind" / "current stable"
- "v3-era" → "legacy"
- "Load References On Demand": update file paths to new names

## Reference File Renames

- `tailwind-v4-guardrails.md` → `tailwind-guardrails.md`
- `tailwind-v3-to-v4-deltas.md` → `tailwind-legacy-to-modern-migration.md`

## tailwind-guardrails.md Content Changes

- Title: "Tailwind v4 Guardrails" → "Tailwind Guardrails (Latest Stable)"
- All "v4" → "modern" / "current stable"
- All "v3" → "legacy"
- Keep directive names as-is (they're API names, not version pins)
- Add header note: verify against latest Tailwind docs

## tailwind-legacy-to-modern-migration.md Content Changes

- Title: "Tailwind v3 to v4 Deltas" → "Tailwind Legacy-to-Modern Migration"
- "v3 → v4" → "legacy → modern"
- Keep migration matrix content
- Add header note: verify migration paths via web search

## framework-recipes.md Content Changes

- "Tailwind v4" → "modern Tailwind" / "current stable"
- Keep `npx nuxi@latest` (already floating latest)
- Add note to verify latest tool versions
