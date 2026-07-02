# New Task SOP

1. Choose a clear task name in snake_case or kebab-case.
2. Run `python tools/make_task.py <task_name>`.
3. Open `tasks/<task_name>/task.md` and write the goal, constraints, inputs, and expected output.
4. Read the workspace `AGENTS.md` and the new task's `AGENTS.md`.
5. Do all task work inside that task folder.
6. Keep outputs in `outputs/`, scratch files in `tmp/`, and logs in `logs/`.
7. Update `README.md` inside the task folder if the workflow changes.
