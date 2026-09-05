# Paper Reading Lab

通过持续阅读 AI 的高质量逐句分析，学习如何根据已有信息作出有依据的判断。

AI 负责讲清对象、线索、必要前提和推导连接；用户可以继续读、反复看或主动追问。默认不出题、不要求回忆或预测、不评分，也不以用户作答作为阅读或交付的门槛。清楚易懂不等于已经证明能力提升。

## 怎么用

```text
@github-mcp @reading-mcp

继续 liqiangcc/paper-reading-lab Issue #N 的逐句分析。
```

日常只有一条路径：

```text
恢复必要状态 → 读取当前原文 → 讲清分析 → 等待下一句
```

“停止”表示本句结束，不是要求换新会话。同一会话可以持续阅读；暂停、自然段落结束或需要交接时保存简短状态。原文出错或将越过已授权范围时才处理阻塞，不为每句话启动验收项目。

## 规则放在哪里

- [AGENTS.md](AGENTS.md)：Agent 入口和必要边界。
- [逐句分析协议](docs/learning/source-first-sentence-reading.md)：唯一的日常分析质量标准。
- [Reading Skill](.agents/skills/source-first-reading/SKILL.md)：读取、解释和保存的操作步骤。
- [阅读状态](docs/learning/reading-sessions.md)：一个可恢复记录，不保存整段聊天。
- [文档导航](docs/README.md)：工具细节、工程维护和历史证据按需查阅。

reading-mcp 提供真实原文与精确定位；GitHub 保存规则和进度。AI 分析不替代原文，不使用未揭示后文，不擅自切换论文版本。

## 验证边界

CI 检查仓库文件和链接，不证明分析正确或用户已经掌握。分析质量在真实阅读中检查：是否误读、是否跳步、依据是否清楚、是否有多余负担；发现具体问题就修正，不另设常规测试流水线。

旧 Pilot、Profile v0.1、实验记录保留为历史证据，不是今天继续阅读的前置清单。新默认分析契约为 `source-first-analysis/v1`；旧 Session 的规则绑定须显式切换，不能改写历史。
