# 领域模型

## 目的

本文件定义 Paper Reading Lab 最小领域对象，以及它们之间不能混淆的身份和状态。

第一版只定义支持 Pilot 所需的对象，不追求一次把所有学习行为结构化。

## 总体关系

```text
Paper
  └── PaperRevision
        └── ReadingSourceBinding
              └── SourceUnitRef

Paper
  └── 1 Primary GitHub Issue

PaperRevision
  └── ReadingSession
        └── ReadingStep / ReadingCheckpoint
              ├── Observation
              ├── Prediction
              ├── KnowledgeGap
              └── TrainingResult
```

其中 Source 的 Section / Paragraph / Sentence 精确身份默认由 `reading-mcp` 提供；Paper Reading Lab 保存引用，不重新建立平行分句系统。

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
primary_issue
```

`paper_id` 应使用仓库内稳定 machine identity，不依赖目录标题显示文本，也不依赖 GitHub Issue number。

推荐关系：

```text
1 Paper
↕
1 Primary GitHub Issue
```

Issue 是长期工作入口和控制面，不承担 Paper identity 本身。

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
reading_source_binding
limitations
```

首次顺序阅读必须绑定一个明确 `revision_id`。

如果阅读过程中更换版本，应创建新 Session 或显式记录 revision change，不能静默切换。

## ReadingSourceBinding

`ReadingSourceBinding` 把 `PaperRevision` 绑定到实际 Source provider。

第一版首选：

```text
provider = reading-mcp
```

建议字段：

```text
provider
reading_document_id
normalized_document_identity
reading_profile_version
segmentation_version
canonical_source
bound_at
limitations
```

它回答：

> 当前这个 PaperRevision 在阅读基础设施里究竟绑定到哪一个可重复定位的文档身份？

如果 `reading-mcp` 返回 locator / cursor stale，必须停止 precise continuation 并显式 reconcile，不能静默重新匹配。

## SourceUnitRef

`SourceUnitRef` 是对上游当前最小可靠 Source Unit 的引用，不是本仓库重新生成的句子对象。

默认优先引用 `reading-mcp` 返回：

```text
reading_document_id
normalized_document_identity
text_unit_id
text_locator
segmentation_version
requested_kind
actual_kind
```

可以附带便于人类阅读的 display 信息：

```text
section_title
page
paragraph_order
sentence_order
native_location
```

但 display 信息不取代 precise identity。

### 不自行推导 Sentence identity

不再以：

```text
revision_id + section path + paragraph order + sentence order
```

生成平行的 `SentenceUnit` identity。

原因：

- Source conversion 可能变化
- segmentation version 可能变化
- 复杂 block 可能只能提供 coarse Paragraph
- 上游已经有 stale 检测和 precise locator 契约

Paper Reading Lab 的职责是引用 Source，而不是重建 Source identity。

### 逐句是默认，不是伪造精度

当上游可以可靠返回 Sentence 时：

```text
actual_kind = sentence
```

当 Source evidence 只能支持更粗单元时，可以是：

```text
actual_kind = paragraph
```

公式、表格、伪代码、图、列表等也允许使用对应的最小可靠 locator。

原则：

```text
Source evidence > 逐句外观
```

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

首次顺序 Session 的 `lookahead_policy` 应明确为：

```text
past-plus-current-only
```

并优先通过 Source access boundary 保证，而不是只依赖 Prompt 自律。

## ReadingStep

`ReadingStep` 表示一次 Source reveal 及其对应的学习更新。

最小 Source 引用：

```text
session_id
step_index
revision_id
source_unit_ref
revealed_at
```

Derived 可以包括：

```text
literal_meaning
relation_to_previous
observed_cues
current_problem_model
new_constraints
explicit_structure
prediction
actual_next_ref
model_update
knowledge_gaps
```

ReadingStep 不等于聊天消息。

一次 AI 对话可以产生零个、一个或多个候选 Step；只有可恢复、可复用的学习状态才需要沉淀。

## ReadingCheckpoint

`ReadingCheckpoint` 是可恢复的 Session 状态，不是完整聊天记录。

建议记录：

```text
session_id
revision_id
revealed_position
current_source_unit_ref
mode
current_problem_model
key_reasoning_links
active_predictions
knowledge_gaps
questions_to_revisit
next_action
```

第一版不要求所有字段必填。

真正必须稳定的是：

```text
revision
source binding
revealed position
mode
source/derived boundary
no-lookahead status
```

## Observation

`Observation` 表示当前已揭示 Source 支持的可观察阅读发现。

例如：

```text
这句话明确提出了前一个方案的限制。
这句话增加了一个性能约束。
这句话从 problem statement 转入 design decision。
```

Observation 必须能指回当前或此前已揭示的 `SourceUnitRef`。

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
based_on_source_unit_ref
candidate_directions
reasoning_basis
confidence
actual_next_ref
comparison
```

Prediction 不进入 Source truth。

如果 Prediction 在下一 Source 已经被读取以后才生成，必须标记为 retrospective，不能伪装成真正预测。

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

## GitHub Issue

Primary Paper Issue 是工作流控制面。

它负责串联：

```text
Paper identity reference
Source / revision 状态
ReadingSession summaries
当前 blocker
下一步 action
```

它不保存：

- 完整论文全文
- 完整逐句 transcript
- Source truth 的替代版本
- 所有 ReadingStep 的长文本复制

Primary Issue 可以长期作为 case 入口；具体 ReadingSession 自己有 completed 状态。

## 核心身份不变量

```text
Paper identity ≠ PaperRevision
PaperRevision ≠ Source file path
PaperRevision ≠ reading-mcp document identity
SourceUnitRef ≠ 句子文本内容本身
SourceUnitRef ≠ AI 解释
ReadingSession identity ≠ AI conversation id
ReadingCheckpoint ≠ transcript
Primary Issue number ≠ Paper identity
Prediction ≠ Source fact
ExportCandidate ≠ validated knowledge
```
