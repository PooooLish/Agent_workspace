# Git Task Isolation Design

## Purpose

Keep the root `Agent_workspace` repository limited to reusable framework assets while allowing selected tasks with real deliverables to be published as independent GitHub repositories. Temporary sandbox work must never enter a normal Git publishing flow.

## Repository Boundaries

The root repository owns reusable workspace material such as operating rules, shared skills, SOPs, prompts, tools, and non-secret project configuration.

Formal task directories under `tasks/` are private by default. The root repository ignores every concrete task directory and tracks only `tasks/README.md`. A task becomes publishable only after the user explicitly selects it and requests publication.

Concrete sandbox experiment directories under `sandboxes/` are always local and ignored by the root repository. The root repository may track only `sandboxes/README.md` as a policy placeholder. Sandbox experiment content is not eligible for the task-publication workflow. If an experiment produces reusable knowledge, that knowledge must be rewritten into an appropriate shared skill, SOP, or document rather than publishing the sandbox itself.

## Independent Task Repositories

An explicitly selected task is published from its existing `tasks/<task_name>/` directory as a nested, independent Git repository. It receives its own Git history, ignore rules, remote, and GitHub repository. The root repository continues to ignore the entire task directory, including the nested `.git` directory.

Publishing a task requires a separate, explicit user instruction. The workflow must not infer publication from task completion, the presence of outputs, or a broad request to update the root workspace repository.

Before initializing or pushing an independent task repository, the agent must:

1. Confirm the exact task directory and intended GitHub repository.
2. Review the task for secrets, private data, generated artifacts, large files, logs, caches, and local environment details.
3. Create or verify a task-local `.gitignore`.
4. Show the proposed file set and obtain confirmation before the first push.
5. Initialize and push only the selected task repository.

## Root Ignore Policy

The root `.gitignore` must enforce these defaults:

```gitignore
tasks/*
!tasks/README.md

sandboxes/*
!sandboxes/README.md
```

There must be no task-specific allow rule in the root `.gitignore`. Publishing an independent task does not require changing the root ignore policy because the task repository is initialized and operated from inside the ignored task directory.

## Existing Local History Cleanup

The root `master` branch currently contains local, unpushed commits for a deployment-only task with no publishable deliverable. Those commits must be removed from the root branch's pending history while preserving all task files in the working tree.

The cleanup must satisfy all of these conditions:

- The root `master` branch returns to the current remote `origin/master` base before approved framework changes are reapplied.
- No task or sandbox file is deleted.
- The deployment task remains local and ignored.
- Existing unrelated working-tree changes remain intact.
- No force push is required because the unwanted commits were never published.

Before rewriting the local branch, verify that the remote branch has not moved and that the index contains no unrelated staged changes. Preserve the approved design commit separately, move `master` back to the verified remote base without discarding the working tree, then reapply only approved framework commits.

## Root Publication Checks

Before pushing the root repository, verify:

- `master` contains no paths under concrete `tasks/` directories.
- `master` contains no paths under `sandboxes/` except `sandboxes/README.md`.
- No task-specific exception exists in the root `.gitignore`.
- Secret, large-file, line-ending, and workspace checks have been run.
- The staged and outgoing file lists contain only intentional framework assets.
- The remote branch has not advanced unexpectedly.

## Failure Handling

If preserving the working tree and cleaning branch history cannot both be demonstrated safely, stop before changing branch history and report the conflicting paths. Do not use a hard reset, delete task files, or force push.

If an independent task audit finds sensitive or ambiguous content, keep the task local until the user explicitly resolves the finding.

## Success Criteria

- Root `master` has no unpushed task-only commits.
- All concrete task directories are ignored by the root repository.
- Every concrete sandbox experiment directory is ignored while `sandboxes/README.md` remains trackable.
- Existing task and sandbox files remain present locally.
- Selected tasks can later be initialized and pushed as independent repositories without changing root ignore rules.
- Root publication remains an explicit, reviewable framework-only operation.
