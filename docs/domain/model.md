# 最小领域模型

正常阅读只需要三个东西：

- **Source binding**：这篇论文的哪个 Revision，对应 reading-mcp 的哪个 document/hash/segmentation。
- **阅读状态**：已授权范围、精确位置、分析契约及已读模型。
- **Primary Issue**：指向这份当前状态，保存必要历史。

详细字段只在 [阅读状态](../learning/reading-sessions.md) 定义，不在这里重复 schema。TextLocator / canonical 单元由 reading-mcp 拥有，不重新构造 identity。

操作定位与分析摘要可同记录分区；需要长期复用时才抽出资产。PredictionRecord、TrainingResult、ExportCandidate 等不再是默认对象；旧记录在原 commit 中保留，不作当前必填字段或流程阶段。

一个 Session 结束不等于论文永久学完。旧 Session、Profile 和 Source identity 不因本次简化被静默改写。
