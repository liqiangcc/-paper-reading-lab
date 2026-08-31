# Paper Reading Lab

Paper Reading Lab 是一个以论文原文为第一手资料、由 AI 陪伴逐步阅读、持续重建作者显式论证结构，并通过反复提取、预测和迁移训练形成研究与系统设计思维的学习实验室。

本仓库首先服务“阅读与学习过程”，而不是把论文快速加工成摘要、知识卡片或结论集合。

## 核心目标

训练的不是“记住论文说了什么”，而是逐渐形成这样的阅读反应链路：

```text
当前 Source Unit
+
此前已经揭示的上下文
        ↓
理解字面含义
        ↓
识别当前单元在论证中的作用
        ↓
恢复新增的事实 / 约束 / 问题 / 决策
        ↓
理解为什么作者此时走到这里
        ↓
更新当前问题模型
        ↓
预测下一步合理方向
        ↓
读取下一 Source Unit
        ↓
继续修正
```

长期目标是从：

```text
“我读过这篇论文”
```

逐渐变成：

```text
“面对作者当时的问题，即使遮住后文，我也能开始推出类似的下一步。”
```

## 核心原则

1. **Source First。** 论文原文是第一手证据，任何摘要、解释、知识卡片都不能反向修改原文事实。
2. **逐句优先。** 默认希望以 Sentence 作为最小学习单元，但 Source 真实结构优先；必要时接受 coarse Paragraph、公式、图表、伪代码等最小可靠 Source Unit。
3. **上下文只向前增长。** 当前解释只能使用已经揭示的前文与当前 Source Unit。
4. **禁止偷看未来。** 首次顺序阅读时，尚未揭示的后文不得参与当前解释、预测或评分；优先通过 Source access boundary 实现，而不仅靠 Prompt。
5. **学习箭头，而不是背文字。** 重点理解“为什么从 A 走到 B”，而不是记忆 AI 的表述。
6. **显式结构可训练。** 记录 cue、relation、problem、constraint、decision、mechanism、evidence、update 等可观察结构，不保存或要求模型暴露私有 chain-of-thought。
7. **Source 与 Derived 分层。** 定位、解释、推理结构、预测、回顾和知识提炼必须能分开审计。
8. **允许反复阅读。** 一篇论文可以有多个 `ReadingSession`；一次读完不意味着永久 `processed=true`。
9. **第一遍与回顾遍分开。** 首次阅读严格 no-lookahead；知道全文后的回顾必须明确标记为 retrospective，不能伪装成首次阅读。
10. **阅读过程与知识资产分离。** 本仓库不承担所有论文知识的最终“done”状态。
11. **预测必须可失败。** 预测下一步的价值在于暴露自己的模型，不要求和作者完全一致。
12. **不确定性必须保留。** 原文不清楚、版本不确定、定位退化时显式记录，不用 AI 自动补全。
13. **不重复制造 Source identity。** 精确 Section / Paragraph / Sentence identity 默认由 `reading-mcp` 提供，本仓库保存引用。
14. **Issue 是控制面。** GitHub Issue 组织工作和长期入口，但不是 Source truth，也不是完整学习 transcript。

## 三层架构

```text
reading-mcp
  Source 获取 / 解析 / 结构 / TextUnit / TextLocator / cursor / stale
        ↓
paper-reading-lab
  PaperRevision / ReadingSession / ReadingStep / Prediction / Recall / Reconstruction
        ↓
GitHub Issue
  Paper 工作入口 / 当前状态 / Session summary / blocker / next action
```

### `reading-mcp`

回答：

> 当前合法 Source 是什么？正文结构和 canonical 顺序是什么？当前最小可靠 Source Unit 如何稳定定位？

Paper Reading Lab 默认不重新实现 PDF / EPUB / HTML 解析，也不平行生成 Sentence identity。

详细契约：

- `docs/integrations/reading-mcp.md`

### `paper-reading-lab`

回答：

> 我怎样逐步理解作者的思考过程，并把这种思考方式训练成自己的能力？

### GitHub Issue

回答：

> 当前这篇 Paper 在做什么、绑定哪个 Revision、有哪些 Session、哪里阻塞、下一步是什么？

核心关系：

```text
1 Paper → 1 Primary GitHub Issue
1 Paper → N ReadingSessions
1 ReadingSession → N ReadingSteps / checkpoints
```

详细工作流：

- `docs/workflows/issue-driven-workflow.md`

## 学习模式

### Learning Mode

AI 一次只处理当前允许 reveal 的 Source Unit，并逐层帮助理解：

```text
这句话 / 单元说了什么？
        ↓
它和已揭示前文是什么关系？
        ↓
它新增了什么？
        ↓
为什么此时需要这一步？
        ↓
当前问题模型如何变化？
```

目标是先学习高质量、可复用的显式思考结构。

### Prediction Mode

在揭示下一 Source Unit 以前，先尝试回答：

```text
基于目前信息，作者下一步可能处理什么？
有哪些合理分支？
什么约束会影响选择？
```

然后再读取原文，对比作者实际选择。

### Recall Mode

遮住解释或原文的一部分，由学习者主动重建：

```text
当前 cue
→ 问题
→ 约束
→ 决策
→ 后果
```

目标是从“看着理解”过渡到“不看也能生成”。

### Reconstruction Mode

完成一节或一篇后，闭卷尝试重建：

```text
Problem
→ Constraints
→ Alternatives（Source 支持时）
→ Decisions
→ Mechanisms
→ Trade-offs
→ Evidence / Boundary
```

### Transfer Mode

换一个表面不同但结构相近的问题，验证是否真正获得可迁移的研究或系统设计能力。

## 领域分层

```text
Source
  Paper identity、Revision、canonical Source、reading-mcp binding

Source Reference
  SourceUnitRef / TextLocator / TextUnit identity / display locator

Reading
  ReadingSession、ReadingStep、revealed position、当前解释、预测与更新

Training
  Recall、Reconstruction、Transfer、薄弱连接与再次训练

Workflow
  Primary Paper Issue、Session summary、blocker、next action

Export
  经复核后可向其他知识仓库输出的候选事实、机制、问题或设计关系
```

详细模型见：

- `docs/domain/model.md`

## Source-First 顺序阅读

首次阅读第 `N` 个 Source Unit 时，只允许使用：

```text
已 reveal 的 Source Units
+
当前 Source Unit
+
当前模式明确允许的既有背景知识
```

禁止使用尚未 reveal 的未来正文。

推荐真实执行：

```text
ReadingSession.revealed_position = N
        ↓
reading-mcp 只提供当前允许 Source Unit
        ↓
理解 / checkpoint / prediction
        ↓
显式 next
        ↓
cursor 前进
```

详细协议见：

- `docs/learning/source-first-sentence-reading.md`
- `docs/integrations/reading-mcp.md`

## ReadingSession 与推理记录

阅读状态不写回 Raw Source，而是通过独立 Session 累积。

一个 Session 至少应能回答：

```text
读的是哪一个 PaperRevision？
当前 Source binding 是什么？
已经 reveal 到哪里？
采用什么 mode？
当前问题模型是什么？
形成了哪些可复用 reasoning links？
哪里判断错或仍然不理解？
下一次应该从哪里继续？
```

长期保存的是结构化 checkpoint，而不是完整 AI transcript。

详见：

- `docs/learning/reading-sessions.md`
- `docs/domain/model.md`

## 与现有知识仓库的边界

### `classic-papers-system-design`

回答：

> 这篇经典论文最终可以沉淀出哪些经过严格复核的系统设计知识资产？

### `systems-mechanism-lab`

回答：

> 这些机制在真实系统里到底怎样工作，哪些 claim 可以通过实验与证据验证？

因此推荐关系是：

```text
reading-mcp
    提供可信 Source 上下文
        ↓
paper-reading-lab
    阅读、理解、预测、重建
        ↓ 候选输出
classic-papers-system-design
    严格事实与分析资产
        ↓ 机制问题
systems-mechanism-lab
    白盒实验、证据与 claim 更新
```

这些系统可以互相引用，但不能互相吞并生命周期和状态语义。

详细边界见：

- `docs/architecture/boundaries.md`

## 版权与 Source Policy

本仓库默认按公开仓库治理。

除非许可证或权利状态明确允许，不直接提交完整受版权保护的论文 PDF 或全文转换文本。优先保存：

- 论文身份元数据
- 官方 / 作者 / 机构来源 URL
- `reading-mcp` document / locator binding
- 页码、章节等显示定位
- 必要且克制的短引用
- 自己生成的 Derived 阅读记录

完整 Source 的合法本地副本、`reading-mcp` cache 或外部来源不自动进入 Git 历史。

详见：

- `docs/source/source-policy.md`

## 当前 Pilot

首个机制 Pilot 已固定为：

```text
Paper:
In Search of an Understandable Consensus Algorithm
Diego Ongaro, John Ousterhout
USENIX ATC 2014

Revision:
raft-2014-usenix-atc14

Scope:
Section 1 — Introduction

Source Adapter:
reading-mcp

Primary Issue:
#1
```

目标闭环：

```text
PaperRevision binding
→ SourceUnit coverage
→ Learning
→ checkpoint recovery
→ Prediction
→ Recall
→ Reconstruction
```

在这个闭环证明有效前，不追求大量论文迁入、复杂 schema 或自动知识图谱。

执行入口：

- `docs/pilot/first-pilot.md`
- GitHub Issue #1

## 基础文档

- `docs/README.md`
- `docs/architecture/boundaries.md`
- `docs/domain/model.md`
- `docs/integrations/reading-mcp.md`
- `docs/learning/source-first-sentence-reading.md`
- `docs/learning/reading-sessions.md`
- `docs/workflows/issue-driven-workflow.md`
- `docs/workflows/paper-reading-lifecycle.md`
- `docs/source/source-policy.md`
- `docs/validation/invariants.md`
- `docs/pilot/first-pilot.md`

## 仓库语言

面向人的文档默认使用中文；稳定 machine identity、schema 字段和必要的论文原文保持其原始语言。论文原文不得为了语言统一而改写。
