# reading-mcp 集成

本文件是按需查阅的工具边界，不是每句阅读的额外前置流程。正式执行步骤只在 [Reading Skill](../../.agents/skills/source-first-reading/SKILL.md) 定义。

## 身份

保留 `paper_id / revision_id` 与 provider 的 `document_id / content_hash / normalized_document_hash / segmentation_version` 绑定。provider document id 不能替代论文版本，旧 hash/locator 不能静默套用新 normalization。

从已保存身份恢复；只在需要打开来源或身份核验时调用相应工具，不在每一句枚举所有工具或单独做健康探针。实际成功调用才是可用性证据。

## 范围与读取

named-section 边界优先取不含正文的结构层级或绑定当前 identity 的预验证边界。不能为了确定停止点搜索尚未揭示正文；边界不明先停。

顺序阅读默认 `get_text_units(requested_kind=sentence, direction=forward, coverage_policy=preserve_source, max_items=1)`，使用当前 document、允许的 owner/section 和精确 anchor。

对返回单元调用 `read_document(document_id, target_locator)`，不要同时传 `section_id`。核对 resolved identity、范围、完整性与截断状态；不能因显示句号编号相同就视作一致。

一个 canonical unit 可以包含多个表面句子，也可能是 fragment/paragraph/heading/caption。保留实际 kind 和顺序，不自造新 identity；结构单元也消耗当前一次读取，除非已有 scope 明确允许进一步过滤。

## 异常

`STALE_LOCATOR / STALE_CURSOR / identity mismatch` 停止精确续作；不拿旧文本做 fuzzy search。原文缺失不使用模型记忆、旧 Issue 解释或 Web 替代。

枚举已经返回文字后，即使精确回读失败，也要保留实际暴露范围；不谎称零揭示。工具或写入失败时保存能确认的状态，恢复不猜测跳过单元。

`search_document` 不得用于获取未来正文、帮助预测或模糊恢复；它不是默认顺序阅读工具。需要外部/跨版本调查时先单独获授权。

## 原始视觉

当前允许内容确需图、表、公式或布局核对时，使用 locator 绑定的原始 source view。区分原始视觉观察、提取文字与 AI 解释，不用 OCR/重绘冒充原页。

优先使用可限制到当前目标的视图；若工具只能暴露带未读内容的整页且无法满足当前边界，先说明限制，不先取整页再声称“没有用后文”。意外暴露必须记录；不能假装忘记。

本仓库不重新实现 parser 或句子索引，也不固定 live Tool 数量。保留不影响当前阅读的已知限制，不能把一个样本成功宣称成全文正确。
