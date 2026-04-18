---
name: ub-markdown
description: >-
  Use this skill when the task involves creating, editing, reviewing, or
  refactoring Markdown documents such as README files, AGENTS.md, SKILL.md,
  prompt/agent docs, workflow docs, or other `.md` files; when the goal is to
  stay aligned with repo markdownlint rules, CommonMark/GitHub Flavored
  Markdown behavior, or Markdown structure conventions; or when the user wants
  to reduce markdownlint errors up front instead of relying on cleanup after
  writing. Do not use it for non-Markdown document formats or as a substitute
  for the domain skill that owns the actual content.
argument-hint: "[markdown target] [goal or lint issue]"
user-invocable: true
disable-model-invocation: false
---

# UB Markdown

## Mission

Use this skill to write Markdown that is structurally correct, repo-config
aware, and far less likely to fail `markdownlint-cli2`.

This skill does not replace linting.
It front-loads the rules and common failure patterns so Markdown starts closer
to passing state before validation runs.

## Bundled Assets

This skill ships reusable Markdown lint scaffolding under `assets/` and a
deterministic helper under `scripts/`.

Use them when a repository wants to adopt the same Markdown authoring profile
instead of rewriting the config by hand.

## When Not To Use

- Do not use this skill for non-Markdown formats like HTML, DOCX, or plain
  text notes.
- Do not use this skill as a substitute for the domain skill that owns the
  actual content being written.
- Do not use this skill to justify skipping repo linting or Markdown
  validation.

## Coordination

- Always load `ub-quality` with this skill when editing Markdown.
- Load the relevant domain skill as well when the Markdown content belongs to a
  specialized surface like workflow, governance, customization, or framework
  guidance.
- Treat `ub-markdown` as the Markdown structure and lint-compliance companion,
  not the content owner.

## Load References On Demand

- Read `../references/authoring-conventions.md` when adjusting shared routing
  guidance, output structure, or cross-skill authoring conventions.
- Read `references/repo-markdownlint-resolution.md` first for how to resolve the
  repository's actual Markdown lint config, ignored paths, and command
  entrypoints without duplicating policy in prose.
- Read `references/official-markdown-foundations.md` when parser behavior,
  Markdown syntax interpretation, or tool behavior matters.
- Read `references/task-bundle.md` only when the target repository wants an
  optional Task-based automation overlay for this skill's starter profile.
- Use `scripts/scaffold_markdownlint.py` with
  `assets/markdownlint-template/` when a target repository needs the lint
  profile scaffolded deterministically.

## Core Workflow

1. Detect whether the task is editing a Markdown file that is covered by the
   repo lint targets.
2. Inspect the repository Markdown lint profile before writing:
   `.markdownlint.jsonc`, `.markdownlintignore`, and any local task-runner,
   package-script, or CI entrypoints when relevant.
3. Follow the repo profile first, then use CommonMark and GFM behavior to
   resolve syntax questions.
4. Write Markdown in a lint-friendly structure from the start:
   ATX headings, blank lines around headings/lists/fences, fenced code blocks
   with languages, consistent list markers, and valid links.
5. Avoid common lint traps like duplicate sibling headings, bare URLs, missing
   code fence languages, skipped heading levels, and emphasis used as fake
   headings.
6. Run Markdown lint after edits and fix any remaining issues instead of
   rationalizing them away.
7. When a repository wants this Markdown authoring profile but does not yet
   have it, scaffold the bundled config assets rather than retyping them.

## Config Resolution

Treat the actual linter files as the style source of truth:

1. `.markdownlint.jsonc` or another repo-local `.markdownlint.*` file defines
   the active rule profile
2. `.markdownlintignore` defines excluded paths
3. task-runner files, package scripts, or CI entrypoints define repo lint
   entrypoints and target globs
4. if config is absent and the user wants this house style, scaffold the
   bundled lint files first instead of embedding policy in Markdown docs
5. use CommonMark, GFM, and markdownlint documentation only after local repo
   config has been checked

## Scaffolding

To scaffold this Markdown lint profile into another repository:

```bash
python .agents/skills/ub-markdown/scripts/scaffold_markdownlint.py /path/to/repo
```

What it scaffolds:

1. `.markdownlint.jsonc`
2. `.markdownlintignore`

It does not install packages or mutate existing task-runner wiring.
After scaffolding, use the current recommended command:

```bash
npx --yes markdownlint-cli2 "<target-globs>"
```

## Anti-Patterns

- Do not write Markdown by copying generic internet examples without checking
  the repo config first.
- Do not assume the parser will rescue ambiguous structure like missing blank
  lines around lists or code fences.
- Do not use bold text as a fake section heading when a real heading is
  intended.
- Do not leave bare URLs in prose when the repo lint profile rejects them.
- Do not omit code fence languages unless the fence genuinely has no sensible
  language tag.
- Do not rely on a final lint pass to discover obvious structure problems that
  can be avoided while writing.
- Do not silently scaffold this profile into another repository without making
  the adopting team aware that it is an opinionated house style.

## Output Requirements

Treat this section as the stable output expectation for non-trivial Markdown
work in this catalog.

When this skill is used for non-trivial Markdown work:

1. briefly note the chosen structure approach and one rejected alternative with
   concise pros and cons
2. call out any inline markdownlint exceptions or disables that were kept on
   purpose
3. report the validation command run and whether the file passed

When this skill is used to scaffold the profile into another repository:

1. state which files were created or skipped
2. call out any repo-specific ignore patterns that still need adaptation
3. report the exact lint command the target repo should run next

## Completion Checklist

- The touched Markdown follows the repository lint profile.
- Heading levels are valid and ATX-only.
- Headings, lists, and fenced code blocks have required surrounding blank
  lines.
- Code fences use backticks and declare a language when appropriate.
- Links are not bare URLs unless angle-bracket autolinks are intentionally
  used.
- The document uses real headings instead of emphasized text for structure.
- Repo Markdown lint has been run on the touched scope.
