# Kafka 2011 首个逐句阅读 Pilot

## 文档状态

```text
historical execution protocol
+
original acceptance baseline
```

首个 Pilot 已经完成，结果为：

```text
COMPLETED WITH FINDINGS
```

本文件保留**当时计划如何验证机制**，不承担当前 Session / next action。实际 closure、scope drift 和后续 hardening 见：

- [`first-pilot-closure.md`](first-pilot-closure.md)
- Kafka Primary Paper Issue 的最新 durable records。

## 为什么选择 Kafka 2011

论文：

*Kafka: a Distributed Messaging System for Log Processing*

选择原因：

- 经典且长期有价值；
- 篇幅较短；
- problem → design goal → mechanism → evidence 链条清楚；
- 已有经过核对的 PaperRevision；
- 双栏 PDF 能真实暴露 Source order / fidelity 风险；
- 适合验证逐句、Prediction、Recall 和 Reconstruction。

## Pilot 目标

首轮目标不是读完整篇论文，而是验证：

```text
PaperRevision binding
→ reading-mcp Source binding
→ canonical SourceUnit order
→ precise TextLocator
→ source-first / no-lookahead Learning
→ durable checkpoint
→ fresh-conversation recovery
→ Prediction before reveal
→ Recall
→ Reconstruction
→ retrospective / closure
```

## 原始 planned scope

首轮历史计划：

```text
Abstract
→ Section 1 Introduction
```

这条范围必须保留为原计划。

实际 Session 后来推进到 Section 3.1，因此：

```text
scope discipline = FAIL
```

不能把实际范围改写成原计划的一部分。该失败推动了后续 `planned_scope` / `current_scope_boundary` hardening。

## Paper / Revision identity

```text
paper_id:
kafka-2011-distributed-messaging

revision_id:
kafka-2011-netdb11

reading provider:
reading-mcp
```

首次 Session 禁止读取既有 Kafka 下游分析资产来帮助解释或预测。

## Gate 0 — Source binding

正式阅读前记录：

```text
paper_id
revision_id
canonical source / provenance
reading_document_id
content_hash
normalized_document_hash
normalization / reading profile version
segmentation_version
media_type
known limitations
```

identity 冲突时停止，不能为了方便继续。

## Gate 1 — Source fidelity / order

Kafka PDF 是双栏排版，Pilot 需要验证：

- canonical section / paragraph / sentence order；
- 页眉页脚是否混入正文；
- Sentence / Paragraph degradation；
- TextLocator 是否可 exact re-read；
- Figure / Table 是否需要 original source view；
- parser / segmentation finding 是否 durable。

Normalized text 正确不自动证明原页视觉结构正确。

## Gate 2 — Session scope

后续 hardening 后的规范要求：

```text
planned_scope
+
current_scope_boundary
```

每次 reveal 前：

```text
next canonical unit inside boundary?
├── yes → allowed
└── no  → STOP before reveal
          → durable scope amendment required
```

原 Pilot 开始时尚未形成这条 executable gate，导致实际 scope drift。该历史事实保留。

## Session A — Learning

严格 no-lookahead：

```text
revealed past
+
current canonical SourceUnit
        ↓
literal meaning
        ↓
relation to revealed past
        ↓
actual cognitive increment
        ↓
current problem model update
        ↓
Source Fact / Derived / Unknown
        ↓
locator + stop boundary
        ↓
STOP
```

默认一次推进一个 canonical SourceUnit；若 provider unit 包含多个 surface sentences，保留 provider identity。

## Session B — Prediction

在下一 SourceUnit reveal 前形成并持久化：

```text
based_on_position
candidate directions
confidence
created_at
```

然后：

```text
actual next SourceUnit
→ match / partial / mismatch
→ missing cue / misconception
→ model update
```

原 Prediction 不得事后覆盖美化。

## Session C — Recall

间隔后测试主动恢复：

- 当前问题背景；
- 关键约束；
- design pressure；
- 已揭示机制；
- 关键 reasoning links。

记录：

```text
spontaneous recall
cue level
recovery after cue
knowledge gap
reasoning gap
```

目标不是简单“答对 / 答错”。

## Session D — Reconstruction

闭卷重建已读范围：

```text
Problem
→ Constraints
→ Alternatives
→ Decisions
→ Mechanisms
→ Trade-offs
→ Evidence
```

必须记录提示级别，且不能加入未读后文或现代 Kafka 实现。

## Original source fidelity

遇到 Figure / Table / Equation / 多栏布局：

```text
current allowed TextLocator
→ original source view
→ visual observation
```

必须区分：

```text
text Source Fact
original-page visual observation
AI interpretation
```

看到整页不授权使用未来正文。

## Durable state

Pilot 后确认需要区分：

### Operational Recovery Checkpoint

用于恢复：

```text
Source / Revision identity
Session / scope / position
latest locator
immutable prediction
blocker / finding
exactly one next action
```

### ReadingSession Learning Artifact

用于支持：

```text
explicit reasoning links
current problem model
knowledge / reasoning gaps
cue history
prediction comparisons
reconstruction findings
```

因此：

```text
Operational Checkpoint
≠ Learning Artifact
≠ Primary Issue summary
≠ full transcript
```

## Primary Issue 原则

```text
1 Paper
→ 1 Primary Paper Issue
```

Issue 保存：

- Paper / Revision / Source 摘要；
- Session summary / references；
- blocker / scope amendment / handoff；
- next action。

Issue 不保存论文全文、每句长解释或完整 transcript。

## 首轮 success criteria

首个 Pilot 原本希望验证：

1. PaperRevision / Source binding 稳定；
2. canonical SourceUnit 顺序可恢复；
3. precise TextLocator 可 exact re-read；
4. no-lookahead 能执行；
5. checkpoint 能跨 conversation 恢复；
6. Prediction 先于 actual reveal；
7. Prediction comparison 能暴露 reasoning gap；
8. Recall 可主动恢复关键连接；
9. Reconstruction 可重建已读论证；
10. Figure / layout 可以回 original source；
11. stale identity fail closed；
12. scope boundary 在 reveal 前执行；
13. checkpoint 与 learning artifact 分工清楚；
14. Session completed 不等于 Paper done。

实际结果不是全部 PASS，详见 closure matrix。

## 失败也必须保留

Pilot finding 不能为了形成“成功案例”而删除：

- scope drift；
- Recall / Reconstruction PARTIAL；
- Issue body / comment live-state drift；
- runtime tool binding failure；
- transient locator serialization failure；
- segmentation / visual fidelity 只验证部分 case。

## Pilot 完成语义

```text
mechanism path exercised
+
findings persisted
+
retrospective completed
```

不表示：

```text
all checks PASS
Kafka Paper done
future Sessions unnecessary
```

## 后续改进顺序

```text
real Session
→ finding
→ minimal workflow / domain fix
→ invariant
→ deterministic validator where justified
→ automation only after repeated evidence
```

首个 Pilot 后已经完成 scope gate、checkpoint / learning artifact 分离、Explanation Profile、thin-entry governance、Source-First Reading Skill 和基础 repository consistency check 等最小 hardening。
