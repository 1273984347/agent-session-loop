# Skill 开源 Runbook：任务流水线 + evals 评估逻辑

> 本文档沉淀 2026-08 将三 skill 开源（deep-review-loop / mem-wrap-up / self-evolution / agent-session-loop）的完整任务与评估逻辑，供后续新 skill 开源或补齐 evals 时复用。
> 两个已落地 evals 的参考实现：[deep-review-loop/evals](https://github.com/1273984347/deep-review-loop/tree/main/evals)、[mem-wrap-up/evals](https://github.com/1273984347/mem-wrap-up/tree/main/evals)。

## 一、开源任务流水线（7 步）

新 skill 从本地到 GitHub 公开，按此顺序执行：

| # | 阶段 | 关键动作 | 验证点 |
|---|---|---|---|
| 1 | **净化脱敏** | 个人绝对路径 → `<memory_root>`/`<project-slug>` 占位符；删 `.bak`；`metadata.source` 个人路径删除 | Grep 个人路径残留 = 0 |
| 2 | **标准合规** | frontmatter：`name`==目录名（小写+连字符）、`description` 双语祈使句 ≤1024、`license`、`metadata.version` semver；正文渐进披露 <500 行，细节拆 `references/` | `skills-ref validate` 通过 |
| 3 | **description 触发合同** | 三层：显式触发词 + intent 触发（"even without keywords"）+ **反触发**（Do not trigger when...） | validate.py 断言 3 个 marker + "Do not trigger" |
| 4 | **CI 双层** | `.github/workflows/validate.yml`：`skills-ref validate "$PWD"` + `python evals/validate.py` | 远程 run success |
| 5 | **分发多方案** | 复制目录 / `.claude-plugin/marketplace.json`（Claude Code `/plugin install`）/ skills.sh CLI | 三方案命令可执行 |
| 6 | **README 双语** | 中文（触发示例 + 适用/不适用表 + 版本兼容表 + MCP 说明）+ README.en.md | 结构一致 |
| 7 | **可发现性** | GitHub Topics 8 个（agent-skills/ai-agents/claude/claude-code/codex/developer-tools/llm/skills）+ 博客（中英）+ 流水线示意图 | topics 生效 |

**踩坑记录**：
- UTF-8 BOM：写文件工具可能加 BOM（EF BB BF），`skills-ref` 报「必须以 `---` 开头」→ 全仓库去 BOM
- `skills-ref validate .` 的目录名解析为空串 → 必须传 `"$PWD"`（绝对路径，basename = 仓库名 = skill 名）
- 建仓权限：GitHub App token（`ghu_`）无 createRepository 权限 → `Remove-Item Env:GH_TOKEN` 回落 keyring OAuth token（`gho_`，有 repo 权限）

## 二、evals 评估逻辑（两种模式）

### 模式 A：validate.py 结构回归（确定性，进 CI）

纯 stdlib Python，断言 4 类合同：

```python
EXPLICIT_MARKERS = ("deep review", "复检", "收敛", "DRL")   # ① 触发词必须存在
assert "Do not trigger" in description                       # ② 反触发条款
REQUIRED_PHRASES = ("真循环", "R0", "R1a", ..., "收敛曲线")  # ③ 协议短语不可丢
assert len(description) <= 1024                               # ④ spec 硬限
assert version == r'\d+\.\d+\.\d+'                           # ⑤ semver
# + evals.json / trigger-eval.json 一致性（fixture 存在、数量、字段）
```

**关键设计**：REQUIRED_PHRASES 是「协议契约」——skill 正文丢了任何一个核心机制（如收敛曲线、验证铁律），CI 立即标红。这是防回归的核心。

### 模式 B：evals.json 行为评估（人/agent 跑，不阻塞 CI）

```json
{
  "id": 1,
  "name": "false-convergence",
  "prompt": "……",
  "expected_output": "执行 5 轮闭环……",
  "files": ["evals/fixtures/eval-1-false-convergence"],
  "expectations": ["抓出假收敛……", "R3 产出收敛曲线……"]
}
```

fixture 是**带矛盾点的真实工作区**（文档声称完成但代码残留、版本号不一致等），供人/agent 在真实环境跑 eval 并核对 expectations。

### 模式 C：trigger-eval.json 触发评估

12 条查询（应触发 + 不应触发），对齐 agentskills.io optimizing-descriptions：不应触发要含**近失配**（关键词重叠但语义不同，如「帮我复检收敛」对 mem-wrap-up 是负例）。

## 三、两仓库 evals 设计对比

| 维度 | deep-review-loop | mem-wrap-up |
|---|---|---|
| 触发词 markers | deep review / 复检 / 收敛 / DRL | wrap up / 收尾 / 继续 |
| 反触发 | 单文件小改 / 常规编码 / 闲聊 | 书面复检（→DRL）/ 复盘（→evolution） |
| 协议短语（REQUIRED_PHRASES） | 13 个：真循环、R0-R3、收敛曲线、residual、P0-P2、边际收益、警报、过拟合、证据铁律、not-applicable | 13 个：7 步、验证铁律、6 面状态矩阵、memory 写入协议、毕业判据、4 段 schema、sediment、work-log、not-applicable、分阶段汇报、deep-review-loop、5Why、禁词 |
| fixture 场景 | 假收敛 / 批量修复 / meta-skill / 文档改动 | 过期文档 / memory 缺段 / 沉淀 / 汇报模板 |
| 断言风格 | 防「假收敛」（审查循环） | 防「声明≠事实」（验证铁律） |
| evals.json 数量 | 4 | 4 |
| trigger queries | 12 | 12 |

**设计差异根因**：DRL 的核心风险是**审查循环断裂**（跳轮/假收敛），所以断言集中在轮次与收敛证据；mem-wrap-up 的核心风险是**声明不落地**（prior session 说已更新但文件没改），所以断言集中在验证铁律与写入协议。

## 四、给新 skill 复用的步骤

1. 从 `deep-review-loop/evals/validate.py` 复制骨架，替换：
   - `EXPLICIT_MARKERS` ← 新 skill 的触发词
   - `REQUIRED_PHRASES` ← 新 skill 正文的核心协议短语（先 Grep 确认每个短语实际存在）
   - 反触发条款 ← 新 skill 的"不适用"场景
2. 写 3-4 条行为 eval（prompt 用真实用户话术）+ 对应 fixture（带矛盾点的迷你工作区）
3. 写 12 条 trigger 查询（含 2-3 条近失配负例）
4. CI 加 `python evals/validate.py`
5. 本地 `python evals/validate.py` 过 → 推送 → 远程确认两层绿

## 五、后续待办

- [ ] self-evolution 补 evals（核心短语候选：11 维度、dim 9、dim 11、知识升级、experience-log、单一事实源、P0/P1/P2/P3）
- [ ] 为 mem-wrap-up 的 6 面状态矩阵写「运行态」验证的可执行脚本（scripts/）
- [ ] 三个仓库的 README 叙事升级（金句/痛点，参考 khazix-skills 风格）
