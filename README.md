# Paper Reading Lab

Paper Reading Lab 是一个以论文原文为第一手资料、由 AI 陪伴逐句阅读、持续重建作者显式论证结构，并通过反复提取、预测和迁移训练形成研究与系统设计思维的学习实验室。

本仓库首先服务“阅读与学习过程”，而不是把论文快速加工成摘要、知识卡片或结论集合。

## 核心目标

训练的不是“记住论文说了什么”，而是逐渐形成这样的阅读反应链路：

```text
当前句子
+
此前已经揭示的上下文
        ↓
理解字面含义
        ↓
识别当前句在论证中的作用
        ↓
恢复新增的事实 / 约束 / 问题 / 决策
        ↓
理解为什么作者此时走到这里
        ↓
更新当前问题模型
        ↓
预测下一步合理方向
        ↓
读取下一句
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
2. **逐句阅读。** 默认最小学习单元是一个 `SentenceUnit`，必要时可退回短语或扩展到相邻句，但不能默认整节总结替代阅读。
3. **上下文只向前增长。** 当前解释只能使用已经揭示的前文与当前句。
4. **禁止偷看未来。** 首次顺序阅读时，尚未揭示的后文不得参与当前解释、预测或评分。
5. **学习箭头，而不是背文字。** 重点理解“为什么从 A 走到 B”，而不是记忆 AI 的表述。
6. **显式结构可训练。** 记录 cue、relation、problem、constraint、decision、response/update 等可观察结构，不保存或要求模型暴露私有 chain-of-thought。
7. **Source 与 Derived 分层。** 句子切分、解释、推理结构、预测、回顾和知识提炼都属于派生层。
8. **允许反复阅读。** 一篇论文可以有多个 `ReadingSession`；一次读完不意味着永久 `processed=true`。
9. **第一遍与回顾遍分开。** 首次阅读严格 no-lookahead；知道全文后的回顾必须明确标记为 retrospective，不能伪装成首次阅读。
10. **阅读过程与知识资产分离。** 本仓库不承担所有论文知识的最终“done”状态。
11. **预测必须可失败。** 预测下一步的价值在于暴露自己的模型，不要求和作者完全一致。
12. **不确定性必须保留。** 原文不清楚、版本不确定、句子切分有歧义时显式记录，不用 AI 自动补全。

## 学习模式

### Learning Mode

AI 一次揭示一个 Source unit，并逐层帮助理解：

```text
这句话说了什么？
        ↓
它和前文是什么关系？
        ↓
它新增了什么？
        ↓
为什么此时需要这一步？
        ↓
当前问题模型如何变化？
```

目标是先学习高质量、可复用的显式思考结构。

### Prediction Mode

在揭示下一句以前，先尝试回答：

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
→ Alternatives
→ Decisions
→ Mechanisms
→ Trade-offs
→ Evidence
```

### Transfer Mode

换一个表面不同但结构相近的问题，验证是否真正获得可迁移的研究或系统设计能力。

## 领域分层

```text
Source
  论文身份、版本、来源定位、页码、原始文本引用位置

Segmentation
  Section / Paragraph / SentenceUnit 边界与稳定定位

Reading
  ReadingSession、revealed position、当前解释、预测与更新

Training
  Recall、Reconstruction、Transfer、薄弱连接与再次训练

Export
  经复核后可向其他知识仓库输出的候选事实、机制、问题或设计关系
```

详细模型见：

- `docs/domain/model.md`

## Source-First 顺序阅读

首次阅读第 `N` 个句子时，只允许使用：

```text
SentenceUnit 1..N-1
+
SentenceUnit N
+
当前模式允许使用的既有背景知识
```

禁止使用：

```text
SentenceUnit N+1..end
```

详细协议见：

- `docs/learning/source-first-sentence-reading.md`

## ReadingSession

阅读状态不写回 Raw Source，而是通过独立 Session 累积。

一个 Session 至少应能回答：

```text
读的是哪一个 PaperRevision？
当前揭示到哪里？
采用什么 mode？
当前关注什么？
发现了哪些可复用结构？
哪里仍然不理解？
下一次应该从哪里继续？
```

详见：

- `docs/learning/reading-sessions.md`

## 与现有仓库的边界

### `paper-reading-lab`

回答：

> 我怎样逐步理解作者的思考过程，并把这种思考方式训练成自己的能力？

### `classic-papers-system-design`

回答：

> 这篇经典论文最终可以沉淀出哪些经过严格复核的系统设计知识资产？

### `systems-mechanism-lab`

回答：

> 这些机制在真实系统里到底怎样工作，哪些 claim 可以通过实验与证据验证？

因此推荐关系是：

```text
paper-reading-lab
    阅读、理解、预测、重建
        ↓ 候选输出
classic-papers-system-design
    严格事实与分析资产
        ↓ 机制问题
systems-mechanism-lab
    白盒实验、证据与 claim 更新
```

三个仓库可以互相引用，但不能互相吞并生命周期和状态语义。

详细边界见：

- `docs/architecture/boundaries.md`

## 版权与 Source Policy

本仓库默认按公开仓库治理。

除非许可证或权利状态明确允许，不直接提交完整受版权保护的论文 PDF 或全文转换文本。优先保存：

- 论文身份元数据
- 官方 / 作者 / 机构来源 URL
- 页码、章节、段落和句子定位信息
- 必要的短引用
- 自己生成的 Derived 阅读记录

完整 Source 的合法本地副本、连接器读取或外部存储不自动进入 Git 历史。

详见：

- `docs/source/source-policy.md`

## 当前阶段

当前处于机制建立阶段：

```text
定义边界
→ 定义 Source / SentenceUnit / ReadingSession
→ 定义 no-lookahead 阅读协议
→ 定义不变量
→ 选 1 篇经典论文做 Pilot
→ 实际逐句完成一个小节
→ 进行第二遍 Recall / Reconstruction
→ 修正机制
→ 再扩展论文集合
```

在 Pilot 证明“逐句定位稳定、上下文不倒灌、Session 可恢复、阅读确实能形成可复用推理结构”之前，不追求大量论文迁入。

## 基础文档

- `docs/architecture/boundaries.md`
- `docs/domain/model.md`
- `docs/learning/source-first-sentence-reading.md`
- `docs/learning/reading-sessions.md`
- `docs/workflows/paper-reading-lifecycle.md`
- `docs/source/source-policy.md`
- `docs/validation/invariants.md`

## 仓库语言

面向人的文档默认使用中文；稳定 machine identity、schema 字段和必要的论文原文保持其原始语言。论文原文不得为了语言统一而改写。
