#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import subprocess


REQUIRED_ITEMS = [
    "AGENTS.md",
    "README.md",
    "WORKSPACE_GUIDE.md",
    "docs",
    "docs/README.md",
    "docs/framework/git-task-isolation.md",
    "docs/framework/workspace-efficiency.md",
    ".gitattributes",
    ".gitignore",
    "WORKSPACE_STATUS.md",
    "skills",
    "sops",
    "prompts",
    "tools",
    "envs",
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
    "tasks/*",
    "sandboxes/*",
    "archives/*",
    ".superpowers/",
    "/docs/superpowers/",
    "*.mp4",
]

PRIVATE_ROOTS = ("tasks", "sandboxes", "archives", "docs/superpowers")
PUBLIC_PRIVATE_AREA_PLACEHOLDERS = {
    "tasks/README.md",
    "sandboxes/README.md",
    "archives/README.md",
}

REQUIRED_GITATTRIBUTES_PATTERNS = [
    "* text=auto eol=lf",
    "*.ps1 text eol=crlf",
    "*.md text eol=lf",
    "*.py text eol=lf",
    "*.png binary",
]

REQUIRED_IGNORED_PATHS = [
    "outputs/first_commit_recommendation.md",
    "tasks/private_example/outputs/generated.txt",
    "tasks/private_example/tmp/scratch.txt",
    "tasks/private_example/logs/run.log",
    "tasks/private_example/node_modules/package/index.js",
    "tasks/private_example/AGENTS.md",
    "sandboxes/private_example/test.txt",
    "archives/private_example/summary.md",
    ".superpowers/sdd/progress.md",
    "docs/superpowers/specs/example-design.md",
]

PLANNING_GATE_REQUIRED_PHRASES = (
    "## Planning artifact gate",
    "Simple, low-risk, localized work",
    "must not create spec or plan files",
    "docs/framework/",
    "tasks/<task_name>/docs/superpowers/",
)

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

OPTIONAL_PRIVATE_TASK_INDEX = "tasks/INDEX.md"

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


def unexpected_tracked_private_paths(paths: list[str]) -> list[str]:
    unexpected: list[str] = []
    for raw_path in paths:
        path = raw_path.replace("\\", "/")
        if path in PUBLIC_PRIVATE_AREA_PLACEHOLDERS:
            continue
        if any(path.startswith(f"{root}/") for root in PRIVATE_ROOTS):
            unexpected.append(path)
    return sorted(unexpected)


def get_tracked_private_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", *PRIVATE_ROOTS],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")
    return unexpected_tracked_private_paths([path for path in result.stdout.split("\0") if path])


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


def check_planning_artifact_gate(root: Path, warnings: list[str]) -> None:
    agents_text = (root / "AGENTS.md").read_text(encoding="utf-8")
    for phrase in PLANNING_GATE_REQUIRED_PHRASES:
        if phrase not in agents_text:
            warnings.append(f"AGENTS.md planning artifact gate missing required phrase: {phrase}")


def get_tool_script_paths(root: Path) -> list[str]:
    return [f"tools/{path.name}" for path in sorted((root / "tools").glob("*.py"))]


def required_items(root: Path) -> list[str]:
    items: list[str] = []
    for item in REQUIRED_ITEMS:
        items.append(item)
        if item == "skills":
            items.extend(get_skill_main_paths(root))
        if item == "sops":
            items.extend(get_sop_paths(root))
        if item == "prompts":
            items.extend(get_prompt_paths(root))
        if item == "tools":
            items.extend(get_tool_script_paths(root))
        if item == "envs":
            items.extend(get_env_paths(root))
    return items


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
    root: Path,
    paths: list[str],
    warnings: list[str],
    *,
    require_items: bool,
    require_status: bool,
    status_text: str,
) -> None:
    required_item_set = set(required_items(root))

    for relative_path in paths:
        if require_items and relative_path not in required_item_set:
            warnings.append(f"{relative_path} is not listed in REQUIRED_ITEMS")
        if require_status and relative_path not in status_text:
            warnings.append(f"{relative_path} is not documented in WORKSPACE_STATUS.md")


def check_tool_registry(root: Path, warnings: list[str]) -> None:
    check_registry_paths(
        root,
        get_tool_script_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=workspace_status_text(root),
    )


def check_sop_registry(root: Path, warnings: list[str]) -> None:
    check_registry_paths(
        root,
        get_sop_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=workspace_status_text(root),
    )


def check_prompt_registry(root: Path, warnings: list[str]) -> None:
    check_registry_paths(
        root,
        get_prompt_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=workspace_status_text(root),
    )


def check_env_registry(root: Path, warnings: list[str]) -> None:
    check_registry_paths(
        root,
        get_env_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=workspace_status_text(root),
    )


def check_skill_registry(root: Path, warnings: list[str]) -> None:
    status_text = workspace_status_text(root)
    check_registry_paths(
        root,
        get_skill_main_paths(root),
        warnings,
        require_items=True,
        require_status=True,
        status_text=status_text,
    )
    check_registry_paths(
        root,
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


def private_task_index_is_active(root: Path) -> bool:
    index_path = root / OPTIONAL_PRIVATE_TASK_INDEX
    return index_path.exists() and not is_git_ignored(root, OPTIONAL_PRIVATE_TASK_INDEX)


def check_private_task_index_quality(root: Path, index_text: str, task_dirs: set[str], warnings: list[str]) -> None:
    current_rows = parse_task_table(get_markdown_section(index_text, "Current Tasks"))
    cleanup_rows = parse_task_table(get_markdown_section(index_text, "Pending Cleanup"))

    if not current_rows:
        warnings.append(f"{OPTIONAL_PRIVATE_TASK_INDEX} has no Current Tasks rows")
    if not cleanup_rows:
        warnings.append(f"{OPTIONAL_PRIVATE_TASK_INDEX} has no Pending Cleanup rows")

    seen: set[str] = set()
    current_tasks: set[str] = set()
    cleanup_tasks: set[str] = set()

    for row in current_rows:
        task_name = task_name_from_cell(row[0]) if row else ""
        if not task_name:
            continue
        current_tasks.add(task_name)
        if task_name in seen:
            warnings.append(f"{OPTIONAL_PRIVATE_TASK_INDEX} lists {task_name} more than once")
        seen.add(task_name)
        if len(row) < 3 or not row[1] or not row[2]:
            warnings.append(f"{OPTIONAL_PRIVATE_TASK_INDEX} current task {task_name} needs status and notes")

    for row in cleanup_rows:
        task_name = task_name_from_cell(row[0]) if row else ""
        if not task_name:
            continue
        cleanup_tasks.add(task_name)
        if task_name in seen:
            warnings.append(f"{OPTIONAL_PRIVATE_TASK_INDEX} lists {task_name} more than once")
        seen.add(task_name)
        if len(row) < 2 or not row[1]:
            warnings.append(f"{OPTIONAL_PRIVATE_TASK_INDEX} cleanup task {task_name} needs a reason")
        if task_name in task_dirs and not is_git_ignored(root, f"tasks/{task_name}/AGENTS.md"):
            warnings.append(f"{OPTIONAL_PRIVATE_TASK_INDEX} cleanup task {task_name} should be ignored by Git")

    indexed_tasks = current_tasks | cleanup_tasks
    for task_name in sorted(task_dirs - indexed_tasks):
        warnings.append(f"tasks/{task_name} is not listed in {OPTIONAL_PRIVATE_TASK_INDEX}")
    for task_name in sorted(indexed_tasks - task_dirs):
        warnings.append(f"{OPTIONAL_PRIVATE_TASK_INDEX} lists missing task directory: {task_name}")


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

    for item in required_items(root):
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

        index_path = root / OPTIONAL_PRIVATE_TASK_INDEX
        if private_task_index_is_active(root):
            index_text = index_path.read_text(encoding="utf-8")
            task_dirs = {
                path.name
                for path in tasks_root.iterdir()
                if path.is_dir() and not is_git_ignored(root, f"tasks/{path.name}/AGENTS.md")
            }
            check_private_task_index_quality(root, index_text, task_dirs, warnings)

    check_required_ignored_paths(root, warnings)
    check_planning_artifact_gate(root, warnings)
    try:
        for relative_path in get_tracked_private_paths(root):
            warnings.append(f"private workspace content is tracked by root Git: {relative_path}")
    except RuntimeError as error:
        warnings.append(f"could not inspect tracked private workspace paths: {error}")
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
