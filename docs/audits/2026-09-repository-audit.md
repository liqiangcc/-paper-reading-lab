# 2026-09 全仓库一致性审查

## 范围

审查基线：

```text
main = aa20d2066c754f3cec11a9f1c48a6852b6215f13
```

覆盖：

- 根级 README / AGENTS；
- `.agents/skills/source-first-reading`；
- architecture / domain / integration / source / learning / workflow / validation / pilot 文档；
- Kafka / Raft Primary Issue 的 control-plane 状态；
- 已合并 Profile / governance work；
- Markdown link、Skill front matter、invariant id、required-file 等基础校验。

本审查不继续 reveal Kafka / Raft Source，不修改 `reading-mcp`，不把历史 finding 改写成成功。

## 总体结论

仓库核心机制已经由真实 Pilot 支持，但多轮修复分别落在不同文档和 PR 后，出现了典型的跨文档模型漂移：

```text
workflow 已 harden
+
Profile 已加入
+
AGENTS / Skill 已加入

但

root overview / domain / adapter / source policy
没有同步成为同一套当前模型
```

本轮以“稳定入口、领域一致、Source Adapter 边界、动态状态归属、轻量自动检查”为主线修复。

## Finding 1 — 稳定文档承担了瞬时 live state

### 现象

静态 README / docs navigation 曾持续写入：

- 当前正在执行哪个 Paper / Issue；
- 下一步是某个具体 Session；
- 已完成 Pilot 阶段仍被描述为未来动作。

### 风险

```text
Issue comments 已推进
但 README 未同步
→ fresh worker 从静态文档恢复错误 current state
```

### 修复

- 根 README 改为稳定仓库入口与方法概览；
- `docs/README.md` 只保存 canonical navigation；
- 明确当前 live state 必须读取对应 Issue 的最新 durable record；
- Pilot 历史状态进入独立 closure 文档。

## Finding 2 — Domain model 未同步 workflow hardening

workflow 已加入：

- `planned_scope`；
- `current_scope_boundary`；
- scope amendment；
- Operational Recovery Checkpoint；
- ReadingSession Learning Artifact；
- Explanation Profile；
- stop boundary。

旧 `docs/domain/model.md` 仍主要表达早期 Paper / Session / checkpoint 模型。

### 修复

Domain model 统一为：

```text
Paper
PaperRevision
ReadingSourceBinding
SourceUnitRef
ExplanationProfileRef
ReadingSession
ScopeAmendment
ReadingStep
OperationalRecoveryCheckpoint
ReadingSessionLearningArtifact
PredictionRecord
KnowledgeGap / ReasoningGap
TrainingResult
ExportCandidate
```

并明确：

```text
Paper identity
≠ Revision identity
≠ provider document identity
≠ Session identity
≠ Issue identity
```

## Finding 3 — ReadingSession 仍使用早期单一 `scope / checkpoint` 语义

### 风险

```text
planned_scope = history
current_scope_boundary = executable gate
```

如果两者不分开，Agent 可能把原计划覆盖，或在 reveal 后才补范围。

单一 checkpoint 还会把“恢复下一动作”和“恢复学习模型”混在一起。

### 修复

`docs/learning/reading-sessions.md` 统一为：

- planned scope / executable boundary；
- reveal 前 scope gate；
- durable scope amendment；
- Profile version binding；
- Operational Recovery Checkpoint；
- ReadingSession Learning Artifact；
- Source / Derived / Unknown；
- explicit stop boundary。

## Finding 4 — reading-mcp integration 落后于已验证能力

早期 adapter 文档没有完整覆盖后来在真实 Raft / Kafka 路径中验证的：

- structure-only named-section hierarchy；
- no-body boundary preflight；
- original source view；
- canonical unit 可能包含多个 surface sentences；
- current capability 必须实际 invocation；
- lexical search 可能造成 future-body leakage。

### 修复

`docs/integrations/reading-mcp.md` 更新为：

```text
structure-only boundary
→ persist executable scope
→ canonical exactly-one reveal
→ exact locator re-read
→ optional current-source visual fidelity
→ stop
```

并明确 stale / search / visual / retry 边界。

## Finding 5 — Source policy 未同步视觉 Source 与安全 boundary evidence

### 修复

`docs/source/source-policy.md` 增加：

- raw / normalized / OCR / original source view 身份分离；
- visual observation 与 text Source Fact 分离；
- named-section boundary 只允许 structure-only metadata 或预验证 artifact；
- lexical future snippet 不能作为 clean no-lookahead preflight；
- public repo 优先持久化 locator，而不是全文。

## Finding 6 — AGENTS / Bootstrap / Skill 重复度过高

初版治理正确建立了三层，但 Skill / bootstrap 重复较多 canonical protocol prose。

### 风险

```text
同一规则存在多份
→ 后续只改其中一份
→ governance drift
```

### 修复

```text
AGENTS.md
= routing + hard invariants

conversation-bootstrap.md
= live-state recovery algorithm

source-first-reading/SKILL.md
= one bounded action procedure

canonical docs
= detailed method truth
```

Skill 保留执行步骤和 failure conditions，减少领域定义复制。

## Finding 7 — Pilot 计划与 closure 混在一起

`first-pilot.md` 同时像原始计划又像当前入口，容易把旧范围和 next action 理解成 live state。

### 修复

- `first-pilot.md` 改为明确 historical execution protocol；
- 新增 `first-pilot-closure.md`；
- 保留 PASS / PARTIAL / FAIL matrix、scope drift、checkpoint limitation、Issue drift 和 completed hardening；
- 不改写原 Pilot 历史。

## Finding 8 — Primary Issue body 落后于 durable comments

### Kafka #2

旧 body 仍描述 Source acquisition / Session A 起点；最新 durable state 已经是：

- first Pilot closure completed with findings；
- workflow hardening completed；
- Profile acceptance completed；
- current locator 已推进；
- acceptance one-unit scope consumed；
- next SourceUnit 需要新的显式 authorization。

### Raft #1

旧 body 仍描述 waiting for Source binding；最新 durable state已经是：

- earlier contaminated Session abandoned；
- named-section boundary gap fixed upstream；
- fresh strict Session A active on new normalized identity；
- Introduction SourceUnits 1–4 revealed；
- current boundary remains Section 1 only。

### 修复

两个 Primary Issue body 已重写为：

```text
stable Paper / Revision identity
current durable summary
historical warning
where to find latest checkpoint
current allowed next action
```

完整历史继续保留在 comments。

## Finding 9 — 缺少最小 repository consistency gate

多轮合并后已真实出现：

- 导航和 current-state 漂移；
- canonical docs 新增但旧入口未同步；
- domain / workflow terminology 不一致；
- concurrent docs PR 对同一 README 有重叠风险。

### 修复

新增：

```text
scripts/validate_repository.py
.github/workflows/repository-consistency.yml
```

只检查确定性结构事实：

- required files；
- Markdown local links；
- Skill front matter；
- duplicate invariant ids；
- canonical navigation entries；
- trailing whitespace / code fence；
- stable docs 中明显旧 live-state 文案。

不进行：

- LLM-as-judge；
- 内容真值评分；
- Source identity 替代；
- 自动 Session schema migration。

## Finding 10 — 合并后 topic branches 仍存在

已合并 Profile / governance topic branches 在远端仍可见。

当前 MCP surface 没有删除 Git ref 的写操作，本轮不使用未授权 shell/API 绕过。它们是非阻塞 hygiene finding；后续由具备 branch-delete capability 的维护动作清理。

## 未修改的历史事实

以下内容继续保留：

- Kafka Pilot scope discipline = FAIL；
- Recall / Reconstruction = PARTIAL；
- transient runtime / serialization finding；
- Raft 第一个 strict Session 因 boundary-preflight lookahead contamination 被 abandoned；
- Profile v0.1 fresh acceptance 是真实 L2 fixture，不单独证明所有 depth class。

## Validation result

在审查分支的 fresh clone 中实际执行：

```text
python3 -m py_compile scripts/validate_repository.py
python3 scripts/validate_repository.py
```

结果：

```text
repository consistency validation: PASS
```

检查覆盖当前 Markdown local links、required governance files、Skill front matter、invariant ids、navigation、formatting 和禁止的明显旧 live-state literal。

GitHub Actions 在 PR 上再次运行同一检查。

## 人工 review 重点

1. stable docs 不再承载瞬时 Session state；
2. Domain / Session / lifecycle / Issue 术语一致；
3. Skill 没有扩大 Source visibility；
4. Primary Issue body 与 latest comments 不冲突；
5. Pilot history 没有被重写；
6. lightweight validator 没有演变成复杂 automation。

## Completion 语义

本审查完成表示：

```text
截至该 Candidate SHA
canonical docs / Agent entry / Issue control summary
重新对齐
+
基础结构 drift 有自动检查
```

不表示：

- 所有论文已读完；
- 所有 Session mode 已充分验证；
- reading-mcp 全部格式无缺陷；
- 仓库永远不再需要审查。
