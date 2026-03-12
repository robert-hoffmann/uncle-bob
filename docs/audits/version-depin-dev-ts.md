# Version De-Pinning — dev-ts

## SKILL.md Changes

- Frontmatter `description`: "TypeScript 5.9.3" → "TypeScript (latest stable)"
- Overview: "TypeScript 5.9.3 modern defaults" → "TypeScript modern defaults for the latest stable release"
- Replace "Version Contract" section with "Version & Research Policy"
- Remove "5.9.3" from all prose
- "TypeScript 6.x" → "pre-release/beta"
- "Load References On Demand": update file paths to new names

## Reference File Renames

- `ts-5-9-3-modern-patterns.md` → `ts-modern-patterns.md`
- `ts-5-9-3-legacy-replacements.md` → `ts-legacy-to-modern-migration.md`

## ts-modern-patterns.md Content Changes

- Title: "TypeScript 5.9.3 Modern Patterns" → "TypeScript Modern Patterns (Latest Stable)"
- "TypeScript 5.9.3" → "latest stable TypeScript" throughout
- "5.9" → "current stable" where used generically
- Keep archetype matrix and tsconfig templates (they're config patterns, not version pins)
- Keep ES target pins (es2023, es2022, esnext) — archetype-appropriate
- Keep release note URLs as historical reference but note to check latest
- Add header note: verify patterns against latest TS docs via web search

## ts-legacy-to-modern-migration.md Content Changes

- Title: "TypeScript 5.9.3 Legacy Replacements" → "TypeScript Legacy-to-Modern Migration"
- "5.9.3" → "latest stable TypeScript"
- Keep migration patterns as-is (they're pattern-based, not version-specific)
- Add header note: verify migration paths via web search
