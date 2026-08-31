# 语言规范

## 默认语言

仓库面向人的内容默认使用中文，包括：

- README
- 方法论文档
- ReadingSession checkpoint
- Issue / PR 说明
- 学习总结
- Validator 报错说明
- Pilot 报告

## 保持原文的内容

以下内容不为了中文统一而翻译或改写：

- 论文标题的正式原名
- 作者姓名
- 论文原始句子或短引用
- DOI / URL
- 公式、代码、算法名
- Source 中的专有名词

如果需要中文理解，可以在 Derived 层追加中文解释，但不能覆盖原文。

## Machine identity

稳定机器标识保持英文，例如：

```text
paper_id
revision_id
sentence_unit_id
session_id
revealed_position
learning
prediction
recall
reconstruction
transfer
retrospective
```

原因：

- 稳定
- 便于 schema / script / validator
- 避免中文显示文字变化影响 identity

## 中文术语与英文术语

首次出现重要术语时建议：

```text
中文名称（English Term）
```

后续根据上下文使用中文或稳定英文缩写。

例如：

```text
提取练习（Retrieval Practice）
一致性哈希（Consistent Hashing）
读后回顾模式（Retrospective Mode）
```

## 不翻译 Source 来制造“原文”

中文翻译永远属于 Derived。

必须区分：

```text
Source wording
Derived translation
Derived interpretation
```

不能把 AI 翻译后的中文句子登记成论文原文。

## 推理结构字段

面向机器的节点类型可以保留英文：

```text
problem
constraint
decision
mechanism
trade-off
evidence
boundary
update
```

面向人的解释使用中文。

## Commit message

仓库默认允许中文 commit message，推荐：

```text
docs: 定义逐句阅读协议
docs: 补充 Source 版本边界
fix: 修正 Session revealed position 语义
feat: 增加 ReadingSession Validator
```

前缀保持常见英文约定，说明部分使用中文。

## 核心原则

```text
人读中文。
机器 identity 稳定英文。
论文 Source 保持原文。
翻译与解释都属于 Derived。
```
