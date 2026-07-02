# Workspace Status

Last generated: 2026-07-02

This file records the current operating state of `D:\MaHong\agent_workspace`.

Regenerate it with:

```powershell
python tools/generate_workspace_status.py
```

## Current Health

- Structure check: passing.
- Git readiness audit: passing.
- Workspace baseline recommendation: available in `outputs/first_commit_recommendation.md`.
- Git candidate files: 59.
- Git candidate size: about 0.14 MB.
- Recommended baseline files: 59.
- Manual confirmation items for baseline review: 0.
- Confirmed public/site assets included: 0.
- Line ending drift reminders: 0.
- Strict 1 MB large-file reminders: 0.

## Core Commands

```powershell
python tools/check_workspace.py
python tools/audit_git_readiness.py
python tools/audit_line_endings.py
python tools/test_workspace_tools.py
python tools/summarize_git_candidates.py
python tools/prepare_first_commit_report.py
python tools/verify_first_commit_report.py
python tools/generate_workspace_status.py
python tools/verify_workspace_status.py
python tools/run_workspace_maintenance.py
```

Use stricter large-file review when preparing a careful baseline or broad structural commit:

```powershell
python tools/audit_git_readiness.py --max-mb 1
```

## Current Tools

- `tools/make_task.py`: creates isolated task folders with safe defaults and `--dry-run`.
- `tools/check_workspace.py`: checks required workspace structure, deliberately trackable optional task index quality, tool/skill/SOP/prompt/environment registry coverage, Git ignore behavior, and UTF-8 text readability.
- `tools/audit_git_readiness.py`: checks Git candidates for large files, sensitive names, and secret-like content.
- `tools/audit_line_endings.py`: reports line ending drift against `.gitattributes` policy.
- `tools/test_workspace_tools.py`: runs lightweight regression tests for workspace tools.
- `tools/summarize_git_candidates.py`: summarizes Git candidates by area, extension, and largest files.
- `tools/prepare_first_commit_report.py`: writes the workspace baseline recommendation report.
- `tools/verify_first_commit_report.py`: verifies that the baseline recommendation matches current Git candidates.
- `tools/generate_workspace_status.py`: regenerates this current-state summary.
- `tools/verify_workspace_status.py`: verifies that `WORKSPACE_STATUS.md` matches the current generated status.
- `tools/run_workspace_maintenance.py`: runs the full maintenance chain.

## Current Skills

- `skills/cli_tool_setup/SKILL.md`
- `skills/code_review/SKILL.md`
- `skills/documentation_writer/SKILL.md`
- `skills/linux_debugging/SKILL.md`
- `skills/python_project_setup/SKILL.md`
- `skills/valorant-highlight-editing/agents/openai.yaml`
- `skills/valorant-highlight-editing/references/platform_style_patterns.md`
- `skills/valorant-highlight-editing/references/research_sources.md`
- `skills/valorant-highlight-editing/references/software_toolchain.md`
- `skills/valorant-highlight-editing/SKILL.md`

## Current SOPs

- `sops/debug_error.md`
- `sops/git_first_commit.md`
- `sops/line_endings.md`
- `sops/modify_existing_project.md`
- `sops/new_task.md`
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

## Git Baseline Notes

The current baseline recommendation treats all 59 recommended files as baseline candidates.

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

## Task Privacy

- Concrete task folders are local-private by default.
- Example concrete task path ignored by Git: yes.
- `tasks/README.md` remains trackable: yes.
- Publish task files only after deliberate review and a narrow ignore-rule exception.

## Ignored Generated Reports

- `outputs/first_commit_recommendation.md` ignored by Git: yes.

## Next Reasonable Actions

1. Review `outputs/first_commit_recommendation.md` before broad commits.
2. Confirm `git ls-files tasks` contains only intended public task placeholders.
3. Stage and commit only after the checks above pass.
4. Regenerate this file after broad workspace maintenance.
