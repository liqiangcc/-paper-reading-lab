# Fresh Conversation Bootstrap

## 目的

本流程定义：一个新的 GPT / Agent conversation 只拿到很薄的入口 Prompt 时，如何从仓库和 GitHub durable state 恢复 Paper Reading Lab 工作，而不是依赖旧聊天上下文。

目标模型：

```text
Prompt ≈ pointer
Repo = rules
Issue = control plane
Checkpoint / Handoff = runtime state
reading-mcp = source truth
```

## 最小入口

推荐入口只提供：

```text
目标 repository
目标 Issue
可用 MCP
“按仓库治理恢复并执行”
```

例如：

```text
@github-mcp @reading-mcp
接管 liqiangcc/-paper-reading-lab Issue #N。
读取 AGENTS.md，并按仓库治理从 live state 恢复后执行；完成或 blocked 后持久化并停止。
```

入口 Prompt 不应重复：

- PaperRevision / document hash；
- TextLocator；
- Session current model；
- Source-First Protocol；
- Explanation Profile 全文；
- get_text_units 参数；
- acceptance checklist；
- 大段历史 transcript。

这些应存在于 canonical repo docs 或 durable Issue / checkpoint state。

## Bootstrap 算法

### Step 1 — 读取仓库治理

读取根级：

```text
AGENTS.md
```

确认当前任务应路由到哪个 Skill，以及本仓库的 Source / Issue / Session / stop 边界。

### Step 2 — 读取 live Issue state

使用 `github-mcp` 读取目标 Issue：

- Issue body；
- comments；
- 当前 state；
- 若是 Task，读取关联 PR / Candidate / evidence；
- 若是 Paper Primary Issue，找到最新 Session checkpoint / handoff / blocker / next_action。

不要只相信 Issue body 的静态“当前状态”；最新 tagged comment 可能是更晚的 durable state。

### Step 3 — 识别 durable record

优先识别与当前任务相关的最新记录，例如：

```text
[SESSION HANDOFF]
[PILOT CHECKPOINT]
[PROFILE ACCEPTANCE HANDOFF]
[BLOCKER]
[EXECUTION REPORT]
[PILOT CLOSURE]
```

Tag 只是定位工具，不替代字段语义。若多个 durable records 冲突，停止并报告，不自行猜“哪个更像最新”。

### Step 4 — 路由到 Skill

如果意图是逐句阅读、继续、resume、下一句、ReadingSession fidelity review，则加载：

```text
.agents/skills/source-first-reading/SKILL.md
```

其他任务按 `AGENTS.md` 的路由规则执行；不存在适用 Skill 时，直接使用 canonical workflow docs，不要强行套用 reading Skill。

### Step 5 — 加载最小 canonical docs

Skill 负责声明它需要哪些文档。

原则：

```text
只加载执行当前 next_action 所需的 canonical docs
≠ 每次启动都全文读取整个仓库
```

如果 Session 绑定 Explanation Profile，则必须按 durable `style_profile.id + version + source` 读取对应 Profile，不得默认仓库最新版。

### Step 6 — 恢复 identity / scope / position

执行前核验：

```text
PaperRevision
Source provider binding
reading_document_id / normalized identity
Session mode
lookahead policy
planned_scope
current_scope_boundary
revealed_position
latest precise locator
bound Profile version（如有）
next_action
```

缺失关键字段时，不从模型记忆补齐。

### Step 7 — Capability reality check

需要调用 `reading-mcp`、`github-mcp` 或其他 MCP 时，以当前 conversation 实际 tool availability 为准。

```text
tool schema / old memory
≠ actual successful invocation
```

必要能力不可调用时，写 blocker / handoff 并停止。

### Step 8 — 执行唯一允许动作

默认只执行 durable state 指定的 `next_action`。

不要因为任务进行顺利就自动扩 scope、开始下一 Session、读取下一篇论文、合并 PR 或执行未授权后续动作。

对于 source-first ReadingStep，默认一次只推进当前 scope 允许的最小 canonical reveal。

### Step 9 — 持久化结果

在自然 durable boundary 写入可操作结果：

```text
完成结果
或
blocker / finding
或
新的 checkpoint / handoff
```

Issue 只保存控制面摘要和 reference，不复制完整长解释或 transcript。

### Step 10 — STOP

执行完当前任务或 next_action 后停止。

如果需要后续工作，写清楚唯一或明确的 next action，让下一个 fresh conversation 恢复。

## 状态优先级

不同来源承担不同职责，不应简单互相覆盖：

```text
Repository canonical docs / invariants
→ 规定方法和不可破坏边界

Issue live state / durable amendments
→ 规定当前任务、scope 和 workflow state

Checkpoint / handoff
→ 规定可恢复位置和 next_action

reading-mcp
→ 规定 paper Source truth / canonical locator

Thin prompt
→ 只负责指向任务
```

如果它们发生真实冲突：

```text
fail closed
→ 记录冲突
→ STOP
```

不要用模型记忆选择一个“看起来合理”的版本。

## Thin prompt acceptance

一个治理良好的 ReadingSession 应能从以下入口恢复：

```text
@github-mcp @reading-mcp
接管 paper-reading-lab Issue #N。
读取 AGENTS.md 并按仓库治理执行。
```

若 Agent 仍需要用户重新粘贴 locator、Profile、完整规则或历史 transcript，说明 durable state / repo governance 仍不完整，应记录为机制 finding。

## 非目标

本 bootstrap 不负责：

- 自动选择用户没有指定的 Paper / Issue；
- 自动创建新 Session；
- 自动跨 scope；
- 自动调度多个 Agent；
- 将 Issue 变成数据库；
- 替代 Source-First Protocol 或 ReadingSession lifecycle；
- 在 tool 不可用时绕过 canonical Source。

## 核心不变量

```text
Thin Prompt 只负责寻址。
规则来自仓库。
动态状态来自 Issue / checkpoint。
Source truth 来自 reading-mcp。
恢复不依赖旧 conversation。
冲突与缺失默认 fail closed。
执行一个明确 next_action 后停止。
```
