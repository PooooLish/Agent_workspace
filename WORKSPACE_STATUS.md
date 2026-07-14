# Workspace Status

This generated file records stable framework inventory and privacy-policy outcomes.

Regenerate it with:

```powershell
python tools/generate_workspace_status.py
```

## Current Health

- Stable framework inventories are generated from the current workspace files.
- Privacy-policy outcomes are checked with `git check-ignore`.
- Run the commands below for live tests, Git readiness, and line-ending results.

## Core Commands

```powershell
python tools/workspace.py new my_task
python tools/workspace.py check
python tools/workspace.py check --full
```

## Current Tools

- `tools/audit_git_readiness.py`: checks Git candidates for large files, sensitive names, and secret-like content.
- `tools/audit_line_endings.py`: reports line ending drift against `.gitattributes` policy.
- `tools/check_workspace.py`: checks required workspace structure, deliberately trackable optional task index quality, registry coverage, Git ignore behavior, and UTF-8 text readability.
- `tools/generate_workspace_status.py`: regenerates this current-state summary.
- `tools/make_task.py`: creates isolated task folders with safe defaults and `--dry-run`.
- `tools/prepare_baseline_report.py`: writes the workspace baseline recommendation report.
- `tools/prepare_first_commit_report.py`: legacy-compatible implementation behind the baseline report command.
- `tools/run_workspace_maintenance.py`: runs the full maintenance chain.
- `tools/summarize_git_candidates.py`: summarizes Git candidates by area, extension, and largest files.
- `tools/test_workspace_tools.py`: runs lightweight regression tests for workspace tools.
- `tools/verify_baseline_report.py`: verifies that the baseline recommendation matches current Git candidates.
- `tools/verify_first_commit_report.py`: legacy-compatible implementation behind the baseline report verifier.
- `tools/verify_workspace_status.py`: verifies that `WORKSPACE_STATUS.md` matches the current generated status.
- `tools/workspace.py`: provides the unified task creation and quick/full workspace check commands.
- `tools/workspace_manifest.py`: centralizes shared workspace tool metadata and maintenance command lists.

## Current Skills

- `skills/cli_tool_setup/SKILL.md`
- `skills/code_review/SKILL.md`
- `skills/documentation_writer/SKILL.md`
- `skills/linux_debugging/SKILL.md`
- `skills/python_project_setup/SKILL.md`
- `skills/visual_design_review/SKILL.md`

## Current SOPs

- `sops/debug_error.md`
- `sops/git_first_commit.md`
- `sops/line_endings.md`
- `sops/modify_existing_project.md`
- `sops/new_task.md`
- `sops/publish_independent_task.md`
- `sops/safe_shell_commands.md`
- `sops/setup_external_api.md`
- `sops/task_closeout.md`
- `sops/workspace_maintenance.md`

## Current Prompts

- `prompts/aider_default.md`
- `prompts/claude_code_default.md`
- `prompts/code_review.md`
- `prompts/codex_default.md`
- `prompts/opencode_default.md`
- `prompts/safe_debug.md`
- `prompts/safe_setup.md`

## Current Environments

- `envs/aider.md`
- `envs/base_python.md`
- `envs/claude_code.md`
- `envs/codex_cli.md`
- `envs/external_api.md`
- `envs/node_tools.md`
- `envs/opencode.md`

## Repository Policy

Repository normalization is governed by `.gitattributes`:

- most text files use LF line endings
- Windows command scripts use CRLF line endings
- images, media, archives, and model artifacts are treated as binary

Important exclusions are governed by `.gitignore`:

- generated outputs, logs, temporary files, and caches
- dependency folders such as `node_modules/`
- local `.env` files and secret material
- raw video media and selected source media
- local backup files such as `*.bak`
- local Playwright CLI artifacts
- concrete task folders under `tasks/*`
- concrete sandbox experiments under `sandboxes/*`
- concrete archived tasks under `archives/*`
- local Superpowers execution state under `.superpowers/`

## Private Workspace Areas

- Concrete task folders are local-private by default.
- Example concrete task path ignored by Git: yes.
- `tasks/README.md` remains trackable: yes.
- Publish an approved task only as a separate Git repository after deliberate review.
- Example sandbox experiment path ignored by Git: yes.
- `sandboxes/README.md` remains trackable: yes.
- Example archived task path ignored by Git: yes.
- `archives/README.md` remains trackable: yes.
- Example Superpowers runtime path ignored by Git: yes.

## Ignored Generated Reports

- `outputs/first_commit_recommendation.md` ignored by Git: yes.

## Routine Actions

1. Run `python tools/workspace.py check` during routine framework work.
2. Run `python tools/workspace.py check --full` before broad framework commits.
3. Publish approved tasks only as separate Git repositories.
