#!/usr/bin/env python3
"""Deterministic test-signal checker for behavior-first TDD quality gates."""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import sys

SUPPORTED_EXTENSIONS = {
    ".ts": "ts",
    ".tsx": "ts",
    ".js": "js",
    ".jsx": "js",
    ".py": "py",
    ".go": "go",
}

BOUNDARY_KEYWORDS = (
    "edge",
    "boundary",
    "invalid",
    "error",
    "fail",
    "empty",
    "none",
    "nil",
    "null",
    "timeout",
    "exception",
    "overflow",
    "underflow",
    "limit",
    "missing",
    "malformed",
    "unauthorized",
    "forbidden",
    "not found",
    "negative",
    "zero",
)

HAPPY_KEYWORDS = (
    "happy",
    "success",
    "valid",
    "works",
    "returns",
    "creates",
    "updates",
    "deletes",
)

TS_RUNTIME_TYPE_KEYWORDS = (
    "required",
    "field is required",
    "type",
    "interface",
    "typing",
    "shape",
)

TS_PRESENCE_ASSERTIONS = (
    "toBeDefined(",
    "toHaveProperty(",
    "toBeTypeOf(",
)

INTERACTION_ASSERTION_PATTERNS = (
    re.compile(r"\.toHaveBeenCalled(?:Times|With)?\("),
    re.compile(r"\bassert_called(?:_once|_once_with|_with)?\b"),
    re.compile(r"\btoHaveBeenNthCalledWith\("),
)

OUTCOME_ASSERTION_PATTERNS = (
    re.compile(r"\.to(?:Equal|StrictEqual|Contain|MatchObject|Throw|BeGreaterThan|BeLessThan|HaveLength|Match|BeCloseTo)\("),
    re.compile(r"\bassert\s+.+==.+"),
    re.compile(r"\bpytest\.raises\("),
    re.compile(r"\brequire\.(?:Equal|NoError|Error|True|False)\("),
    re.compile(r"\bassert\.Equal\("),
    re.compile(r"\bassert\.NoError\("),
)

TEST_FILE_PATTERNS = (
    re.compile(r".*\.test\.(?:ts|tsx|js|jsx)$"),
    re.compile(r".*\.spec\.(?:ts|tsx|js|jsx)$"),
    re.compile(r".*/__tests__/.*\.(?:ts|tsx|js|jsx)$"),
    re.compile(r".*/test_.*\.py$"),
    re.compile(r".*/.*_test\.py$"),
    re.compile(r".*/.*_test\.go$"),
)

RULE_TG001 = "TG001"
RULE_TG002 = "TG002"
RULE_TG003 = "TG003"
RULE_TG004 = "TG004"
RULE_TG005 = "TG005"

RULE_LABELS = {
    RULE_TG001 : "Type Redundancy",
    RULE_TG002 : "Interaction Without Outcome",
    RULE_TG003 : "Pass-Through Test",
    RULE_TG004 : "Happy-Path-Only Suite",
    RULE_TG005 : "Internal-Detail Bias",
}

INTERNAL_DETAIL_KEYWORDS = (
    "private",
    "internal",
    "implementation detail",
    "call order",
    "invocation order",
    "called once",
    "called twice",
    "tohavebeencalled",
    "assert_called",
    "spy",
    "mock",
)

PUBLIC_CONTRACT_KEYWORDS = (
    "public api",
    "api contract",
    "public interface",
    "observable behavior",
)


@dataclass(slots=True)
class TestBlock:
    file_path: Path
    language: str
    name: str
    body: str


@dataclass(slots=True)
class AnalysisReport:
    files_scanned: int = 0
    tests_scanned: int = 0
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    test_names: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "fail" if self.violations else "pass"

    @property
    def summary(self) -> str:
        return (
            f"Analyzed {self.files_scanned} test file(s), "
            f"{self.tests_scanned} test block(s); "
            f"{len(self.violations)} violation(s), {len(self.warnings)} warning(s)."
        )

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "violations": self.violations,
            "warnings": self.warnings,
            "summary": self.summary,
        }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check tests for low-signal anti-patterns.")
    parser.add_argument("--path", required=True, help="Test file or directory to scan.")
    parser.add_argument(
        "--language",
        default="auto",
        choices=("auto", "ts", "py", "go", "js", "other"),
        help="Language override. Use auto for per-file detection.",
    )
    parser.add_argument(
        "--format",
        default="text",
        choices=("text", "json"),
        help="Output format.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when violations are found.",
    )
    return parser.parse_args(argv)


def is_test_file(path: Path) -> bool:
    normalized = str(path.as_posix())
    return any(pattern.match(normalized) for pattern in TEST_FILE_PATTERNS)


def iter_test_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    files: list[Path] = []
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            continue
        if is_test_file(file_path):
            files.append(file_path)
    return sorted(files)


def detect_language(path: Path, preferred: str) -> str:
    if preferred != "auto":
        return preferred
    return SUPPORTED_EXTENSIONS.get(path.suffix, "other")


def extract_test_blocks(path: Path, language: str, content: str) -> list[TestBlock]:
    lines = content.splitlines()
    starts: list[tuple[int, str]] = []

    if language in {"ts", "js"}:
        pattern = re.compile(r"^\s*(?:it|test)\s*\(\s*(['\"`])(.+?)\1")
        for idx, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                starts.append((idx, match.group(2).strip()))
    elif language == "py":
        pattern = re.compile(r"^\s*def\s+(test_[A-Za-z0-9_]+)\s*\(")
        for idx, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                starts.append((idx, match.group(1)))
    elif language == "go":
        pattern = re.compile(r"^\s*func\s+(Test[A-Za-z0-9_]+)\s*\(")
        for idx, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                starts.append((idx, match.group(1)))

    if not starts:
        return []

    blocks: list[TestBlock] = []
    for index, (start_line, test_name) in enumerate(starts):
        end_line = starts[index + 1][0] if index + 1 < len(starts) else len(lines)
        body = "\n".join(lines[start_line:end_line])
        blocks.append(TestBlock(file_path=path, language=language, name=test_name, body=body))
    return blocks


def has_interaction_assertions(body: str) -> bool:
    return any(pattern.search(body) for pattern in INTERACTION_ASSERTION_PATTERNS)


def has_outcome_assertions(body: str) -> bool:
    return any(pattern.search(body) for pattern in OUTCOME_ASSERTION_PATTERNS)


def boundary_keyword_count(names: Iterable[str]) -> int:
    lowered = [name.lower() for name in names]
    return sum(1 for name in lowered if any(keyword in name for keyword in BOUNDARY_KEYWORDS))


def happy_keyword_count(names: Iterable[str]) -> int:
    lowered = [name.lower() for name in names]
    return sum(1 for name in lowered if any(keyword in name for keyword in HAPPY_KEYWORDS))


def rule_message(rule_id: str, message: str, location: str | None = None) -> str:
    label = RULE_LABELS.get(rule_id)
    prefix = f"[{rule_id} {label}]" if label else f"[{rule_id}]"
    if location:
        return f"{prefix} {location} -> {message}"
    return f"{prefix} {message}"


def interaction_assertion_count(body: str) -> int:
    return sum(len(pattern.findall(body)) for pattern in INTERACTION_ASSERTION_PATTERNS)


def outcome_assertion_count(body: str) -> int:
    return sum(len(pattern.findall(body)) for pattern in OUTCOME_ASSERTION_PATTERNS)


def has_probable_internal_detail_focus(block: TestBlock) -> bool:
    lower_name = block.name.lower()
    lower_body = block.body.lower()

    interaction_count = interaction_assertion_count(block.body)
    outcome_count = outcome_assertion_count(block.body)
    if interaction_count == 0 or outcome_count == 0:
        return False

    detail_hits = sum(
        1
        for keyword in INTERNAL_DETAIL_KEYWORDS
        if keyword in lower_name or keyword in lower_body
    )
    has_internal_focus = any(
        keyword in lower_name or keyword in lower_body
        for keyword in ("private", "internal", "implementation detail", "call order", "invocation order")
    )
    public_contract_hits = sum(
        1
        for keyword in PUBLIC_CONTRACT_KEYWORDS
        if keyword in lower_name or keyword in lower_body
    )
    return (
        has_internal_focus
        and detail_hits >= 2
        and public_contract_hits == 0
        and interaction_count >= outcome_count
    )


def analyze_block(block: TestBlock, report: AnalysisReport) -> None:
    lower_name = block.name.lower()
    lower_body = block.body.lower()
    location = f"{block.file_path}:{block.name}"
    has_outcomes = has_outcome_assertions(block.body)

    if block.language in {"ts", "js"} and any(
        keyword in lower_name for keyword in TS_RUNTIME_TYPE_KEYWORDS
    ):
        has_presence_only = any(token.lower() in lower_body for token in TS_PRESENCE_ASSERTIONS)
        if has_presence_only and not has_outcomes:
            report.violations.append(
                rule_message(
                    RULE_TG001,
                    "Runtime test appears to restate type-system guarantees.",
                    location,
                )
            )

    if "getter" in lower_name or "setter" in lower_name:
        report.violations.append(
            rule_message(
                RULE_TG003,
                "Trivial getter/setter test detected. Prefer behavior-level coverage.",
                location,
            )
        )

    has_interactions = has_interaction_assertions(block.body)
    if has_interactions and not has_outcomes:
        report.violations.append(
            rule_message(
                RULE_TG002,
                "Interaction assertions found without observable outcome assertions.",
                location,
            )
        )

    if has_probable_internal_detail_focus(block):
        report.warnings.append(
            rule_message(
                RULE_TG005,
                "Test may prioritize internal-detail verification over public interface behavior.",
                location,
            )
        )


def analyze_happy_path_bias(report: AnalysisReport) -> None:
    if not report.test_names:
        return
    boundary_count = boundary_keyword_count(report.test_names)
    happy_count = happy_keyword_count(report.test_names)
    total = len(report.test_names)

    if total >= 6 and boundary_count == 0 and happy_count >= max(3, total // 2):
        report.violations.append(
            rule_message(
                RULE_TG004,
                "Suite naming indicates repeated happy-path focus without boundary/error coverage tags.",
            )
        )
    elif total >= 4 and boundary_count == 0 and happy_count >= 2:
        report.warnings.append(
            rule_message(
                RULE_TG004,
                "Suite appears happy-path heavy without explicit boundary/error test naming.",
            )
        )


def print_text(report: AnalysisReport) -> None:
    print(report.summary)
    if report.violations:
        print("\nViolations:")
        for item in report.violations:
            print(f"- {item}")
    if report.warnings:
        print("\nWarnings:")
        for item in report.warnings:
            print(f"- {item}")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    target = Path(args.path).expanduser().resolve()
    if not target.exists():
        print(f"Target does not exist: {target}", file=sys.stderr)
        return 2

    files = iter_test_files(target)
    if not files:
        report = AnalysisReport()
        report.warnings.append("No matching test files found for analysis.")
        if args.format == "json":
            print(json.dumps(report.to_json(), indent=2))
        else:
            print_text(report)
        return 0

    report = AnalysisReport(files_scanned=len(files))
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            report.warnings.append(f"Skipped non-UTF-8 file: {file_path}")
            continue
        language = detect_language(file_path, args.language)
        blocks = extract_test_blocks(file_path, language, content)
        if not blocks:
            report.warnings.append(f"No test blocks parsed in: {file_path}")
            continue
        report.tests_scanned += len(blocks)
        for block in blocks:
            report.test_names.append(block.name)
            analyze_block(block, report)

    analyze_happy_path_bias(report)

    if args.format == "json":
        print(json.dumps(report.to_json(), indent=2))
    else:
        print_text(report)

    if args.strict and report.violations:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
