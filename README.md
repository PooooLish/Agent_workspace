# Agent Workspace

**English** | [简体中文](README.zh-CN.md)

This workspace is a personal, reusable home for learning and using Codex, Claude Code, OpenCode, Aider, and similar coding agents. It keeps shared rules, prompts, SOPs, and task folders in one place so each task stays isolated and repeatable.

## Documentation

- [English workspace guide](WORKSPACE_GUIDE.md)
- [简体中文说明](README.zh-CN.md)

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
- `archives/`: completed or abandoned task archives; concrete archive folders remain local-private.
- `secrets/`: templates only, never real secrets.

## How to create a new task

Run:

```bash
python tools/workspace.py new my_task
```

This creates `tasks/my_task/` with task-level docs, source folders, test folders, output folders, and local ignore rules.

Concrete task folders stay local by default. Keep task status, registries, and cleanup notes inside the task folder unless you deliberately decide to publish them.

## How to publish a task independently

Concrete task folders remain private to the root workspace repository. When a task has a real deliverable and should be published, follow `sops/publish_independent_task.md` to initialize that task directory as a separate Git repository. Never publish a concrete experiment directory under `sandboxes/`; only its policy README belongs to the root repository.

## How to check before committing

Run the quick, read-only check during routine framework work:

```bash
python tools/workspace.py check
```

Before a broad framework commit, run the full check that also regenerates maintenance reports:

```bash
python tools/workspace.py check --full
```

The readiness audit reports large Git candidates, sensitive-looking file names, and secret-like content without printing secret values.
Use `python tools/audit_git_readiness.py --max-mb 1` for a stricter large-file review.
The baseline recommendation report is written to `outputs/first_commit_recommendation.md`.
The workspace status summary is regenerated in `WORKSPACE_STATUS.md`.
For the first commit or any broad structural commit, follow `sops/git_first_commit.md`.
For individual compatibility commands and the detailed procedure, follow `sops/workspace_maintenance.md`.

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
3. Move the task folder into `archives/` only when it is complete or intentionally abandoned; this does not make it public to the root repository.
4. Keep enough notes so the task can be understood later without re-running everything.
