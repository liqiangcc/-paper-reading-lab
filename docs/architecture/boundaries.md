# 仓库边界

## 目的

本文件定义 Paper Reading Lab 的职责边界，避免逐句阅读、知识沉淀、机制实验、论文存档和 AI 对话记录混成一个系统。

## 本仓库负责什么

Paper Reading Lab 负责“学习过程”。

核心问题是：

> 学习者如何在只看到当前与过去信息的条件下，逐步理解作者的论证、设计和研究思路，并通过反复提取、预测、重建和迁移把这些思路转化为自己的能力？

因此本仓库重点管理：

- Paper identity 与可追溯 Source locator
- Section / Paragraph / SentenceUnit 顺序
- ReadingSession
- revealed position
- 当前句与前文的显式关系
- 当前问题模型的增量更新
- Prediction / Recall / Reconstruction / Transfer 训练
- knowledge gap 与 learner weakness
- 可向下游输出的候选发现

## 本仓库不负责什么

### 不负责永久保存所有论文全文

本仓库默认公开，不把“拥有完整 PDF/全文副本”当作阅读系统的必要条件。

完整论文来源可以通过官方网页、作者主页、机构仓库、合法本地文件或已授权连接器访问。

### 不负责把 AI 对话全文当作知识库

ReadingSession 只沉淀可恢复、可复用的 checkpoint，不保存大量重复 transcript。

### 不负责暴露模型私有 chain-of-thought

学习对象是可观察、可教授的 reasoning structure，例如：

```text
cue
relation
problem
constraint
decision
mechanism
trade-off
evidence
update
```

不是模型不可观察的内部推理轨迹。

### 不负责最终论文知识资产的完成门禁

论文事实、机制链、语义、trade-off、evidence validation、knowledge card 等严格知识资产，由专门知识仓库治理。

### 不负责真实系统机制的实验闭环

运行时实验、raw evidence、claim falsification 和 mechanism learned 状态属于机制实验仓库。

## 与 `classic-papers-system-design` 的分离

`paper-reading-lab` 的核心状态是：

```text
我读到哪里？
当前理解是什么？
当前能够预测什么？
哪些思维连接还不稳定？
```

`classic-papers-system-design` 的核心状态是：

```text
哪些论文事实已经复核？
哪些分析已经独立 review？
哪些结论达到知识资产门禁？
```

因此：

```text
ReadingSession completed
≠
Paper analysis reviewed
≠
Knowledge asset done
```

阅读时产生的 finding 只能作为候选输入：

```text
Reading finding
    ↓
显式 export / review
    ↓
classic-papers-system-design 中的正式事实或分析
```

不得因为 ReadingSession 中 AI 给出了一个漂亮解释，就直接升级成正式论文结论。

## 与 `systems-mechanism-lab` 的分离

阅读论文可能产生机制问题：

```text
作者声称机制 M 具有性质 P
```

这仍然只是论文语境中的 source claim 或阅读发现。

如果需要回答：

> 在当前真实系统中 M 到底怎样运行？P 是否能被观察或证伪？

应进入 `systems-mechanism-lab`：

```text
paper reading
→ mechanism question
→ hypothesis
→ experiment
→ raw evidence
→ observation / inference
→ claim update
```

Paper Reading Lab 不把“作者写了什么”自动转换成“现实系统永远如此”。

## Source 与 Derived 边界

### Source

Source 层只保存或引用来源本身可以证明的内容：

- 论文身份
- 版本
- 来源位置
- section / page / paragraph locator
- 原始句子或允许范围内的短引用
- 图表 / 公式 locator

### Derived

以下全部属于 Derived：

- 句子切分结果
- 语义解释
- 句间关系
- 问题树
- 推理结构
- 预测
- 作者意图判断
- 设计 rationale
- trade-off 分析
- 回顾总结
- 学习者表现

Derived 可以修改、深化或推翻；Source 事实不能因为 Derived 变化而被悄悄改写。

## 首次阅读与回顾阅读边界

首次顺序阅读必须满足：

```text
past + current only
```

已经读完整篇后的第二遍，可以使用全文，但必须标记为：

```text
retrospective
```

不能把“知道结局后的解释”伪装成“当时只看到这里就能得出的判断”。

## 预测与作者事实的边界

Prediction 记录的是学习者或 AI 在当前信息下认为“下一步合理可能是什么”。

它不是作者事实。

必须区分：

```text
predicted direction
actual next source
comparison
```

预测失败也有学习价值，因为它暴露当前问题模型和作者模型之间的差异。

## 生命周期边界

可以完成的是：

- 一个 ReadingSession
- 一次 Section pass
- 一次 Recall test
- 一次 Reconstruction
- 一次 Transfer exercise

不能永久完成的是：

- “这篇论文已经没有继续学习价值”

新知识、新目标、新版本、新问题都可以触发下一次阅读。

## 核心不变量

```text
Source 不被 Derived 覆盖。
首次阅读不读取未来。
阅读完成不等于知识资产完成。
论文 claim 不等于现实系统 claim。
Prediction 不等于作者事实。
AI transcript 不等于学习资产。
可恢复 checkpoint 比完整聊天记录更重要。
```
