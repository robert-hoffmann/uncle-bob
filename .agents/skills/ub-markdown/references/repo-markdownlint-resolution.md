# Repo Markdownlint Resolution

Use this reference first when editing Markdown in this repository.

Its job is not to duplicate repo style in prose.
Its job is to show where the real Markdown lint policy lives and how to read
it.

## Policy Source Of Truth

Use these files in order:

1. `.markdownlint.jsonc` or another repo-local `.markdownlint.*` file for the
   active rule set
2. `.markdownlintignore` for excluded paths
3. `Taskfile.yml` or other task runner files for the lint entrypoints and
   target globs
4. CommonMark, GFM, and markdownlint docs when local config does not answer the
   question

If a repo does not yet have Markdown lint config but wants this house style,
scaffold the bundled files first and then adapt them to local repo truth.

## Active Linter Entry Points

Primary repo command:

```bash
npx --yes markdownlint-cli2
```

Task entrypoint from `Taskfile.yml`:

```bash
task lint-md
```

Current Markdown lint targets:

- `AGENTS.md`
- `README.md`
- `docs/**/*.md`
- `.github/agents/**/*.md`
- `.agents/skills/*/SKILL.md`
- `.agents/skills/*/references/**/*.md`
- `.agents/skills/*/assets/**/*.md`
- `.ub-workflows/**/*.md`

Ignored paths from `.markdownlintignore`:

- `tmp/**`
- `tests/skills/ub-governance/fixtures/repo_integrity/**`

Reusable scaffold assets shipped with this skill:

- `assets/markdownlint-template/.markdownlint.jsonc`
- `assets/markdownlint-template/.markdownlintignore`
- `scripts/scaffold_markdownlint.py`

Use the scaffolded files as a starting point in new repositories, then adapt
the ignore paths and lint target globs to local repo truth.

## How To Inspect The Live Repo Profile

Use the config files directly instead of trusting a secondary summary.

Useful reads:

```bash
sed -n '1,240p' .markdownlint.jsonc
sed -n '1,120p' .markdownlintignore
rg -n "lint-md|markdownlint" Taskfile.yml package.json .github
```

What to look for:

1. heading, list, code-fence, link, and formatting rules in
   `.markdownlint.jsonc`
2. repo-specific generated, fixture, or temp exclusions in
   `.markdownlintignore`
3. which Markdown paths are actually linted by default from task-runner or CI
   commands

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
task lint-md
```
````

Good:

````markdown
```bash
task lint-md
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
