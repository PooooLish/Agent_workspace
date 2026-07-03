#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CORE_MAINTENANCE_COMMANDS = [
    "python tools/check_workspace.py",
    "python tools/audit_git_readiness.py",
    "python tools/audit_line_endings.py --strict",
    "python tools/test_workspace_tools.py",
    "python tools/summarize_git_candidates.py",
    "python tools/prepare_baseline_report.py",
    "python tools/verify_baseline_report.py",
    "python tools/generate_workspace_status.py",
    "python tools/verify_workspace_status.py",
    "python tools/run_workspace_maintenance.py",
]


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

    def test_tool_scripts_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.REQUIRED_ITEMS)
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_tool_script_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

    def test_registry_helper_reports_missing_coverage(self) -> None:
        warnings: list[str] = []
        self.check_workspace.check_registry_paths(
            ["tools/not_registered.py"],
            warnings,
            require_items=True,
            require_status=True,
            status_text="",
        )

        self.assertIn("tools/not_registered.py is not listed in REQUIRED_ITEMS", warnings)
        self.assertIn("tools/not_registered.py is not documented in WORKSPACE_STATUS.md", warnings)

    def test_skills_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.REQUIRED_ITEMS)
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_skill_main_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

        for relative_path in self.check_workspace.get_skill_resource_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, status_text)

    def test_sops_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.REQUIRED_ITEMS)
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_sop_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

    def test_prompts_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.REQUIRED_ITEMS)
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_prompt_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

    def test_envs_are_registered_and_documented(self) -> None:
        required_items = set(self.check_workspace.REQUIRED_ITEMS)
        status_text = (ROOT / "WORKSPACE_STATUS.md").read_text(encoding="utf-8")

        for relative_path in self.check_workspace.get_env_paths(ROOT):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, required_items)
                self.assertIn(relative_path, status_text)

    def test_core_maintenance_commands_are_in_docs(self) -> None:
        doc_texts = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "README.zh-CN.md": (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            "WORKSPACE_GUIDE.md": (ROOT / "WORKSPACE_GUIDE.md").read_text(encoding="utf-8"),
            "WORKSPACE_GUIDE.zh-CN.md": (ROOT / "WORKSPACE_GUIDE.zh-CN.md").read_text(encoding="utf-8"),
        }

        for filename, text in doc_texts.items():
            for command in CORE_MAINTENANCE_COMMANDS:
                with self.subTest(filename=filename, command=command):
                    self.assertIn(command, text)

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

    def test_status_generator_has_tool_descriptions(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        described_tools = set(generator.TOOL_DESCRIPTIONS)
        actual_tools = {
            str(path.relative_to(ROOT)).replace("\\", "/")
            for path in (ROOT / "tools").glob("*.py")
        }

        self.assertEqual(actual_tools, described_tools)


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
