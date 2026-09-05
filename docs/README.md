# 文档导航

## 日常只读这些

- [AGENTS](../AGENTS.md)：入口与必要边界。
- [逐句分析协议](learning/source-first-sentence-reading.md)：`source-first-analysis/v2`，分析质量唯一日常标准。
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

## 历史引用

旧 Profile 与 Pilot 已从当前文件树删除，不保留可执行训练入口。旧 Session 需要核对历史时按绑定的 commit + path 获取；例如 [旧 Profile v0.1](https://github.com/liqiangcc/paper-reading-lab/blob/27471ed0b2b99ad9c25c088a55cbbf6ad7c5ee67/docs/learning/incremental-explanation-profile.md)、[Pilot 原记录](https://github.com/liqiangcc/paper-reading-lab/tree/c000a92c71d07026882a4d13d86b98a55ecf27fc/docs/pilot) 与 [分析契约 v1](https://github.com/liqiangcc/paper-reading-lab/blob/c000a92c71d07026882a4d13d86b98a55ecf27fc/docs/learning/source-first-sentence-reading.md)。不把 main 当成旧版本，不执行历史 next_action，不把历史未测或失败改为 PASS。

[历史仓库审查](audits/2026-09-repository-audit.md) 与 [闭环复核](audits/2026-09-05-closure-verification.md) 仅记录已发生的工程事实，不是运行规则。实时状态只查对应 Issue；已被用户目标取消的旧任务和未合并候选不再阻塞阅读。

## 本地检查

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repository.py
```
