# ReadingSession 学习会话

## 目的

真实论文可以被反复阅读，每次阅读的目标、范围、既有知识和训练方式都可能不同。

`ReadingSession` 表示一次有明确边界、可暂停、可恢复、可完成或可放弃的学习过程。

它不修改 Raw Source，也不代表整篇论文永久“学完”。

## 核心原则

```text
Source 保持稳定。
Session 独立累积。
范围先持久化，再 reveal。
操作恢复与学习恢复分开。
理解可以深化、修正和迁移。
```

不能因为完成一次 Session，就给 Paper 写入永久：

```text
processed = true
```

## Session 必须绑定什么

最少绑定：

```text
session_id
paper_id
revision_id
source_binding
mode
learning_goal
lookahead_policy
planned_scope
current_scope_boundary
status
revealed_position
```

采用正式 Explanation Profile 的 Session 还必须绑定：

```text
style_profile.id
style_profile.version
style_profile.source
```

### 字段作用

- `revision_id`：防止阅读过程中静默换论文版本；
- `source_binding`：固定 `reading-mcp` document / normalized identity；
- `mode`：说明当前是 Learning、Prediction、Recall 等哪一种活动；
- `planned_scope`：Session 创建时的历史计划；
- `current_scope_boundary`：当前真正可执行的 reveal 边界；
- `lookahead_policy`：说明允许使用什么 Source；
- `revealed_position`：记录已经知道到哪里；
- `style_profile`：固定解释与呈现契约，不扩大 Source 可见范围。

## Session Mode

### Learning

AI 对当前允许的 canonical SourceUnit 做逐句、逐层解释。

目标：

- 理解字面；
- 识别 cue；
- 识别句间关系；
- 建立当前问题模型；
- 学习可复用显式结构。

### Prediction

在揭示下一 SourceUnit 前，学习者先预测下一步合理方向。

目标：

- 训练问题推进能力；
- 暴露当前模型缺失；
- 对比作者真实选择。

### Recall

隐藏目标原文或 Derived 解释，要求主动提取：

```text
cue
→ problem
→ constraint
→ decision
→ consequence
```

目标是从熟悉感转向可主动生成。

### Reconstruction

按段、节或整篇闭卷重建：

```text
Problem
→ Constraints
→ Alternatives
→ Decisions
→ Mechanisms
→ Trade-offs
→ Evidence
```

必须记录提示级别：

```text
closed-book
minimal-cue
outline-assisted
open-source
```

### Transfer

给一个真正的新问题，要求调用从论文中学到的思考结构。

Transfer 不是复述论文，也不把迁移结果反写成论文事实。

### Retrospective

已经知道后文或全文后重新阅读。

必须显式标记：

```text
lookahead_policy = retrospective
```

不能用于伪造首次阅读位置当时的判断。

## planned_scope 与 current_scope_boundary

### planned_scope

Session 创建时持久化的学习范围，例如：

```text
paper
named section
paragraph_range
sentence_range
question_focus
mechanism_focus
```

它是历史事实，后续 scope 扩展不能覆盖它。

### current_scope_boundary

当前真正允许 reveal 的边界，例如：

```text
allowed owner section
stop-before next sibling
end locator
max_new_canonical_units
```

每次新 canonical reveal 之前必须检查：

```text
next unit inside current_scope_boundary?
├── yes → reveal allowed
└── no  → STOP before reveal
          → durable scope amendment required
```

### Scope amendment

确实需要扩展时，先持久化：

```text
old_boundary
new_boundary
reason
amendment_point
```

然后才允许 reveal 新范围。用户继续说“下一句”不自动构成 amendment。

## revealed_position 与 view_position

首次顺序 Session 中：

```text
revealed_position
= 已经揭示到哪里，只能单调向前

view_position
= 当前正在回看哪里，可选且可后退
```

回看旧 SourceUnit 不会降低已经知道未来内容的事实。

## Explanation Profile binding

Source-first protocol 规定：

```text
允许读取什么、何时允许读取
```

Explanation Profile 规定：

```text
取得当前 SourceUnit 后怎样解释和呈现
```

采用正式 Profile 的 Session 示例：

```yaml
style_profile:
  id: source-first-incremental-explanation
  version: v0.1
  source: docs/learning/incremental-explanation-profile.md

style_overrides:
  language: zh-CN
  depth: adaptive
```

### Profile version 不得静默切换

- `id + version` 共同承担 identity；
- 历史 ReadingStep 继续绑定开始时的 Profile version；
- 新版本默认用于新 Session；
- 同一 Session 切换必须显式记录 transition、位置和影响；
- 未绑定正式 Profile 的历史 Session 不被事后假定使用当前最新版。

### Handoff 只引用 Profile identity

Issue comment 或 `[SESSION HANDOFF]` 保存：

```text
profile id
profile version
canonical source path
必要 style overrides
```

不复制整篇长 Style Prompt。Fresh conversation 读取 canonical Profile 恢复。

## ReadingStep

一次“下一句 / 下一步”通常对应一个有界 ReadingStep。

建议结构：

```text
step_id
session_id
current SourceUnitRef
source observations
derived interpretations
observed relations
current problem model update
explicit reasoning links
knowledge / reasoning gaps
stop_boundary
next_action
```

默认 source-first Learning Step：

```text
scope gate
→ exactly one canonical SourceUnit
→ exact locator re-read
→ explain Past + Current only
→ save locator / stop boundary
→ STOP
```

### Source / Derived / Unknown

Checkpoint 或 learning artifact 中应区分：

```text
Source-grounded Observation
→ 当前或此前已揭示 Source 直接支持

Derived Interpretation
→ 有限推论，可被后续修正

Unknown
→ 当前 Source 尚未回答
```

每个显式 reasoning arrow 必须能追溯到已揭示 Source，或保持 Derived 身份。

## Operational Recovery Checkpoint

目标：让 fresh conversation **安全继续操作**，而不是恢复完整聊天。

建议包含：

```text
checkpoint_id
session_id
paper_id
revision_id
source binding
mode / lookahead policy
planned_scope
current_scope_boundary
revealed_position
latest precise SourceUnitRef / TextLocator
style_profile / overrides（如有）
immutable prediction reference（如有）
blocker / finding
stop_boundary
exactly one next_action
```

它回答：

```text
当前绑定哪一个 Source？
允许读到哪里？
已经 reveal 到哪里？
下一步唯一允许做什么？
```

### 不保存什么

默认不沉淀：

- 每一句完整长解释；
- 整段 AI transcript；
- 无复用价值的寒暄；
- 模型私有 chain-of-thought。

## ReadingSession Learning Artifact

目标：支持 later Recall、Reconstruction 和 Retrospective。

建议保留：

```text
artifact_id
session identity / mode / scope
revealed range
source ref summary
explicit reasoning links
current problem model / compressed model updates
knowledge gaps
reasoning gaps
cue level / recovery result
prediction comparisons
reconstruction findings
```

它应明显小于完整 transcript，但比 Operational Recovery Checkpoint 更丰富。

因此：

```text
Operational Recovery Checkpoint
≠ ReadingSession Learning Artifact
≠ Primary Issue summary
≠ full transcript
```

## Prediction checkpoint

正式 Prediction 必须发生在 actual reveal 前。

揭示前记录：

```text
prediction_id
based_on_position
candidate_directions
confidence
created_at
```

揭示后只追加：

```text
actual_next_source_ref
match_type
what_was_missing
model_update
```

不得事后改写原 prediction 让它“更准”。

## KnowledgeGap 与 ReasoningGap

### KnowledgeGap

```text
term-gap
background-gap
math-gap
mechanism-gap
```

### ReasoningGap

```text
relation-gap
prediction-gap
reconstruction-gap
transfer-gap
```

Session 的重要输出不是“读了多少句”，而是发现哪些连接不能主动恢复。

## Session Summary

一次 Session 暂停、完成或放弃时，Primary Issue 只保存简洁可操作摘要：

```text
session_id
revision / source binding
mode
planned_scope / current boundary
revealed range
关键 reasoning findings
knowledge / reasoning gaps
prediction / recall / reconstruction finding
checkpoint / learning artifact reference
next action
```

不把完整聊天复制进 Issue。

## Session 生命周期

```text
planned
  ↓
active
  ├──→ paused
  │      ↓
  └──── active
  ↓
completed
```

异常路径：

```text
planned / active
→ abandoned
```

### completed

只表示本 Session 的目标达到，例如：

- 完成一个小节首次 Learning；
- 完成一个 Prediction pass；
- 完成一次 closed-book Reconstruction。

### abandoned

适用于：

- PaperRevision binding 错误；
-重大 segmentation 问题；
- boundary preflight 导致不可恢复 lookahead contamination；
- 当前 Session 无法保持原 contract。

Abandoned Session 保留审计事实，不改写成成功。

## 多次 Session 的关系

同一 Paper 可以有：

```text
Session A：首次逐句 Learning
Session B：Prediction
Session C：Recall
Session D：Reconstruction
Session E：Transfer
Session F：Retrospective
Session G：Revision comparison
```

这些不是永久固定流水线。每次 Session 按自己的目标划界。

## Fresh-conversation 恢复

```text
thin prompt
→ AGENTS.md
→ target Issue live state
→ latest checkpoint / handoff
→ bound canonical docs / Profile
→ verify Source identity / scope / position
→ execute exactly one next_action
→ persist result
→ STOP
```

Session 不应依赖完整旧 conversation 才能继续。

## 核心不变量

```text
一个 Session 有明确边界。
Session 必须绑定 PaperRevision + Source provider。
planned_scope 保留历史，current_scope_boundary 控制 reveal。
首次 Session revealed_position 只能向前。
Profile version 不能静默切换。
Prediction 必须先于 actual reveal。
Checkpoint 支持操作续作，Learning Artifact 支持理解恢复。
Source Fact / Derived / Unknown 保持可区分。
Session completed 不等于 Paper done。
```
