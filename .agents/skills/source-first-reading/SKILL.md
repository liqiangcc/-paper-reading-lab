---
name: source-first-reading
description: 基于 reading-mcp 原文提供一次高质量逐句分析，支持下一句、追问、回看和继续；不用于仓库修改，不默认进行作答训练或隔离验收。
---

# Source-First Reading

遵循 [AGENTS](../../../AGENTS.md) 和 [分析协议](../../../docs/learning/source-first-sentence-reading.md)。本文件只保留操作步骤，不复制分析质量标准。

## 开始或恢复

读取目标 Issue 当前正文及明确指向的 [阅读状态](../../../docs/learning/reading-sessions.md)，核对 Source identity、已读 locator、授权范围、分析契约和必要前文模型。默认不读取全部评论或历史验收答案。旧记录缺失/冲突时按 [状态规则](../../../docs/workflows/issue-driven-workflow.md) 处理，不能猜测游标。

同一会话已核验的规则和状态直接继续使用；不用每句重读仓库、探测所有工具或新开 Session。能力检查并入实际需要的工具调用。

## 下一句

1. 确认下一单元在当前授权范围内；边界无法确认或将越界时先停，不先读再改范围。
2. 调用 `get_text_units`，使用绑定 document、当前 owner/section 和精确 anchor，默认 `requested_kind=sentence`、`coverage_policy=preserve_source`、`direction=forward`、`max_items=1`。
3. 使用返回的 `TextLocator` 调用 `read_document(document_id, target_locator)` 精确回读，不同时加 `section_id`；核对 identity、范围、完整性。保留 provider 单元，不擅自过滤后再读取第二个。
4. 按分析协议呈现原文、必要翻译和清楚的分析；更新本会话中的已读位置和模型增量。
5. 本次输出结束，等待用户继续；不附带考试、长 checklist 或新会话提示词。

## 追问与回看

只解释已有内容，按需要精确回读已授权 locator；不推进新正文。当前图表/公式确有需要时才使用 locator 绑定的原始视觉，不能借整页看后文。细节见 [Source Adapter](../../../docs/integrations/reading-mcp.md)。

## 保存与异常

自然边界、暂停、交接、范围变化或故障时写一份完整、简短的阅读状态并回读；不把逐句输出逐条写成 START/RESULT/HANDOFF。

若在枚举后精确回读失败，保留已经实际暴露的单元/locator及失败事实，不谎称未揭示。身份或范围不确定时停止，不能换成最像的文本。未持久化的会话进度可能丢失；恢复以最后可靠保存位置为准，必要时重复已读单元而不猜测跳过。

原文正确性不受简化流程影响；阻塞原因未变不重复写同样记录。只在实际需要交接时换会话，不为了保持风格而定期重测。
