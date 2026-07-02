# Workspace Guide

This document is the maintainable master guide for `D:\MaHong\agent_workspace`. It is intended to help a future you, or any coding agent working with you, understand the purpose, structure, components, workflows, and maintenance model of the entire workspace from a single file.

## 1. Purpose

This workspace is a personal operations hub for coding agents such as Codex, Claude Code, OpenCode, and Aider.

It exists to solve four recurring problems:

1. Keep shared rules and habits in one place.
2. Isolate formal tasks from temporary experiments.
3. Reuse prompts, SOPs, and skill cards instead of reinventing them.
4. Make work easier to audit, hand off, archive, and resume later.

The design philosophy is:

- safety first
- task isolation
- minimal changes
- reusable workflows
- human-readable documentation

## 2. Current Root Structure

The workspace currently contains:

- `AGENTS.md`
- `README.md`
- `README.zh-CN.md`
- `WORKSPACE_GUIDE.md`
- `WORKSPACE_GUIDE.zh-CN.md`
- `WORKSPACE_STATUS.md`
- `.gitattributes`
- `.gitignore`
- `.git/`
- `skills/`
- `sops/`
- `prompts/`
- `tools/`
- `envs/`
- `tasks/`
- `sandboxes/`
- `archives/`
- `secrets/`

Each top-level item has a specific responsibility and should stay focused on that role.

## 3. Root Governance Files

### `AGENTS.md`

This is the root operating policy for agents.

It defines:

- the global role of the agent
- core safety rules
- the default work loop
- task isolation rules
- file modification rules

It is the most important behavioral file in the workspace. Any agent working in this repository should read it first.

### `README.md`

This is the short English overview. It explains the workspace purpose, directory layout, new-task flow, how to use agents, how to handle secrets, and how to archive tasks.

### `README.zh-CN.md`

This is the short Chinese overview. It mirrors the main workspace concepts in Chinese and serves as the most accessible entry point for daily use.

The Chinese Markdown files are UTF-8. On Windows PowerShell, use explicit UTF-8 when reading them from the terminal:

```powershell
Get-Content -Raw -Encoding UTF8 README.zh-CN.md
Get-Content -Raw -Encoding UTF8 WORKSPACE_GUIDE.zh-CN.md
```

### `.gitignore`

This file protects the repository from accidentally tracking:

- `.env` files
- key and certificate files
- `outputs/`, `tmp/`, and `logs/`
- Python cache directories
- virtual environments
- large model artifacts
- editor metadata

Its job is to keep the repository clean and reduce the chance of leaking secrets or committing generated noise.

### `.gitattributes`

This file keeps Git diffs and checkouts stable across Windows and Unix-like environments.

It defines:

- LF endings for most text files
- CRLF endings for Windows command scripts
- binary handling for images, media, archives, model artifacts, and other non-text files

Use it to avoid noisy line-ending changes and accidental binary diffs.

### `WORKSPACE_STATUS.md`

This is the current-state companion to the long-form guide.

It records:

- latest health-check status
- Git readiness status
- first-commit recommendation summary
- key maintenance commands
- ignored/generated report notes
- task privacy and Git baseline notes

Regenerate it with `python tools/generate_workspace_status.py` after broad workspace maintenance, before or after the first commit, or whenever the workspace operating model changes materially.

### `.git/`

The workspace has already been initialized as a Git repository. This enables version control for the workspace structure, prompts, templates, scripts, and future task changes if you choose to commit them.

## 4. Shared Reusable Components

### `skills/`

This directory stores reusable skill cards. A skill card is not code; it is a compact operational guide for a repeatable type of work.

Current skills:

- `code_review/`
- `python_project_setup/`
- `cli_tool_setup/`
- `linux_debugging/`
- `documentation_writer/`

Each `SKILL.md` follows the same format:

- Purpose
- When to use
- Procedure
- Safety rules
- Expected output

Role of each current skill:

- `code_review`: review code for bugs, regressions, and missing tests.
- `python_project_setup`: create or organize a small Python task safely.
- `cli_tool_setup`: document or standardize local CLI workflows.
- `linux_debugging`: debug shell, process, path, or environment issues methodically.
- `documentation_writer`: turn project context into clear and practical docs.

When to extend this directory:

- add a new skill when the same kind of work appears repeatedly across tasks
- avoid adding one-off project notes here

### `sops/`

This directory stores Standard Operating Procedures.

Current SOPs:

- `new_task.md`
- `debug_error.md`
- `modify_existing_project.md`
- `setup_external_api.md`
- `task_closeout.md`
- `safe_shell_commands.md`
- `git_first_commit.md`
- `workspace_maintenance.md`

Role of each SOP:

- `new_task.md`: how to create and begin a formal task
- `debug_error.md`: how to perform minimal debugging from a real error
- `modify_existing_project.md`: how to change an existing codebase safely
- `setup_external_api.md`: how to integrate external APIs without storing real keys
- `task_closeout.md`: how to wrap up a task, summarize it, and prepare archival
- `safe_shell_commands.md`: which commands are risky and require manual confirmation
- `git_first_commit.md`: how to inspect Git candidates before the first workspace commit
- `workspace_maintenance.md`: how to run routine workspace health, audit, and status maintenance

When to use an SOP:

- when the work has a repeatable sequence
- when mistakes are costly
- when you want agents to behave consistently

### `prompts/`

This directory stores reusable prompt templates for different agents and workflows.

Current prompt templates:

- `codex_default.md`
- `claude_code_default.md`
- `opencode_default.md`
- `aider_default.md`
- `safe_debug.md`
- `safe_setup.md`
- `code_review.md`

Common behavior enforced by these prompts:

- read `AGENTS.md`, `README.md`, and `task.md` first
- do not delete files
- do not edit outside the intended task scope
- do not store or reveal real API keys
- propose a short plan before editing
- run minimal verification after changes
- finish with changed files, commands run, and verification result

Use these prompts as reliable starting points, then customize per task if needed.

## 5. Helper Scripts

### `tools/make_task.py`

This script creates a formal task folder under `tasks/<task_name>/`.

Usage:

```bash
python tools/make_task.py task_name
```

What it creates:

- `AGENTS.md`
- `task.md`
- `README.md`
- `.gitignore`
- `src/`
- `scripts/`
- `data/`
- `outputs/`
- `tests/`
- `tmp/`
- `logs/`
- `docs/`

Important behavior:

- it does not overwrite existing files
- it reports created items and skipped items
- it gives every task a local working structure immediately

This is the main entry point for creating new formal work.

### `tools/check_workspace.py`

This script checks whether the workspace contains its required baseline components.

Usage:

```bash
python tools/check_workspace.py
```

What it checks:

- `AGENTS.md`
- `README.md`
- `.gitignore`
- `skills/`
- `sops/`
- `prompts/`
- `tools/`
- `envs/`
- `tasks/`
- `sandboxes/`
- `archives/`
- `secrets/`
- `secrets/env.example`

This is useful after manual changes, cleanup work, or future refactors.

### `tools/audit_git_readiness.py`

This script audits files that Git would track before staging or committing.

Usage:

```bash
python tools/audit_git_readiness.py
```

Use a stricter threshold when preparing a careful first commit:

```bash
python tools/audit_git_readiness.py --max-mb 1
```

What it checks:

- large candidate files that are not ignored
- sensitive-looking candidate file names
- secret-like content in small text files

Important behavior:

- it uses Git's own exclude rules to inspect only trackable candidates
- it reports paths and pattern names, not secret values
- it exits with code `2` when it finds review-worthy issues

Run it before the first commit and before any later commit that touches broad workspace structure.

### `tools/summarize_git_candidates.py`

This script summarizes files that Git would track before staging or committing.

Usage:

```bash
python tools/summarize_git_candidates.py
```

What it reports:

- candidate file count
- total candidate size
- counts by top-level area or task
- counts by file extension
- largest candidate files

Use it with `sops/git_first_commit.md` to review the intended baseline before staging.

### `tools/test_workspace_tools.py`

This script runs lightweight regression tests for the workspace maintenance tools.

Usage:

```bash
python tools/test_workspace_tools.py
```

It uses only the Python standard library and avoids creating files except through explicit dry-run checks.

### `tools/prepare_first_commit_report.py`

This script writes a Markdown recommendation for the first workspace commit.

Usage:

```bash
python tools/prepare_first_commit_report.py
```

Default output:

- `outputs/first_commit_recommendation.md`

What it does:

- separates recommended baseline files from files needing manual confirmation
- documents intentionally excluded or deferred paths
- includes the verification commands to rerun before staging

The output lives in `outputs/`, so it is intentionally not tracked by Git unless explicitly moved.

### `tools/generate_workspace_status.py`

This script regenerates `WORKSPACE_STATUS.md` from the current checks and Git candidate state.

Usage:

```bash
python tools/generate_workspace_status.py
```

It runs the workspace check, Git readiness audit, first-commit report generation, and strict large-file reminder, then writes the current-state summary.

### `tools/run_workspace_maintenance.py`

This script runs the standard maintenance chain in order:

- workspace structure check
- tool regression tests
- Git readiness audit
- Git candidate summary
- first-commit report generation
- workspace status regeneration
- strict 1 MB large-file reminder

Usage:

```bash
python tools/run_workspace_maintenance.py
```

The strict large-file reminder is allowed to return a non-zero exit code so known public assets can still be reviewed without failing the default maintenance run.

## 6. Environment Notes

### `envs/`

This directory stores environment-specific usage notes, not installers.

Current files:

- `base_python.md`
- `node_tools.md`
- `codex_cli.md`
- `claude_code.md`
- `opencode.md`
- `aider.md`
- `external_api.md`

What these files are for:

- record conventions
- explain local workflows
- describe safe setup patterns
- document provider usage without storing secrets

#### `envs/opencode.md`

This is currently the most developed environment note.

It records:

- that OpenCode CLI is installed
- that `opencode --version` was verified
- the recommended launch point: inside a task directory
- useful commands such as `opencode .`, `opencode run`, `opencode web`, and `opencode providers list`
- the preferred provider setup pattern: environment variables
- the expected closing report format

#### `envs/external_api.md`

This file defines the workspace policy for API integrations:

- never store real keys in tracked files
- prefer environment variables
- use placeholder templates like `env.example`
- do not commit local secret files

The other environment files are still lightweight and act more as placeholders for future expansion.

## 7. Secrets Policy

### `secrets/`

This directory is intentionally template-only.

Current files:

- `README.md`
- `env.example`

#### `secrets/README.md`

This explains the policy:

- do not store real secrets here
- real credentials should live in system environment variables or a password manager
- agents should not print, store, or commit real secrets

#### `secrets/env.example`

This is a placeholder template containing:

- `OPENAI_API_KEY=`
- `ANTHROPIC_API_KEY=`
- `DEEPSEEK_API_KEY=`
- `OPENROUTER_API_KEY=`
- `GEMINI_API_KEY=`

It should remain empty except for variable names.

## 8. Task System

### `tasks/`

This is where all formal work belongs.

Rule:

- one formal task = one dedicated folder under `tasks/`

Each task should ideally contain:

- local `AGENTS.md`
- local `task.md`
- local `README.md`
- source code
- scripts
- tests
- outputs
- temp files
- logs
- docs

### Task privacy

Concrete task folders are local-private by default and are ignored by Git through `.gitignore`.

The tracked task placeholder is:

- `tasks/README.md`

Use task-local files for active task status, registries, and cleanup notes. Publish a task file only after reviewing it deliberately and adding a narrow Git ignore exception.

When creating a new formal task:

1. Create the task with `python tools/make_task.py <task_name>`.
2. Fill in `tasks/<task_name>/task.md`.
3. Keep task-specific status details inside the task folder.
4. Leave the task folder ignored unless you intentionally decide it is safe to publish.

## 9. Sandboxes and Archives

### `sandboxes/`

This is reserved for temporary experiments.

Use it for:

- quick prototypes
- throwaway tests
- environment experiments
- one-off investigations

Do not treat it as a permanent project area.

### `archives/`

This is reserved for completed or abandoned tasks.

A task should move here only after:

- verification is done
- the task has enough documentation to understand later
- useful outputs are preserved

Both `sandboxes/` and `archives/` include local README files so their purpose remains visible in the Git baseline even when they contain no active experiment or archived task.

## 10. Installed External Agent Tooling

This workspace also connects to tools outside the repository itself.

### Git

Git was initialized for the workspace. The repository exists and can track future changes.

### OpenCode

OpenCode CLI is installed on the machine and is already reflected in `envs/opencode.md`.

Recommended usage:

```powershell
cd D:\MaHong\agent_workspace\tasks\my_task_name
opencode .
```

Recommended provider pattern:

```powershell
$env:OPENAI_API_KEY="your_key_here"
opencode .
```

### Global Codex skills

Outside the workspace repo, your Codex user environment currently also has these installed under `C:\Users\MaHong\.codex\skills`:

- `cli-creator`
- `jupyter-notebook`
- `playwright`
- `screenshot`
- `security-best-practices`

These extend Codex itself rather than the workspace directory, but they are part of your practical setup.

## 11. Recommended Daily Workflow

The intended day-to-day workflow is:

1. Create a task with `python tools/make_task.py <task_name>`.
2. Fill in `tasks/<task_name>/task.md`.
3. Enter that task folder.
4. Start the agent of choice.
5. Ask the agent to read:
   - workspace `AGENTS.md`
   - local `AGENTS.md`
   - local `task.md`
6. Keep all edits within the task unless shared assets truly need updating.
7. Run minimal verification after each meaningful change.
8. Finish with a summary and archive later if appropriate.

## 12. What Is Mature vs. What Is Still Lightweight

Currently mature:

- workspace structure
- root rules
- secrets policy
- task scaffolding
- workspace checking
- prompt starters
- baseline OpenCode documentation
- private task-folder policy

Currently lightweight:

- most environment notes besides OpenCode
- task archive practices, because no real tasks are archived yet
- sandbox conventions, because no experiments are stored yet
- advanced per-agent customization for prompts and skills

This is expected. The workspace is intentionally scaffold-first and should evolve with real use.

## 13. Maintenance Rules

To keep the workspace maintainable:

- keep root files generic and reusable
- keep task-specific details inside task folders
- add new skills only when a workflow repeats
- add new SOPs only when a sequence deserves standardization
- update `envs/` when tool usage changes
- update `secrets/env.example` only for placeholder names, never real values
- prefer adding new docs over rewriting unrelated existing ones
- back up important notes before major changes

## 14. Suggested Future Improvements

Good next improvements would be:

- add a dedicated OpenCode prompt template under `prompts/`
- add bilingual task templates
- expand `envs/codex_cli.md`, `envs/claude_code.md`, and `envs/aider.md`
- add a `summary.md` convention to real tasks
- add a private task registry convention inside task folders or `tasks/` if task volume grows
- define naming conventions for archives and sandboxes

## 15. Quick Reference

Create a task:

```bash
python tools/make_task.py my_task
```

Check the workspace:

```bash
python tools/check_workspace.py
```

Audit Git readiness:

```bash
python tools/audit_git_readiness.py
```

Summarize Git candidates:

```bash
python tools/summarize_git_candidates.py
```

Prepare first commit report:

```bash
python tools/prepare_first_commit_report.py
```

Regenerate workspace status:

```bash
python tools/generate_workspace_status.py
```

Run full workspace maintenance:

```bash
python tools/run_workspace_maintenance.py
```

Launch OpenCode in a task:

```powershell
cd D:\MaHong\agent_workspace\tasks\my_task
opencode .
```

Set a provider key for the current shell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

## 16. Summary

This workspace already provides a solid shared operating layer for agent-assisted development:

- a rule system
- task isolation
- prompt templates
- SOPs
- helper scripts
- secret-handling policy
- environment notes
- a private task-folder policy
- OpenCode integration

Its main value is not any single file. Its value comes from how all the parts work together:

- root rules constrain behavior
- prompts shape execution
- SOPs standardize process
- tools reduce setup friction
- tasks isolate work
- secrets stay out of the repository
- environment notes connect local tools to safe workflows

Treat this file as the single source of truth for understanding the workspace at a glance, and update it whenever the structure or working model changes materially.
