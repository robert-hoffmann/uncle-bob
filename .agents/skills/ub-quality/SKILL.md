---
name: ub-quality
description: Portable baseline quality skill for creating, modifying, reviewing, and refactoring code or documents. Load and apply the required references. Favor high-signal documentation that reduces cognitive load for future readers, including tool-assisted agents. For touched eligible vertical separator blocks, enforce separator-column alignment.
---

# UB Quality

## Critical Contract

Before generating or modifying any code or document, load and apply the required references in this skill.

For every touched eligible vertical separator block, separators must align into one column. Use separator-column alignment (`key : value`), not value-column alignment (`key: value`).

This applies across code, configs, comments, docstrings, markup attributes, and documentation blocks when the structure is eligible.

Treat embedded language blocks such as `<style>` and `<script>` as native CSS and JavaScript formatting surfaces, not as generic HTML text.

Only syntax breakage or a verified tooling or runtime constraint may justify leaving an eligible touched block unaligned.

Compliant:

```text
grid      : ''
solar     : ''
textMuted : ''
```

Non-compliant:

```text
grid:      ''
solar:     ''
textMuted: ''
```

## When To Use

Use this skill for:

- New code generation
- Code edits and refactors
- Code review responses
- Documentation, config, comment, and formatting normalization in touched regions

Apply this skill whenever you create, modify, review, refactor, or normalize code or documents.

## Do Not Treat As Optional

- Do not treat formatting and alignment as optional cleanup.
- If this skill is loaded, its formatting and alignment rules apply to all touched eligible blocks.
- Do not skip alignment because nearby code is unaligned, because a shorter style looks more familiar, or because the block is in documentation rather than code.
- Do not normalize unrelated blocks outside the touched logical scope unless broader normalization was explicitly requested.

## Required References

- Load and apply `references/design-patterns.md` for architecture and implementation principles.
- Load and apply `references/formatting-alignment.md` for mandatory alignment rules and guardrails.
- Load and apply `references/documentation-structure-refactoring.md` for documentation standards, file structure, and refactoring workflow.
- Load and apply `references/important-tags-and-doc-generation.md` for mandatory comment-tag preservation and document-generation policy.
- Load and apply `references/response-readability.md` for user-facing response structure, comparison formatting, and narrow-pane readability guidance.
- Read `references/freshness-portability.md` when deciding whether a quality rule is repository policy, a strong house default, or an advisory freshness concern.

## Non-Compliance

The following are non-compliant when a touched block is eligible for alignment:

- An eligible vertical separator block whose separators do not form one column.
- Value-column alignment in an eligible block.
- Leaving embedded CSS/JS blocks unformatted as native language blocks when the touched content is eligible for alignment.
- Skipping alignment because of convenience, omission, or surrounding local style.
- Normalizing unrelated blocks outside the touched logical scope.

## Decision Analysis Baseline

For planning, design, architecture, implementation direction, and other
choice-bearing guidance:

- Surface `2+` plausible approaches by default.
- Prefer a curated set of `2-4` options instead of exhaustive enumeration.
- Include concise pros/cons for each option and identify the recommended path.
- If only one path is materially meaningful, say that explicitly and explain
  why the alternatives are not meaningfully different instead of fabricating a
  fake option set.
- Leave sibling skills free to add domain-specific tradeoff dimensions when
  they add real value.

## Readability Baseline

For user-facing responses across chat, planning, reviews, specs, and
explanations:

- Lead with the answer, recommendation, or key point.
- Use informative headings for substantial responses.
- Keep paragraphs short and visually separated.
- Use bullets for collections and numbered steps for sequence.
- Keep list items parallel in grammar and intent.
- Use tables only for true multi-attribute comparisons that stay compact.
- Avoid dense text blocks when structure would improve scanning.
- Keep short answers compact and avoid ceremonial formatting.

Table rule:

- Prefer compact tables only when they materially improve side-by-side
  comparison.
- Usually keep tables to `2-4` columns with short headers and brief cells.
- Do not force sentence-length prose into table cells.
- When a table becomes too wide, dense, or renderer-fragile, convert it to a
  safer fallback structure instead of trying to preserve the grid.

## Core Workflow

1. Inspect the task scope and touched files.
2. Load and apply the required references before writing.
3. Apply the decision-analysis baseline for planning, design, architecture,
   implementation direction, and other choice-bearing guidance.
4. Apply the readability baseline for user-facing responses and choose tables
   versus safer fallback structures accordingly.
5. Choose the simplest approach that preserves behavior and constraints.
6. Apply formatting, documentation, and structure rules only in touched logical blocks.
7. Validate behavior and explain any intentional exceptions allowed by the required references.

## Skill Coordination

- Apply this skill together with the most relevant language/framework skill when available.
- Treat syntax, runtime, and framework correctness as primary constraints.
- Do not treat formatter preference or familiar house style as a valid reason to violate the alignment contract.
- Prefer code and naming to carry mechanics, then use docs and comments for
  contract, rationale, and non-obvious constraints.

## Policy Versus Defaults

- In this repository, the alignment contract and required-reference workflow are repository policy when `ub-quality` is loaded.
- Many language/framework recommendations coordinated through sibling skills are strong defaults, not universal portability requirements.
- Treat volatile setup recipes as freshness-review candidates first, not as automatic blockers, unless the repository explicitly promotes them to policy.

## Output Requirements

When generating or modifying code:

1. Include concise pros/cons and a recommendation for meaningful implementation
   choices.
2. Keep solutions simple and avoid overengineering.
3. Preserve existing behavior unless change is explicitly requested.
4. Call out any intentionally retained technical debt or deferred cleanup.
5. Favor high-signal documentation over broad narration, especially in shared
   guidance and heavily reused code.
6. Make user-facing explanations easy to scan before deep reading.
7. Match the structure to the information shape instead of defaulting to dense
   prose or oversized tables.

## Completion Gate

Before finalizing:

- Check every touched eligible separator block.
- Treat touched `<style>` and `<script>` content as native CSS and JavaScript surfaces.
- Expand dense multiline-capable structures (for example literals, argument lists, and config/data blocks) into one-item-per-line form when required by `references/formatting-alignment.md`, then align eligible entries.
- Align separators into one column using the longest-left-token rule from `references/formatting-alignment.md`.
- Confirm no unrelated blocks were normalized.
- If any eligible block remains unaligned, the edit is incomplete unless a named exception from `references/formatting-alignment.md` applies.
- Ensure special comment tags and `AGENT_TODO` handling policy are respected.
- Expose the answer or recommendation early in user-facing responses.
- Use headings, bullets, steps, tables, or fallback blocks only when they
  improve scanability for the information shape.
- Confirm list items stay parallel and concise.
- Confirm any table adds clarity rather than width or density problems.
- If a comparison table became too wide or text-heavy, convert it to a stacked
  fallback structure instead of forcing the grid.
- Keep brief answers brief.
