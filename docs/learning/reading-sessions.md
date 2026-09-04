# ReadingSession 学习会话

## 目的

真实论文可以被反复阅读，每次阅读的目标、已知背景和训练方式都可能不同。

`ReadingSession` 表示一次有明确边界、可暂停、可恢复、可完成的阅读过程。

它不修改 Raw Source，也不代表整篇论文永久“学完”。

## 核心原则

```text
Source 保持稳定。
Session 独立累积。
理解可以深化、修正和迁移。
```

不能因为完成一次 Session，就给 Paper 写入永久：

```text
processed = true
```

## Session 必须绑定什么

最少绑定：

```text
paper_id
revision_id
mode
scope
lookahead_policy
revealed_position
```

其中：

- `revision_id` 防止阅读过程中静默换版本。
- `scope` 限定本次是全文、章节、小节或某个问题范围。
- `lookahead_policy` 明确是否是首次 no-lookahead 阅读。
- `revealed_position` 是可恢复阅读状态。

采用正式 Explanation Profile 的 Session 还必须绑定 `style_profile`，用于固定解释风格的 machine identity 与版本。

## Session Mode

### Learning

AI 逐句、逐层解释当前 Source unit。

目标：

- 理解字面
- 识别 cue
- 识别句间关系
- 建立当前问题模型
- 学习可复用显式结构

### Prediction

在揭示下一 Source unit 前，学习者先预测下一步合理方向。

目标：

- 训练问题推进能力
- 暴露当前模型缺失
- 对比作者真实选择

### Recall

隐藏部分原文或 Derived 解释，要求主动提取：

```text
cue
→ problem
→ constraint
→ decision
→ consequence
```

目标：从熟悉感转向可主动生成。

### Reconstruction

按段、节或整篇闭卷重建论文的主要结构：

```text
Problem
→ Constraints
→ Alternatives
→ Decisions
→ Mechanisms
→ Trade-offs
→ Evidence
```

### Transfer

给一个新问题，要求调用从论文中学到的思考结构。

Transfer 不是复述论文，而是验证迁移。

### Retrospective

已经知道后文或全文后重新阅读。

必须显式标记：

```text
lookahead_policy = retrospective
```

不能用于伪造首次阅读时的判断。

## Session Scope

建议允许：

```text
paper
section
paragraph_range
sentence_range
question_focus
mechanism_focus
```

第一版 Pilot 优先使用一个小节，而不是整篇论文。

原因是先验证：

```text
逐句定位
→ no-lookahead
→ checkpoint
→ 恢复
→ 下一句
```

是否真的可用。

## Explanation Profile binding

Source-first 协议规定允许读取什么以及何时允许读取；Explanation Profile 规定已经取得当前 SourceUnit 后怎样解释和呈现。

采用正式 Profile 的 Session 建议绑定：

```yaml
style_profile:
  id: source-first-incremental-explanation
  version: v0.1
  source: docs/learning/incremental-explanation-profile.md

style_overrides:
  language: zh-CN
  depth: adaptive
```

其中：

- `id + version` 共同标识一个具体 Profile；
- `source` 指向 canonical Profile 文档；
- `style_overrides` 只能在 Profile 允许范围内调整语言或深度，不能取消 MUST 规则；
- 未绑定正式 Profile 的历史 Session 不应被事后假定使用了当前最新 Profile。

### Profile version 不能静默切换

Session 开始后，历史 ReadingStep 和 checkpoint 继续绑定开始时采用的 Profile version。

如果希望采用新版本，应：

- 新建 Session；或
- 显式记录 Profile transition、切换位置和影响。

不得因为仓库中的 Profile 文件更新，就把旧 checkpoint 静默解释为新版本。

### Handoff 只引用 Profile identity

Issue comment 或 `[SESSION HANDOFF]` 应保存：

```text
profile id
profile version
canonical source path
必要的 style overrides
```

不应复制一份越来越长的 Style Prompt。Fresh conversation 应读取 canonical Profile，再结合 checkpoint 恢复风格。

## revealed position

首次顺序 Session 中：

```text
revealed_position
```

只能单调向前。

如果用户回看前一句，只是视图位置后退，不代表允许未来信息进入过去 checkpoint。

因此需要区分：

```text
revealed_position     已经揭示到哪里
view_position         当前正在回看哪里（可选）
```

## ReadingCheckpoint

Session 不应该依赖完整聊天记录才能继续。

一个实用 checkpoint 建议包含：

```text
session_id
revision_id
mode
scope
revealed_position
current_sentence_unit_id
focus
current_problem_model
new_constraints
observed_relations
explicit_structure
prediction_state
style_profile
style_overrides
knowledge_gaps
open_questions
stop_boundary
next_action
```

### 不保存什么

默认不沉淀：

- 大量重复解释
- 整段 AI transcript
- 没有复用价值的寒暄
- 模型私有 chain-of-thought

保存 checkpoint 的目标是：

> 换一个会话以后，仍然可以在不偷看未来的前提下继续学习。

其中 `stop_boundary` 应明确本次 ReadingStep 已经完成到哪里，以及下一独立 SourceUnit 尚未 reveal；它与 precise locator 一起构成可审计的停止位置。

## Observation 与 Interpretation

Checkpoint 内建议区分：

### Source-grounded Observation

例如：

> 当前句明确说方案 A 在条件 C 下性能下降。

### Derived Interpretation

例如：

> 这更像是在为后续重新设计数据布局制造动机。

Derived interpretation 可以以后被修正。

## Prediction checkpoint

预测必须发生在下一 Source unit reveal 前。

建议记录：

```text
based_on_position
candidate_directions
confidence
```

揭示后再追加：

```text
actual_next_unit
match_type
what_was_missing
model_update
```

不要事后改写原预测使其“看起来更准”。

## KnowledgeGap

Session 的重要输出不是“读了多少句”，而是发现哪些连接不稳定。

建议分类但不必强制枚举：

```text
term-gap
background-gap
math-gap
mechanism-gap
relation-gap
prediction-gap
reconstruction-gap
transfer-gap
```

例如：

```text
能理解一致性哈希定义
但无法从“节点数量变化导致大规模 remap”主动推出需要新的映射策略
```

这里真正需要训练的是：

```text
constraint
→ design pressure
```

而不是再背一遍定义。

## Session Summary

一个 Session 完成时，只生成短 summary：

```text
读到哪里
本次 focus
最重要的新理解
暴露的 knowledge gaps
形成的可复用 reasoning links
预测 / recall 表现
建议下一 Session
```

不把整个聊天复制进仓库。

## 多次 Session 的关系

同一 Paper 可以有：

```text
Session A：首次逐句 Learning
Session B：同一小节 Prediction
Session C：Recall
Session D：整节 Reconstruction
Session E：Transfer
Session F：知识提升后的 Retrospective
```

这些不是固定编号，也不构成永久 pipeline。

每次 Session 按自己的目标划界。

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

允许：

```text
abandoned
```

例如 Source revision 发现错误，需要放弃旧 Session 并重新开始。

`completed` 只表示本次 session 的目标已完成。

## 核心不变量

```text
一个 Session 有边界。
一篇 Paper 可以有无限多个 Session。
Session 必须绑定 PaperRevision。
首次 Session 的 revealed position 只能向前。
Prediction 必须先于 actual reveal。
Checkpoint 可以恢复学习，但不等于 transcript。
正式 Explanation Profile 必须绑定 id + version。
Session 恢复不得静默切换 Profile version。
Retrospective 必须显式标记。
```
