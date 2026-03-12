# Version De-Pinning — Master Overview

## Goal

Remove hardcoded framework/language version pins from all skills and AGENTS.MD. Replace with a "latest-aware + web-search verification" model so skills stay evergreen.

## Decisions

1. **Scope**: All 7 versioned skills + AGENTS.MD + governance baselines (9 skills total)
2. **Reference files**: Rename to version-neutral names
3. **Web search model**: Hybrid — keep curated patterns as good defaults, add per-skill web search mandate
4. **Version contract**: Latest-aware, respects project constraints (package.json/lockfiles/pyproject.toml)
5. **Migration content**: Keep but generalize (e.g. "legacy → modern")
6. **Browser support snapshot**: Keep as baseline, add web search verification directive
7. **AGENTS.MD descriptions**: "Technology (latest stable): capabilities" style
8. **AGENTS.MD version table**: New centralized Technology | Version Policy | Primary Tool | Fallback table
9. **Tooling defaults**: bun (or npm) for JS/TS; uv (or pip) for Python
10. **Tool abstraction style**: Name the default with fallback — "bun (or npm)", "uv (or pip)"
11. **Meta-instruction**: Per-skill "Version & Research Policy" section
12. **Single branch**: All changes on one branch
13. **Immutable refs**: PEP numbers, NIST AI RMF 1.0, EU AI Act, DTCG spec URLs stay as-is

## Shared "Version & Research Policy" Template

Every dev-* skill SKILL.md gets this section (replacing old "Version Contract"):

```markdown
## Version & Research Policy

- Target the latest stable release of [Technology].
- Detect the project's actual version from [package.json / pyproject.toml / lockfiles].
- Use web search to verify current best practices, API availability, and migration guidance.
- When the project's installed version is behind latest stable, note the gap and recommend upgrade path.
- Refer to AGENTS.MD for centralized version policy and default tooling.
- Do not hardcode version numbers in generated guidance — keep recommendations evergreen.
```

## Reference File Rename Map

| Skill        | Old Name                          | New Name                                 |
| ------------ | --------------------------------- | ---------------------------------------- |
| dev-vuejs    | `vue-3-5-modern-patterns.md`      | `vue-modern-patterns.md`                 |
| dev-vuejs    | `vue-3-legacy-replacements.md`    | `vue-legacy-to-modern-migration.md`      |
| dev-nuxt     | `nuxt4-vue-patterns.md`           | `nuxt-vue-patterns.md`                   |
| dev-nuxt     | `nuxt3-to-nuxt4-deltas.md`        | `nuxt-legacy-to-modern-migration.md`     |
| dev-ts       | `ts-5-9-3-modern-patterns.md`     | `ts-modern-patterns.md`                  |
| dev-ts       | `ts-5-9-3-legacy-replacements.md` | `ts-legacy-to-modern-migration.md`       |
| dev-tailwind | `tailwind-v4-guardrails.md`       | `tailwind-guardrails.md`                 |
| dev-tailwind | `tailwind-v3-to-v4-deltas.md`     | `tailwind-legacy-to-modern-migration.md` |
| dev-css      | `support-snapshot-2026-02.md`     | `browser-support-baseline.md`            |
| governance   | `stack-baseline-2026-03.md`       | `stack-baseline.md`                      |
| governance   | `repository-baseline-2026-03.md`  | `repository-baseline.md`                 |
| governance   | `evidence-baseline-2026-03.md`    | `evidence-baseline.md`                   |

## Files Unchanged

- `dev-nuxt/references/ecosystem-preferences.md` — name is neutral (content gets version pin removal)
- `dev-nuxt/references/typescript-modern.md` — already neutral
- `dev-css/references/modern-css-source.md` — name is neutral (content gets minor version pin removal)
- `dev-tailwind/references/framework-recipes.md` — name is neutral (content gets version pin removal)
- `dev-python/references/python-standards.md` — name is neutral (content gets version pin removal)
- `code-quality/*` — no changes needed

## Execution Order

1. Create PRD audit docs (this phase)
2. Update AGENTS.MD (version table + description rewrites)
3. dev-vuejs → dev-nuxt → dev-ts → dev-tailwind → dev-python → dev-css → governance → code-quality
4. Cross-cutting verification
