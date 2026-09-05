# Kafka 2011：三单元学习资产候选

## 身份与证据等级

```yaml
artifact_id: kafka-2011-transfer-fixture-learning
artifact_version: v0.1
artifact_status_at_creation: candidate
artifact_kind: derived-learning-artifact
paper_id: kafka-2011-distributed-messaging
revision_id: kafka-2011-netdb11
primary_issue: 2
validation_task: 12
build_execution: issue12-artifact-build-20260905T0540Z
mode: retrospective-evidence-compression
governance_sha: 27471ed0b2b99ad9c25c088a55cbbf6ad7c5ee67
style_profile:
  id: source-first-incremental-explanation
  version: v0.1
  status: pilot-candidate
  source: docs/learning/incremental-explanation-profile.md
  source_commit: 27471ed0b2b99ad9c25c088a55cbbf6ad7c5ee67
  git_blob_sha: 7435b08fb32deeefa914fb7eb0254df736b7bd42
new_source_units: 0
```

这是对已完成精确回读的 R0/R1/R2 记录所作的 **Derived 压缩**，不是新的 canonical Source，也不是整节总结。Source 核验继承下列三次执行的明确证据，不是因为 Issue 中出现某段文字就将其升格为原文。资产作者本步没有再次调用 reading-mcp；当前工具可用性和独立 Source 复核不在本资产的证明范围内。

本文的中文内容均为转述或解释，不镜像返回的原文字节。canonical wording 仍以绑定的 reading-mcp locator 为准。完整规范见 [ReadingSession](../../reading-sessions.md#readingsession-learning-artifact) 和 [Source policy](../../../source/source-policy.md#公开仓库版权边界)。

## 样本范围与历史证据

| 论文顺序 | Case | 回放 Session | exact-read 结果记录 | 记录的返回字符数 | 深度判定 |
| --- | --- | --- | --- | --- | --- |
| 1 | R1 | `validation-r1-replay-20260905T0522Z` | [R1 结果](https://github.com/liqiangcc/paper-reading-lab/issues/12#issuecomment-5549629434) | 90 | L1 |
| 2 | R0 | `validation-r0-replay-20260905T0443Z` | [R0 结果](https://github.com/liqiangcc/paper-reading-lab/issues/12#issuecomment-5549597879) | 97 | L0 |
| 3 | R2 | `validation-r2-replay-20260905T0523Z` | [R2 结果](https://github.com/liqiangcc/paper-reading-lab/issues/12#issuecomment-5549641481) | 209 | L2 |

验收执行顺序为 R0、R1、R2；论文局部顺序为 R1、R0、R2。Case 是验证别名，不是新建的 SourceUnit identity。三次记录均报告一次 `read_document`、`exact_target`、`complete=true`、`truncated=false`、完整 `resolved_target_locator` 匹配和 `new_source_units=0`。字符数是历史响应元数据，不从 comment 中的排版引用重新计算。

回放是 retrospective，不能计作新的 clean first-pass。L0/L1/L2 是该 Profile 下的解释深度判断，不是论文或 provider 自带的分类；尤其 R1 也具有过渡功能，本样本选择 L1 不证明分类唯一。

## 局部学习模型

### R1：引入关注点

**Source-grounded Observation S1（R1）**：当前单元包含“Efficient transfer”标注，并表达对 Kafka 数据进出传输处理的重视。

**Derived D1**：它把局部关注点落在传输效率上，因此本样本按 L1 的普通认知增量处理；这不是已经给出了具体成本模型或优化机制。只处于 R1 时，后续机制仍未知。

### R0：重新激活前文

**Source-grounded Observation S2（R0）**：作者明确回指此前已说明的能力：producer 可在一次发送请求中提交一组消息。

**Derived D2**：回指表达承担 recap / bridge 作用；此处不必强行制造一个新机制。这里只核验了作者的回指句，没有重新核验被回指的更早段落。只处于 R0 时，它将支持的下一论点仍未知。

### R2：区分两个粒度

**Source-grounded Observation S3（R2）**：consumer API 每次迭代一条消息；底层一次 pull request 则取回多条消息，受一定大小限制，通常为数百 KB。“通常”不是普遍固定值；本单元没有给出精确阈值。

**Derived D3**：逐条 API 迭代与批量底层获取可以共存，因此不能由 API 的逐条外观推出每个请求只取一条消息。这是本 L2 样本的机制连接。

### 压缩后的显式连接

| 连接 | 性质及依据 | 限制 |
| --- | --- | --- |
| S1 传输关注 → S2 producer 批量发送回顾 → S3 consumer 批量获取 | 论证顺序是按三个 locator 排列；“关注→回顾→具体机制”的组织方式是 D1/D2/D3 的结构解释 | 不是设计必然性或因果证明；不代表整节的全部论证 |
| S3 的逐条 API 迭代 ≠ 底层逐条请求 → 两种粒度可以分离 | D3，直接依据 S3 中的对比 | 不能据此推断底层其他实现 |
| 一次请求获取多条消息 → 可能摊薄每条消息分担的固定请求开销 | 条件性 Derived D4，继承 R2 结果中的效率解释；前提是存在可共同分担的固定开销且其他因素可比 | 不是本单元明说或实测的性能结论；不推出吞吐、延迟或最优批量大小 |

证据整理说明：R2 执行记录中“摊销开销”的说法在这里明确保留为条件性 Derived，不提升为 Source Fact；历史执行记录不改写。不能把已知 R2 的解释倒填到 R1/R0 当时的未知项中，声称当时已经知道机制。

## 未知项与薄弱连接

**最终 Unknown U1**：大小限制的选择理由、具体阈值和完整成本模型，三单元不足以回答。

**最终 Unknown U2**：更大或更小批量的完整 trade-off、量化效果和其他底层机制，均不在已核验范围。

**待训练连接 G1**：能否从当前单元的实际作用区分“目标引入、回顾、具体机制”，而不是每句话都硬套完整机制链。

**待训练连接 G2**：能否在没有模型提示时区分 API 粒度与传输粒度，并保留“通常”和大小限制的限定。

G1/G2 是据样本提出的练习目标，不是已证明的学习者错误或掌握结论。本次没有新的 Prediction、cue history、学习者作答或 Reconstruction 结果。

## 覆盖与恢复边界

只覆盖下面三个精确目标，不把最小 start 到最大 end 的包络视为整段读取授权，也不把这三单元等同于整个 Section 3.1。没有重新验证更早章节、Figure、全文顺序或现代 Kafka 语义。

历史 first-pass 停点仍为 R2 所引用的 page 3 / paragraph 3 / sentence 3 / `[1851,2060)`；本资产不推进也不降低 revealed_position，不激活已消费的旧 Session。

候选创建时：样本 Source 回读证据已存在；本资产的独立恢复验收尚未执行；学习者 Recall / Reconstruction 为 NOT TESTED。最新执行状态属于 Issue #12，而不是由此文件持续更新。恢复程序见 [操作检查点](transfer-fixture-recovery.md)。

## 精确 Source 引用

以下对象从固定 binding 和已验证目标字段完整展开，可直接作为 `target_locator`；不是重切分或 fuzzy 重建。回放记录中 `returned_locator` 省略了部分可选字段，完整匹配依据为 `resolved_target_locator`。未来发生 stale 时必须停止，不能删 hash 续作。

### R1 TextLocator

```json
{
  "content_hash": "sha256:4abdeba2503eb20a5d7ed84aa8e7680bcbe3088541712626315deae0b07c2821",
  "document_id": "doc:sha256:d6c12b150874cc4b1ae0eab559e5a03854112e40f1d8d5a2e75a9ed83cb2677c",
  "native_location": "pdf:page:3",
  "normalized_document_hash": "sha256:65572ab96d3b3a506671b6fa3d156cb6fefbb5c7fbcccc63fd6e6f8c7070a16d",
  "owner_section_id": "section://page-3",
  "paragraph_index": 3,
  "section_path": [
    "Page 3"
  ],
  "segmentation_version": "text-segmentation/v2",
  "sentence_index": 1,
  "normalized_range": {
    "start": 1662,
    "end": 1752
  }
}
```

### R0 TextLocator

```json
{
  "content_hash": "sha256:4abdeba2503eb20a5d7ed84aa8e7680bcbe3088541712626315deae0b07c2821",
  "document_id": "doc:sha256:d6c12b150874cc4b1ae0eab559e5a03854112e40f1d8d5a2e75a9ed83cb2677c",
  "native_location": "pdf:page:3",
  "normalized_document_hash": "sha256:65572ab96d3b3a506671b6fa3d156cb6fefbb5c7fbcccc63fd6e6f8c7070a16d",
  "owner_section_id": "section://page-3",
  "paragraph_index": 3,
  "section_path": [
    "Page 3"
  ],
  "segmentation_version": "text-segmentation/v2",
  "sentence_index": 2,
  "normalized_range": {
    "start": 1753,
    "end": 1850
  }
}
```

### R2 TextLocator

```json
{
  "content_hash": "sha256:4abdeba2503eb20a5d7ed84aa8e7680bcbe3088541712626315deae0b07c2821",
  "document_id": "doc:sha256:d6c12b150874cc4b1ae0eab559e5a03854112e40f1d8d5a2e75a9ed83cb2677c",
  "native_location": "pdf:page:3",
  "normalized_document_hash": "sha256:65572ab96d3b3a506671b6fa3d156cb6fefbb5c7fbcccc63fd6e6f8c7070a16d",
  "owner_section_id": "section://page-3",
  "paragraph_index": 3,
  "section_path": [
    "Page 3"
  ],
  "segmentation_version": "text-segmentation/v2",
  "sentence_index": 3,
  "normalized_range": {
    "start": 1851,
    "end": 2060
  }
}
```
