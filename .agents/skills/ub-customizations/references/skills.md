# Agent Skills Reference

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
| `description` | Yes | **Primary triggering mechanism.** Must include what the skill does AND when to use it. |
| `argument-hint` | No | Placeholder text shown when invoked explicitly. |
| `user-invocable` | No | Set `true` to allow explicit invocation as a slash command. |
| `disable-model-invocation` | No | Set `true` to prevent auto-activation — only user invocation works. |

## Description-Writing Formula

The description is the most critical field — it controls when the skill activates. Follow this pattern:

> Use this skill when the user wants **X**, **Y**, or **Z**; when the task involves **A/B/C**; or when they ask for related outcomes even if they do not use exact terminology. Do not use it for simple one-step cases that built-in tools handle directly.

**Rules:**

- Use **imperative phrasing**.
- Focus on **user intent**, not internal implementation.
- Include **trigger keywords and adjacent phrasings** the user might say.
- Mention both **what it does** and **when to use it**.
- Keep short enough to avoid context bloat (~2-4 sentences).

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
  Use this skill when the user wants to create, run, debug, or organize
  browser-based tests with Playwright, especially when reusable templates,
  workflows, or troubleshooting steps are helpful.
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
- [ ] Description is trigger-optimized (what + when + keywords)
- [ ] SKILL.md body is under 500 lines
- [ ] References are one level deep and clearly linked from SKILL.md
- [ ] No auxiliary documentation files (README, CHANGELOG, etc.)
- [ ] Naming: lowercase, hyphens, verb-led, under 64 chars
- [ ] Scripts tested if included
- [ ] No hardcoded secrets or sensitive data
