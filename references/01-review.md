# Phase 1：审查（Deep Review）详案

> 本文件在 Phase 1 激活时读取。核心是「审查 → 修复 → **重新审查**」的真循环，直到连续 N 轮无新问题才判定收敛。

## 真循环铁律（最高优先级）

- **绝不允许假收敛**：不是「审查→修复→验证」单次流程，必须是循环，直到连续 N 轮重新审查均未发现新问题。
- **假收敛标志**：用 1 路快速审查（如仅 Grep）就判 0 问题，下一轮深度审查反弹。
- **真收敛标志**：问题数严格单调递减到 0，且下一轮重新审查仍未发现新问题。
- **每轮修复后必须重新审查**：修复可能引入回归（短路子句副作用、状态锁清理路径、事件拦截边界）。
- **收敛曲线必须记录**：每轮问题数（P0/P1/P2）单独记录，标注假/真收敛。

## 5 轮协议

| Round | 动作 | 执行者 | 状态 |
|:------|:-----|:-------|:----:|
| **R0** | 表面检查：file size + verdict 字眼 grep + 路径验证 + 项目阶段判定 | inline me | 必先跑 |
| **R1a** | 3 独立 verifier 交叉验证（factual / completeness / reusability） | 3 subagents parallel | 必派 |
| **R1b** | 对抗性审查（default refuted=true + class-level scope + 严重度门槛） | 1 subagent | 必派 |
| **R2** | 独立审计 + self-revision（NOT inline）+ 边际收益 gate | 1 subagent | 必派 |
| **R3** | ≥3 residual risk + 收敛曲线 + 过拟合警报 | inline me | 必走 |

### R0 surface check

1. **file size sanity**：Read 工具观察行数（目标 ≤500 行 / 5000 tokens）
2. **residual verdict words**：Grep pattern `完成|PASS|OK|没问题|12/12|闭环`，count 应 = 0
3. **expected hits 必现**：Grep pattern `R0|R1a|R1b|R2|R3|residual`，确认结构词命中
4. **项目阶段判定** → N_max：比赛级=0 / 生产=3 / 原型=10；判定依据优先级：user 声明 > 项目记忆 > cwd 推断 > 默认 3

### R1a 3 independent verifiers

3-lens split（缺一不算 R1a），单消息内发 3 个 parallel subagent：

| Verifier | Lens | Prompt 模板 |
|:---------|:-----|:------------|
| **A — Factual** | 数字/路径/引用准确 | 「Verify 文中每个数字/路径/引用 vs 源（Grep + Read trace 到 file:line）。每个 claim 必 trace。0 unverifiable = 0 finding。只做研究，不改代码。」 |
| **B — Completeness** | 覆盖度 | 「Verify 文段是否覆盖声明的 scope。0 missing = 0 finding。只做研究。」 |
| **C — Reusability** | 陌生人 cold-start | 「Verify 陌生人能否凭此文 cold-start 执行。路径全名 vs 缩写、命令完整 vs 缺参数、错误处理 vs happy-path-only。0 ambiguous = 0 finding。只做研究。」 |

**硬性要求（防 verifier 失误）**：
- 每个 finding 必须附 ≥1 个工具调用输出（LS/Read/Grep/Glob）作为 Trace evidence；禁止二手转述
- 「目录/文件存在或缺失」声明必须附 LS/Read 输出；「file:line」声明必须附 Read 输出
- 0 finding 也必须附 ≥1 个工具输出证明「已实际执行验证」
- subagent prompt 必须 inline 包含上述硬性要求（subagent 无文档访问权限）
- 违反 → 该 finding 视为「未验证」，不计入收敛判定，重新派

### R1b adversarial subagent

Prompt 必须含：default refuted=true + 严重度门槛（P0 崩溃/安全/数据丢失；P1 核心功能失效；P2 体验问题记录不强制修；P3 不报，class-level instance 例外升级 P2）+ 4 必做任务：
1. Attack R1a 判定 + verdict self-claim + silent skip
2. Class-level enumeration：先 Grep 定位相关目录，再列 ALL affected files
3. 用与 R1a 不同的工具/视角
4. 0 finding 也要给 ≥3 residual risk

### R2 independent audit

**NOT inline**（Self-audit ≠ 独立审计）。Tasks：交叉核对 R1a/R1b findings（claim vs evidence）→ 矛盾优先级裁决 → memory sync 审计 → verdict grep 审计 → **边际收益 gate**（修复成本 > 危害 × 3 → 标记「建议接受残留」+ 理由）。

### R3 convergence + residual + alarms

**Residual risk 必含 3 类**（各附 fresh verification command + exit code + output 截取）：
1. subagent 盲点 2. sample/time-point 3. 跨 session

**收敛曲线模板**（必记）：
```
Round N: P0=0 / P1=0 / P2≤N_max / 接受残留=P1:A1/P2:A2 / 回归率≤30% (真收敛，连续 2 轮 P0/P1 0 新发现)
```

**过拟合警报**（触发任一 → STOP 报告）：
- 警报 A：P0 反弹 1 轮即 STOP；P1 反弹连续 2 轮；P0/P1 持平连续 4 轮（停滞型）。例外：边际收益 gate 接受的残留导致的持平不触发
- 警报 B：某轮回归率 >30%

**收敛判定表**：

| 条件 | 判定 |
|:-----|:-----|
| P0=0 AND P1=0 AND 连续 2 轮无新 P0/P1 | ✅ 真收敛（硬条件最优先） |
| P2 ≤ N_max | ✅ 允许残留 |
| 警报 A/B | ❌ STOP 报告（优先级最高） |
| 修复成本 > 危害 × 3 | ⚠️ 接受残留 |
| 优先级 | 警报 A/B > 边际收益 gate > P2 超标 |

## 5 步独立 verify（V1-V5）

| 步 | 内容 |
|:---|:---|
| V1 | file exists + content count + link target + 行数 |
| V2 | 5 步 grep 范式（size / 残留 / 期望 hits / 期望 0 hits / post-fix 实证） |
| V3 | verdict 字眼 grep（`完成|PASS|OK|没问题|12/12|闭环`，历史 log 例外） |
| V4 | memory sync 4 维度（user 偏好 / 项目规则 / topics / retrospective） |
| V5 | 3-case dry-run（best / worst / null），一次性工具必跑 |

## 防跳轮三件套

1. **Pressure Scenarios**（5 类压力）：时间压力+测试通过 / 用户紧急+单文件 / 自证+看起来完整 / docs-only / meta-skill 自身修改——每类都要「仍跑全轮」
2. **Rationalization Table**：6 类借口（「tests 都过了」「用户急」「0 finding」「manual check 过」「单文件」「本 skill 不用自审」）→ 全部反驳
3. **Red Flags**：跳过任一 round 无 justification / verdict 字眼 / R3 写 0 residual / R1a 缺 3-lens / 证据缺失 / R2 inline → 任一命中 STOP

## 触发场景

- plan / spec / quickref / skill / long-doc 写完后
- 批量修复（>10 项）后
- user 说「deep review / 复检 / 收敛 / DRL」
- 本 skill 自身修改后（meta-skill 闭环）
- 怀疑假收敛时
