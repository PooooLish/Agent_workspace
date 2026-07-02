# AGENTS.md

## Global role

- The agent is my private coding and research assistant.
- By default, work only inside `~/agent_workspace` or the current task folder under it.

## Safety rules

- Do not delete files unless I explicitly approve it.
- Do not use `sudo` unless I explicitly approve it.
- Do not print, save, or commit any real API key, token, SSH key, or password.
- Do not change global shell configuration files.
- Do not run unknown install scripts.
- Do not execute `curl | sh`.
- Do not access `~/.ssh`, `~/.aws`, `~/.config`, or similar sensitive directories unless I explicitly ask.

## Default work loop

1. Inspect: check the directory structure first.
2. Read: read `AGENTS.md`, `README.md`, and `task.md` in the current scope.
3. Plan: propose the smallest useful execution plan.
4. Act: modify only the files that are necessary.
5. Verify: run the minimum verification commands.
6. Report: summarize changed files, commands run, verification results, and remaining issues.

## Rule hierarchy

- The workspace root `AGENTS.md` is the global rule set for all tasks.
- Each task may have its own local `AGENTS.md` with task-specific instructions.
- A task-level `AGENTS.md` can only supplement or tighten the workspace rules.
- A task-level `AGENTS.md` must not weaken the workspace safety rules.
- If the root rules and the task rules differ, follow the stricter rule.

## Task isolation rules

- Each formal task must live in `tasks/<task_name>/`.
- Each temporary experiment must live in `sandboxes/<experiment_name>/`.
- Task outputs go to `outputs/`.
- Temporary files go to `tmp/`.
- Logs go to `logs/`.
- Task-local skills, notes, and reusable discoveries that are specific to one task should stay inside that task folder, preferably under `docs/skills/`.
- Do not let one task modify another task's files.

## Knowledge placement rules

- Put cross-task, reusable skills in the root `skills/` directory.
- Put task-specific skills, checklists, notes, and lessons in the task folder.
- Promote a task-local skill into the root `skills/` directory only after it has proven reusable across multiple tasks.

## File modification rules

- Prefer creating new files instead of rewriting existing ones.
- Back up config files before changing them.
- Make small, reviewable edits.
- Do not refactor an entire project unless I explicitly ask.
