# Agent Workspace

<details open>
<summary><strong>English</strong></summary>

This workspace is a personal, reusable home for learning and using Codex, Claude Code, OpenCode, Aider, and similar coding agents. It keeps shared rules, prompts, SOPs, and task folders in one place so each task stays isolated and repeatable.

## Documentation

- [English workspace guide](WORKSPACE_GUIDE.md)

## Directory overview

- `AGENTS.md`: root operating rules for all agents.
- `.gitattributes`: text, line-ending, and binary-file normalization rules.
- `skills/`: reusable capability notes and playbooks.
- `sops/`: standard operating procedures.
- `prompts/`: copy-paste prompt templates for different agents.
- `tools/`: small helper scripts for task creation and workspace checks.
- `envs/`: environment notes and setup templates.
- `WORKSPACE_STATUS.md`: latest health, audit, and commit-readiness status.
- `tasks/`: formal task folders for local work; concrete task folders are ignored by Git by default.
- `tasks/README.md`: tracked placeholder explaining the private task-folder policy.
- `sandboxes/`: temporary experiments.
- `archives/`: completed or abandoned task archives; concrete archive folders remain local-private.
- `secrets/`: templates only, never real secrets.

## How to create a new task

Run:

```bash
python tools/workspace.py new my_task
```

This creates `tasks/my_task/` with task-level docs, source folders, test folders, output folders, and local ignore rules.

Concrete task folders stay local by default. Keep task status, registries, and cleanup notes inside the task folder unless you deliberately decide to publish them.

## How to publish a task independently

Concrete task folders remain private to the root workspace repository. When a task has a real deliverable and should be published, follow `sops/publish_independent_task.md` to initialize that task directory as a separate Git repository. Never publish a concrete experiment directory under `sandboxes/`; only its policy README belongs to the root repository.

## How to check before committing

Run the quick, read-only check during routine framework work:

```bash
python tools/workspace.py check
```

Before a broad framework commit, run the full check that also regenerates maintenance reports:

```bash
python tools/workspace.py check --full
```

The readiness audit reports large Git candidates, sensitive-looking file names, and secret-like content without printing secret values.
Use `python tools/audit_git_readiness.py --max-mb 1` for a stricter large-file review.
The baseline recommendation report is written to `outputs/first_commit_recommendation.md`.
The workspace status summary is regenerated in `WORKSPACE_STATUS.md`.
For the first commit or any broad structural commit, follow `sops/git_first_commit.md`.
For individual compatibility commands and the detailed procedure, follow `sops/workspace_maintenance.md`.

## Notes for multilingual docs on Windows

The Chinese Markdown files are UTF-8. In Windows PowerShell, read them with explicit UTF-8 when needed:

```powershell
Get-Content -Raw -Encoding UTF8 README.md
Get-Content -Raw -Encoding UTF8 WORKSPACE_GUIDE.md
```

## How to work with Codex, Claude Code, OpenCode, or Aider

1. Enter a task folder under `tasks/<task_name>/`.
2. Ask the agent to read:
   - `../AGENTS.md` at the workspace root
   - local `AGENTS.md`
   - local `task.md`
3. Keep all edits inside that task folder unless you explicitly intend to update shared workspace assets.
4. Use `prompts/` templates as the starting prompt.
5. Run the minimum verification commands after each meaningful change.

## How to use skills, SOPs, and prompts

- Use `skills/` when the task matches a reusable capability.
- Use `sops/` for repeatable workflows such as debugging or closing out a task.
- Use `prompts/` to start a safe, structured agent session.

## How to handle secrets

- Never store real keys in this repository.
- Keep only templates in `secrets/`.
- Prefer environment variables or a password manager.
- Use `secrets/env.example` as a placeholder reference only.

## Recommended safety habits

- Inspect before editing.
- Prefer small changes over large rewrites.
- Ask for confirmation before risky commands.
- Do not commit generated outputs, logs, or temporary files.
- Keep task data and experiments isolated.

## How to archive a task

1. Finish the task and write a short `summary.md` if needed.
2. Move final deliverables into the task's `docs/` or `outputs/`.
3. Move the task folder into `archives/` only when it is complete or intentionally abandoned; this does not make it public to the root repository.
4. Keep enough notes so the task can be understood later without re-running everything.

</details>

<details>
<summary><strong>简体中文</strong></summary>

这是一个个人长期使用的 agent 工作区，用来学习和使用 Codex、Claude Code、OpenCode、Aider 等 coding agent。它把通用规则、提示词、SOP、环境说明和任务目录集中在一起，方便复用，也方便把不同任务彼此隔离。

## 文档

- [工作区完整指南](WORKSPACE_GUIDE.md)

## 目录说明

- `AGENTS.md`：所有 agent 的根规则与安全边界。
- `README.md`：中英文工作区总览。
- `WORKSPACE_GUIDE.md`：中英文工作区完整指南。
- `skills/`：可复用技能卡与方法说明。
- `sops/`：标准操作流程。
- `prompts/`：给不同 agent 直接复用的提示词模板。
- `tools/`：建任务、检查工作区等辅助脚本。
- `envs/`：不同 CLI、模型提供方、环境的使用说明。
- `tasks/`：正式任务目录；具体任务文件夹默认只保留在本地，不进入 Git。
- `tasks/README.md`：被 Git 跟踪的占位说明，用来记录任务目录的私有策略。
- `sandboxes/`：临时实验目录。
- `archives/`：已完成或废弃任务的归档目录；具体归档任务默认只保留在本地。
- `secrets/`：只放模板，不放真实密钥。

## 规则层级

- workspace 根 `AGENTS.md` 是全局规则。
- 每个任务目录下的 `AGENTS.md` 是该任务的局部规则。
- 任务规则只能补充或收紧根规则，不能放松根规则。
- 如果根规则和任务规则看起来不同，以更严格的规则为准。

## 新建任务

应在工作区根目录执行：

```bash
python tools/workspace.py new my_task
```

这会创建 `tasks/my_task/`，包括任务规则、状态文档、源码、测试、输出、日志和任务私有技能目录。

具体任务目录默认被 `.gitignore` 排除。任务状态、登记表和清理说明应保留在任务目录内部。需要发布时，经过人工审查后在该任务目录内初始化独立 Git 仓库，不得加入 workspace 根仓库。

## 独立发布任务

具体任务和归档任务始终对 workspace 根仓库保持私有。只有用户明确选择某个任务后，才能按照 `sops/publish_independent_task.md` 在任务目录内初始化独立 Git 仓库并单独发布。

## 如何在任务中使用 Agent

1. 进入 `tasks/<task_name>/`。
2. 先让 agent 读取工作区根 `AGENTS.md`、当前任务 `AGENTS.md`、`task.md` 和 `README.md`。
3. 明确要求 agent 只在当前任务目录内工作，除非你允许它修改共享资产。
4. 优先使用 `prompts/` 下的模板作为开场提示。
5. 每次改动后运行最小验证命令，并汇报修改文件、执行命令和验证结果。

## 任务内 Skill 应该放哪里

- 跨多个任务都能复用的 skill 放在根 `skills/`。
- 只对当前任务有用的 skill、经验和检查清单放在 `tasks/<task_name>/docs/skills/`。
- 某个任务私有 skill 只有在多个任务里证明可复用后，再提升到根 `skills/`。

## 如何使用 Skills、SOP 和 Prompts

- `skills/`：当问题可复用时，先找技能卡再执行。
- `sops/`：当任务属于固定流程时，直接按 SOP 走。
- `prompts/`：给不同 agent 开工时提供统一且安全的起点。

## 提交前如何检查

日常修改框架时运行：

```powershell
python tools/workspace.py check
```

大范围框架提交前运行：

```powershell
python tools/workspace.py check --full
```

详细步骤与兼容命令见 `sops/workspace_maintenance.md`。

## Secrets 的处理方式

- 不要把真实 API key、token、SSH key、密码写入仓库。
- `secrets/` 目录里只保留模板文件。
- 优先使用系统环境变量或密码管理器。
- 本地 secret 文件必须被 Git 忽略。

## 推荐安全习惯

- 先读文档，再改代码。
- 先做最小改动，再做验证。
- 风险命令先确认，不直接执行。
- 不跨任务修改文件。
- 不提交生成产物、日志和临时文件。
- 不让 agent 打印或提交真实密钥。

## 如何归档任务

1. 完成任务后运行最小最终验证。
2. 在任务目录里补充 `summary.md`（如果需要）。
3. 把稳定产物放到 `docs/` 或 `outputs/`。
4. 任务完成或废弃后，再移动到 `archives/`；归档不会让任务进入根仓库。
5. 保留足够说明，保证以后不重新运行也能理解任务结果。

</details>
