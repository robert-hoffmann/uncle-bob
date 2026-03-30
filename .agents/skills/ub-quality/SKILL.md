---
name: ub-quality
description: Portable baseline quality skill for creating, modifying, reviewing, and refactoring code or documents. Load and apply the required references. For touched eligible vertical separator blocks, enforce separator-column alignment.
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

## Non-Compliance

The following are non-compliant when a touched block is eligible for alignment:

- An eligible vertical separator block whose separators do not form one column.
- Value-column alignment in an eligible block.
- Leaving embedded CSS/JS blocks unformatted as native language blocks when the touched content is eligible for alignment.
- Skipping alignment because of convenience, omission, or surrounding local style.
- Normalizing unrelated blocks outside the touched logical scope.

## Core Workflow

1. Inspect the task scope and touched files.
2. Load and apply the required references before writing.
3. Propose at least two implementation approaches for non-trivial work, with concise pros and cons.
4. Choose the simplest approach that preserves behavior and constraints.
5. Apply formatting, documentation, and structure rules only in touched logical blocks.
6. Validate behavior and explain any intentional exceptions allowed by the required references.

## Skill Coordination

- Apply this skill together with the most relevant language/framework skill when available.
- Treat syntax, runtime, and framework correctness as primary constraints.
- Do not treat formatter preference or familiar house style as a valid reason to violate the alignment contract.

## Output Requirements

When generating or modifying code:

1. Include short pros/cons for major implementation choices.
2. Keep solutions simple and avoid overengineering.
3. Preserve existing behavior unless change is explicitly requested.
4. Call out any intentionally retained technical debt or deferred cleanup.

## Completion Gate

Before finalizing:

- Check every touched eligible separator block.
- Treat touched `<style>` and `<script>` content as native CSS and JavaScript surfaces.
- Expand dense multiline-capable structures (for example literals, argument lists, and config/data blocks) into one-item-per-line form when required by `references/formatting-alignment.md`, then align eligible entries.
- Align separators into one column using the longest-left-token rule from `references/formatting-alignment.md`.
- Confirm no unrelated blocks were normalized.
- If any eligible block remains unaligned, the edit is incomplete unless a named exception from `references/formatting-alignment.md` applies.
- Ensure special comment tags and `AGENT_TODO` handling policy are respected.
