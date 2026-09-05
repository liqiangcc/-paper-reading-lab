# 2026-09-05 闭环复核与校验器回归修复

## 对象与已核验证据

任务：Issue #10，复核前一轮 Issue #8 / PR #9。基线为 `b9b70cd1e1388a826c0ae26ba7b4aca5056565d1`。

- PR #9 candidate：`3909c5d1c749ef3a7f2a00ef75b623216bfad31c`；GitHub live state 确认已合并。
- merge/main：`b9b70cd1e1388a826c0ae26ba7b4aca5056565d1`。
- [PR CI run 33895382077](https://github.com/liqiangcc/paper-reading-lab/actions/runs/33895382077)：completed / success。
- [main CI run 33895822884](https://github.com/liqiangcc/paper-reading-lab/actions/runs/33895822884)：Actions live 页面关联上述 main commit，completed successfully。
- [历史 closure](https://github.com/liqiangcc/paper-reading-lab/issues/8#issuecomment-5543567206) 存在；#8 GitHub state 为 closed / completed。

因此上一轮 merge/CI 的闭环不是只有聊天声明。但仍发现控制面摘要冲突及检查覆盖不足，不能把旧 PASS 当作全部问题均已消失。

## 复现与修复

| Finding | 基线行为 | 修复 / 验收用例 |
| --- | --- | --- |
| #8 已关闭，body 却为 in progress 且 owner 未释放 | API state 与摘要冲突 | 同步 body、owner、清单、证据索引并回读；历史 comments 不覆盖 |
| fenced code 中示例链接 | 误报 broken link | 代码区屏蔽，示例 PASS；围栏外真正坏链接仍 FAIL |
| inline code 中示例链接 | 误报 broken link | 匹配 backtick span 屏蔽；未配对 backtick 不吞掉正常链接 |
| 未闭合 tilde fence | 漏报，PASS | opener/closer 状态检查，FAIL |
| 四反引号 opener + 三反引号 closer | 漏报，PASS | 短 closer 不闭合，FAIL |
| 已有 Markdown 文件中的不存在标题 fragment | fragment 被丢弃，PASS | 保留并检查本地普通标题锚点，FAIL |
| 删除 CI workflow | 不属于 required files，PASS | validator / tests / workflow 都加入 required files，FAIL |

六个检查器复现用例先在基线隔离快照运行，确认错误结果，再写入回归。补充正向/负向情况包括编码路径、图片、越界、重复标题、代码区中的假 invariant 与导航路径只被提及未形成链接等。

Task workflow 新增 closure 证据门禁，AGENTS / bootstrap 引用同一规则；I-94 固化 candidate、merge、main CI、review 状态以及 body/state/owner 回读要求。该 live-state 门禁不冒充离线 validator 能力。

## 验证方式

本轮容器不能联网 clone。使用 GitHub MCP 从固定 SHA 下载文件，逐文件核对 Git blob SHA，建立独立快照；不能称为 fresh clone。基线 validator 与 Python 编译检查实际通过。

修复后执行：

```bash
python3 -m py_compile scripts/validate_repository.py tests/test_validate_repository.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_repository.py
```

本地结果、最终 candidate、PR CI、merge SHA、合并后 main CI 和 Issue 状态回读，分别在 [Issue #10](https://github.com/liqiangcc/paper-reading-lab/issues/10) durable report 中记录，避免本文件在提交前预写未来 CI / merge 成功。检查范围详见 [repository checks](../validation/repository-checks.md)。

## 保留边界

没有调用论文正文工具，没有改变 #1 / #2 的阅读游标与授权范围；没有修改 Profile v0.1。历史 Recall / Reconstruction PARTIAL、scope discipline FAIL、污染与 transient finding 继续保留。L2 fixture 不自动证明 L0/L1 或真实学习效果。

基线三个已合并 topic branches 仍存在，GitHub MCP 未提供 ref-delete；这是非阻塞维护限制，不声称已经清理。本轮不扩大权限、不以 delete_file 删除分支，也不把未验证的 branch protection 说成已配置。

## 完成语义

本轮目标是让已复现的校验错误及 Task 状态漂移有修复、回归和可核验的提交/CI证据，不代表所有学习机制已经充分实测，更不代表论文已读完。
