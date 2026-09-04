# Kafka 2011 首个 Paper Reading Lab Pilot — Closure

## 状态

```text
First Pilot mechanism validation
= COMPLETED WITH FINDINGS

Kafka Paper
≠ done

Primary Paper Issue
= remains open for future Sessions
```

本文件是首个 Pilot 的稳定 closure 摘要。完整时间顺序、SourceLocator、runtime failure、Prediction 和 acceptance 证据保留在 Kafka Primary Paper Issue 的 durable comments 中。

## Pilot 目标

验证以下链路是否能在真实论文上运行：

```text
Stable PaperRevision
→ reading-mcp Source binding
→ source-first / no-lookahead reveal
→ precise locator
→ durable checkpoint
→ fresh-conversation recovery
→ Prediction before reveal
→ Prediction vs Actual
→ Recall
→ Reconstruction
→ original-source fidelity
→ retrospective / closure
```

目标不是读完整篇 Kafka 2011，也不是直接产出最终知识卡片。

## Source binding

Pilot 绑定：

```text
paper_id:
kafka-2011-distributed-messaging

revision_id:
kafka-2011-netdb11

provider:
reading-mcp
```

正式 Session 还绑定了 provider document、content、normalized identity 和 segmentation version。后续 normalization / Profile 更新不能静默改写历史 Pilot identity。

## Closure matrix

| 项目 | 结果 | 说明 |
|---|---|---|
| PaperRevision / Source binding | PASS | durable identity 与 exact-read identity 一致 |
| Canonical SourceUnit sequential reveal | PASS | 实际使用有界 sentence-first reveal |
| Precise TextLocator exact re-read | PASS | fresh conversation 中成功回读当前 locator |
| No-lookahead | PASS | Prediction 先锁定；Tool blocker 时未绕过 Source Adapter |
| Cross-conversation recovery | PASS | 仅靠 Issue checkpoint + canonical Source 恢复 |
| Prediction before reveal | PASS | 时间顺序有 durable evidence |
| Prediction vs Actual | PASS | 保留 partial match、missing cue 和 model update |
| Recall | PARTIAL | 能恢复局部结构，但 checkpoint 信息密度不足以恢复全部已读模型 |
| Reconstruction | PARTIAL | 能重建当前可恢复范围，未达到全部历史范围高保真重建 |
| Figure / original-source fidelity | PASS（tested case） | Figure 2 通过 original source view 核对 |
| Segmentation | PARTIAL | 当前 prose locator 稳定；不能据此声称全文无缺陷 |
| Stale fail-closed | PASS | 错误 normalized hash 返回 stale，未 fuzzy rebase |
| Checkpoint usability | PARTIAL | 操作续作足够，学习模型恢复偏轻 |
| Issue control plane | PARTIAL / usable | 能 durable handoff，但 Issue body 容易落后于最新 comments |
| Scope discipline | FAIL | 原计划 Abstract → Section 1，真实阅读推进到 Section 3.1 |

## 关键成功证据

### 1. Source 与 Session 分离成立

```text
PaperRevision identity
+
reading-mcp precise Source identity
→ 可以跨 conversation 回到同一 canonical unit
```

### 2. No-lookahead 在失败路径中仍可执行

当旧 conversation 的 `reading-mcp` invocation 被禁用时，Session 没有：

- 用模型记忆补下一句；
- 从已经看到的整页 PDF 偷读未来正文；
- 使用下游 Kafka 分析资产；
- 通过 Web 替代 Source provider。

而是持久化 blocker / handoff 并在 fresh conversation 恢复。

### 3. Prediction-before-reveal 有实际学习价值

原 Prediction 预期作者会立即从高层 transfer concern 进入具体成本 / mechanism。

Actual next unit 先用 backward-reference recap 重新激活 producer batching。

暴露的 reasoning gap：

```text
高层过渡
≠ 下一句一定立刻引入新机制

作者可能先用 recap / bridge
→ 恢复前文设计线索
→ 再继续论证
```

### 4. Original source view 是必要补充

Figure 2 证明：

```text
normalized text
≠ visual document semantics
```

原始页面可以补足 Figure、布局和箭头关系；但整页视觉仍不能绕过 canonical no-lookahead reveal。

## 主要失败与影响

### Scope drift

原 `planned_scope`：

```text
Abstract
→ Section 1 Introduction
```

真实 reading position 最终进入 Section 3.1。

原因：

```text
文档中写了 scope
但没有 executable current_scope_boundary
→ 连续“下一句”自然跨界
```

影响：

- 不否定 Source identity、no-lookahead、fresh recovery、Prediction 和 stale fail-closed 证据；
- 不能声称 Pilot 严格按原预定小节执行；
- scope discipline 必须保留为 FAIL。

已完成 hardening：

```text
planned_scope durable
+
current_scope_boundary executable
+
pre-reveal boundary check
+
cross-scope default STOP
+
durable amendment before expansion
```

### Checkpoint 信息密度不足

Pilot 证明：

```text
cursor / locator / next_action
→ 足以操作恢复

但

cursor / locator / next_action
→ 不足以高保真 Recall / Reconstruction
```

因此已明确：

```text
Operational Recovery Checkpoint
≠ ReadingSession Learning Artifact
```

### Issue body 与 comments 漂移

Issue body 适合稳定 Paper / Revision / Source / goal 摘要；实时 Session 状态需要最新 tagged durable record。

治理结论：

```text
Issue = control plane
但 worker 必须读取 live comments
不能只信 body 中旧“当前状态”
```

## 后续已完成机制修复

首个 Pilot 后已经形成：

- durable `planned_scope` / `current_scope_boundary`；
- scope amendment 规则；
- Operational Recovery Checkpoint / Learning Artifact 分离；
- Explanation Profile v0.1；
- thin-entry `AGENTS.md` / conversation bootstrap；
- Source-First Reading Skill；
- named-section structure-only boundary 能力的真实 Raft 验证；
- original-source view 的真实 Kafka 验证。

## 仍然保留的边界

1. Profile v0.1 通过 fresh-conversation L2 fixture，但不单独证明所有 L0 / L1 / L2 情况都充分覆盖。
2. Recall / Reconstruction 需要更多真实 Learning Artifact 证据。
3. 全文 segmentation fidelity 未被首个 Pilot 全量证明。
4. transient nested-integer serialization failure 曾出现，后来同 locator fresh exact-read 成功；保留为历史 runtime finding，不据此声称稳定 defect 已消失或仍存在。
5. Issue comments 的 durable-record 选择仍主要依赖治理协议，而不是专用数据库。

## Completion 语义

```text
首个机制 Pilot completed
≠ 所有机制 PASS
≠ Kafka Paper done
≠ future Sessions unnecessary
```

同一篇 Kafka 论文以后仍可进行：

- deeper Learning；
- new Prediction cycle；
- Recall；
- Reconstruction；
- Transfer；
- Retrospective；
- revision comparison。

这些应创建新的 ReadingSession，并绑定明确 scope、Source identity 和 Profile version。

## 下一步原则

未来改进继续遵循：

```text
真实 Session
→ finding
→ 最小机制修复
→ invariant
→ 可机器检查部分
→ automation
```

不因首个 Pilot 完成就提前建立复杂数据库、自动评分或完整知识图谱。
