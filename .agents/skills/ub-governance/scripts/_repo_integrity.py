from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUTPUT_ENCODING = "utf-8"
LOCAL_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
READ_REF_PATTERN = re.compile(r"- Read `([^`]+)`")
PYPROJECT_VERSION_PATTERN = re.compile(r'^version\s*=\s*"([^"]+)"$', re.MULTILINE)
COUNT_CLAIM_PATTERN = re.compile(
    r"(?P<skills>\d+)\s+domain skills.*?and\s+(?P<agents>\d+)\s+custom agents",
    re.IGNORECASE | re.DOTALL,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding=DEFAULT_OUTPUT_ENCODING)


def write_payload(payload: dict[str, Any], output: str | None) -> None:
    content = json.dumps(payload, indent=2) + "\n"
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding=DEFAULT_OUTPUT_ENCODING)
    print(content, end="")


def exact_case_path_exists(repo_root: Path, relative_path: str) -> bool:
    current = repo_root.resolve()
    for part in Path(relative_path).parts:
        if not current.is_dir():
            return False
        children = {child.name: child for child in current.iterdir()}
        if part not in children:
            return False
        current = children[part]
    return True


def collect_skill_names(repo_root: Path) -> list[str]:
    skills_root = repo_root / ".agents" / "skills"
    if not skills_root.exists():
        return []
    return sorted(
        child.name
        for child in skills_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    )


def collect_agent_names(repo_root: Path) -> list[str]:
    agents_root = repo_root / ".github" / "agents"
    if not agents_root.exists():
        return []
    return sorted(
        child.name.removesuffix(".agent.md")
        for child in agents_root.iterdir()
        if child.is_file() and child.name.endswith(".agent.md")
    )


def section_text(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"(?ms)^\s{{0,3}}## {re.escape(heading)}\n\n(.*?)(?=^\s{{0,3}}##\s|\Z)")
    match = pattern.search(markdown)
    return match.group(1) if match else ""


def parse_markdown_table_names(path: Path, heading: str) -> list[str]:
    section = section_text(read_text(path), heading)
    names: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        first_cell = cells[0].replace("**", "").strip()
        if first_cell in {"Skill", "Agent", "Path"}:
            continue
        if set(first_cell) == {"-"}:
            continue
        names.append(first_cell)
    return names


def parse_pyproject_version(path: Path) -> str | None:
    match = PYPROJECT_VERSION_PATTERN.search(read_text(path))
    return match.group(1) if match else None


def parse_marketplace_count_claim(description: str) -> tuple[int, int] | None:
    match = COUNT_CLAIM_PATTERN.search(description)
    if not match:
        return None
    return int(match.group("skills")), int(match.group("agents"))


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        return None, text
    marker = text.find("\n---\n", 4)
    if marker == -1:
        return None, text
    frontmatter_text = text[4:marker]
    body = text[marker + 5 :]
    data = yaml.safe_load(frontmatter_text)
    return data if isinstance(data, dict) else None, body


def collect_local_reference_targets(skill_dir: Path, body: str) -> list[str]:
    targets: list[str] = []
    targets.extend(READ_REF_PATTERN.findall(body))
    for match in LOCAL_LINK_PATTERN.findall(body):
        target = match.strip()
        if not target or "://" in target or target.startswith("#"):
            continue
        targets.append(target)
    unique_targets = sorted(dict.fromkeys(targets))
    return [target for target in unique_targets if (skill_dir / target).exists() or not target.startswith("http")]


def unresolved_local_reference_targets(skill_dir: Path, body: str) -> list[str]:
    unresolved: list[str] = []
    for target in sorted(dict.fromkeys(READ_REF_PATTERN.findall(body) + LOCAL_LINK_PATTERN.findall(body))):
        clean_target = target.strip()
        if not clean_target or "://" in clean_target or clean_target.startswith("#"):
            continue
        candidate = (skill_dir / clean_target).resolve()
        if not candidate.exists():
            unresolved.append(clean_target)
    return unresolved
