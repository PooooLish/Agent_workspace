#!/usr/bin/env python3
from __future__ import annotations

import subprocess
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
    task_folder_ignored = is_ignored(root, "tasks/private_example/AGENTS.md")
    task_placeholder_ignored = is_ignored(root, "tasks/README.md")
    sandbox_folder_ignored = is_ignored(root, "sandboxes/private_example/test.txt")
    sandbox_placeholder_ignored = is_ignored(root, "sandboxes/README.md")
    archive_folder_ignored = is_ignored(root, "archives/private_example/summary.md")
    archive_placeholder_ignored = is_ignored(root, "archives/README.md")
    superpowers_ignored = is_ignored(root, ".superpowers/sdd/progress.md")
    report_ignored = is_ignored(root, "outputs/first_commit_recommendation.md")

    sop_items = markdown_file_items(root, "sops")
    prompt_items = markdown_file_items(root, "prompts")
    env_items = markdown_file_items(root, "envs")
    skill_items = skill_file_items(root)
    tool_items = tool_file_items(root)

    lines = [
        "# Workspace Status",
        "",
        "This generated file records stable framework inventory and privacy-policy outcomes.",
        "",
        "Regenerate it with:",
        "",
        "```powershell",
        "python tools/generate_workspace_status.py",
        "```",
        "",
        "## Current Health",
        "",
        "- Stable framework inventories are generated from the current workspace files.",
        "- Privacy-policy outcomes are checked with `git check-ignore`.",
        "- Run the commands below for live tests, Git readiness, and line-ending results.",
        "",
        "## Core Commands",
        "",
        "```powershell",
        *CORE_MAINTENANCE_COMMANDS,
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
        "## Repository Policy",
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
        "- concrete archived tasks under `archives/*`",
        "- local Superpowers execution state under `.superpowers/`",
        "",
        "## Private Workspace Areas",
        "",
        "- Concrete task folders are local-private by default.",
        f"- Example concrete task path ignored by Git: {'yes' if task_folder_ignored else 'no'}.",
        f"- `tasks/README.md` remains trackable: {'yes' if not task_placeholder_ignored else 'no'}.",
        "- Publish an approved task only as a separate Git repository after deliberate review.",
        f"- Example sandbox experiment path ignored by Git: {'yes' if sandbox_folder_ignored else 'no'}.",
        f"- `sandboxes/README.md` remains trackable: {'yes' if not sandbox_placeholder_ignored else 'no'}.",
        f"- Example archived task path ignored by Git: {'yes' if archive_folder_ignored else 'no'}.",
        f"- `archives/README.md` remains trackable: {'yes' if not archive_placeholder_ignored else 'no'}.",
        f"- Example Superpowers runtime path ignored by Git: {'yes' if superpowers_ignored else 'no'}.",
        "",
        "## Ignored Generated Reports",
        "",
        f"- `outputs/first_commit_recommendation.md` ignored by Git: {'yes' if report_ignored else 'no'}.",
        "",
        "## Routine Actions",
        "",
        "1. Run `python tools/workspace.py check` during routine framework work.",
        "2. Run `python tools/workspace.py check --full` before broad framework commits.",
        "3. Publish approved tasks only as separate Git repositories.",
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
