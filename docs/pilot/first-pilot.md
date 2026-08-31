# 首个逐句阅读 Pilot：Kafka 2011

## 目的

首个 Pilot 不追求“读完一篇经典论文”，而是验证 Paper Reading Lab 最核心的学习机制是否真实可用。

要证明的是：

```text
稳定 PaperRevision
→ Codex Source acquisition
→ reading-mcp 稳定 SourceUnit
→ no-lookahead 逐项 reveal
→ AI 一层一层解释
→ ReadingStep / checkpoint 可恢复
→ Prediction 先于下一 SourceUnit
→ 新 Source 到来后更新判断
→ 第二遍 Recall / Reconstruction
```

如果这条链没有跑通，不扩展论文数量。

## 已选择论文

首个 Pilot 正式绑定：

**Jay Kreps, Neha Narkhede, Jun Rao — Kafka: a Distributed Messaging System for Log Processing**

发表信息：

```text
Year: 2011
Venue: NetDB'11
Date: June 12, 2011
Location: Athens, Greece
```

仓库 machine identity：

```text
paper_id = kafka-2011-distributed-messaging
revision_id = kafka-2011-netdb11
```

Primary Paper Issue：

```text
#2 — [Paper] Kafka 2011 — 首个逐句阅读 Pilot
```

## 为什么选择 Kafka 2011

这篇论文非常适合作为第一篇，而不仅仅因为 Kafka 经典：

- 原始论文只有约 7 页，适合快速跑完整机制闭环；
- 问题背景、设计目标、机制和实验验证之间关系清晰；
- 能训练分布式系统设计中常见的“需求压力 → 现有方案边界 → 设计选择 → trade-off”思考方式；
- 现有 `classic-papers-system-design` 已经对同一论文完成严格 Source Gate、原 PDF 核对和多轮独立 review；
- Figure 1–5、Algorithm 1 和 Section 1–6 均已有稳定来源记录；
- 原 PDF 是双栏布局，真实暴露 `reading-mcp` 的 PDF 阅读顺序与 fidelity 问题，非常适合验证基础设施；
- 后续可以自然扩展到 Kafka、distributed log、messaging、storage、stream processing 等学习路径。

## 重要的 no-lookahead 边界

`classic-papers-system-design` 已经存在 Kafka 2011 的完整分析资产，但**首个 ReadingSession 不允许读取这些分析内容**。

首次学习时禁止使用：

```text
papers/kafka/kafka-2011-distributed-messaging/01-facts.md
...
papers/kafka/kafka-2011-distributed-messaging/09-knowledge-card.md
reviews/kafka/... 的既有结论
```

原因：

```text
已有知识资产
≠
首次 Source-first 阅读时允许提前知道的上下文
```

这些资产只能在首次 ReadingSession 完成后，用于 retrospective comparison、export review 或独立质量检查。

## 已验证的 Source 背景

现有 `classic-papers-system-design` Source 记录：

```text
sources/kafka/kafka-2011-distributed-messaging/paper.pdf
sources/kafka/kafka-2011-distributed-messaging/paper.md
sources/kafka/kafka-2011-distributed-messaging/figures/
sources/kafka/kafka-2011-distributed-messaging/conversion-notes.md
```

已知事实包括：

- 原 PDF 为 7 页；
- Abstract、Section 1–6、References 可定位；
- Figure 1–5 已核对；
- Algorithm 1 位于原 PDF p.4；
- 原论文没有独立复杂数学公式环境；
- 双栏 PDF 在纯文本页边界可能出现列顺序跳转；
- Algorithm 1 的 boxed layout 在纯文本转换中会丢失视觉版式。

这些 Source-quality 信息可以用于验证读取基础设施，但不能把论文后续技术内容倒灌到当前阅读步骤。

## Source Acquisition：Issue 驱动 + Codex 执行

首个 Pilot 采用：

```text
Primary Paper Issue
        ↓
Codex Source acquisition
        ↓
reading-mcp Source Workspace
        ↓
reading-mcp binding
        ↓
ReadingSession
```

Codex 读取 Issue #2 后负责：

```text
验证 paper / revision identity
→ 获取目标 PDF
→ 放入 reading-mcp 已授权 Source Workspace
→ 校验 PDF 非空、格式有效、页数与既有 Source 记录一致
→ 计算 SHA-256
→ 创建 source metadata
→ 交给 reading-mcp 打开
→ 回写 document binding
```

推荐工作区相对结构：

```text
papers/
└── kafka-2011-distributed-messaging/
    └── kafka-2011-netdb11/
        ├── paper.pdf
        └── source.json
```

该目录属于 reading-mcp 的受控 Source Workspace，不意味着 PDF 自动进入公开 `paper-reading-lab` Git 历史。

`source.json` 至少记录：

```text
paper_id
revision_id
source_url
acquired_at
sha256
size
content_type
source_provenance
```

## Reading provider

默认 Source Adapter：

```text
provider = reading-mcp
```

推荐真实调用链：

```text
open_document(local paper.pdf)
        ↓
读取 reading_profile/v1
        ↓
get_document_structure
        ↓
定位 Abstract / Section 1
        ↓
get_text_units(
  requested_kind = sentence,
  coverage_policy = preserve_source
)
        ↓
TextLocator + TextUnitCursor
        ↓
read_document(target_locator)
        ↓
逐项 reveal
```

Paper Reading Lab 不重新解析 PDF、不重新生成平行 Sentence identity。

## Pilot Gate 0：Source binding

开始逐句阅读前必须记录：

```text
paper_id
revision_id
source acquisition provenance
source SHA-256
reading_provider
reading_document_id
raw/content identity
normalized_document_identity
reading_profile_version
segmentation_version
Source limitations
```

并确认：

- 当前读取的 bytes 与目标 Kafka 2011 revision 一致；
- PDF 有效且页数合理；
- Source 不静默切换；
- reading-mcp binding 可重复恢复。

如果不能满足，先停在 Source workflow。

## Pilot Gate 1：SourceUnit coverage

Kafka 2011 是双栏 PDF，因此这一步是首个 Pilot 的真实门禁，而不是形式检查。

至少验证：

- Abstract → Section 1 的 canonical 阅读顺序；
- 双栏顺序没有明显串列；
- 页眉、页脚没有被当成正文；
- Sentence 边界基本可靠；
- 每个 precise SourceUnit 可以通过 `TextLocator → read_document` 精确回读；
- 如果只能可靠降级成 coarse Paragraph，保留 degradation，不人工制造假 Sentence；
- 任何 parser 顺序异常都必须作为 finding 留下。

`reading-mcp` Issue #53 的 Original PDF View 是重要 P1 能力，但当前不是首轮纯文本 Introduction Pilot 的硬 blocker。需要视觉核对时应显式记录 limitation，不能假装 normalized text 已证明原页面 fidelity。

## 首轮阅读范围

第一轮先严格限定：

```text
Abstract
→ Section 1. Introduction
```

目的不是一次读完整篇，而是先把：

```text
Source acquisition
→ Source binding
→ sequential reading
→ checkpoint
→ training
```

跑通。

在当前范围完成前，不提前读取 Section 2+ 来帮助解释或预测。

## Pilot Gate 2：Primary Paper Issue

Kafka 的 Primary Paper Issue 是：

```text
Issue #2
```

Issue 长期关联：

```text
paper_id
revision_id
Source acquisition
reading-mcp binding
当前阅读 scope
当前 phase
Session summaries
blockers
knowledge gaps
next action
```

ReadingSession 不默认各自创建 Issue。

关系保持：

```text
1 Paper
↕
1 Primary Issue

1 Paper
↕
N ReadingSessions
```

## Pilot Session A：Learning

目标：验证“逐项 + 一层一层解释”。

对每个新 SourceUnit：

```text
1. reading-mcp 只提供当前允许 reveal 的 unit
2. read_document 返回当前 canonical 原文
3. 解释字面含义
4. 解释与已经揭示前文的关系
5. 识别新增 fact / problem / constraint / decision / evidence
6. 更新 current problem model
7. 形成 ReadingStep / checkpoint
8. 停下
```

不要每一步都强制 Prediction。

先确认基础阅读体验自然。

### AI 的输出边界

AI 不能：

- 提前总结整篇 Kafka 论文；
- 使用 Section 2+ 的内容解释当前 Abstract / Introduction；
- 读取已有 01–09 分析后再假装“根据当前句推出来”；
- 把现代 Kafka 能力倒灌到 2011 论文；
- 把 reviewer inference 说成作者当时明确写出的 reasoning。

已有通用背景知识可以使用，但必须和“当前 Source 已经建立的事实”分开。

## Pilot Session B：Prediction

第二遍或自然 checkpoint，在揭示下一 SourceUnit 前记录：

```text
当前最合理的下一步问题是什么？
有哪些候选方向？
哪个已知约束最可能推动作者继续？
```

然后才请求 `reading-mcp` 提供下一 unit。

记录：

```text
prediction
based_on_source_unit_ref
actual_next_ref
match / mismatch
missing cue / misconception
model update
```

重点不是预测命中率，而是发现当前问题模型在哪里不足。

原始 prediction 不得在看到后文后覆盖美化。

## Pilot Session C：Recall

间隔后，只提供有限 cue 或已读范围定位。

测试能否主动恢复：

```text
Kafka 2011 开篇在解决什么问题背景？
作者为何认为需要新的 messaging system？
哪些 workload / operational requirements 开始推动设计？
当前 Source 已经建立了哪些显式 reasoning links？
```

如果需要提示，记录提示层级，不把提示后的回答当成 spontaneous recall。

## Pilot Session D：Reconstruction

不逐句查看 Abstract / Introduction，尝试重建其显式论证结构：

```text
Problem context
→ Workload / requirement pressure
→ Existing-system limitation
→ Design goals
→ Proposed system direction
→ Claimed benefits / evidence boundary
```

只有重建完成后再回 Source 校正。

不能把 Section 2+ 的实现细节补进 Introduction reconstruction。

## 可选 Session E：Transfer

前四步跑通后，再给一个不直接提 Kafka 的新问题，例如：

```text
需要设计一个持续产生大量事件数据、既供在线消费又供离线处理的数据系统。
现有消息系统在哪些约束下可能开始不合适？
```

检查能否迁移出：

- workload-first 分析；
- throughput / persistence / consumer 模型约束；
- producer、storage、consumer 职责分离；
- 从需求压力推导设计选择。

Transfer 只能称为学习迁移，不反写成 Kafka 论文新增事实。

## ReadingStep 要记录什么

只保存可复用结构，不保存完整聊天 transcript。

Source reference：

```text
session_id
step_index
revision_id
reading_document_id
text_unit_id
text_locator
segmentation_version
revealed_at
```

Derived：

```text
literal_meaning
relation_to_previous
observed_cues
current_problem_model
new_constraints
explicit_reasoning_links
prediction
actual_next_ref
model_update
knowledge_gaps
```

## Pilot 成功标准

第一轮至少证明：

1. Codex 能依据 Paper Issue 稳定准备目标 Source。
2. 同一 SourceUnit 可以跨会话通过 reading-mcp 稳定重新定位。
3. 首次阅读没有未来 Source 倒灌。
4. no-lookahead 不只是 Prompt，而是未来 unit 尚未提供给当前步骤。
5. checkpoint 足以在新会话继续。
6. Prediction 确实发生在 reveal 前，而不是事后解释。
7. AI 输出能够保持“小步”，不会自动展开后续 Kafka 机制。
8. 第二遍学习能从“看懂”转向“主动重建”。
9. 至少发现一个具体 reasoning gap，而不只是记录“这句不会”。
10. 双栏 PDF 的顺序风险被真实验证，而不是被假定正确。
11. stale locator / revision change 会 fail closed，而不是 fuzzy rebase。
12. Session completed 没有被错误解释成 Paper done。

## Pilot 失败也要保留的 finding

例如：

- Sentence 粒度过细，破坏自然理解；
- Abstract 更适合 reveal group；
- 双栏 PDF 出现阅读顺序错误；
- 页边界污染影响 sequential reading；
- checkpoint 太重，维护成本高；
- reading-mcp 某些区域只能 coarse paragraph；
- no-lookahead 被已有 Kafka 知识间接破坏；
- AI 过度解释作者意图；
- Primary Issue summary 过重或过轻；
- Source Workspace / Codex acquisition 边界不清楚。

这些 finding 应推动修改机制，而不是为了“Pilot PASS”隐藏问题。

## Raft 的状态

Raft 2014 仍然是正式 Paper case，但不再作为首个 Pilot。

```text
Raft Paper Issue #1
= 保留
= 后续阅读对象
≠ 当前 first pilot
```

不能把 Issue #1 直接改造成 Kafka，因为 Primary Issue identity 必须绑定 Paper。

## Pilot 完成后再决定什么

首个 Pilot 完成后再决定：

- ReadingStep / Session artifact 的正式 schema；
- Validator 脚本；
- 是否需要自动 checkpoint writer；
- Issue Label taxonomy；
- `classic-papers-system-design` export protocol；
- Source Workspace 自动治理；
- Original Source View 与 #53 的实际优先级；
- 是否需要学习者薄弱 reasoning-link 统计。

以下事项已经确定：

```text
Issue-driven = yes
1 Paper → 1 Primary Issue
Codex = Source acquisition executor
reading-mcp = 首选 Source Adapter
Source precise identity 不在 paper-reading-lab 重复实现
首次学习不读取既有下游分析资产
```

## 下一步

```text
Issue #2
→ Codex 获取 Kafka 2011 Source
→ 写入 reading-mcp Source Workspace
→ 固定 PaperRevision binding
→ 枚举 Abstract / Introduction SourceUnit
→ 人工抽查双栏 coverage
→ 开始 Session A 第一条 SourceUnit
```
