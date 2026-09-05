# 阅读状态

正常学习只有“读取当前原文并分析”这条主线；不按 Learning → Prediction → Recall → Reconstruction 排流水线。用户追问或回看也不必创建新 Session。

## 一份状态足够

每篇论文保留一个 Primary Issue。正文指向唯一的当前 `[READING STATE]`；状态至少包含：

```text
论文/Revision + reading-mcp document/hash/segmentation identity
当前已授权范围 + 已揭示位置/精确 TextLocator
分析契约 id + source commit（旧 Profile 如存在则保留）
简短前文模型：已知事实、关键连接、尚未回答的问题
当前状态/阻塞 + 下一动作
```

这是字段语义，不是新增 JSON Schema。复用已有可靠绑定与完整 locator，不要求用户填写。事实和推论在摘要内能区分即可；无内容的字段不必机械列出。

操作定位和分析摘要可以放在同一记录的两个区块，语义分开，不强制拆成两份文件。只有摘要明显过长或用户要求反复查阅时，才抽出一份资产并链接；不为每句或每个模式增加独立对象。

## 何时保存

同一会话逐句更新当前位置；自然段落/机制收束、暂停、交接、范围变化或故障时再写 GitHub。没有这些变化不制造新 comment。用户要求保存时立即保存。

写入完整新状态后，更新 Issue 正文指针并回读确认；旧状态留作历史。若写入中断导致指针落后，按 [恢复规则](../workflows/issue-driven-workflow.md#恢复与并发) 检查较新控制记录，不能按旧指针盲目前进。

不保存完整 transcript，也不声称未持久化的会话状态可以无损恢复。

## 范围与版本

`planned_scope` 是既有历史计划；`current_scope_boundary` 是当前实际授权，不因简化删除。下一单元越界前先获用户许可并保存变化；若用户明确授权整节，则不用逐句再申请授权。

Source/normalization 变化不自动迁移旧 locator；分析契约切换记录一次旧/新绑定、生效位置与依据。已读位置只增不减。回看只改变视图，不把看过的内容变回未知。

历史 Session 的 completed/abandoned/contamination 保留；本轮阅读结束不意味着论文永久学完，也不要求追加 Recall 或其他验收才能完成。

## ReadingSession Learning Artifact

资产是帮助 AI 恢复已读模型、风格和开放问题的简短分析摘要，不是默认考试答案库。旧三单元候选保留其 Source refs、版本、历史证据和限制；正常继续无需再做一次 asset-only 盲恢复。

用户主动要求训练时另行定义小范围和证据语义；不创建默认训练计划。没有学习者作答时不宣称用户掌握或失败。
