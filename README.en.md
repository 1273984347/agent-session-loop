<div align="center">

[中文](./README.md) · **English**

</div>

# agent-session-loop

[![license](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![CI](https://github.com/1273984347/agent-session-loop/actions/workflows/validate.yml/badge.svg)](https://github.com/1273984347/agent-session-loop/actions/workflows/validate.yml)
[![skills-ref](https://img.shields.io/badge/skills--ref-passing-2ea44f)](https://agentskills.io)
[![version](https://img.shields.io/badge/version-v1.0.1-1d76db)](https://github.com/1273984347/agent-session-loop/releases/latest)

> One pipeline managing the full lifecycle of an agent session: **deep review (review) → 7-step wrap-up → retro evolution**.

> "Agent sessions rarely break while working — usually at wrap-up: conclusions declared done without verification, experience closed away unsedimented, and the next session starts from zero."

You've probably seen it too: review, wrap-up, and retro are all being done — but every time they rely on manual reminders, goodwill, and mood. Miss one, and the whole loop breaks. This repo strings three standalone skills (`deep-review-loop` / `mem-wrap-up` / `self-evolution`) into a single, standalone session-lifecycle pipeline: every session closes in order, turning "verified conclusions" into "reusable experience."

## Pipeline

```
        Phase 1                 Phase 2                Phase 3
   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
   │ Review          │ →  │ Wrap-up         │ →  │ Evolution      │
   │ 5-round deep    │    │ 7-step pipeline │    │ quick/full retro│
   │ R0→R3 + V1→V5   │    │ memory audit    │    │ 11 dims + upgrade│
   └────────────────┘    └────────────────┘    └────────────────┘
       output: verdict       output: wrap-up       output: compounding
       + residual risk        + sediment            experience + rules
```

Handoff contract:

| Handoff | Upstream output | Downstream consumption |
|:---|:---|:---|
| Review → Wrap-up | convergence curve + ≥3 residual risks | wrap-up verification checklist + items to sediment |
| Wrap-up → Evolution | sediment (numbered + 5-Why chain) + work-log | inputs for the retro dimensions |
| Evolution → next session | knowledge-layer upgrades + action items | rules & checklists for the next session |

## Installation

A standard Agent Skill (`SKILL.md` + `references/`), installable by any Agent Skills client. Pick one:

**Option A: natural-language install (recommended)**

In Claude Code, Codex, or any Agent Skills client, just say:

```text
Install this skill: https://github.com/1273984347/agent-session-loop
```

The agent clones it into your skills directory and registers it automatically. If your tool doesn't support that, copy it manually:

```bash
git clone https://github.com/1273984347/agent-session-loop.git
cp -r agent-session-loop <your-skills-dir>/agent-session-loop
```

**Option B: Claude Code plugin marketplace (one command)**

```text
/plugin marketplace add 1273984347/agent-session-loop
/plugin install agent-session-loop@agent-session-loop
```

**Option C: skills.sh CLI (the npm of agents)**

```bash
# npx downloads the CLI on first run; no global install needed
npx skills add https://github.com/1273984347/agent-session-loop
```

**Prefer standalone skills?** If you only need one phase, install them individually:
- [deep-review-loop](https://github.com/1273984347/deep-review-loop) (review)
- [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) (wrap-up)
- [self-evolution](https://github.com/1273984347/self-evolution) (evolution)

## Usage

The agent auto-activates this skill and runs the three phases on session wrap-up, after batch fixes / long docs, or when you say "wrap up / 复检 / 复盘 / retro".

**Trim by scenario** (trimming must be explicitly marked `not-applicable`, never silently skipped):

| Scenario | Required | Can trim |
|:---|:---|:---|
| Pure debugging session | Phase 2 wrap-up (minimal) | Phases 1 / 3 → `not-applicable` |
| Batch fix / long doc | Phase 1 review (full) | Phase 3 → quick mode |
| Weekly summary / explicit retro | Phase 3 full mode | Phase 1 → R0 |
| Full session wrap-up | All three phases | — |

## Environment

- **Path placeholders (read before first use)**: the skill uses `<memory_root>` / `<project-slug>` placeholders — replace them before running:
  - `<memory_root>` = your agent's memory root. Common setups: TRAE → `.trae-cn/memory`; Claude Code → projects dir; WorkBuddy → `~/.workbuddy/memory/` or in-repo `.workbuddy/memory/`; if no memory system exists, create an in-repo `.agent-memory/`.
  - `<project-slug>` = the current workspace's project dir name (e.g. `open-source`).
  - **Not sure?** Run `ls` (POSIX) / `Get-ChildItem` (PowerShell) to inspect your agent environment's existing dirs, then map against the examples above; **never guess paths**. If the environment truly has no memory system, mark the step `not-applicable` — never fabricate evidence.
- **Tools**: file search (Grep/Read/LS) + shell (PowerShell examples; see the "工具名映射（跨平台）" section of SKILL.md for per-platform tool mapping and POSIX equivalents); subagent/task spawning is **optional** — without it, the skill falls back to the degradation mode (see SKILL.md「无子代理平台的降级模式」: serial instead of parallel, explicitly marked `degraded (no-subagent)`).
- **MCP extension**: this skill and MCP are **complementary** — MCP provides external tool/data connections; the skill teaches the agent how to orchestrate complex workflows over those tools. To integrate MCP, declare the server as an **optional tool** (e.g. note "use when X MCP is needed" in `compatibility`, falling back to built-in tools without it) — never hard-bind the skill to a specific server.

## Version compatibility

| Check | Value |
|---|---|
| SKILL.md version | 1.0.1 |
| Agent Skills standard | Compatible ([agentskills.io](https://agentskills.io); frontmatter: name/description/license/metadata) |
| CI gate | Five steps: `skills-ref validate` + `python evals/validate.py` + `python evals/run_behavior.py` + `python scripts/version-lint.py` + `python scripts/fragment-lint.py` (see [.github/workflows/validate.yml](.github/workflows/validate.yml)) |
| Runtime deps | Skill runtime: file search (Grep/Read) + optional shell; subagent optional (degradation mode when absent); CI lint scripts are dev-time only |
| MCP deps | None (optional) |
| Linked skills | [deep-review-loop](https://github.com/1273984347/deep-review-loop) / [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) / [self-evolution](https://github.com/1273984347/self-evolution) — works standalone |

**Client compatibility**:

| Client | Install method | Support |
|---|---|---|
| Claude Code | `/plugin marketplace add` or copy folder | ✅ |
| Codex / Cursor / OpenCode etc. | Copy folder (Agent Skills standard clients) | ✅ |
| WorkBuddy / QwenWork / TRAE | Copy folder into skills dir, auto-registered | ✅ |
| Others | Requires SKILL.md frontmatter + progressive disclosure | Depends |

## License

[Apache-2.0](LICENSE)

## Related repos

| Repo | Role |
|:---|:---|
| [deep-review-loop](https://github.com/1273984347/deep-review-loop) | Standalone: 5-round deep review |
| [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) | Standalone: 7-step wrap-up |
| [self-evolution](https://github.com/1273984347/self-evolution) | Standalone: retro & sedimentation |
