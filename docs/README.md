# 文档导航

Paper Reading Lab 当前文档按“先边界、再领域、再学习协议、最后执行与验证”的顺序阅读。

## 推荐阅读顺序

1. [`../README.md`](../README.md)
   - 仓库目标、核心原则、学习模式和整体边界。

2. [`architecture/boundaries.md`](architecture/boundaries.md)
   - 明确本仓库与 `classic-papers-system-design`、`systems-mechanism-lab` 的职责分离。

3. [`domain/model.md`](domain/model.md)
   - 定义 `Paper`、`PaperRevision`、`SentenceUnit`、`ReadingSession`、`ReadingCheckpoint` 等核心对象。

4. [`learning/source-first-sentence-reading.md`](learning/source-first-sentence-reading.md)
   - 定义逐句、累积上下文、no-lookahead 和一层一层解释的核心学习协议。

5. [`learning/reading-sessions.md`](learning/reading-sessions.md)
   - 定义 Learning、Prediction、Recall、Reconstruction、Transfer、Retrospective 等 Session 模式和 checkpoint。

6. [`workflows/paper-reading-lifecycle.md`](workflows/paper-reading-lifecycle.md)
   - 分离 Source 生命周期和 ReadingSession 生命周期，并明确 Paper 不存在永久 `done`。

7. [`source/source-policy.md`](source/source-policy.md)
   - 定义论文版本、来源定位、转换文本、OCR 和公开仓库版权边界。

8. [`validation/invariants.md`](validation/invariants.md)
   - 定义后续 Validator 要保护的关键不变量。

9. [`conventions/language.md`](conventions/language.md)
   - 人类文档默认中文，machine identity 使用稳定英文，Source 保持原文。

10. [`pilot/first-pilot.md`](pilot/first-pilot.md)
    - 定义首个真实逐句阅读 Pilot 的范围、Gate、Session 和成功标准。

## 当前权威入口

当前阶段以下文件构成第一版方法论核心：

```text
README.md
+
docs/architecture/boundaries.md
+
docs/domain/model.md
+
docs/learning/source-first-sentence-reading.md
+
docs/learning/reading-sessions.md
+
docs/workflows/paper-reading-lifecycle.md
+
docs/source/source-policy.md
+
docs/validation/invariants.md
```

`docs/pilot/first-pilot.md` 是当前执行入口。

## 当前不应该继续扩展的内容

在首个 Pilot 以前，暂时不要急着增加：

- 大量 schema
- 自动 sentence segmentation
- 复杂数据库
- 完整知识图谱
- 大量论文目录
- 自动跨仓库同步
- 完整评分系统

这些都应由真实逐句阅读暴露的需求驱动。

## 下一步

```text
选择一篇经典论文
→ 建立稳定 PaperRevision
→ 只准备一个短小节
→ 人工确认 SentenceUnit
→ 执行第一轮 Learning Session
```
