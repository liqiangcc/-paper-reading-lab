# Source Policy

## 原文与分析分开

论文的明确 Revision 是研究对象；reading-mcp 提供 canonical 单元与 locator。中文翻译、机制解释、作者意图判断和关系链不是新的原文。

当前说法须能回到已揭示 Source；推论注明前提，不用现代实现或后文倒填当前判断。必要背景与论文自身证据分开。

## 身份与缺失

保留版本、来源、内容/normalized identity、segmentation 和精确 TextLocator。版本或 normalization 改变时不静默匹配旧位置；缺句、缺图、公式不可读时不靠生成式补全继续。

只核验当前阅读所需范围，不为做全篇覆盖检查提前暴露后文。已知但不影响本单元的限制简短记录，不自动扩大成全仓治理任务。

## 投影与视觉

normalized text/OCR 是提取投影，不等于原始排版；AI 重建更不能当 authoritative wording。当前图表等确有需要时核对绑定的原始视觉，不能借整页获得未读内容；细节见 [Source Adapter](../integrations/reading-mcp.md)。

## 公开仓库版权边界

默认不保存整篇论文或大段连续原文。保留 metadata、hash、来源、精确 locator、短而必要的引用及自己的分析摘要。存在本地副本不自动意味着可公开分发。

Issue comment 不成为 canonical Source，分析资产也不替代精确原文。旧证据保留原身份和限制，不因后续修改重写历史。
