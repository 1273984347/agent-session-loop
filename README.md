# agent-session-loop

> 一条流水线管理 Agent 会话的完整生命周期：**深度复检（审查）→ 7 步收尾 → 复盘沉淀**。

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
npm install -g @anthropic-ai/skills
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

- **路径**：正文使用 `<memory_root>` / `<project-slug>` 占位符，按你的 agent 环境替换（如 TRAE `.trae-cn/memory`、Claude Code projects 目录，或项目内 `.agent-memory`）。
- **工具**：需要 subagent/task 派生能力 + 文件搜索工具（Grep/Read/LS）+ shell（PowerShell 示例，跨平台需相应调整）。
- **MCP 扩展**：本 skill 与 MCP **互补**——MCP 提供外部工具/数据连接，本 skill 教 agent 如何编排这些工具的复杂工作流。如需接入 MCP，把 MCP server 作为**可选工具**声明（如 `compatibility` 字段注明「需要 X MCP 时使用」，无 MCP 时回退到内建工具），不要把 skill 绑定死在特定 server 上。

## 许可证

[Apache-2.0](LICENSE)

## 相关仓库

| 仓库 | 定位 |
|:---|:---|
| [deep-review-loop](https://github.com/1273984347/deep-review-loop) | 独立版：5 轮深度复检 |
| [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) | 独立版：7 步收尾 |
| [self-evolution](https://github.com/1273984347/self-evolution) | 独立版：复盘沉淀 |
