#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StepSpec:
    name: str
    command: tuple[str, ...]
    allow_nonzero: bool = False


QUICK_CHECK_STEPS = (
    StepSpec("tool regression tests", ("{python}", "tools/test_workspace_tools.py")),
    StepSpec("workspace structure", ("{python}", "tools/check_workspace.py")),
    StepSpec("git readiness", ("{python}", "tools/audit_git_readiness.py")),
    StepSpec("line endings", ("{python}", "tools/audit_line_endings.py", "--strict")),
)

FULL_ONLY_STEPS = (
    StepSpec("git candidate summary", ("{python}", "tools/summarize_git_candidates.py", "--top", "8")),
    StepSpec("baseline report", ("{python}", "tools/prepare_baseline_report.py")),
    StepSpec("baseline freshness", ("{python}", "tools/verify_baseline_report.py")),
    StepSpec("workspace status", ("{python}", "tools/generate_workspace_status.py")),
    StepSpec("workspace status freshness", ("{python}", "tools/verify_workspace_status.py")),
    StepSpec(
        "strict large-file reminder",
        ("{python}", "tools/audit_git_readiness.py", "--max-mb", "1"),
        allow_nonzero=True,
    ),
)


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

TOOL_DESCRIPTIONS = {
    "tools/audit_git_readiness.py": "checks Git candidates for large files, sensitive names, and secret-like content.",
    "tools/audit_line_endings.py": "reports line ending drift against `.gitattributes` policy.",
    "tools/check_workspace.py": "checks required workspace structure, deliberately trackable optional task index quality, registry coverage, Git ignore behavior, and UTF-8 text readability.",
    "tools/generate_workspace_status.py": "regenerates this current-state summary.",
    "tools/make_task.py": "creates isolated task folders with safe defaults and `--dry-run`.",
    "tools/prepare_baseline_report.py": "writes the workspace baseline recommendation report.",
    "tools/prepare_first_commit_report.py": "legacy-compatible implementation behind the baseline report command.",
    "tools/run_workspace_maintenance.py": "runs the full maintenance chain.",
    "tools/summarize_git_candidates.py": "summarizes Git candidates by area, extension, and largest files.",
    "tools/test_workspace_tools.py": "runs lightweight regression tests for workspace tools.",
    "tools/verify_baseline_report.py": "verifies that the baseline recommendation matches current Git candidates.",
    "tools/verify_first_commit_report.py": "legacy-compatible implementation behind the baseline report verifier.",
    "tools/verify_workspace_status.py": "verifies that `WORKSPACE_STATUS.md` matches the current generated status.",
    "tools/workspace_manifest.py": "centralizes shared workspace tool metadata and maintenance command lists.",
    "tools/workspace.py": "provides the unified task creation and quick/full workspace check commands.",
}
