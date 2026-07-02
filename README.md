# Agent Workspace

This workspace is a personal, reusable home for learning and using Codex, Claude Code, OpenCode, Aider, and similar coding agents. It keeps shared rules, prompts, SOPs, and task folders in one place so each task stays isolated and repeatable.

## Directory overview

- `AGENTS.md`: root operating rules for all agents.
- `.gitattributes`: text, line-ending, and binary-file normalization rules.
- `skills/`: reusable capability notes and playbooks.
- `sops/`: standard operating procedures.
- `prompts/`: copy-paste prompt templates for different agents.
- `tools/`: small helper scripts for task creation and workspace checks.
- `envs/`: environment notes and setup templates.
- `WORKSPACE_STATUS.md`: latest health, audit, and commit-readiness status.
- `tasks/`: formal task folders for local work; concrete task folders are ignored by Git by default.
- `tasks/README.md`: tracked placeholder explaining the private task-folder policy.
- `sandboxes/`: temporary experiments.
- `archives/`: completed or abandoned task archives.
- `secrets/`: templates only, never real secrets.

## How to create a new task

Run:

```bash
python tools/make_task.py my_task_name
```

This creates `tasks/my_task_name/` with task-level docs, source folders, test folders, output folders, and local ignore rules.

Concrete task folders stay local by default. Keep task status, registries, and cleanup notes inside the task folder unless you deliberately decide to publish them.

## How to check before committing

Run:

```bash
python tools/check_workspace.py
python tools/audit_git_readiness.py
python tools/test_workspace_tools.py
python tools/summarize_git_candidates.py
python tools/prepare_first_commit_report.py
python tools/generate_workspace_status.py
```

Or run the full maintenance chain:

```bash
python tools/run_workspace_maintenance.py
```

The readiness audit reports large Git candidates, sensitive-looking file names, and secret-like content without printing secret values.
Use `python tools/audit_git_readiness.py --max-mb 1` for a stricter large-file review.
The first-commit report is written to `outputs/first_commit_recommendation.md`.
The workspace status summary is regenerated in `WORKSPACE_STATUS.md`.
For a first commit, follow `sops/git_first_commit.md`.
For routine workspace upkeep, follow `sops/workspace_maintenance.md`.

## Notes for Chinese docs on Windows

The Chinese Markdown files are UTF-8. In Windows PowerShell, read them with explicit UTF-8 when needed:

```powershell
Get-Content -Raw -Encoding UTF8 README.zh-CN.md
Get-Content -Raw -Encoding UTF8 WORKSPACE_GUIDE.zh-CN.md
```

## How to work with Codex, Claude Code, OpenCode, or Aider

1. Enter a task folder under `tasks/<task_name>/`.
2. Ask the agent to read:
   - `../AGENTS.md` at the workspace root
   - local `AGENTS.md`
   - local `task.md`
3. Keep all edits inside that task folder unless you explicitly intend to update shared workspace assets.
4. Use `prompts/` templates as the starting prompt.
5. Run the minimum verification commands after each meaningful change.

## How to use skills, SOPs, and prompts

- Use `skills/` when the task matches a reusable capability.
- Use `sops/` for repeatable workflows such as debugging or closing out a task.
- Use `prompts/` to start a safe, structured agent session.

## How to handle secrets

- Never store real keys in this repository.
- Keep only templates in `secrets/`.
- Prefer environment variables or a password manager.
- Use `secrets/env.example` as a placeholder reference only.

## Recommended safety habits

- Inspect before editing.
- Prefer small changes over large rewrites.
- Ask for confirmation before risky commands.
- Do not commit generated outputs, logs, or temporary files.
- Keep task data and experiments isolated.

## How to archive a task

1. Finish the task and write a short `summary.md` if needed.
2. Move final deliverables into the task's `docs/` or `outputs/`.
3. Move the task folder into `archives/` only when it is complete or intentionally abandoned.
4. Keep enough notes so the task can be understood later without re-running everything.
