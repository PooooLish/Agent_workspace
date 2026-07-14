# 工作区总说明

这份文档是 `D:\MaHong\agent_workspace` 的可维护总说明，目标是让你或未来协作的 agent 只通过这一份文档，就能理解整个 workspace 的定位、目录结构、核心组件、使用流程和维护方式。

## 1. 工作区定位

这个 workspace 是一个面向个人长期使用的 agent 工作中枢，用来统一管理 Codex、Claude Code、OpenCode、Aider 等 coding agent 的共用规则、提示词、SOP、环境说明、任务模板和示例任务。

它主要解决四类问题：

1. 把共享规则和工作习惯放在一个地方。
2. 把正式任务和临时实验隔离开。
3. 把 prompts、SOP、skills 复用起来，而不是每次从头写。
4. 让工作过程更容易审查、接续、归档和回看。

它的设计原则是：

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
- `README.zh-CN.md`
- `WORKSPACE_GUIDE.md`
- `WORKSPACE_GUIDE.zh-CN.md`
- `.gitignore`
- `.git/`
- `skills/`
- `sops/`
- `prompts/`
- `tools/`
- `envs/`
- `tasks/`
- `tasks/README.md`
- `sandboxes/`
- `archives/`
- `secrets/`

这些顶层项目各自承担不同职责，后续维护时应尽量保持边界清晰，不混放用途不同的内容。

## 3. 根层治理文件

### `AGENTS.md`

这是整个工作区的根规则文件，也是最重要的行为边界说明。

它当前定义了：

- agent 的全局角色
- 安全规则
- 默认工作循环
- 规则层级关系
- 任务隔离规则
- 知识放置规则
- 文件修改规则

规则层级应理解为：

- workspace 根 `AGENTS.md` 是全局规则
- 每个任务自己的 `AGENTS.md` 是局部规则
- 局部规则只能补充或收紧全局规则
- 如果两者冲突，以更严格者为准

### `README.md`

这是英文版简要总览，说明了 workspace 的用途、目录结构、新建任务流程、如何使用 agent、如何处理 secrets，以及如何归档任务。

### `README.zh-CN.md`

这是中文版简要总览，内容与 `README.md` 对应，更适合作为日常查阅入口。

### `.gitignore`

这个文件负责避免把不该跟踪的内容纳入仓库，包括：

- `.env` 文件
- key / pem 等敏感文件
- `outputs/`、`tmp/`、`logs/`
- Python 缓存目录
- 虚拟环境
- 大模型权重和中间产物
- 编辑器元数据

它的作用是保护仓库整洁，减少误提交密钥和生成垃圾文件的风险。

### `.git/`

工作区已经完成 Git 初始化。它的作用是为整个 workspace 提供版本控制能力，方便以后记录结构、模板、脚本和文档的演进。

## 4. 共享可复用组件

### `skills/`

这里存放的是可复用的技能卡。技能卡不是代码，而是把某一类重复工作整理成可复用的操作说明。

当前已有的 skills：

- `code_review/`
- `python_project_setup/`
- `cli_tool_setup/`
- `linux_debugging/`
- `documentation_writer/`

每个 `SKILL.md` 都采用统一结构：

- Purpose
- When to use
- Procedure
- Safety rules
- Expected output

当前各 skill 的作用：

- `code_review`：用于代码审查，重点检查 bug、行为回归、测试缺失。
- `python_project_setup`：用于快速搭建小型 Python 项目或任务骨架。
- `cli_tool_setup`：用于记录和规范 CLI 工具的安全使用方式。
- `linux_debugging`：用于系统化排查 Linux 下的命令、路径、进程或环境问题。
- `documentation_writer`：用于把项目上下文整理成清晰、可执行的文档。

什么时候应该新增 skill：

- 当某类工作在多个任务中反复出现时
- 当它适合作为跨任务复用资产时

什么时候不该放在这里：

- 当经验、技能、检查清单只对某一个任务有用时
- 当它强依赖某个具体任务的仓库结构、数据或业务语境时

对这类内容，更推荐放到：

- `tasks/<task_name>/docs/skills/`

当它在多个任务中被反复证明可复用后，再提升到 `workspace/skills/`。

### `sops/`

这里存放标准操作流程文档。

当前已有 SOP：

- `new_task.md`
- `debug_error.md`
- `modify_existing_project.md`
- `setup_external_api.md`
- `task_closeout.md`
- `safe_shell_commands.md`

各自的作用：

- `new_task.md`：说明如何创建并开始一个正式任务
- `debug_error.md`：说明如何围绕报错做最小修复
- `modify_existing_project.md`：说明如何安全地修改已有项目
- `setup_external_api.md`：说明如何接入外部 API 而不保存真实 key
- `task_closeout.md`：说明如何收尾、总结和准备归档
- `safe_shell_commands.md`：列出哪些命令属于高风险命令，必须人工确认后执行

### `prompts/`

这里存放给不同 agent 和不同工作场景使用的提示词模板。

当前已有：

- `codex_default.md`
- `claude_code_default.md`
- `opencode_default.md`
- `aider_default.md`
- `safe_debug.md`
- `safe_setup.md`
- `code_review.md`

这些模板共同约束的行为包括：

- 先读 `AGENTS.md`、`README.md`、`task.md`
- 不删除文件
- 不修改任务范围外的文件
- 不保存或暴露真实 API key
- 先给简短计划
- 改完后做最小验证
- 最后汇报 changed files、commands run、verification result

## 5. 辅助脚本

### `tools/make_task.py`

这是创建正式任务目录的脚本。

用法：

```bash
python tools/make_task.py task_name
```

推荐在 workspace 根目录上下文中执行这个命令，而不是把线程根目录长期放在 `tasks/`。

它会在 `tasks/<task_name>/` 下创建：

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
- `docs/skills/`

新的任务级 `AGENTS.md` 应明确说明：

- 先遵守 workspace 根规则
- 再遵守 task 局部规则
- 局部规则只能补充或收紧全局规则

具体任务目录默认被 `.gitignore` 排除。任务状态、登记表和清理说明应保留在任务目录内部。需要发布时，经过人工审查后在该任务目录内初始化独立 Git 仓库，不得修改根 `.gitignore` 将具体任务加入 workspace 仓库。

### `tools/check_workspace.py`

这是检查工作区基础结构是否齐全的脚本。

用法：

```bash
python tools/check_workspace.py
```

它目前检查这些项目是否存在：

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

### `tools/audit_git_readiness.py`

这是提交前的 Git 候选文件审计脚本。

用法：

```bash
python tools/audit_git_readiness.py
```

严格大文件提醒：

```bash
python tools/audit_git_readiness.py --max-mb 1
```

它会检查 Git 会跟踪的候选文件中是否存在大文件、敏感命名和疑似 secret 内容。它只报告路径和模式名，不打印 secret 值。

### `tools/audit_line_endings.py`

这是 `.gitattributes` 换行策略审计脚本。

用法：

```bash
python tools/audit_line_endings.py
python tools/audit_line_endings.py --strict
```

如果需要按策略自动归一化候选文件换行：

```bash
python tools/audit_line_endings.py --fix
```

### `tools/test_workspace_tools.py`

这是 workspace 工具的轻量回归测试脚本。

用法：

```bash
python tools/test_workspace_tools.py
```

### `tools/summarize_git_candidates.py`

这是 Git 候选文件摘要脚本。

用法：

```bash
python tools/summarize_git_candidates.py
```

### `tools/prepare_baseline_report.py`

这是 workspace baseline 推荐报告生成脚本。

用法：

```bash
python tools/prepare_baseline_report.py
```

默认输出：

- `outputs/first_commit_recommendation.md`

这个输出文件默认被 Git 忽略。旧的 `tools/prepare_first_commit_report.py` 仍然保留，用来兼容早期命令名。

### `tools/verify_baseline_report.py`

这是 baseline 推荐报告的新鲜度验证脚本。

用法：

```bash
python tools/verify_baseline_report.py
```

它会比较当前候选文件和已生成报告，提醒是否需要重新生成。

### `tools/generate_workspace_status.py`

这是 workspace 当前状态文件生成脚本。

用法：

```bash
python tools/generate_workspace_status.py
```

### `tools/verify_workspace_status.py`

这是 workspace 状态文件新鲜度验证脚本。

用法：

```bash
python tools/verify_workspace_status.py
```

### `tools/run_workspace_maintenance.py`

这是完整维护链脚本。

用法：

```bash
python tools/run_workspace_maintenance.py
```

它会依次运行状态引导刷新、工具回归测试、结构检查、Git readiness、候选文件摘要、baseline 报告生成和验证、状态文件生成和验证、换行审计，以及严格大文件提醒。

## 6. 环境说明层

### `envs/`

这里存放的是“如何安全使用工具和环境”的说明，不是安装脚本目录。

当前文件有：

- `base_python.md`
- `node_tools.md`
- `codex_cli.md`
- `claude_code.md`
- `opencode.md`
- `aider.md`
- `external_api.md`

这些文件的主要作用是：

- 记录使用约定
- 说明本地工作流
- 沉淀安全配置方式
- 描述 provider 用法而不保存真实 secrets

#### `envs/opencode.md`

这是当前最完整的一份环境说明。

它记录了：

- OpenCode CLI 已安装
- `opencode --version` 已验证
- 推荐在 task 目录中启动 OpenCode
- 常用命令，如 `opencode .`、`opencode run`、`opencode web`、`opencode providers list`
- 推荐的 provider 配置方式：环境变量
- 推荐的结果汇报格式

## 7. Secrets 策略

### `secrets/`

这个目录是刻意设计成“只放模板”的。

当前包含：

- `README.md`
- `env.example`

#### `secrets/README.md`

它明确规定：

- 这里不存放真实密钥
- 真实凭据应放在系统环境变量或密码管理器中
- 不应要求 agent 打印、保存或提交真实密钥

#### `secrets/env.example`

这是占位模板，目前包含：

- `OPENAI_API_KEY=`
- `ANTHROPIC_API_KEY=`
- `DEEPSEEK_API_KEY=`
- `OPENROUTER_API_KEY=`
- `GEMINI_API_KEY=`

## 8. 正式任务系统

### `tasks/`

所有正式任务都应该放在这里。

核心规则：

- 一个正式任务，对应 `tasks/` 下的一个独立目录
- 创建任务的动作应在 workspace 根目录上下文中完成
- 实际执行某个任务时，应把工作范围收紧到该任务目录
- 具体任务目录默认只保留在本地，不进入 Git

理想情况下，每个任务应包含：

- 局部 `AGENTS.md`
- 局部 `task.md`
- 局部 `README.md`
- 源代码
- 辅助脚本
- 测试
- 输出结果
- 临时文件
- 日志
- 文档
- `docs/skills/` 下的任务私有技能、经验与清单

### task 内知识沉淀规则

如果某条 skill、经验、调试路径、检查清单只适用于当前任务，应放在：

- `tasks/<task_name>/docs/skills/`

如果它后来在多个任务中复用成功，再考虑提升到：

- `workspace/skills/`

### 任务目录入库策略

Git 默认只跟踪：

- `tasks/README.md`

具体任务目录不默认入库。这样可以降低误提交私人项目上下文、生成产物、媒体文件和本地笔记的风险。需要共享某个任务时，应先人工审查内容，再添加窄范围例外。

## 9. Sandboxes 与 Archives

### `sandboxes/`

这里用于存放临时实验。

适合放：

- 快速原型
- 一次性验证
- 环境实验
- 临时调查内容

### `archives/`

这里用于存放已经完成或明确废弃的任务。

具体归档任务仍然对 workspace 根仓库保持私有并被 Git 忽略。需要发布时，只能在选定任务目录内建立独立 Git 仓库。

## 10. 已接入的外部 agent 工具

### Git

workspace 已初始化 Git 仓库，后续可以跟踪结构和文档变化。

### OpenCode

OpenCode CLI 已安装，本地接入说明已经写入 `envs/opencode.md`。

推荐使用方式：

```powershell
cd D:\MaHong\agent_workspace\tasks\my_task_name
opencode .
```

推荐 provider 模式：

```powershell
$env:OPENAI_API_KEY="your_key_here"
opencode .
```

### Codex 全局技能

Codex 全局 skill 和插件位于本仓库之外，可能独立变化。需要时应从当前 Codex 会话查询；本 workspace 自己维护的 skill 清单以自动生成的 `WORKSPACE_STATUS.md` 为准。

## 11. 推荐日常工作流

推荐的日常路径是：

1. 在 workspace 根目录运行 `python tools/workspace.py new <task_name>`
2. 填写 `tasks/<task_name>/task.md`
3. 进入该任务目录
4. 选择一个 agent 开始工作
5. 要求 agent 读取：
   - 根目录 `AGENTS.md`
   - 当前任务 `AGENTS.md`
   - 当前任务 `task.md`
   - 当前任务 `README.md`
6. 除非确有必要，否则把所有修改限制在当前任务目录中
7. 任务私有 skill 和经验默认沉淀在 `docs/skills/`
8. 每次有意义修改后做最小验证
9. 最后补总结，需要时再归档

## 12. 维护规则

为了让这个 workspace 长期可维护，建议遵循：

- 根目录文件尽量保持通用和可复用
- 任务细节尽量只放在任务目录里
- task-local skill 默认先沉淀在任务目录
- 只有当某类工作重复出现时才新增 workspace 级 skill
- 工具使用方式变化时，同步更新 `envs/`
- `secrets/env.example` 只维护变量名，不写真实值

## 13. 总结

这个 workspace 的价值不在于某一个单独文件，而在于这些部分如何协同工作：

- 根规则约束行为
- 任务规则提供局部收紧与补充
- prompts 规范执行入口
- SOP 固化流程
- tools 降低建任务和检查成本
- tasks 隔离正式工作
- docs/skills/ 承接任务私有知识
- workspace/skills/ 承接跨任务公共能力
- secrets 保护敏感信息
- envs 把本地工具和安全工作流连接起来

建议把这份文档作为“理解整个 workspace 的单一入口”，只要结构或工作模式有实质变化，就同步更新它。
