#!/usr/bin/env python3
from __future__ import annotations


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
}
