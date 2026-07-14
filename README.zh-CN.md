# Agent Workspace 中文说明

这是一个个人长期使用的 agent 工作区，用来学习和使用 Codex、Claude Code、OpenCode、Aider 等 coding agent。它把通用规则、提示词、SOP、环境说明和任务目录集中在一起，方便复用，也方便把不同任务彼此隔离。

## 目录说明

- `AGENTS.md`：所有 agent 的根规则与安全边界。
- `README.md`：英文版总说明。
- `README.zh-CN.md`：中文版总说明。
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

建议把“创建任务”这一步放在 `D:\MaHong\agent_workspace` 这个根目录上下文里完成，而不是放在 `tasks/` 目录里。

这会创建：

```text
tasks/my_task_name/
├── AGENTS.md
├── task.md
├── README.md
├── summary.md
├── src/
├── scripts/
├── data/
├── outputs/
├── tests/
├── tmp/
├── logs/
├── docs/
└── docs/skills/
```

具体任务目录默认被 `.gitignore` 排除。任务状态、登记表和清理说明应保留在任务目录内部。需要发布时，经过人工审查后在该任务目录内初始化独立 Git 仓库，不得加入 workspace 根仓库。

## 独立发布任务

具体任务和归档任务始终对 workspace 根仓库保持私有。只有用户明确选择某个任务后，才能按照 `sops/publish_independent_task.md` 在任务目录内初始化独立 Git 仓库并单独发布。

## 如何在 task 中使用 Codex / Claude Code / OpenCode / Aider

1. 进入 `tasks/<task_name>/`。
2. 先让 agent 读取：
   - 工作区根目录 `AGENTS.md`
   - 当前任务目录 `AGENTS.md`
   - 当前任务目录 `task.md`
   - 当前任务目录 `README.md`
3. 明确要求 agent 只在当前 task 目录内工作，除非你明确允许它修改共享资产。
4. 优先使用 `prompts/` 下的模板作为开场提示。
5. 每次改动后运行最小验证命令，并让 agent 汇报：
   - changed files
   - commands run
   - verification result

## task 内 skill 应该放哪里

- 跨多个任务都能复用的 skill，放在 `workspace/skills/`。
- 只对当前任务有用的 skill、经验、检查清单、调试结论，放在当前任务目录里。
- 推荐默认放在：`tasks/<task_name>/docs/skills/`
- 某个 task-local skill 只有在多个任务里重复证明可复用后，再提升到 `workspace/skills/`。

## OpenCode 快速开始

如果本机已安装 `opencode`，推荐在任务目录里启动：

```powershell
cd D:\MaHong\agent_workspace\tasks\my_task_name
opencode .
```

常用命令：

```powershell
opencode .
opencode run "read AGENTS.md and task.md, then propose a plan"
opencode web .
opencode providers list
```

如果要用 OpenAI API，请优先使用环境变量，不要把真实密钥写入仓库：

```powershell
$env:OPENAI_API_KEY="your_key_here"
opencode .
```

密钥模板请参考 `secrets/env.example`，真实密钥只放在系统环境变量或密码管理器里。

## 如何使用 skills、SOP 和 prompts

- `skills/`：当问题可复用时，先找技能卡再执行。
- `sops/`：当任务属于固定流程时，直接按 SOP 走。
- `prompts/`：给不同 agent 开工时提供统一且安全的起点。

推荐搭配：

- 调试问题：`sops/debug_error.md` + `prompts/safe_debug.md`
- 新建任务：`sops/new_task.md` + `tools/make_task.py`
- 接外部 API：`sops/setup_external_api.md` + `secrets/env.example`
- 结束任务：`sops/task_closeout.md`

## 提交前如何检查

日常修改框架时，运行只读快速检查：

```powershell
python tools/workspace.py check
```

大范围框架提交前，运行会刷新维护报告的完整检查：

```powershell
python tools/workspace.py check --full
```

baseline 推荐报告写入 `outputs/first_commit_recommendation.md`，该文件默认被 Git 忽略。详细步骤与兼容命令见 `sops/workspace_maintenance.md`。

## secrets 的处理方式

- 不要把真实 API key、token、SSH key、密码写入仓库。
- `secrets/` 目录里只保留模板文件。
- 优先使用系统环境变量。
- 如果必须本地保存，也应放在 `.env.local` 一类未提交文件中，并确保被忽略。

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
5. 保留足够说明，保证以后不重新跑也能理解任务结果。
