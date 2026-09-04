# 架构边界

## 目的

Paper Reading Lab 只在职责边界清楚时才有可信的 Source-first 学习记录。

本仓库不能同时充当：

- 论文下载器；
- PDF 解析器；
- Source truth；
- 完整聊天数据库；
- 最终知识仓库；
- Agent runtime；
- 自动评分系统。

当前架构把这些职责分开。

## 总体关系

```text
Authoritative paper / approved PaperRevision
                ↓
          reading-mcp
                ↓
canonical structure / SourceUnit / TextLocator / source view
                ↓
       paper-reading-lab
                ↓
ReadingSession / checkpoint / reasoning finding / training result
                ↓
          ExportCandidate
                ↓
     target repository gate
                ↓
       validated knowledge
```

控制面独立存在：

```text
GitHub Primary Paper Issue
→ Source binding / Session summary / blocker / handoff / next_action
```

## `reading-mcp` 的职责

`reading-mcp` 是首选 Source Adapter，负责：

- 打开批准的本地或 HTTPS 文档；
- 计算和返回 document / content / normalized identity；
- 提供 canonical section hierarchy；
- 在支持时提供 structure-only named-section boundary；
- 枚举 canonical Paragraph / Sentence SourceUnit；
- 返回 precise `TextLocator`；
- 对 locator 做 exact re-read；
- 在 identity 变化时返回 stale，而不是 fuzzy rebase；
- 渲染 locator 绑定的 original source page 用于 fidelity review；
- 暴露 source-preserving degradation 和 parsing limitation。

`reading-mcp` 不负责：

- 判断当前 Paper 的学习目标；
- 选择 Session mode；
- 决定 planned scope；
- 记录 prediction / recall / reconstruction；
- 保存长期 learning artifact；
- 把 AI 解释升级为作者事实；
- 管理 GitHub Task / PR 生命周期。

## `paper-reading-lab` 的职责

本仓库负责：

- `Paper` 与 `PaperRevision` identity；
- `PaperRevision ↔ reading-mcp document` binding；
- Source readiness / segmentation readiness 的治理状态；
- ReadingSession mode、scope、lookahead policy 和 lifecycle；
- `planned_scope` 与 `current_scope_boundary`；
- no-lookahead reveal gate；
- ReadingStep、current problem model 和 reasoning links；
- Operational Recovery Checkpoint；
- ReadingSession Learning Artifact；
- Explanation Profile；
- Prediction-before-reveal；
- Recall / Reconstruction / Transfer / Retrospective；
- knowledge gap / reasoning gap；
- Pilot retrospective；
- ExportCandidate 与下游 gate 的关系。

本仓库不负责平行生成自己的 Sentence identity。正式 `SourceUnitRef` 必须优先引用 Source provider identity。

## GitHub Issue 的职责

### Primary Paper Issue

默认：

```text
1 Paper
→ 1 Primary Paper Issue
```

它是长期控制面，负责：

- Paper / Revision 摘要；
- Source binding；
- 当前和历史 ReadingSession 的可操作摘要；
- blocker / finding；
- scope amendment；
- checkpoint / artifact reference；
- 唯一或明确的 next action。

它不是：

- 论文全文；
- canonical Source；
- 每句长篇解释 transcript；
- 完整 learning database；
- Paper identity 本身。

### Task / Bug Issue

Source recovery、adapter defect、workflow hardening、Profile、Validator、governance 等具有独立边界的工作可以创建可关闭 Task / Bug Issue。

Task Issue 不能取代 Primary Paper Issue。

## `AGENTS.md`、Bootstrap、Skill 与 canonical docs

```text
AGENTS.md
= repository routing + tool boundary + hard invariants

docs/workflows/conversation-bootstrap.md
= thin prompt → live state → Skill → next_action 的恢复算法

.agents/skills/source-first-reading/SKILL.md
= source-first ReadingSession 的有界执行程序

canonical docs
= method / domain / lifecycle / invariant truth
```

边界要求：

- `AGENTS.md` 保持 pointer 与硬约束，不复制完整方法论；
- Bootstrap 不保存具体 Paper locator；
- Skill 不平行定义领域模型；
- 动态 Session state 不写死在 Skill；
- canonical docs 不承担实时调度状态；
- Thin Prompt 只负责寻址。

## Explanation Profile 的职责

Explanation Profile 规定**已经 canonical reveal 的当前 SourceUnit如何解释和呈现**。

它可以规定：

- 原文 / 翻译 / 关系 / 增量的顺序；
- Source Fact / Derived Interpretation / Unknown 的边界；
- reasoning arrow 可追溯性；
- L0 / L1 / L2 自适应解释深度；
- locator 与 stop boundary 的呈现。

它不能：

- 扩大当前 Source 可见范围；
- 允许读取未来 Source；
- 改写 PaperRevision；
- 替代 Source-first protocol；
- 把历史 Session 静默切换到新 Profile version。

## Checkpoint 与 Learning Artifact

### Operational Recovery Checkpoint

回答：

```text
当前绑定什么 Source？
允许读到哪里？
已经 reveal 到哪里？
唯一下一动作是什么？
```

### ReadingSession Learning Artifact

回答：

```text
这一 Session 建立了哪些 reasoning links？
当前问题模型如何变化？
哪些知识或推理连接不稳定？
Recall / Reconstruction 表现如何？
```

因此：

```text
Operational Recovery Checkpoint
≠ ReadingSession Learning Artifact
≠ Primary Issue summary
≠ full transcript
```

## Raw Source、Projection 与 Original Source View

```text
Raw / authoritative source
→ 发布者原始 PDF / HTML / manuscript

Normalized text
→ 供结构化阅读的 projection

Original source view
→ locator 绑定的原始页面视觉证据
```

Normalized text 适合顺序 reveal，但不自动证明：

- 多栏视觉顺序；
- Figure / Table 空间关系；
- Equation 排版；
- 页脚 / 脚注归属。

遇到视觉语义时应回到 original source view；但看到整页不授权使用尚未 canonical reveal 的未来正文。

## 下游知识仓库边界

Reading finding 仍属于学习层：

```text
Source-grounded observation
+
Derived interpretation
        ↓
ExportCandidate
        ↓
explicit review
        ↓
target repository gate
        ↓
validated knowledge
```

下游仓库可以拒绝、修正或重新组织 ExportCandidate，但不能反写论文原文或历史 Session 当时看到的 Source。

## 首次阅读与 Retrospective

```text
first-pass no-lookahead
= past + current Source only

retrospective
= 已知后文后显式回顾
```

两者必须分开。已经发生 future Source contamination 的 Session 不能继续伪装成 clean first-pass。

## 不属于当前仓库的能力

- 通用 Agent 调度 / Worker registry；
- 浏览器或终端 runtime；
- PDF parser 实现；
- OCR 引擎；
- GitHub provider 本身；
- 自动真值判定；
- 自动风格审美评分；
- 通用知识图谱；
- 未经 review 的跨仓库自动发布。

## 核心不变量

```text
reading-mcp 是 paper Source truth。
paper-reading-lab 是学习与 Session 层。
GitHub Issue 是控制面。
AGENTS / Bootstrap / Skill 是执行入口，不是 Source。
Explanation Profile 不能扩大 Source 可见范围。
Checkpoint 与 Learning Artifact 分工不同。
Reading finding 不自动成为正式知识。
工具或 identity 冲突时 fail closed。
```
