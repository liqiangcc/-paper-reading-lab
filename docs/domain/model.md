# 领域模型

## 目的

本模型用于区分：

- 论文是什么；
- 当前读取的是哪个版本；
- Source provider 中绑定的是哪个文档；
- 某次 ReadingSession 允许读什么、已经读到哪里；
- 如何恢复操作状态；
- 如何保存比 checkpoint 更丰富、但明显小于 transcript 的学习状态；
- 哪些内容是 Source Fact，哪些只是 Derived Interpretation。

核心原则：

```text
Paper identity
≠ PaperRevision identity
≠ reading provider document identity
≠ ReadingSession identity
≠ GitHub Issue identity
```

## 总体关系

```text
Paper
└── PaperRevision 1..N
    └── ReadingSourceBinding 0..N
        └── SourceUnitRef 0..N

Paper
└── ReadingSession 0..N
    ├── ReadingStep 0..N
    ├── OperationalRecoveryCheckpoint 0..N
    ├── ReadingSessionLearningArtifact 0..N
    ├── ExplanationProfileRef 0..1
    ├── KnowledgeGap 0..N
    └── TrainingResult 0..N

Paper / ReadingSession finding
└── ExportCandidate 0..N
```

## Paper

表示论文这一长期智力对象，不绑定某一个具体文件。

建议字段：

```text
paper_id
canonical_title
authors
year
venue / publication context
canonical identifiers（DOI 等，可选）
primary_issue_ref
```

### 不变量

- `paper_id` 是稳定 machine identity；
- Issue number、标题或 PDF 文件名不能替代 `paper_id`；
- Paper 不存在永久 `done = true`；
- 同一 Paper 可以有多个 Revision 和无限多个 ReadingSession。

## PaperRevision

表示某个可明确识别的论文版本，例如：

- 正式会议版本；
- extended technical report；
- 作者 manuscript；
- 后续修订版。

建议字段：

```text
revision_id
paper_id
revision_kind
publication_identity
canonical_source_ref
source_provenance
raw_hash（可选）
known_relationships
known_limitations
```

### 不变量

- ReadingSession 必须绑定一个 `revision_id`；
- Session 开始后不能静默切换 Revision；
- 新 Revision 不覆盖旧 Session 历史；
- Revision 关系可以通过独立 revision-comparison Session 分析。

## ReadingSourceBinding

把 `PaperRevision` 与具体 Source provider 中的 document identity 关联起来。

建议字段：

```text
binding_id
paper_id
revision_id
provider
reading_document_id
content_hash
normalized_document_hash
normalization_version
reading_profile_version
segmentation_version
media_type
source_location
known_limitations
created_at
```

其中：

```text
revision_id
= 论文版本身份

reading_document_id
= Source provider 内部文档身份

normalized_document_hash
= 当前 normalized projection 身份
```

三者不能相互替代。

### 不变量

- precise continuation 必须同时满足 Revision 与 provider identity；
- normalized identity 变化时旧 locator 默认 stale；
- stale 不能 fuzzy rebase 成“最像文本”；
- Binding limitation 必须 durable，可由 fresh conversation 恢复。

## SourceUnitRef

表示 Source provider 中可精确回读的 canonical 阅读单元引用。

建议字段：

```text
provider
reading_document_id
normalized_document_hash
segmentation_version
text_unit_id（如 provider 提供）
text_locator
actual_kind
content_class
source_order
```

`text_locator` 可以包含：

```text
owner_section_id
section_path
native_location
paragraph_index
sentence_index
normalized_range
content_hash
normalized_document_hash
segmentation_version
```

### 不变量

- 本仓库不平行生成自己的 Sentence identity；
- page / paragraph / sentence display number 不能单独承担 precise identity；
- SourceUnitRef 必须能交回 provider exact re-read；
- coarse Paragraph 不能在本仓库伪装成 Sentence；
- reveal group 只允许组合 canonical 顺序连续单元。

## ExplanationProfileRef

表示 ReadingSession 采用的版本化解释与呈现 Profile。

建议字段：

```text
profile_id
version
source_path
status
style_overrides
bound_at
transition_ref（可选）
```

例如：

```yaml
profile_id: source-first-incremental-explanation
version: v0.1
source_path: docs/learning/incremental-explanation-profile.md
style_overrides:
  language: zh-CN
  depth: adaptive
```

### 不变量

- `profile_id + version` 共同承担 identity；
- Profile 只控制解释与呈现，不扩大 Source 可见范围；
- Session 恢复不得静默采用“仓库最新版”；
- Profile 切换必须新建 Session，或显式记录 transition、位置和影响。

## ReadingSession

表示一次有明确目标、范围、模式和生命周期的学习活动。

建议字段：

```text
session_id
paper_id
revision_id
source_binding_id
mode
learning_goal
lookahead_policy
planned_scope
current_scope_boundary
status
revealed_position
view_position（可选）
style_profile_ref（可选）
created_at
updated_at
contamination_state
```

### planned_scope

Session 创建时的历史计划，例如：

```text
Section 1 — Introduction
sentence_range
mechanism_focus
question_focus
```

它不得被后续范围扩展覆盖。

### current_scope_boundary

当前真正可执行的 reveal gate，例如：

```text
allowed owner_section_id
stop-before next sibling section
max_new_canonical_units
explicit end locator
```

每次新 Source reveal 前都必须检查。

### revealed_position 与 view_position

```text
revealed_position
= Session 已经知道到哪里，只能单调向前

view_position
= 当前回看位置，可以后退
```

回看旧句子不等于删除已经知道的未来内容。

### status

```text
planned
→ active
↔ paused
→ completed

active / planned
→ abandoned
```

- `completed` 只表示本 Session 目标达到；
- `abandoned` 保留 Source identity、contamination 和 failure evidence；
- `Session completed ≠ Paper done`。

## ScopeAmendment

表示 Session 范围的显式 durable 扩展。

建议字段：

```text
amendment_id
session_id
old_boundary
new_boundary
reason
amendment_point
created_at
```

### 不变量

- amendment 必须发生在越界 Source reveal 之前；
- amendment 只改变后续 `current_scope_boundary`；
- 原 `planned_scope` 和旧 boundary 历史保留；
- 用户连续说“下一句”不自动构成 amendment。

## ReadingStep

表示一次有界学习动作。

建议字段：

```text
step_id
session_id
mode
input_source_refs
current_source_ref
source_observations
derived_interpretations
observed_relations
current_problem_model_update
explicit_reasoning_links
knowledge_gaps
prediction_state（可选）
stop_boundary
next_action
created_at
```

### Source / Derived / Unknown

正式 Step 必须能区分：

```text
Source Fact
= 已揭示 Source 直接支持

Derived Interpretation
= 基于已揭示 Source 的有限推论

Unknown
= 当前 Source 尚未回答
```

### stop_boundary

至少表达：

```text
current SourceUnitRef / TextLocator
revealed_position
next independent SourceUnit revealed? false
scope state
next_action
```

### 不变量

- 一个“下一句 / 下一步”默认对应一个有界 ReadingStep；
- 当前解释不能引用未来 SourceUnitRef；
- 显式 reasoning link 必须可追溯到已揭示 Source，或保持 Derived 身份；
- ReadingStep 不等于完整聊天 transcript。

## OperationalRecoveryCheckpoint

用于让 fresh conversation 安全恢复**操作位置和下一动作**。

建议字段：

```text
checkpoint_id
session_id
paper_id
revision_id
source_binding
mode
lookahead_policy
planned_scope
current_scope_boundary
revealed_position
latest_source_ref
style_profile_ref（可选）
immutable_prediction_ref（可选）
blocker / finding
stop_boundary
exactly_one_next_action
created_at
```

它回答：

```text
当前绑定哪一个 Source？
允许读到哪里？
已经 reveal 到哪里？
下一步唯一允许做什么？
```

它不需要保存完整历史解释。

## ReadingSessionLearningArtifact

用于支持后续 Recall、Reconstruction 和 Retrospective。

建议字段：

```text
artifact_id
session_id
paper_id
revision_id
mode
scope / revealed_range
explicit_reasoning_links
current_problem_model
model_update_history（压缩）
knowledge_gaps
reasoning_gaps
cue_level
cue_recovery_result
prediction_comparisons
reconstruction_findings
source_ref_summary
created_at
```

它应：

- 明显小于完整 transcript；
- 比 Operational Recovery Checkpoint 更丰富；
- 保留可主动恢复和重建的关键连接；
- 不把 Derived 内容写成 Source Fact。

因此：

```text
OperationalRecoveryCheckpoint
≠ ReadingSessionLearningArtifact
≠ Primary Issue summary
≠ full transcript
```

## PredictionRecord

表示下一 Source reveal 前冻结的预测。

建议字段：

```text
prediction_id
session_id
based_on_position
candidate_directions
confidence
created_at
actual_next_source_ref（揭示后追加）
match_type（揭示后追加）
what_was_missing（揭示后追加）
model_update（揭示后追加）
```

### 不变量

- `prediction.created_at < actual_next_source.revealed_at`；
- actual reveal 后只能追加 comparison，不能修改原预测；
- Prediction 不能成为 Source Fact。

## KnowledgeGap / ReasoningGap

### KnowledgeGap

描述术语、背景、数学或机制知识不足，例如：

```text
term-gap
background-gap
math-gap
mechanism-gap
```

### ReasoningGap

描述已知信息之间的连接无法主动生成，例如：

```text
relation-gap
prediction-gap
reconstruction-gap
transfer-gap
```

重要区别：

```text
不知道一个定义
≠
知道定义但推不出 design pressure
```

## TrainingResult

表示 Prediction、Recall、Reconstruction 或 Transfer 的一次训练证据。

建议字段：

```text
training_result_id
session_id
mode
source_scope
prompt / cue level
response summary
comparison / review
knowledge_gaps
reasoning_gaps
model_update
```

### 特殊边界

- Recall 展示答案后不能继续算无提示 Recall；
- Reconstruction 必须记录 `closed-book / minimal-cue / outline-assisted / open-source`；
- Transfer 必须使用真正的新问题；
- Retrospective 必须显式声明已知后文。

## ExportCandidate

表示从 ReadingSession 中提炼、等待下游审核的候选知识。

建议字段：

```text
export_candidate_id
paper_id
revision_id
session_id
source_refs
claim
claim_type
source_observation
derived_interpretation
confidence / limitation
target_repository
review_status
```

生命周期：

```text
Reading finding
→ ExportCandidate
→ explicit review
→ target repository gate
→ validated knowledge
```

下游拒绝或修正不改写历史 Source / Session。

## GitHubIssueRef

Issue 是外部控制面引用：

```text
repository
issue_number
role = primary-paper | task | bug
```

### 不变量

- 默认 `1 Paper → 1 Primary Issue`；
- ReadingSession 不默认各建一个 Issue；
- Issue number 不承担 Paper identity；
- Issue summary 不替代 checkpoint / learning artifact；
- Issue close 不等于 Paper learned。

## 状态所有权

```text
Paper / Revision identity
→ paper-reading-lab

Canonical structure / SourceUnit / locator
→ reading-mcp

Session / scope / checkpoint / Profile
→ paper-reading-lab

Current workflow state
→ GitHub Issue durable record

Validated downstream knowledge
→ target repository
```

## 核心不变量

```text
Paper、Revision、provider document、Session、Issue identity 分离。
Session 必须绑定 Revision + Source provider。
planned_scope 保留历史，current_scope_boundary 控制 reveal。
revealed_position 单调向前。
Profile 只控制解释，不控制 Source visibility。
Checkpoint 支持续作，Learning Artifact 支持恢复理解。
Source Fact、Derived Interpretation、Unknown 可区分。
Prediction 先于 actual reveal。
Session completed 不等于 Paper done。
```
