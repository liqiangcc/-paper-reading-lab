# Source-First 增量解释 Profile

## Profile identity

以下字段是本 Profile 的规范身份：

```yaml
profile_id: source-first-incremental-explanation
version: v0.1
status: pilot-candidate
language: zh-CN
extends:
  - source-first-sentence-reading
```

`profile_id + version` 共同标识一个不可静默改写的 Profile 版本。

`pilot-candidate` 表示它已经来自真实阅读经验，但仍需通过 Kafka 2011 等 Pilot 的跨会话验收后再决定是否升级为稳定版本。

## 目的

本 Profile 规定：当 `reading-mcp` 已经提供当前允许揭示的 canonical `SourceUnit` 后，AI 应如何稳定解释和呈现该单元。

它要解决的是：

```text
Source-First Protocol
→ 规定允许读取什么、何时允许读取

Explanation Profile
→ 规定拿到当前 SourceUnit 后怎样解释和呈现

ReadingCheckpoint
→ 记录当前 Session 状态、Profile 绑定和恢复入口
```

本 Profile 不改变 Source identity、SourceUnit 顺序、TextLocator 或 no-lookahead 规则，也不替代 `docs/learning/source-first-sentence-reading.md`。

## 适用范围

默认用于：

- Source-first Learning Session；
- 首次 no-lookahead 逐句阅读；
- 对已经 canonical reveal 的 Figure / Table / Equation 做原始视觉核对；
- 需要跨 conversation 保持解释风格的 ReadingSession。

Prediction、Recall、Reconstruction、Transfer 和 Retrospective 可以引用本 Profile 的 Source / Derived 边界与箭头规则，但应按照各自 Session mode 调整输出结构。

## 输入前提

执行一次增量解释前，至少应具备：

```text
PaperRevision binding
+
当前 Session mode / scope / lookahead policy
+
已经揭示的历史 SourceUnitRef
+
当前 canonical SourceUnitRef
+
当前 ReadingCheckpoint
+
本 Profile 的 id / version
```

如果当前 SourceUnit 不可精确回读、locator stale、revision 冲突，或者 future Source 已被意外暴露，应先按照仓库既有协议 fail closed 或记录 contamination，而不是继续生成看似完整的解释。

## 规范词

本文使用：

- **MUST**：不满足即不符合本 Profile；
- **SHOULD**：默认执行，只有明确理由时才偏离；
- **MAY**：根据当前 SourceUnit 和学习目标选择执行。

## MUST：不可破坏的规则

### M-01 先展示当前 canonical 原文

输出必须先锚定当前 `SourceUnit` 的原始 wording。

如果 Source provider 返回的是 canonical fragment 或 coarse Paragraph，应忠实展示实际 kind，不得人工伪装成更精确的 Sentence。

### M-02 翻译与解释分离

忠实翻译只表达当前原文的直接含义。

不得把后文知识、设计动机、现代实现或自己的评价混入翻译，再把它们伪装成作者原句已经表达的内容。

### M-03 只使用 Past + Current Source

首次 no-lookahead Session 只能使用：

```text
已揭示 SourceUnit 1..N-1
+
当前 SourceUnit N
+
Session 明确允许的既有背景知识
```

不得使用尚未 reveal 的 `SourceUnit N+1..end`。

### M-04 说明当前句与前文的关系

至少应说明当前单元是在：

```text
承接 / 澄清 / 对比 / 因果 / 约束 / 例证
问题提出 / 假设 / 决策 / 后果 / 证据 / 边界 / 过渡
```

中的哪一种或哪几种关系。

关系无法由已揭示 Source 支撑时，应标为有限推论或保持 Unknown。

### M-05 只提取真实认知增量

解释必须回答：

> 相对于已经揭示的模型，当前 SourceUnit 真正新增了什么？

不得为了显得深入而重复整个历史模型，也不得给只承担结构作用的句子制造不存在的机制结论。

### M-06 区分 Source Fact、Derived Interpretation 和 Unknown

输出中的内容必须能够被区分为：

```text
Source Fact
→ 当前或此前已揭示 Source 直接支持

Derived Interpretation
→ 基于已揭示 Source 的有限推论，可在后续修正

Unknown
→ 当前 Source 尚未回答，不能由模型记忆补齐
```

不要求每次都建立三个独立标题，但语义边界必须清楚。

### M-07 显式 reasoning arrow 必须可追溯

每一个显式箭头：

```text
A
→
B
```

都必须满足至少一种条件：

1. 当前 SourceUnit 直接表达；
2. 此前已揭示 SourceUnit 直接表达；
3. 由上述事实组合得到的有限推论，并明确保持 Derived 身份。

无法说明箭头依据时，应删除该箭头，或改写为开放问题。

### M-08 不倒灌未来版本或现代实现

历史论文按当前绑定的 `PaperRevision` 解释。

现代系统知识、后续版本差异或同一论文未来章节只有在明确标记为外部背景、版本对照或 Retrospective 时才可出现；不能反向覆盖当前历史 Source 的语义。

### M-09 保留 precise Source reference

正式 ReadingStep 必须保留当前 `SourceUnitRef` / `TextLocator`，至少能重新交给 Source provider 精确回读。

仅有页面号、段落号或人工句号编号不能承担 precise identity。

### M-10 在当前自然学习边界停止

完成当前单元解释后必须停止，不读取下一独立正文。

ReadingStep 应明确保存：

```text
revealed_position
current SourceUnitRef / TextLocator
stop_boundary
next_action
```

`stop_boundary` 表示本次输出结束时尚未 reveal 下一独立 SourceUnit。

## SHOULD：默认呈现方式

### S-01 默认结构

普通正文默认按以下顺序组织：

```text
原文
→ 忠实翻译
→ 字面含义
→ 与前文关系
→ 当前认知增量
→ 当前问题模型更新
→ Source / Derived / Unknown 边界
→ locator
→ STOP
```

标题名称可以根据句子自然调整，不要求机械复制固定模板。

### S-02 箭头用于表达关系，而不是装饰

箭头图应优先展示：

```text
Problem
→ Constraint
→ Decision
→ Mechanism
→ Effect
→ Boundary
```

或当前 Source 实际支持的子链。

不应使用大量无来源箭头制造“看起来像推理”的排版。

### S-03 避免重复整个历史模型

每一步主要展示当前新增或被修正的边。

完整累积模型只在自然 checkpoint、机制闭环、段落收束或用户明确要求时重述。

### S-04 长度随信息密度自适应

```text
风格稳定
≠
每句固定长度
```

结构句应紧凑；普通认知增量使用标准模板；关键机制、因果闭环或 trade-off 才深入展开。

### S-05 解释当前“为什么现在需要这一步”

当 Source 足够支持时，应说明：

> 如果只知道此前内容，哪个压力、缺口或开放问题推动作者在这里加入当前信息？

如果 Source 不足以证明作者意图，使用“当前更像”“可能”“从结构上看”，而不是断言作者心理。

### S-06 保留开放问题

当前句留下的关键未知项应显式保留，作为后续模型更新的入口。

不要用模型记忆提前关闭这些问题。

## MAY：按需增强

### A-01 原始视觉核对

正文引用 Figure、Table、Equation、Algorithm 或复杂排版时，可以通过 `get_source_view` 查看绑定的原始视觉 Source。

必须区分：

```text
正文直接说明
vs
原图直接观察
```

看到整页时，不得把页面中尚未 canonical reveal 的未来正文用于当前解释。

### A-02 Before / New / After

当前认知变化适合对比时，可以使用：

```text
Before
→ 已有模型

New Source
→ 当前增量

After
→ 更新后的模型
```

### A-03 独立 Known / Inference / Unknown 区块

当一句话容易被过度推导、涉及故障语义、性能原因或版本差异时，可以单独列出三类边界。

### A-04 术语等价表

作者明确使用 `called`、`referred to as`、`equivalently`、`interchangeably` 等声明时，可以维护术语表：

```text
Term A
≡
Term B
```

等价范围必须受当前 `PaperRevision` 和当前语境约束。

### A-05 版本边界说明

当学习者主动询问历史设计与现代实现差异时，可以增加独立对照，但必须明确：

```text
当前论文 Source
≠
现代版本事实
```

继续首次阅读时，仍按历史 Source 语义推进。

## 自适应解释深度

解释深度由当前 SourceUnit 的功能和信息密度决定。

### L0：结构、过渡或标注单元

适用：

- heading；
- transition；
- caption；
- terminology note；
- 章节导航；
- 图例说明。

最小输出：

```text
原文 / 标题
→ 翻译或结构说明
→ 它在当前论证中的作用
→ locator
→ STOP
```

L0 不强行生成完整 `Problem → Mechanism → Effect`。

### L1：普通认知增量

适用：

- 新事实；
- 一般约束；
- 普通定义；
- 局部关系；
- 未形成完整闭环的机制片段。

默认输出：

```text
原文
→ 翻译
→ 字面含义
→ 与前文关系
→ 新增信息
→ 当前模型更新
→ 边界
→ locator
→ STOP
```

### L2：关键机制、因果闭环或 trade-off

适用：

- 核心设计选择；
- 设计理由首次闭环；
- 明确机制；
- 性能或可靠性 trade-off；
- 重要版本语义差异；
- 容易被错误扩大解释的限定。

根据 Source 实际支持的部分展开：

```text
Problem
→ Constraint
→ Decision
→ Mechanism
→ Effect
→ Trade-off / Boundary
```

L2 可以较长，但仍不得越过当前 Source 边界。

## 深度选择规则

开始解释前依次判断：

```text
1. 当前单元是否主要承担结构作用？
   → 是：L0

2. 当前单元是否只增加一个普通事实、定义或局部关系？
   → 是：L1

3. 当前单元是否闭合重要因果链、引入关键机制或揭示 trade-off？
   → 是：L2
```

无法确定时，默认选择较低深度；后续 Source 到来后再更新模型，而不是在当前步过度展开。

## 翻译边界

翻译应优先保持作者的限定和强度：

```text
may        ≠ must
can        ≠ always
typically  ≠ universally
approximately ≠ exactly
```

术语第一次出现时可保留英文；后续保持一致。若中文译法会掩盖论文中的技术区别，应使用中文解释并保留英文术语。

## 当前问题模型

每一步只更新受当前 Source 影响的部分：

```text
Known facts
Current problem
Constraints
Explicit reasoning links
Open questions
```

不得把“完整总结整节”当作每个 ReadingStep 的默认产物。

## Checkpoint / Handoff 引用

使用本 Profile 的 Session 应保存：

```yaml
style_profile:
  id: source-first-incremental-explanation
  version: v0.1
  source: docs/learning/incremental-explanation-profile.md

style_overrides:
  language: zh-CN
  depth: adaptive
```

`style_overrides` 只能在 Profile 允许范围内调整呈现，不能取消 MUST 规则。

Issue comment 或 `[SESSION HANDOFF]` 应引用 `profile_id + version + source`，而不是复制完整长 Prompt。

## 跨会话恢复

Fresh conversation 恢复顺序：

```text
读取 Primary Issue live state
→ 读取最新 Session checkpoint / handoff
→ 读取绑定的 Source-First Protocol
→ 读取绑定的 Explanation Profile version
→ 核验 PaperRevision / Source identity / revealed_position
→ 执行唯一 next_action
```

恢复时不得：

- 根据模型记忆猜测 Profile；
- 静默切换到仓库中的更新版本；
- 因换 conversation 自动读取未来 Source；
- 用复制的旧长 Prompt 覆盖 canonical Profile。

## Profile 版本生命周期

### pilot-candidate

来自真实 Pilot，但仍允许根据 acceptance finding 修订。

### stable

至少满足：

- 在真实论文上完成跨会话恢复；
- L0 / L1 / L2 均有实际样本；
- 没有破坏 no-lookahead；
- checkpoint 只凭 Profile identity 即可恢复主要风格；
- 关键 finding 已进入 retrospective review。

### 版本变更

任何会改变 MUST、深度含义或 checkpoint 恢复语义的修改都必须产生新版本。

历史 Session 继续绑定开始时使用的版本。不得把旧 checkpoint 静默解释为新版本。

## Kafka 2011 acceptance checklist

Kafka 2011 Issue #2 是本 Profile 的首个真实 fixture。Fresh-conversation acceptance 至少检查：

```text
□ 只 reveal exactly one canonical SourceUnit
□ 未使用未来 Source
□ 原文、翻译、关系、增量和模型更新保持清楚
□ Source Fact / Derived / Unknown 可区分
□ 显式箭头均有已揭示 Source 依据
□ L0 结构句没有被过度展开
□ L2 机制句能够自然深入
□ 保存 precise locator 和 stop boundary
□ handoff 不复制完整 Style Prompt
□ 仅凭 Profile identity + checkpoint 可以恢复风格
```

验收失败也应保留 finding，不能为了升级为 `stable` 隐藏问题。

## 非目标

本 Profile 不负责：

- 重新解析论文；
- 生成与 `reading-mcp` 平行的 SourceUnit identity；
- 自动判断作者观点正确与否；
- 保存完整 AI transcript；
- 自动风格评分或 LLM-as-judge；
- 固定每句话的字数；
- 强制每个 SourceUnit 都做 Prediction；
- 把 Reading finding 直接升级为正式知识。

## 核心不变量

```text
Source Protocol 决定可见边界。
Explanation Profile 决定解释与呈现方式。
Profile 不能扩大 Source 可见范围。
当前解释只依赖 Past + Current Source。
事实、有限推论和未知项保持可区分。
每个显式箭头必须可追溯。
解释深度自适应，不等于固定长度。
每步保存 locator，并在当前边界停止。
Profile 版本不能在 Session 中静默切换。
```
