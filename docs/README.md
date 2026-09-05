# 文档导航

Paper Reading Lab 的静态文档只承担**稳定方法、领域模型和治理规则**，不承担实时任务状态。当前 Paper / Session / Task 的 live state 始终以对应 GitHub Issue 的最新 durable record 为准。

## Agent / fresh-conversation 入口

面向 GPT、Codex 和其他 Agent 的入口：

```text
../AGENTS.md
→ 仓库级规则、工具边界、Skill 路由和 fail-closed 不变量

workflows/conversation-bootstrap.md
→ 薄 Prompt 如何从 live Issue / checkpoint / handoff 恢复执行状态

../.agents/skills/source-first-reading/SKILL.md
→ source-first ReadingSession 的有界执行程序
```

推荐入口保持很薄：

```text
repo + Issue
→ 读取 AGENTS.md
→ 按 bootstrap 路由 Skill
→ 从 durable state 恢复
```

不要在入口 Prompt 中重复 TextLocator、Profile 全文、历史 transcript 或整套 Source-First 规则。

## 推荐阅读顺序

1. [`../README.md`](../README.md)
   - 仓库目标、总体模型、稳定入口与核心不变量。

2. [`../AGENTS.md`](../AGENTS.md)
   - Agent 长期工作规则、工具职责、路由与停止条件。

3. [`architecture/boundaries.md`](architecture/boundaries.md)
   - 明确 `paper-reading-lab`、`reading-mcp`、GitHub Issue 和下游知识仓库之间的职责分离。

4. [`domain/model.md`](domain/model.md)
   - 定义 `Paper`、`PaperRevision`、`ReadingSourceBinding`、`SourceUnitRef`、`ReadingSession`、`ReadingStep`、checkpoint、learning artifact 和 Explanation Profile 等领域对象。

5. [`integrations/reading-mcp.md`](integrations/reading-mcp.md)
   - 定义 `reading-mcp` 作为 Source Adapter 的 identity、named-section structure、locator、stale、source view 和 no-lookahead 边界。

6. [`source/source-policy.md`](source/source-policy.md)
   - 定义论文版本、来源、转换文本、OCR、原始视觉 Source 和公开仓库版权边界。

7. [`learning/source-first-sentence-reading.md`](learning/source-first-sentence-reading.md)
   - 规定允许读取什么、何时允许读取，以及逐句增量学习的基本协议。

8. [`learning/incremental-explanation-profile.md`](learning/incremental-explanation-profile.md)
   - 规定取得当前 SourceUnit 后的解释与呈现方式，包括 MUST / SHOULD / MAY 和 L0 / L1 / L2 自适应深度。

9. [`learning/reading-sessions.md`](learning/reading-sessions.md)
   - 定义 Learning、Prediction、Recall、Reconstruction、Transfer、Retrospective、scope、Profile binding、checkpoint 和 learning artifact。

10. [`workflows/issue-driven-workflow.md`](workflows/issue-driven-workflow.md)
    - 定义 `1 Paper → 1 Primary Issue`，以及 Issue 作为控制面而非 Source truth 的边界。

11. [`workflows/paper-reading-lifecycle.md`](workflows/paper-reading-lifecycle.md)
    - 分离 Source 生命周期、ReadingSession 生命周期和 export 生命周期。

12. [`workflows/conversation-bootstrap.md`](workflows/conversation-bootstrap.md)
    - 定义 fresh conversation 的恢复顺序、durable-record 选择、capability check、执行和停止。

13. [`validation/invariants.md`](validation/invariants.md)
    - 定义后续 Validator 和人工 review 必须保护的关键不变量。

14. [`conventions/language.md`](conventions/language.md)
    - 人类文档默认中文，machine identity 使用稳定英文，Source 保持原文。

15. [`pilot/first-pilot.md`](pilot/first-pilot.md)
    - Kafka 2011 首个真实 Pilot 的历史执行协议和原始验收基线。

16. [`pilot/first-pilot-closure.md`](pilot/first-pilot-closure.md)
    - 首个 Pilot 的 closure matrix、真实 finding、已完成 hardening 和未解决边界。

17. [`audits/2026-09-repository-audit.md`](audits/2026-09-repository-audit.md)
    - 本轮全仓库一致性审查、修复和剩余 finding。

## 可执行 Skill

### Source-First Reading

路径：

```text
../.agents/skills/source-first-reading/SKILL.md
```

适用于：

- 开始、继续或恢复 source-first ReadingSession；
- 用户说“下一句 / 下一步”；
- 按 durable checkpoint 执行 exactly-one ReadingStep；
- 当前已允许 Source 的 Figure / Table / Equation fidelity review；
- scope、locator、revision、Profile 或 MCP blocker 时安全停止。

Skill 是**有界执行程序**，不是新的方法论来源。它必须引用 canonical docs，不得平行重建 Source identity 或扩大 no-lookahead 可见范围。

## 文档职责图

```text
AGENTS.md
→ repository routing + hard invariants

conversation-bootstrap.md
→ fresh-conversation recovery algorithm

source-first-reading/SKILL.md
→ bounded execution procedure

source-first-sentence-reading.md
→ source visibility / incremental learning protocol

incremental-explanation-profile.md
→ explanation and presentation contract

reading-sessions.md
→ Session modes / scope / durable learning state

reading-mcp.md
→ Source Adapter contract

invariants.md
→ review / validator protection targets
```

## 稳定入口与实时状态

静态文档可以引用 Paper Issue 作为案例，但不把“当前正在执行哪个 Issue”写成长期真相。

实时查询应回答：

```text
这个 Paper 的 Primary Issue 是什么？
最新 Session checkpoint / handoff 是什么？
当前 scope / revealed_position / next_action 是什么？
哪些 Task / PR 已完成或被阻塞？
```

而不是从 README 中推断当前任务。

## 当前不自动化的部分

在更多真实 Session 证明必要前，不急于增加：

- 大型数据库；
- 自建 sentence segmentation；
- 完整知识图谱；
- 自动风格评分或 LLM-as-judge；
- 完整 Session JSON schema；
- 自动跨仓库同步；
- 大量 mode / score Label。

已经有重复性证据的基础治理检查可进入轻量 Validator，但不能替代 Source provider、人工 review 或真实 Pilot。

## 有界学习资产案例

[Kafka 三单元 Learning Artifact](learning/artifacts/kafka-2011/transfer-fixture-v0-1.md) 与 [操作恢复检查点](learning/artifacts/kafka-2011/transfer-fixture-recovery.md) 展示学习模型和操作状态的分离；它们是固定范围的 Derived 案例，不是实时调度入口或正式论文结论。候选与验收进度读取关联 Task 的最新 durable record。

## 本地校验

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repository.py
```

详细范围与未覆盖项见 [`validation/repository-checks.md`](validation/repository-checks.md)。历史审查见 [`audits/2026-09-repository-audit.md`](audits/2026-09-repository-audit.md)，闭环复核与回归记录见 [`audits/2026-09-05-closure-verification.md`](audits/2026-09-05-closure-verification.md)。
