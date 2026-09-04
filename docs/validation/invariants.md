# 核心不变量与 Validator 方向

## 目的

Paper Reading Lab 的价值不只是“有一套好看的阅读方法”，而是保证真正执行时不会悄悄破坏：

- Source / Derived 边界；
- no-lookahead；
- revision / provider identity；
- named-section scope boundary；
- ReadingSession 可恢复性；
- Prediction 时间顺序；
- Explanation Profile version；
- Issue / checkpoint / artifact 职责；
- Agent bootstrap / Skill / canonical docs 的分层。

第一版先定义不变量；只有确定性、可机器检查的部分才进入轻量 Validator，其余继续人工 review。

## Source identity 不变量

### I-01 Paper 与 Revision 分离

任何 ReadingSession 必须绑定：

```text
paper_id
revision_id
```

不能只用标题、Issue number 或文件名作为 identity。

### I-02 Revision 不可静默切换

Session 开始后，Source version 变化必须：

- 新建 Session；或
- 显式记录 revision transition。

不得把旧 checkpoint 改写成新 Revision。

### I-03 Source limitation 可见

影响阅读可靠性的限制必须存在于 durable Source metadata，不能只存在于聊天记忆。

### I-04 PaperRevision 必须绑定 Source provider

使用 `reading-mcp` 时至少需要：

```text
provider = reading-mcp
reading_document_id
content / normalized identity
segmentation_version
```

不能只保存 URL 就声称 precise Session 可恢复。

### I-05 stale 必须 fail closed

若上游返回：

```text
STALE_LOCATOR
STALE_CURSOR
identity mismatch
```

当前 precise continuation 必须停止。

禁止：

```text
old snippet
→ similarity search
→ silently choose nearest result
```

## SourceUnitRef 与结构不变量

### I-10 上游 identity 优先

本仓库不自行生成与 `reading-mcp` 平行的 section / sentence identity。

正式 Source reference 优先保存：

```text
reading_document_id
normalized_document_identity
text_unit_id（如有）
text_locator
segmentation_version
```

### I-11 SourceUnitRef 必须可回读

正式 checkpoint 使用的 precise `SourceUnitRef` 必须能交回 Source provider exact re-read。

仅有：

```text
section title
page
paragraph display number
sentence display number
```

不能单独承担 precise identity。

### I-12 降级不能伪装精确

若 provider 只能提供：

```text
actual_kind = paragraph
```

本仓库不能人工伪造：

```text
actual_kind = sentence
```

Source-preserving degradation 必须保留。

### I-13 reveal group 不改变 Source 顺序

多个 SourceUnit 合并阅读时，只允许 canonical 顺序连续 group，并记录成员 identity。

### I-14 display order 不能覆盖 provider order

本地句号编号、UI 排序或人工段落号不得取代 provider canonical order / cursor。

### I-15 Named-section boundary 不得泄露未来正文

严格 named-section Session 的 boundary preflight 必须使用：

- structure-only canonical hierarchy；或
- 绑定当前 Revision / normalized identity 的预验证 boundary artifact。

不得用返回未来正文 snippet 的 lexical search 建立 clean no-lookahead boundary。

## No-lookahead 与 scope 不变量

### I-20 首次顺序 Session 显式声明

严格首次阅读必须声明：

```text
lookahead_policy = past-plus-current-only
```

### I-21 revealed_position 单调递增

```text
new_revealed_position >= old_revealed_position
```

回看旧 SourceUnit 不降低“已经知道到哪里”的事实。

### I-22 当前解释不能引用未来 SourceUnitRef

位置 `N` 的 explanation / prediction / Derived observation 不能把未 reveal 的 `N+1..end` 当作依据。

### I-23 Future Source 不应提前供应

强约束不是：

```text
全文已经交给模型
+
Prompt 要求不要看后文
```

而是：

```text
未来 SourceUnit 尚未通过读取边界供应
```

工具层访问边界优先于 Prompt 自律。

### I-24 污染必须记录

未来内容意外暴露时必须记录：

```text
contaminated_at
future_range_exposed
impact
```

不得继续把 Session 标记为 clean first-pass。

### I-25 Retrospective 显式

知道后文后的回顾必须标记：

```text
mode / lookahead_policy = retrospective
```

### I-26 Search 不得绕过 reveal

clean first-pass Session 不得使用全文搜索：

- 帮助预测下一句；
- fuzzy 恢复 stale locator；
- 绕过 scope gate；
- 建立会泄露未来正文的 section boundary。

### I-27 planned_scope 保留历史

Session 创建时的 `planned_scope` 不得被后续 amendment 覆盖。

### I-28 current_scope_boundary 在 reveal 前执行

每次新 canonical reveal 之前必须确认 next unit 在 `current_scope_boundary` 内。

越界默认 STOP。

### I-29 Scope amendment 先于扩展 reveal

扩展范围必须先 durable 记录：

```text
old_boundary
new_boundary
reason
amendment_point
```

然后才允许 reveal 新范围。

## Prediction 不变量

### I-30 预测先于揭示

正式 Prediction 必须满足：

```text
prediction.created_at
<
actual_next_source.revealed_at
```

无法证明顺序时，只能视为 retrospective hypothesis。

### I-31 Prediction 不等于 Source

Prediction 永远不能写回 `source fact`。

### I-32 原预测不可事后美化

actual reveal 后只能追加 comparison，不能覆盖原 prediction。

## ReadingSession 与 durable state 不变量

### I-40 Session 必须可恢复

Paused Session 的 Operational Recovery Checkpoint 至少需要：

```text
revision_id
source binding
mode / lookahead policy
planned_scope
current_scope_boundary
revealed_position
latest precise locator
next_action
```

缺少关键状态时不能声称可恢复。

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

合理查询是：

- 哪些 scope 做过哪些 mode；
- 最近 checkpoint；
- knowledge / reasoning gaps；
- training results。

### I-43 ReadingStep 不等于 transcript

完整 AI 对话不能自动成为正式 ReadingStep history。

### I-44 ReadingStep 必须保存 precise locator 与 stop boundary

正式增量 Step 至少保存：

```text
current SourceUnitRef / TextLocator
revealed_position
stop_boundary
next_action
```

`stop_boundary` 必须说明下一独立 SourceUnit 尚未 reveal。

## GitHub Issue 与静态文档不变量

### I-45 一个 Paper 一个 Primary Issue

默认：

```text
1 Paper
→ 1 Primary GitHub Issue
```

ReadingSession 不默认各建一个 Issue。

### I-46 Issue number 不承担 Paper identity

Issue number、标题、Label 只是控制面引用。

### I-47 Issue summary 不替代 Session durable state

```text
Primary Issue summary
≠ Operational Recovery Checkpoint
≠ ReadingSession Learning Artifact
```

### I-48 Issue close 不等于 Paper learned

即使关闭某个工作阶段，也不能推导 Paper 无更多学习价值。

### I-49 稳定文档不承担实时调度状态

README / canonical docs 不应把某个瞬时 Issue、Session locator 或 next action 写成长期“当前状态”。

实时状态必须从 live Issue durable record 恢复。

## Source / Derived 与 Explanation Profile 不变量

### I-50 原文事实与解释分离

Derived Interpretation 必须能与 Source wording / SourceUnitRef 区分。

### I-51 AI 补全不能成为 Source

生成式重建内容不能标记为：

```text
raw source
source fact
confirmed source wording
```

### I-52 OCR / 转换文本保持 projection 身份

除非本身就是原始发布格式，否则 OCR / converted text 不替代 Raw / authoritative Source。

### I-53 provider identity 不等于 PaperRevision identity

`reading_document_id` 与 `revision_id` 必须通过 ReadingSourceBinding 显式关联。

### I-54 Profile 不能扩大 Source 可见范围

Explanation Profile 只规定当前 SourceUnit 的解释和呈现，不授权未来 Source reveal。

### I-55 显式 reasoning arrow 必须可追溯

任何正式关系：

```text
A
→ B
```

必须追溯到：

- 当前或此前已揭示 Source；或
- 明确标记为 Derived 的有限推论。

无法说明依据的箭头不能作为 validated reasoning link 持久化。

### I-56 Source Fact、Derived Interpretation 与 Unknown 可区分

Profile 输出不能把三类内容混成同一确定结论。

### I-57 解释深度允许自适应

结构句、标题、图注或术语说明不得被强制包装成不存在的深层机制。

```text
风格稳定
≠ 每句固定长度
```

这一项主要人工 review，不用简单字数评分。

### I-58 Explanation Profile 必须版本化

正式 Profile 至少需要：

```text
profile_id
version
canonical source path
```

### I-59 Session 恢复不得静默切换 Profile version

需要切换时必须新建 Session，或显式记录 transition、位置和影响。

## Training 不变量

### I-60 Recall 与重新阅读分离

展示目标答案后，该次结果不能继续计作无提示 Recall。

### I-61 Reconstruction 必须声明提示级别

至少区分：

```text
closed-book
minimal-cue
outline-assisted
open-source
```

### I-62 Transfer 使用真正的新问题

仅把原题换几个词不能自动证明迁移。

## Export 不变量

### I-70 Finding 不能直接变正式知识

```text
Reading finding
→ ExportCandidate
→ explicit review
→ target repository gate
```

### I-71 下游状态不能反写 Source

下游知识被修正时不能修改历史论文原文或历史 Session 当时看到的内容。

## 版权 / Source Policy 不变量

### I-80 公开仓库不默认持久化完整受版权保护全文

Source artifact 入 Git 必须有明确依据或审批。

### I-81 Locator 优先

能够通过 provider locator 恢复 Source 时，不因工程方便复制大段全文。

## Agent governance 不变量

### I-90 Thin Prompt 只负责寻址

入口 Prompt 不应复制 locator、Profile 全文、Tool 参数或历史 transcript。

### I-91 AGENTS / Bootstrap / Skill / canonical docs 分层

```text
AGENTS.md = routing + hard invariants
Bootstrap = recovery algorithm
Skill = bounded procedure
Canonical docs = detailed method truth
```

任一层都不能静默取代其他层的职责。

### I-92 Capability 以实际 invocation 为准

工具 schema、release note 或历史成功不能替代当前 conversation 的真实调用结果。

### I-93 授权动作完成后停止

Agent 不因当前动作成功而自动扩 scope、开始下一 Session、处理下一 Paper 或合并不相关 Task。

## 建议的 Validator 分阶段实现

### Phase 1 — Repository structure

确定性检查：

- required files；
- Markdown local links；
- Skill front matter；
- duplicate invariant ids；
- canonical docs navigation；
- trailing whitespace / unbalanced fences；
- 稳定 README 中明显旧 live-state 文案。

### Phase 2 — Session structure

未来可检查：

- Revision + provider binding；
- SourceUnitRef presence；
- planned scope / current boundary；
- checkpoint completeness；
- locator + stop boundary；
- bound Profile identity。

### Phase 3 — Temporal invariants

未来可检查：

- revealed_position monotonic；
- prediction before reveal；
- scope amendment before cross-boundary reveal；
- valid Session transitions；
- contamination consistency；
- Profile transition 不改写历史 Step。

### Phase 4 — Source identity

未来可检查：

- locator / cursor identity；
- stale 不能继续；
- segmentation version；
- coarse degradation 未伪装；
- named-section boundary artifact 与 current identity 一致。

### Phase 5 — Source references / export

未来可检查：

- no-lookahead Step 的显式 Source refs 未越界；
- reasoning links 的 Source refs 已 reveal；
- ExportCandidate 指向具体 Source / Session；
- Derived 内容未伪装成 target repository 已验证结论。

## 第一版最重要 Gate

```text
1. Session 绑定 revision + reading provider
2. SourceUnitRef 可以 precise exact re-read
3. stale locator / cursor fail closed
4. named-section boundary 不泄露未来正文
5. planned_scope 与 current_scope_boundary 分离
6. revealed_position 单调前进
7. Prediction 先于 actual reveal
8. Profile version 不静默切换
9. locator + stop boundary 可恢复
10. Session completed 不升级成 Paper done
```

## 核心原则

```text
能机器检查的边界才自动检查。
解释质量和深度继续人工 review。
Validator 保护方法，不取代 Source provider。
真实 Pilot finding 先于复杂 automation。
```
