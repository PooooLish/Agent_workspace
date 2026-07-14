# README Language Navigation Design

## Goal

Make the GitHub repository documentation easy to navigate in English and Simplified Chinese while keeping English as the default repository landing page.

## Scope

- Add a compact language switcher to `README.md` and `README.zh-CN.md`.
- Mark the current language in bold and link the other language with a relative Markdown link.
- Add a documentation section to each README.
- Link the English README to `WORKSPACE_GUIDE.md` and the Chinese README to `WORKSPACE_GUIDE.zh-CN.md`.
- Keep all links relative so they work on GitHub and in local Markdown viewers.

## Presentation

The language switcher appears immediately below the title:

```text
English | 简体中文
```

The documentation section appears before the directory overview so the detailed guide is discoverable without scanning the full README.

## Verification

- Confirm all four relative links resolve to tracked files.
- Run the workspace quick check.
- Run `git diff --check`.
- Confirm unrelated local task documents remain untracked.
