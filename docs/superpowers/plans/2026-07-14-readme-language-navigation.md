# README Language Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add bilingual README navigation and direct links to the matching English and Simplified Chinese workspace guides.

**Architecture:** Keep `README.md` as GitHub's English default landing page and use relative Markdown links for language switching. Each README links to the guide in the same language so navigation works both on GitHub and in local Markdown viewers.

**Tech Stack:** Markdown, relative repository links, Python workspace checks, Git validation.

## Global Constraints

- English remains the default `README.md` landing page.
- Only `README.md`, `README.zh-CN.md`, and this implementation plan are modified or created during implementation.
- Existing untracked task documents remain untracked.
- Links must be relative and resolve to tracked files.

---

### Task 1: Add README language and documentation navigation

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Test: `tools/workspace.py`

**Interfaces:**
- Consumes: tracked files `README.md`, `README.zh-CN.md`, `WORKSPACE_GUIDE.md`, and `WORKSPACE_GUIDE.zh-CN.md`.
- Produces: clickable relative links between both README files and from each README to its matching workspace guide.

- [x] **Step 1: Add navigation to the English README**

Insert below the title:

```markdown
**English** | [简体中文](README.zh-CN.md)
```

Insert before `## Directory overview`:

```markdown
## Documentation

- [English workspace guide](WORKSPACE_GUIDE.md)
- [简体中文说明](README.zh-CN.md)
```

- [x] **Step 2: Add navigation to the Chinese README**

Insert below the title:

```markdown
[English](README.md) | **简体中文**
```

Insert before `## 目录说明`:

```markdown
## 文档

- [中文工作区指南](WORKSPACE_GUIDE.zh-CN.md)
- [English README](README.md)
```

- [x] **Step 3: Verify relative link targets**

Run:

```powershell
@('README.md', 'README.zh-CN.md', 'WORKSPACE_GUIDE.md', 'WORKSPACE_GUIDE.zh-CN.md') | ForEach-Object { if (-not (Test-Path -LiteralPath $_)) { throw "Missing link target: $_" } }
```

Expected: exit code `0` with no output.

- [x] **Step 4: Run workspace and Git checks**

Run:

```powershell
python tools/workspace.py check
git diff --check
git status --short
```

Expected: 40 tests pass, the workspace structure check passes, `git diff --check` prints no errors, and only the two README files plus this plan are part of the intended change. The two pre-existing `2026-07-07-cs-interview-bagu-stats` documents remain untracked.

- [ ] **Step 5: Commit and push**

```powershell
git add -- README.md README.zh-CN.md docs/superpowers/plans/2026-07-14-readme-language-navigation.md
git commit -m "docs: add bilingual README navigation"
git push origin master
```

Expected: the commit succeeds and `master` is pushed to `origin`.
