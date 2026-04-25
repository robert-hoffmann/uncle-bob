import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const SKIP_DIRS = new Set([
  ".git",
  ".pytest_cache",
  ".venv",
  "dist",
  "node_modules",
  "tmp",
]);
const STATIC_ASSET_EXTENSIONS = new Set([
  ".avif",
  ".gif",
  ".ico",
  ".jpeg",
  ".jpg",
  ".png",
  ".svg",
  ".webp",
]);
const INSTALL_DOC                    = "docs/install.md";
const DOCS_AGENTS                    = "docs/AGENTS.md";
const VITEPRESS_CONFIG               = "docs/.vitepress/config.ts";
const GENERATED_PATH_REFERENCES      = new Set([
  "docs/adr/registry.json",
]);
const INSTALL_COMMAND                = "npx skills add robert-hoffmann/uncle-bob";
const PROGRESSIVE_DISCLOSURE_DOC     = "docs/guide/references-progressive-disclosure.md";
const REQUIRED_SKILL_DOC_SECTIONS    = [
  "## Core Principles",
  "## Behavior In Practice",
  "## Reference Highlights",
  "## Progressive Disclosure",
  "## Common Invocation Examples",
  "## Boundaries",
  "## Tradeoffs",
];
const REQUIRED_SKILL_DEEP_DIVE_LINKS = new Map([
  ["ub-workflow", "/deep-dives/ub-workflow"],
  ["ub-governance", "/deep-dives/ub-governance"],
]);
const failures                       = [];

function toPosix(filePath) {
  return filePath.split(path.sep).join("/");
}

function walk(dir, base = ROOT) {
  const abs = path.resolve(base, dir);
  if (!fs.existsSync(abs)) return [];

  const out = [];
  const stack = [abs];
  while (stack.length > 0) {
    const current = stack.pop();
    if (!current) continue;

    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) {
        if (SKIP_DIRS.has(entry.name)) continue;
        stack.push(full);
        continue;
      }
      if (entry.isFile()) {
        out.push(toPosix(path.relative(ROOT, full)));
      }
    }
  }
  return out.sort();
}

function read(filePath) {
  return fs.readFileSync(path.resolve(ROOT, filePath), "utf8");
}

function recordFailure(message) {
  failures.push(message);
}

function getMarkdownFiles() {
  const candidates = [
    "AGENTS.md",
    "README.md",
    ".github/workflows/README.md",
    ...walk("docs").filter((file) => file.endsWith(".md")),
  ];
  return candidates.filter((file) => fs.existsSync(path.resolve(ROOT, file)));
}

function getPublicDocsMarkdownFiles() {
  return walk("docs").filter((file) => file.endsWith(".md") && file !== DOCS_AGENTS);
}

function sanitizeLinkTarget(rawTarget) {
  const trimmed        = rawTarget.trim();
  const [withoutHash]  = trimmed.split("#");
  const [withoutQuery] = withoutHash.split("?");
  return withoutQuery.trim();
}

function checkPathExistsAny(candidates) {
  return candidates.some((candidate) => fs.existsSync(path.resolve(ROOT, candidate)));
}

function resolveDocsRouteCandidates(routePath) {
  const route = routePath.replace(/^\/+/, "");
  if (!route) return ["docs/index.md"];

  const ext = path.extname(route);
  if (ext) {
    if (STATIC_ASSET_EXTENSIONS.has(ext.toLowerCase())) {
      return [`docs/public/${route}`];
    }
    return [`docs/${route}`];
  }

  const clean = route.replace(/\/+$/, "");
  return [`docs/${clean}.md`, `docs/${clean}/index.md`];
}

function resolveRelativeLinkCandidates(sourceFile, targetPath) {
  const sourceDir = path.dirname(sourceFile);
  const base      = toPosix(path.normalize(path.join(sourceDir, targetPath)));
  const ext       = path.extname(base);
  if (ext) return [base];
  return [base, `${base}.md`, `${base}/index.md`];
}

function extractMarkdownLinks(content) {
  return [...content.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)].map((match) => match[1]);
}

function collectSkillNames() {
  return walk(".agents/skills", ROOT)
    .filter((file) => file.endsWith("/SKILL.md"))
    .map((file) => file.split("/").at(-2))
    .filter(Boolean)
    .sort();
}

function checkMarkdownLinks() {
  for (const file of getMarkdownFiles()) {
    const content = read(file);
    for (const rawTarget of extractMarkdownLinks(content)) {
      const target = sanitizeLinkTarget(rawTarget);
      if (!target || target.startsWith("#")) continue;
      if (
        target.startsWith("http://") ||
        target.startsWith("https://") ||
        target.startsWith("mailto:")
      ) {
        continue;
      }

      if (target.startsWith("/")) {
        const candidates = resolveDocsRouteCandidates(target);
        if (!checkPathExistsAny(candidates)) {
          recordFailure(
            `${file}: broken absolute docs link \`${rawTarget}\` (checked: ${candidates.join(", ")}).`,
          );
        }
        continue;
      }

      const candidates = resolveRelativeLinkCandidates(file, target);
      if (!checkPathExistsAny(candidates)) {
        recordFailure(
          `${file}: broken relative link \`${rawTarget}\` (checked: ${candidates.join(", ")}).`,
        );
      }
    }
  }
}

function checkSidebarRouteLinks() {
  const content = read(VITEPRESS_CONFIG);
  const links   = [...content.matchAll(/link:\s*"([^"]+)"/g)].map((match) => match[1]);
  for (const link of links) {
    if (!link.startsWith("/")) continue;
    const candidates = resolveDocsRouteCandidates(link);
    if (!checkPathExistsAny(candidates)) {
      recordFailure(
        `${VITEPRESS_CONFIG}: sidebar/nav link \`${link}\` has no matching doc page (checked: ${candidates.join(", ")}).`,
      );
    }
  }
}

function checkNpmRunReferences() {
  const packageJson = JSON.parse(read("package.json"));
  const scripts     = packageJson.scripts ?? {};

  for (const file of getMarkdownFiles()) {
    const content = read(file);
    for (const match of content.matchAll(/\bnpm run ([a-zA-Z0-9:_-]+)/g)) {
      const scriptName = match[1];
      if (!scripts[scriptName]) {
        recordFailure(`${file}: references missing npm script \`npm run ${scriptName}\`.`);
      }
    }
  }
}

function checkExplicitPathCodeReferences() {
  const allowedPrefixes = [
    ".agents/",
    ".github/",
    ".ub-workflows/",
    "AGENTS.md",
    "README.md",
    "Taskfile.yml",
    "assets/",
    "docs/",
    "package.json",
    "plugin.json",
    "pyproject.toml",
    "scripts/",
    "tests/",
  ];

  for (const file of getMarkdownFiles()) {
    const content   = read(file);
    const codeSpans = [...content.matchAll(/`([^`\n]+)`/g)].map((match) => match[1].trim());
    for (const token of codeSpans) {
      if (!allowedPrefixes.some((prefix) => token === prefix || token.startsWith(prefix))) continue;
      if (token.includes("<") || token.includes(">")) continue;
      if (token.includes("*") || token.includes("{") || token.includes("}")) continue;
      if (/\s/.test(token)) continue;

      const cleaned = token.replace(/[),.:;]+$/, "");
      if (GENERATED_PATH_REFERENCES.has(cleaned)) continue;
      if (!fs.existsSync(path.resolve(ROOT, cleaned))) {
        recordFailure(`${file}: references missing path \`${cleaned}\`.`);
      }
    }
  }
}

function checkSkillDocs() {
  const skillNames = collectSkillNames();
  const docsIndex  = read("docs/skills/index.md");

  for (const skillName of skillNames) {
    const docsPath = `docs/skills/${skillName}.md`;
    if (!fs.existsSync(path.resolve(ROOT, docsPath))) {
      recordFailure(`Missing skill docs page for \`${skillName}\`: expected ${docsPath}.`);
      continue;
    }

    const docs = read(docsPath);
    if (!docs.includes(`.agents/skills/${skillName}/SKILL.md`)) {
      recordFailure(`${docsPath}: must reference its source skill path.`);
    }
    for (const section of REQUIRED_SKILL_DOC_SECTIONS) {
      if (!docs.includes(section)) {
        recordFailure(`${docsPath}: missing required section \`${section}\`.`);
      }
    }
    if (
      fs.existsSync(path.resolve(ROOT, `.agents/skills/${skillName}/references`)) &&
      !docs.includes(`.agents/skills/${skillName}/references/`)
    ) {
      recordFailure(`${docsPath}: must highlight at least one source reference path.`);
    }
    const requiredDeepDive = REQUIRED_SKILL_DEEP_DIVE_LINKS.get(skillName);
    if (requiredDeepDive && !docs.includes(requiredDeepDive)) {
      recordFailure(`${docsPath}: missing required deep-dive link \`${requiredDeepDive}\`.`);
    }
    if (!docsIndex.includes(`./${skillName}`)) {
      recordFailure(`docs/skills/index.md: missing catalog link for \`${skillName}\`.`);
    }
  }

  const documentedSkillPages = walk("docs/skills")
    .filter((file) => file.match(/^docs\/skills\/ub-[^/]+\.md$/))
    .map((file) => path.posix.basename(file, ".md"));
  for (const pageSkillName of documentedSkillPages) {
    if (!skillNames.includes(pageSkillName)) {
      recordFailure(`docs/skills/${pageSkillName}.md: no matching skill directory.`);
    }
  }
}

function checkDocsPlatformConfig() {
  const content = read(VITEPRESS_CONFIG);
  const requiredSnippets = [
    'const base = "/uncle-bob/";',
    'outDir     : "../dist"',
    'srcExclude : [',
    '"AGENTS.md"',
    "https://github.com/robert-hoffmann/uncle-bob",
    "/guide/references-progressive-disclosure",
  ];

  for (const snippet of requiredSnippets) {
    if (!content.includes(snippet)) {
      recordFailure(`${VITEPRESS_CONFIG}: missing required config snippet \`${snippet}\`.`);
    }
  }

  if (fs.existsSync(path.resolve(ROOT, "vite.config.ts"))) {
    recordFailure("vite.config.ts must not exist; this repo uses VitePress-only docs.");
  }
}

function checkForbiddenClaims() {
  const forbidden = [
    { pattern: /\bParallax\b/i, reason: "copied source-project docs" },
    { pattern: /\bparallax\b/i, reason: "copied source-project docs" },
    { pattern: /\bitech-agents\b/i, reason: "stale pre-rename repository identity" },
    { pattern: /\/uncle-bob\/docs\//i, reason: "old nested docs Pages base" },
    { pattern: /github\.com\/robert-hoffmann\/itech-agents/i, reason: "stale GitHub URL" },
  ];

  for (const file of getMarkdownFiles()) {
    const content = read(file);
    for (const rule of forbidden) {
      if (rule.pattern.test(content)) {
        recordFailure(`${file}: contains forbidden claim (${rule.reason}).`);
      }
    }
  }
}

function checkPublicDocsFocus() {
  const forbiddenPublicPatterns = [
    {
      pattern : /\bTaskfile\.yml\b/i,
      reason  : "repo-maintenance command surface belongs outside public skill docs",
    },
    {
      pattern : /\.github\/workflows/i,
      reason  : "CI internals belong outside public skill docs",
    },
    {
      pattern : /scripts\/repo-maintenance/i,
      reason  : "repo-maintenance scripts belong outside public skill docs",
    },
    {
      pattern : /\bRepository Architecture\b/i,
      reason  : "repo architecture must not be a public docs focus",
    },
    {
      pattern : /\bCI and Deployment\b/i,
      reason  : "deployment internals must not be a public docs focus",
    },
    {
      pattern : /\bDocs Sync\b/i,
      reason  : "repo docs-sync policy belongs in AGENTS.md and README.md",
    },
  ];

  for (const file of getPublicDocsMarkdownFiles()) {
    if (file.startsWith("docs/reference/")) {
      recordFailure(`${file}: public site must not publish repo-maintenance reference pages.`);
    }

    const content = read(file);
    for (const rule of forbiddenPublicPatterns) {
      if (rule.pattern.test(content)) {
        recordFailure(`${file}: contains repo-maintenance focus (${rule.reason}).`);
      }
    }
  }
}

function checkInstallDocs() {
  const readme     = read("README.md");
  const installDoc = read(INSTALL_DOC);

  for (const [file, content] of [
    ["README.md", readme],
    [INSTALL_DOC, installDoc],
  ]) {
    if (!content.includes(INSTALL_COMMAND)) {
      recordFailure(`${file}: missing canonical skills.sh install command.`);
    }
  }
}

function checkRequiredDocs() {
  const requiredDocs = [
    "docs/index.md",
    DOCS_AGENTS,
    INSTALL_DOC,
    "docs/guide/skill-system.md",
    "docs/guide/core-stack.md",
    "docs/guide/routing-model.md",
    PROGRESSIVE_DISCLOSURE_DOC,
    "docs/guide/portability-model.md",
    "docs/skills/index.md",
    "docs/deep-dives/ub-workflow.md",
    "docs/deep-dives/ub-governance.md",
    "docs/deep-dives/workflow-governance.md",
  ];

  for (const docsPath of requiredDocs) {
    if (!fs.existsSync(path.resolve(ROOT, docsPath))) {
      recordFailure(`Missing required docs page: ${docsPath}.`);
    }
  }
}

checkRequiredDocs();
checkMarkdownLinks();
checkSidebarRouteLinks();
checkNpmRunReferences();
checkExplicitPathCodeReferences();
checkSkillDocs();
checkPublicDocsFocus();
checkInstallDocs();
checkDocsPlatformConfig();
checkForbiddenClaims();

if (failures.length > 0) {
  console.error("check-docs-sync: FAILED");
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log("check-docs-sync: OK");
