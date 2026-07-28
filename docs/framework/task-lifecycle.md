# Task Lifecycle

This document defines the workspace task lifecycle and the boundary between
lightweight tasks and durable planning artifacts.

## Design goals

- Keep Markdown and Git as the primary, human-readable state.
- Make task status and handoff information recoverable without replaying chat.
- Preserve the rule that simple work does not create specification or plan files.
- Keep task contents private to the root workspace repository.
- Require explicit intent before executing task-defined commands.

## Complexity levels

### Simple

Use for localized, low-risk work. Record the goal, acceptance criteria, progress,
next action, and verification commands in `task.md`. Do not create standalone
specification or plan files.

### Standard

Use for multi-file work that benefits from a durable task record but does not
need a separate specification. Maintain decisions, phase, progress, blockers,
and verification commands in `task.md`.

### Complex

Use for ambiguous, high-risk, cross-module, long-running, or multi-agent work.
Task-local specifications and plans may live under `docs/superpowers/`.
Multi-agent work must use `coordination/contract.md` to record task IDs,
dependencies, owners, worktrees, allowed paths, verification, and status.

## Lifecycle commands

The unified entry point is `python tools/workspace.py`.

```powershell
python tools/workspace.py new my_task --complexity standard
python tools/workspace.py status
python tools/workspace.py resume my_task
python tools/workspace.py doctor my_task
python tools/workspace.py verify my_task
python tools/workspace.py close my_task
```

`doctor` also accepts no task name to inspect every private task. `verify`
displays task-defined verification commands, while `verify my_task --run`
explicitly executes them inside the task.

Verification commands use one command per line. `--run` executes trusted shell
commands with the task directory as their working directory; it does not provide a sandbox.
Commands can still access parent paths, absolute paths, the network, and inherited
environment variables. Use Codex sandboxing, a container, or another restricted
executor when actual isolation is required.

`close` does not archive, publish, delete, or execute verification commands.
Those remain deliberate, separate actions.

## State ownership

`task.md` is the current execution state and `summary.md` is the final outcome.
There is no tracked central registry of private tasks. Generated workspace
inventory may describe the framework but must not expose task contents.

## Recovery packet

`resume` reports:

- task name, status, complexity, and phase
- goal and constraints
- durable decisions and progress
- last recorded verification information
- next action and blockers
- task repository branch and commit when available

Long logs stay in `logs/` and are not loaded unless the task requires them.

## Safety

- Verification is read-only unless `--run` is supplied.
- Task commands start in the selected task directory but are not path-isolated.
- Task names must pass the existing safe-name validation.
- Lifecycle tools never archive, publish, or delete tasks.
- Root Git checks continue to reject tracked private task content.

Legacy tasks without `Complexity` or `Phase` are interpreted as `standard`;
their phase is inferred from status. `close` adds the missing fields.
