# Workspace Documentation

This directory contains durable documentation for the reusable workspace framework.

## Placement Rules

- `framework/` contains lasting architecture, privacy, and operating-model decisions for the root workspace.
- Simple, low-risk, localized changes do not create standalone specifications or implementation plans.
- Task-specific designs and plans belong inside the owning task, preferably under `tasks/<task_name>/docs/superpowers/`.
- Root-level `docs/superpowers/` is intentionally ignored and must not be committed.
- Completed step-by-step plans should be removed when they no longer serve as an operating reference.

## Current Framework Decisions

- [`framework/git-task-isolation.md`](framework/git-task-isolation.md): root Git privacy and independent task repository boundaries.
- [`framework/task-lifecycle.md`](framework/task-lifecycle.md): task complexity, recovery, verification, and closeout rules.
- [`framework/workspace-efficiency.md`](framework/workspace-efficiency.md): workspace commands, handoff, privacy checks, and deterministic maintenance behavior.
