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
- 本地 Markdown link、Skill front matter、invariant id、required-file 等基础校验。

本审查不继续 reveal Kafka / Raft Source，不修改 `reading-mcp`，不把历史 finding 改写成成功。

## 总体结论

仓库核心机制已经由真实 Pilot 支持，但多轮修复分别落在不同文档和 PR 后，出现了典型的**跨文档模型漂移**：

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

## Finding 2 — Domain model 未同步真实 workflow hardening

### 现象

workflow 已经加入：

- `planned_scope`；
- `current_scope_boundary`；
- scope amendment；
- Operational Recovery Checkpoint；
- ReadingSession Learning Artifact；
- Explanation Profile；
- stop boundary。

但旧 `docs/domain/model.md` 仍主要表达早期 Paper / Session / checkpoint 模型。

### 修复

重写 domain model，使以下对象和 identity 关系成为 canonical：

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

## Finding 3 — ReadingSession 文档仍使用早期单一 `scope / checkpoint` 语义

### 风险

这会让 Agent 忽略：

```text
planned_scope = history
current_scope_boundary = executable gate
```

也会继续把“能恢复下一动作”和“能恢复完整学习模型”混成一个 checkpoint。

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

### 现象

早期 adapter 文档没有完整覆盖后来在真实 Raft / Kafka 路径中验证的：

- structure-only named-section hierarchy；
- no-body boundary preflight；
- original source view；
- canonical unit 可能包含多个 surface sentences；
- current capability 必须实际 invocation；
- lexical search 可能造成 future-body leakage。

### 修复

更新 `docs/integrations/reading-mcp.md`：

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

- raw / normalized / OCR / original source view 的身份分离；
- visual observation 与 text Source Fact 分离；
- named-section boundary 只允许 structure-only metadata 或预验证 artifact；
- lexical future snippet 不能作为 clean no-lookahead preflight；
- public repo 优先持久化 locator，而不是全文。

## Finding 6 — AGENTS / Bootstrap / Skill 重复度过高

### 现象

初版治理正确建立了三层，但 Skill 和 bootstrap 仍重复较多 canonical protocol 解释。

### 风险

```text
同一规则存在多份 prose
→ 后续只改其中一份
→ governance drift
```

### 修复

三层收敛为：

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

Skill 保留执行步骤和 failure conditions，减少领域定义重复。

## Finding 7 — Pilot 计划与 closure 混在一起

### 现象

`first-pilot.md` 是原始计划 / 历史协议，但缺少一个稳定 closure 入口，读者容易把计划中的旧范围和下一动作理解成当前状态。

### 修复

新增：

```text
docs/pilot/first-pilot-closure.md
```

保留：

- PASS / PARTIAL / FAIL matrix；
- scope drift；
- checkpoint limitation；
- Issue body/comment drift；
- completed hardening；
- `Pilot completed ≠ Paper done`。

不改写原 Pilot 历史。

## Finding 8 — Primary Issue body 落后于 durable comments

### Kafka #2

历史 body 仍描述 Source acquisition / Session A 起点；latest durable state 已经是：

- first Pilot closure completed with findings；
- workflow hardening completed；
- Profile acceptance completed；
- current locator 已推进；
- acceptance one-unit scope consumed；
- next SourceUnit 需要新的显式 authorization。

### Raft #1

历史 body 仍描述 waiting for Source binding；latest durable state 已经是：

- earlier contaminated Session abandoned；
- named-section boundary gap fixed upstream；
- fresh strict Session A active on new normalized identity；
- Introduction SourceUnits 1–4 revealed；
- current boundary remains Section 1 only。

### 修复

重写两个 Primary Issue body 为：

```text
stable Paper / Revision identity
current durable summary
historical warning
where to find latest checkpoint
current allowed next action
```

完整历史仍保留在 comments。

## Finding 9 — 缺少最小 repository consistency gate

### 证据

多轮合并后已经真实出现：

- 导航和当前状态漂移；
- canonical docs 新增但旧入口未同步；
- domain / workflow terminology 不一致；
- concurrent docs PR 对同一 README 有重叠风险。

### 修复

新增轻量：

```text
scripts/validate_repository.py
.github/workflows/repository-consistency.yml
```

只检查可确定的结构事实：

- required files；
- Markdown local links；
- Skill front matter；
- duplicate invariant ids；
- canonical navigation entries；
- stable docs 中禁止的明显旧 “current entry” 文案。

不进行：

- LLM-as-judge；
- 内容真值评分；
- Source identity 替代；
- 自动 Session schema migration。

## Finding 10 — 合并后 topic branches 仍存在

已合并 Profile / governance topic branches 在远端仍可见。

当前 MCP surface 没有删除 Git ref 的写操作，本轮不使用未授权 shell/API 绕过。它们是非阻塞 hygiene finding；后续由具备 branch-delete capability 的维护动作清理。

## 未修改的历史事实

以下内容必须保留：

- Kafka Pilot scope discipline = FAIL；
- Recall / Reconstruction = PARTIAL；
- transient runtime / serialization finding；
- Raft 第一个 strict Session 因 boundary-preflight lookahead contamination 被 abandoned；
- Profile v0.1 的 fresh acceptance 是真实 L2 fixture，不单独证明所有 depth class。

## 验证计划

```text
python3 scripts/validate_repository.py
```

PR review 还应人工检查：

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
仓库 canonical docs / Agent entry / Issue control summary
已经重新对齐
+
基础结构 drift 有自动检查
```

不表示：

- 所有论文已读完；
- 所有 Session mode 已充分验证；
- reading-mcp 全部格式无缺陷；
- 仓库永远不再需要审查。
