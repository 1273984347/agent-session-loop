# 把 Agent 会话管成一条流水线：审查 → 收尾 → 沉淀，我开源了三个 Skill

> 用 AI 开发的人越来越多，但大多数人和 AI 的协作方式是「用完即走」：
> 任务做完了，结论没验证，经验没沉淀，下一个 session 又从零开始。
> 这篇文章分享我怎么用三个 Agent Skill 把会话管成一条可复利的流水线，并已经全部开源。

---

## 一、三个真实痛点

先说我遇到的三个问题，你可能也踩过。

**痛点 1：假收敛。**
让 Agent 批量修 bug 或写一份长文档，它做完会说「0 问题，完成」。结果你让它再仔细查一遍，立刻翻出五六个问题。不是它骗你——是它只做了**一次**浅层检查就下了结论。更糟的是，它自己还会给「看起来完整」的东西打包票。

**痛点 2：收尾靠记忆。**
session 结束了，改了哪些文件、验证过什么、有什么待确认项——全靠 agent 脑子里的上下文。换个 session，全丢了。文档说「已同步」，其实文件根本没改；代码说「已修复」，git 里根本没提交。

**痛点 3：经验不沉淀。**
这次踩的坑、找到的方法、写的一次性脚本，用完就扔。下个 session 遇到同样问题，重新踩一遍。Agent 不会自己「长记性」，除非你把记性变成协议。

这三个痛点的共同根源是：**Agent 的 session 没有生命周期管理**。我开始把它当成一个工程问题来解决——于是有了三个 Skill 组成的闭环。

## 二、解决方案：三 Skill 闭环

```
  审查（Review）  →   收尾（Wrap-up）  →   沉淀（Evolution）
  5 轮深度复检         7 步收尾流水线         双模式复盘
  不收敛不收尾         不验证不交接            不复利不闭环
```

三个 Skill 各自独立、可单独安装，也可以组合成一条流水线：

| Skill | 定位 | 核心机制 |
|---|---|---|
| [deep-review-loop](https://github.com/1273984347/deep-review-loop) | 审查 | 5 轮复检（R0-R3）+ 4 层过拟合防护 |
| [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) | 收尾 | 7 步流水线 + 6 面状态矩阵 + 验证铁律 |
| [self-evolution](https://github.com/1273984347/self-evolution) | 沉淀 | 3 问自检 / 11 维度复盘 + 知识升级 |

如果你想一步到位，还有个整合版 [agent-session-loop](https://github.com/1273984347/agent-session-loop)，把三步编成一条完整的会话生命周期流水线。

下面逐个讲它们解决什么问题、怎么做到的。

## 三、deep-review-loop：把「审查」变成真循环

核心是一条铁律：**绝不允许假收敛**。

普通的审查是「审查 → 修复 → 验证」一次完事。这个 Skill 把它改成：

```
审查 → 修复 → 重新审查 → 修复 → 重新审查 → …直到连续 N 轮无新问题
```

具体是 5 轮协议：

- **R0**：表面检查。查文件大小、查「完成/PASS/OK」这类 verdict 字眼（自证反模式的信号）、判定项目阶段。
- **R1a**：派 3 个独立 subagent 交叉验证，三个视角：**事实准确性**（数字/路径/引用）、**覆盖度**（声明 vs 实际）、**可复用性**（陌生人能不能照着做）。
- **R1b**：派 1 个对抗性 subagent，**默认你有罪**（default refuted=true），主动找茬而不是顺着你。
- **R2**：独立审计，而且明确禁止「自己审自己」（Self-audit ≠ 独立审计）。
- **R3**：必须写 ≥3 条残余风险 + 收敛曲线，即使 0 finding 也要写。

**反过拟合**是这个 Skill 的另一半。它知道审查可能「越修越多」——所以有 4 层防护：

1. **P2 残留 N**：P0/P1 必须为 0，但 P2（体验级）允许残留（比赛级 0 条/生产 3 条/原型 10 条），防止追求完美；
2. **边际收益 gate**：修复成本 > 问题危害 × 3，就标记「接受残留」；
3. **过拟合警报**：连续几轮问题数不降反升，或回归率 >30%，立刻 STOP 报告而不是硬修；
4. **严重度门槛**：P3 及以下不报，避免噪声。

还有一个细节值得抄：**每个 finding 必须附工具调用证据**。subagent 说「这个目录不存在」必须附上 LS 输出，说「某行有问题」必须附上 Read 输出，连「0 finding」也要附证据证明你真查了。这直接堵死了 subagent 编结论的路。

## 四、mem-wrap-up：把「收尾」变成可交接的状态

Session 结束不是「说再见」，是把状态审计到「可交接」。7 步流水线：

1. memory 健康检查
2. memory 审计（5 个 phase：frontmatter / 重复 / 空文件 / 超大文件 / 断链）+ **6 面状态矩阵**
3. 文件数同步检查
4. 文档同步 spot-check + work-log 记录
5. 经验沉淀（sediment）
6. 4 步 verify
7. memory 层复查 + 反向审查

**6 面状态矩阵**是我最喜欢的部分：把一致性拆成六个事实面——代码、运行态、文档、规则、记忆、工作区。每面必须标状态（已核实 / 待定 / 不适用）。小项目没部署，运行态就标 `not-applicable`，**不编造证据**。

**验证铁律**是这个 Skill 的灵魂：

> Grep spot-check 文件内容，验证版本号和任务 ID 实际落地，**不信任 prior session 的「已落地」声明**。

为什么？因为「Edit 成功」不等于「文件真改了」——old_string 不匹配会静默失败，并行 Edit 会互相覆盖，改完不验证就是白改。我在实际项目里被这个坑坑了十几次，最后固化成铁律：声明 ≠ 事实，验证才算数。

## 五、self-evolution：把「复盘」变成复利

最后一步是把 session 的经验变成可复用的规则。两种模式：

**快速模式**（每次任务完成自动跑）：3 问自检——有新发现吗？踩坑了吗？有 Skill 缺口吗？有就写进 experience-log，没有就跳过。成本极低，保证每次都做。

**全面模式**（周汇总/复盘时）：11 个维度深度分析——经验复用、技能评估、问题预防（强制 5Why）、工作流优化、一次性工具沉淀……其中两个维度**必走不可跳过**：

- **维度 9：一次性工具沉淀**。任务中临时写的脚本/命令，用完即弃还是沉淀成模板？撞 1 次也走，不等到撞满 3 次。
- **维度 11：复盘过程的复盘**。复盘本身有没有撞坑？这是元层兜底。

然后是**知识层升级**链路：

```
experience（经验）→ pattern（模式，≥3 次）→ heuristic（启发式，成功率>80%）→ policy（政策，需人工确认）
```

注意最后一级：`policy` 必须**人工确认**，AI 不能自己给自己立规矩。以及单一事实源原则——experience-log 是权威源，quickref 是索引，retrospective 是报告，**不复制成第二处真相**。

## 六、整合版：agent-session-loop

如果你不想管理三个 skill，[agent-session-loop](https://github.com/1273984347/agent-session-loop) 把三步编成一条流水线：

```
        Phase 1                 Phase 2                Phase 3
   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
   │  审查 (Review)  │ →  │  收尾 (Wrap-up) │ →  │  沉淀 (Evolution)│
   │ 5 轮深度复检     │    │ 7 步收尾流水线   │    │ 快速/全面复盘     │
   └────────────────┘    └────────────────┘    └────────────────┘
       收敛曲线+residual   收尾报告+sediment      复利经验+规则升级
```

每阶段的产出就是下一阶段的输入：审查的 residual risk 是收尾的验证清单，收尾的 sediment 是复盘的分析素材，复盘的规则升级喂回下一个 session。**上一轮的结论变成下一轮的起点，这就是复利。**

还支持按场景裁剪：纯调试 session 只走收尾；批量修复后重点走审查；周汇总重点走复盘。裁剪必须显式标注 `not-applicable`，**不允许静默跳过**。

## 七、工程化的细节：标准、CI、MCP

开源不是把 markdown 丢上 GitHub 就完事。我按 Agent Skills 开放标准（[agentskills.io](https://agentskills.io)）做了三件事：

**1. 遵循标准格式。** SKILL.md 的 frontmatter：`name` 必须等于目录名、小写+连字符、≤64 字符；`description` 双语、祈使句（「Use when…/当…时使用」）方便 agent 触发；加了 `license: Apache-2.0`。正文按**渐进披露**组织：SKILL.md 保持 <500 行，细节拆到 `references/`，agent 按需加载，不占上下文。

**2. CI 自动校验。** 每个仓库加了 GitHub Actions，用官方 `skills-ref validate` 校验 frontmatter 合规：

```yaml
- name: Validate SKILL.md
  run: skills-ref validate "$PWD"
```

从此每次 push 都会自动检查，格式不合规直接标红。

**3. 为 MCP 预留扩展位。** Skill 和 MCP 是互补的：MCP 提供外部工具/数据连接，Skill 教 Agent 如何编排这些工具的复杂工作流。所以这几个 skill 把 MCP 当**可选依赖**——有对应 MCP server 就用，没有就回退到内建工具，绝不绑死。

## 八、踩过的坑（开源才知道的）

开源过程本身就验证了审查的价值：

1. **UTF-8 BOM 坑**：文件开头带 BOM（EF BB BF），`skills-ref` 校验「SKILL.md 必须以 `---` 开头」直接失败。写文件的工具可能加 BOM，GitHub 不拦，但校验器拦。
2. **路径参数化**：原版 skill 里全是我的个人绝对路径（`C:\Users\...`）。开源版全部改成 `<memory_root>` / `<project-slug>` 占位符，README 里说明替换规则——**自己的 skill 自己先脱敏**。
3. **description 是触发命脉**：agent 只靠 name + description 决定要不要加载 skill。描述写得含糊，skill 就永远不会被触发；描述过宽，会在不该出现的时候刷存在感。

## 九、结尾

这三个 skill 对我最大的改变是：**AI 协作从「对话」变成了「复利」**。每次 session 结束，审查过的结论、收尾后的状态、沉淀下来的经验，都是下一次会话的起点。

仓库地址（Apache-2.0，欢迎 Star / PR / Issue）：

- [agent-session-loop](https://github.com/1273984347/agent-session-loop) —— 整合版流水线
- [deep-review-loop](https://github.com/1273984347/deep-review-loop) —— 审查
- [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) —— 收尾
- [self-evolution](https://github.com/1273984347/self-evolution) —— 沉淀

安装就是 clone 后把目录放进你 agent 的 skills 目录。如果你也在和 Agent 长期协作，试试把「审查、收尾、沉淀」做成自己的闭环——不用我的方案，但一定要有自己的闭环。
