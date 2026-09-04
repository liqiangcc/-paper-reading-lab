# 文档导航

Paper Reading Lab 当前文档按“先边界、再领域、再 Source Adapter、再学习协议、最后执行与验证”的顺序阅读。

## Agent / Fresh conversation 入口

面向 GPT / Codex / Agent 的仓库治理入口：

```text
../AGENTS.md
→ 仓库长期 Agent 规则、工具边界、Skill 路由和 fail-closed 不变量

workflows/conversation-bootstrap.md
→ 薄入口 Prompt 如何从 live Issue / checkpoint / handoff 恢复执行状态

../.agents/skills/source-first-reading/SKILL.md
→ “下一句 / 下一步 / resume ReadingSession” 的可执行 Source-First Reading Skill
```

推荐 fresh conversation 入口保持很薄：

```text
repo + Issue
→ 读取 AGENTS.md
→ 按 bootstrap 路由 Skill
→ 从 durable state 恢复
```

不要把 locator、Profile 全文、历史 transcript 或整套 Source-First 规则重复塞进入口 Prompt。

## 推荐阅读顺序

1. [`../README.md`](../README.md)
   - 仓库目标、核心原则、学习模式和整体边界。

2. [`architecture/boundaries.md`](architecture/boundaries.md)
   - 明确本仓库与 `reading-mcp`、`classic-papers-system-design`、`systems-mechanism-lab` 的职责分离。

3. [`domain/model.md`](domain/model.md)
   - 定义 `Paper`、`PaperRevision`、`ReadingSourceBinding`、`SourceUnitRef`、`ReadingSession`、`ReadingStep`、`ReadingCheckpoint` 等核心对象。

4. [`integrations/reading-mcp.md`](integrations/reading-mcp.md)
   - 定义 `reading-mcp` 作为首选 Source Adapter 的身份、定位、stale、no-lookahead 和降级边界。

5. [`learning/source-first-sentence-reading.md`](learning/source-first-sentence-reading.md)
   - 定义逐句优先、累积上下文、no-lookahead 和一层一层解释的核心学习协议。

6. [`learning/reading-sessions.md`](learning/reading-sessions.md)
   - 定义 Learning、Prediction、Recall、Reconstruction、Transfer、Retrospective 等 Session 模式和 checkpoint。

7. [`workflows/issue-driven-workflow.md`](workflows/issue-driven-workflow.md)
   - 定义 `1 Paper → 1 Primary GitHub Issue`，以及 Issue 作为控制面而非 Source truth 的边界。

8. [`workflows/paper-reading-lifecycle.md`](workflows/paper-reading-lifecycle.md)
   - 分离 Source 生命周期和 ReadingSession 生命周期，并明确 Paper 不存在永久 `done`。

9. [`source/source-policy.md`](source/source-policy.md)
   - 定义论文版本、来源定位、转换文本、OCR 和公开仓库版权边界。

10. [`validation/invariants.md`](validation/invariants.md)
    - 定义后续 Validator 要保护的关键不变量。

11. [`conventions/language.md`](conventions/language.md)
    - 人类文档默认中文，machine identity 使用稳定英文，Source 保持原文。

12. [`pilot/first-pilot.md`](pilot/first-pilot.md)
    - 当前执行入口：Raft 2014 USENIX `Introduction` + `reading-mcp` 的首个真实逐句阅读 Pilot。

## 当前权威入口

当前阶段第一版方法论核心：

```text
README.md
+
docs/architecture/boundaries.md
+
docs/domain/model.md
+
docs/integrations/reading-mcp.md
+
docs/learning/source-first-sentence-reading.md
+
docs/learning/reading-sessions.md
+
docs/workflows/issue-driven-workflow.md
+
docs/workflows/paper-reading-lifecycle.md
+
docs/source/source-policy.md
+
docs/validation/invariants.md
```

当前执行入口：

```text
docs/pilot/first-pilot.md
+
GitHub Issue #1 — Raft 2014 Introduction 逐句阅读 Pilot
```

## 已经确定、不再重复设计的边界

```text
reading-mcp = 首选 Source Adapter
paper-reading-lab = 学习 / Session / 推理 checkpoint 层
GitHub Issue = 工作流控制面

1 Paper → 1 Primary Issue
1 Paper → N ReadingSessions

Source precise identity 由 reading-mcp 提供
paper-reading-lab 保存 SourceUnitRef，不平行重建 Sentence identity
```

## 当前不应该继续扩展的内容

在首个 Pilot 以前，暂时不要急着增加：

- 大量 schema
- 自建 sentence segmentation
- 复杂数据库
- 完整知识图谱
- 大量论文目录
- 自动跨仓库同步
- 完整评分系统
- 大量 Label taxonomy

这些都应由真实逐句阅读暴露的需求驱动。

## 下一步

```text
Issue #1
→ reading-mcp 打开 Raft USENIX PDF
→ 固定 PaperRevision binding
→ 枚举 Section 1 Introduction SourceUnit
→ coverage 抽查
→ Session A 第一条 SourceUnit
```
