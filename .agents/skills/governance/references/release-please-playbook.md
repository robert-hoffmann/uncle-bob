# Release Please Playbook

Use this file for repositories that publish versioned artifacts.

## 1) Why `release-please` Is Default

`release-please` provides:

1. release PR generation from commit history
2. changelog generation aligned with Conventional Commits
3. manifest-mode support for multi-package repositories

Primary references:

- <https://github.com/googleapis/release-please>
- <https://github.com/googleapis/release-please-action>
- <https://github.com/googleapis/release-please/blob/main/docs/manifest-releaser.md>
- <https://github.com/googleapis/release-please/blob/main/schemas/config.json>

## 2) Workflow Contract (GitHub Actions)

Minimum workflow properties:

1. trigger on push to release branch (`main` by default)
2. explicit permissions (`contents: write`, `pull-requests: write`)
3. explicit config/manifest files

Skeleton:

```yaml
name: release-please

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          config-file: release-please-config.json
          manifest-file: .release-please-manifest.json
```

## 3) Commit Semantics Requirement

Use Conventional Commits to drive version and changelog behavior.
Non-conforming commit messages are ignored by release automation.

Reference:

- <https://www.conventionalcommits.org/en/v1.0.0/>
- <https://github.com/googleapis/release-please/blob/main/docs/customizing.md>

## 4) Token Caveat

Use default `GITHUB_TOKEN` when sufficient.
Use approved PAT/App token only when downstream workflow chaining explicitly requires it.

## 5) Non-Default Alternatives

### Alternative A: `semantic-release`

Pros:

- mature plugin ecosystem

Cons:

- often higher configuration complexity for mixed stacks

### Alternative B: manual releases

Pros:

- full manual control

Cons:

- higher operational overhead and inconsistency risk
