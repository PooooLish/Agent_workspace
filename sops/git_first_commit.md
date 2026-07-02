# Git First Commit SOP

Use this SOP before creating the first workspace commit or any broad structural commit.

## Procedure

1. Run `python tools/check_workspace.py`.
2. Run `python tools/audit_git_readiness.py`.
3. Run `python tools/summarize_git_candidates.py`.
4. Run `python tools/prepare_first_commit_report.py`.
5. Review `outputs/first_commit_recommendation.md`.
6. Confirm that generated outputs, logs, dependency folders, raw media, and local secrets are ignored.
7. Confirm that pending cleanup items in `tasks/INDEX.md` are either removed with approval or ignored.
8. Stage only the intended baseline files.
9. Run the checks again after staging if the staged set is broad.

## Safety rules

- Do not stage real secrets, credentials, private keys, or local `.env` files.
- Do not stage dependency folders such as `node_modules/`.
- Do not stage raw media, generated renders, logs, caches, or temporary files unless explicitly intended.
- Do not stage local backup files such as `*.bak`; keep the canonical file instead.
- Public site assets may be staged when source code or docs reference them and the readiness audit passes.
- Do not delete cleanup candidates without explicit approval.

## Expected report

End with:

- candidate file count
- readiness audit result
- first commit recommendation path
- notable large files, if any
- files or directories intentionally excluded
- remaining cleanup items
