# New Task SOP

1. Choose a clear task name in snake_case or kebab-case.
2. Classify the task as `simple`, `standard`, or `complex`.
3. Run `python tools/workspace.py new <task_name> --complexity <level>`.
4. Open `tasks/<task_name>/task.md` and write the goal, non-goals, constraints, inputs, acceptance criteria, and verification commands.
5. Read the workspace `AGENTS.md` and the new task's `AGENTS.md`.
6. Do all task work inside that task folder.
7. Keep outputs in `outputs/`, scratch files in `tmp/`, and logs in `logs/`.
8. Run `python tools/workspace.py doctor <task_name>` after filling the task state.
9. Update `README.md` inside the task folder if the workflow changes.

Keep `Status`, `Progress`, `Next action`, and `Blockers` current after meaningful work so another agent can resume without reconstructing the task history. Use the generated `summary.md` for the final outcome, changes, verification, and open issues.

Simple tasks must not create standalone specification or plan files. Complex
tasks use `docs/superpowers/` for task-local planning and
`coordination/contract.md` for multi-agent boundaries.
