# Custom Instructions Reference

## When to Use Instructions

Use custom instructions when the guidance should be **always-on** — loaded into every chat without user action. Instructions are for team conventions, architecture rules, coding standards, and review expectations.

Do NOT use instructions for:

- User-invoked tasks → use prompt files
- Multi-step reusable workflows → use skills
- Role-specific personas with tool restrictions → use custom agents
- Deterministic lifecycle automation → use hooks

## Three Instruction Types

### 1. Repo-Wide Instructions (`copilot-instructions.md`)

**Location**: `.github/copilot-instructions.md`

Automatically loaded in every Copilot chat for the workspace. Use for broad conventions that apply everywhere.

```markdown
# .github/copilot-instructions.md

## Project conventions
- Use pnpm for package management.
- Use TypeScript strict mode.
- Run `pnpm test` after non-trivial changes.

## Architecture notes
- API routes live in `src/api`.
- Shared UI primitives live in `src/components/ui`.

## Review expectations
- Prefer minimal diffs.
- Add tests for behavior changes.
```

**Rules:**

- Keep concise — only non-obvious, project-specific, human-important rules.
- Prefer examples over vague declarations.
- Do not duplicate what linters or formatters already enforce.
- Do not turn this into a policy encyclopedia.

### 2. Scoped Instructions (`.instructions.md`)

**Location**: `.github/instructions/*.instructions.md` or alongside code

Use `applyTo` frontmatter to limit scope to specific files, folders, or languages.

```markdown
---
applyTo: "src/**/*.ts,src/**/*.tsx"
---

# TypeScript and React instructions
- Prefer functional components and hooks.
- Keep components small and focused.
- Use existing design-system primitives before adding new UI patterns.
```

**Rules:**

- Use when different stacks coexist and need different rules.
- The `applyTo` field accepts glob patterns — matches against workspace-relative file paths.
- Multiple globs can be comma-separated.
- Prefer scoped instructions over one giant file when rules differ by file type.

### 3. Portable Guidance Files

**`AGENTS.md`** — placed at repo root or in subdirectories. Read by multiple agent ecosystems (VS Code, Codex, Copilot CLI). Use when cross-agent portability matters.

**`CLAUDE.md`** — VS Code can read this file. Useful in teams that also use Claude Code. Do not assume equivalent support for other vendor files.

**`GEMINI.md`**, **`CODEX.md`** — other vendor-specific guidance files. VS Code does not read these natively. Generate only when cross-vendor export is requested.

**Layered overrides**: `AGENTS.md` files in subdirectories override or extend the root file for that subtree. Keep guidance close to the code it governs.

## File Location Summary

| File | Location | Scope | Auto-loaded |
| --- | --- | --- | --- |
| `copilot-instructions.md` | `.github/` | Repo-wide | Yes |
| `*.instructions.md` | `.github/instructions/` or alongside code | File-pattern scoped | When `applyTo` matches |
| `AGENTS.md` | Repo root or subdirectories | Repo-wide or subtree | Yes (by compatible agents) |
| `CLAUDE.md` | Repo root | Repo-wide | Yes (VS Code reads it) |

## Content Guidelines

- Write in **imperative** form: "Use X", "Prefer Y", not "You should use X".
- Focus on **non-obvious rules** — skip rules that any competent developer or linter already knows.
- Show **desired and avoided patterns** with short code examples.
- Include **examples where ambiguity is likely**.
- Keep instruction files **concise** — they load into every chat and consume context.
- One rule per bullet or short section — avoid walls of text.

## Generation Checklist

- [ ] Correct file location (`.github/` for repo-wide, `.github/instructions/` for scoped)
- [ ] Valid `applyTo` glob pattern (if scoped)
- [ ] Concise — no policy encyclopedia
- [ ] Non-obvious rules only — no linter duplication
- [ ] Examples included where ambiguity is likely
- [ ] Imperative phrasing
- [ ] No hardcoded secrets or sensitive data
