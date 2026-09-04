# Paper Reading Lab

Paper Reading Lab 是一个以 **稳定论文原文、可恢复 ReadingSession 和显式推理训练** 为核心的实验仓库。

它不把“读过一篇论文”视为一次性完成状态，而是把同一篇论文上的不同学习活动分开治理：

```text
Paper / PaperRevision
        ↓
Stable Source binding
        ↓
ReadingSession
        ├── Learning
        ├── Prediction
        ├── Recall
        ├── Reconstruction
        ├── Transfer
        └── Retrospective
```

仓库的目标不是保存大量论文摘要，而是验证并固化以下链路：

```text
稳定 Source
→ source-first / no-lookahead reveal
→ 当前问题模型增量更新
→ durable checkpoint
→ fresh-conversation recovery
→ Prediction before reveal
→ Recall / Reconstruction
→ mechanism finding
→ explicit review / export
```

## 核心边界

```text
reading-mcp
= 论文 Source、canonical structure、SourceUnit、TextLocator、original source view

paper-reading-lab
= PaperRevision binding、ReadingSession、学习协议、checkpoint、reasoning finding

GitHub Issue
= 长期控制面、blocker、handoff、next action

下游知识仓库
= 经独立 gate 审核后的正式知识资产
```

因此：

- Issue comment 不是论文 Source；
- AI 解释不是作者原文；
- ReadingCheckpoint 不是完整 transcript；
- Session completed 不等于 Paper done；
- `reading_document_id` 不替代 `revision_id`；
- 历史 Session 不因 Source 或 Profile 更新而被静默改写。

## Agent / fresh-conversation 入口

仓库支持薄入口：Prompt 只负责指向目标，完整规则和动态状态由仓库与 GitHub durable state 提供。

```text
@github-mcp @reading-mcp

接管 liqiangcc/paper-reading-lab Issue #N。
读取 AGENTS.md，并按仓库治理从 live state 恢复后执行；
完成或 blocked 后持久化并停止。
```

Agent 进入仓库后按以下路径恢复：

```text
AGENTS.md
→ target Issue live state + comments
→ docs/workflows/conversation-bootstrap.md
→ applicable Skill
→ canonical method docs
→ checkpoint / handoff / scope / next_action
→ reading-mcp Source
→ bounded action
→ durable result
→ STOP
```

关键入口：

- [`AGENTS.md`](AGENTS.md)：仓库级 Agent 规则、工具边界、路由和 fail-closed 不变量；
- [`docs/workflows/conversation-bootstrap.md`](docs/workflows/conversation-bootstrap.md)：fresh conversation 的统一恢复算法；
- [`.agents/skills/source-first-reading/SKILL.md`](.agents/skills/source-first-reading/SKILL.md)：逐句阅读、下一句、resume 和当前 Source fidelity review 的执行 Skill；
- [`docs/README.md`](docs/README.md)：完整文档导航。

## Source-first 逐句阅读

首次顺序阅读处于位置 `N` 时，只允许使用：

```text
已揭示 SourceUnit 1..N-1
+
当前 SourceUnit N
+
Session 明确允许的既有背景知识
```

禁止使用同一论文尚未 reveal 的未来正文解释当前位置。

默认 ReadingStep：

```text
scope gate
→ exactly one canonical SourceUnit
→ precise locator re-read
→ 原文 / 忠实翻译
→ 与已揭示前文的关系
→ 当前真实认知增量
→ Source Fact / Derived Interpretation / Unknown
→ current problem model update
→ locator + stop boundary
→ STOP
```

详细协议：

- [`docs/learning/source-first-sentence-reading.md`](docs/learning/source-first-sentence-reading.md)
- [`docs/learning/incremental-explanation-profile.md`](docs/learning/incremental-explanation-profile.md)
- [`docs/learning/reading-sessions.md`](docs/learning/reading-sessions.md)

## Session 与 scope

每个 ReadingSession 必须有明确边界。

```text
planned_scope
= Session 创建时的历史计划

current_scope_boundary
= 当前真正允许 reveal 的可执行边界
```

每次 reveal 前都必须检查边界：

```text
next canonical unit inside current_scope_boundary?
├── yes → reveal allowed
└── no  → STOP before reveal
          → durable scope amendment required
```

scope amendment 只能改变后续允许范围，不能覆盖原 `planned_scope` 历史。

## Durable state

仓库区分两种不同目标的持久化状态：

### Operational Recovery Checkpoint

用于让 fresh conversation 安全续作，至少恢复：

```text
Paper / Revision / Source identity
Session mode / lookahead policy
planned_scope / current_scope_boundary
revealed_position / precise locator
bound Explanation Profile
immutable prediction reference（如有）
blocker / finding
exactly one next action
```

### ReadingSession Learning Artifact

用于支持 Recall / Reconstruction / retrospective，保留：

```text
revealed range
explicit reasoning links
current problem model / model updates
knowledge gaps / reasoning gaps
cue level
prediction / reconstruction findings
```

两者都应明显小于完整聊天 transcript。

## 领域对象

当前主要对象：

```text
Paper
PaperRevision
ReadingSourceBinding
SourceUnitRef
ReadingSession
ReadingStep
OperationalRecoveryCheckpoint
ReadingSessionLearningArtifact
ExplanationProfileRef
KnowledgeGap
ExportCandidate
```

详见 [`docs/domain/model.md`](docs/domain/model.md)。

## Issue 驱动

默认关系：

```text
1 Paper
↕
1 Primary Paper Issue

1 Paper
↕
N ReadingSessions
```

Primary Issue 长期保持为入口，负责 Source binding、Session summary、blocker、handoff 和 next action；它不保存论文全文或每一句长解释。

独立的 Source recovery、workflow hardening、adapter defect、Profile、Validator 等工作可创建可关闭的 Task / Bug Issue。

详见 [`docs/workflows/issue-driven-workflow.md`](docs/workflows/issue-driven-workflow.md)。

## 文档结构

```text
.
├── AGENTS.md
├── .agents/skills/
├── docs/
│   ├── architecture/
│   ├── conventions/
│   ├── domain/
│   ├── integrations/
│   ├── learning/
│   ├── pilot/
│   ├── source/
│   ├── validation/
│   └── workflows/
└── scripts/
```

文档推荐阅读顺序见 [`docs/README.md`](docs/README.md)。

## 已验证机制

首个 Kafka 2011 Pilot 已实际覆盖：

- stable PaperRevision / reading-mcp binding；
- canonical SourceUnit sequential reveal；
- precise TextLocator re-read；
- no-lookahead 与 fail-closed；
- cross-conversation checkpoint recovery；
- Prediction-before-reveal 与 Prediction-vs-Actual；
- Recall / Reconstruction 的部分验证；
- Figure original-source fidelity；
- scope drift、checkpoint 信息密度与 runtime binding 等真实 finding。

历史 Pilot 的计划、证据和 closure 见：

- [`docs/pilot/first-pilot.md`](docs/pilot/first-pilot.md)
- [`docs/pilot/first-pilot-closure.md`](docs/pilot/first-pilot-closure.md)

当前 Paper / Session 的实际状态始终以对应 GitHub Issue 的最新 durable record 为准；静态 README 不承担实时调度状态。

## 校验

仓库提供轻量一致性检查：

```bash
python3 scripts/validate_repository.py
```

检查范围包括：

- 必需治理文件；
- Markdown 本地链接；
- Skill front matter；
- invariant id 唯一性；
- 文档导航中的 canonical entry；
- 不允许重新出现的明显静态入口漂移。

它不尝试自动评判解释质量，也不替代 reading-mcp Source identity 或人工 review。

## 核心不变量

```text
Source status 与 Session status 分离。
Source Fact 与 Derived Interpretation 分离。
未来 Source 不提前供应。
revealed_position 单调向前。
scope 在 reveal 前检查。
stale locator / revision conflict fail closed。
Prediction 先于 actual reveal。
Profile 版本不能静默切换。
Issue 是 control plane，不是 Source truth。
Session completed 不等于 Paper done。
Reading finding 不自动升级为正式知识。
```
