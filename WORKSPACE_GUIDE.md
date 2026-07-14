# Workspace Guide

<details open>
<summary><strong>English</strong></summary>

This document is the maintainable master guide for `D:\MaHong\agent_workspace`. It is intended to help a future you, or any coding agent working with you, understand the purpose, structure, components, workflows, and maintenance model of the entire workspace from a single file.

## 1. Purpose

This workspace is a personal operations hub for coding agents such as Codex, Claude Code, OpenCode, and Aider.

It exists to solve four recurring problems:

1. Keep shared rules and habits in one place.
2. Isolate formal tasks from temporary experiments.
3. Reuse prompts, SOPs, and skill cards instead of reinventing them.
4. Make work easier to audit, hand off, archive, and resume later.

The design philosophy is:

- safety first
- task isolation
- minimal changes
- reusable workflows
- human-readable documentation

Primary commands:

```powershell
python tools/workspace.py new my_task
python tools/workspace.py check
python tools/workspace.py check --full
```

## 2. Current Root Structure

The workspace currently contains:

- `AGENTS.md`
- `README.md`
- `WORKSPACE_GUIDE.md`
- `WORKSPACE_STATUS.md`
- `.gitattributes`
- `.gitignore`
- `.git/`
- `skills/`
- `sops/`
- `prompts/`
- `tools/`
- `envs/`
- `tasks/`
- `sandboxes/`
- `archives/`
- `secrets/`

Each top-level item has a specific responsibility and should stay focused on that role.

## 3. Root Governance Files

### `AGENTS.md`

This is the root operating policy for agents.

It defines:

- the global role of the agent
- core safety rules
- the default work loop
- task isolation rules
- file modification rules

It is the most important behavioral file in the workspace. Any agent working in this repository should read it first.

### `README.md`

This is the bilingual short overview. Its English section is open by default, and its Simplified Chinese section can be expanded on the same GitHub page.

The Chinese Markdown files are UTF-8. On Windows PowerShell, use explicit UTF-8 when reading them from the terminal:

```powershell
Get-Content -Raw -Encoding UTF8 README.md
Get-Content -Raw -Encoding UTF8 WORKSPACE_GUIDE.md
```

### `.gitignore`

This file protects the repository from accidentally tracking:

- `.env` files
- key and certificate files
- `outputs/`, `tmp/`, and `logs/`
- Python cache directories
- virtual environments
- large model artifacts
- editor metadata

Its job is to keep the repository clean and reduce the chance of leaking secrets or committing generated noise.

### `.gitattributes`

This file keeps Git diffs and checkouts stable across Windows and Unix-like environments.

It defines:

- LF endings for most text files
- CRLF endings for Windows command scripts
- binary handling for images, media, archives, model artifacts, and other non-text files

Use it to avoid noisy line-ending changes and accidental binary diffs.

### `WORKSPACE_STATUS.md`

This is the current-state companion to the long-form guide.

It records:

- latest health-check status
- Git readiness status
- workspace baseline recommendation summary
- key maintenance commands
- ignored/generated report notes
- task privacy and Git baseline notes

Regenerate it with `python tools/generate_workspace_status.py` after broad workspace maintenance, before or after broad structural commits, or whenever the workspace operating model changes materially.

### `.git/`

The workspace has already been initialized as a Git repository. This enables version control for the workspace structure, prompts, templates, scripts, and future task changes if you choose to commit them.

## 4. Shared Reusable Components

### `skills/`

This directory stores reusable skill cards. A skill card is not code; it is a compact operational guide for a repeatable type of work.

Current skills:

- `code_review/`
- `python_project_setup/`
- `cli_tool_setup/`
- `linux_debugging/`
- `documentation_writer/`

Each `SKILL.md` follows the same format:

- Purpose
- When to use
- Procedure
- Safety rules
- Expected output

Role of each current skill:

- `code_review`: review code for bugs, regressions, and missing tests.
- `python_project_setup`: create or organize a small Python task safely.
- `cli_tool_setup`: document or standardize local CLI workflows.
- `linux_debugging`: debug shell, process, path, or environment issues methodically.
- `documentation_writer`: turn project context into clear and practical docs.

When to extend this directory:

- add a new skill when the same kind of work appears repeatedly across tasks
- avoid adding one-off project notes here

### `sops/`

This directory stores Standard Operating Procedures.

Current SOPs:

- `new_task.md`
- `debug_error.md`
- `modify_existing_project.md`
- `setup_external_api.md`
- `task_closeout.md`
- `safe_shell_commands.md`
- `git_first_commit.md`
- `workspace_maintenance.md`

Role of each SOP:

- `new_task.md`: how to create and begin a formal task
- `debug_error.md`: how to perform minimal debugging from a real error
- `modify_existing_project.md`: how to change an existing codebase safely
- `setup_external_api.md`: how to integrate external APIs without storing real keys
- `task_closeout.md`: how to wrap up a task, summarize it, and prepare archival
- `safe_shell_commands.md`: which commands are risky and require manual confirmation
- `git_first_commit.md`: how to inspect Git candidates before the first workspace commit
- `workspace_maintenance.md`: how to run routine workspace health, audit, and status maintenance

When to use an SOP:

- when the work has a repeatable sequence
- when mistakes are costly
- when you want agents to behave consistently

### `prompts/`

This directory stores reusable prompt templates for different agents and workflows.

Current prompt templates:

- `codex_default.md`
- `claude_code_default.md`
- `opencode_default.md`
- `aider_default.md`
- `safe_debug.md`
- `safe_setup.md`
- `code_review.md`

Common behavior enforced by these prompts:

- read `AGENTS.md`, `README.md`, and `task.md` first
- do not delete files
- do not edit outside the intended task scope
- do not store or reveal real API keys
- propose a short plan before editing
- run minimal verification after changes
- finish with changed files, commands run, and verification result

Use these prompts as reliable starting points, then customize per task if needed.

## 5. Helper Scripts

### `tools/make_task.py`

This script creates a formal task folder under `tasks/<task_name>/`.

Usage:

```bash
python tools/make_task.py task_name
```

What it creates:

- `AGENTS.md`
- `task.md`
- `README.md`
- `.gitignore`
- `src/`
- `scripts/`
- `data/`
- `outputs/`
- `tests/`
- `tmp/`
- `logs/`
- `docs/`

Important behavior:

- it does not overwrite existing files
- it reports created items and skipped items
- it gives every task a local working structure immediately

This is the main entry point for creating new formal work.

### `tools/check_workspace.py`

This script checks whether the workspace contains its required baseline components.

Usage:

```bash
python tools/check_workspace.py
```

What it checks:

- `AGENTS.md`
- `README.md`
- `.gitignore`
- `skills/`
- `sops/`
- `prompts/`
- `tools/`
- `envs/`
- `tasks/`
- `sandboxes/`
- `archives/`
- `secrets/`
- `secrets/env.example`

This is useful after manual changes, cleanup work, or future refactors.

### `tools/audit_git_readiness.py`

This script audits files that Git would track before staging or committing.

Usage:

```bash
python tools/audit_git_readiness.py
```

Use a stricter threshold when preparing a careful baseline or broad structural commit:

```bash
python tools/audit_git_readiness.py --max-mb 1
```

What it checks:

- large candidate files that are not ignored
- sensitive-looking candidate file names
- secret-like content in small text files

Important behavior:

- it uses Git's own exclude rules to inspect only trackable candidates
- it reports paths and pattern names, not secret values
- it exits with code `2` when it finds review-worthy issues

Run it before any commit that touches broad workspace structure.

### `tools/summarize_git_candidates.py`

This script summarizes files that Git would track before staging or committing.

Usage:

```bash
python tools/summarize_git_candidates.py
```

What it reports:

- candidate file count
- total candidate size
- counts by top-level area or task
- counts by file extension
- largest candidate files

Use it with `sops/git_first_commit.md` to review the intended baseline before staging.

### `tools/test_workspace_tools.py`

This script runs lightweight regression tests for the workspace maintenance tools.

Usage:

```bash
python tools/test_workspace_tools.py
```

It uses only the Python standard library and avoids creating files except through explicit dry-run checks.

### `tools/audit_line_endings.py`

This script audits candidate file line endings against `.gitattributes`.

Usage:

```bash
python tools/audit_line_endings.py --strict
```

Use `--fix` when you intentionally want to rewrite candidate files to the configured policy.

### `tools/prepare_baseline_report.py`

This script writes a Markdown recommendation for the current workspace baseline.

Usage:

```bash
python tools/prepare_baseline_report.py
```

Default output:

- `outputs/first_commit_recommendation.md`

What it does:

- separates recommended baseline files from files needing manual confirmation
- documents intentionally excluded or deferred paths
- includes the verification commands to rerun before staging

The output lives in `outputs/`, so it is intentionally not tracked by Git unless explicitly moved.

The older `tools/prepare_first_commit_report.py` command remains available for compatibility.

### `tools/verify_baseline_report.py`

This script verifies that the generated baseline report still matches the current Git candidates.

Usage:

```bash
python tools/verify_baseline_report.py
```

### `tools/generate_workspace_status.py`

This script regenerates `WORKSPACE_STATUS.md` from the current checks and Git candidate state.

Usage:

```bash
python tools/generate_workspace_status.py
```

It runs the workspace check, Git readiness audit, baseline report generation, and strict large-file reminder, then writes the current-state summary.

### `tools/run_workspace_maintenance.py`

This script runs the standard maintenance chain in order:

- workspace structure check
- tool regression tests
- Git readiness audit
- Git candidate summary
- baseline report generation
- workspace status regeneration
- strict 1 MB large-file reminder

Usage:

```bash
python tools/run_workspace_maintenance.py
```

The strict large-file reminder is allowed to return a non-zero exit code so known public assets can still be reviewed without failing the default maintenance run.

## 6. Environment Notes

### `envs/`

This directory stores environment-specific usage notes, not installers.

Current files:

- `base_python.md`
- `node_tools.md`
- `codex_cli.md`
- `claude_code.md`
- `opencode.md`
- `aider.md`
- `external_api.md`

What these files are for:

- record conventions
- explain local workflows
- describe safe setup patterns
- document provider usage without storing secrets

#### `envs/opencode.md`

This is currently the most developed environment note.

It records:

- that OpenCode CLI is installed
- that `opencode --version` was verified
- the recommended launch point: inside a task directory
- useful commands such as `opencode .`, `opencode run`, `opencode web`, and `opencode providers list`
- the preferred provider setup pattern: environment variables
- the expected closing report format

#### `envs/external_api.md`

This file defines the workspace policy for API integrations:

- never store real keys in tracked files
- prefer environment variables
- use placeholder templates like `env.example`
- do not commit local secret files

The other environment files are still lightweight and act more as placeholders for future expansion.

## 7. Secrets Policy

### `secrets/`

This directory is intentionally template-only.

Current files:

- `README.md`
- `env.example`

#### `secrets/README.md`

This explains the policy:

- do not store real secrets here
- real credentials should live in system environment variables or a password manager
- agents should not print, store, or commit real secrets

#### `secrets/env.example`

This is a placeholder template containing:

- `OPENAI_API_KEY=`
- `ANTHROPIC_API_KEY=`
- `DEEPSEEK_API_KEY=`
- `OPENROUTER_API_KEY=`
- `GEMINI_API_KEY=`

It should remain empty except for variable names.

## 8. Task System

### `tasks/`

This is where all formal work belongs.

Rule:

- one formal task = one dedicated folder under `tasks/`

Each task should ideally contain:

- local `AGENTS.md`
- local `task.md`
- local `README.md`
- source code
- scripts
- tests
- outputs
- temp files
- logs
- docs

### Task privacy

Concrete task folders are local-private by default and are ignored by Git through `.gitignore`.

The tracked task placeholder is:

- `tasks/README.md`

Use task-local files for active task status, registries, and cleanup notes. Publish a selected task only after deliberate review by initializing an independent Git repository inside that task directory.

When creating a new formal task:

1. Create the task with `python tools/make_task.py <task_name>`.
2. Fill in `tasks/<task_name>/task.md`.
3. Keep task-specific status details inside the task folder.
4. Leave the task folder ignored by the root repository; use an independent task repository when publication is approved.

## 9. Sandboxes and Archives

### `sandboxes/`

This is reserved for temporary experiments.

Use it for:

- quick prototypes
- throwaway tests
- environment experiments
- one-off investigations

Do not treat it as a permanent project area.

### `archives/`

This is reserved for completed or abandoned tasks.

A task should move here only after:

- verification is done
- the task has enough documentation to understand later
- useful outputs are preserved

Both `sandboxes/` and `archives/` include local README files so their purpose remains visible in the Git baseline even when they contain no active experiment or archived task.

Concrete archived task folders remain local-private and ignored by the workspace root repository.

## 10. Installed External Agent Tooling

This workspace also connects to tools outside the repository itself.

### Git

Git was initialized for the workspace. The repository exists and can track future changes.

### OpenCode

OpenCode CLI is installed on the machine and is already reflected in `envs/opencode.md`.

Recommended usage:

```powershell
cd D:\MaHong\agent_workspace\tasks\my_task_name
opencode .
```

Recommended provider pattern:

```powershell
$env:OPENAI_API_KEY="your_key_here"
opencode .
```

### Global Codex skills

Global Codex skills and plugins live outside this repository and can change independently. Inspect the current Codex session when that inventory matters; use `WORKSPACE_STATUS.md` as the generated source for skills owned by this workspace.

## 11. Recommended Daily Workflow

The intended day-to-day workflow is:

1. Create a task with `python tools/workspace.py new <task_name>`.
2. Fill in `tasks/<task_name>/task.md`.
3. Enter that task folder.
4. Start the agent of choice.
5. Ask the agent to read:
   - workspace `AGENTS.md`
   - local `AGENTS.md`
   - local `task.md`
6. Keep all edits within the task unless shared assets truly need updating.
7. Run minimal verification after each meaningful change.
8. Finish with a summary and archive later if appropriate.

## 12. What Is Mature vs. What Is Still Lightweight

Currently mature:

- workspace structure
- root rules
- secrets policy
- task scaffolding
- workspace checking
- prompt starters
- baseline OpenCode documentation
- private task-folder policy

Currently lightweight:

- most environment notes besides OpenCode
- task archive practices, because no real tasks are archived yet
- sandbox conventions, because no experiments are stored yet
- advanced per-agent customization for prompts and skills

This is expected. The workspace is intentionally scaffold-first and should evolve with real use.

## 13. Maintenance Rules

To keep the workspace maintainable:

- keep root files generic and reusable
- keep task-specific details inside task folders
- add new skills only when a workflow repeats
- add new SOPs only when a sequence deserves standardization
- update `envs/` when tool usage changes
- update `secrets/env.example` only for placeholder names, never real values
- prefer adding new docs over rewriting unrelated existing ones
- back up important notes before major changes

## 14. Suggested Future Improvements

Good next improvements would be:

- add a dedicated OpenCode prompt template under `prompts/`
- add bilingual task templates
- expand `envs/codex_cli.md`, `envs/claude_code.md`, and `envs/aider.md`
- add a `summary.md` convention to real tasks
- add a private task registry convention inside task folders or `tasks/` if task volume grows
- define naming conventions for archives and sandboxes

## 15. Quick Reference

Use the unified workspace front door:

```bash
python tools/workspace.py new my_task
python tools/workspace.py check
python tools/workspace.py check --full
```

Launch OpenCode in a task:

```powershell
cd D:\MaHong\agent_workspace\tasks\my_task
opencode .
```

Set a provider key for the current shell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

## 16. Summary

This workspace already provides a solid shared operating layer for agent-assisted development:

- a rule system
- task isolation
- prompt templates
- SOPs
- helper scripts
- secret-handling policy
- environment notes
- a private task-folder policy
- OpenCode integration

Its main value is not any single file. Its value comes from how all the parts work together:

- root rules constrain behavior
- prompts shape execution
- SOPs standardize process
- tools reduce setup friction
- tasks isolate work
- secrets stay out of the repository
- environment notes connect local tools to safe workflows

Treat this file as the single source of truth for understanding the workspace at a glance, and update it whenever the structure or working model changes materially.

</details>

<details>
<summary><strong>简体中文</strong></summary>

这份文档是 `D:\MaHong\agent_workspace` 的可维护总说明，目标是让你或未来协作的 agent 通过这一份文档理解整个 workspace 的定位、目录结构、核心组件、使用流程和维护方式。

## 1. 工作区定位

这个 workspace 是个人长期使用的 agent 工作中枢，用来统一管理 Codex、Claude Code、OpenCode、Aider 等 coding agent 的共用规则、提示词、SOP、环境说明和任务模板。

它主要解决四类问题：

1. 把共享规则和工作习惯放在一个地方。
2. 把正式任务和临时实验隔离开。
3. 复用 prompts、SOP 和 skills，而不是每次从头编写。
4. 让工作过程更容易审查、接续、归档和回看。

设计原则：

- 安全优先
- 任务隔离
- 最小修改
- 流程可复用
- 文档可读、可维护

日常统一入口：

```powershell
python tools/workspace.py new my_task
python tools/workspace.py check
python tools/workspace.py check --full
```

## 2. 当前根目录结构

当前工作区根目录包含：

- `AGENTS.md`
- `README.md`
- `WORKSPACE_GUIDE.md`
- `WORKSPACE_STATUS.md`
- `.gitattributes`
- `.gitignore`
- `skills/`
- `sops/`
- `prompts/`
- `tools/`
- `envs/`
- `tasks/`
- `sandboxes/`
- `archives/`
- `secrets/`

这些顶层项目各自承担不同职责，维护时应尽量保持边界清晰。

## 3. 根层治理文件

### `AGENTS.md`

这是整个工作区的根规则文件，也是最重要的行为边界说明。它定义 agent 的全局角色、安全规则、默认工作循环、规则层级、任务隔离和文件修改规则。

规则层级：

- workspace 根 `AGENTS.md` 是全局规则。
- 每个任务自己的 `AGENTS.md` 是局部规则。
- 局部规则只能补充或收紧全局规则。
- 如果两者冲突，以更严格者为准。

### `README.md`

这是中英文合并的简要总览。英文默认展开，简体中文可以在同一个 GitHub 仓库首页展开，不需要跳转到另一个文件。

### `WORKSPACE_GUIDE.md`

这是中英文合并的完整工作区指南，也是理解工作区结构和维护方式的主要入口。

### `.gitignore`

负责避免把 `.env`、密钥、生成输出、日志、缓存、虚拟环境、大型模型文件和具体私有任务纳入根仓库。

### `.gitattributes`

负责统一跨 Windows 和 Unix 环境的文本换行及二进制文件处理方式，减少无意义 Git 差异。

### `WORKSPACE_STATUS.md`

这是自动生成的当前状态摘要。工作区结构或维护模型发生较大变化后，运行以下命令刷新：

```powershell
python tools/generate_workspace_status.py
```

## 4. 共享可复用组件

### `skills/`

存放跨多个任务可复用的技能卡。只有在多个任务中反复证明有价值的能力才应放在根 `skills/`。

当前通用 skills 包括：

- `code_review/`
- `python_project_setup/`
- `cli_tool_setup/`
- `linux_debugging/`
- `documentation_writer/`
- `visual_design_review/`

只对某个任务有用的 skill、经验或检查清单应放在：

```text
tasks/<task_name>/docs/skills/
```

### `sops/`

存放标准操作流程，例如新建任务、调试、修改已有项目、接入外部 API、任务收尾、安全命令、Git 提交和工作区维护。

### `prompts/`

存放给不同 agent 和工作场景使用的提示词模板。它们通常要求先读规则、限制修改范围、保护密钥、进行最小验证并汇报结果。

## 5. 辅助脚本

### `tools/workspace.py`

这是推荐的统一入口：

```powershell
python tools/workspace.py new my_task
python tools/workspace.py check
python tools/workspace.py check --full
```

- `new`：创建隔离的正式任务目录。
- `check`：执行日常只读检查。
- `check --full`：刷新维护报告并执行完整检查。

### 其他主要工具

- `tools/make_task.py`：创建任务骨架。
- `tools/check_workspace.py`：检查工作区基础结构和策略。
- `tools/audit_git_readiness.py`：检查大文件、敏感命名和疑似 secret。
- `tools/audit_line_endings.py`：检查 `.gitattributes` 换行策略。
- `tools/test_workspace_tools.py`：运行工作区工具回归测试。
- `tools/generate_workspace_status.py`：刷新 `WORKSPACE_STATUS.md`。
- `tools/run_workspace_maintenance.py`：运行完整维护链。

## 6. 环境说明

### `envs/`

这里存放如何安全使用本地工具和环境的说明，而不是未知安装脚本。当前覆盖 Python、Node.js、Codex CLI、Claude Code、OpenCode、Aider 和外部 API。

环境文件用于记录：

- 使用约定
- 本地工作流
- 安全配置方式
- 不包含真实 secret 的 provider 配置方式

## 7. Secrets 策略

### `secrets/`

这个目录只存放模板：

- 不保存真实 API key、token、SSH key 或密码。
- 真实凭据应放在系统环境变量或密码管理器中。
- `secrets/env.example` 只保留变量名和空值。
- Agent 不应打印、保存或提交真实凭据。

## 8. 正式任务系统

### `tasks/`

所有正式任务都应该放在 `tasks/<task_name>/` 下。每个任务应拥有自己的规则、目标、源码、测试、输出、日志和文档。

具体任务目录默认被根 `.gitignore` 排除，只在本地保存。根仓库只跟踪 `tasks/README.md` 作为政策说明。

需要发布某个任务时，应先人工审查，然后在该任务目录内部初始化独立 Git 仓库，不得把具体任务加入 workspace 根仓库。

## 9. Sandboxes 与 Archives

### `sandboxes/`

用于快速原型、一次性验证和临时环境实验。具体实验永远不应上传根仓库。

### `archives/`

用于已完成或明确废弃的任务。具体归档任务仍然保持本地私有；需要发布时使用独立仓库。

## 10. 外部 Agent 工具

Git 已用于跟踪工作区框架。Codex、Claude Code、OpenCode 和 Aider 的全局插件或 skills 位于本仓库之外，可能独立变化。

推荐在具体任务目录中启动 agent，例如：

```powershell
cd D:\MaHong\agent_workspace\tasks\my_task_name
opencode .
```

## 11. 推荐日常工作流

1. 在根目录运行 `python tools/workspace.py new <task_name>`。
2. 填写 `tasks/<task_name>/task.md`。
3. 进入该任务目录。
4. 让 agent 读取根规则和任务规则。
5. 除非确有必要，否则只修改当前任务目录。
6. 把任务私有 skill 放在 `docs/skills/`。
7. 每次有意义修改后进行最小验证。
8. 完成后更新总结，需要时再归档。

## 12. 维护规则

- 根目录文件保持通用和可复用。
- 任务细节只放在任务目录。
- 只有重复出现的能力才提升为根级 skill。
- 工具使用方式变化时同步更新 `envs/`。
- `secrets/env.example` 只维护变量名。
- 大范围框架修改前运行 `python tools/workspace.py check --full`。

## 13. 总结

这个 workspace 的价值来自各部分协同：

- 根规则约束行为。
- prompts 规范执行入口。
- SOP 固化流程。
- tools 降低建任务和检查成本。
- tasks 隔离正式工作。
- `docs/skills/` 承接任务私有知识。
- 根 `skills/` 承接跨任务公共能力。
- secrets 保护敏感信息。
- envs 连接本地工具和安全工作流。

把这份文档作为理解整个 workspace 的单一入口，并在结构或工作模式发生实质变化时同步更新。

</details>
