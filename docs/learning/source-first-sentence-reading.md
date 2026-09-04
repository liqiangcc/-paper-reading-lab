# Source-First 逐句阅读协议

## 目的

本协议用于训练：

> 跟着论文原文，在有限信息下逐步建立、检验和修正问题模型。

它不是知道全文结论后的事后总结，也不是用百科知识替代当前论文阅读。

默认粒度：

```text
一篇论文
→ 一个有界 ReadingSession
→ 一个 named section / paragraph range / sentence range
→ 一个 canonical SourceUnit
→ 一次只推进一个解释层
```

## 与其他文档的关系

```text
本协议
→ 决定允许读取什么、何时允许读取

incremental-explanation-profile.md
→ 决定取得当前 SourceUnit 后怎样解释和呈现

reading-sessions.md
→ 决定 Session mode、scope、checkpoint 和 learning artifact

reading-mcp.md
→ 决定 canonical structure / SourceUnit / TextLocator / source view
```

Explanation Profile 不能扩大本协议规定的 Source 可见范围。

## 前置 Gate

任何正文 reveal 前必须已经具备：

```text
stable PaperRevision
+
reading-mcp Source binding
+
Session mode / lookahead policy
+
planned_scope
+
current_scope_boundary
```

每次新 canonical reveal 前都要检查：

```text
next unit inside current_scope_boundary?
├── yes → reveal allowed
└── no  → STOP before reveal
          → durable scope amendment required
```

不得先读越界正文，再事后补 scope。

## 核心规则：禁止未来上下文倒灌

首次顺序阅读处于位置 `N` 时，只允许使用：

```text
已揭示 SourceUnit 1..N-1
+
当前 SourceUnit N
+
Session 明确允许的既有背景知识
```

禁止使用：

```text
SourceUnit N+1..end
```

包括：

- 用后文结论解释作者“此时一定在想什么”；
- 因为知道最终机制而强化当前句意图；
- 提前透露下一问题、设计或实验结果；
- 用全文摘要给当前 prediction 打分；
- 用下游分析资产补当前 Source；
- 用 Web 或模型记忆绕过 bound Source provider；
- 用整页视觉中尚未 canonical reveal 的未来正文帮助当前解释。

## 为什么必须 no-lookahead

真实研究与系统设计是增量的：

```text
有限信息
→ 建立当前模型
→ 形成候选下一步
→ 新信息到来
→ 更新模型
```

若先看到结论再回看前文，很容易产生：

```text
结局已知
→ 前文看起来理所当然
```

这会隐藏当时存在的 alternatives、uncertainty 和 reasoning gap。

## Canonical SourceUnit

默认由 `reading-mcp.get_text_units` 按 provider canonical order 返回。

普通 sentence-first Step 通常使用：

```text
requested_kind = sentence
coverage_policy = preserve_source
max_items = 1
```

### Provider identity 优先

一个 canonical SentenceUnit 可能：

- 对应一个 surface sentence；
- 因 segmentation 包含多个 surface sentences；
- 因公式 / PDF extraction 退化为 fragment；
- 只能可靠提供 Paragraph；
- 被标记为 structural / caption / code / unknown。

本仓库必须保留 actual unit identity，不根据标点私自生成平行 Sentence identity。

## Exactly-one 与最小有用输入

默认：

```text
一次 ReadingStep
→ exactly one canonical SourceUnit
```

但句子不是绝对语义边界。以下情况可以使用显式 reveal group：

- 公式把一句自然语言拆开；
- 引文或脚注导致句法不完整；
- 一个定义必须与紧邻 unit 联合才构成最小可解释输入；
- PDF 转换造成错误断句。

规则：

```text
最小有用输入
>
机械表面句号
```

任何 reveal group 都必须：

- canonical 顺序连续；
- 记录所有成员 SourceUnitRef；
- 不跨 `current_scope_boundary`；
- 不借机读取下一个独立推理单元；
- 由 durable next_action 或当前 protocol 明确授权。

若当前 scope 只授权一个 canonical unit，则不能为了得到“更完整”内容自行扩大。

## Precise re-read

当前允许 SourceUnit 应通过 precise `TextLocator` exact re-read。

```text
get_text_units
→ current SourceUnitRef
→ read_document(document_id, target_locator)
```

stale、identity mismatch 或 exact-read failure 时 fail closed；不通过旧 snippet + search 做 fuzzy rebase。

## 一个 SourceUnit 的默认学习层次

### 1. 字面含义

回答：

> 当前 Source 直接说了什么？

只做必要释义，不提前扩展完整背景。

### 2. 与已揭示前文的关系

回答：

> 为什么它接在这里？它承接、澄清、转折、限制或回答了什么？

常见关系：

```text
continue
clarify
contrast
cause
constraint
example
counterexample
problem
assumption
decision
consequence
evidence
boundary
transition
recap / bridge
```

### 3. 当前真实认知增量

回答：

> 相对于此前模型，当前 unit 新增或修正了什么？

可能是：

- 新事实；
- 假设；
- 限制；
- 目标；
- failure mode；
- design choice；
- mechanism；
- evidence；
- boundary。

### 4. 为什么现在需要这一步

当 Source 足够支持时回答：

> 如果只知道此前内容，哪个压力、缺口或开放问题推动作者在这里加入当前信息？

当前文本不足以证明作者意图时，使用“可能 / 更像 / 从结构上看”，而不是断言作者心理。

### 5. 当前状态更新

维护：

```text
Known facts
Current problem
Constraints
Explicit reasoning links
Open questions
```

只更新受当前 Source 影响的部分，不在每一步重复整节 summary。

### 6. 停止边界

记录：

```text
current SourceUnitRef / TextLocator
revealed_position
stop_boundary
next_action
```

当前解释结束后停止，不自动读取下一独立 SourceUnit。

## Source Fact、Derived Interpretation、Unknown

### Source Fact

当前或此前已 reveal Source 直接支持。

### Derived Interpretation

基于已揭示 Source 的有限推论，可在后续修正。

### Unknown

当前 Source 尚未回答。

所有显式 reasoning arrow 必须能追溯到已揭示 Source，或保持 Derived 身份。

## 前置知识规则

No-lookahead 不等于禁止所有已有知识。

允许使用学习者已有的通用背景，例如：

- 操作系统；
- 数据库；
- 网络；
- 数学基础。

但必须区分：

```text
Source 当前证明了什么
vs
我因为外部背景还知道什么
```

来自同一论文未来部分的知识，在 clean first-pass Session 中不可使用。

现代实现与历史论文不同时，应明确版本边界，不能倒灌覆盖历史 Source 语义。

## Figure / Table / Equation

当前允许 Source 涉及视觉对象时，可使用 original source view。

必须区分：

```text
正文 Source Fact
original-page visual observation
AI visual interpretation
```

看到整页不授权使用尚未 canonical reveal 的未来正文。

## Prediction

Prediction 是独立的时序证据。

正式流程：

```text
基于 revealed position 形成 prediction
→ durable persist
→ actual next Source reveal
→ comparison
→ missing cue / misconception
→ model update
```

Prediction 不要求命中作者，但原 prediction 不得事后修改。

不是每个普通 Learning Step 都必须自动做 Prediction；是否执行由当前 Session mode / durable next_action 决定。

## Recall / Reconstruction / Transfer

### Recall

只看 cue 或问题，主动恢复关键连接。展示答案后不能继续算无提示 Recall。

### Reconstruction

按明确提示级别重建：

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

把同一思考结构应用到真正的新问题，不是原题换词。

这些 mode 仍必须保持 Source / Derived 边界，但不等同于首次顺序 reveal。

## Retrospective

读过后文后可以回看早期句子，但必须显式标记 retrospective。

可以分析：

- 早期伏笔后来如何展开；
- 术语后文如何精确定义；
- 早期约束最终影响什么机制。

同时必须说明：

> 这是知道后文后的回顾，不是首次位置当时可确定的结论。

## AI 行为

AI 应：

- 先恢复 durable Session state；
- reveal 前执行 scope gate；
- 一次只取得当前授权 SourceUnit / reveal group；
- 保留 provider actual kind / identity；
- exact re-read 当前 locator；
- 区分 Source Fact / Derived / Unknown；
- 明确 current cognitive increment；
- 在自然学习边界停止；
- Tool / identity / scope failure 时 fail closed。

AI 不应：

- 因为知道整篇论文而提前剧透；
- 把 prediction 或 reconstruction 写成作者事实；
- 用百科知识替代当前 Source；
- 一次生成整节 summary 绕过逐句学习；
- 用全文 search 寻找下一句；
- 静默扩 scope；
- 把完整 chain-of-thought 当作 learning artifact。

## 核心不变量

```text
Scope 在 reveal 前检查。
上下文只能沿 revealed_position 增长。
当前解释不能依赖未来 Source。
Provider canonical identity 优先。
Precise locator failure fail closed。
事实、有限推论和未知分开。
Prediction 与 Source fact 分开。
首次阅读与 Retrospective 分开。
一次只推进授权的最小输入。
每步以明确 stop boundary 结束。
最终训练的是可迁移的思考结构，而不是 AI 文本记忆。
```
