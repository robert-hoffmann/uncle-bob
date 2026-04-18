# Markdown Task Bundle

Use this reference only when the target repository wants an optional Task-based
automation overlay for the `ub-markdown` starter profile.

This is an adoption bundle, not part of the core markdownlint scaffold
contract.

## Purpose

The bundle gives the host repository a small Task wrapper for the same
markdownlint workflow that `ub-markdown` already scaffolds with:

1. `.markdownlint.jsonc`
2. `.markdownlintignore`

It is meant to make adoption easier for repositories that want Task-based local
automation, not to redefine the main skill around Task.

## When To Use

Use this bundle when:

1. the target repository wants a Task wrapper for Markdown linting
2. the repository does not already have equivalent Task, package-script, or CI
   wiring
3. the team wants a small starting point they can adapt locally

## When Not To Use

Do not use this bundle when:

1. the repository already has adequate Markdown lint automation
2. the repository does not use Task and does not want to adopt it
3. the repository already has a root `Taskfile.yml` and adding overlapping
   tasks would create confusion without a clear reconciliation plan

## Files Shipped

This bundle ships:

1. `assets/task-bundle/ub-markdown.Taskfile.yml`

The file is source material for adoption, not a live runtime dependency.

## Reconciliation Rules

Before recommending or adopting this bundle, inspect:

1. whether `Taskfile.yml` already exists
2. whether package scripts already expose Markdown lint
3. whether CI already runs the desired command shape
4. whether task names such as `lint-md` or `lint-md-files` would overlap with
   existing local conventions

Decision rule:

1. if equivalent automation already exists, prefer reusing host-repo truth
2. if automation is absent or weak, this bundle may be adapted

## Adoption Guidance

Default fallback:

```bash
npx --yes markdownlint-cli2 "**/*.md"
```

Task bundle task surface:

1. `lint-md`
2. `lint-md-files`

Recommended usage:

1. copy or adapt the bundle task definitions into the host repository's own
   automation surface
2. keep names only if they fit the host repo cleanly
3. adjust target globs to match host-repo truth before relying on them

Do not treat the installed skill asset path itself as the portable runtime
contract, especially under `skills.sh`.

## Pros / Cons

Using the bundle:

Pros:

1. faster adoption for repos that want Task
2. keeps the task surface aligned with the skill's starter profile
3. stays optional

Cons:

1. still requires local reconciliation
2. may be redundant if the host repo already has good automation
3. should not be copied blindly into a mature repo
