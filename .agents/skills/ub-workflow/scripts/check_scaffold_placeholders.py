#!/usr/bin/env python3
"""Check generated initiative artifacts for unresolved scaffold placeholders."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
SCAFFOLD_SCRIPT = SCRIPT_DIR / "scaffold_initiative.py"


def load_scaffold_module():
    spec = importlib.util.spec_from_file_location("ub_workflow_scaffold_initiative", SCAFFOLD_SCRIPT)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load scaffold helper from {SCAFFOLD_SCRIPT.as_posix()}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(spec.name, module)
    spec.loader.exec_module(module)
    return module


SCAFFOLD_MODULE = load_scaffold_module()


def build_payload(scan_root: Path) -> dict[str, object]:
    initiative_roots = SCAFFOLD_MODULE.discover_initiative_roots_for_placeholder_scan(scan_root)
    payload_roots: list[dict[str, object]] = []
    required_count = 0
    advisory_count = 0

    for initiative_root in initiative_roots:
        findings = SCAFFOLD_MODULE.collect_placeholder_findings(initiative_root)
        root_required = sum(1 for finding in findings if finding.severity == "required")
        root_advisory = len(findings) - root_required
        required_count += root_required
        advisory_count += root_advisory
        payload_roots.append(
            {
                "initiativeRoot": initiative_root.as_posix(),
                "requiredCount": root_required,
                "advisoryCount": root_advisory,
                "summary": SCAFFOLD_MODULE.format_placeholder_summary(initiative_root, findings),
                "findings": [
                    {
                        "file": finding.file_path.resolve().relative_to(initiative_root.resolve()).as_posix(),
                        "line": finding.line_number,
                        "category": finding.category,
                        "severity": finding.severity,
                        "marker": finding.marker,
                        "lineText": finding.line_text,
                    }
                    for finding in findings
                ],
            }
        )

    status = "fail" if required_count else "pass"
    return {
        "status": status,
        "scanRoot": scan_root.resolve().as_posix(),
        "initiativeCount": len(initiative_roots),
        "requiredCount": required_count,
        "advisoryCount": advisory_count,
        "roots": payload_roots,
    }


def print_text_report(payload: dict[str, object]) -> None:
    roots = payload.get("roots")
    if not isinstance(roots, list):
        raise ValueError("Payload roots must be a list")
    if not roots:
        print("placeholder summary: no initiative roots were found in scope")
        return
    for index, root_payload in enumerate(roots):
        if index:
            print()
        print(root_payload["summary"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scan_root",
        nargs="?",
        default=str(Path(".ub-workflows") / "initiatives"),
        help="Initiative root, initiatives directory, .ub-workflows root, or repo root to scan",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when required unresolved placeholders are present",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )
    args = parser.parse_args()

    scan_root = Path(args.scan_root).resolve()
    payload = build_payload(scan_root)

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print_text_report(payload)

    if args.strict and payload["requiredCount"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
