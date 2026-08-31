# 核心不变量与 Validator 方向

## 目的

Paper Reading Lab 的关键价值不只是“有一套好看的阅读方法”，而是保证真正执行时不会悄悄破坏：

- Source / Derived 边界
- no-lookahead
- revision identity
- Session 可恢复性
- Prediction 时间顺序

第一版先定义不变量，后续再把其中可机器检查的部分实现为 Validator。

## Source identity 不变量

### I-01 Paper 与 Revision 分离

任何 ReadingSession 必须绑定：

```text
paper_id
revision_id
```

不能只用标题作为 identity。

### I-02 Revision 不可静默切换

Session 开始后，如果 Source version 变化，必须：

- 新建 Session，或
- 显式记录 revision transition

不得把旧 checkpoint 改写成新 revision。

### I-03 Source limitation 可见

影响阅读可靠性的限制必须存在于 Source metadata，不能只存在于聊天记忆中。

## Segmentation 不变量

### I-10 顺序稳定

同一 `revision_id` 下，Section / Paragraph / SentenceUnit 必须存在可恢复顺序。

### I-11 SentenceUnit 有定位

每个用于持久化 checkpoint 的 SentenceUnit 必须能回到 Source locator。

### I-12 歧义不能伪装确认

如果断句存在歧义：

```text
segmentation_status != confirmed
```

不能为了流程方便自动标记 confirmed。

### I-13 reveal group 不改变 Source 顺序

多个 SentenceUnit 合并阅读时，只允许形成顺序连续 group。

## No-lookahead 不变量

### I-20 首次顺序 Session 显式声明

严格首次阅读必须声明：

```text
lookahead_policy = no-lookahead
```

### I-21 revealed_position 单调递增

在 `no-lookahead` Session 中：

```text
new_revealed_position >= old_revealed_position
```

回看旧句子不能降低“已经知道到哪里”的事实。

### I-22 当前解释不能引用未来 Source locator

对于 position `N` 的首次阅读 checkpoint：

Derived observation / prediction / explanation 不能把 `N+1..end` 的 SourceUnit 当作依据。

后续 Validator 可以检查显式 Source references。

### I-23 污染必须记录

如果未来内容意外暴露，必须记录 contamination。

不能继续把 Session 标记为严格 clean no-lookahead。

### I-24 Retrospective 显式

知道后文后的回顾必须：

```text
mode = retrospective
```

或等价显式字段。

## Prediction 不变量

### I-30 预测先于揭示

一个正式 Prediction 必须满足：

```text
prediction.created_at
<
actual_next_unit.revealed_at
```

如果无法证明时间顺序，只能视为 retrospective hypothesis，不能当作真实预测训练记录。

### I-31 Prediction 不等于 Source

Prediction 永远不能写回：

```text
source fact
```

### I-32 原预测不可事后美化

揭示实际下一句后，可以追加 comparison，但不能覆写原 prediction，使其看起来更准确。

## ReadingSession 不变量

### I-40 Session 必须可恢复

Paused Session 至少需要：

```text
revision_id
mode
scope
lookahead_policy
revealed_position
next_action
```

缺少这些关键状态时不能声称 checkpoint 可恢复。

### I-41 Session completed 只描述本次目标

不能从：

```text
session.status = completed
```

推导：

```text
paper.done = true
```

### I-42 Paper 不存在永久 done

第一版领域模型不允许永久“论文已经完全学习完”的状态。

可以查询的是：

- 哪些 scope 做过哪些 mode
- 最近 checkpoint
- knowledge gaps
- training results

## Source / Derived 不变量

### I-50 原文事实与解释分离

Derived interpretation 必须能与 Source wording / locator 区分。

### I-51 AI 补全不能成为 Source

任何生成式重建内容都不能标记为：

```text
raw source
source fact
confirmed source wording
```

### I-52 OCR / 转换文本保持 projection 身份

除非其本身就是原始发布格式，否则 OCR / converted text 不替代 Raw / authoritative Source。

## Training 不变量

### I-60 Recall 与重新阅读分离

如果 Recall 过程中已经展示了目标答案，则该次结果不能继续计作无提示 Recall。

### I-61 Reconstruction 必须声明提示级别

建议至少区分：

```text
closed-book
minimal-cue
outline-assisted
open-source
```

避免把“看着提纲复述”和“闭卷重建”混成同一种表现。

### I-62 Transfer 使用新问题

如果所谓 Transfer 只是原题换几个词，不能自动视为已经证明迁移。

第一版可以人工 review，不急于自动评分。

## Export 不变量

### I-70 Finding 不能直接变正式知识

必须：

```text
Reading finding
→ ExportCandidate
→ explicit review
→ target repository gate
```

### I-71 下游状态不能反写 Source

即使下游知识后来被推翻，也不能修改历史论文原文或历史 ReadingSession 当时看到的内容。

## 版权 / Source Policy 不变量

### I-80 公开仓库不默认持久化完整受版权保护全文

若 source artifact 要进入 Git，必须有显式允许依据或仓库策略审批。

### I-81 Locator 优先

能用稳定 locator 恢复 Source 时，不因工程方便复制大段全文。

## 建议的 Validator 分阶段实现

### Phase 1：结构 Validator

检查：

- 必填字段
- stable ids
- revision binding
- allowed status
- locator presence
- session checkpoint completeness

### Phase 2：时序 Validator

检查：

- revealed_position monotonic
- prediction before reveal
- completed / paused transition 合法
- contamination 标记一致

### Phase 3：引用 Validator

检查 no-lookahead Session 的显式 Source references 是否越过 revealed position。

### Phase 4：跨仓库 Export Validator

检查 ExportCandidate 是否：

- 指向具体 Source / Session
- 明确 Derived 身份
- 没有伪装成目标仓库已验证结论

## 最重要的五个 Gate

如果第一版只实现五个检查，优先：

```text
1. Session 必须绑定 revision
2. SentenceUnit 必须可定位
3. no-lookahead revealed_position 单调前进
4. Prediction 必须发生在 reveal 前
5. Session completed 不能升级成 Paper done
```

这五个约束直接保护本仓库最核心的方法论。
