# Issue 驱动工作流

## 日常阅读

一篇论文一个 Primary Issue；一次“下一句”不建新 Issue、不建 PR、不重复 claim。正文保存论文/Source 摘要及当前完整 `[READING STATE]` 的指针。状态内容见 [阅读状态](../learning/reading-sessions.md)，分析质量见 [分析协议](../learning/source-first-sentence-reading.md)。

同一会话连续阅读，必要状态在内存中更新；自然边界、暂停、交接、范围改变或故障时持久化。没有变化不写重复 handoff/blocker。旧评论和 Pilot 记录只作历史，不能成为新任务的自动授权。

## 恢复与并发

先读 Issue body、current-state 指针和当前 comment 数，再选择性取状态与较新控制记录，排除 superseding update；不要默认 `perPage=100` 全量加载。不能把“最新一条 comment”硬编码成永远是某个 entry，也不固定 comment 页码。

旧 Issue 没有可靠指针时，选择性检查最新匹配 Session 的 checkpoint/handoff；必要时向前逐条查控制记录。评论可能含未读论文分析，若无法安全区分，先停止由维护动作整理入口，不用答案反推游标。

有别的执行者正在推进、绑定冲突、或无法判断哪份状态有效时不并行覆盖。正常恢复不依赖旧聊天，但允许使用已经授权的分析摘要；这不是必须遮住摘要的盲测。

保存顺序：先追加完整状态 → 更新 body 指针 → 回读。出现正文与较新记录矛盾时保留历史、核对身份和时序；仍不能确定才停止。不能为了减少一次读取而误用陈旧位置。

## 仓库修改

只有具体 Source 故障、重复分析问题或规则/代码修改才建一个有界 Task。普通阅读不套工程流程。

```text
明确修改范围 → 独立分支/PR → 自审或所需 review + CI → 合并及对应检查 → 简短结果
```

不默认为每个 Task 增加独立 fresh conversation、学习者测验或 Profile stable 门禁。Contract 真正需要的测试才执行；通过的固定候选不因换会话重测。分析质量以具体语义问题审查，不用 CI PASS 代替。

## Task closure 证据门禁

此节只用于工程/文档修改，不用于每句阅读。

完成报告记录：base/candidate、PR、实际 review 与该候选检查链接、merge SHA、对应 main 检查、剩余限制、最终状态。自审写自审，review requested 不等于独立批准；没有运行的检查不称 PASS。

未合并为待合并；已合并但必要检查未完成为 `merged-awaiting-verification`。关闭 Task 前回读 body/state/owner，释放 owner，下一动作不能仍指向已完成项。保留历史失败，不把取消需求改成测试成功。

遗留分支、学习者未测、Profile 历史候选状态与当前交付分别处理，不把它们自动变成阻塞。不得为了清理分支扩大权限或用 delete_file 冒充删除 ref。

## 不作为默认流程的内容

不运行预测锁定/揭示对照、Recall、Reconstruction、训练评分、隔离试次或跨仓库知识导出。用户明确要求时才单独界定范围；历史实验保留其证据语义，不能复用成今天的成绩。

GitHub 只保存规则、状态和必要分析摘要，不是 canonical Source。原文缺失不能用旧评论补造，公开仓库不镜像整篇论文。
