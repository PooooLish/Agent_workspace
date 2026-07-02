#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Step:
    name: str
    command: list[str]
    allow_nonzero: bool = False


STEPS = [
    Step("workspace status bootstrap", ["python", "tools/generate_workspace_status.py"]),
    Step("tool regression tests", ["python", "tools/test_workspace_tools.py"]),
    Step("workspace structure", ["python", "tools/check_workspace.py"]),
    Step("git readiness", ["python", "tools/audit_git_readiness.py"]),
    Step("git candidate summary", ["python", "tools/summarize_git_candidates.py", "--top", "8"]),
    Step("baseline report", ["python", "tools/prepare_baseline_report.py"]),
    Step("baseline report freshness", ["python", "tools/verify_baseline_report.py"]),
    Step("workspace status", ["python", "tools/generate_workspace_status.py"]),
    Step("workspace status freshness", ["python", "tools/verify_workspace_status.py"]),
    Step("line ending audit", ["python", "tools/audit_line_endings.py"]),
    Step("strict large-file reminder", ["python", "tools/audit_git_readiness.py", "--max-mb", "1"], allow_nonzero=True),
]


def run_step(root: Path, step: Step) -> int:
    print(f"\n== {step.name} ==", flush=True)
    print(" ".join(step.command), flush=True)
    result = subprocess.run(
        step.command,
        cwd=root,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0 and not step.allow_nonzero:
        print(f"Step failed: {step.name} (exit {result.returncode})", flush=True)
        return result.returncode
    if result.returncode != 0 and step.allow_nonzero:
        print(f"Reminder step returned exit {result.returncode}; review output above.", flush=True)
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    for step in STEPS:
        code = run_step(root, step)
        if code:
            return code

    print("\nMaintenance checks completed.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
