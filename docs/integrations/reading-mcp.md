# reading-mcp 集成

## 目的

`reading-mcp` 是 Paper Reading Lab 的首选 Source Adapter。

本文件只定义：

- 本仓库如何使用其 live capability；
- 哪些 identity 必须持久化；
- 如何执行 structure-only scope preflight、canonical reveal、exact re-read 和 original-source fidelity review；
- stale、degradation、tool failure 与 no-lookahead 的边界。

它不固定某个部署版本的 Tool 数量，也不把仓库文档当作 live runtime 的替代品。

## 职责分离

```text
reading-mcp
= document / structure / SourceUnit / TextLocator / source view

paper-reading-lab
= PaperRevision / Session / scope / learning / checkpoint
```

`reading-mcp` 返回的 document identity 不替代本仓库的 `paper_id` / `revision_id`。

## Capability reality

仓库文档中的接口描述只是 contract 期望。每个 fresh conversation 在真正执行前仍应确认当前 MCP capability 能实际调用。

```text
tool schema / release note / old conversation memory
≠ current successful invocation
```

若必需 Tool 不可调用：

```text
persist blocker / handoff
→ do not infer Source from memory
→ STOP
```

## Source binding

正式 ReadingSession 开始前至少记录：

```text
paper_id
revision_id
provider = reading-mcp
reading_document_id
content_hash
normalized_document_hash
normalization_version（如返回）
reading_profile_version（如返回）
segmentation_version
media_type
source location / provenance
known limitations
```

### Identity 层次

```text
PaperRevision
→ 出版 / 版本身份

reading_document_id
→ provider 中的文档身份

content_hash
→ 原始或绑定内容身份

normalized_document_hash
→ 当前 normalized projection 身份

segmentation_version
→ 当前 SourceUnit 边界规则身份
```

旧 Session 必须继续绑定其原 identity。新 normalization 或 segmentation 不能静默重写历史 checkpoint。

## 打开 Source

典型流程：

```text
approved source location
→ open_document
→ verify returned identity
→ compare with expected PaperRevision
→ persist ReadingSourceBinding
```

只有以下条件满足时才进入 `reading-ready`：

- PaperRevision identity 已确认；
- Source 可重复访问；
- 当前 scope 的 structure / order 可恢复；
- locator 可以精确回读；
- 已知 limitation durable；
- no-lookahead reveal 可执行。

## Structure-only named-section preflight

严格 section-bounded Session 在正文 reveal 前需要知道：

```text
allowed named section
+
next sibling / stop boundary
```

优先使用 `get_document_structure` 的 canonical named hierarchy，要求返回：

- section id；
- title；
- parent / sibling relation；
- source order / body order；
- source location metadata；
- 不返回正文内容。

典型 gate：

```text
resolve section://1-introduction
→ resolve next sibling section://2-...
→ persist current_scope_boundary
→ only then reveal first allowed SourceUnit
```

不得使用会返回未来正文 snippet 的全文 lexical search 作为 clean no-lookahead boundary preflight。

如果 named structure 不可用且没有预验证 boundary artifact：

```text
planned section scope
→ cannot become executable boundary safely
→ fail closed / block Session start
```

## Canonical sequential reveal

普通 sentence-first ReadingStep 默认：

```text
get_text_units(
  document_id,
  section_id,
  requested_kind = sentence,
  direction = forward,
  coverage_policy = preserve_source,
  max_items = 1,
  anchor_locator = latest precise locator
)
```

### `coverage_policy = preserve_source`

用于保留 provider 的真实边界和 degradation：

- Sentence 可用时返回 Sentence；
- 只能可靠提供 Paragraph 时保留 Paragraph；
- structural / caption / code / unknown classification 不被本仓库伪造为正文 Sentence。

### Exactly-one 的语义

`max_items = 1` 限制 canonical unit 数量，不保证该 unit 只有一个表面句号。一个 provider-defined SentenceUnit 可能因当前 segmentation 包含多个 surface sentences；本仓库必须保留 actual unit identity，并把它作为 finding，而不是私自拆成新 identity。

若当前单元是 structural / non-prose：

- 仍记录当前 canonical unit；
- 是否继续到下一单元取决于 Session scope / durable next_action；
- 不得为了找到“更有内容”的正文一次批量读取后文。

## Precise exact re-read

对允许 reveal 的 SourceUnit，使用：

```text
read_document(
  document_id,
  target_locator
)
```

只传当前 document identity 和 exact target locator；不通过旧 snippet 做相似搜索。

成功条件：

- returned locator identity 与目标一致；
- returned content 对应当前 allowed unit；
- 没有 fuzzy rebase；
- 没有额外 reveal 第二个 unit。

## Stale 与 fail closed

当 provider 返回：

```text
STALE_LOCATOR
STALE_CURSOR
identity mismatch
```

必须：

```text
STOP precise continuation
→ preserve old checkpoint
→ record current provider identity
→ decide explicit migration / new Session
```

禁止：

```text
old snippet
→ search_document
→ choose most similar result
→ silently continue old Session
```

## `search_document` 边界

全文搜索会返回匹配内容，因此在 clean first-pass Session 中可能泄露未来 Source。

允许场景包括：

- 已显式进入 retrospective / open-source mode；
- 当前 KnowledgeGap 调查允许离开顺序阅读，并记录 contamination / mode change；
- 搜索范围本身已经全部 reveal；
- 非正文 metadata 调查且 Tool contract 保证不返回未来正文。

不能用于：

- 预测下一句；
- named-section no-lookahead preflight；
- stale locator fuzzy recovery；
- 绕过 scope gate。

## Original source view

当当前已允许 Source 涉及：

- Figure；
- Table；
- Equation；
- Algorithm；
- 多栏排版；
- 脚注 / 页眉 / 图注归属；
- parser fidelity ambiguity；

可以使用：

```text
get_source_view(
  document_id,
  target_locator,
  representation = original
)
```

期望行为：

- locator 与 current normalized identity 精确绑定；
- 返回 original source page 的视觉表示和 audit metadata；
- 不使用 OCR 或生成式重建替代原页；
- stale 时 fail closed；
- 不 fuzzy rebase。

### 视觉边界

必须区分：

```text
Text Source Fact
vs
Original-page visual observation
vs
AI visual interpretation
```

看到整页只授权检查当前允许对象；页面上尚未 canonical reveal 的未来正文不能进入 clean first-pass explanation / prediction。

## Context 工具边界

`get_context` 可以用于显式请求的邻居、容器或结构上下文，但其调用必须受 Session mode、scope 和 no-lookahead 约束。

默认 ReadingStep 不因为“上下文可能有帮助”而读取未来 neighbor。容器 / structural context 只有在 Tool contract 不返回越界正文且 current scope 允许时使用。

## Source fidelity 与 segmentation finding

需要分别记录：

```text
Raw source fidelity
Normalized text fidelity
Canonical order
SourceUnit boundary quality
Content classification
Visual fidelity
```

一个 prose locator exact re-read 成功，不代表：

- 整篇双栏顺序全部正确；
- Figure / Table 已被文本完整表达；
- 所有 sentence boundary 都正确；
- future page / section ownership 已被验证。

finding 应绑定具体 document identity、locator、scope 和 provider version。

## Tool failure 与 retry

安全 retry 只允许在以下条件下进行：

- 不改变 Source scope；
- 不获取第二个 SourceUnit；
- 不更换 Revision / normalized identity；
- 不使用 Web / model memory 代替；
- retry 结果可审计。

若 invocation path、serialization 或 binding 异常无法安全确认：

```text
persist blocker
→ keep current revealed_position
→ STOP
```

后续 fresh invocation 成功不能删除此前 transient finding，只能追加复现结论。

## 典型 source-first action

```text
recover durable Session state
→ verify current reading-mcp capability
→ verify PaperRevision / document identity
→ scope gate
→ get_text_units(max_items=1)
→ exact read_document(locator)
→ optional get_source_view(current locator)
→ explain current unit
→ persist locator / stop boundary when required
→ STOP
```

## 本仓库不做的事情

- 自建 PDF parser；
- 自建与 provider 平行的 section / sentence identity；
- 把 OCR / AI 重建内容标记为 original Source；
- 通过全文搜索偷看未来正文；
- 在 stale 后自动迁移旧 Session；
- 仅凭 tools/list 文字就声称能力已验证；
- 把 current runtime Tool 数量写成长期领域真相。

## 核心不变量

```text
PaperRevision 与 provider document identity 显式绑定。
Named-section scope 优先通过 structure-only preflight 建立。
Future Source 不为 boundary discovery 提前泄露。
Canonical unit identity 优先于本地表面句号判断。
Exact locator re-read 优先于 snippet search。
Stale / identity conflict fail closed。
Original source view 补充视觉 fidelity，不扩大 no-lookahead 范围。
Current capability 以实际 invocation 为准。
```
