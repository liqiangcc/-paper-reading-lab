# 论文来源与阅读生命周期

## 目的

Paper Reading Lab 同时治理多种不同状态：

```text
PaperRevision / Source readiness
ReadingSession lifecycle
Explanation Profile binding
Operational recovery
Learning artifact maturity
Export review
```

这些状态不能混成一个 `paper_status`。

## Source 生命周期

```text
discovered
→ source-review
   ├── blocked
   └── source-ready
       → segmentation-review
       → reading-ready
```

### discovered

已经知道论文存在，但还没有稳定 PaperRevision 或可重复访问 Source。

### source-review

审核：

- title / author / year / venue；
- DOI 或 canonical identifier；
- 当前使用哪个 Revision；
- Source provenance；
- PDF / HTML / manuscript 关系；
- raw/content hash；
- known limitations。

不在这里判断论文观点是否正确。

### blocked

Source 不足以安全阅读，例如：

- 只能找到截断文本；
- Revision identity 冲突；
- OCR 严重损坏；
- 公式或正文不可读；
- canonical order 无法恢复；
- named-section boundary 只能通过泄露未来正文获得。

不能用 AI 重建缺失原文来 unblock。

### source-ready

```text
Paper identity stable
+ PaperRevision stable
+ provenance traceable
+ content identity known
+ limitations durable
```

不表示 sentence segmentation 已可用。

### segmentation-review

验证当前 Pilot / Session scope 所需结构：

```text
named section hierarchy
paragraph / sentence order
SourceUnit boundary
content classification
Figure / Table / Equation locator
original source view
```

重点检查：

- 多栏 PDF 顺序；
- 标题 / 页眉 / 脚注污染；
- 公式 / 列表断句；
- canonical unit 是否含多个 surface sentences；
- coarse degradation 是否被保留；
- exact locator re-read；
- structure-only scope boundary 是否可建立。

### reading-ready

满足：

- stable PaperRevision；
- explicit ReadingSourceBinding；
- 当前 scope 的 canonical order 可恢复；
- `planned_scope` 可以转化为 executable `current_scope_boundary`；
- current SourceUnit / locator 足以进行 no-lookahead reveal；
- known limitation durable。

`reading-ready` 只表示可以启动 ReadingSession，不表示论文“学完”。

## ReadingSession 生命周期

```text
planned
→ active
↔ paused
→ completed
```

异常路径：

```text
planned / active
→ abandoned
```

### planned

开始前持久化：

```text
session_id
paper_id / revision_id / source binding
mode
learning_goal
lookahead_policy
planned_scope
current_scope_boundary
Explanation Profile identity（如采用）
revealed_position = none or resumed locator
```

`planned_scope` 是历史计划；`current_scope_boundary` 是当前真正可执行的 reveal gate。

### Scope preflight

正文 reveal 前：

```text
planned_scope
→ resolve canonical owner / stop boundary
→ persist current_scope_boundary
→ only then start SourceUnit reveal
```

named-section preflight 必须 structure-only，不得通过 future-body lexical search 建立 clean boundary。

### active

每次新 reveal 前：

```text
verify Source / Profile identity
→ verify next unit inside current_scope_boundary
→ execute bounded action
→ update revealed_position
→ record stop_boundary
```

首次 no-lookahead Session 中 `revealed_position` 单调向前。

### Scope amendment

跨出当前 boundary 前先记录：

```text
old_boundary
new_boundary
reason
amendment_point
```

然后才更新 `current_scope_boundary`。原 `planned_scope` 不覆盖。

### paused

当前 Session 暂停，但 Operational Recovery Checkpoint 足以恢复：

- Source / Revision；
- scope / position；
- Profile；
- immutable prediction；
- blocker；
- exactly one next action。

换 conversation 不自动授权未来 reveal。

### completed

只表示本 Session 目标达到，例如：

- 完成 Introduction 首次 Learning；
- 完成一轮 Prediction pass；
- 完成一次 closed-book Reconstruction；
- 完成一个 Profile acceptance fixture。

`Session completed ≠ Paper done`。

### abandoned

适用于：

- Revision / Source binding 错误；
- 重大 segmentation defect；
- lookahead contamination；
- scope contract 无法保持；
- stale identity 无法安全迁移。

Abandoned Session 保留审计信息，不能改写成 paused / completed。

## Explanation Profile 生命周期

```text
pilot-candidate
→ acceptance evidence
→ stable
```

或：

```text
pilot-candidate
→ finding
→ revised new version
```

### 绑定

Session 使用：

```text
profile_id
version
canonical source path
style overrides
```

Profile 只控制解释与呈现，不扩大 Source visibility。

### 版本更新

改变 MUST、深度语义或恢复契约时产生新版本。

历史 Session 继续绑定旧 Profile。切换必须新 Session 或显式 transition。

## Operational Recovery Checkpoint 生命周期

在以下 boundary 更新：

- Session start；
- pause / resume；
- Prediction lock；
- scope amendment；
- blocker；
- current ReadingStep stop；
- acceptance / handoff。

目标：

```text
fresh conversation
→ safe operation continuation
```

它不是 full transcript，也不承担高保真 Recall。

## ReadingSession Learning Artifact 生命周期

在自然学习边界压缩更新：

- 段落或机制闭环；
- Session pause / completion；
- Recall / Reconstruction finding；
- retrospective review。

目标：

```text
later active recall / reconstruction
→ recover reasoning structure
```

它比 Operational Checkpoint 更丰富，但仍明显小于 transcript。

## 首次阅读污染

future Source 意外暴露时记录：

```text
contaminated_at
future_range_exposed
impact
```

根据影响：

- 标记 contaminated 并转换 mode；
- abandoned 后开 fresh Session；
- 显式进入 retrospective。

不得“假装忘掉”后继续声称 strict first-pass。

## Source Revision / normalization 更新

```text
Paper
├── Revision A / Binding A
└── Revision B / Binding B
```

旧 Session 永远绑定旧 Revision / Binding identity。

normalized identity 变化时旧 locator stale。可以：

- 新建 Session；
- 显式 migration；
- revision / normalization comparison。

不能 fuzzy rebase 后静默继续。

## Paper 没有永久 done

同一篇论文以后仍可进行：

- deeper Learning；
- Prediction；
- Recall；
- Reconstruction；
- Transfer；
- Retrospective；
- new Revision comparison；
- new research-question Session。

合理查询：

```text
有哪些 completed / abandoned Sessions？
哪些 scope 做过哪些 mode？
最近 revealed_position 是什么？
哪些 knowledge / reasoning gaps 仍存在？
```

而不是：

```text
Paper done?
```

## Export 生命周期

```text
Reading finding
→ ExportCandidate
→ explicit review
→ target repository gate
→ validated knowledge
```

下游拒绝或修正 ExportCandidate 不改变历史 Source / Session。

## Pilot 推荐流程

```text
选择经典论文
→ verify PaperRevision / Source binding
→ define small planned_scope
→ structure-only boundary preflight
→ segmentation review
→ reading-ready
→ source-first Learning
→ Operational Recovery Checkpoint
→ minimal Learning Artifact
→ fresh-conversation recovery
→ Prediction / Recall
→ Reconstruction
→ retrospective / mechanism findings
→ closure
```

只有真实链路跑通后，才决定是否扩全文、增加更多论文或实现复杂 schema / automation。

## 状态所有权

```text
Source readiness
→ Source / integration docs + durable Issue summary

Session status / scope / position
→ ReadingSession durable state

Current workflow next action
→ live Issue record

Paper body truth
→ reading-mcp

Explanation format
→ bound Profile

Validated knowledge
→ target repository
```

## 核心不变量

```text
Source status 与 Session status 分离。
source-ready 不等于 reading-ready。
reading-ready 不等于学完。
planned_scope 保留历史。
current_scope_boundary 在 reveal 前执行。
跨 scope 默认 STOP，先 amendment 后 reveal。
Profile version 不静默切换。
Operational Checkpoint ≠ Learning Artifact。
contamination 必须记录。
Session completed 不等于 Paper done。
旧 Session 永远绑定旧 Revision / Source identity。
```
