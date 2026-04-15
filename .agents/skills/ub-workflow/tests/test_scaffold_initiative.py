from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
SCRIPT = PROJECT_ROOT / ".agents" / "skills" / "ub-workflow" / "scripts" / "scaffold_initiative.py"
PYTHON_BIN = sys.executable


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
            self.assertTrue((target / "sprint-template" / "sprint.md").exists())

            root_readme = (ops_root / "initiatives" / "README.md").read_text(encoding="utf-8")
            readme = (target / "README.md").read_text(encoding="utf-8")
            roadmap = (target / "roadmap.md").read_text(encoding="utf-8")

            self.assertIn("`initiatives/2026-04-01-my-new-initiative`", root_readme)
            self.assertIn("My New Initiative", readme)
            self.assertIn("2026-04-01", readme)
            self.assertIn("Template scaffolded, awaiting PRD import", readme)
            self.assertIn("`prd_ready: blocked`", readme)
            self.assertIn("unassigned", readme)
            self.assertIn("Master PRD imported into `./prd.md`", roadmap)
            self.assertIn("- Next sprint: `define after roadmap approval`", roadmap)

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
            self.assertIn("PRD copied, awaiting review and roadmap planning", readme)
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
            self.assertIn("PRD imported, awaiting roadmap planning", readme)
            self.assertIn("`prd_ready: pass`", readme)

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
- [ ] All sprint folders initialized under `./sprints/` from `./sprint-template/`

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
            self.assertIn("- [x] All sprint folders initialized under `./sprints/` from `./sprint-template/`", roadmap)
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
- [ ] All sprint folders initialized under `./sprints/` from `./sprint-template/`

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
- [x] All sprint folders initialized under `./sprints/` from `./sprint-template/`
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
