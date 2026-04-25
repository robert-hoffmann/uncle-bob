# UB Quality

Source: `.agents/skills/ub-quality/SKILL.md`

`ub-quality` is the companion baseline for clear, reviewable agent work. It
does not own a language or framework. It makes every other skill more
disciplined by forcing scoped choices, readable explanations, validation, and
consistent formatting in touched content.

## Core Principles

- KISS: keep the solution simple before making it clever.
- DRY: remove repeated knowledge when one shared abstraction improves clarity,
  but do not deduplicate unrelated cases into a forced abstraction.
- YAGNI: do not build speculative extension points, configuration surfaces, or
  framework layers before the project actually needs them.
- Prefer single responsibility, separation of concerns, and composition over
  inheritance when both are viable.
- Preserve behavior and scope unless the user explicitly asks for broader
  change.
- Explain meaningful implementation choices with pros, cons, and a
  recommendation.
- Prefer names, types, and structure to carry mechanics before adding prose.
- Use documentation for contracts, constraints, examples, and reader
  orientation.
- Align touched eligible separator blocks so related data scans cleanly.
- Distinguish repository policy from portable defaults and volatile freshness
  guidance.

## Behavior In Practice

- Forces choice-bearing work to compare practical options, name pros and cons,
  and recommend one path instead of hiding tradeoffs in a confident paragraph.
- Keeps refactors scoped to the touched logical area. It can improve the code
  under the task, but it should not opportunistically reshape unrelated files.
- Uses design-pattern guidance as a filter: extract real duplication, keep
  functions focused, split responsibilities, and prefer composable boundaries.
- Treats documentation as part of quality when it carries contracts,
  constraints, examples, or rationale; it rejects comments that only narrate
  obvious mechanics.
- Enforces separator-column alignment in touched eligible blocks across code,
  configs, examples, docstrings, markup attributes, and documentation tables.
- Separates hard repository policy from strong defaults and advisory freshness
  guidance so portable recommendations do not become fake universal rules.

## Reference Highlights

- `.agents/skills/ub-quality/references/design-patterns.md`: turns KISS, DRY,
  YAGNI, single responsibility, separation of concerns, composition, and
  forward-compatible design into concrete review pressure. It asks whether an
  abstraction removes real complexity or merely anticipates imaginary reuse.
- `.agents/skills/ub-quality/references/formatting-alignment.md`: defines the
  touched-block alignment policy, the separator-column rule, dense-structure
  expansion, and the finalization gate that makes formatting part of done.
- `.agents/skills/ub-quality/references/documentation-structure-refactoring.md`:
  distinguishes useful public docs, comments, file organization, module size,
  safe extraction, naming cleanup, and behavior-preserving refactors.
- `.agents/skills/ub-quality/references/response-readability.md`: pushes
  answer-first structure, compact comparisons, parallel bullets, and readable
  plans or reviews without forcing tables where they would become dense.
- `.agents/skills/ub-quality/references/freshness-portability.md`: decides
  whether a rule is repository policy, a strong local default, a portability
  boundary, or a freshness warning that should be reviewed but not blocked.

## Progressive Disclosure

The main skill applies immediately. References load only when the task needs
their detail: design decisions load design principles, docs edits load the
documentation reference, and substantial user-facing explanations load the
readability reference.

This is why `ub-quality` can be always useful without forcing every response to
be a full style manual.

## Common Invocation Examples

- “Use `ub-quality` to review this plan for missing tradeoffs.”
- “Apply `ub-quality` while cleaning up this documentation.”
- “Check whether this refactor is too broad for the requested scope.”
- “Make this review easier to scan without losing the important findings.”

## Boundaries

Do not use `ub-quality` as the owner of language, framework, runtime,
workflow, or governance decisions. Pair it with the skill that owns the work.

## Tradeoffs

Strength: makes agent output more consistent, reviewable, and safe to resume.

Cost: strict formatting and documentation rules can feel heavy for tiny edits.
The intended balance is to apply the rules to touched logical areas, not to
restyle unrelated files.
