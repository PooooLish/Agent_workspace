#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import subprocess


REQUIRED_ITEMS = [
    "AGENTS.md",
    "README.md",
    "README.zh-CN.md",
    "WORKSPACE_GUIDE.md",
    "WORKSPACE_GUIDE.zh-CN.md",
    ".gitattributes",
    ".gitignore",
    "WORKSPACE_STATUS.md",
    "skills",
    "skills/cli_tool_setup/SKILL.md",
    "skills/code_review/SKILL.md",
    "skills/documentation_writer/SKILL.md",
    "skills/linux_debugging/SKILL.md",
    "skills/python_project_setup/SKILL.md",
    "skills/valorant-highlight-editing/SKILL.md",
    "sops",
    "sops/debug_error.md",
    "sops/git_first_commit.md",
    "sops/line_endings.md",
    "sops/modify_existing_project.md",
    "sops/new_task.md",
    "sops/safe_shell_commands.md",
    "sops/setup_external_api.md",
    "sops/task_closeout.md",
    "sops/workspace_maintenance.md",
    "prompts",
    "prompts/aider_default.md",
    "prompts/claude_code_default.md",
    "prompts/code_review.md",
    "prompts/codex_default.md",
    "prompts/opencode_default.md",
    "prompts/safe_debug.md",
    "prompts/safe_setup.md",
    "tools",
    "tools/audit_git_readiness.py",
    "tools/audit_line_endings.py",
    "tools/check_workspace.py",
    "tools/generate_workspace_status.py",
    "tools/make_task.py",
    "tools/prepare_first_commit_report.py",
    "tools/run_workspace_maintenance.py",
    "tools/summarize_git_candidates.py",
    "tools/test_workspace_tools.py",
    "tools/verify_first_commit_report.py",
    "tools/verify_workspace_status.py",
    "envs",
    "envs/aider.md",
    "envs/base_python.md",
    "envs/claude_code.md",
    "envs/codex_cli.md",
    "envs/external_api.md",
    "envs/node_tools.md",
    "envs/opencode.md",
    "tasks",
    "tasks/README.md",
    "sandboxes",
    "sandboxes/README.md",
    "archives",
    "archives/README.md",
    "secrets",
    "secrets/env.example",
]

REQUIRED_GITIGNORE_PATTERNS = [
    ".env",
    ".env.*",
    "secrets/*",
    "**/outputs/",
    "**/tmp/",
    "**/logs/",
    "**/node_modules/",
    "*.mp4",
]

REQUIRED_GITATTRIBUTES_PATTERNS = [
    "* text=auto eol=lf",
    "*.ps1 text eol=crlf",
    "*.md text eol=lf",
    "*.py text eol=lf",
    "*.png binary",
]

REQUIRED_IGNORED_PATHS = [
    "outputs/first_commit_recommendation.md",
    "tasks/example_python_demo/outputs/generated.txt",
    "tasks/example_python_demo/tmp/scratch.txt",
    "tasks/example_python_demo/logs/run.log",
    "tasks/example_python_demo/node_modules/package/index.js",
    "tasks/example_python_demo/AGENTS.md",
    "tasks/good_task-name_123/AGENTS.md",
]

REQUIRED_TASK_ITEMS = [
    "AGENTS.md",
    "task.md",
    "README.md",
    ".gitignore",
    "outputs",
    "tmp",
    "logs",
    "docs/skills",
]

TASK_INDEX_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|", re.MULTILINE)
TASK_INDEX_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

UTF8_TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".example",
    ".html",
    ".js",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".ts",
    ".txt",
    ".vue",
    ".yaml",
    ".yml",
}

UTF8_TEXT_NAMES = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "README",
}


def is_utf8_candidate(relative_path: str) -> bool:
    path = Path(relative_path)
    return path.name in UTF8_TEXT_NAMES or path.suffix.lower() in UTF8_TEXT_SUFFIXES


def get_git_candidate_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return []
    return [path for path in result.stdout.split("\0") if path]


def is_git_ignored(root: Path, relative_path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", relative_path],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode == 0


def check_required_ignored_paths(root: Path, warnings: list[str]) -> None:
    for relative_path in REQUIRED_IGNORED_PATHS:
        if not is_git_ignored(root, relative_path):
            warnings.append(f"{relative_path} should be ignored by Git but is not")


def get_tool_script_paths(root: Path) -> list[str]:
    return [f"tools/{path.name}" for path in sorted((root / "tools").glob("*.py"))]


def get_sop_paths(root: Path) -> list[str]:
    return [f"sops/{path.name}" for path in sorted((root / "sops").glob("*.md"))]


def get_prompt_paths(root: Path) -> list[str]:
    return [f"prompts/{path.name}" for path in sorted((root / "prompts").glob("*.md"))]


def get_env_paths(root: Path) -> list[str]:
    return [f"envs/{path.name}" for path in sorted((root / "envs").glob("*.md"))]


def get_skill_main_paths(root: Path) -> list[str]:
    return [
        str(path.relative_to(root)).replace("\\", "/")
        for path in sorted((root / "skills").glob("*/SKILL.md"))
    ]


def get_skill_resource_paths(root: Path) -> list[str]:
    return [
        str(path.relative_to(root)).replace("\\", "/")
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file()
    ]


def workspace_status_text(root: Path) -> str:
    status_path = root / "WORKSPACE_STATUS.md"
    return status_path.read_text(encoding="utf-8") if status_path.exists() else ""


def check_registry_paths(
    paths: list[str],
    warnings: list[str],
    *,
    require_items: bool,
    require_status: bool,
    status_text: str,
) -> None:
    required_items = set(REQUIRED_ITEMS)

    for relative_path in paths:
        if require_items and relative_path not in required_items:
            warnings.append(f"{relative_path} is not listed in REQUIRED_ITEMS")
        if require_status and relative_path not in status_text:
            warnings.append(f"{relative_path} is not documented in WORKSPACE_STATUS.md")


def check_tool_registry(root: Path, warnings: list[str]) -> None:
    check_registry_paths(
        get_tool_script_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=workspace_status_text(root),
    )


def check_sop_registry(root: Path, warnings: list[str]) -> None:
    check_registry_paths(
        get_sop_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=workspace_status_text(root),
    )


def check_prompt_registry(root: Path, warnings: list[str]) -> None:
    check_registry_paths(
        get_prompt_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=workspace_status_text(root),
    )


def check_env_registry(root: Path, warnings: list[str]) -> None:
    check_registry_paths(
        get_env_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=workspace_status_text(root),
    )


def check_skill_registry(root: Path, warnings: list[str]) -> None:
    status_text = workspace_status_text(root)
    check_registry_paths(
        get_skill_main_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=status_text,
    )
    check_registry_paths(
        get_skill_resource_paths(root),
        warnings,
        require_items=False,
        require_status=True,
        status_text=status_text,
    )


def get_markdown_section(text: str, heading: str) -> str:
    matches = list(TASK_INDEX_SECTION_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip() != heading:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[start:end]
    return ""


def parse_task_table(section_text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or "`" not in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows.append(cells)
    return rows


def task_name_from_cell(cell: str) -> str:
    match = re.search(r"`([^`]+)`", cell)
    return match.group(1) if match else ""


def check_task_index_quality(root: Path, index_text: str, task_dirs: set[str], warnings: list[str]) -> None:
    current_rows = parse_task_table(get_markdown_section(index_text, "Current Tasks"))
    cleanup_rows = parse_task_table(get_markdown_section(index_text, "Pending Cleanup"))

    if not current_rows:
        warnings.append("tasks/INDEX.md has no Current Tasks rows")
    if not cleanup_rows:
        warnings.append("tasks/INDEX.md has no Pending Cleanup rows")

    seen: set[str] = set()
    current_tasks: set[str] = set()
    cleanup_tasks: set[str] = set()

    for row in current_rows:
        task_name = task_name_from_cell(row[0]) if row else ""
        if not task_name:
            continue
        current_tasks.add(task_name)
        if task_name in seen:
            warnings.append(f"tasks/INDEX.md lists {task_name} more than once")
        seen.add(task_name)
        if len(row) < 3 or not row[1] or not row[2]:
            warnings.append(f"tasks/INDEX.md current task {task_name} needs status and notes")

    for row in cleanup_rows:
        task_name = task_name_from_cell(row[0]) if row else ""
        if not task_name:
            continue
        cleanup_tasks.add(task_name)
        if task_name in seen:
            warnings.append(f"tasks/INDEX.md lists {task_name} more than once")
        seen.add(task_name)
        if len(row) < 2 or not row[1]:
            warnings.append(f"tasks/INDEX.md cleanup task {task_name} needs a reason")
        if task_name in task_dirs and not is_git_ignored(root, f"tasks/{task_name}/AGENTS.md"):
            warnings.append(f"tasks/INDEX.md cleanup task {task_name} should be ignored by Git")

    indexed_tasks = current_tasks | cleanup_tasks
    for task_name in sorted(task_dirs - indexed_tasks):
        warnings.append(f"tasks/{task_name} is not listed in tasks/INDEX.md")
    for task_name in sorted(indexed_tasks - task_dirs):
        warnings.append(f"tasks/INDEX.md lists missing task directory: {task_name}")


def check_utf8_text_files(root: Path, warnings: list[str]) -> None:
    candidate_paths = get_git_candidate_paths(root)
    if not candidate_paths:
        warnings.append("could not collect git candidate paths for UTF-8 text validation")
        return

    for relative_path in candidate_paths:
        if not is_utf8_candidate(relative_path):
            continue

        path = root / relative_path
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            warnings.append(f"{relative_path} is not valid UTF-8 text: {exc}")
        except OSError as exc:
            warnings.append(f"{relative_path} could not be read for UTF-8 validation: {exc}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing: list[str] = []
    existing: list[str] = []
    warnings: list[str] = []

    for item in REQUIRED_ITEMS:
        path = root / item
        if path.exists():
            existing.append(item)
        else:
            missing.append(item)

    print("Existing items:")
    for item in existing:
        print(f"  + {item}")

    print("Missing items:")
    for item in missing:
        print(f"  - {item}")

    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        gitignore_text = gitignore_path.read_text(encoding="utf-8")
        for pattern in REQUIRED_GITIGNORE_PATTERNS:
            if pattern not in gitignore_text:
                warnings.append(f".gitignore missing recommended pattern: {pattern}")

    gitattributes_path = root / ".gitattributes"
    if gitattributes_path.exists():
        gitattributes_text = gitattributes_path.read_text(encoding="utf-8")
        for pattern in REQUIRED_GITATTRIBUTES_PATTERNS:
            if pattern not in gitattributes_text:
                warnings.append(f".gitattributes missing recommended pattern: {pattern}")

    tasks_root = root / "tasks"
    if tasks_root.exists():
        task_dirs_to_check = [
            path
            for path in sorted(tasks_root.iterdir())
            if path.is_dir() and not is_git_ignored(root, f"tasks/{path.name}/AGENTS.md")
        ]
        for task_dir in task_dirs_to_check:
            for item in REQUIRED_TASK_ITEMS:
                if not (task_dir / item).exists():
                    warnings.append(f"tasks/{task_dir.name} missing recommended item: {item}")

        index_path = tasks_root / "INDEX.md"
        if index_path.exists() and not is_git_ignored(root, "tasks/INDEX.md"):
            index_text = index_path.read_text(encoding="utf-8")
            task_dirs = {
                path.name
                for path in tasks_root.iterdir()
                if path.is_dir() and not is_git_ignored(root, f"tasks/{path.name}/AGENTS.md")
            }
            check_task_index_quality(root, index_text, task_dirs, warnings)

    check_required_ignored_paths(root, warnings)
    check_tool_registry(root, warnings)
    check_skill_registry(root, warnings)
    check_sop_registry(root, warnings)
    check_prompt_registry(root, warnings)
    check_env_registry(root, warnings)
    check_utf8_text_files(root, warnings)

    print("Warnings:")
    for warning in warnings:
        print(f"  ! {warning}")

    if missing or warnings:
        print(f"Summary: {len(missing)} missing required item(s), {len(warnings)} warning(s), {len(existing)} existing required item(s).")
        if missing:
            return 1
        return 2

    print(f"Summary: workspace looks complete with {len(existing)} required item(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
