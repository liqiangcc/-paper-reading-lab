# Issue 驱动工作流

## 目的

Paper Reading Lab 使用 GitHub Issue 作为长期操作入口和控制面，但不把 Issue 当作：

- canonical paper Source；
- 完整学习 transcript；
- 全量 Session 数据库；
- Paper identity 本身；
- 静态 README 的替代品。

核心关系：

```text
1 Paper
↕
1 Primary Paper Issue

1 Paper
↕
N ReadingSessions

1 ReadingSession
↕
N ReadingSteps / checkpoints / artifacts
```

## Primary Paper Issue

一篇 Paper 默认创建一个主 Issue。

负责：

- 关联稳定 `paper_id`；
- 记录 Paper / Revision / Source binding 摘要；
- 汇总 ReadingSession；
- 保存 scope amendment、blocker、handoff、next action；
- 指向 Operational Recovery Checkpoint / Learning Artifact；
- 作为后续 AI / 人重新进入该 Paper 的统一入口。

Issue number、标题和 Label 都不是 `paper_id`。

## Stable body 与 live comments

### Issue body

保存相对稳定内容：

```text
Paper identity
Revision / canonical source
current accepted Source binding summary
historical warning
current Session summary
where to find latest durable records
current high-level authorization
```

### Tagged durable comments

保存动态工作状态：

```text
[SESSION START]
[SESSION HANDOFF]
[OPERATIONAL RECOVERY CHECKPOINT]
[IMMUTABLE PREDICTION]
[PREDICTION VS ACTUAL]
[SCOPE AMENDMENT]
[BLOCKER]
[ACCEPTANCE RESULT]
[CLOSURE]
```

fresh worker 不能只读取 body；必须扫描 relevant comments，并选择与目标 Session identity 匹配、时间上最新且未被 supersede 的 durable record。

Body 与 comments 冲突时：

```text
preserve conflict
→ follow canonical lifecycle / identity rules
→ fail closed if state remains ambiguous
```

不能靠模型猜测“更像当前”的状态。

## 为什么不是一次 Session 一个 Issue

ReadingSession 是可重复的短生命周期学习活动。

若每次 Learning / Prediction / Recall 都新建 Issue：

```text
同一 Paper identity
→ 被大量操作 Issue 打碎
→ 长期入口不稳定
→ 难以观察完整学习历史
```

默认：

```text
Paper = Primary Issue
ReadingSession = linked durable records / artifact references
```

## 哪些情况创建 Task / Bug Issue

具有明确边界、可独立关闭的工作，例如：

- Source recovery；
- Revision 关系调查；
- `reading-mcp` adapter defect；
- locator / segmentation defect；
- workflow hardening；
- Explanation Profile；
- repository governance；
- Validator / schema migration；
- export 工程任务。

这些 Issue 不承担 Paper primary identity。

## Task Issue 基本流程

```text
Task contract
→ isolated branch / Candidate
→ PR
→ evidence / review
→ accept / revise / block
→ merge / close
```

Task body 应明确：

- scope / non-goals；
- deliverables；
- acceptance criteria；
- current branch / Candidate；
- stop conditions。

不要因为 PR mergeable 就自动认为 acceptance 已通过，也不要声称未运行的 CI 为 PASS。

## Task closure 证据门禁

本节只适用于有界的工程 / 文档 Task，不把 Primary Paper Issue 的 open 状态解释为失败，也不把 Task completed 解释为 Paper done。

关闭前在目标 Issue 的 durable report 记录可追溯链：

```text
contract / base_sha
→ candidate_sha + PR
→ review 结果 + 该 candidate 的检查 / run URL
→ merge_commit_sha
→ 合并后该 main SHA 的检查 / run URL
→ remaining findings 分类
→ Issue body / state / owner 回读确认
```

每项 evidence 记录观察对象、结果和可打开的 reference。PR 检查若运行在测试 merge ref，必须说明其与 candidate/base 的关系，不能把旧 head 的成功当作新 head 的验证。主分支后来又变化时，历史成功只绑定当时的 merge SHA，不代表任意新的 main。

合并只是一个阶段。所需 post-merge check 未完成时，状态为 `merged-awaiting-verification`，不能提前写整体 PASS。自动 close 的 Task 若后续必要验证失败，应补 blocker 并重开或建立明确关联的修复 Task。工具不可用时记录 `NOT VERIFIED / BLOCKED`，不得拿旧聊天的成功声明代替检查。

终态同步要求：body 的执行状态与 GitHub 实际 state 一致，`active_owner: none`，完成清单按证据更新，`next_action` 不再指向已执行的旧动作。写入后重新读取，不能只凭写调用成功就假定所有投影已同步。历史 claim / prediction / acceptance / closure comments 保持原样；纠正通过追加 superseding record。

剩余 finding 必须分为 `resolved`、`accepted-limitation` 或 `blocked-follow-up`，附依据及必要的 Task reference。分支清理、Profile 深度覆盖、学习者 Recall 等属于不同验收维度，不能用一个 CI PASS 混为全部闭环。

`review requested`、无 review、无 blocking comment，都不等于独立 reviewer 已批准。自审应标为自审；若 Contract 要求独立验收而证据缺失，必须保留该 gate。

无 ref-delete capability 时不拿 `delete_file` 替代，不加大 token / workflow 权限只为删除分支。残留已合并分支可以作为非阻塞维护限制单独登记。

详见 [repository checks](../validation/repository-checks.md)：离线脚本不验证 GitHub live state、branch protection 或真实 ReadingSession。

## Issue 不保存什么

不要完整复制：

- 论文全文；
- 每个 Sentence 的长引用；
- 每一步长篇 AI 解释；
- 完整聊天 transcript；
- 模型私有 chain-of-thought；
- 未 review 的下游正式知识资产。

Issue 应保持为可操作摘要和 durable reference。

## Session summary

一次 Session 暂停、完成或放弃时，可以追加：

```text
session_id
revision_id / source binding
mode / lookahead policy
planned_scope
current_scope_boundary
revealed range
latest precise locator
关键 reasoning findings
knowledge / reasoning gaps
prediction / recall / reconstruction finding
checkpoint reference
learning artifact reference
next action
```

Summary 不替代 checkpoint 或 learning artifact。

## Operational Recovery Checkpoint

目标：让 fresh conversation 不依赖旧聊天即可安全续作。

至少恢复：

```text
paper_id
revision_id
reading_document_id / normalized identity
segmentation version
Session id / mode / lookahead policy
planned_scope
current_scope_boundary
revealed position
latest precise locator
bound Profile identity（如有）
immutable prediction reference（如有）
blocker / finding
stop boundary
exactly one next action
```

它驱动“从哪里安全继续”。

## ReadingSession Learning Artifact

目标：支持 Recall / Reconstruction / Retrospective。

至少保留：

```text
session identity / mode / scope
revealed range
source ref summary
explicit reasoning links
current problem model / model updates
knowledge gaps
reasoning gaps
cue level / recovery result
prediction comparison
reconstruction finding
```

它应明显小于 full transcript。

因此：

```text
Primary Issue summary
≠ Operational Recovery Checkpoint
≠ ReadingSession Learning Artifact
≠ full transcript
```

## Scope amendment

`planned_scope` 是历史计划；`current_scope_boundary` 是当前 executable gate。

若确需扩大范围，必须在越界 reveal 前持久化：

```text
old_boundary
new_boundary
reason
amendment_point
```

用户连续说“下一句”不自动构成 amendment。

## Prediction durable order

正式 Prediction 记录：

```text
persist immutable prediction
→ actual next Source reveal
→ append comparison
```

Issue 中的 Prediction comment 可以作为时间顺序证据，但不能替代 Source provider 的 actual locator。

## Label 原则

Label 只做粗粒度投影，不承担领域真相。

可保持极简：

```text
type:paper
type:task
status:source-review
status:reading
status:blocked
```

精确 mode、scope、position、Profile 和 next action 应存在于 durable state，而不是依赖 Label。

## Source 与 Issue

Issue 可以引用：

```text
PaperRevision
reading_document_id
normalized identity
canonical source
Source limitations
```

但“作者写了什么”必须由 `reading-mcp` SourceUnitRef / TextLocator 证明。

不能因为 Issue comment 中 AI 曾写过某个句子，就把它当作 Source Fact。

## Finding 与正式知识

Issue 中 reading finding 仍属于学习层：

```text
Reading finding
→ ExportCandidate
→ explicit review
→ target repository gate
→ validated knowledge
```

不能跳过目标仓库 gate。

## 生命周期

Primary Paper Issue 默认可以长期 open，因为同一 Paper 可以不断新增 Session。

可关闭的通常是：

- Source recovery Task；
- parser / locator Bug；
- workflow / governance Task；
- Profile / schema / Validator Task；
- 独立 export implementation。

Primary Issue 即使关闭，也只能表示当前工作阶段结束，不能表达：

```text
Paper has no more learning value
```

## 推荐 Primary Issue 结构

```text
# Paper
- paper_id
- title / authors / year

# Revision / Source
- revision_id
- canonical source
- provider binding
- limitations

# Historical warning
- abandoned / contaminated / stale sessions

# Current durable summary
- current Session identity / state
- planned_scope / current boundary
- revealed range / latest locator

# Durable-record rule
- latest tagged records to inspect

# Current next action
- explicit authorization / STOP condition
```

## 核心不变量

```text
1 Paper → 1 Primary Issue。
Issue number ≠ Paper identity。
ReadingSession 不默认创建独立 Issue。
Issue body 保存稳定摘要，comments 保存动态 durable state。
Fresh worker 必须读取 live comments。
Issue 是 control plane，不是 Source truth。
planned_scope 保留历史，current_scope_boundary 控制 reveal。
Operational Checkpoint ≠ Learning Artifact。
Issue summary 不替代二者。
Session completed ≠ Paper done。
```
