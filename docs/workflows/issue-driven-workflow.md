# Issue 驱动工作流

## 目的

Paper Reading Lab 使用 GitHub Issue 作为长期操作入口和工作流控制面，但不把 Issue 当作 Source、数据库或完整学习 transcript。

核心关系：

```text
1 Paper
↕
1 Primary GitHub Issue

1 Paper
↕
N ReadingSessions

1 ReadingSession
↕
N ReadingSteps / checkpoints
```

## Primary Paper Issue

一篇 Paper 创建一个主 Issue。

主 Issue 负责：

- 关联稳定 `paper_id`
- 记录目标论文与版本状态
- 指向 canonical Source / `PaperRevision`
- 指向 `reading-mcp` binding
- 记录当前学习目标
- 汇总 ReadingSession
- 记录 blocker / action
- 作为后续 AI / 人重新进入该 Paper 的统一入口

Issue number、标题和 Label 都不是 `paper_id`。

## 为什么不是“一次 Session 一个 Issue”

ReadingSession 是可重复的短生命周期学习活动。

如果每一次 Learning / Prediction / Recall 都新建 Issue，会导致：

```text
同一 Paper identity
→ 被大量操作 Issue 打碎
→ 长期入口不稳定
→ 很难快速看出这篇论文的学习历史
```

因此默认：

```text
Paper = primary Issue
ReadingSession = linked artifact / checkpoint history
```

## 哪些情况可以额外创建 Task Issue

只有当工作本身有明确边界、可以独立关闭时，例如：

- Source recovery
- 论文版本关系调查
- reading-mcp 某格式解析问题
- locator / segmentation defect
- Validator 实现
- Session schema migration
- 自动 checkpoint 工具
- export 到下游仓库的工程任务

这些 Issue 是 Task / Bug，不承担 Paper primary identity。

## Issue 不保存什么

不要把以下内容完整复制进 Primary Issue：

- 论文全文
- 每一个 Sentence 的长引用
- 完整 AI 对话 transcript
- 每一步长篇解释
- 未复核的下游正式知识资产

Issue 应保持为可操作摘要。

## Session summary

一次 ReadingSession 完成或暂停后，可以向 Primary Issue 追加简洁 summary：

```text
session_id
revision_id
mode
planned_scope
current_scope_boundary
revealed range
关键 reasoning findings
knowledge gaps
prediction / reconstruction finding
next action
operational checkpoint reference
learning artifact reference
```

summary 不应替代 Operational Recovery Checkpoint，也不应替代 ReadingSession Learning Artifact。

## Operational Recovery Checkpoint

这是 control plane 的**续作状态**：目标是让 fresh conversation 不依赖旧聊天就能安全继续。

至少需要能够恢复：

```text
paper_id
revision_id
reading_document_id
content / normalized identity
segmentation_version
current phase / mode
planned_scope
current_scope_boundary
revealed position
latest precise TextLocator
immutable prediction reference（如存在）
blocker / finding
exactly one next action
```

特别地，`current_scope_boundary` 必须在下一次 canonical reveal **之前**被检查。若 next unit 越界，worker 必须 STOP；不能因为 Primary Issue body 仍写着旧目标或用户继续说“下一句”就自动扩展。

scope 扩展必须先留下 durable amendment：

```text
old_scope
new_scope
reason
amendment_point
```

原 `planned_scope` 作为历史事实保留。

## ReadingSession Learning Artifact

这是学习层的**可恢复认知摘要**：目标是支持 Recall / Reconstruction / retrospective，而不是驱动 Source reveal。

第一版至少覆盖语义：

```text
session identity / mode / scope
revealed range
explicit reasoning links
current problem model / latest model update
knowledge gaps
reasoning gaps
cue level / cue recovery result
prediction comparison finding（如存在）
reconstruction finding（如存在）
```

它应明显小于完整 transcript。Primary Issue 只保存 session summary / references，不演变成 learning database。

因此 fresh recovery 与 later recall 使用不同 durable information：

```text
继续操作 → Operational Recovery Checkpoint
主动恢复 / 重建 → ReadingSession Learning Artifact
```

## 生命周期

Primary Paper Issue 默认可以长期保持 open，因为 Paper 可以不断新增 ReadingSession。

可关闭的通常是：

- Source recovery task
- segmentation bug
- schema task
- 一次实现任务

如果未来决定关闭 Primary Paper Issue，关闭只能表示当前工作阶段结束，不能表达：

```text
Paper has no more learning value
```

## Label 原则

Label 只做状态投影，不承担领域真相。

第一版可以保持极简，例如：

```text
type:paper
type:task
status:source-review
status:reading
status:blocked
```

不要一开始制造大量 mode / pass / score Label。

`mode`、`revealed_position` 等精确 Session 状态应保存在 Session artifact，而不是依赖 Label。

## Source 与 Issue 的关系

Issue 可以引用：

```text
PaperRevision
reading_document_id
canonical source
Source limitations
```

但“作者实际写了什么”必须由 Source provider 和 locator 证明。

不能因为 Issue comment 中 AI 曾经写过某个结论，就把它视为 Source fact。

## Finding 与正式知识的关系

Issue 中记录的 reading finding 仍然属于学习层：

```text
Reading finding
→ review / export candidate
→ 下游仓库自己的 gate
→ validated knowledge
```

不能跳过目标仓库的验证门禁。

## 推荐 Primary Issue 结构

```text
# 论文
- paper_id
- title
- authors
- year

# Source
- revision_id
- canonical source
- reading provider
- document binding
- limitations

# 当前目标
- planned_scope
- current_scope_boundary
- current phase

# Reading Sessions
- session summaries / links

# 当前薄弱点
- knowledge gaps
- reasoning gaps

# 下一步
- next action
```

## 核心不变量

```text
1 Paper → 1 Primary Issue。
Issue number ≠ Paper identity。
ReadingSession 不默认创建独立 Issue。
Issue 是控制面，不是 Source truth。
planned_scope 是 durable history；current_scope_boundary 是 executable reveal gate。
跨 scope 默认 STOP；scope amendment 必须先 durable、后 reveal。
Operational Recovery Checkpoint ≠ ReadingSession Learning Artifact。
Issue summary ≠ Operational Recovery Checkpoint ≠ ReadingSession Learning Artifact。
Label 是投影，不是领域状态根。
Session completed ≠ Paper done。
Paper Issue 的关闭不等于 Paper 学习完成。
```
