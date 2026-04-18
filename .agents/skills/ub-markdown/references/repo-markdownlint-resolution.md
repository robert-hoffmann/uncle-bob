# Repo Markdownlint Resolution

Use this reference first when editing Markdown in a repository that already
has markdownlint or wants to adopt the bundled starter profile.

Its job is not to duplicate live repo style in prose.
Its job is to show where the real Markdown lint policy lives and how to
resolve it without hardcoding one repository's commands.

## Policy Source Of Truth

Use these inputs in order:

1. `.markdownlint.jsonc`, `.markdownlint-cli2.*`, or another repo-local
   `.markdownlint.*` file for the active rule set
2. `.markdownlintignore` for excluded paths
3. local task-runner, package-script, or CI entrypoints for the enforced
   command shape and target globs
4. CommonMark, GFM, and markdownlint docs when local config does not answer the
   question

If a repo does not yet have Markdown lint config but wants this house style,
scaffold the bundled files first and then adapt them to local repo truth.

## Common Entry Point Shapes

The exact command depends on the adopting repository.
Resolve it from local automation first.

Common patterns:

1. a repo wrapper such as `task lint-md`, `npm run lint:md`, or `make lint-md`
2. a targeted-file wrapper such as `task lint-md-files -- path/to/file.md`
3. a direct CLI call such as
   `npx --yes markdownlint-cli2 "docs/**/*.md"` when the repo uses
   `markdownlint-cli2` directly

This skill ships portable scaffold assets:

- `assets/markdownlint-template/.markdownlint.jsonc`
- `assets/markdownlint-template/.markdownlintignore`
- `scripts/scaffold_markdownlint.py`

Use the scaffolded files as a starting point in new repositories, then adapt
ignore paths, target globs, and automation entrypoints to local repo truth.

## How To Inspect The Live Repo Profile

Use the config files directly instead of trusting a secondary summary.

What to look for:

1. heading, list, code-fence, link, and formatting rules in
   `.markdownlint.*`
2. generated, fixture, cache, or temp exclusions in `.markdownlintignore`
3. which Markdown paths are actually linted by default from task-runner, CI,
   or package-script commands
4. which local wrapper or direct CLI entrypoint the repository expects users
   and automation to run

## Practical Interpretation

Once the config has been inspected, write Markdown to match it directly.

Common local failure clusters tend to be:

1. missing blank lines around headings, lists, or fenced code blocks
2. bare URLs where the config requires links or autolinks
3. missing code-fence info strings
4. duplicate or skipped heading structure
5. using emphasis as a fake heading

These are examples of how Markdown lint often fails here, not a replacement for
reading the actual config file.

## Common Failure Patterns

### 1. Missing Blank Lines

Bad:

```markdown
## Heading
- item
```

Good:

```markdown
## Heading

- item
```

### 2. Bare URLs

Bad:

```markdown
See https://example.com for details.
```

Good:

```markdown
See <https://example.com> for details.
```

### 3. Missing Fence Language

Bad:

````markdown
```
name: Example
enabled: true
```
````

Good:

````markdown
```yaml
name: Example
enabled: true
```
````

### 4. Fake Headings

Bad:

```markdown
**Important Notes**
```

Good:

```markdown
## Important Notes
```
