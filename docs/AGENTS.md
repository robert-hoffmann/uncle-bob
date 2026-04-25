# Public Documentation Instructions

## Scope

These instructions apply to files under `docs/`.

The public VitePress site explains how the portable Uncle Bob skills work after
installation. It is not the place for factory-repository maintenance details.

## Source Truth

Use the real skill files as the operational source of truth:

1. `.agents/skills/<skill>/SKILL.md` defines routing, activation, boundaries,
   workflow, output expectations, and completion behavior.
2. `.agents/skills/<skill>/references/` contains deeper rules, examples,
   patterns, migration guidance, and validation policy.
3. `docs/` explains those contracts for humans. It must summarize and teach,
   not copy skill files verbatim.

When editing public docs, verify claims against the current skill and reference
files before presenting them as behavior.

## Public Site Focus

Keep public docs centered on installed skill usage:

1. what each skill is for
2. when to invoke it
3. what it changes in agent behavior
4. the principles and tradeoffs behind the skill
5. examples of practical invocation
6. boundaries and non-use cases
7. how skills interact with each other

Do not turn the public site into a guide for repository maintenance, local CI,
release mechanics, packaging internals, or factory-only scripts. Those belong
in repository-control surfaces such as `AGENTS.md`, `README.md`, and targeted
maintenance notes outside the public site.

## Skill Page Contract

Every `docs/skills/<skill>.md` page must include these sections:

1. `## Core Principles`
2. `## Behavior In Practice`
3. `## Reference Highlights`
4. `## Progressive Disclosure`
5. `## Common Invocation Examples`
6. `## Boundaries`
7. `## Tradeoffs`

The important section is `Behavior In Practice`. It should surface the useful
ideas hidden in references so readers understand what the skill actually does.
Do not stop at listing reference paths.

Good examples:

1. `ub-quality` should explain KISS, DRY, YAGNI, scope discipline,
   readability, alignment, documentation quality, freshness, and portability.
2. `ub-python` should explain modern Python typing, boundary validation,
   dataclasses, Pydantic v2, structured errors, repository-tooling detection,
   validation, and legacy avoidance.
3. `ub-governance` should explain lean versus advanced mode, ADR escalation,
   evidence, claim checks, TDD red/green/refactor, Prove-It regression flow,
   DAMP test readability, RED realism, and low-signal test detection.
4. Framework specialists should explain modern defaults, migration boundaries,
   official-source freshness posture, and what the skill rejects.

## Reference Highlights

Reference highlights should do two jobs:

1. name the important source reference paths
2. explain the practical behavior those references contain

Do not document every reference equally. Prioritize the references that explain
the skill's most distinctive behavior, risk model, migration policy, or usage
pattern.

## Progressive Disclosure

Progressive disclosure is part of the product story.

Explain that `SKILL.md` stays compact while deeper references, assets, and
scripts are loaded only when the task triggers them. This should help readers
understand why the system can be lightweight for small tasks and still deep for
complex work.

## Deep Dives

Use deep dives for skills whose behavior is too important or multi-stage for a
single skill page.

Current required deep dives:

1. `docs/deep-dives/ub-workflow.md`
2. `docs/deep-dives/ub-governance.md`
3. `docs/deep-dives/workflow-governance.md`

Deep dives should explain models, decisions, lifecycle, and tradeoffs. They may
use Mermaid diagrams where a diagram makes behavior easier to understand.
Avoid diagrams that only decorate a page without clarifying workflow.

## Tone And Audience

Write for developers and managers evaluating or using the installed skills.

Use direct, concrete language:

1. prefer "the skill checks..." over "the skill may help with..."
2. explain why an opinion exists, not only that it exists
3. name tradeoffs honestly
4. avoid marketing filler
5. avoid raw contract duplication
6. keep examples practical and invocation-oriented

The docs should show that Uncle Bob is modern and opinionated without sounding
like an advertisement.

## Mermaid Diagrams

Use Mermaid diagrams for workflow, routing, lifecycle, gate, or mode behavior.

When writing diagrams:

1. quote node labels that contain punctuation or long phrases
2. keep diagrams small enough to scan
3. prefer one clear decision model over one giant diagram
4. validate with `npm run docs:build`

## Synchronization Rules

When a skill or reference changes, update affected public docs in the same
change or explicitly state why no docs update is needed.

When docs change, check the described behavior against the actual skill and
reference files. If a new convention can be enforced deterministically, update
`scripts/check-docs-sync.mjs`.

For docs changes, run the smallest relevant validation:

1. `npm run check:docs-sync`
2. `npm run docs:build` when public pages, diagrams, or VitePress config
   change
3. broader repository checks when the change also affects repository-control
   behavior
