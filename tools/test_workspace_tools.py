#!/usr/bin/env python3
from __future__ import annotations

import io
import importlib.util
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from workspace_manifest import CORE_MAINTENANCE_COMMANDS, TASK_LIFECYCLE_COMMANDS


ROOT = Path(__file__).resolve().parents[1]


def load_tool(name: str):
    path = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load tool module: {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MakeTaskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.make_task = load_tool("make_task")

    def test_task_name_validation(self) -> None:
        valid = ["task1", "task_name", "task-name_123"]
        invalid = ["", "../escape", "bad/name", "-starts-with-dash", "has space"]

        for name in valid:
            with self.subTest(name=name):
                self.assertRegex(name, self.make_task.TASK_NAME_RE)

        for name in invalid:
            with self.subTest(name=name):
                self.assertNotRegex(name, self.make_task.TASK_NAME_RE)

    def test_dry_run_does_not_create_task(self) -> None:
        task_name = "dry_run_regression_task"
        task_path = ROOT / "tasks" / task_name
        self.assertFalse(task_path.exists(), "test precondition failed; task path already exists")

        result = subprocess.run(
            ["python", "tools/make_task.py", task_name, "--dry-run"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry run:", result.stdout)
        self.assertFalse(task_path.exists(), "dry-run unexpectedly created a task folder")

    def test_task_template_contains_handoff_sections(self) -> None:
        text = self.make_task.build_task_md("example", "standard")
        for heading in (
            "## Status",
            "## Complexity",
            "## Phase",
            "## Goal",
            "## Non-goals",
            "## Acceptance criteria",
            "## Verification commands",
            "## Decisions",
            "## Progress",
            "## Next action",
            "## Blockers",
        ):
            self.assertIn(heading, text)
        self.assertIn("planning", text)
        self.assertIn("standard", text)

    def test_complex_scaffold_adds_planning_and_coordination_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tasks").mkdir()

            created, _ = self.make_task.scaffold_task(root, "example", complexity="complex")

            planning = root / "tasks" / "example" / "docs" / "superpowers" / "README.md"
            contract = root / "tasks" / "example" / "coordination" / "contract.md"
            self.assertIn(str(planning), created)
            self.assertIn(str(contract), created)
            self.assertTrue(planning.is_file())
            self.assertTrue(contract.is_file())

    def test_simple_scaffold_does_not_add_planning_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tasks").mkdir()

            self.make_task.scaffold_task(root, "example", complexity="simple")

            task_root = root / "tasks" / "example"
            self.assertFalse((task_root / "docs" / "superpowers").exists())
            self.assertFalse((task_root / "coordination").exists())

    def test_scaffold_creates_summary_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tasks").mkdir()

            created, skipped = self.make_task.scaffold_task(root, "example")

            self.assertFalse(skipped)
            summary_path = root / "tasks" / "example" / "summary.md"
            self.assertIn(str(summary_path), created)
            summary = summary_path.read_text(encoding="utf-8")
            for heading in ("## Goal", "## Outcome", "## Changes", "## Verification", "## Open issues"):
                self.assertIn(heading, summary)

    def test_scaffold_rejects_invalid_task_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tasks").mkdir()
            for task_name in ("parent/child", "../escape", "has space"):
                with self.subTest(task_name=task_name):
                    with self.assertRaises(ValueError):
                        self.make_task.scaffold_task(root, task_name)

    def test_scaffold_rejects_invalid_complexity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tasks").mkdir()

            with self.assertRaises(ValueError):
                self.make_task.scaffold_task(root, "example", complexity="huge")


class TaskLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lifecycle = load_tool("task_lifecycle")

    def write_task(
        self,
        root: Path,
        name: str = "example",
        *,
        status: str = "active",
        complexity: str = "standard",
        phase: str = "implementation",
        summary_complete: bool = True,
    ) -> Path:
        task_root = root / "tasks" / name
        task_root.mkdir(parents=True)
        task_root.joinpath("task.md").write_text(
            f"""# Task: {name}

## Status

{status}

## Complexity

{complexity}

## Phase

{phase}

## Goal

Deliver the feature.

## Non-goals

No unrelated refactor.

## Constraints

- Stay local.

## Inputs

- Existing source.

## Acceptance criteria

- The command succeeds.

## Verification commands

```powershell
python -c "print('verified')"
```

## Decisions

- Keep Markdown as state.

## Progress

- Parser designed.

## Next action

Implement the command.

## Blockers

None
""",
            encoding="utf-8",
        )
        if summary_complete:
            summary = """# Summary: example

## Goal

Deliver the feature.

## Outcome

Feature delivered.

## Changes

Added lifecycle commands.

## Verification

Tests passed.

## Open issues

None.
"""
        else:
            summary = "# Summary: example\n\n## Goal\n\n## Outcome\n"
        task_root.joinpath("summary.md").write_text(summary, encoding="utf-8")
        return task_root

    def test_load_task_parses_lifecycle_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_task(root)

            task = self.lifecycle.load_task(root, "example")

            self.assertEqual(task.status, "active")
            self.assertEqual(task.complexity, "standard")
            self.assertEqual(task.phase, "implementation")
            self.assertEqual(task.next_action, "Implement the command.")
            self.assertEqual(task.verification_commands, ('python -c "print(\'verified\')"',))

    def test_markdown_headings_inside_fences_do_not_replace_task_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root)
            task_path = task_root / "task.md"
            task_path.write_text(
                task_path.read_text(encoding="utf-8").replace(
                    'python -c "print(\'verified\')"',
                    "## Status\npython -c \"print('verified')\"",
                ),
                encoding="utf-8",
            )

            task = self.lifecycle.load_task(root, "example")

            self.assertEqual(task.status, "active")
            self.assertEqual(task.verification_commands, ('python -c "print(\'verified\')"',))

    def test_duplicate_lifecycle_heading_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root)
            task_path = task_root / "task.md"
            task_path.write_text(
                task_path.read_text(encoding="utf-8") + "\n## Status\n\nblocked\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "duplicate section"):
                self.lifecycle.load_task(root, "example")

    def test_legacy_task_defaults_are_compatible_with_close(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root)
            task_path = task_root / "task.md"
            legacy = task_path.read_text(encoding="utf-8")
            legacy = legacy.replace("## Complexity\n\nstandard\n\n", "")
            legacy = legacy.replace("## Phase\n\nimplementation\n\n", "")
            task_path.write_text(legacy, encoding="utf-8")

            task = self.lifecycle.load_task(root, "example")

            self.assertEqual(task.complexity, "standard")
            self.assertEqual(task.phase, "implementation")
            self.assertEqual(self.lifecycle.diagnose_task(task), [])
            self.lifecycle.close_task(task)
            closed = task_path.read_text(encoding="utf-8")
            self.assertIn("## Complexity\n\nstandard", closed)
            self.assertIn("## Phase\n\ncompleted", closed)

    def test_resume_packet_contains_only_durable_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_task(root)

            packet = self.lifecycle.build_resume_packet(self.lifecycle.load_task(root, "example"))

            for text in (
                "Status: active",
                "Complexity: standard",
                "Goal",
                "Decisions",
                "Progress",
                "Next action",
                "Blockers",
                "python -c",
            ):
                self.assertIn(text, packet)

    def test_doctor_reports_incomplete_task_and_complex_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root, complexity="complex")
            task_root.joinpath("task.md").write_text(
                task_root.joinpath("task.md").read_text(encoding="utf-8").replace(
                    "Implement the command.", "Describe the single next useful action."
                ),
                encoding="utf-8",
            )

            findings = self.lifecycle.diagnose_task(self.lifecycle.load_task(root, "example"))

            self.assertTrue(any("Next action" in finding for finding in findings))
            self.assertTrue(any("coordination/contract.md" in finding for finding in findings))

    def test_doctor_rejects_planning_artifacts_for_simple_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root, complexity="simple")
            planning_root = task_root / "docs" / "superpowers"
            planning_root.mkdir(parents=True)
            planning_root.joinpath("plan.md").write_text("# Plan\n", encoding="utf-8")

            findings = self.lifecycle.diagnose_task(self.lifecycle.load_task(root, "example"))

            self.assertTrue(any("simple task" in finding for finding in findings))

    def test_doctor_validates_complex_coordination_contract_columns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root, complexity="complex")
            (task_root / "docs" / "superpowers").mkdir(parents=True)
            contract = task_root / "coordination" / "contract.md"
            contract.parent.mkdir()
            contract.write_text("# Contract\n\n| ID | Owner |\n", encoding="utf-8")

            findings = self.lifecycle.diagnose_task(self.lifecycle.load_task(root, "example"))

            self.assertTrue(any("missing columns" in finding for finding in findings))

    def test_doctor_accepts_valid_complex_coordination_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root, complexity="complex")
            (task_root / "docs" / "superpowers").mkdir(parents=True)
            contract = task_root / "coordination" / "contract.md"
            contract.parent.mkdir()
            contract.write_text(
                """# Contract

| ID | Dependencies | Owner | Worktree | Allowed paths | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | None | agent-a | wt-a | src/a.py | python tests/a.py | in_progress |
| T2 | T1 | agent-b | wt-b | src/a.py | python tests/b.py | pending |
""",
                encoding="utf-8",
            )

            findings = self.lifecycle.diagnose_task(self.lifecycle.load_task(root, "example"))

            self.assertEqual(findings, [])

            with self.assertRaisesRegex(ValueError, "unfinished coordination rows"):
                self.lifecycle.close_task(self.lifecycle.load_task(root, "example"))

    def test_doctor_rejects_unsafe_or_conflicting_coordination_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root, complexity="complex")
            (task_root / "docs" / "superpowers").mkdir(parents=True)
            contract = task_root / "coordination" / "contract.md"
            contract.parent.mkdir()
            contract.write_text(
                """# Contract

| ID | Dependencies | Owner | Worktree | Allowed paths | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | T2 | agent-a | wt-a | ../outside.py | test-a | running |
| T1 | Missing | agent-b | wt-b | src/shared.py | test-b | pending |
| T2 | T1 | agent-c | wt-c | src/shared.py | test-c | pending |
""",
                encoding="utf-8",
            )

            findings = self.lifecycle.diagnose_task(self.lifecycle.load_task(root, "example"))
            joined = "\n".join(findings)

            self.assertIn("duplicate ID", joined)
            self.assertIn("unknown dependency", joined)
            self.assertIn("unsafe Allowed paths", joined)
            self.assertIn("invalid Status", joined)
            self.assertIn("dependency cycle", joined)

    def test_verify_is_read_only_without_run_flag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_task(root)
            calls: list[tuple[str, Path]] = []

            with redirect_stdout(io.StringIO()):
                code = self.lifecycle.verify_task(
                    self.lifecycle.load_task(root, "example"),
                    run=False,
                    command_runner=lambda command, cwd: calls.append((command, cwd)) or 0,
                )

            self.assertEqual(code, 0)
            self.assertEqual(calls, [])

    def test_verify_runs_commands_in_task_and_stops_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root)
            calls: list[tuple[str, Path]] = []

            def runner(command: str, cwd: Path) -> int:
                calls.append((command, cwd))
                return 5

            with redirect_stdout(io.StringIO()):
                code = self.lifecycle.verify_task(
                    self.lifecycle.load_task(root, "example"),
                    run=True,
                    command_runner=runner,
                )

            self.assertEqual(code, 5)
            self.assertEqual(calls, [('python -c "print(\'verified\')"', task_root)])

    def test_default_command_runner_executes_one_line_in_selected_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            code = self.lifecycle.default_command_runner(
                'python -c "import os; raise SystemExit(0 if os.getcwd() else 1)"',
                Path(directory),
            )

            self.assertEqual(code, 0)

    def test_close_requires_complete_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_task(root, summary_complete=False)
            task = self.lifecycle.load_task(root, "example")

            with self.assertRaises(ValueError):
                self.lifecycle.close_task(task)

    def test_close_marks_task_completed_without_archiving(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_root = self.write_task(root)

            self.lifecycle.close_task(self.lifecycle.load_task(root, "example"))

            text = task_root.joinpath("task.md").read_text(encoding="utf-8")
            self.assertIn("## Status\n\ncompleted", text)
            self.assertIn("## Phase\n\ncompleted", text)
            self.assertIn("## Next action\n\nNone", text)
            self.assertTrue(task_root.is_dir())


class GitReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = load_tool("audit_git_readiness")

    def test_credential_name_filter(self) -> None:
        self.assertTrue(self.audit.is_credential_name("OPENAI_API_KEY"))
        self.assertTrue(self.audit.is_credential_name("AUTH_TOKEN"))
        self.assertTrue(self.audit.is_credential_name("password"))
        self.assertFalse(self.audit.is_credential_name("tokenizer"))
        self.assertFalse(self.audit.is_credential_name("next_token"))
        self.assertFalse(self.audit.is_credential_name("token"))


class LineEndingAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = load_tool("audit_line_endings")

    def test_expected_line_ending_policy(self) -> None:
        self.assertEqual(self.audit.expected_line_ending("README.md"), "lf")
        self.assertEqual(self.audit.expected_line_ending("tools/check_workspace.py"), "lf")
        self.assertEqual(self.audit.expected_line_ending("scripts/build.ps1"), "crlf")
        self.assertIsNone(self.audit.expected_line_ending("tasks/private_example/assets/logo.png"))

    def test_normalize_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf_path = root / "README.md"
            crlf_path = root / "script.ps1"
            lf_path.write_bytes(b"one\r\ntwo\r\n")
            crlf_path.write_bytes(b"one\ntwo\n")

            changed = self.audit.normalize_line_endings(root, ["README.md"], ["script.ps1"])

            self.assertEqual(changed, 2)
            self.assertEqual(lf_path.read_bytes(), b"one\ntwo\n")
            self.assertEqual(crlf_path.read_bytes(), b"one\r\ntwo\r\n")


class CheckWorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.check_workspace = load_tool("check_workspace")

    def test_utf8_candidate_filter(self) -> None:
        self.assertTrue(self.check_workspace.is_utf8_candidate("README.zh-CN.md"))
        self.assertTrue(self.check_workspace.is_utf8_candidate("tools/check_workspace.py"))
        self.assertTrue(self.check_workspace.is_utf8_candidate(".gitattributes"))
        self.assertFalse(self.check_workspace.is_utf8_candidate("tasks/private_example/assets/logo.png"))
        self.assertFalse(self.check_workspace.is_utf8_candidate("archives/sample.zip"))

    def test_required_ignored_paths_are_ignored(self) -> None:
        for relative_path in self.check_workspace.REQUIRED_IGNORED_PATHS:
            with self.subTest(relative_path=relative_path):
                self.assertTrue(self.check_workspace.is_git_ignored(ROOT, relative_path))

    def test_task_folders_are_private_by_default(self) -> None:
        self.assertTrue(self.check_workspace.is_git_ignored(ROOT, "tasks/private_example/AGENTS.md"))
        self.assertFalse(self.check_workspace.is_git_ignored(ROOT, "tasks/README.md"))

    def test_sandboxes_are_private_by_default(self) -> None:
        self.assertTrue(self.check_workspace.is_git_ignored(ROOT, "sandboxes/private_example/test.txt"))
        self.assertFalse(self.check_workspace.is_git_ignored(ROOT, "sandboxes/README.md"))

    def test_archives_are_private_by_default(self) -> None:
        self.assertTrue(self.check_workspace.is_git_ignored(ROOT, "archives/private_example/summary.md"))
        self.assertFalse(self.check_workspace.is_git_ignored(ROOT, "archives/README.md"))

    def test_superpowers_runtime_state_is_ignored(self) -> None:
        self.assertTrue(self.check_workspace.is_git_ignored(ROOT, ".superpowers/sdd/progress.md"))

    def test_root_superpowers_docs_are_ignored(self) -> None:
        self.assertTrue(
            self.check_workspace.is_git_ignored(ROOT, "docs/superpowers/specs/example-design.md")
        )

    def test_planning_artifact_gate_is_documented(self) -> None:
        warnings: list[str] = []
        self.check_workspace.check_planning_artifact_gate(ROOT, warnings)
        self.assertEqual(warnings, [])

    def test_publication_docs_require_independent_repository(self) -> None:
        docs = [
            "README.md",
            "WORKSPACE_GUIDE.md",
            "tasks/README.md",
            "sops/git_first_commit.md",
            "sops/publish_independent_task.md",
        ]
        forbidden = (
            "narrow Git ignore exception",
            "narrow ignore-rule exception",
            "精确的 Git 例外",
            "单独加入版本库",
            "窄范围例外",
        )
        for relative_path in docs:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(relative_path=relative_path):
                self.assertTrue("independent" in text.lower() or "独立 Git 仓库" in text)
                for phrase in forbidden:
                    self.assertNotIn(phrase, text)

    def test_tracked_private_content_is_rejected(self) -> None:
        paths = [
            "tasks/README.md",
            "tasks/private/source.py",
            "sandboxes/README.md",
            "sandboxes/demo/result.txt",
            "archives/README.md",
            "archives/old/summary.md",
            "docs/superpowers/specs/root-noise.md",
        ]
        self.assertEqual(
            self.check_workspace.unexpected_tracked_private_paths(paths),
            [
                "archives/old/summary.md",
                "docs/superpowers/specs/root-noise.md",
                "sandboxes/demo/result.txt",
                "tasks/private/source.py",
            ],
        )
        self.assertEqual(self.check_workspace.get_tracked_private_paths(ROOT), [])

    def test_tool_scripts_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.required_items(ROOT))
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_tool_script_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

    def test_registry_helper_reports_missing_coverage(self) -> None:
        warnings: list[str] = []
        self.check_workspace.check_registry_paths(
            ROOT,
            ["tools/not_registered.py"],
            warnings,
            require_items=True,
            require_status=True,
            status_text="",
        )

        self.assertIn("tools/not_registered.py is not listed in REQUIRED_ITEMS", warnings)
        self.assertIn("tools/not_registered.py is not documented in WORKSPACE_STATUS.md", warnings)

    def test_skills_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.required_items(ROOT))
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_skill_main_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

        for relative_path in self.check_workspace.get_skill_resource_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, status_text)

    def test_sops_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.required_items(ROOT))
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_sop_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

    def test_prompts_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.required_items(ROOT))
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_prompt_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

    def test_envs_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.required_items(ROOT))
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_env_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

    def test_core_maintenance_commands_are_in_docs(self) -> None:
        doc_texts = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "WORKSPACE_GUIDE.md": (ROOT / "WORKSPACE_GUIDE.md").read_text(encoding="utf-8"),
        }

        for filename, text in doc_texts.items():
            for command in CORE_MAINTENANCE_COMMANDS:
                with self.subTest(filename=filename, command=command):
                    self.assertIn(command, text)

    def test_task_lifecycle_commands_are_in_docs(self) -> None:
        doc_texts = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "WORKSPACE_GUIDE.md": (ROOT / "WORKSPACE_GUIDE.md").read_text(encoding="utf-8"),
            "docs/framework/task-lifecycle.md": (
                ROOT / "docs" / "framework" / "task-lifecycle.md"
            ).read_text(encoding="utf-8"),
        }

        for filename, text in doc_texts.items():
            for command in TASK_LIFECYCLE_COMMANDS:
                with self.subTest(filename=filename, command=command):
                    self.assertIn(command, text)

    def test_task_verification_safety_and_ci_matrix_are_documented(self) -> None:
        lifecycle = (ROOT / "docs" / "framework" / "task-lifecycle.md").read_text(
            encoding="utf-8"
        )
        workflow = (ROOT / ".github" / "workflows" / "workspace-check.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("does not provide a sandbox", lifecycle)
        self.assertIn("one command per line", lifecycle)
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("windows-latest", workflow)

    def test_ignored_private_task_index_is_inactive(self) -> None:
        self.assertFalse(self.check_workspace.private_task_index_is_active(ROOT))

    def test_private_task_index_quality_inputs(self) -> None:
        index_path = ROOT / self.check_workspace.OPTIONAL_PRIVATE_TASK_INDEX
        if not self.check_workspace.private_task_index_is_active(ROOT):
            return

        index_text = index_path.read_text(encoding="utf-8")
        current_rows = self.check_workspace.parse_task_table(
            self.check_workspace.get_markdown_section(index_text, "Current Tasks")
        )
        cleanup_rows = self.check_workspace.parse_task_table(
            self.check_workspace.get_markdown_section(index_text, "Pending Cleanup")
        )

        current_tasks = {self.check_workspace.task_name_from_cell(row[0]) for row in current_rows}
        cleanup_tasks = {self.check_workspace.task_name_from_cell(row[0]) for row in cleanup_rows}

        for task_name in current_tasks:
            with self.subTest(task_name=task_name):
                self.assertTrue((ROOT / "tasks" / task_name).is_dir())
        for task_name in cleanup_tasks:
            with self.subTest(task_name=task_name):
                self.assertTrue(self.check_workspace.is_git_ignored(ROOT, f"tasks/{task_name}/AGENTS.md"))


class WorkspaceStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.verify_status = load_tool("verify_workspace_status")

    def test_status_verifier_loads_generator(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        status = generator.build_status(ROOT)

        self.assertIn("# Workspace Status", status)
        self.assertIn("## Current Health", status)

    def test_status_generator_lists_all_tool_scripts(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        status = generator.build_status(ROOT)

        for path in sorted((ROOT / "tools").glob("*.py")):
            relative_path = str(path.relative_to(ROOT)).replace("\\", "/")
            with self.subTest(relative_path=relative_path):
                self.assertIn(f"- `{relative_path}`:", status)

    def test_status_generator_lists_framework_docs(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        status = generator.build_status(ROOT)

        for item in generator.framework_doc_items(ROOT):
            with self.subTest(item=item):
                self.assertIn(item, status)
        self.assertIn("root Superpowers document path ignored by Git: yes", status)

    def test_status_generator_has_tool_descriptions(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        described_tools = set(generator.TOOL_DESCRIPTIONS)
        actual_tools = {
            str(path.relative_to(ROOT)).replace("\\", "/")
            for path in (ROOT / "tools").glob("*.py")
        }

        self.assertEqual(actual_tools, described_tools)

    def test_status_generator_uses_independent_task_publication(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        status = generator.build_status(ROOT)

        self.assertIn("separate Git repository", status)
        self.assertNotIn("narrow ignore-rule exception", status)

    def test_status_omits_volatile_local_metrics(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        status = generator.build_status(ROOT)
        for phrase in (
            "Last generated:",
            "Git candidate files:",
            "Git candidate size:",
            "Line ending drift reminders:",
            "large-file reminders:",
        ):
            self.assertNotIn(phrase, status)

    def test_status_documents_archive_privacy(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        status = generator.build_status(ROOT)

        self.assertIn("archives/README.md", status)
        self.assertIn("archived task path ignored by Git: yes", status)

    def test_status_build_is_deterministic(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)

        first = generator.build_status(ROOT)
        second = generator.build_status(ROOT)

        self.assertEqual(first, second)
        self.assertEqual(first, (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8"))


class WorkspaceCommandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = load_tool("workspace")

    def test_quick_checks_are_read_only(self) -> None:
        commands = [step.command for step in self.workspace.QUICK_CHECK_STEPS]
        flattened = [part for command in commands for part in command]
        self.assertNotIn("tools/generate_workspace_status.py", flattened)
        self.assertNotIn("tools/prepare_baseline_report.py", flattened)

    def test_full_checks_generate_and_verify_reports(self) -> None:
        scripts = [step.command[1] for step in self.workspace.FULL_CHECK_STEPS if len(step.command) > 1]
        self.assertIn("tools/prepare_baseline_report.py", scripts)
        self.assertIn("tools/verify_baseline_report.py", scripts)
        self.assertIn("tools/generate_workspace_status.py", scripts)
        self.assertIn("tools/verify_workspace_status.py", scripts)

    def test_run_steps_propagates_failure(self) -> None:
        calls: list[list[str]] = []

        def runner(command, **kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(command, 7)

        with redirect_stdout(io.StringIO()):
            code = self.workspace.run_steps(ROOT, self.workspace.QUICK_CHECK_STEPS[:1], runner=runner)

        self.assertEqual(code, 7)
        self.assertEqual(len(calls), 1)

    def test_reminder_failure_does_not_stop_later_steps(self) -> None:
        steps = (
            self.workspace.StepSpec("reminder", ("{python}", "reminder.py"), allow_nonzero=True),
            self.workspace.StepSpec("required", ("{python}", "required.py")),
        )
        return_codes = iter((3, 0))
        calls: list[list[str]] = []

        def runner(command, **kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(command, next(return_codes))

        with redirect_stdout(io.StringIO()):
            code = self.workspace.run_steps(ROOT, steps, runner=runner)

        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 2)

    def test_parser_exposes_lifecycle_commands(self) -> None:
        parser = self.workspace.build_parser()

        self.assertEqual(parser.parse_args(["status"]).command, "status")
        self.assertEqual(parser.parse_args(["resume", "demo"]).task_name, "demo")
        self.assertEqual(parser.parse_args(["doctor", "demo"]).task_name, "demo")
        self.assertFalse(parser.parse_args(["verify", "demo"]).run)
        self.assertTrue(parser.parse_args(["verify", "demo", "--run"]).run)
        self.assertEqual(parser.parse_args(["close", "demo"]).task_name, "demo")
        self.assertEqual(
            parser.parse_args(["new", "demo", "--complexity", "complex"]).complexity,
            "complex",
        )


class FirstCommitVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.verify_report = load_tool("verify_baseline_report")

    def test_normalize_generated_line(self) -> None:
        original = "# Report\n\nGenerated: 2026-07-02 10:00:00\n\nBody"
        expected = "# Report\n\nGenerated: <ignored>\n\nBody"
        self.assertEqual(self.verify_report.normalize_generated_line(original), expected)

    def test_report_verifier_loads_generator(self) -> None:
        generator = self.verify_report.load_report_generator(ROOT)
        report = generator.build_report(ROOT, generator.candidate_files(ROOT))

        self.assertIn("# Workspace Baseline Recommendation", report)
        self.assertIn("## Summary", report)


class FirstCommitReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = load_tool("prepare_baseline_report").load_legacy_report_tool(ROOT)

    def test_confirmed_public_assets(self) -> None:
        self.assertFalse(self.report.is_confirmed_asset("tasks/private_example/docs/public/logo.png"))
        self.assertFalse(self.report.is_confirmed_asset("tasks/private_example/docs/public/content-index.json"))
        self.assertFalse(self.report.is_confirmed_asset("tasks/private_example/package.json"))

    def test_no_current_review_suffixes(self) -> None:
        self.assertFalse(self.report.needs_review("envs/opencode.md"))
        self.assertFalse(self.report.needs_review("tasks/private_example/docs/public/logo.png"))


if __name__ == "__main__":
    raise SystemExit(unittest.main(verbosity=2))
