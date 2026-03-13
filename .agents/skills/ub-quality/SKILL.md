---
name: ub-quality
description: Enforce cross-language code quality standards for design patterns, formatting/alignment, documentation, code structure, and refactoring. Use when creating, editing, reviewing, or refactoring code so output stays readable, maintainable, and consistently documented.
---

# UB Quality

## Overview

Use this skill as the baseline quality policy for code work in this repository.

This skill is cross-language and complements language/framework-specific skills.

## When To Use

Use this skill for:

- New code generation
- Code edits and refactors
- Code review responses
- Documentation and formatting normalization in touched regions

## Mandatory references to use/apply

- Read `references/design-patterns.md` for architecture and implementation principles.
- Read `references/formatting-alignment.md` for alignment policy and formatting guardrails.
- Read `references/documentation-structure-refactoring.md` for documentation standards, file structure, and refactoring workflow.
- Read `references/important-tags-and-doc-generation.md` for mandatory comment-tag preservation and document-generation policy.

## Core Workflow

1. Inspect the task scope and touched files.
2. Propose at least two implementation approaches for non-trivial work, with concise pros and cons.
3. Choose the simplest approach that preserves behavior and constraints.
4. Apply formatting, documentation, and structure rules only in touched logical blocks.
5. Validate behavior and explain any intentional exceptions.
6. In vertical separator blocks, enforce separator-column alignment (`key : value`) rather than value-column alignment (`key: value`).

## Skill Coordination

- Apply this skill together with the most relevant language/framework skill when available.
- Treat syntax, runtime, and framework correctness as primary constraints.
- Apply ub-quality formatting and documentation rules where they do not conflict with toolchain or framework requirements.

## Output Requirements

When generating or modifying code:

1. Include short pros/cons for major implementation choices.
2. Keep solutions simple and avoid overengineering.
3. Preserve existing behavior unless change is explicitly requested.
4. Call out any intentionally retained technical debt or deferred cleanup.

## Completion Checklist

- Design stays simple (KISS/DRY/YAGNI/SRP/SOC).
- Touched blocks follow alignment and readability guardrails.
- Colon-separated vertical blocks keep separators in one column (`key : value`).
- Non-obvious logic is documented with concise "why" comments.
- File structure remains coherent and predictable.
- Refactoring preserves behavior and improves clarity.
- Special comment tags and `AGENT_TODO` handling policy are respected.
