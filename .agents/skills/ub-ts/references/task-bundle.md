# TypeScript Task Bundle

Use this reference only when the target repository wants an optional Task-based
automation overlay for the `ub-ts` starter profile.

This is an adoption bundle, not part of the core TypeScript scaffold contract.

## Purpose

The bundle gives the host repository a small Task wrapper for the TypeScript
starter profile:

1. a base typecheck-only overlay
2. an ESLint-aware overlay for repos that also adopt the optional ESLint
   starter

It is meant to accelerate adoption for Task-using repositories without making
Task part of the core TypeScript skill contract.

## When To Use

Use this bundle when:

1. the target repository wants a Task wrapper for typecheck and optional ESLint
2. the repository does not already expose equivalent automation cleanly
3. the team wants a small starting point they can adapt locally

## When Not To Use

Do not use this bundle when:

1. the repository already has adequate TypeScript or ESLint automation
2. the repository does not use Task and does not want to adopt it
3. the repository already has a root `Taskfile.yml` and the bundle would create
   overlapping task names without a reconciliation plan

## Files Shipped

This bundle ships:

1. `assets/task-bundle/base/ub-ts.Taskfile.yml`
2. `assets/task-bundle/eslint/ub-ts.Taskfile.yml`

Use the base variant when the repo only wants typecheck.
Use the ESLint variant when the repo also adopts the optional ESLint starter.

## Reconciliation Rules

Before recommending or adopting this bundle, inspect:

1. whether `Taskfile.yml` already exists
2. whether package scripts or CI already expose typecheck and lint commands
3. whether the repo is using the ESLint starter or some other lint stack
4. whether task names such as `typecheck` and `lint-eslint` fit local
   conventions cleanly

Decision rule:

1. if equivalent automation already exists, prefer reusing host-repo truth
2. if typecheck or lint automation is absent or weak, this bundle may be
   adapted

## Adoption Guidance

Default fallback:

```bash
npx tsc --noEmit
```

If the repo also adopts the optional ESLint starter, the typical lint fallback
is:

```bash
npx eslint .
```

Task bundle task surface:

1. base variant: `typecheck`
2. eslint variant: `typecheck`, `lint-eslint`

Recommended usage:

1. choose the variant that matches the host repo's adopted starter set
2. copy or adapt the task definitions into the host repository's own automation
   surface
3. rename tasks if the host repo already uses different local naming

Do not treat the installed skill asset path itself as the portable runtime
contract, especially under `skills.sh`.

## Pros / Cons

Using the bundle:

Pros:

1. faster adoption for Task-using TS repos
2. supports both typecheck-only and ESLint-aware starters
3. stays optional and secondary to the core skill

Cons:

1. still requires reconciliation with host-repo automation
2. ESLint expectations must match the adopted starter
3. redundant in mature repos with existing automation
