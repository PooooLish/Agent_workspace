# Workspace Efficiency Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair workspace privacy boundaries, remove publication-policy drift, improve task handoff, and provide one read-only-first command for routine checks.

**Architecture:** Keep the existing helper scripts as compatibility entry points. Add shared step definitions to `workspace_manifest.py`, expose them through a small `workspace.py` dispatcher, and make generated status depend only on stable framework inventory and privacy policy. Drive each behavior through the existing `unittest` suite before changing implementation.

**Tech Stack:** Python 3 standard library, PowerShell verification commands, Git ignore rules, Markdown documentation.

## Global Constraints

- Do not delete, move, publish, or rewrite existing concrete task folders.
- Do not move the existing untracked task-specific Superpowers documents.
- Track the credential-free project `.codex/config.toml`; do not access or change global Codex configuration.
- Keep all existing helper-script commands working.
- Quick checks must not generate or rewrite tracked files.
- Concrete tasks may be published only as independent Git repositories.

## File Map

- `.gitignore`: privacy boundaries for archives and local Superpowers state.
- `.codex/config.toml`: tracked credential-free project MCP policy.
- `tools/check_workspace.py`: executable privacy assertions.
- `tools/make_task.py`: richer task and summary scaffolding.
- `tools/workspace_manifest.py`: shared quick/full check definitions and tool descriptions.
- `tools/workspace.py`: unified command dispatcher.
- `tools/run_workspace_maintenance.py`: compatibility wrapper for the full check.
- `tools/generate_workspace_status.py`: stable deterministic status content.
- `tools/test_workspace_tools.py`: all regression coverage.
- `README.md`, `README.zh-CN.md`: daily operational entry points.
- `WORKSPACE_GUIDE.md`, `WORKSPACE_GUIDE.zh-CN.md`: policy consistency and detailed reference.
- `tasks/README.md`, `archives/README.md`: task and archive privacy policy.
- `sops/new_task.md`, `sops/task_closeout.md`, `sops/workspace_maintenance.md`: lifecycle commands and boundaries.
- `WORKSPACE_STATUS.md`: regenerated stable inventory.

---

### Task 1: Enforce Archive Privacy And Independent Publication

**Files:**
- Modify: `.gitignore`
- Modify: `tools/check_workspace.py`
- Modify: `tools/test_workspace_tools.py`
- Modify: `tasks/README.md`
- Modify: `archives/README.md`
- Modify: `sops/task_closeout.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `WORKSPACE_GUIDE.md`
- Modify: `WORKSPACE_GUIDE.zh-CN.md`
- Track: `.codex/config.toml`

**Interfaces:**
- Consumes: existing `is_git_ignored(root, relative_path) -> bool`.
- Produces: archive and local-state paths in `REQUIRED_IGNORED_PATHS`; one publication rule across root docs.

- [ ] **Step 1: Write failing privacy and policy tests**

Add to `CheckWorkspaceTests` in `tools/test_workspace_tools.py`:

```python
    def test_archives_are_private_by_default(self) -> None:
        self.assertTrue(self.check_workspace.is_git_ignored(ROOT, "archives/private_example/summary.md"))
        self.assertFalse(self.check_workspace.is_git_ignored(ROOT, "archives/README.md"))

    def test_superpowers_runtime_state_is_ignored(self) -> None:
        self.assertTrue(self.check_workspace.is_git_ignored(ROOT, ".superpowers/sdd/progress.md"))

    def test_publication_docs_require_independent_repository(self) -> None:
        docs = [
            "README.md",
            "README.zh-CN.md",
            "WORKSPACE_GUIDE.md",
            "WORKSPACE_GUIDE.zh-CN.md",
            "tasks/README.md",
            "sops/publish_independent_task.md",
        ]
        forbidden = ("narrow Git ignore exception", "narrow ignore-rule exception", "精确的 Git 例外", "单独加入版本库")
        for relative_path in docs:
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(relative_path=relative_path):
                self.assertTrue("independent" in text.lower() or "独立 Git 仓库" in text)
                for phrase in forbidden:
                    self.assertNotIn(phrase, text)
```

- [ ] **Step 2: Run the tests and verify the expected failures**

Run:

```powershell
python -m unittest tools.test_workspace_tools.CheckWorkspaceTests -v
```

Expected: archive and `.superpowers` assertions fail because those paths are not ignored; publication consistency fails on the old exception wording.

- [ ] **Step 3: Implement the privacy rules**

Add to `.gitignore`:

```gitignore
# Completed task archives remain local-private; keep only the policy placeholder public.
archives/*
!archives/README.md

# Local Superpowers execution state is not reusable framework content.
.superpowers/
```

Add these paths to `REQUIRED_IGNORED_PATHS` in `tools/check_workspace.py`:

```python
"archives/private_example/summary.md",
".superpowers/sdd/progress.md",
```

- [ ] **Step 4: Normalize publication and archive documentation**

Update every file listed above to state:

```text
Concrete task folders and archived task folders remain private to the workspace repository. Publish a selected task only by initializing an independent Git repository inside that task directory after deliberate review.
```

Use the equivalent Chinese wording in Chinese files. State that moving a task to `archives/` does not make it public. Remove all advice to add root ignore exceptions. Keep `.codex/config.toml` credential-free and eligible for the root commit.

- [ ] **Step 5: Verify Task 1**

Run:

```powershell
python -m unittest tools.test_workspace_tools.CheckWorkspaceTests -v
python tools/check_workspace.py
python tools/audit_line_endings.py --strict
```

Expected: all commands exit `0`; `.superpowers/` no longer appears in line-ending findings.

- [ ] **Step 6: Commit Task 1**

```powershell
git add .gitignore .codex/config.toml tools/check_workspace.py tools/test_workspace_tools.py tasks/README.md archives/README.md sops/task_closeout.md README.md README.zh-CN.md WORKSPACE_GUIDE.md WORKSPACE_GUIDE.zh-CN.md
git commit -m "fix: preserve private workspace boundaries"
```

---

### Task 2: Make New Tasks Ready For Multi-Turn Handoff

**Files:**
- Modify: `tools/make_task.py`
- Modify: `tools/test_workspace_tools.py`
- Modify: `sops/new_task.md`

**Interfaces:**
- Produces: `build_summary_md(task_name: str) -> str`.
- Produces: `scaffold_task(workspace_root: Path, task_name: str, dry_run: bool = False) -> tuple[list[str], list[str]]`.
- Preserves: `python tools/make_task.py <name> [--dry-run]`.

- [ ] **Step 1: Write failing scaffold tests**

Add to `MakeTaskTests`:

```python
    def test_task_template_contains_handoff_sections(self) -> None:
        text = self.make_task.build_task_md("example")
        for heading in (
            "## Status", "## Goal", "## Non-goals", "## Acceptance criteria",
            "## Verification commands", "## Decisions", "## Progress",
            "## Next action", "## Blockers",
        ):
            self.assertIn(heading, text)
        self.assertIn("planning", text)

    def test_scaffold_creates_summary_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tasks").mkdir()
            created, skipped = self.make_task.scaffold_task(root, "example")
            self.assertFalse(skipped)
            self.assertIn(str(root / "tasks" / "example" / "summary.md"), created)
            summary = (root / "tasks" / "example" / "summary.md").read_text(encoding="utf-8")
            for heading in ("## Goal", "## Outcome", "## Changes", "## Verification", "## Open issues"):
                self.assertIn(heading, summary)
```

- [ ] **Step 2: Run the tests and verify they fail**

```powershell
python -m unittest tools.test_workspace_tools.MakeTaskTests -v
```

Expected: missing lifecycle headings and missing `scaffold_task` fail.

- [ ] **Step 3: Implement the richer templates and testable scaffold function**

Replace `build_task_md` content with the exact headings asserted above, retaining Constraints and Inputs. Add:

```python
def build_summary_md(task_name: str) -> str:
    return f"""# Summary: {task_name}

## Goal

## Outcome

## Changes

## Verification

## Open issues
"""
```

Move directory/file creation into `scaffold_task`. Include `summary.md` in normal creation and dry-run output. Have `main()` validate arguments, resolve the workspace root, call `scaffold_task`, and preserve the existing console format.

- [ ] **Step 4: Update the new-task SOP**

Document the lifecycle fields and instruct agents to keep `Status`, `Progress`, `Next action`, and `Blockers` current after meaningful work.

- [ ] **Step 5: Verify Task 2**

```powershell
python -m unittest tools.test_workspace_tools.MakeTaskTests -v
python tools/make_task.py plan_test --dry-run
```

Expected: tests pass; dry run lists `summary.md` and creates no directory.

- [ ] **Step 6: Commit Task 2**

```powershell
git add tools/make_task.py tools/test_workspace_tools.py sops/new_task.md
git commit -m "feat: scaffold resumable workspace tasks"
```

---

### Task 3: Add One Read-Only-First Workspace Command

**Files:**
- Create: `tools/workspace.py`
- Modify: `tools/workspace_manifest.py`
- Modify: `tools/run_workspace_maintenance.py`
- Modify: `tools/test_workspace_tools.py`
- Modify: `WORKSPACE_STATUS.md`

**Interfaces:**
- Produces: `QUICK_CHECK_STEPS: tuple[StepSpec, ...]` and `FULL_CHECK_STEPS: tuple[StepSpec, ...]` in `workspace_manifest.py`.
- Produces: `run_steps(root: Path, steps: Sequence[StepSpec], runner=subprocess.run) -> int`.
- CLI: `new <name> [--dry-run]`, `check`, and `check --full`.

- [ ] **Step 1: Write failing command-definition tests**

Add a `WorkspaceCommandTests` class:

```python
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
        commands = [step.command for step in self.workspace.FULL_CHECK_STEPS]
        self.assertIn(("tools/prepare_baseline_report.py",), tuple((command[1],) for command in commands if len(command) > 1))
        self.assertIn(("tools/generate_workspace_status.py",), tuple((command[1],) for command in commands if len(command) > 1))

    def test_run_steps_propagates_failure(self) -> None:
        calls = []
        def runner(command, **kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(command, 7)
        code = self.workspace.run_steps(ROOT, self.workspace.QUICK_CHECK_STEPS[:1], runner=runner)
        self.assertEqual(code, 7)
        self.assertEqual(len(calls), 1)
```

- [ ] **Step 2: Run the tests and verify module loading fails**

```powershell
python -m unittest tools.test_workspace_tools.WorkspaceCommandTests -v
```

Expected: failure because `tools/workspace.py` does not exist.

- [ ] **Step 3: Define shared step specifications**

In `workspace_manifest.py`, add:

```python
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
    StepSpec("strict large-file reminder", ("{python}", "tools/audit_git_readiness.py", "--max-mb", "1"), True),
)
```

Add this tool description at the same time:

```python
"tools/workspace.py": "provides the unified task creation and quick/full workspace check commands.",
```

Expose `FULL_CHECK_STEPS = QUICK_CHECK_STEPS + FULL_ONLY_STEPS` from `workspace.py`, replacing `{python}` with `sys.executable` before execution.

- [ ] **Step 4: Implement `tools/workspace.py`**

Use `argparse` subcommands. `new` invokes `make_task.py` with `sys.executable`; `check` chooses quick or full steps. `run_steps` prints each step, calls the injected runner with `cwd=root`, `check=False`, and returns the first required failure code. Allowed reminder failures print a warning and continue.

- [ ] **Step 5: Preserve the maintenance entry point**

Change `run_workspace_maintenance.py` into a thin wrapper that imports `run_checks` from `workspace` and executes the full step list. Preserve its final `Maintenance checks completed.` message.

- [ ] **Step 6: Refresh the compatibility status inventory**

Run the existing generator once so the new registered tool appears in the tracked inventory:

```powershell
python tools/generate_workspace_status.py
```

This explicit generation step is part of framework maintenance; `workspace.py check` itself remains read-only.

- [ ] **Step 7: Verify Task 3**

```powershell
python -m unittest tools.test_workspace_tools.WorkspaceCommandTests -v
python tools/workspace.py new command_test --dry-run
$before = (Get-FileHash WORKSPACE_STATUS.md -Algorithm SHA256).Hash
python tools/workspace.py check
$after = (Get-FileHash WORKSPACE_STATUS.md -Algorithm SHA256).Hash
if ($before -ne $after) { throw "quick check modified WORKSPACE_STATUS.md" }
```

Expected: all exit `0`; the status-file hashes are equal after the quick check.

- [ ] **Step 8: Commit Task 3**

```powershell
git add tools/workspace.py tools/workspace_manifest.py tools/run_workspace_maintenance.py tools/test_workspace_tools.py WORKSPACE_STATUS.md
git commit -m "feat: add unified workspace command"
```

---

### Task 4: Stabilize Status And Simplify Operational Documentation

**Files:**
- Modify: `tools/generate_workspace_status.py`
- Modify: `tools/test_workspace_tools.py`
- Modify: `tools/workspace_manifest.py`
- Modify: `WORKSPACE_STATUS.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `WORKSPACE_GUIDE.md`
- Modify: `WORKSPACE_GUIDE.zh-CN.md`
- Modify: `sops/workspace_maintenance.md`

**Interfaces:**
- Preserves: `build_status(root: Path) -> str` and `python tools/generate_workspace_status.py`.
- Changes: status output is deterministic for unchanged framework files and ignore policy.

- [ ] **Step 1: Write failing stable-status tests**

Add to `WorkspaceStatusTests`:

```python
    def test_status_omits_volatile_local_metrics(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        status = generator.build_status(ROOT)
        for phrase in (
            "Last generated:", "Git candidate files:", "Git candidate size:",
            "Line ending drift reminders:", "large-file reminders:",
        ):
            self.assertNotIn(phrase, status)

    def test_status_documents_archive_privacy(self) -> None:
        generator = self.verify_status.load_status_generator(ROOT)
        status = generator.build_status(ROOT)
        self.assertIn("archives/README.md", status)
        self.assertIn("archived task path ignored by Git: yes", status)
```

- [ ] **Step 2: Run the tests and verify volatile-content failure**

```powershell
python -m unittest tools.test_workspace_tools.WorkspaceStatusTests -v
```

Expected: volatile metrics are still present and archive privacy is absent.

- [ ] **Step 3: Make status generation deterministic**

Remove date, candidate-file enumeration, baseline parsing, line-ending execution, and large-file execution from `build_status`. Keep generated inventories for tools, skills, SOPs, prompts, and environments. Keep stable `git check-ignore` outcomes for tasks, sandboxes, archives, placeholders, generated reports, and `.superpowers/`.

Rename `## Task And Sandbox Privacy` to `## Private Workspace Areas` and include:

```text
- Example archived task path ignored by Git: yes.
- `archives/README.md` remains trackable: yes.
```

Add `tools/workspace.py` to `TOOL_DESCRIPTIONS`.

Replace `CORE_MAINTENANCE_COMMANDS` with the three public front-door commands so documentation tests enforce the simpler interface:

```python
CORE_MAINTENANCE_COMMANDS = [
    "python tools/workspace.py new my_task",
    "python tools/workspace.py check",
    "python tools/workspace.py check --full",
]
```

- [ ] **Step 4: Simplify operational docs**

Put these commands near the top of both README files:

```powershell
python tools/workspace.py new my_task
python tools/workspace.py check
python tools/workspace.py check --full
```

Include the same three commands in the Quick Reference sections of both guides so `CORE_MAINTENANCE_COMMANDS` documentation coverage remains enforced. Replace duplicated command walls with links to `sops/workspace_maintenance.md`. Update both guides to treat generated `WORKSPACE_STATUS.md` as the inventory source instead of manually claiming a fixed installed-skill list. Preserve detailed safety explanations and existing filenames.

- [ ] **Step 5: Regenerate and verify stable status**

```powershell
python tools/generate_workspace_status.py
python tools/verify_workspace_status.py
python tools/workspace.py check --full
python tools/verify_workspace_status.py
```

Expected: all exit `0`; the second full check does not change `WORKSPACE_STATUS.md`.

- [ ] **Step 6: Run full regression and inspect scope**

```powershell
python tools/test_workspace_tools.py
python tools/check_workspace.py
python tools/audit_git_readiness.py --max-mb 1
git diff --check
git status --short
git diff --stat
```

Expected: tests and checks pass; no task or sandbox content is included; unrelated untracked files remain untouched.

- [ ] **Step 7: Commit Task 4**

```powershell
git add tools/generate_workspace_status.py tools/test_workspace_tools.py tools/workspace_manifest.py WORKSPACE_STATUS.md README.md README.zh-CN.md WORKSPACE_GUIDE.md WORKSPACE_GUIDE.zh-CN.md sops/workspace_maintenance.md
git commit -m "docs: streamline workspace operations"
```

## Final Review

- [ ] Run `python tools/workspace.py check --full` once more.
- [ ] Run `git diff origin/master...HEAD --check`.
- [ ] Inspect `git diff --name-status origin/master...HEAD` and confirm no concrete task, sandbox experiment, `.superpowers/`, secret, or unrelated untracked document is present.
- [ ] Request code review using `superpowers:requesting-code-review`.
- [ ] Apply valid review findings with tests first.
- [ ] Run `superpowers:verification-before-completion` before reporting success.
