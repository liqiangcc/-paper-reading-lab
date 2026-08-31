# 首个逐句阅读 Pilot

## 目的

首个 Pilot 不追求“读完一篇经典论文”，而是验证 Paper Reading Lab 最核心的学习机制是否真实可用。

要证明的是：

```text
稳定 Source
→ 稳定 SentenceUnit
→ no-lookahead 逐句 reveal
→ AI 一层一层解释
→ checkpoint 可恢复
→ Prediction 先于下一句
→ 新 Source 到来后更新判断
→ 第二遍 Recall / Reconstruction
```

如果这条链没有跑通，不扩展论文数量。

## Pilot 范围

第一轮只选择：

```text
1 篇论文
×
1 个适合的短小节
```

建议控制在约：

```text
10–30 个 SentenceUnit
```

具体数量服从自然论证边界，不机械追求句数。

## 论文选择标准

优先选择：

- 经典且长期有价值
- 有稳定官方 / 作者 / 机构 Source
- 版本身份清楚
- 当前小节自然语言论证较完整
- 公式和复杂图表不是主要障碍
- 作者的问题 → 约束 → 设计推进比较清晰
- 后续可以进入 `classic-papers-system-design` 或与其已有论文对应

第一篇不要选择：

- Source 版本关系复杂的论文
- 大量扫描 OCR 的论文
- 主要依赖复杂数学证明的章节
- 当前必须跨很多页才能理解一句的材料

## 候选方向

为了减少 Source 和知识准备成本，优先从已有 `classic-papers-system-design` 覆盖的经典论文中选。

适合的候选包括：

- *MapReduce: Simplified Data Processing on Large Clusters*
- *The Google File System*
- *Dynamo: Amazon's Highly Available Key-value Store*
- *In Search of an Understandable Consensus Algorithm (Raft)*

首个 Pilot 不因为候选列表存在就自动绑定某篇论文；启动时仍需建立正式 `Paper` / `PaperRevision`。

## Pilot Gate 0：Source

开始逐句阅读前确认：

```text
paper_id 已建立
revision_id 已建立
canonical source 可重复访问
版本关系无未解释冲突
目标小节 locator 稳定
```

如果不能满足，先停在 Source workflow。

## Pilot Gate 1：Segmentation

目标小节需要形成有序 Source units：

```text
SectionUnit
→ ParagraphUnit
→ SentenceUnit
```

人工抽查：

- 顺序正确
- 没有多栏串行错误
- 页眉页脚没有混入正文
- 公式没有造成明显错误断句
- 句子可重新定位到原 Source

不要求整个论文一次切完。

## Pilot Session A：Learning

目标：验证“逐句 + 一层一层解释”。

对每个新 SentenceUnit：

```text
1. 只揭示当前句
2. 解释字面
3. 解释与前文关系
4. 识别新增事实 / 约束 / 问题 / 决策
5. 更新当前问题模型
6. 停下
```

不要每句都强制 Prediction。

先确认基础阅读体验自然。

## Pilot Session B：Prediction

在同一小节重新走一遍，但读取下一句前先回答：

```text
当前最合理的下一步问题是什么？
有哪些候选方向？
哪一个约束最可能推动作者继续？
```

然后揭示下一句并记录：

```text
prediction
actual source
差异
缺失的判断
model update
```

重点不是命中率，而是找到自己的思维连接在哪断掉。

## Pilot Session C：Recall

间隔后，只提供部分 cue：

```text
当前问题 / 当前约束 / 当前段落开头
```

测试能否恢复：

```text
为什么作者走到这里？
当前选择解决什么？
下一步的逻辑压力是什么？
```

提示级别必须记录。

## Pilot Session D：Reconstruction

不逐句看论文，尝试重建整个小节：

```text
Problem
→ Constraints
→ Alternatives（如果 Source 支持）
→ Decisions
→ Mechanisms
→ Consequences
→ Evidence / Boundary
```

再回 Source 校正。

## Pilot 要记录什么

只保存可复用 checkpoint，而不是所有聊天内容。

至少记录：

```text
revision
scope
mode
revealed_position
关键 reasoning links
knowledge gaps
prediction findings
reconstruction gaps
no-lookahead 是否保持
```

## Pilot 成功标准

第一轮至少证明：

1. 同一 SentenceUnit 可以跨会话稳定重新定位。
2. 首次阅读没有未来 Source 倒灌。
3. checkpoint 足以在新会话继续。
4. Prediction 确实发生在 reveal 前，而不是事后解释。
5. AI 的输出能够保持“小步”，不会不断自动总结后文。
6. 第二遍学习能明显从“看懂”转向“主动重建”。
7. 至少发现一个具体的 reasoning gap，而不只是记录“这句不会”。
8. Session completed 没有被错误解释成 Paper done。

## Pilot 失败也要保留的 finding

例如：

- 句子粒度过细，破坏自然理解
- 每句都预测导致节奏很差
- checkpoint 太重，维护成本高
- no-lookahead 在工具层无法可靠保证
- Source locator 跨格式不稳定
- AI 过度解释作者意图
- 已有背景知识和未来论文知识边界难区分

这些 finding 应推动修改方法论文档，而不是为了“Pilot PASS”隐藏问题。

## Pilot 后再决定什么

首个 Pilot 完成后再决定：

- 是否需要 Issue-driven 工作流
- 是否需要 schema
- 是否需要自动 Sentence segmentation
- 是否需要 Session 存储文件格式
- 是否需要 Validator 脚本
- 是否需要与 `classic-papers-system-design` 自动 export
- 是否需要支持 reading-mcp / connector 作为 Source provider

先验证学习体验，再工程化。

## 推荐下一步

```text
从已有经典论文中选 1 篇
→ 建立 Paper / PaperRevision
→ 只准备一个短小节
→ 人工确认 SentenceUnit
→ 开始 Session A
```

这是本仓库完成基础文档后的第一项实际工作。
