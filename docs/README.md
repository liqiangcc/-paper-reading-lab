# 文档导航

## 日常只读这些

- [AGENTS](../AGENTS.md)：入口与必要边界。
- [逐句分析协议](learning/source-first-sentence-reading.md)：`source-first-analysis/v1`，分析质量唯一日常标准。
- [Reading Skill](../.agents/skills/source-first-reading/SKILL.md)：实际操作，不重复方法定义。
- [阅读状态](learning/reading-sessions.md)：保存/恢复所需的一份记录。

入口提示词只提供 repo + Issue；具体游标从 Issue 当前状态恢复。不要每次加载下面全部文件。

## 按需查阅

- [Issue 与工程流程](workflows/issue-driven-workflow.md)：状态指针、并发冲突、代码修改与关闭证据。
- [Source Adapter](integrations/reading-mcp.md) 与 [Source policy](source/source-policy.md)：工具异常、身份与原始视觉边界。
- [核心不变量](validation/invariants.md) 与 [检查范围](validation/repository-checks.md)：结构检查不等于分析质量评分。
- [语言约定](conventions/language.md)：中文解释与稳定术语。

## 兼容入口，不是新增步骤

[Bootstrap](workflows/conversation-bootstrap.md)、[领域模型](domain/model.md)、[生命周期](workflows/paper-reading-lifecycle.md)、[架构边界](architecture/boundaries.md) 已收敛为短说明，不再平行维护流程或长 schema。

## 历史资料，日常不加载

- [旧 Explanation Profile v0.1](learning/incremental-explanation-profile.md)：冻结内容，供历史绑定使用；不替代新默认协议。
- [首个 Pilot 计划](pilot/first-pilot.md) 与 [Closure](pilot/first-pilot-closure.md)：保留真实 PASS/PARTIAL/FAIL，不作为继续阅读的待办。
- [历史仓库审查](audits/2026-09-repository-audit.md) 与 [闭环复核](audits/2026-09-05-closure-verification.md)：已发生的工程证据，不重新运行其当时的 next_action。

实时进度、候选和任务状态只查对应 Issue，不写死在导航中。未合并资产候选和其固定证据仍按原 PR/SHA 管理，不在本次精简中重写。

## 本地检查

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repository.py
```
