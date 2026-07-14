# Tasks

Formal task folders live here during local work.

Task folders are ignored by Git by default because they often contain user-specific work, generated files, local notes, media, or private project context.

Keep reusable, cross-task knowledge in the root workspace folders such as `skills/`, `sops/`, `prompts/`, and `envs/`.

If a task must be shared, review it deliberately and initialize an independent Git repository inside that task directory. Never add a concrete task to the workspace root repository.

If you want a local registry, use `tasks/INDEX.md`; it is private by default because `tasks/*` is ignored.
