# Workspace Maintenance SOP

Use this SOP after broad workspace edits, before handoff, and periodically while the workspace evolves.

## Procedure

1. Run `python tools/run_workspace_maintenance.py`.
2. Review `WORKSPACE_STATUS.md`.
3. Review `outputs/first_commit_recommendation.md` before staging or committing.
4. Run `git ls-files tasks` and confirm only intended public task placeholders are tracked.
5. Update root docs when the workspace structure, tools, SOPs, prompts, or safety model changes.
6. Keep task-specific details inside task folders unless the knowledge is reusable across tasks.

## When To Run

- after adding or changing root tools
- after changing `.gitignore` or `.gitattributes`
- after adding, archiving, or reorganizing tasks
- before the first workspace commit
- before handing the workspace to another agent

## Safety Rules

- Do not delete cleanup candidates without explicit approval.
- Do not stage generated outputs, logs, dependency folders, raw media, or local secrets.
- Treat `python tools/audit_git_readiness.py` as the default commit gate.
- Treat `python tools/audit_git_readiness.py --max-mb 1` as a stricter review reminder, not an automatic failure.

## Expected Report

End with:

- maintenance command result
- Git candidate count
- readiness audit result
- workspace status freshness result
- line ending drift reminders, if any
- strict large-file reminders, if any
- private task tracking check
