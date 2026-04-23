---
name: ub-authoring
description: >-
  Use this skill when the task involves creating, reviewing, or refactoring
  installable skills, shared skill references, or reusable agent-authoring
  guidance; when the work depends on routing-quality descriptions, non-use
  boundaries, naming, progressive disclosure, or cross-skill authoring
  conventions; or when you want to normalize skill and guidance structure
  without turning the task into a full customization-builder workflow. Do not
  use it for end-to-end customization generation, normal code implementation,
  or general repository planning.
argument-hint: "[authoring surface] [goal]"
user-invocable: true
disable-model-invocation: false
---

# UB Authoring

## Mission

Use this skill to shape portable, installable authoring guidance for skills and
related agent-behavior surfaces.

This skill owns the reusable authoring conventions that should travel with the
skill catalog itself instead of living in repo-only docs or in one
customization-specific skill.

## When Not To Use

- Do not use this skill for end-to-end customization generation; defer that to
  `ub-customizations`.
- Do not use this skill for ordinary code implementation or framework work
  where no shared authoring contract is being changed.
- Do not use this skill as a substitute for repo-local maintenance docs or
  packaging metadata that belong to a development repository rather than the
  distributable skill payload.

## Embedded Contract

These rules are the base contract of this skill and must not depend on a
secondary document to be applied correctly.

1. Treat descriptions as routing metadata, not marketing copy.
2. Add explicit non-use boundaries when wrong-skill activation is realistically
   costly or common.
3. Prefer concrete examples and acceptance boundaries over vague admonitions.
4. Keep the main skill surface lean and move deeper detail into targeted
   references.
5. Keep shared authoring guidance portable across installed skill payloads and
   avoid repo-local live truth in the reusable contract.
6. Keep reusable choice-question UX contracts in shared authoring guidance
   instead of re-encoding the same multiple-choice rules in each skill.

## Load References On Demand

- Read `references/authoring-conventions.md` when shaping shared skill
  structure, cross-skill wording, routing quality, reusable choice-question
  UX, or other reusable authoring patterns.

## Core Workflow

1. Decide whether the task is changing a reusable authoring convention or a
   single skill's local content.
2. Keep portable shared guidance in this skill and domain-specific guidance in
   the owning skill.
3. Normalize descriptions, examples, non-use boundaries, and shared
   choice-question behavior only where the changed surfaces actually benefit
   from them.
4. Keep reusable references installable and avoid dead links into repo-only
   docs.

## Output Requirements

When producing non-trivial authoring updates, include:

1. `routing_note`
2. `boundary_note`
3. `reference_note`
4. `validation_note`

## Completion Checklist

- Shared guidance remains portable inside `.agents/skills/`.
- Description wording reads like routing logic, not inventory prose.
- Non-use boundaries are explicit where misrouting is realistic.
- Examples are concrete where abstract guidance would be easy to misapply.
- Shared references avoid repo-only assumptions unless clearly labeled as such.
