# 领域模型

## 目的

本文件定义 Paper Reading Lab 最小领域对象，以及它们之间不能混淆的身份和状态。

第一版只定义支持 Pilot 所需的对象，不追求一次把所有学习行为结构化。

## 总体关系

```text
Paper
  └── PaperRevision
        └── SourceLocator
              └── SectionUnit
                    └── ParagraphUnit
                          └── SentenceUnit

PaperRevision
  └── ReadingSession
        └── ReadingCheckpoint
              ├── Observation
              ├── Prediction
              ├── KnowledgeGap
              └── TrainingResult
```

## Paper

`Paper` 表示“作品身份”，而不是某个具体 PDF 文件。

建议字段：

```text
paper_id
title
authors
publication_year
venue
canonical_identifier
```

`paper_id` 应使用仓库内稳定 machine identity，不依赖目录标题显示文本。

## PaperRevision

`PaperRevision` 表示一次具体可读取版本。

同一 Paper 可能存在：

- conference version
- journal version
- author manuscript
- publisher version
- corrected version
- technical report version

这些版本不能自动视为完全相同。

建议字段：

```text
revision_id
paper_id
version_label
source_url
source_kind
captured_or_verified_at
content_fingerprint
limitations
```

首次顺序阅读必须绑定一个明确 `revision_id`。

如果阅读过程中更换版本，应创建新 Session 或显式记录 revision change，不能静默切换。

## SourceLocator

`SourceLocator` 用于定位原文，不承担解释。

优先使用稳定定位组合：

```text
section
page
paragraph_index
sentence_index
figure/table/equation id
```

不同格式之间页码可能不同，因此 locator 允许同时保存：

```text
published_page
pdf_page
section_path
local_order
```

## SectionUnit

论文自然章节单元。

作用：

- 导航
- session 范围控制
- sentence identity 的上层上下文

SectionUnit 不等于知识主题。

## ParagraphUnit

原文段落单元。

逐句阅读默认保留段落边界，因为句子的意义经常依赖同段前文。

段落边界属于 Source structure 或 conversion projection，必须说明来源。

## SentenceUnit

`SentenceUnit` 是默认最小顺序阅读单元。

建议 identity：

```text
sentence_unit_id = revision_id + section path + paragraph order + sentence order
```

建议字段：

```text
sentence_unit_id
revision_id
section_id
paragraph_index
sentence_index
source_locator
source_text_ref
segmentation_status
```

### SentenceUnit 不是永久语言学真理

PDF 转文本、公式、引用、缩写和脚注都可能造成句子边界歧义。

因此 `segmentation_status` 至少允许：

```text
confirmed
provisional
ambiguous
```

如果一个句子无法独立构成最小有用输入，可以把相邻句作为一次 reveal group，但必须保留原始顺序和边界信息。

## ReadingSession

`ReadingSession` 表示一次有边界的学习过程。

建议字段：

```text
session_id
paper_id
revision_id
mode
scope
started_at
revealed_position
focus
prior_knowledge_policy
lookahead_policy
status
completed_at
```

`mode` 第一版建议支持：

```text
learning
prediction
recall
reconstruction
transfer
retrospective
```

一个 Session 可以完成；一篇 Paper 不存在永久“学习完成”。

## ReadingCheckpoint

`ReadingCheckpoint` 是可恢复的学习状态，不是完整聊天记录。

建议记录：

```text
session_id
revealed_position
current_sentence_unit_id
literal_meaning
relation_to_previous
observed_cues
current_problem_model
new_constraints
explicit_structure
prediction
knowledge_gaps
questions_to_revisit
next_action
```

第一版不要求所有字段必填。

真正必须稳定的是：

```text
revision
position
mode
source/derived boundary
no-lookahead status
```

## Observation

`Observation` 表示当前 Source 支持的可观察阅读发现。

例如：

```text
这句话明确提出了前一个方案的限制。
这句话增加了一个性能约束。
这句话从 problem statement 转入 design decision。
```

Observation 必须能指回 Source locator。

## ExplicitReasoningStructure

学习“思维链”时，本仓库保存的是显式、可训练结构，而不是私有 chain-of-thought。

常见节点：

```text
cue
fact
assumption
problem
constraint
alternative
decision
mechanism
consequence
trade-off
evidence
boundary
update
```

常见边：

```text
supports
contrasts
causes
constrains
motivates
requires
chooses
implements
produces
limits
validates
updates
```

第一版可以只在人类可读 Session checkpoint 中表达，不急于图数据库化。

## Prediction

Prediction 是在下一 Source unit 揭示以前形成的候选下一步。

建议记录：

```text
based_on_position
candidate_directions
reasoning_basis
confidence
actual_next_unit
comparison
```

Prediction 不进入 Source truth。

## KnowledgeGap

表示阅读过程中暴露的缺口，例如：

```text
术语不理解
机制背景不足
数学推导缺口
无法解释作者为什么转向该方案
能理解文字但无法预测下一步
```

KnowledgeGap 是训练计划输入，不代表论文错误。

## TrainingResult

用于 Recall / Reconstruction / Transfer。

可观察维度可以包括：

```text
能否恢复问题
能否恢复关键约束
能否解释决策理由
能否恢复机制链
能否识别边界与 trade-off
是否依赖提示
是否能迁移到新问题
```

不建议第一版制造复杂总分。

先记录“在哪个连接断掉”比一个 82 分更有价值。

## ExportCandidate

阅读中可能产生值得进入下游仓库的内容：

```text
source fact candidate
problem candidate
mechanism candidate
trade-off candidate
engineering mapping candidate
experiment question candidate
```

这些只是 `ExportCandidate`。

正式进入其他仓库前必须经过目标仓库自己的 review / validator / gate。

## 核心身份不变量

```text
Paper identity ≠ PaperRevision
PaperRevision ≠ Source file path
SentenceUnit identity ≠ 句子文本内容本身
ReadingSession identity ≠ AI conversation id
ReadingCheckpoint ≠ transcript
Prediction ≠ Source fact
ExportCandidate ≠ validated knowledge
```
