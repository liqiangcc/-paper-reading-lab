# 论文来源与阅读生命周期

## 目的

Paper Reading Lab 需要同时治理两种完全不同的状态：

1. 论文 Source 是否足够稳定，可以开始逐句阅读。
2. 某一次 ReadingSession 当前进行到哪里。

这两类状态不能混成一个 `paper_status`。

## Source 生命周期

建议第一版：

```text
discovered
    ↓
source-review
    ├──→ blocked
    │      ↓
    │   source fixed / clarified
    │      ↓
    └──── source-review
            ↓
       source-ready
            ↓
     segmentation-review
            ↓
      reading-ready
```

### discovered

已经知道论文存在，但还没有建立稳定身份或可重复访问的 Source。

可能只有：

- 标题
- DOI
- 搜索结果
- 二手引用

### source-review

审核的是来源身份和版本，不审核论文观点是否正确。

需要确认：

- title / author / year / venue
- DOI 或其他 canonical identifier
- 当前读取的是哪个版本
- 来源是否可重复访问
- PDF / HTML / manuscript 的关系
- 页码、章节等 locator 是否可用
- 已知缺失和限制是否记录

### blocked

Source 当前不足以安全阅读，例如：

- 只能找到截断文本
- 版本身份冲突
- OCR 严重损坏
- 公式不可读
- 来源顺序无法恢复

不能为了 unblock 用 AI 重建缺失原文。

### source-ready

表示：

```text
Paper identity 稳定
+
PaperRevision 稳定
+
来源可追溯
+
已知限制已记录
```

这不意味着句子切分已经可用。

### segmentation-review

验证用于顺序阅读的结构：

```text
section
paragraph
sentence order
figure/table/equation locator
```

重点检查：

- PDF 转换是否打乱顺序
- 标题 / 页眉 / 脚注是否混入正文
- 公式是否破坏断句
- 列表是否被错误拼接
- SentenceUnit 边界是否足以支持逐句 reveal

### reading-ready

满足：

- stable PaperRevision
- 可恢复顺序
- 当前 Pilot scope 的 SentenceUnit 足够稳定
- no-lookahead reveal 可以执行

`reading-ready` 只代表可以开始 ReadingSession。

它不代表论文“学完”。

## ReadingSession 生命周期

独立使用：

```text
planned
  ↓
active
  ├──→ paused
  │      ↓
  └──── active
  ↓
completed
```

异常路径：

```text
active
  ↓
abandoned
```

### planned

已经定义并持久化：

- revision
- `planned_scope`
- `current_scope_boundary`
- mode
- lookahead policy
- learning goal

`planned_scope` 是 Session 创建时的历史事实；`current_scope_boundary` 是当前真正可执行的 reveal 边界。两者初始通常一致，但后者只有经过 durable scope amendment 才能扩大。

### active

开始揭示 Source unit。

必须维护：

```text
revealed_position
latest precise TextLocator
current_scope_boundary
```

每次 reveal **之前**必须执行 boundary check：

```text
next canonical unit inside current_scope_boundary?
├─ yes → continue
└─ no  → STOP before reveal
          ↓
       durable scope amendment required
```

不能先 reveal 越界正文，再事后补 scope。

### Scope amendment

确实需要扩大 Session 范围时，先持久化：

```text
old_scope
new_scope
reason
amendment_point
```

然后才更新 `current_scope_boundary` 并继续。原 `planned_scope` 不得被覆盖，因此审计时始终能够区分“原计划”与“后来扩展”。

### paused

当前 Session 暂停，但 Operational Recovery Checkpoint 足以恢复**操作位置和安全边界**。

恢复时不得因为换了 AI conversation 就自动读取未来内容，也不得仅凭旧聊天记忆扩大 scope。

### Operational Recovery Checkpoint

checkpoint 的职责是跨 conversation 安全续作，至少需要表达：

```text
paper_id
revision_id
reading_document_id
content / normalized identity
segmentation_version
current phase / mode
planned_scope
current_scope_boundary
revealed position
latest precise TextLocator
immutable prediction reference（如存在）
blocker / finding
exactly one next action
```

它不承担完整学习状态。

### ReadingSession Learning Artifact

Learning Artifact 的职责是支持 Recall / Reconstruction / retrospective，至少保留如下语义信息：

```text
session identity / mode / scope
revealed range
explicit reasoning links
current problem model / latest model update
knowledge gaps
reasoning gaps
cue level / cue recovery result
prediction comparison finding（如存在）
reconstruction finding（如存在）
```

第一版只定义语义，不在这里规定正式 JSON Schema。Artifact 应明显小于完整 transcript。

因此：

```text
Operational Recovery Checkpoint
≠ ReadingSession Learning Artifact
```

### completed

只表示本 Session 的目标已经达到。

例如：

- 完成 Introduction 第一遍逐句阅读
- 完成某小节 Prediction pass
- 完成一次闭卷 Reconstruction

### abandoned

例如：

- PaperRevision 绑定错误
- segmentation 发现重大错误
- Session 发生不可恢复的 lookahead contamination

Abandoned Session 保留审计信息，不改写成成功记录。

## Paper 没有永久 done

本仓库不定义：

```text
Paper = done
```

原因：

同一篇论文以后可能继续进行：

- deeper reading
- prediction
- recall
- reconstruction
- transfer
- retrospective
- new revision comparison
- new research-question reading

因此合理的查询是：

```text
这篇论文有哪些 completed sessions？
哪些 scope 已经做过哪些 mode？
哪些 knowledge gaps 仍然存在？
```

而不是：

```text
这篇论文处理完了吗？
```

## 首次阅读污染处理

如果首次 no-lookahead Session 意外读取了未来 Source：

不要假装没有发生。

记录：

```text
contaminated_at
future_range_exposed
impact
```

根据影响选择：

- 在后续位置继续，但将 Session 标记为 contaminated
- 或 abandoned 后开启新的首次阅读 Session
- 或转换为 retrospective mode

不得把已知道的未来内容“忘掉”并继续声称这是严格首次阅读。

## Source Revision 更新

如果发现更可靠版本：

```text
Paper
├── Revision A
└── Revision B
```

旧 Session 继续绑定旧 revision，不能批量改写为 Revision B。

可以新建：

```text
revision-comparison session
```

分析版本差异。

## Export 生命周期

ReadingSession finding 不自动进入知识仓库。

建议：

```text
reading finding
    ↓
export candidate
    ↓
explicit review
    ↓
目标仓库接收
    ↓
目标仓库自己的 gate
```

目标仓库拒绝或修正 ExportCandidate，不影响原 ReadingSession 的历史事实。

## Pilot 推荐流程

第一篇论文不要直接跑全文。

推荐：

```text
选择一篇经典论文
→ 验证 PaperRevision
→ 只切一个小节
→ persist planned_scope + current_scope_boundary
→ segmentation review
→ reading-ready
→ reveal 前执行 scope boundary check
→ Learning Session 逐句完成小节
→ 保存 Operational Recovery Checkpoint
→ 保存最小 Learning Artifact
→ 新会话恢复一次
→ Prediction / Recall 再走一遍
→ 小节 Reconstruction
→ review 机制问题
```

只有这条链跑通以后，再决定是否扩到整篇论文和更多论文。

## 核心不变量

```text
Source status 与 Session status 分离。
source-ready 不等于 reading-ready。
reading-ready 不等于学完。
planned_scope 必须持久化，current_scope_boundary 必须可执行。
跨 current_scope_boundary 的 reveal 默认 STOP，必须先 durable scope amendment。
Operational Recovery Checkpoint ≠ ReadingSession Learning Artifact。
Session completed 不等于 Paper done。
旧 Session 永远绑定旧 Revision。
lookahead contamination 必须显式记录。
```
