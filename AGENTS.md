# Agent Working Rules

## 目标

本仓库只提供高质量、低理解摩擦的逐句分析。用户通过持续阅读 AI 的连贯分析逐渐学习分析方法；分析质量由 AI 负责，不给用户设置刻意练习。训练、测验、评分和验收式阅读已移除，不保留可选入口。

## 入口

日常阅读：读取目标 Issue 当前正文及其指向的最新阅读状态，然后使用 [Reading Skill](.agents/skills/source-first-reading/SKILL.md) 和 [分析协议](docs/learning/source-first-sentence-reading.md)。同一会话已经核验的规则不每句重载。

只读取本动作需要的材料。不要默认扫描全部 comments 或整仓库；恢复位置不清时，先检查最新相关控制记录，无法确定才停止。旧 body 缺少可信状态入口时不得猜测。

仓库修改：按 [工程流程](docs/workflows/issue-driven-workflow.md#task-closure-证据门禁) 使用独立分支/PR；不要套用 Reading Skill。维护用的检查和 review 不得成为用户每读一句的操作负担。

## 必须保留的边界

- reading-mcp 是 canonical Source / TextLocator 的来源；schema 和历史成功不等于当前调用成功。
- 分析只使用已揭示前文、当前允许单元和明确允许的背景；不从 Web、下游答案或模型记忆补未来正文。
- 保留论文版本、provider identity、精确 locator、已揭示位置和授权范围；stale / mismatch 不做相似搜索迁移。
- 下一单元越界时先停止并获得范围授权；不能先读再补范围。当前 user 指令可作为授权，Agent 保存即可，不要求用户编辑字段。
- 事实、有限推论、未知必须能区分；不能为了流畅掩盖前提或信息缺口。
- 既有 Source / 分析契约绑定不静默切换；现行契约见分析协议。旧规则按原 commit 查询，不从 main 同路径猜测；历史结果保持原样。
- 一句结束等待下一句，不自动继续；也不因此要求新会话。

## 保存与故障

同一会话记录当前 locator 和模型增量。自然边界、暂停、交接、范围改变或故障时保存一份 [阅读状态](docs/learning/reading-sessions.md)，回读核对；不每句追加 START/RESULT/HANDOFF，不复制完整 transcript。

阻塞时说明具体缺失、保存已知位置和一个可行下一动作。原因未变不要反复追加同一 blocker，也不要反复要求重开会话。不要把问题转成新的隔离试次。

## 修改规则

只围绕用户目标做必要修改，不新增无实际用途的 schema、评分系统或模式流水线。运行现有 unittest/validator，记录真实 candidate/check 结果；未合并或未验证的工作不称已生效。历史 Pilot/实验文档不是当前任务授权。
