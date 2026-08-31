# 首个逐句阅读 Pilot：Raft 2014 Introduction

## 目的

首个 Pilot 不追求“读完一篇经典论文”，而是验证 Paper Reading Lab 最核心的学习机制是否真实可用。

要证明的是：

```text
稳定 PaperRevision
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

首个 Pilot 绑定：

**Diego Ongaro, John Ousterhout — In Search of an Understandable Consensus Algorithm**

正式发表版本：2014 USENIX Annual Technical Conference（USENIX ATC 14）。

仓库 machine identity：

```text
paper_id = raft-2014-understandable-consensus
revision_id = raft-2014-usenix-atc14
```

首轮只读：

```text
Section 1 — Introduction
```

不提前进入后续 Raft design sections。

## 为什么选 Raft Introduction

它适合作为机制 Pilot，而不仅仅因为论文经典：

- 有稳定公开的 USENIX Source
- 论文版本身份容易明确
- Introduction 以自然语言论证为主
- 数学公式和复杂图表不是主要障碍
- 作者会逐步建立 consensus 的问题背景、Paxos 的现实困难、understandability 目标以及 Raft 的设计方向
- 很适合训练“问题 → 约束 / 痛点 → 设计目标 → 方法方向”的 reasoning structure
- `classic-papers-system-design` 已有 Raft 主题，后续可以验证 export 边界

## Source

首选正式 Source：

```text
USENIX presentation page:
https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro

USENIX paper PDF:
https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf
```

可以把 `raft.github.io/raft.pdf` 的 extended version 作为后续版本比较来源，但首个 no-lookahead Pilot **不混用** extended version。

原因：

```text
USENIX published revision
≠
extended revision
```

首次 Session 必须始终绑定 `raft-2014-usenix-atc14`。

## Reading provider

首个 Pilot 的默认 Source Adapter：

```text
provider = reading-mcp
```

推荐真实调用链：

```text
open_document(USENIX PDF)
        ↓
读取 reading_profile/v1
        ↓
get_document_structure
        ↓
定位 Section 1 — Introduction
        ↓
get_text_units(
  requested_kind = sentence,
  coverage_policy = preserve_source,
  anchored to Introduction
)
        ↓
TextLocator + TextUnitCursor
        ↓
逐项 reveal
```

不在 Paper Reading Lab 内重新进行 PDF 分句。

## Pilot Gate 0：Source binding

开始逐句阅读前必须记录：

```text
paper_id
revision_id
canonical source
reading_provider
reading_document_id
normalized_document_identity
reading_profile_version
segmentation_version
Source limitations
```

并确认：

- USENIX Source 可重复访问
- 当前读取的是正式 ATC 14 revision
- 不静默切换到 extended version
- `Introduction` locator 稳定

如果不能满足，先停在 Source workflow。

## Pilot Gate 1：SourceUnit coverage

通过 `reading-mcp` 枚举 `Introduction` 范围内的 Source units。

人工抽查：

- canonical 顺序正确
- 没有把页眉页脚混入正文
- 多栏 PDF 没有串行错误
- Sentence 边界基本可靠
- 每个 precise unit 可以通过 `TextLocator` 重新读取
- 如果某处只能可靠降级成 coarse Paragraph，保留 degradation，不人工制造假 Sentence

不要求整个论文一次切完。

## Pilot Gate 2：Primary Paper Issue

创建 1 个 Primary Paper Issue，长期作为 Raft case 的操作入口。

Issue 至少关联：

```text
paper_id
revision_id
USENIX Source
reading-mcp binding
Pilot scope = Section 1 Introduction
当前 phase
Session summaries
blockers
next action
```

ReadingSession 不默认各自创建 Issue。

## Pilot Session A：Learning

目标：验证“逐项 + 一层一层解释”。

对每个新 SourceUnit：

```text
1. reading-mcp 只提供当前允许 reveal 的 unit
2. 解释字面含义
3. 解释与已揭示前文的关系
4. 识别新增 fact / problem / constraint / decision / evidence
5. 更新 current problem model
6. 形成 ReadingStep / checkpoint
7. 停下
```

不要每一步都强制 Prediction。

先确认基础阅读体验自然。

### AI 的输出边界

AI 不能：

- 提前总结整个 Introduction
- 用 Section 2+ 的内容解释当前句
- 因为“知道 Raft”就把后续正式设计倒灌进当前解释
- 把作者未写出的替代方案说成作者实际考虑过

已有通用背景知识可以使用，但必须和“当前 Source 已经建立的事实”分开。

## Pilot Session B：Prediction

第二遍或适合的自然 checkpoint，在揭示下一 SourceUnit 前记录：

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
missing cue
model update
```

重点不是命中率，而是找到自己的思维连接在哪断掉。

## Pilot Session C：Recall

间隔后，只提供部分 cue 或已读范围定位。

测试能否恢复：

```text
作者当前首先在解决什么问题？
为什么已有方法让作者认为需要新的设计？
understandability 为什么成为一个设计目标？
已经出现的 reasoning links 是什么？
```

如果需要提示，记录提示层级，不把提示后的回答当成 spontaneous recall。

## Pilot Session D：Reconstruction

不逐句查看 Introduction，尝试重建其显式论证结构：

```text
Problem context
→ Existing difficulty / limitation
→ Design goal
→ Proposed direction
→ Claimed benefit / evidence boundary
```

只有重建完成后再回 Source 校正。

不能把后续 Section 的细节补进 Introduction reconstruction。

## 可选 Session E：Transfer

Pilot 前四步跑通后，再给一个不直接提 Raft 的新系统问题，例如：

```text
某个关键分布式机制功能正确，但工程团队普遍难以理解、实现和验证。
应该如何把“可理解性”变成设计约束？
```

检查能否迁移出：

- 分解问题
- 减少需要同时考虑的状态
- 明确子问题边界
- 把可理解性作为可验证设计目标

Transfer 只能称为学习迁移，不反向写成 Raft paper 的新增事实。

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

1. 同一 SourceUnit 可以跨会话通过 `reading-mcp` 稳定重新定位。
2. 首次阅读没有未来 Source 倒灌。
3. no-lookahead 不只是 Prompt，而是未来 unit 尚未提供给当前步骤。
4. checkpoint 足以在新会话继续。
5. Prediction 确实发生在 reveal 前，而不是事后解释。
6. AI 输出能够保持“小步”，不会自动展开后续 Raft 设计。
7. 第二遍学习能从“看懂”转向“主动重建”。
8. 至少发现一个具体 reasoning gap，而不只是记录“这句不会”。
9. stale locator / revision change 会 fail closed，而不是 fuzzy rebase。
10. Session completed 没有被错误解释成 Paper done。

## Pilot 失败也要保留的 finding

例如：

- Sentence 粒度过细，破坏自然理解
- 每句都预测导致节奏很差
- checkpoint 太重，维护成本高
- Introduction 的论证粒度更适合 reveal group
- reading-mcp 某些 PDF unit 只能 coarse paragraph
- no-lookahead 仍被其他上下文间接破坏
- AI 过度解释作者意图
- 已有 Raft 背景知识和当前 Source 事实边界难区分
- Primary Issue summary 过重或过轻

这些 finding 应推动修改机制，而不是为了“Pilot PASS”隐藏问题。

## Pilot 完成后再决定什么

首个 Pilot 完成后再决定：

- ReadingStep / Session artifact 的正式 schema
- Validator 脚本
- 是否需要自动 checkpoint writer
- Issue Label taxonomy
- `classic-papers-system-design` export protocol
- 是否需要更多 Source provider
- 是否需要学习者弱点统计

以下事项当前已经不再开放讨论：

```text
Issue-driven = yes，但 1 Paper → 1 Primary Issue
reading-mcp = 首选 Source Adapter
Source precise identity 不在 paper-reading-lab 重复实现
```

## 下一步

```text
创建 Raft Primary Paper Issue
→ 用 reading-mcp 打开 USENIX revision
→ 固定 PaperRevision binding
→ 枚举 Introduction SourceUnit
→ 人工抽查 coverage
→ 开始 Session A 第一条 SourceUnit
```
