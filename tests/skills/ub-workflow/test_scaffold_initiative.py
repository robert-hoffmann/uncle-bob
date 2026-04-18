from __future__ import annotations

from argparse import Namespace
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


def find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "pyproject.toml").exists() and (candidate / ".agents").exists():
            return candidate
    msg = "Could not locate repository root for workflow tests"
    raise RuntimeError(msg)


PROJECT_ROOT = find_repo_root()
SCRIPT = PROJECT_ROOT / ".agents" / "skills" / "ub-workflow" / "scripts" / "scaffold_initiative.py"
CHECK_SCRIPT = PROJECT_ROOT / ".agents" / "skills" / "ub-workflow" / "scripts" / "check_scaffold_placeholders.py"
PYTHON_BIN = sys.executable

SCRIPT_SPEC = importlib.util.spec_from_file_location("ub_workflow_scaffold_initiative", SCRIPT)
assert SCRIPT_SPEC is not None and SCRIPT_SPEC.loader is not None
SCRIPT_MODULE = importlib.util.module_from_spec(SCRIPT_SPEC)
sys.modules[SCRIPT_SPEC.name] = SCRIPT_MODULE
SCRIPT_SPEC.loader.exec_module(SCRIPT_MODULE)


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


class ScaffoldInitiativeScriptTests(unittest.TestCase):
    def test_create_bootstraps_ops_root_and_scaffolds_blank_initiative(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / ".ub-workflows"

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    "my-new-initiative",
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-01",
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            target = ops_root / "initiatives" / "2026-04-01-my-new-initiative"
            self.assertTrue((ops_root / "initiatives" / "README.md").exists())
            self.assertTrue((ops_root / "initiatives" / "operation-guide.md").exists())
            self.assertTrue((ops_root / "initiatives" / "user-guide.md").exists())
            self.assertTrue((ops_root / "initiatives" / "AGENTS.md").exists())
            self.assertTrue((target / "README.md").exists())
            self.assertTrue((target / "roadmap.md").exists())
            self.assertFalse((target / "sprint-template").exists())

            root_readme = (ops_root / "initiatives" / "README.md").read_text(encoding="utf-8")
            ops_user_guide = (ops_root / "initiatives" / "user-guide.md").read_text(encoding="utf-8")
            readme = (target / "README.md").read_text(encoding="utf-8")
            roadmap = (target / "roadmap.md").read_text(encoding="utf-8")

            self.assertIn("`initiatives/2026-04-01-my-new-initiative`", root_readme)
            self.assertIn("My New Initiative", readme)
            self.assertIn("2026-04-01", readme)
            self.assertIn("Scaffold valid for PRD authoring; PRD import pending", readme)
            self.assertIn("`prd_ready: blocked`", readme)
            self.assertIn("unassigned", readme)
            self.assertIn("Master PRD imported into `./prd.md`", roadmap)
            self.assertIn("- Next sprint: `define after roadmap approval`", roadmap)
            self.assertIn("Start the next sprint.", ops_user_guide)
            self.assertIn("preview only; execution begins only after", ops_user_guide)
            self.assertIn("later approval message", ops_user_guide)
            self.assertIn("What Repo Truth Says", ops_user_guide)
            self.assertIn("Implementation Paths", ops_user_guide)
            self.assertIn("artifact or validation", ops_user_guide)

    def test_create_uses_prd_source_slug_and_copies_prd_without_rewriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            prd_source = Path(tmp) / "service-accounts-prd.md"
            prd_body = "# Service Accounts PRD\n\nThis content must be copied as-is.\n"
            prd_source.write_text(prd_body, encoding="utf-8")

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    "--ops-root",
                    str(ops_root),
                    "--prd-source",
                    str(prd_source),
                    "--date",
                    "2026-04-03",
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

            target = ops_root / "initiatives" / "2026-04-03-service-accounts-prd"
            self.assertEqual((target / "prd.md").read_text(encoding="utf-8"), prd_body)

            readme = (target / "README.md").read_text(encoding="utf-8")
            self.assertIn("Scaffold valid for PRD review; roadmap planning pending", readme)
            self.assertIn("`prd_ready: blocked`", readme)
            self.assertIn("Do not initialize sprint directories until `roadmap_ready: pass`", readme)

    def test_create_supports_imported_prd_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            prd_source = Path(tmp) / "parser-modernization-prd.md"
            prd_source.write_text("# Parser Modernization\n", encoding="utf-8")

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    "--ops-root",
                    str(ops_root),
                    "--prd-source",
                    str(prd_source),
                    "--initiative-name",
                    "Parser Modernization",
                    "--owner",
                    "Platform Team",
                    "--prd-imported",
                    "--date",
                    "2026-04-02",
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

            target = ops_root / "initiatives" / "2026-04-02-parser-modernization"
            readme = (target / "README.md").read_text(encoding="utf-8")

            self.assertIn("Parser Modernization", readme)
            self.assertIn("Platform Team", readme)
            self.assertIn("Scaffold valid for roadmap planning; roadmap approval pending", readme)
            self.assertIn("`prd_ready: pass`", readme)

    def test_prepare_sprints_ignores_legacy_local_sprint_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)
            self.assertFalse((initiative_root / "sprint-template").exists())

            legacy_template_root = initiative_root / "sprint-template"
            legacy_template_root.mkdir(parents=True, exist_ok=True)
            (legacy_template_root / "sprint.md").write_text(
                "# Sprint PRD\n\nLEGACY LOCAL TEMPLATE SHOULD NOT BE USED.\n",
                encoding="utf-8",
            )
            (legacy_template_root / "closeout.md").write_text("# Sprint Closeout\n", encoding="utf-8")
            (legacy_template_root / "decision-log.md").write_text("# Sprint Decision Log\n", encoding="utf-8")
            (legacy_template_root / "evidence").mkdir(exist_ok=True)

            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`roadmap_ready: pass`"),
                encoding="utf-8",
            )

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "prepare-sprints", str(initiative_root)])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            sprint_text = (initiative_root / "sprints" / "01-define-contract" / "sprint.md").read_text(encoding="utf-8")
            self.assertIn("## Machine-Derived Context", sprint_text)
            self.assertNotIn("LEGACY LOCAL TEMPLATE SHOULD NOT BE USED", sprint_text)

    def test_prepare_sprints_renders_roadmap_metadata_into_sprint_prds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Current Position

- Current sprint: `none`
- Last completed sprint: `none`
- Next sprint: `define after roadmap approval`
- Resume from: `review or generate roadmap from ./prd.md`
- Active blockers: `none`

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
    - Goal: Define the contract
            so every later sprint inherits one stable workflow baseline
  - Depends on: `none`
    - Validation focus: Contract review
            with lifecycle and gate consistency checks
  - Subtasks:
        - [ ] Draft the contract
                and capture the shared gate vocabulary
    - [ ] Review the contract with stakeholders
  - Evidence folder: `./sprints/01-define-contract/evidence/`

- [ ] Sprint 02 - Wire Runtime
  - Path: `./sprints/02-wire-runtime/sprint.md`
  - Goal: Wire runtime behavior
  - Depends on: `Sprint 01 - Define Contract`
  - Validation focus: Engine integration tests
  - Subtasks:
    - [ ] Implement runtime changes
  - Evidence folder: `./sprints/02-wire-runtime/evidence/`

## Final Audit Step

1. Confirm completeness.
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`roadmap_ready: pass`"),
                encoding="utf-8",
            )
            self.assertFalse((initiative_root / "sprint-template").exists())

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "prepare-sprints", str(initiative_root)])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            first_sprint = (initiative_root / "sprints" / "01-define-contract" / "sprint.md").read_text(encoding="utf-8")
            second_sprint = (initiative_root / "sprints" / "02-wire-runtime" / "sprint.md").read_text(encoding="utf-8")
            readme = readme_path.read_text(encoding="utf-8")
            roadmap = (initiative_root / "roadmap.md").read_text(encoding="utf-8")

            self.assertIn("## Machine-Derived Context", first_sprint)
            self.assertIn(
                "- Goal: Define the contract so every later sprint inherits one stable workflow baseline",
                first_sprint,
            )
            self.assertIn(
                "- Validation focus: Contract review with lifecycle and gate consistency checks",
                first_sprint,
            )
            self.assertIn("- [ ] Draft the contract and capture the shared gate vocabulary", first_sprint)
            self.assertNotIn("REPLACE_", first_sprint)
            self.assertIn("PENDING_HANDOFF:", second_sprint)
            self.assertIn("`sprint_content_ready: pass`", readme)
            self.assertIn("Sprint pack prepared, awaiting Sprint 01 execution", readme)
            self.assertIn(
                "- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template",
                roadmap,
            )

    def test_prepare_sprints_preserves_non_placeholder_sprint_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`roadmap_ready: pass`"),
                encoding="utf-8",
            )

            init_result = run_cmd([PYTHON_BIN, str(SCRIPT), "init-sprints", str(initiative_root)])
            self.assertEqual(init_result.returncode, 0, msg=init_result.stdout + init_result.stderr)

            sprint_path = initiative_root / "sprints" / "01-define-contract" / "sprint.md"
            sprint_path.write_text(
                "# Sprint PRD\n\n## Summary\n\nPrepared custom sprint content.\n",
                encoding="utf-8",
            )

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "prepare-sprints", str(initiative_root)])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertEqual(
                sprint_path.read_text(encoding="utf-8"),
                "# Sprint PRD\n\n## Summary\n\nPrepared custom sprint content.\n",
            )
            self.assertIn("preserved", result.stdout)

    def test_prepare_sprints_accepts_recorded_roadmap_approval_after_gate_advances(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: generated

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`sprint_closeout: pass`"),
                encoding="utf-8",
            )

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "prepare-sprints", str(initiative_root)])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((initiative_root / "sprints" / "01-define-contract" / "sprint.md").exists())

    def test_prepare_sprints_blocks_without_roadmap_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [ ] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`
""",
                encoding="utf-8",
            )

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "prepare-sprints", str(initiative_root)])

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("Sprint preparation blocked because the roadmap is not ready", result.stderr)
            self.assertIn("roadmap_ready: pass", result.stderr)

    def test_resume_order_for_placeholder_sprint_falls_back_to_prd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            roadmap_path = initiative_root / "roadmap.md"
            roadmap_path.write_text(
                """# Sprint Roadmap

Status: generated

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Current Position

- Current sprint: `none`
- Last completed sprint: `none`
- Next sprint: `Sprint 01 - Define Contract`
- Resume from: `sprints/01-define-contract/sprint.md`
- Active blockers: `none`

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`roadmap_ready: pass`"),
                encoding="utf-8",
            )

            init_result = run_cmd([PYTHON_BIN, str(SCRIPT), "init-sprints", str(initiative_root)])
            self.assertEqual(init_result.returncode, 0, msg=init_result.stdout + init_result.stderr)

            ordered = SCRIPT_MODULE.resolve_resume_file_order(initiative_root)

            self.assertEqual(
                [path.resolve().relative_to(initiative_root.resolve()).as_posix() for path in ordered],
                ["roadmap.md", "sprints/01-define-contract/sprint.md", "README.md", "prd.md"],
            )

    def test_resume_order_for_later_prepared_sprint_uses_prior_closeout_without_prd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            roadmap_path = initiative_root / "roadmap.md"
            roadmap_path.write_text(
                """# Sprint Roadmap

Status: generated

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Current Position

- Current sprint: `none`
- Last completed sprint: `Sprint 01 - Define Contract`
- Next sprint: `Sprint 02 - Wire Runtime`
- Resume from: `sprints/02-wire-runtime/sprint.md`
- Active blockers: `none`

## Sprint Sequence

- [x] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`

- [ ] Sprint 02 - Wire Runtime
  - Path: `./sprints/02-wire-runtime/sprint.md`
  - Goal: Wire runtime behavior
  - Depends on: `Sprint 01 - Define Contract`
  - Validation focus: Engine integration tests
  - Subtasks:
    - [ ] Implement runtime changes
  - Evidence folder: `./sprints/02-wire-runtime/evidence/`
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`sprint_content_ready: pass`"),
                encoding="utf-8",
            )

            prepare_result = run_cmd([PYTHON_BIN, str(SCRIPT), "prepare-sprints", str(initiative_root)])
            self.assertEqual(prepare_result.returncode, 0, msg=prepare_result.stdout + prepare_result.stderr)

            (initiative_root / "sprints" / "01-define-contract" / "closeout.md").write_text(
                "# Sprint Closeout\n\n## handoff_note\n\nReady for Sprint 02.\n",
                encoding="utf-8",
            )

            ordered = SCRIPT_MODULE.resolve_resume_file_order(
                initiative_root,
                initiative_root / "sprints" / "02-wire-runtime" / "sprint.md",
            )

            self.assertEqual(
                [path.resolve().relative_to(initiative_root.resolve()).as_posix() for path in ordered],
                [
                    "roadmap.md",
                    "sprints/01-define-contract/closeout.md",
                    "sprints/02-wire-runtime/sprint.md",
                    "README.md",
                ],
            )

    def test_archive_blocks_without_archive_review_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "README.md").write_text(
                """# Initiative Status

## Snapshot

| Field | Value |
| ----- | ----- |
| Initiative | Parser Modernization |
| Imported on | 2026-04-02 |
| Current phase | Final audit complete, awaiting archive review |
| Current gate | `sprint_closeout: pass` |
| Roadmap status | `complete` |
| Active sprint | `none` |
| Last completed sprint | `Final Audit - Confirm Completion` |
| Next step | `archive review needed` |
| Blockers | `none` |

## Validation Pointers

Complete.
""",
                encoding="utf-8",
            )
            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: complete

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template
- [x] Sprint execution started
- [x] All sprint closeouts completed
- [x] Final audit completed as the last roadmap item
- [x] Follow-up audit or refactor decision recorded
- [x] `./retained-note.md` written
""",
                encoding="utf-8",
            )
            (initiative_root / "retained-note.md").write_text(
                """# Retained Note

## Outcome

Completed successfully.
""",
                encoding="utf-8",
            )

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "archive", str(initiative_root), "--ops-root", str(ops_root)])

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("archive_ready: pass", result.stderr)
            self.assertTrue(initiative_root.exists())

    def test_init_sprints_creates_all_roadmap_directories_and_updates_status_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            roadmap_path = initiative_root / "roadmap.md"
            roadmap_path.write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Current Position

- Current sprint: `none`
- Last completed sprint: `none`
- Next sprint: `define after roadmap approval`
- Resume from: `review or generate roadmap from ./prd.md`
- Active blockers: `none`

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`

- [ ] Sprint 02 - Wire Runtime
  - Path: `./sprints/02-wire-runtime/sprint.md`
  - Goal: Wire runtime behavior
  - Depends on: `Sprint 01 - Define Contract`
  - Validation focus: Engine integration tests
  - Subtasks:
    - [ ] Implement runtime changes
  - Evidence folder: `./sprints/02-wire-runtime/evidence/`

- [ ] Final Audit - Confirm Completion
    - Path: `./sprints/03-final-audit/sprint.md`
    - Goal: Confirm initiative completeness
    - Depends on: `all prior implementation sprints`
    - Validation focus: Final initiative audit
    - Subtasks:
        - [ ] Confirm final closeout state
    - Evidence folder: `./sprints/03-final-audit/evidence/`

## Final Audit Step

1. Confirm completeness.
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`roadmap_ready: pass`"),
                encoding="utf-8",
            )
            self.assertFalse((initiative_root / "sprint-template").exists())

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "init-sprints", str(initiative_root)])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((initiative_root / "sprints" / "01-define-contract" / "sprint.md").exists())
            self.assertTrue((initiative_root / "sprints" / "01-define-contract" / "closeout.md").exists())
            self.assertTrue((initiative_root / "sprints" / "01-define-contract" / "evidence").exists())
            self.assertTrue((initiative_root / "sprints" / "02-wire-runtime" / "sprint.md").exists())
            self.assertTrue((initiative_root / "sprints" / "03-final-audit" / "sprint.md").exists())

            readme = (initiative_root / "README.md").read_text(encoding="utf-8")
            roadmap = roadmap_path.read_text(encoding="utf-8")
            self.assertIn("Roadmap approved, sprint initialization complete", readme)
            self.assertIn("Start Sprint 01 - Define Contract", readme)
            self.assertIn("`roadmap_ready: pass`", readme)
            self.assertIn("Status: generated", roadmap)
            self.assertIn(
                "- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template",
                roadmap,
            )
            self.assertIn("- Next sprint: `Sprint 01 - Define Contract`", roadmap)

    def test_init_sprints_blocks_until_roadmap_ready_gate_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [ ] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
    - Path: `./sprints/01-define-contract/sprint.md`
    - Goal: Define the contract
    - Depends on: `none`
    - Validation focus: Contract review
    - Subtasks:
        - [ ] Draft the contract
    - Evidence folder: `./sprints/01-define-contract/evidence/`
""",
                encoding="utf-8",
            )

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "init-sprints", str(initiative_root)])

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("roadmap is not ready", result.stderr)
            self.assertIn("`roadmap_ready: pass`", result.stderr)

    def test_archive_blocks_incomplete_initiatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [PYTHON_BIN, str(SCRIPT), "create", str(initiative_root), "--ops-root", str(ops_root)]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "archive", str(initiative_root), "--ops-root", str(ops_root)])

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("Archive blocked because the initiative is not complete", result.stderr)
            self.assertTrue(initiative_root.exists())

    def test_archive_moves_completed_initiative_and_syncs_root_readme(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "README.md").write_text(
                """# Initiative Status

## Snapshot

| Field | Value |
| ----- | ----- |
| Initiative | Parser Modernization |
| Imported on | 2026-04-02 |
| Current phase | Complete |
| Current gate | `initiative_complete: pass` |
| Roadmap status | `complete` |
| Active sprint | `none` |
| Last completed sprint | `Sprint 02 - Wire Runtime` |
| Next step | `none` |
| Blockers | `none` |

## Validation Pointers

Complete.
""",
                encoding="utf-8",
            )
            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: complete

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template
- [x] Sprint execution started
- [x] All sprint closeouts completed
- [x] Final audit completed as the last roadmap item
- [x] Follow-up audit or refactor decision recorded
- [x] `./retained-note.md` written
""",
                encoding="utf-8",
            )
            (initiative_root / "retained-note.md").write_text(
                """# Retained Note

## Outcome

Completed successfully.
""",
                encoding="utf-8",
            )

            result = run_cmd([PYTHON_BIN, str(SCRIPT), "archive", str(initiative_root), "--ops-root", str(ops_root)])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertFalse(initiative_root.exists())
            self.assertTrue((ops_root / "archive" / "2026-04-02-parser-modernization").exists())
            root_readme = (ops_root / "initiatives" / "README.md").read_text(encoding="utf-8")
            self.assertNotIn("`initiatives/2026-04-02-parser-modernization`", root_readme)

    def test_script_blocks_rerun_against_populated_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing-initiative"
            target.mkdir(parents=True, exist_ok=True)
            (target / "README.md").write_text("existing", encoding="utf-8")

            result = run_cmd([PYTHON_BIN, str(SCRIPT), str(target)])

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("already contains files", result.stderr)
            self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "existing")

    def test_dry_run_reports_without_writing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    "dry-run-initiative",
                    "--ops-root",
                    str(ops_root),
                    "--dry-run",
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("dry-run: operations root would be", result.stdout)
            self.assertFalse(ops_root.exists())

    def test_create_reports_placeholder_summary_for_generated_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / ".ub-workflows"

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    "my-new-initiative",
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-01",
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("placeholder summary:", result.stdout)
            self.assertIn("phase status: scaffold is valid for PRD authoring.", result.stdout)
            self.assertIn("prd.md", result.stdout)
            self.assertIn("roadmap.md", result.stdout)

    def test_create_spec_reports_phase_status_for_generated_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / ".ub-workflows"
            target = ops_root / "specs" / "2026-04-01-workflow-gap-note"

            result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create-spec",
                    "workflow-gap-note",
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-01",
                ]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((target / "spec.md").exists())
            self.assertIn(f"scaffolded lightweight spec at {target.resolve().as_posix()}", result.stdout)
            self.assertIn("phase status: scaffold is valid for spec authoring.", result.stdout)
            self.assertIn("placeholder summary:", result.stdout)

    def test_check_scaffold_placeholders_strict_fails_for_placeholder_only_sprint_shells(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            roadmap_path = initiative_root / "roadmap.md"
            roadmap_path.write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Current Position

- Current sprint: `none`
- Last completed sprint: `none`
- Next sprint: `define after roadmap approval`
- Resume from: `review or generate roadmap from ./prd.md`
- Active blockers: `none`

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`roadmap_ready: pass`"),
                encoding="utf-8",
            )

            init_result = run_cmd([PYTHON_BIN, str(SCRIPT), "init-sprints", str(initiative_root)])
            self.assertEqual(init_result.returncode, 0, msg=init_result.stdout + init_result.stderr)

            result = run_cmd([PYTHON_BIN, str(CHECK_SCRIPT), str(initiative_root), "--strict"])

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("sprints/01-define-contract/sprint.md", result.stdout)
            self.assertIn("REPLACE_SPRINT_TITLE", result.stdout)

    def test_prepare_sprints_strict_placeholders_passes_with_advisory_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Current Position

- Current sprint: `none`
- Last completed sprint: `none`
- Next sprint: `define after roadmap approval`
- Resume from: `review or generate roadmap from ./prd.md`
- Active blockers: `none`

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
    so every later sprint inherits one stable workflow baseline
  - Depends on: `none`
  - Validation focus: Contract review
    with lifecycle and gate consistency checks
  - Subtasks:
    - [ ] Draft the contract
      and capture the shared gate vocabulary
  - Evidence folder: `./sprints/01-define-contract/evidence/`

- [ ] Sprint 02 - Wire Runtime
  - Path: `./sprints/02-wire-runtime/sprint.md`
  - Goal: Wire runtime behavior
  - Depends on: `Sprint 01 - Define Contract`
  - Validation focus: Engine integration tests
  - Subtasks:
    - [ ] Implement runtime changes
  - Evidence folder: `./sprints/02-wire-runtime/evidence/`

## Final Audit Step

1. Confirm completeness.
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`roadmap_ready: pass`"),
                encoding="utf-8",
            )

            result = run_cmd(
                [PYTHON_BIN, str(SCRIPT), "prepare-sprints", str(initiative_root), "--strict-placeholders"]
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("placeholder summary:", result.stdout)
            self.assertIn("advisory", result.stdout)
            self.assertIn("PENDING_HANDOFF:", result.stdout)

    def test_prepare_sprints_fails_when_canonical_sprint_template_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: planned

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template

## Sprint Sequence

- [ ] Sprint 01 - Define Contract
  - Path: `./sprints/01-define-contract/sprint.md`
  - Goal: Define the contract
  - Depends on: `none`
  - Validation focus: Contract review
  - Subtasks:
    - [ ] Draft the contract
  - Evidence folder: `./sprints/01-define-contract/evidence/`
""",
                encoding="utf-8",
            )

            readme_path = initiative_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("`prd_ready: blocked`", "`roadmap_ready: pass`"),
                encoding="utf-8",
            )

            missing_template_root = Path(tmp) / "missing-sprint-template"
            with (
                mock.patch.object(SCRIPT_MODULE, "CANONICAL_SPRINT_TEMPLATE_ROOT", missing_template_root),
                self.assertRaisesRegex(ValueError, "Canonical `ub-workflow` sprint template is missing or invalid") as exc,
            ):
                SCRIPT_MODULE.command_prepare_sprints(
                    Namespace(
                        initiative_root=str(initiative_root),
                        strict_placeholders=False,
                        dry_run=False,
                    )
                )

            self.assertIn(missing_template_root.as_posix(), str(exc.exception))

    def test_placeholder_checker_ignores_code_examples_and_quoted_placeholder_prose(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ops_root = Path(tmp) / "ops"
            initiative_root = ops_root / "initiatives" / "2026-04-02-parser-modernization"

            create_result = run_cmd(
                [
                    PYTHON_BIN,
                    str(SCRIPT),
                    "create",
                    str(initiative_root),
                    "--ops-root",
                    str(ops_root),
                    "--date",
                    "2026-04-02",
                    "--initiative-name",
                    "Parser Modernization",
                ]
            )
            self.assertEqual(create_result.returncode, 0, msg=create_result.stdout + create_result.stderr)

            (initiative_root / "prd.md").write_text(
                """# Example PRD

## Example output

```text
Unresolved placeholders:
- REPLACE_OWNER (optional)
```

## Notes

Treat any `Replace with...` or `REPLACE_` string anywhere in the repository as an unconditional failure.
""",
                encoding="utf-8",
            )
            (initiative_root / "roadmap.md").write_text(
                """# Sprint Roadmap

Status: generated

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [x] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template
""",
                encoding="utf-8",
            )
            (initiative_root / "README.md").write_text(
                """# Initiative Status

## Snapshot

| Field | Value |
| ----- | ----- |
| Initiative | Parser Modernization |
| Current gate | `roadmap_ready: pass` |
""",
                encoding="utf-8",
            )

            result = run_cmd([PYTHON_BIN, str(CHECK_SCRIPT), str(initiative_root), "--strict"])

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("no unresolved generated-artifact placeholders", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
