# Fresh Conversation Bootstrap

恢复程序已合并到 [Reading Skill](../../.agents/skills/source-first-reading/SKILL.md) 与 [状态恢复规则](issue-driven-workflow.md#恢复与并发)。本路径仅保留兼容入口，不再维护第二套十步流程。

日常入口：AGENTS → 目标 Issue 当前阅读状态 → Skill / 分析协议。同一会话不用每句重新 bootstrap。

新会话只在暂停后恢复或上下文需要交接时使用；不是逐句阅读的固定阶段，也不是默认隔离验收。历史试次按其原 commit/授权理解，不自动重跑。
