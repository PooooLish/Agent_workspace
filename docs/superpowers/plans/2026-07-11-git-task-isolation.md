# Git Task Isolation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove private task-only commits from the root repository's unpublished history, keep every local task and sandbox file, and enforce independent repositories for explicitly published tasks.

**Architecture:** The root repository ignores all concrete task directories and concrete sandbox experiments while retaining only the sandbox policy README. A selected task can later become a nested independent Git repository without changing the root ignore policy. History cleanup uses a mixed reset to the verified remote base so tracked task files remain in the working tree, after which only approved framework policy files are committed.

**Tech Stack:** Git, PowerShell, Markdown, existing Python workspace audit tools

## Global Constraints

- Do not delete task or sandbox files.
- Do not use `git reset --hard` or force push.
- Do not access or print SSH keys, tokens, passwords, or other credentials.
- Concrete task directories remain private unless the user explicitly requests publication to a separate repository.
- Concrete experiment directories under `sandboxes/` remain local; only `sandboxes/README.md` is trackable.
- Preserve unrelated working-tree changes and stage only exact approved paths.

---

## File Structure

- Modify: `.gitignore` - enforce root-level privacy defaults for tasks and sandboxes.
- Modify: `README.md` - link the independent task publication workflow.
- Modify: `WORKSPACE_STATUS.md` - regenerate workspace registry coverage after adding the SOP.
- Modify: `tools/check_workspace.py` - enforce concrete sandbox privacy while retaining the policy README.
- Modify: `tools/generate_workspace_status.py` - describe independent task publication and sandbox policy accurately.
- Modify: `tools/test_workspace_tools.py` - cover sandbox privacy and publication wording.
- Create: `skills/visual_design_review/SKILL.md` - include the previously approved reusable skill already documented by the generated workspace status.
- Create: `sops/publish_independent_task.md` - define the explicit audit, initialization, review, and push procedure for a selected task.
- Preserve: `docs/superpowers/specs/2026-07-11-git-task-isolation-design.md` - retain the approved design after local history cleanup.
- Preserve: `docs/superpowers/plans/2026-07-11-git-task-isolation.md` - retain this implementation plan after local history cleanup.
- Create temporarily: `tmp/git-task-isolation-before.csv` - SHA-256 manifest for private files present in the unpublished commit range; ignored by Git.
- Create temporarily: `tmp/gitignore.before-task-isolation.bak` - backup of the current root ignore file; ignored by Git.

### Task 1: Preserve Local Data and Clean Unpublished History

**Files:**
- Preserve: `tasks/**`
- Preserve: `sandboxes/**`
- Preserve: `docs/superpowers/specs/2026-07-11-git-task-isolation-design.md`
- Preserve: `docs/superpowers/plans/2026-07-11-git-task-isolation.md`
- Create temporarily: `tmp/git-task-isolation-before.csv`
- Create temporarily: `tmp/gitignore.before-task-isolation.bak`

**Interfaces:**
- Consumes: local `master`, `origin/master`, the approved design commit, and the current working tree.
- Produces: `master` at the verified remote base with all local files still present as working-tree files.

- [ ] **Step 1: Verify branch, remote base, and an empty index**

Run:

```powershell
$git = 'D:\Apps\Git\cmd\git.exe'
$branch = & $git -c safe.directory=D:/MaHong/agent_workspace branch --show-current
$staged = & $git -c safe.directory=D:/MaHong/agent_workspace diff --cached --name-only
& $git -c safe.directory=D:/MaHong/agent_workspace status --short --branch
if ($branch -ne 'master') { throw "Expected master, found $branch." }
if ($staged) { $staged; throw 'Index is not empty; stop before rewriting history.' }
$localRemote = & $git -c safe.directory=D:/MaHong/agent_workspace rev-parse origin/master
$remoteLine = & $git ls-remote https://github.com/PooooLish/Agent_workspace.git refs/heads/master
$remoteSha = ($remoteLine -split '\s+')[0]
Write-Output "LOCAL_REMOTE=$localRemote"
Write-Output "REMOTE=$remoteSha"
if ($localRemote -ne $remoteSha) { throw 'origin/master is stale; stop before rewriting history.' }
```

Expected: branch is `master`; the cached diff is empty; local `origin/master` and GitHub `master` match. At plan creation they both resolve to `e1b8b2936367db7e3a7c065069e885aa88928138`. Stop if the branch, index, or SHA comparison differs.

- [ ] **Step 2: Record hashes for private files in outgoing history and back up `.gitignore`**

Run:

```powershell
New-Item -ItemType Directory -Path 'tmp' -Force | Out-Null
$git = 'D:\Apps\Git\cmd\git.exe'
$privatePaths = & $git -c safe.directory=D:/MaHong/agent_workspace diff --name-only origin/master..HEAD -- 'tasks' 'sandboxes'
$manifest = foreach ($relativePath in $privatePaths) {
  if (-not (Test-Path -LiteralPath $relativePath)) { throw "Missing private file before cleanup: $relativePath" }
  $hash = Get-FileHash -LiteralPath $relativePath -Algorithm SHA256
  [pscustomobject]@{ Path = $relativePath; Hash = $hash.Hash }
}
$manifest | Sort-Object Path | Export-Csv 'tmp/git-task-isolation-before.csv' -NoTypeInformation -Encoding UTF8
Copy-Item '.gitignore' 'tmp/gitignore.before-task-isolation.bak'
```

Expected: the manifest contains the eight deployment-task files in outgoing history; both temporary files exist; no source file changes or deletions occur. Generated directories and unrelated nested repositories are not traversed because `git reset --mixed` does not modify the working tree.

- [ ] **Step 3: Move `master` to the verified remote base without discarding files**

Run:

```powershell
$git = 'D:\Apps\Git\cmd\git.exe'
& $git -c safe.directory=D:/MaHong/agent_workspace reset --mixed origin/master
```

Expected: `HEAD` becomes `e1b8b29`; previously committed task files and the approved design document remain in the working tree. No hard reset is used.

- [ ] **Step 4: Verify every task and sandbox file was preserved**

Run:

```powershell
$before = Import-Csv 'tmp/git-task-isolation-before.csv'
$after = foreach ($item in $before) {
  if (-not (Test-Path -LiteralPath $item.Path)) { throw "Private file missing after cleanup: $($item.Path)" }
  $hash = Get-FileHash -LiteralPath $item.Path -Algorithm SHA256
  [pscustomobject]@{ Path = $item.Path; Hash = $hash.Hash }
}
$difference = Compare-Object $before $after -Property Path,Hash
if ($difference) { $difference; throw 'Task or sandbox files changed during history cleanup.' }
$git = 'D:\Apps\Git\cmd\git.exe'
& $git -c safe.directory=D:/MaHong/agent_workspace rev-list --left-right --count origin/master...HEAD
Test-Path 'docs/superpowers/specs/2026-07-11-git-task-isolation-design.md'
Test-Path 'docs/superpowers/plans/2026-07-11-git-task-isolation.md'
```

Expected: no hash differences; revision count is `0 0`; the design and implementation plan documents still exist.

### Task 2: Enforce Root Privacy and Document Independent Publication

**Files:**
- Modify: `.gitignore`
- Modify: `README.md`
- Modify: `WORKSPACE_STATUS.md`
- Modify: `tools/check_workspace.py`
- Modify: `tools/generate_workspace_status.py`
- Modify: `tools/test_workspace_tools.py`
- Create: `skills/visual_design_review/SKILL.md`
- Create: `sops/publish_independent_task.md`
- Preserve: `docs/superpowers/specs/2026-07-11-git-task-isolation-design.md`
- Preserve: `docs/superpowers/plans/2026-07-11-git-task-isolation.md`

**Interfaces:**
- Consumes: the approved design and the clean remote-based `master` from Task 1.
- Produces: framework rules that ignore all concrete tasks and all sandbox content, plus an explicit independent-repository SOP.

- [ ] **Step 1: Update root ignore rules**

Apply this exact task and sandbox section in `.gitignore`:

```gitignore
# Formal task folders and local task registries are private workspace data by default.
tasks/*
!tasks/README.md

# Sandbox experiments are local; the policy README remains trackable.
sandboxes/*
!sandboxes/README.md
```

Remove every `tasks/llm_101/` exception. Preserve all unrelated ignore rules.

- [ ] **Step 2: Create the independent task publication SOP**

Create `sops/publish_independent_task.md` with these mandatory stages:

```markdown
# Publish an Independent Task Repository

Use this SOP only after the user explicitly selects one `tasks/<task_name>/` directory for publication.

1. Confirm the exact task directory and separate GitHub repository name.
2. Read the root and task-level `AGENTS.md` and the task's `task.md`.
3. Audit the proposed repository for secrets, private data, logs, caches, generated output, local paths, and large files without printing secret values.
4. Create or review the task-local `.gitignore`.
5. Show the complete proposed first-commit file list and wait for user confirmation.
6. Initialize Git inside the selected task directory only.
7. Commit only the confirmed files and verify the commit contents.
8. Add only the confirmed independent remote and push only after explicit approval.

Never modify the root `.gitignore` to publish a task. Never publish a directory under `sandboxes/`.
```

- [ ] **Step 3: Link the SOP from `README.md`**

Add this paragraph after the task-creation section:

```markdown
## How to publish a task independently

Concrete task folders remain private to the root workspace repository. When a task has a real deliverable and should be published, follow `sops/publish_independent_task.md` to initialize that task directory as a separate Git repository. Never publish a directory under `sandboxes/`.
```

- [ ] **Step 4: Verify ignore behavior before staging**

Run:

```powershell
$git = 'D:\Apps\Git\cmd\git.exe'
& $git -c safe.directory=D:/MaHong/agent_workspace check-ignore -v --no-index tasks/llm_101/task.md
& $git -c safe.directory=D:/MaHong/agent_workspace check-ignore -v --no-index tasks/opencode_wsl_deployment/task.md
& $git -c safe.directory=D:/MaHong/agent_workspace check-ignore -v --no-index sandboxes/mini_game_test/index.html
& $git -c safe.directory=D:/MaHong/agent_workspace check-ignore -q --no-index tasks/README.md
Write-Output "TASKS_README_IGNORE_EXIT=$LASTEXITCODE"
```

Expected: both concrete task files and the sandbox file report matching ignore rules; `TASKS_README_IGNORE_EXIT=1` because `tasks/README.md` remains trackable.

- [ ] **Step 5: Regenerate workspace status**

Run:

```powershell
Copy-Item 'WORKSPACE_STATUS.md' 'tmp/workspace-status.before-task-isolation.bak' -Force
$env:GIT_CONFIG_COUNT='1'
$env:GIT_CONFIG_KEY_0='safe.directory'
$env:GIT_CONFIG_VALUE_0='D:/MaHong/agent_workspace'
python tools/generate_workspace_status.py
```

Expected: `WORKSPACE_STATUS.md` lists `sops/publish_independent_task.md`; the backup remains under ignored `tmp/`.

- [ ] **Step 6: Stage only approved framework files**

Run:

```powershell
$git = 'D:\Apps\Git\cmd\git.exe'
& $git -c safe.directory=D:/MaHong/agent_workspace add -- '.gitignore' 'README.md' 'WORKSPACE_STATUS.md' 'sops/publish_independent_task.md' 'docs/superpowers/specs/2026-07-11-git-task-isolation-design.md' 'docs/superpowers/plans/2026-07-11-git-task-isolation.md' 'tools/check_workspace.py' 'tools/generate_workspace_status.py' 'tools/test_workspace_tools.py' 'skills/visual_design_review/SKILL.md'
& $git -c safe.directory=D:/MaHong/agent_workspace diff --cached --name-status
& $git -c safe.directory=D:/MaHong/agent_workspace diff --cached --check
```

Expected: exactly ten approved paths are staged and the cached diff check exits `0`.

- [ ] **Step 7: Commit the policy**

Run:

```powershell
$git = 'D:\Apps\Git\cmd\git.exe'
& $git -c safe.directory=D:/MaHong/agent_workspace commit -m "chore: isolate private tasks from workspace git"
```

Expected: one new framework-only commit on top of `origin/master`.

### Task 3: Verify Root Push Readiness

**Files:**
- Verify only: root Git history and working tree

**Interfaces:**
- Consumes: the framework-only commit from Task 2.
- Produces: evidence that outgoing history contains no concrete task or sandbox files.

- [ ] **Step 1: Inspect outgoing history and paths**

Run:

```powershell
$git = 'D:\Apps\Git\cmd\git.exe'
& $git -c safe.directory=D:/MaHong/agent_workspace rev-list --left-right --count origin/master...HEAD
& $git -c safe.directory=D:/MaHong/agent_workspace log --oneline origin/master..HEAD
$outgoing = & $git -c safe.directory=D:/MaHong/agent_workspace diff --name-only origin/master..HEAD
$outgoing
if ($outgoing -match '^(tasks/(?!README\.md)|sandboxes/(?!README\.md))') { throw 'Private task or sandbox experiment path found in outgoing history.' }
```

Expected: branch is ahead by one framework commit; no concrete task or sandbox path appears.

- [ ] **Step 2: Run repository safety audits**

Run:

```powershell
$env:GIT_CONFIG_COUNT='1'
$env:GIT_CONFIG_KEY_0='safe.directory'
$env:GIT_CONFIG_VALUE_0='D:/MaHong/agent_workspace'
python tools/audit_git_readiness.py --max-mb 1
python tools/check_workspace.py
python tools/test_workspace_tools.py
python tools/audit_line_endings.py --strict
python tools/generate_workspace_status.py
python tools/verify_workspace_status.py
```

Expected: readiness, workspace, tool tests, and status verification pass. If the strict line-ending audit reports unrelated untracked `.superpowers/` files, report them separately and do not stage them as part of this plan. If status regeneration changes `WORKSPACE_STATUS.md`, amend only that generated file and this plan into the unpublished framework commit, then run status verification again.

- [ ] **Step 3: Verify local data and final scope once more**

Run:

```powershell
$before = Import-Csv 'tmp/git-task-isolation-before.csv'
$after = foreach ($item in $before) {
  if (-not (Test-Path -LiteralPath $item.Path)) { throw "Private file missing after cleanup: $($item.Path)" }
  $hash = Get-FileHash -LiteralPath $item.Path -Algorithm SHA256
  [pscustomobject]@{ Path = $item.Path; Hash = $hash.Hash }
}
$difference = Compare-Object $before $after -Property Path,Hash
if ($difference) { $difference; throw 'Local private data changed.' }
$git = 'D:\Apps\Git\cmd\git.exe'
& $git -c safe.directory=D:/MaHong/agent_workspace status --short --branch
```

Expected: no task or sandbox hash differences; unrelated existing working-tree changes remain uncommitted; `master` contains only the approved outgoing framework commit.

- [ ] **Step 4: Stop before push**

Report the final outgoing commit and file list. Do not push until the user gives a separate explicit instruction.
