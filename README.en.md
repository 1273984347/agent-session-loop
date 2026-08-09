<div align="center">

[中文](./README.md) · **English**

</div>

# agent-session-loop

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
npm install -g @anthropic-ai/skills
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

- **Paths**: use `<memory_root>` / `<project-slug>` placeholders — replace per your agent environment (e.g. TRAE `.trae-cn/memory`, Claude Code projects dir, or in-repo `.agent-memory`).
- **Tools**: needs subagent/task spawning + file search (Grep/Read/LS) + shell (PowerShell examples; adjust per platform).
- **MCP extension**: this skill and MCP are **complementary** — MCP provides external tool/data connections; the skill teaches the agent how to orchestrate complex workflows over those tools. To integrate MCP, declare the server as an **optional tool** (e.g. note "use when X MCP is needed" in `compatibility`, falling back to built-in tools without it) — never hard-bind the skill to a specific server.

## License

[Apache-2.0](LICENSE)

## Related repos

| Repo | Role |
|:---|:---|
| [deep-review-loop](https://github.com/1273984347/deep-review-loop) | Standalone: 5-round deep review |
| [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) | Standalone: 7-step wrap-up |
| [self-evolution](https://github.com/1273984347/self-evolution) | Standalone: retro & sedimentation |
