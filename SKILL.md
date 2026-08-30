---
name: agent-session-loop
description: >
  Manages the full agent session lifecycle as a single pipeline: deep review (审查) → wrap-up (收尾) →
  evolution (沉淀). Use at session end, after batch fixes or large docs, when the user says
  "收尾 / wrap up / 复检 / 复盘 / retro", or when docs and code mismatch and the session needs a complete
  close-out with memory sedimentation.
  将 Agent 会话完整生命周期整合为一条流水线：深度复检（审查）→ 7 步收尾 → 复盘沉淀。
  会话收尾、批量修复/长文档完成后、用户说「收尾/复检/复盘/retro」、或文档与代码不一致需完整闭环时使用。
  Do not trigger for one-off single-file edits or casual Q&A, or when the user asks for a standalone
  deep review or retro — use deep-review-loop / self-evolution instead.
license: Apache-2.0
compatibility: Agent-agnostic. Requires file search (Grep/Read) and a memory directory convention; subagent/task spawning optional (degradation mode when absent).
metadata:
  version: "1.0.2"
---

# agent-session-loop

> 一条流水线管理 Agent 会话的完整生命周期：**审查 → 收尾 → 沉淀**。
> 每个 session 结束时按此顺序闭环，把「验证过的结论」沉淀为「可复用的经验」。

**Announce at start:** "I'm using the agent-session-loop skill to run the session lifecycle pipeline (review → wrap-up → evolution)."

## 工具名映射（跨平台）

正文中的工具名按「通用能力」描述，实际执行时映射到你所在平台的等价工具：

| 正文写法 | 通用能力 | 常见平台实现 |
|:---|:---|:---|
| subagent / Task | 派独立子代理（可并行） | TRAE Task / Codex spawn_agent / Claude Code Task |
| RunCommand | 执行 shell 命令 | PowerShell（Windows）/ bash / zsh（macOS）/ sh |
| Grep 工具 | 文本搜索 | TRAE Grep / `rg` / `grep` / Select-String |
| Read / Edit / Write | 文件读写 | 各平台内建文件工具 / apply_patch |
| LS / Glob | 枚举文件与目录 | `ls` / `Get-ChildItem` / glob |
| Skill 工具 | 调用另一个 skill | 各平台 skill 机制；无则按对应 SKILL.md 手动执行 |
| NEEDS_CONTEXT | 子代理缺上下文的回退信号 | 通用约定：子代理报告「信息不足/上下文缺失」时按 fallback 处理；个别平台内建等价信号（如 TRAE NEEDS_CONTEXT）直接映射 |

**命令示例（Windows PowerShell ↔ macOS/Linux POSIX）**：

| 目的 | PowerShell | POSIX |
|:---|:---|:---|
| 行数统计 | `(Get-Content FILE).Count` | `wc -l FILE` |
| 文件/路径存在 | `Test-Path FILE` | `test -e FILE` / `test -f FILE` |
| 递归枚举 | `Get-ChildItem -Recurse -File` | `find . -type f` |
| 超大文件 | `Get-ChildItem -Recurse \| Where-Object {$_.Length -gt 50KB}` | `find . -type f -size +50k` |
| 软链目标 | `Get-Item LINK \| Select-Object Target` | `readlink -f LINK` / `ls -l LINK` |
| 命中计数 | Grep output_mode=count | `grep -c PATTERN FILE` / `rg -c PATTERN FILE` |

## 无子代理平台的降级模式

平台不支持子代理/任务派生时，**降级 ≠ 跳过**，三阶段流水线必须全部执行，只改变执行者：

| 原执行方式 | 降级方式 | 铁律 |
|:---|:---|:---|
| Phase 1 R1a：3 个 parallel verifier | 串行逐个派发；无派发能力则由主代理分 3 轮独立视角内审 | 3-lens 拆成 3 轮独立检查，禁止一轮合并 |
| Phase 1 R1b / R2：独立 subagent | 主代理自我对抗：换视角重读 + 默认 refute 自己结论 | self-audit ≠ 独立审计，降级显式标注 `degraded (no-subagent)` |
| 子代理缺上下文回退（NEEDS_CONTEXT） | 主代理自查 scope 是否过宽，缩小到具体 file:line 后重跑 | 不允许静默跳过 |

降级后收尾报告必须显式标注 `degraded (no-subagent mode)`，不编造子代理证据。

## 流水线总览

```
        Phase 1                 Phase 2                Phase 3
   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
   │  审查 (Review)  │ →  │  收尾 (Wrap-up) │ →  │  沉淀 (Evolution)│
   │ 5 轮深度复检     │    │ 7 步收尾流水线   │    │ 快速/全面复盘     │
   │ R0→R3 + V1→V5  │    │ memory 审计     │    │ 11 维度 + 知识升级 │
   └────────────────┘    └────────────────┘    └────────────────┘
       输出: 收敛结论         输出: 收尾报告         输出: 复利经验
        + residual risk       + sediment            + 规则升级
```

**阶段输入输出契约**（每阶段产出喂给下一阶段）：

| 交接点 | 上游产出 | 下游消费 |
|:---|:---|:---|
| 审查 → 收尾 | 收敛曲线 + ≥3 residual risk | 收尾 Step 4/7 的验证清单 + 待沉淀项 |
| 收尾 → 沉淀 | sediment（编号+5Why 链）+ work-log | 复盘维度 1/5/9 的输入 |
| 沉淀 → 下一 session | 知识层升级 + 行动项 | 下次会话的规则与 checklist |

## 触发条件

- 会话收尾（用户说「收尾 / wrap up」）
- 批量修复（>10 项）或长文档/方案/skill 写完后
- 用户说「复检 / 收敛 / DRL / 复盘 / retro」
- session 已跑 30+ 轮 / token 接近上限 / 重大里程碑达成
- 怀疑假收敛 / 文档与代码不一致，需要完整闭环

## 精简执行（按场景裁剪）

不是每次收尾都要跑满三阶段。按场景裁剪：

| 场景 | 必走 | 可裁剪 |
|:---|:---|:---|
| 纯调试 session（无版本推进、无新经验） | Phase 2 收尾（最小化） | Phase 1 / Phase 3 标 `not-applicable` |
| 批量修复 / 长文档完成后 | Phase 1 审查（全量） | Phase 3 用快速模式 |
| 周汇总 / 用户明确要求复盘 | Phase 3 全面模式 | Phase 1 降为 R0 表面检查 |
| 完整 session 收尾 | 全三阶段 | — |

> 裁剪不是跳过：被裁剪的阶段必须显式标注 `not-applicable` 并说明理由，不允许静默跳过（对齐「不编造证据」原则）。

---

## Phase 1：审查（Deep Review）

**目标**：在收尾前先证明「本 session 的产出真的没问题」——不收敛就谈不上收尾。

**核心协议**（详情见 [references/01-review.md](references/01-review.md)）：

1. **R0 表面检查**：file size + verdict 字眼 grep + expected hits 必现 + 项目阶段判定（N_max）
2. **R1a 3 独立 verifier**（3 subagent parallel，factual / completeness / reusability，必附工具证据）
3. **R1b 对抗性审查**（1 subagent，default refuted=true + class-level scope + 严重度门槛）
4. **R2 独立审计**（1 subagent，NOT inline，边际收益 gate）
5. **R3 收敛判定**（≥3 residual risk + 收敛曲线 + 过拟合警报）

**4 层过拟合防护**（本阶段强制执行）：
- 层 1：P2 残留 N（比赛级 0 / 生产 3 / 原型 10）；P0/P1 必须为 0
- 层 2：边际收益 gate（修复成本 > 危害 × 3 → 标记接受残留）
- 层 3：过拟合警报（增强版：P0 反弹 1 轮即 STOP / P1 反弹连续 2 轮 / P0/P1 持平走 4 轮窗口停滞观察 / 回归率 >30% → STOP 报告；被动验证见 references/01-review.md）
- 层 4：严重度门槛（P3 及以下不报；class-level instance 例外升级 P2）

**阶段出口条件**：真收敛（P0=0 AND P1=0 AND 连续 2 轮无新 P0/P1）→ 携带收敛曲线 + residual risk 进入 Phase 2。
- **条件 ACK 门禁**：residual risk 含 P1 及以上，或收敛判定含「接受残留」→ 必须等人类 `ACK + 风险接受` 才能进 Phase 2；仅 P2 残留 → 自动放行，但收尾报告须标注「待确认项」。

> 本阶段可与独立 skill [deep-review-loop](https://github.com/1273984347/deep-review-loop) 互换：装了独立 skill 时直接调用；未装时按本仓库 references/01-review.md 手动执行。

## Phase 2：收尾（Wrap-up）

**目标**：把 session 的状态、文档、记忆审计到「可交接」状态，并沉淀本次经验。

**核心协议**（详情见 [references/02-wrap-up.md](references/02-wrap-up.md)）：

1. **memory 健康检查**：目录规模 + P0/P1/P2 标记 + session 文件统计
2. **memory audit（5 phase）**：frontmatter / dup / empty / big-file / broken-link + 6 面状态矩阵
3. **fileCount sync**：实际文件数 vs 声明，drift >5% 告警
4. **文档同步 spot-check**：Grep 验证版本号 + 任务 ID 落地（**不信任 prior session 声明**）+ work-log 追加 4 段 schema
5. **经验沉淀（sediment）**：Read-before-Edit → Grep-verify-after-Edit → 毕业判据分流
6. **4-step verify**：file exists / content count / link target / 行数
7. **反向验证**：Grep spot-check memory 层 + 调用 Phase 1 审查收尾本身

**阶段出口条件**：收尾报告（影响 / 改动 / 待确认 / 遗留）+ sediment 记录 → 进入 Phase 3。

> 本阶段可与独立 skill [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) 互换。

## Phase 3：沉淀（Evolution）

**目标**：把 session 的经验升级为可复利的规则，喂回下一 session。

**核心协议**（详情见 [references/03-evolution.md](references/03-evolution.md)）：

1. **快速模式**（默认，任务完成自动）：3 问自检 → 写入 experience-log / quickref / skill-usage-checklist
2. **全面模式**（周汇总 / 用户要求）：11 维度分析 → retrospective.md → 多件套 sync verify
3. **知识层升级**：experience → pattern → heuristic → policy（policies 需人工确认）
4. **行动项分流**：P0/P1 立即执行，P2 等确认，P3 只记录

**阶段出口条件**：复利经验入库 + 行动项清单（含待确认项）→ 闭环完成。

> 本阶段可与独立 skill [self-evolution](https://github.com/1273984347/self-evolution) 互换。

---

## memory 路径约定

本 skill 涉及 memory 操作时，使用占位符路径，按你的环境替换：

- `<memory_root>` = agent 的 memory 根目录（按平台映射：TRAE `~/.trae-cn/memory`；Claude Code `%USERPROFILE%\.claude\projects`（Windows）/ `~/Library/Application Support/Claude/projects`（macOS）；WorkBuddy `~/.workbuddy/memory/` 或项目内 `.workbuddy/memory/`；无现成 memory 系统时在项目内建 `.agent-memory/`）
- `<project-slug>` = 当前 workspace 对应的 memory 项目目录名（执行时按当前 cwd 映射）
- `<date>` = 当日日期目录（`YYYYMMDD`）

**路径预检（首次运行强制）**：
- 用占位符前必须先验证路径存在：`test -e <memory_root>`（macOS/Linux）或 `Test-Path <memory_root>`（Windows）。
- **预检失败 → 中断并问用户**，不允许用「猜测的路径」继续跑流水线。
- **Grep 空结果判别**：Grep 返回 0 hits 时，先确认是「路径错误 / 文件不存在」还是「内容真无匹配」——用 `test -e` 验证目标文件/目录存在后再下结论；无法区分时标 `unverifiable` 并询问用户，**不得把「空结果」当「通过」**。

**文件结构约定**：

```
<memory_root>/
├── user_profile.md                          # 用户级偏好与铁律（跨项目）
├── knowledge/
│   ├── patterns/                            # 经验升级：pattern 层
│   ├── heuristics/                          # 经验升级：heuristic 层
│   └── policies/                            # 经验升级：policy 层（需人工确认）
└── projects/<project-slug>/
    ├── project_memory.md                    # 项目级规则
    ├── experience-log.md                    # 经验记录权威源
    ├── experience-quickref.md               # 速查表
    ├── skill-usage-checklist.md             # Skill 使用检查清单
    └── <date>/
        ├── work-log.md                      # 收尾 work-log（4 段 schema）
        ├── topics.md                        # 近期 topic
        └── retrospective.md                 # 全面复盘报告
```

## Verdict 字眼合规自检
- 全文 Grep 禁词：`完成|PASS|12/12|闭环|OK|没问题|looks good`
- 用「数据 + 实证 + residual risk 列表」代替 verdict 字眼
- 历史 log 文件例外（引用过往 verdict 不算违规）

## Failure handling
- 任一步骤失败 → 不继续下一步，stderr 报告
- 裁剪必须显式标注 `not-applicable` + 理由，不允许静默跳过
- Token 超额（Phase 1 派 3 subagent）→ 降级为 1 subagent / 分批派 / 等 user 拍板

## Self-Disclosure
- 0 verdict 字眼
- 三阶段按序执行，被裁剪阶段显式标注 `not-applicable`
- Phase 1 必出收敛曲线 + ≥3 residual risk
- Phase 2 必出收尾报告 + 验证铁律 spot-check（项目层 + memory 层）
- Phase 3 必出 sediment / 复盘报告 + 多件套 sync verify
- 4 层过拟合防护必走（P2 残留 N / 边际收益 gate / 过拟合警报 / 严重度门槛）

## Reference
- **组成**：三阶段分别对应独立 skill [deep-review-loop](https://github.com/1273984347/deep-review-loop) / [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) / [self-evolution](https://github.com/1273984347/self-evolution)；本仓库为整合流水线，references/ 为各阶段详案
- **设计来源**：从真实编码会话中蒸馏的「三 skill 闭环」（2026-07 建立）——审查 → 收尾 → 沉淀，多次假收敛 / 声明未落地教训固化
