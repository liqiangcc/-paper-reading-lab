# Repository checks：范围与证据边界

## 运行

在仓库根目录执行，依赖 Python 标准库：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repository.py
```

测试在临时目录构造正向、负向 fixture，不修改真实论文、Session、Issue 或仓库文件。测试本身也会验证完整仓库通过、插入真实坏链接失败、恢复后再次通过。

CI 在 PR 与 main push 上运行相同命令。第三方 Actions 保持固定 commit SHA，权限为 `contents: read`。CI 配置存在不代表仓库已经启用强制 required checks / branch protection；远端保护策略需要单独读取和授权配置。

## 已自动检查

| 检查 | 实际边界 |
| --- | --- |
| 必需文件 | 当前日常核心规则，以及 validator、回归测试和 CI workflow 的文件存在性；历史 Pilot/旧 Profile 不作为默认启动依赖 |
| 本地链接与图片 | 普通 inline Markdown destination 的存在性、仓库路径越界；支持 URL 编码、尖括号包裹路径、可选引号标题及一层路径圆括号 |
| 代码区 | 忽略顶层 backtick / tilde fenced code 和匹配 backtick inline code 中的示例链接 |
| 围栏闭合 | opener / closer 字符相同，closer 长度不少于 opener，closer 后只能有空白 |
| 本地标题锚点 | 本仓库普通 ATX heading、Unicode 文本、重复标题编号及显式 id/name anchor；引用其他文件与同文件均检查 |
| 导航 | 核心日常规则必须有真实 inline link，只出现路径字符串不算导航；不强制把历史实验列为必读 |
| Invariant | 正文 invariant ID 唯一且关键 ID 存在；代码示例不冒充正式定义 |
| Skill | 检查现有简单 front matter 的 name 与非空 description；不是完整 YAML Schema 验证 |
| 格式 | Markdown 尾随空格、tab、未闭合顶层 fence；少量已知过期 README 字面值 |

## 不宣称覆盖

这不是完整 CommonMark / GitHub Markdown renderer。reference-style links、Setext headings、复杂嵌套列表 / blockquote 中的 fenced code、任意 HTML 和扩展标题属性，未作为完整兼容性承诺。新增此类用于正式导航的语法前，应补相应用例与实现，或采用已支持的简单 inline link / ATX heading。非 Markdown 文件的 fragment（例如 PDF 页码）不解释；外部 URL 不联网验证。

脚本不校验 workflow YAML 的完整语义、远端分支保护、GitHub Issue 状态、CI 运行真实性、真实 Source identity、no-lookahead 执行历史、解释质量或用户能力变化。发现 live-state 冲突必须依据 [Task closure gate](../workflows/issue-driven-workflow.md#task-closure-证据门禁) 人工 / Agent 复核。

删除整个 workflow 后未必有该 workflow 继续执行；必需文件检查不是平台强制保护的替代品。

## 回归维护

修复 validator 时先保留最小复现，并让负向 fixture 明确要求 FAIL、正向 fixture 明确要求 PASS。不要只验证“仓库当前能过”：错误检查器也可能在健康仓库上通过。

可验证的闭环是：已确认的错误输入 → 原检查错误结果 → 修复 → 相同用例获得预期结果 → PR CI → merge SHA 的 main CI → durable report。fixture 通过仅证明覆盖的分支，不升级为“仓库永远无问题”。

日常语义质量只由实际分析与具体问题审查，不新增评分流水线。原有 Markdown 正负向回归保留；精简不移除身份、范围或原文准确性要求。
