# Fresh Conversation Bootstrap

## 目的

本流程定义：一个新的 GPT / Agent conversation 只拿到薄入口 Prompt 时，如何从仓库与 GitHub durable state 恢复 Paper Reading Lab 工作，而不是依赖旧聊天上下文。

```text
Prompt = pointer
Repo = rules
Issue = control plane
Checkpoint / Handoff = runtime state
reading-mcp = paper Source truth
```

## 最小入口

推荐只提供：

```text
目标 repository
目标 Issue
允许使用的 MCP
按仓库治理执行
```

例如：

```text
@github-mcp @reading-mcp

接管 liqiangcc/paper-reading-lab Issue #N。
读取 AGENTS.md，并按仓库治理从 live state 恢复后执行；
完成或 blocked 后持久化并停止。
```

入口不应重复：

- PaperRevision / document hashes；
- TextLocator；
- current problem model；
- Source-First Protocol；
- Explanation Profile 全文；
- Tool 参数；
- acceptance checklist；
- 历史 transcript。

这些必须存在于 canonical docs 或 durable Issue state。

## Bootstrap 算法

### 1. 读取 `AGENTS.md`

确认：

- 仓库职责；
- 工具边界；
- 当前意图应路由到哪个 Skill；
- fail-closed 与停止条件。

### 2. 读取 target Issue live state

使用 `github-mcp` 读取：

- Issue body；
- relevant comments；
- state / labels / assignee（如使用）；
- linked PR / Candidate / evidence（Task 场景）；
- latest checkpoint / handoff / blocker / next action（Paper / Session 场景）。

不要只相信 Issue body 中的静态“当前状态”。最新 tagged durable record 通常更接近 live state。

### 3. 选择 applicable durable record

常见 tag：

```text
[SESSION START]
[SESSION HANDOFF]
[OPERATIONAL RECOVERY CHECKPOINT]
[IMMUTABLE PREDICTION]
[PREDICTION VS ACTUAL]
[BLOCKER]
[EXECUTION REPORT]
[ACCEPTANCE RESULT]
[CLOSURE]
```

选择规则：

1. 必须与目标 Paper / Task / Session identity 匹配；
2. 使用时间上最新且未被后续 record supersede 的记录；
3. immutable record 只能被引用，不能被后来改写；
4. body 与 comments 冲突时保留冲突并按 canonical lifecycle 判断；
5. 仍无法唯一确定时 fail closed，不猜测。

Tag 只是导航，不替代字段语义。

### 4. 路由 Skill

逐句阅读、下一句、resume、当前 Source fidelity review 使用：

```text
.agents/skills/source-first-reading/SKILL.md
```

其他任务按 `AGENTS.md` 和目标 Issue contract 执行。

Skill 不适用时，读取相关 canonical workflow docs；不要为了复用而强行套 Skill。

### 5. 加载最小 canonical docs

只读取执行当前 `next_action` 所需文档：

```text
needed docs
≠ every repository file
```

但必须覆盖当前动作依赖的：

- domain / identity；
- Source Adapter；
- Session / scope / lookahead；
- bound Explanation Profile；
- Issue / lifecycle / invariant。

若 Session 绑定 Profile，按 durable `profile_id + version + source` 读取，不默认最新版。

### 6. 恢复并核验状态

执行前恢复：

```text
paper_id / revision_id
source provider / document identity
Session id / mode / lookahead policy
planned_scope / current_scope_boundary
revealed_position / latest precise locator
bound Profile identity（如有）
immutable prediction reference（如有）
blocker / contamination state
exactly one next_action
```

缺失关键字段时不从模型记忆补齐。

### 7. Capability reality check

需要使用某个 MCP 时，以当前 conversation 的实际 invocation 为准：

```text
schema / release / historical success
≠ current availability
```

必需能力不可调用时：

```text
persist blocker / handoff
→ STOP
```

### 8. 执行授权动作

默认只执行 durable state 指定的当前动作。

不要因为执行顺利而自动：

- 扩 scope；
- reveal 第二个独立 SourceUnit；
- 开始下一 Session；
- 处理下一 Paper；
- 合并或关闭未授权 Task。

对于 source-first ReadingStep，先做 scope gate，再按 Skill 执行 bounded reveal。

### 9. 持久化结果

只在 meaningful durable boundary 写 GitHub：

- result / evidence；
- blocker / contamination；
- checkpoint / handoff；
- scope amendment；
- acceptance / closure。

Issue 只保存可操作摘要与 reference，不复制每句长解释或完整 transcript。

### 10. STOP

执行完当前 action 后停止。

若还有工作，持久化一个明确 next action，使下一 fresh conversation 可以恢复。

## 状态来源与优先级

不同来源拥有不同职责：

```text
Canonical repo docs / invariants
→ 方法和不可破坏边界

Issue live durable state
→ 当前任务、Session、scope、amendment、next action

Checkpoint / handoff
→ 恢复位置和执行状态

reading-mcp
→ Paper Source / canonical locator

Thin prompt
→ 只负责寻址
```

它们不能互相随意覆盖。

真实冲突处理：

```text
fail closed
→ record conflict
→ STOP
```

## Paper / Session 特殊规则

- Primary Paper Issue 可以长期 open；
- `Session completed ≠ Paper done`；
- abandoned / contaminated Session 保留历史；
- 新 Source normalization 不静默迁移旧 Session；
- scope amendment 发生在越界 reveal 前；
- Profile version transition 必须显式；
- Issue body 的历史计划不能覆盖更新的 durable Session record。

## Task / PR 特殊规则

Task 场景还应核验：

```text
Task contract
branch / Candidate SHA
linked PR
review / check evidence
remaining gate
```

不要把“PR mergeable”自动解释为已通过 review，也不要声称未运行的 CI 为 PASS。

## Thin-entry acceptance

治理成功的标准：fresh conversation 仅收到：

```text
repo + Issue + “读取 AGENTS.md 并按仓库治理执行”
```

仍能自行恢复：

- applicable Skill；
- canonical docs；
- Source / Revision / Session identity；
- scope / locator / Profile；
- current next action；
- failure / stop rules。

若仍要求用户重新粘贴 locator、Profile、完整规则或旧 transcript，应记录为 governance / durable-state finding。

## 非目标

本 bootstrap 不负责：

- 自动选择用户未指定的 Paper / Issue；
- 自动创建或扩展 Session；
- 自动调度多 Agent；
- 将 Issue 变成数据库；
- 替代 Source-first protocol；
- 在 Tool 不可用时绕过 canonical Source；
- 判断论文观点真假；
- 自动关闭所有后续工作。

## 核心不变量

```text
Thin Prompt 只负责寻址。
规则来自仓库。
动态状态来自 Issue / checkpoint。
Source truth 来自 reading-mcp。
恢复不依赖旧 conversation。
冲突与缺失默认 fail closed。
执行授权动作后持久化并停止。
```
