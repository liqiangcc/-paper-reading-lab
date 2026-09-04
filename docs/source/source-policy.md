# Source Policy

## 目的

Paper Reading Lab 的学习记录只有在 Source 身份、版本、投影和视觉证据边界清楚时才可信。

本策略规定：

- 如何识别 `Paper` 与 `PaperRevision`；
- 什么可以作为 authoritative / raw source；
- normalized text、OCR、original source view 的身份；
- Source artifact 是否可以进入 Git；
- no-lookahead Session 如何避免未来正文泄露；
- Source 更新、stale locator 和迁移如何处理。

## Paper 与 PaperRevision

```text
Paper
= 长期论文对象

PaperRevision
= 某个明确发布 / 修订版本
```

同一 Paper 可能包括：

- conference version；
- journal version；
- technical report；
- author manuscript；
- extended version；
- later revision。

ReadingSession 必须绑定明确 `revision_id`，不能只保存标题或 URL。

## Authoritative / Raw Source

优先级按具体论文判断，常见候选：

1. 出版方或会议官方 PDF / HTML；
2. 作者或机构发布的明确版本；
3. 可验证的镜像；
4. 经人工核对的本地工作副本。

Source metadata 至少记录：

```text
paper_id
revision_id
source location
source provenance
acquired_at
content type
size
raw/content hash
known limitations
```

URL 可变化，因此 URL 本身不能承担完整 revision identity。

## ReadingSourceBinding

正式阅读还必须绑定 Source provider：

```text
provider = reading-mcp
reading_document_id
content_hash
normalized_document_hash
normalization_version
reading_profile_version
segmentation_version
```

`reading_document_id` 只表示 provider document identity；它不替代 `revision_id`。

## Normalized text 是 projection

PDF / HTML 经解析后得到的 normalized text 是供顺序阅读和 locator 使用的 projection。

它可以支持：

- section / paragraph / sentence enumeration；
- canonical order；
- exact TextLocator re-read；
- source-grounded quotation；
- current-step explanation。

但它不自动等价于原始发布视觉：

```text
normalized text
≠ original page layout
≠ Figure / Table spatial semantics
≠ Equation typesetting
```

## OCR 与生成式补全

OCR、转换文本和 AI 重建必须保留其身份：

```text
OCR output
= projection / extraction result

AI reconstruction
= generated interpretation
```

它们不得被标记为：

- raw source；
- authoritative wording；
- confirmed author text；
- precise replacement for missing source。

Source 缺失、截断或公式不可读时，默认 blocked；不能用 AI “补完整”后继续声称 source-first。

## Original source view

当 normalized text 无法证明视觉语义时，应使用 locator 绑定的 original source view。

典型场景：

- Figure；
- Table；
- Equation；
- Algorithm；
- 双栏排版；
- 脚注 / 页眉页脚；
- 图注与正文归属；
- parser 顺序疑问。

应记录：

```text
source locator
page identity
audit metadata
visual observation
AI interpretation（如有）
```

### 不变量

- original source view 必须绑定 current document / normalized identity；
- stale 时 fail closed；
- 不用 OCR 或 AI 重绘冒充原页；
- 看到整页不授权读取尚未 canonical reveal 的未来正文；
- 视觉观察与正文 Source Fact 分开。

## Named-section boundary Source

严格 no-lookahead Session 在正文 reveal 前可能需要 named-section boundary。

允许作为 boundary evidence 的来源：

- provider 的 structure-only canonical hierarchy；
- 预先验证且绑定当前 PaperRevision / normalized identity 的 boundary artifact；
- 不返回正文的结构 metadata。

不允许：

- 用全文 lexical search 返回未来正文 snippet；
- 从模型记忆猜测 page / section 边界；
- 使用另一 Revision 的页码静默套用；
- 先 reveal 越界正文再补 scope amendment。

## Source readiness

### source-ready

表示：

```text
Paper identity 稳定
+ PaperRevision 稳定
+ provenance 可追溯
+ raw/content identity 可核验
+ limitation durable
```

### reading-ready

在 source-ready 之上还需要：

```text
canonical order 可恢复
+ 当前 scope boundary 可执行
+ SourceUnit / locator 足够稳定
+ no-lookahead reveal 可执行
```

`source-ready ≠ reading-ready`。

## Source limitation

需要 durable 记录的 limitation 包括：

- 双栏顺序风险；
- OCR / parser 噪声；
- heading / body classification 不稳定；
- Formula / Table 丢失；
- page-level structure only；
- SentenceUnit 含多个 surface sentences；
- original source view 不可用；
- Source location 访问不稳定。

limitation 不能只存在于某个旧聊天里。

## Source 更新与 stale

当 provider normalization、segmentation 或 document identity 变化时：

```text
old locator
→ stale
→ precise continuation STOP
```

允许的处理：

1. 旧 Session 继续绑定旧 Source（若仍可访问）；
2. 创建新 Session 绑定新 identity；
3. 创建显式 migration / revision-comparison 记录。

禁止：

```text
old snippet
→ fuzzy search
→ silently choose similar new location
```

## 公开仓库版权边界

公开仓库默认不持久化完整受版权保护论文全文或大量连续正文。

优先保存：

- metadata；
- hashes；
- provenance；
- stable locator；
- 短而必要的 source excerpt；
- Derived learning artifact；
- finding / review evidence。

本地授权 Source Workspace 中存在 PDF 工作副本，不自动意味着可以提交到公开 Git 历史。

## Issue 中的 Source 引用

Primary Issue 可以引用：

```text
paper_id
revision_id
canonical source
reading_document_id
normalized identity
source limitations
```

但 Issue comment 中复制的原文不成为 canonical Source truth。正式 claim 仍应回到 provider locator。

## Source 与下游知识

```text
Source wording
→ immutable historical evidence

Reading interpretation
→ revisable Derived state

Validated downstream knowledge
→ target repository review result
```

下游知识被修正时，不能回写改变历史 Source 或旧 Session 当时看到的内容。

## 核心不变量

```text
Paper 与 Revision 分离。
Revision 与 provider document identity 分离。
Normalized text 和 OCR 保持 projection 身份。
AI reconstruction 永远不是 Source。
视觉 fidelity 通过 original source view 补充。
Named-section boundary 不能靠未来正文搜索获得。
Source limitation 必须 durable。
Stale precise locator fail closed。
公开仓库优先保存 locator，而不是全文。
```
