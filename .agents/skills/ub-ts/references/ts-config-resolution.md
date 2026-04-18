# TypeScript Config Resolution

Use this reference when local TypeScript config discovery, starter scaffolding,
 or optional ESLint support matters.

Do not treat this file as the active policy source of truth.
The real TypeScript and ESLint policy lives in the target repository's actual
config files and automation entrypoints.

## Resolution Order

Use these sources in order:

1. `tsconfig*.json`
2. `eslint.config.*` when ESLint is already present
3. `package.json`, lockfiles, and runtime tooling files
4. task-runner or CI entrypoints that show the real command shape
5. official TypeScript, ESLint, and typescript-eslint docs when local config
   does not answer the question

## Practical Interpretation

If the target repository lacks live TypeScript or ESLint config, treat the
bundled assets in this skill as strong-default starter profiles rather than as
already-enforced repository policy.

## Bundled Starter Assets

This skill ships:

- `assets/tsconfig-template/node/tsconfig.json`
- `assets/tsconfig-template/bundler/tsconfig.json`
- `assets/tsconfig-template/library/tsconfig.json`
- `assets/eslint-template/eslint.config.mjs`
- `scripts/scaffold_ts_baseline.py`

Use the `tsconfig` templates as the primary starter.
Use the ESLint starter only when the target repo wants flat-config linting in
addition to the TypeScript baseline.

## Adaptation Points After Scaffolding

After copying a starter into another repository, review at least:

1. chosen archetype: Node app, bundler app, or library
2. `target`, `lib`, and `types`
3. include and exclude globs
4. declaration and emit posture
5. path aliases or workspace structure
6. whether ESLint is actually wanted, and if so, whether the required
   dependencies are present

## Practical Guidance

1. Inspect real project config first.
2. If the repo already has TypeScript or ESLint config, obey it rather than
   overwriting it.
3. If the repo lacks config and the user wants this house style, scaffold the
   starter and explain the remaining adaptation work explicitly.
4. Do not silently install packages or rewrite CI as part of scaffolding.
