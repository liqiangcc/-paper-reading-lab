# Reading MCP 集成契约

## 目的

Paper Reading Lab 默认使用 `reading-mcp` 作为首选 Source Adapter。

两者必须保持职责分离：

```text
reading-mcp
= 打开来源、解析结构、提供稳定 Source Unit 与定位

paper-reading-lab
= 管理 ReadingSession、学习状态、预测、复盘与训练
```

本仓库不重新实现 PDF / EPUB / HTML / DOCX 解析，不重新建立与 `reading-mcp` 冲突的句子 identity。

## 为什么使用 reading-mcp

Paper Reading Lab 的核心要求包括：

- Source-first
- 逐句或最小可靠 Source Unit 阅读
- canonical 正文顺序
- 可恢复定位
- no-lookahead
- Source 变化后显式失效，而不是模糊重定位

`reading-mcp` 已经提供：

```text
open_document
get_document_structure
get_text_units
get_context
read_document
```

逐句读取时推荐：

```text
open_document
    ↓
读取 reading_profile/v1
    ↓
get_document_structure
    ↓
get_text_units(
  requested_kind = sentence,
  coverage_policy = preserve_source
)
    ↓
TextLocator + TextUnitCursor
    ↓
read_document / get_context
```

`body-order/v1` 负责正文 canonical 顺序；不能把结构树 preorder 自动当成正文阅读顺序。

## Source Unit 所有权

### reading-mcp 拥有

以下内容属于 Source / segmentation 基础设施：

- document identity
- normalized document identity
- Section 结构
- Paragraph / Sentence TextUnit
- TextLocator
- TextUnitCursor
- segmentation version
- source-preserving degradation
- stale locator / stale cursor 判定
- page / section / native location 等可追溯位置

### paper-reading-lab 拥有

以下内容属于学习领域：

- Paper
- PaperRevision 与 reading-mcp document binding
- Primary Paper Issue
- ReadingSession
- ReadingStep / ReadingCheckpoint
- revealed position
- mode
- observed cues
- current problem model
- constraints
- prediction
- actual-next comparison
- model update
- knowledge gap
- Recall / Reconstruction / Transfer result

## 不重新制造 Sentence identity

本仓库不再使用：

```text
revision_id + section path + paragraph order + sentence order
```

自行推导一个平行 `SentenceUnit` identity。

优先保存上游已经返回的稳定引用：

```text
reading_document_id
normalized_document_identity
text_unit_id
text_locator
segmentation_version
```

Paper Reading Lab 可以保存便于人阅读的：

```text
section title
page
paragraph order
sentence order
```

但这些只是 display/navigation 信息，不取代上游 precise identity。

## PaperRevision 与 reading-mcp 的绑定

一个 `PaperRevision` 应显式记录当前 Source binding：

```text
paper_id
revision_id
source_kind
canonical_source
reading_provider = reading-mcp
reading_document_id
normalized_document_identity
reading_profile_version
limitations
```

一个 ReadingSession 必须绑定一个明确 `PaperRevision`。

如果 `reading-mcp` 因来源或 normalized identity 变化返回 stale：

```text
STALE_LOCATOR
或
STALE_CURSOR
```

Paper Reading Lab 必须停止当前 precise continuation，并显式执行 revision / locator reconcile。

禁止：

```text
复制旧句子文本
→ 搜索相似文本
→ 自动猜测“应该还是这句话”
→ 静默继续旧 Session
```

## no-lookahead 的工具层实现

首次顺序阅读不能先把整个小节读入 AI，再靠 Prompt 要求“假装不知道后文”。

推荐真实访问模型：

```text
ReadingSession.revealed_position = N
        ↓
reading-mcp 只提供当前允许的 Source Unit
        ↓
AI + 学习者解释 / 预测
        ↓
保存 ReadingStep
        ↓
显式 next
        ↓
cursor 前进到 N+1
```

核心原则：

> Future Source should not be supplied before reveal.

Prompt-level no-lookahead 是补充约束，不替代 Source access boundary。

## 最小可靠 Source Unit

“逐句”是默认体验，不是强制伪造句子的要求。

当 `reading-mcp` 只有 coarse Paragraph 级证据，或 Source 是：

- blockquote
- list item
- preformatted
- table
- equation
- figure
- pseudocode

应接受上游 source-preserving degradation，并使用当前最小可靠 Source Unit。

禁止为了维持“每一步必须是一句话”的外观而人工伪造精确定位。

## ReadingStep 建议引用

一个 ReadingStep 最小建议保存：

```text
session_id
step_index
revision_id
reading_document_id
text_unit_id
text_locator
segmentation_version
revealed_at
mode
```

以及 Derived：

```text
literal_meaning
relation_to_previous
observed_cues
current_problem_model
new_constraints
prediction
actual_next_ref
model_update
knowledge_gaps
```

Source 引用与 Derived 学习记录必须可以分开审计。

## 上下文读取规则

`get_context` 可以帮助理解当前句的允许前文，但首次 no-lookahead Session 必须限制在已经 revealed 的范围内。

不能为了方便直接请求包含未来正文的大窗口。

如果某一句必须依赖标题、当前段落已揭示前文、图表或前置定义才能理解，可以扩大到这些已授权上下文，但要在 checkpoint 中记录原因。

## Search 的边界

`search_document` 用于：

- Source 定位
- retrospective audit
- Knowledge gap 的显式补充任务

首次顺序阅读过程中，不能用全文 Search 搜索未来内容来帮助当前预测。

Search 命中也不能取代 canonical sequential reveal。

## 故障与降级

以下情况必须 fail closed 或显式降级：

- locator stale
- cursor stale
- revision identity 变化
- 句子覆盖不完整
- PDF 多栏解析错误
- 公式 / 图表缺失导致当前论证不可可靠理解
- Source 只能得到 coarse unit

允许：

```text
sentence → coarse paragraph
```

不允许：

```text
不可靠 source → AI 猜测补全
```

## 与 GitHub 的关系

GitHub 是控制面和长期可审计记录，不是 Source parser。

推荐：

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

Issue 记录：

- Paper identity
- Source / revision 状态
- 当前阅读目标
- Session links / summaries
- blockers
- actions

不要把完整逐句 transcript 全部塞进 Issue。

## 核心不变量

```text
reading-mcp 提供 Source identity；paper-reading-lab 不重复制造。
TextLocator 是引用，不是 AI 解释。
首次阅读的未来 Source 不提前提供。
stale 必须显式处理，不 fuzzy rebase。
逐句优先，但 Source evidence 优先于逐句外观。
Search 不得绕过 sequential reveal。
GitHub Issue 是控制面，不是 Source truth。
ReadingSession 保存学习状态，不修改上游 Source。
```
