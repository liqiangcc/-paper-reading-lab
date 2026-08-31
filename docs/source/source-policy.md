# Source Policy

## 目的

Paper Reading Lab 需要忠实依赖论文原文，但“能够阅读论文”不等于“应该把完整论文复制进 Git 仓库”。

本仓库默认按公开仓库治理，因此 Source policy 同时关注：

- 来源身份
- 版本关系
- 可重复定位
- 转换质量
- 版权与公开分发边界

本文件是仓库工程策略，不构成法律意见。

## 基本原则

```text
能够定位原文
≠
必须保存完整原文到 Git
```

优先保存：

- Paper metadata
- DOI / canonical identifier
- 官方、作者或机构来源 URL
- 版本说明
- section / page / paragraph / sentence locator
- 必要且克制的短引用
- 自己生成的 Derived 阅读记录

## Source 优先级

在可用时优先：

1. 出版方官方页面 / 官方 PDF
2. 作者主页或作者明确提供版本
3. 大学 / 研究机构仓库
4. 会议 / 学会官方归档
5. 其他能够强验证身份与完整性的镜像

搜索摘要、博客、二手笔记不能替代完整 Source。

## PaperRevision 必须显式

同一论文可能存在：

- preprint
- author manuscript
- conference paper
- journal extension
- publisher version
- corrected version

阅读时必须知道当前绑定哪一个 revision。

不能因为标题相同就自动认为：

```text
所有版本逐句完全一致
```

## 完整 PDF / 全文

### 可以进入 Git 的情况

只有在权利状态明确允许仓库公开分发时，例如：

- 明确开放许可证允许再分发
- 公有领域
- 用户自己拥有并明确授权公开提交的材料
- 其他已经确认允许公开仓库保存的情况

仍应记录来源和许可证信息。

### 默认不进入 Git 的情况

如果许可证或权利状态不明确，不提交：

- 完整 PDF
- 完整 HTML dump
- 全文 Markdown 转换
- 大规模逐句复制的全文镜像

可以在本地工作区、合法连接器或外部来源中读取，然后只在 Git 中保存定位信息和 Derived 学习资产。

## 引用策略

为了支持逐句学习，Session 可能需要显示当前原文句子。

仓库持久化时遵循：

```text
最少必要引用
+
准确 locator
+
Derived 解释
```

不要为了方便恢复 Session 而把整篇论文逐句复制进公开仓库。

如果一个 Pilot 需要完整文本才能自动恢复，应优先设计：

- 外部 Source locator
- 本地不入 Git 的缓存
- connector reference
- content fingerprint

而不是降低 Source policy。

## Source locator

建议尽量组合：

```text
canonical URL
revision id
section title
published page
pdf page
paragraph order
sentence order
figure/table/equation id
```

目标是让另一个阅读会话能够重新打开合法 Source 并定位同一位置。

## 转换文本

PDF → text / Markdown 属于 Source projection，不自动等于 Raw Source。

必须记录：

- 转换工具
- 转换日期或版本
- 页码是否保留
- 多栏排版是否正确
- 公式是否损坏
- 图表是否缺失
- 脚注 / 页眉 / 参考文献是否混入正文

转换文本可以用于导航和 SentenceUnit segmentation，但高风险语义应回到可视原文确认。

## OCR

OCR 永远属于 Derived projection。

即使 OCR 经过人工 fidelity review，也不能把 OCR 字节提升成原始扫描页本身。

结构：

```text
Raw image / scanned page
        ↓
OCR projection
        ↓
segmentation
        ↓
reading
```

## 公式、图表与特殊结构

论文思路不只存在于自然语言句子。

遇到：

- equation
- figure
- table
- algorithm
- pseudocode
- footnote

可以创建专门 SourceUnit 或 locator。

不要为了坚持“逐句”而忽略真正承载论证的图或公式。

原则是：

```text
逐句是默认学习粒度，
Source 真实结构优先于机械文本格式。
```

## Source 完整性限制

以下问题必须显式记录：

- 页面缺失
- 只能访问片段
- 图表不可读
- 公式转换损坏
- 版本关系不确定
- 出版页码与 PDF 页码不一致
- 当前 Source 以后可能失效

如果这些问题影响当前阅读可靠性，Source 状态应保持 `blocked` 或 `source-review`。

## 不允许的补全

禁止：

```text
缺一句 → AI 按上下文补一句
缺公式 → AI 猜作者公式
图看不清 → 用二手博客描述当原图
版本不确定 → 默认最方便的版本就是正式版
```

AI 可以给出恢复建议，但不能把重建内容登记为 Source truth。

## 与 Derived 的关系

Source 只回答：

> 作者在这个 revision 的这个位置实际呈现了什么？

Derived 才回答：

> 我们如何理解它？它和前文是什么关系？为什么重要？

两者必须始终可以分开审计。

## 核心不变量

```text
Source 可追溯优先于 Source 大量复制。
版本身份必须显式。
公开仓库默认不镜像权利状态不明确的全文。
OCR / 转换文本不自动等于 Raw Source。
高风险语义可以回到可视原文复核。
AI 不补造缺失 Source。
```
