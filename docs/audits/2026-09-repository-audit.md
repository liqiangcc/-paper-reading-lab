# 2026-09 全仓库一致性审查

## 范围

审查基线：

```text
main = aa20d2066c754f3cec11a9f1c48a6852b6215f13
```

覆盖根级治理、全部 canonical 文档、Source-First Reading Skill、Kafka / Raft Primary Issue 控制面，以及轻量 repository consistency checks。本审查不继续 reveal 论文 Source，不修改 `reading-mcp`，不改写历史 finding。

## 总体结论

仓库核心机制已经由真实 Pilot 支持，但多轮 workflow、Profile、AGENTS 和 Skill 修复分别合并后，出现了跨文档模型漂移：

```text
workflow / Profile / Agent governance 已演进
但 root overview / domain / adapter / source policy 未同步
```

本轮以稳定入口、领域一致、Source Adapter 边界、动态状态归属和轻量自动检查为主线修复。

## 主要 finding 与修复

### 1. 稳定文档承担瞬时 live state

旧 README / 导航曾写死“当前 Issue / 当前下一步”，而 Issue comments 已推进。

修复：README 只保存稳定方法入口；实时状态必须读取对应 Issue 的最新 durable record；Pilot 历史与 closure 分开。

### 2. Domain model 落后

旧模型未完整覆盖：

```text
planned_scope
current_scope_boundary
ScopeAmendment
ExplanationProfileRef
OperationalRecoveryCheckpoint
ReadingSessionLearningArtifact
stop_boundary
```

修复：同步 `docs/domain/model.md`、ReadingSession、lifecycle、Issue workflow 和 invariants。

### 3. Source Adapter / Source Policy 落后

真实 Kafka / Raft 路径已经验证：

- structure-only named-section boundary；
- future-body lexical search 会污染 no-lookahead；
- original source view；
- canonical unit 可能包含多个 surface sentences；
- capability 必须靠当前实际 invocation；
- stale locator 必须 fail closed。

修复：更新 `docs/integrations/reading-mcp.md` 和 `docs/source/source-policy.md`。

### 4. AGENTS / Bootstrap / Skill 重复

修复后职责收敛为：

```text
AGENTS.md = routing + hard invariants
conversation-bootstrap.md = live-state recovery algorithm
source-first-reading/SKILL.md = one bounded action procedure
canonical docs = detailed method truth
```

### 5. Pilot 计划与 closure 混合

修复：`first-pilot.md` 明确为 historical execution protocol；新增 `first-pilot-closure.md`，保留 PASS / PARTIAL / FAIL matrix、scope drift、checkpoint limitation 和 completed hardening。

### 6. Primary Issue body 陈旧

Kafka #2 和 Raft #1 的 body 已根据最新 durable comments 重写为稳定 Paper / Revision 摘要、current Session summary、historical warning、durable-record rule 和当前授权边界。完整历史继续留在 comments。

### 7. 缺少确定性一致性 Gate

新增：

```text
scripts/validate_repository.py
.github/workflows/repository-consistency.yml
```

检查：

- required governance files；
- Markdown local links；
- Skill front matter；
- invariant id 唯一性及关键 id；
- canonical navigation；
- trailing whitespace / code fences；
- stable docs 中明显旧 live-state literal。

第三方 GitHub Actions 使用 immutable commit SHA 固定。Validator 不做 LLM-as-judge，不替代 Source provider 或人工语义 review。

## 必须保留的历史事实

- Kafka Pilot scope discipline = FAIL；
- Recall / Reconstruction = PARTIAL；
- transient runtime / serialization finding；
- Raft 第一个 strict Session 因 boundary-preflight lookahead contamination 被 abandoned；
- Profile v0.1 acceptance 是真实 L2 fixture，不单独证明所有 depth class。

## Validation

在最终审查分支的 fresh clone 中实际执行：

```text
python3 -m py_compile scripts/validate_repository.py
python3 scripts/validate_repository.py
```

结果：

```text
repository consistency validation: PASS
```

这只证明脚本定义的确定性 repository checks；PR 上的 GitHub Actions 会再次执行相同检查。

## 剩余非阻塞 finding

已合并的 Profile / governance topic branches 仍存在。当前 MCP surface 没有删除 Git ref 的写能力，本轮不绕过权限使用未授权 API；后续由具备 branch-delete capability 的维护动作清理。

## Completion 语义

本审查完成表示：

```text
截至本 Candidate SHA
canonical docs / Agent entry / Issue control summary 已重新对齐
并且基础结构 drift 有确定性检查
```

不表示所有论文读完、所有 Session mode 已充分验证，或仓库以后不再需要审查。
