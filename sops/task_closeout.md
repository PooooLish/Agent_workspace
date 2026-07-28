# Task Closeout SOP

1. Preview verification with `python tools/workspace.py verify <task_name>`.
2. Review every command, then explicitly run trusted commands with `python tools/workspace.py verify <task_name> --run`; this is not a sandbox.
3. Clean up task notes so another agent can understand the result.
4. Complete `summary.md` with goal, outcome, changes, verification, and open issues.
5. Run `python tools/workspace.py doctor <task_name>`.
6. Run `python tools/workspace.py close <task_name>` to mark the task completed.
7. Ensure outputs are in `outputs/` and stable docs are in `docs/`.
8. Move completed or abandoned tasks into `archives/` only as a separate, deliberate action.
9. Do not archive secrets or unnecessary temporary files.
10. Publish a selected task only through an independent Git repository inside that task directory.
