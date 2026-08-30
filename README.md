<div align="center">

**中文** · [English](./README.en.md)

</div>

# agent-session-loop

> 一条流水线管理 Agent 会话的完整生命周期：**深度复检（审查）→ 7 步收尾 → 复盘沉淀**。

[![license](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![CI](https://github.com/1273984347/agent-session-loop/actions/workflows/validate.yml/badge.svg)](https://github.com/1273984347/agent-session-loop/actions/workflows/validate.yml)
[![skills-ref](https://img.shields.io/badge/skills--ref-passing-2ea44f)](https://agentskills.io)
[![version](https://img.shields.io/badge/version-v1.0.1-1d76db)](https://github.com/1273984347/agent-session-loop/releases/latest)

> "AI 会话很少在做事的时候崩溃，多半是在收尾的时候：结论没验证就宣布完成，经验没沉淀就关窗走人，下一个 session 从零开始。"

你大概也遇到过：审查、收尾、复盘这三个动作每个都在做，但每次都靠手动提醒、凭自觉、看心情——漏掉一个，整条闭环就断了。本仓库把三个独立 skill（`deep-review-loop` / `mem-wrap-up` / `self-evolution`）串成一条可独立使用的会话生命周期流水线，每个 session 结束时按序闭环，把「验证过的结论」沉淀为「可复用的经验」。

## 流水线

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

阶段输入输出契约：

| 交接点 | 上游产出 | 下游消费 |
|:---|:---|:---|
| 审查 → 收尾 | 收敛曲线 + ≥3 residual risk | 收尾的验证清单 + 待沉淀项 |
| 收尾 → 沉淀 | sediment（编号+5Why 链）+ work-log | 复盘维度的输入 |
| 沉淀 → 下一 session | 知识层升级 + 行动项 | 下次会话的规则与 checklist |

## 安装

标准 Agent Skill（`SKILL.md` + `references/`），任何支持 Agent Skills 的客户端都能装。三种方式任选：

**方式 A：自然语言安装（推荐）**

在 Claude Code、Codex 等支持 Agent Skills 的工具里，直接说：

```text
帮我安装这个 skill：https://github.com/1273984347/agent-session-loop
```

Agent 会自动 clone 到 skills 目录并注册，不用手动找路径。工具不支持时，手动复制：

```bash
git clone https://github.com/1273984347/agent-session-loop.git
cp -r agent-session-loop <your-skills-dir>/agent-session-loop
```

**方式 B：Claude Code 插件市场（一条命令）**

```text
/plugin marketplace add 1273984347/agent-session-loop
/plugin install agent-session-loop@agent-session-loop
```

**方式 C：skills.sh CLI（Agent 界的 npm）**

```bash
# npx 首次运行会自动下载 skills CLI，无需全局安装
npx skills add https://github.com/1273984347/agent-session-loop
```

**搭配独立 skill**——如果你只需要某一阶段，可单独安装：
- [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查）
- [mem-wrap-up](https://github.com/1273984347/mem-wrap-up)（收尾）
- [self-evolution](https://github.com/1273984347/self-evolution)（沉淀）

## 使用

会话收尾、批量修复/长文档完成后、用户说「收尾 / 复检 / 复盘 / retro」时，agent 会自动激活本 skill 并按三阶段执行。

**按场景裁剪**（裁剪必须显式标注 `not-applicable`，不允许静默跳过）：

| 场景 | 必走 | 可裁剪 |
|:---|:---|:---|
| 纯调试 session | Phase 2 收尾（最小化） | Phase 1 / 3 标 `not-applicable` |
| 批量修复 / 长文档 | Phase 1 审查（全量） | Phase 3 用快速模式 |
| 周汇总 / 明确复盘 | Phase 3 全面模式 | Phase 1 降为 R0 |
| 完整 session 收尾 | 全三阶段 | — |

## 环境适配

- **路径占位符（首次使用必读）**：正文使用 `<memory_root>` / `<project-slug>` 占位符，执行前先替换：
  - `<memory_root>` = agent 的 memory 根目录。常见环境：TRAE → `~/.trae-cn/memory`；Claude Code → `%USERPROFILE%\.claude\projects`（Windows）/ `~/Library/Application Support/Claude/projects`（macOS）；WorkBuddy → `~/.workbuddy/memory/` 或项目内 `.workbuddy/memory/`；无现成 memory 系统时，在项目内建 `.agent-memory/` 即可。
  - `<project-slug>` = 当前 workspace 的项目目录名（如 `open-source`）。
  - **不确定怎么填？** 先 `ls`（macOS/Linux）/ `Get-ChildItem`（Windows）查看你的 agent 环境已有目录，对照上述示例再替换；**不要凭空猜路径**。若环境确无 memory 系统，相关步骤标 `not-applicable`，不编造证据。
- **工具**：文件搜索（Grep/Read/LS）+ shell（PowerShell 示例，macOS/Linux 用 bash/zsh 等价命令，见 SKILL.md「命令示例（Windows PowerShell ↔ macOS/Linux POSIX）」）；subagent/task 派生为**可选能力**——无则自动走降级模式（见 SKILL.md「无子代理平台的降级模式」：串行替代并行，显式标注 `degraded (no-subagent)`）。
- **MCP 扩展**：本 skill 与 MCP **互补**——MCP 提供外部工具/数据连接，本 skill 教 agent 如何编排这些工具的复杂工作流。如需接入 MCP，把 MCP server 作为**可选工具**声明（如 `compatibility` 字段注明「需要 X MCP 时使用」，无 MCP 时回退到内建工具），不要把 skill 绑定死在特定 server 上。

## 版本兼容性

| 检查项 | 值 |
|---|---|
| SKILL.md 版本 | 1.0.1 |
| Agent Skills 标准 | 兼容（[agentskills.io](https://agentskills.io) 开放标准，frontmatter: name/description/license/metadata） |
| CI 门禁 | 五步：`skills-ref validate` + `python evals/validate.py` + `python evals/run_behavior.py` + `python scripts/version-lint.py` + `python scripts/fragment-lint.py`（见 [.github/workflows/validate.yml](.github/workflows/validate.yml)） |
| 运行依赖 | skill 运行：文件搜索（Grep/Read）+ 可选 shell；subagent 可选（无则降级）；CI lint 脚本仅开发期需要 |
| MCP 依赖 | 无（可选接入） |
| 联动 skill | [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查）/ [mem-wrap-up](https://github.com/1273984347/mem-wrap-up)（收尾）/ [self-evolution](https://github.com/1273984347/self-evolution)（沉淀）——不装也能独立运行 |

**客户端兼容矩阵**：

| 客户端 | 安装方式 | 支持 |
|---|---|---|
| Claude Code | `/plugin marketplace add` 或复制目录 | ✅ |
| Codex / Cursor / OpenCode 等 | 复制目录（Agent Skills 标准客户端） | ✅ |
| WorkBuddy / QwenWork / TRAE | 复制目录到 skills 目录，自动注册 | ✅ |
| 其他 | 需支持 SKILL.md frontmatter + 渐进披露 | 视实现 |

## 许可证

[Apache-2.0](LICENSE)

## 相关仓库

| 仓库 | 定位 |
|:---|:---|
| [deep-review-loop](https://github.com/1273984347/deep-review-loop) | 独立版：5 轮深度复检 |
| [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) | 独立版：7 步收尾 |
| [self-evolution](https://github.com/1273984347/self-evolution) | 独立版：复盘沉淀 |
