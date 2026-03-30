# Agent Skills Reference

Use this reference to write skills that trigger reliably, stay lean in context, and communicate clear activation boundaries.

## When to Use Skills

Use a skill when the workflow is **reusable, multi-step, and benefits from bundled resources** (scripts, references, assets). Skills are the right choice for on-demand domain workflows that need more than a simple prompt file can provide.

Do NOT use skills for:

- Always-on guidance → use instructions
- Simple one-step user-invoked tasks → use prompt files
- Role-specific personas with tool restrictions → use custom agents
- Deterministic automation → use hooks

## Skill Anatomy

Every skill is a directory containing a required `SKILL.md` and optional resources:

```text
skill-name/
├── SKILL.md            (required — frontmatter + instructions)
├── scripts/            (optional — executable code for deterministic tasks)
├── references/         (optional — docs loaded on-demand into context)
└── assets/             (optional — files used in output, not loaded into context)
```

### Locations

VS Code searches these paths for skills:

- `.github/skills/<name>/SKILL.md`
- `.agents/skills/<name>/SKILL.md`
- `.claude/skills/<name>/SKILL.md`
- User profile skills folder

This repo uses `.agents/skills/` by convention.

### Open Standard

Skills follow the Agent Skills open standard (agentskills.io). They work across VS Code, Copilot CLI, and Copilot coding agent.

## Frontmatter Fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Skill name. Lowercase, hyphens, verb-led, under 64 characters. |
| `description` | Yes | **Primary triggering mechanism.** Treat it as routing logic: state what the skill does, when to use it, adjacent phrasings the user may use, and when not to use it. |
| `argument-hint` | No | Placeholder text shown when invoked explicitly. |
| `user-invocable` | No | Set `true` to allow explicit invocation as a slash command. |
| `disable-model-invocation` | No | Set `true` to prevent auto-activation — only user invocation works. |

## Description-Writing Formula

The description is the most critical field. It controls whether the skill activates at all, so write it like routing logic, not like marketing copy or an internal implementation note.

Follow this pattern:

> Use this skill when the user wants **X**, **Y**, or **Z**; when the task involves **A/B/C**; or when they ask for related outcomes even if they do not use exact terminology. Do not use it for simple one-step cases that built-in tools handle directly.

**Rules:**

- Put the highest-signal **user intents first**.
- Focus on **what the user is trying to achieve**, not internal implementation details.
- Include **trigger keywords, adjacent phrasings, and neighboring task language** the user might use.
- State both **what it does** and **when to use it**.
- Include at least one **clear non-use boundary** so the skill does not over-trigger.
- Keep it short enough to avoid context bloat, but specific enough to route reliably (usually 2-4 sentences).

### Weak vs Strong Descriptions

Weak:

> Helps with BigQuery workflows and reusable resources.

Why it fails:

- It describes the implementation vaguely instead of the user intent.
- It has no trigger phrases, adjacent phrasings, or exclusion boundary.
- It gives the model almost no signal for when to activate the skill.

Strong:

> Use this skill when the user wants to create, review, debug, migrate, or explain BigQuery queries, datasets, schemas, jobs, or warehouse workflows; when the task involves BigQuery SQL, permissions, costs, or query optimization; or when they ask for related analytics outcomes even without saying BigQuery explicitly. Do not use it for generic SQL tasks that do not touch BigQuery.

### Description Failure Modes to Avoid

- Descriptions that say only what the skill contains, not when to use it.
- Descriptions that rely on internal terms the user is unlikely to say.
- Descriptions with no exclusion boundary.
- Descriptions that are so broad they compete with built-in tools or unrelated skills.
- Descriptions that are so narrow they miss common adjacent phrasings.

## Progressive Disclosure

Skills use three-level loading to manage context efficiently:

1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — loaded when skill triggers (target < 500 lines)
3. **Bundled resources** — loaded on-demand as needed (unlimited)

### Pattern 1: High-Level Guide with References

```markdown
# PDF Processing

## Quick start
Extract text with pdfplumber:
[code example]

## Advanced features
- **Form filling**: See [references/forms.md](references/forms.md)
- **API reference**: See [references/api.md](references/api.md)
```

### Pattern 2: Domain-Specific Organization

```text
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

When a user asks about sales metrics, only `sales.md` is loaded.

### Pattern 3: Conditional Details

```markdown
# DOCX Processing

## Creating documents
Use docx-js for new documents. See [references/docx-js.md](references/docx-js.md).

## Editing documents
For simple edits, modify the XML directly.
**For tracked changes**: See [references/redlining.md](references/redlining.md)
```

**Key guidelines:**

- Keep references **one level deep** from SKILL.md — no nested references.
- For files longer than 100 lines, include a **table of contents** at the top.
- Move variant-specific details to separate reference files; keep only core workflow in SKILL.md.
- Avoid duplication between SKILL.md and reference files.

## Naming Conventions

- Lowercase letters, digits, and hyphens only.
- Normalize user titles to hyphen-case: "Plan Mode" → `plan-mode`.
- Under 64 characters.
- Prefer short, **verb-led phrases** that describe the action.
- Namespace by tool when it improves clarity: `gh-address-comments`, `linear-address-issue`.
- Name the skill folder exactly after the skill name.

## Bundled Resources

### Scripts (`scripts/`)

Executable code for tasks requiring **deterministic reliability** or frequently rewritten logic.

- Include when the same code gets rewritten repeatedly.
- Example: `scripts/rotate_pdf.py` for PDF rotation.
- Scripts may be executed without loading into context — token efficient.
- Test scripts by running them before shipping.

### References (`references/`)

Documentation loaded on-demand into context.

- Include for detailed specs, schemas, API docs, domain knowledge.
- Keep SKILL.md lean — move heavy detail here.
- If files are large (>10k words), include grep patterns in SKILL.md.

### Assets (`assets/`)

Files used in output, NOT loaded into context.

- Templates, images, icons, boilerplate code, fonts.
- Separates output resources from documentation.

## What NOT to Include

Do not create auxiliary files that add clutter:

- No `README.md`, `INSTALLATION_GUIDE.md`, `QUICK_REFERENCE.md`, `CHANGELOG.md`.
- Only files directly needed by the agent to do the job.

## Template

```markdown
---
name: playwright-testing
description: >-
  Use this skill when the user wants to create, run, debug, review, or
  organize browser-based tests with Playwright; when the task involves
  selectors, fixtures, tracing, retries, or cross-browser behavior; or when
  they ask for related end-to-end browser automation outcomes even without
  naming Playwright directly. Do not use it for simple unit tests or generic
  front-end debugging that does not involve Playwright.
argument-hint: "[target page or test goal]"
user-invocable: true
disable-model-invocation: false
---

# Playwright Testing

## When to use
Use this skill for browser-based testing tasks, not for simple unit tests.

## Workflow
1. Inspect existing Playwright config and test patterns.
2. Reuse local templates/examples before creating new structure.
3. Create or update tests.
4. Run tests and collect failures.
5. Suggest fixes and rerun.

## References
- See [references/config-patterns.md](references/config-patterns.md)
- See [references/selectors.md](references/selectors.md)
```

## Generation Checklist

- [ ] Skill directory at correct location (`.agents/skills/<name>/`)
- [ ] SKILL.md has valid frontmatter: `name` and `description`
- [ ] Description is trigger-optimized (what + when + adjacent phrasings + non-use boundary)
- [ ] SKILL.md body is under 500 lines
- [ ] References are one level deep and clearly linked from SKILL.md
- [ ] No auxiliary documentation files (README, CHANGELOG, etc.)
- [ ] Naming: lowercase, hyphens, verb-led, under 64 chars
- [ ] Scripts tested if included
- [ ] No hardcoded secrets or sensitive data
