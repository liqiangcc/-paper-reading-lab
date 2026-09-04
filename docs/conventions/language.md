# 语言与命名约定

## 目的

Paper Reading Lab 的人类文档以中文为主，同时保留稳定、可跨工具和跨仓库引用的英文 machine identity。

## 人类文档

默认使用中文：

- README；
- workflow / lifecycle / audit 文档；
- Issue body / durable summary；
- 学习解释；
- retrospective / finding。

技术术语首次出现时可以保留英文，例如：

```text
planned_scope（计划范围）
current_scope_boundary（当前可执行边界）
SourceUnitRef
Operational Recovery Checkpoint
ReadingSession Learning Artifact
```

后续保持同一术语，不在同一文档中随意切换多个译法。

## Machine identity

稳定 identity 使用英文、ASCII 和可预测格式：

```text
paper_id
revision_id
session_id
profile_id
source_binding_id
artifact_id
```

推荐：

```text
lowercase-kebab-case
```

示例：

```text
kafka-2011-distributed-messaging
kafka-2011-netdb11
source-first-incremental-explanation
```

Machine identity 不使用 Issue title、中文显示名或可变路径替代。

## Source 保持原文

论文原文保持作者发布语言和 wording。

输出顺序通常是：

```text
canonical original
→ faithful Chinese translation
→ explanation
```

翻译不能混入 Derived Interpretation，也不能把现代实现或后文知识写进原句。

## 规范词

方法文档可以使用：

- **MUST**：不满足即违反 contract；
- **SHOULD**：默认遵守，偏离需要理由；
- **MAY**：按当前 Source / Session 选择。

中文正文可以同时解释含义，但 machine-facing 规范词保持一致。

## 状态与 Tag

Durable comment tag 使用稳定英文大写形式，正文可以中文：

```text
[SESSION START]
[SESSION HANDOFF]
[OPERATIONAL RECOVERY CHECKPOINT]
[IMMUTABLE PREDICTION]
[PREDICTION VS ACTUAL]
[SCOPE AMENDMENT]
[BLOCKER]
[ACCEPTANCE RESULT]
[CLOSURE]
```

Tag 只用于导航，不能取代 `session_id`、时间、Source identity 或字段语义。

## Source / Derived / Unknown

正式学习状态中优先使用稳定分类：

```text
Source Fact
Derived Interpretation
Unknown
```

中文解释可写为：

- 原文直接事实；
- 有限推论；
- 当前未知。

但三类语义不得混合。

## 历史论文与现代版本

描述历史论文时保持该 `PaperRevision` 的原始语义。

现代版本对照必须显式标注：

```text
current paper revision
≠ modern implementation / later revision
```

不能使用“现在 Kafka / Raft 是怎样”替代论文当时写了什么。

## 文件与目录命名

仓库路径优先使用稳定英文：

```text
docs/learning/
docs/workflows/
docs/validation/
.agents/skills/source-first-reading/
```

文档标题和正文可使用中文。

新增 Skill 使用标准：

```text
.agents/skills/<skill-name>/SKILL.md
```

front matter 的 `name` 使用英文 machine identity，`description` 说明触发场景与非目标。

## 写作风格

- 先结论，再解释边界；
- 使用短段落和必要箭头；
- 不用大段重复 Prompt 代替 canonical reference；
- 不把静态 README 写成瞬时 live state；
- 不把完整聊天 transcript 写进 Issue；
- 不通过语言强度扩大 Source claim。

特别保留限定词：

```text
may ≠ must
can ≠ always
typically ≠ universally
approximately ≠ exactly
```

## 核心不变量

```text
Human docs 默认中文。
Machine identity 使用稳定英文。
Source wording 保持原文。
翻译与解释分离。
Durable tags 不替代 identity。
术语在同一文档中保持一致。
历史 Revision 与现代实现明确分界。
```
