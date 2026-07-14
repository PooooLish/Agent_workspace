# Workspace Efficiency Repair Design

## Objective

Repair the confirmed privacy, policy-drift, and workflow-efficiency problems in the workspace without changing its core model: reusable framework files stay in the root repository, concrete tasks stay private, and publishable tasks use independent Git repositories.

## Scope

This change will:

- keep concrete archived tasks private from the root Git repository
- make every publication instruction use the independent-repository policy
- classify local Codex and Superpowers state so it does not create permanent Git noise
- improve generated task files for multi-turn agent handoff
- provide one discoverable workspace command with quick and full check modes
- keep quick checks read-only and reserve generated reports for full maintenance
- reduce volatile data in the tracked workspace status
- add regression coverage for each changed behavior

This change will not:

- publish, move, delete, or rewrite any existing concrete task
- introduce a task database or background service
- replace the existing helper scripts immediately
- add GitHub Actions, automatic commits, automatic pushes, or automatic archiving
- change global Codex configuration or credentials

## Privacy Model

The root `.gitignore` will ignore concrete folders under `archives/` while preserving `archives/README.md`, matching the existing task and sandbox policy. Workspace checks will verify all three private path classes: tasks, sandboxes, and archives.

`.superpowers/` is local execution state and will be ignored. The existing project MCP configuration contains no credential and is reusable framework configuration, so `.codex/config.toml` will be tracked as part of the root framework. Secrets must continue to be referenced through environment variables or OAuth rather than stored in that file.

Task-specific planning documents belong inside their task directories. This repair will document and enforce that policy for future files, but it will not move existing untracked documents without separate approval.

## Publication Policy

All root documentation will state one rule: concrete task folders never enter the workspace repository. A selected task may be published only by following `sops/publish_independent_task.md` and initializing Git inside that task directory after explicit review.

No documentation may recommend adding root `.gitignore` exceptions for concrete tasks.

## Unified Command

A new `tools/workspace.py` command will provide a stable front door while preserving existing scripts for compatibility.

Initial interface:

```text
python tools/workspace.py new <task_name> [--dry-run]
python tools/workspace.py check
python tools/workspace.py check --full
```

`new` delegates to the existing task creation behavior. `check` runs only fast, read-only validation: tool tests, structure checks, Git readiness, and strict line-ending checks. `check --full` additionally generates and verifies the baseline and workspace-status reports, then runs the stricter large-file reminder.

The command returns nonzero when a required step fails, prints the failed step and command, and does not hide output. Existing script entry points remain supported.

## Task Template

New `task.md` files will include:

- status, defaulting to `planning`
- goal
- non-goals
- constraints
- inputs
- acceptance criteria
- verification commands
- decisions
- progress
- next action
- blockers

The task creator will also create a `summary.md` skeleton containing goal, outcome, changes, verification, and open issues. Existing tasks are not modified.

## Maintenance And Status

Quick checks must not generate or rewrite tracked files. Full maintenance may generate reports because it is an explicit maintenance action.

`run_workspace_maintenance.py` remains available but will use the same centrally defined step groups as `tools/workspace.py` where practical. The tracked status will contain stable framework inventories and privacy-policy outcomes. It will omit the generation timestamp, Git candidate counts and sizes, line-ending reminder counts, and large-file reminder counts so unrelated local files do not rewrite it. Exact candidate details remain available from ignored generated reports and command output.

## Documentation

The English and Chinese README files will become the operational entry points and show the unified command first. Detailed guides will stop duplicating manually maintained skill, tool, and environment inventories where generated status already provides them.

This repair will make targeted consistency edits rather than rewriting all documentation. Existing filenames and cross-links remain valid.

## Testing

Tests will be added before implementation for:

- concrete archive folders are ignored while `archives/README.md` remains trackable
- `.superpowers/` is ignored
- publication documentation contains the independent-repository rule and no task Git-exception recommendation
- generated task files contain lifecycle and handoff sections
- `summary.md` is created
- unified quick checks contain no report-generation steps
- unified full checks include report generation and verification
- command failures propagate a nonzero exit code

After implementation, run:

```powershell
python tools/test_workspace_tools.py
python tools/check_workspace.py
python tools/workspace.py check
python tools/workspace.py check --full
python tools/audit_git_readiness.py --max-mb 1
```

The final review must also inspect `git status`, the complete diff, and the outgoing file list. Existing unrelated untracked files must not be staged or modified.

## Compatibility

All existing documented helper commands remain valid. The unified command is an additive front door. Existing task folders, generated reports, and local tools are not migrated automatically.

## Success Criteria

- archiving a concrete task cannot make it a root Git candidate
- all publication guidance agrees on independent task repositories
- local Superpowers state no longer causes line-ending or Git-candidate noise
- a new task is ready for multi-turn continuation without manually inventing status sections
- users can remember one command for routine workspace checks
- routine checks are read-only
- all regression and workspace checks pass
