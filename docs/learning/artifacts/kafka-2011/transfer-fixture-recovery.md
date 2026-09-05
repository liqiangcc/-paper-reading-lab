# Kafka 三单元资产：操作恢复检查点

此文件只保存恢复方法、身份和边界，不复制学习答案。它与 [Learning Artifact](transfer-fixture-v0-1.md) 分工不同，不能单独证明认知模型已恢复。

```yaml
checkpoint_id: kafka-2011-transfer-fixture-recovery-v0-1
artifact_id: kafka-2011-transfer-fixture-learning
artifact_version: v0.1
artifact_path: docs/learning/artifacts/kafka-2011/transfer-fixture-v0-1.md
candidate_commit: read-from-latest-issue12-handoff
paper_id: kafka-2011-distributed-messaging
revision_id: kafka-2011-netdb11
mode: artifact-assisted-recovery
lookahead_policy: retrospective-fixed-artifact-only
governance_sha: 27471ed0b2b99ad9c25c088a55cbbf6ad7c5ee67
profile_id: source-first-incremental-explanation
profile_version: v0.1
profile_source: docs/learning/incremental-explanation-profile.md
profile_commit: 27471ed0b2b99ad9c25c088a55cbbf6ad7c5ee67
profile_blob_sha: 7435b08fb32deeefa914fb7eb0254df736b7bd42
planned_scope:
  kind: fixed-artifact-recovery
  members: [R0, R1, R2]
current_scope_boundary:
  max_new_canonical_units: 0
  source_body_calls: 0
  whole_page_view_allowed: false
  sequential_forward_reveal_allowed: false
historical_first_pass_checkpoint:
  issue: 2
  comment_id: 5542784783
  latest_target: pdf:page:3 / paragraph:3 / sentence:3 / [1851,2060)
  effect: unchanged
```

`candidate_commit` 不是有效 Git ref；必须先从 live handoff 解析为完整 commit SHA，再读取本检查点和同一 commit 的资产，禁止默用 main。这样避免文件用自身 commit 自引用；Profile 固定在上述已存在的独立 commit，不随资产候选改变。

## 入口与输入隔离

先遵循固定治理的 [AGENTS](../../../../AGENTS.md) 和 [bootstrap](../../../workflows/conversation-bootstrap.md)。本动作是 Task 资产恢复，不是新的逐句 Source reveal，不强行路由成顺序阅读 Skill。

从 Issue #12 body、最新适用的 `[ARTIFACT RECOVERY HANDOFF]`、关联 PR 元数据及当前 scope 恢复执行身份。相关历史 Source 输出可在答后核对，不是恢复前必读材料。Issue #2 是历史路由，不需要在恢复前读取其正文或旧长解释。

恢复前写 `[ARTIFACT RECOVERY START]`：记录独立 conversation / execution identity、candidate SHA、实际输入清单和是否已暴露旧答案。先确认没有更晚的 scope / blocker superseding record。

如工具、自动附加上下文或 bootstrap 已提供 R0/R1/R2 的旧长解释、Issue #2 模型或其他答案，必须记录 exposure；不得声称“仅凭资产”。可以进行 `control-record-assisted` 辅助恢复，但资产独立充分性只能 PARTIAL / NOT TESTED，另留隔离试次。不能要求模型假装忘记。

## 唯一有界动作

1. 按 handoff 的固定 SHA 读取本检查点与资产，并核对绑定的 Profile；不访问 Source provider，不读取论文新正文。
2. 仅依据实际允许输入，组织三单元范围内的模型、显式连接、事实/推论/未知边界、gap、覆盖限制及停止位置。无需复述资产的每一句。
3. **先**把恢复文本与实际输入引用保存为 `[ARTIFACT RECOVERY RESPONSE]`，冻结首答；**再**按需要打开资产中列出的三条历史回读结果作答后核对。不得事后美化首答。
4. 追加 `[ARTIFACT RECOVERY RESULT]`：逐项记录身份/版本一致、模型恢复、关系依据、Unknown/gap、覆盖与停止边界，以及独立性/exposure。PASS 只对应实际通过的维度；报告遗漏和误推，不能用字数评分。
5. 同步 #12 状态、checkpoint 引用和唯一 next_action；释放 owner 并 STOP。结果写回后不得自动合并 PR、关闭全部 #12 或开始新的 Source/训练动作。

如果候选变化、关键引用缺失或输入身份不确定，写 blocker 并停止；不换版本、不搜索论文补答案。本会话若就是资产作者，也不能自称独立 fresh-conversation evaluator。

## 证据语义

本试次是 artifact-assisted recovery，不是 closed-book Recall，不证明学习者掌握，也不重新证明历史 reading-mcp 实际调用。论文事实的独立复核仍由未来明确授权的 Source 动作承担。

学习者 Recall / Reconstruction 需要另行安排真实作答、提示级别和答后核对；不得先展示本资产答案再计作无提示成功。候选文件、CI PASS、独立恢复和 Profile stable 是不同 gate。

本检查点不保存动态执行结果：候选 SHA、PR、检查结果和最新 next_action 以 Issue #12 的适用 handoff 为准。
