#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from datetime import date
from pathlib import Path

from workspace_manifest import CORE_MAINTENANCE_COMMANDS, TOOL_DESCRIPTIONS


def run_command(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def run_python_tool(root: Path, script: str, extra_args: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    return run_command(root, ["python", script, *(extra_args or [])])


def git_candidate_files(root: Path) -> list[Path]:
    result = run_command(root, ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")

    files: list[Path] = []
    for raw in result.stdout.split("\0"):
        if not raw:
            continue
        path = root / raw
        if path.is_file():
            files.append(path)
    return files


def extract_int(pattern: str, text: str, default: int = 0) -> int:
    match = re.search(pattern, text)
    if not match:
        return default
    return int(match.group(1))


def extract_float(pattern: str, text: str, default: float = 0.0) -> float:
    match = re.search(pattern, text)
    if not match:
        return default
    return float(match.group(1))


def is_ignored(root: Path, path: str) -> bool:
    result = run_command(root, ["git", "check-ignore", "-q", "--", path])
    return result.returncode == 0


def markdown_file_items(root: Path, directory: str) -> list[str]:
    return [f"- `{directory}/{path.name}`" for path in sorted((root / directory).glob("*.md"))]


def skill_file_items(root: Path) -> list[str]:
    return [
        f"- `{str(path.relative_to(root)).replace(chr(92), '/')}`"
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file()
    ]


def tool_file_items(root: Path) -> list[str]:
    items: list[str] = []
    for path in sorted((root / "tools").glob("*.py")):
        relative_path = str(path.relative_to(root)).replace("\\", "/")
        description = TOOL_DESCRIPTIONS.get(relative_path, "workspace helper script.")
        items.append(f"- `{relative_path}`: {description}")
    return items


def build_status(root: Path) -> str:
    check = run_python_tool(root, "tools/check_workspace.py")
    audit = run_python_tool(root, "tools/audit_git_readiness.py")
    line_endings = run_python_tool(root, "tools/audit_line_endings.py")
    strict_audit = run_python_tool(root, "tools/audit_git_readiness.py", ["--max-mb", "1"])

    files = git_candidate_files(root)
    total_size = sum(path.stat().st_size for path in files) / (1024 * 1024)

    report_path = root / "outputs" / "first_commit_recommendation.md"
    report_text = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
    recommended = extract_int(r"Recommended baseline files: (\d+)", report_text)
    manual = extract_int(r"Needs manual confirmation: (\d+)", report_text)
    confirmed_assets = extract_int(r"Confirmed public/site assets included: (\d+)", report_text)

    strict_large = extract_int(r"Summary: (\d+) large file\(s\)", strict_audit.stdout)
    line_ending_drift = extract_int(r"Summary: (\d+) line ending drift reminder\(s\)", line_endings.stdout)

    task_folder_ignored = is_ignored(root, "tasks/private_example/AGENTS.md")
    task_placeholder_ignored = is_ignored(root, "tasks/README.md")
    sandbox_folder_ignored = is_ignored(root, "sandboxes/private_example/test.txt")
    sandbox_placeholder_ignored = is_ignored(root, "sandboxes/README.md")
    report_ignored = is_ignored(root, "outputs/first_commit_recommendation.md")

    check_status = "passing" if check.returncode == 0 else f"failing with exit code {check.returncode}"
    audit_status = "passing" if audit.returncode == 0 else f"failing with exit code {audit.returncode}"
    report_status = "available" if report_path.exists() else "missing"

    sop_items = markdown_file_items(root, "sops")
    prompt_items = markdown_file_items(root, "prompts")
    env_items = markdown_file_items(root, "envs")
    skill_items = skill_file_items(root)
    tool_items = tool_file_items(root)

    lines = [
        "# Workspace Status",
        "",
        f"Last generated: {date.today().isoformat()}",
        "",
        "This file records the current operating state of `D:\\MaHong\\agent_workspace`.",
        "",
        "Regenerate it with:",
        "",
        "```powershell",
        "python tools/generate_workspace_status.py",
        "```",
        "",
        "## Current Health",
        "",
        f"- Structure check: {check_status}.",
        f"- Git readiness audit: {audit_status}.",
        f"- Workspace baseline recommendation: {report_status} in `outputs/first_commit_recommendation.md`.",
        f"- Git candidate files: {len(files)}.",
        f"- Git candidate size: about {total_size:.2f} MB.",
        f"- Recommended baseline files: {recommended}.",
        f"- Manual confirmation items for baseline review: {manual}.",
        f"- Confirmed public/site assets included: {confirmed_assets}.",
        f"- Line ending drift reminders: {line_ending_drift}.",
        f"- Strict 1 MB large-file reminders: {strict_large}.",
        "",
        "## Core Commands",
        "",
        "```powershell",
        *CORE_MAINTENANCE_COMMANDS,
        "```",
        "",
        "Use stricter large-file review when preparing a careful baseline or broad structural commit:",
        "",
        "```powershell",
        "python tools/audit_git_readiness.py --max-mb 1",
        "```",
        "",
        "## Current Tools",
        "",
        *tool_items,
        "",
        "## Current Skills",
        "",
        *skill_items,
        "",
        "## Current SOPs",
        "",
        *sop_items,
        "",
        "## Current Prompts",
        "",
        *prompt_items,
        "",
        "## Current Environments",
        "",
        *env_items,
        "",
        "## Git Baseline Notes",
        "",
        f"The current baseline recommendation treats all {recommended} recommended files as baseline candidates.",
        "",
        "Repository normalization is governed by `.gitattributes`:",
        "",
        "- most text files use LF line endings",
        "- Windows command scripts use CRLF line endings",
        "- images, media, archives, and model artifacts are treated as binary",
        "",
        "Important exclusions are governed by `.gitignore`:",
        "",
        "- generated outputs, logs, temporary files, and caches",
        "- dependency folders such as `node_modules/`",
        "- local `.env` files and secret material",
        "- raw video media and selected source media",
        "- local backup files such as `*.bak`",
        "- local Playwright CLI artifacts",
        "- concrete task folders under `tasks/*`",
        "- concrete sandbox experiments under `sandboxes/*`",
        "",
        "## Task And Sandbox Privacy",
        "",
        "- Concrete task folders are local-private by default.",
        f"- Example concrete task path ignored by Git: {'yes' if task_folder_ignored else 'no'}.",
        f"- `tasks/README.md` remains trackable: {'yes' if not task_placeholder_ignored else 'no'}.",
        "- Publish an approved task only as a separate Git repository after deliberate review.",
        f"- Example sandbox experiment path ignored by Git: {'yes' if sandbox_folder_ignored else 'no'}.",
        f"- `sandboxes/README.md` remains trackable: {'yes' if not sandbox_placeholder_ignored else 'no'}.",
        "",
        "## Ignored Generated Reports",
        "",
        f"- `outputs/first_commit_recommendation.md` ignored by Git: {'yes' if report_ignored else 'no'}.",
        "",
        "## Next Reasonable Actions",
        "",
        "1. Review `outputs/first_commit_recommendation.md` before broad commits.",
        "2. Confirm `git ls-files tasks` contains only intended public task placeholders.",
        "3. Stage and commit only after the checks above pass.",
        "4. Regenerate this file after broad workspace maintenance.",
        "",
    ]

    return "\n".join(lines)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    status = build_status(root)
    output = root / "WORKSPACE_STATUS.md"
    output.write_text(status, encoding="utf-8", newline="\n")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
