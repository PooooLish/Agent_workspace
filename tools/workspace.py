#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Callable, Sequence

from workspace_manifest import FULL_ONLY_STEPS, QUICK_CHECK_STEPS, StepSpec


FULL_CHECK_STEPS = QUICK_CHECK_STEPS + FULL_ONLY_STEPS
Runner = Callable[..., subprocess.CompletedProcess[str]]


def resolve_command(command: tuple[str, ...]) -> list[str]:
    return [sys.executable if part == "{python}" else part for part in command]


def run_steps(
    root: Path,
    steps: Sequence[StepSpec],
    *,
    runner: Runner = subprocess.run,
) -> int:
    for step in steps:
        command = resolve_command(step.command)
        print(f"\n== {step.name} ==", flush=True)
        print(" ".join(command), flush=True)
        result = runner(
            command,
            cwd=root,
            check=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            stderr=subprocess.STDOUT,
        )
        if result.returncode == 0:
            continue
        if step.allow_nonzero:
            print(f"Reminder step returned exit {result.returncode}; review output above.", flush=True)
            continue
        print(f"Step failed: {step.name} (exit {result.returncode})", flush=True)
        return result.returncode
    return 0


def run_checks(root: Path, *, full: bool) -> int:
    steps = FULL_CHECK_STEPS if full else QUICK_CHECK_STEPS
    code = run_steps(root, steps)
    if code == 0:
        mode = "Full" if full else "Quick"
        print(f"\n{mode} workspace checks completed.", flush=True)
    return code


def run_new(root: Path, task_name: str, *, dry_run: bool) -> int:
    command = [sys.executable, "tools/make_task.py", task_name]
    if dry_run:
        command.append("--dry-run")
    return subprocess.run(command, cwd=root, check=False).returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create tasks and check the agent workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="create a private task scaffold")
    new_parser.add_argument("task_name")
    new_parser.add_argument("--dry-run", action="store_true")

    check_parser = subparsers.add_parser("check", help="run workspace checks")
    check_parser.add_argument("--full", action="store_true", help="generate and verify maintenance reports")
    return parser


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    args = build_parser().parse_args()
    if args.command == "new":
        return run_new(root, args.task_name, dry_run=args.dry_run)
    return run_checks(root, full=args.full)


if __name__ == "__main__":
    raise SystemExit(main())
