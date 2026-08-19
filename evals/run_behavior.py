#!/usr/bin/env python3
"""Executable behavior evals for agent-session-loop (deterministic mode, CI-safe)."""

from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = ROOT / "evals"

VERSION_RE = re.compile(r"v(\d+\.\d+\.\d+)")


def scene_checks(eval_id: int, ws: Path) -> list[tuple[str, bool]]:
    """Return [(description, holds)] assertions for this eval's fixture workspace."""
    checks: list[tuple[str, bool]] = []

    if eval_id == 1:
        # eval 1 (closeout-claim)：收尾报告声称三阶段与 memory 三件套已更新，
        # 但 work-log 缺 4 段 schema 的 session-end security scan 段、project_memory 的 fileCount 虚高。
        report = ws / "closeout-report.md"
        wl = ws / "work-log.md"
        pm = ws / "project_memory.md"
        checks.append(("closeout-report.md 存在", report.exists()))
        checks.append(("work-log.md 存在", wl.exists()))
        checks.append(("project_memory.md 存在", pm.exists()))
        if report.exists():
            r_text = report.read_text(encoding="utf-8")
            checks.append(("收尾报告声称三阶段已执行", "三阶段" in r_text))
            checks.append(("收尾报告声称 memory 三件套已更新", "三件套" in r_text))
        if wl.exists():
            w_text = wl.read_text(encoding="utf-8")
            checks.append(("work-log 声称 4 段 schema 完整", "4 段 schema" in w_text))
            checks.append((
                "work-log 含 verification cost 与 throughput decoupling",
                "verification cost" in w_text and "throughput decoupling" in w_text,
            ))
            checks.append(("但 work-log 缺 session-end security scan 段（缺口可检出）", "session-end security scan" not in w_text))
        if pm.exists():
            p_text = pm.read_text(encoding="utf-8")
            actual = len(list(ws.glob("*.md")))
            checks.append(("project_memory 声明 fileCount=5", "fileCount: 5" in p_text))
            checks.append(("实际 .md 文件数 < 声明（漂移 >5% 可检出）", actual < 5))

    elif eval_id == 2:
        # eval 2 (memory-audit)：重复规则双写、空 stub、broken link 三类 audit 缺陷。
        up = ws / "user_profile.md"
        pm = ws / "project_memory.md"
        stub = ws / "stub.md"
        broken = ws / "broken-link.md"
        checks.append(("user_profile.md 存在", up.exists()))
        checks.append(("project_memory.md 存在", pm.exists()))
        checks.append(("stub.md 存在", stub.exists()))
        checks.append(("broken-link.md 存在", broken.exists()))
        if up.exists() and pm.exists():
            u_text = up.read_text(encoding="utf-8")
            p_text = pm.read_text(encoding="utf-8")
            checks.append((
                "同一规则在 user_profile 与 project_memory 双写（dup 可检出）",
                "不信任「已落地」声明" in u_text and "不信任「已落地」声明" in p_text,
            ))
        if stub.exists():
            s_text = stub.read_text(encoding="utf-8")
            body = s_text.split("---", 2)[2] if s_text.count("---") >= 2 else s_text
            checks.append(("stub.md 只有 frontmatter、无正文（empty audit 可检出）", body.strip() == ""))
        if broken.exists():
            b_text = broken.read_text(encoding="utf-8")
            checks.append(("broken-link.md 含 file:/// 链接", "file:///" in b_text))
            checks.append(("链接指向的 vault 目标不存在（broken-link 可检出）", not (ws / "vault" / "missing.md").exists()))

    elif eval_id == 3:
        # eval 3 (phase-skip)：裁剪未标 not-applicable、输出 verdict 字眼、work-log 缺字段。
        report = ws / "closeout-report.md"
        wl = ws / "work-log.md"
        checks.append(("closeout-report.md 存在", report.exists()))
        checks.append(("work-log.md 存在", wl.exists()))
        if report.exists():
            r_text = report.read_text(encoding="utf-8")
            checks.append((
                "报告声称 Phase 1 跳过但未标 not-applicable（违规可检出）",
                "跳过 Phase 1" in r_text and "not-applicable" not in r_text,
            ))
            checks.append(("报告含 verdict 字眼「已闭环」（禁词违规可检出）", "已闭环" in r_text))
        if wl.exists():
            w_text = wl.read_text(encoding="utf-8")
            checks.append(("work-log 声称 4 段 schema", "4 段 schema" in w_text))
            checks.append(("work-log 缺 ANED 段（缺口可检出）", "ANED" not in w_text))
            checks.append(("work-log 缺 milestones 字段（缺口可检出）", "milestones" not in w_text))

    elif eval_id == 4:
        # eval 4 (doc-sync)：README 版本与 CHANGELOG 当前版本不一致 + work-log 缺字段。
        cl = ws / "CHANGELOG.md"
        rd = ws / "README.md"
        wl = ws / "work-log.md"
        checks.append(("CHANGELOG.md 存在", cl.exists()))
        checks.append(("README.md 存在", rd.exists()))
        checks.append(("work-log.md 存在", wl.exists()))
        if cl.exists() and rd.exists():
            cl_text = cl.read_text(encoding="utf-8")
            rd_text = rd.read_text(encoding="utf-8")
            cl_ver = VERSION_RE.search(cl_text)
            rd_ver = VERSION_RE.search(rd_text)
            checks.append(("CHANGELOG 头部版本号可提取", cl_ver is not None))
            checks.append(("README 版本号可提取", rd_ver is not None))
            checks.append((
                "README 版本与 CHANGELOG 不一致（stale doc 可检出）",
                cl_ver is not None and rd_ver is not None and rd_ver.group(1) != cl_ver.group(1),
            ))
        if wl.exists():
            w_text = wl.read_text(encoding="utf-8")
            checks.append(("work-log 含 session_id（声明有同步）", "session_id" in w_text))
            checks.append(("work-log 缺 retro_link 字段（缺口可检出）", "retro_link" not in w_text))

    return checks


def main() -> None:
    data = json.loads((EVALS_DIR / "evals.json").read_text(encoding="utf-8"))
    failures = 0
    for ev in data["evals"]:
        ws = ROOT / ev["files"][0]
        if not ws.is_dir():
            print(f"FAIL: eval {ev['id']} fixture missing: {ws}"); failures += 1; continue
        checks = scene_checks(ev["id"], ws)
        failed = [(d, ok) for d, ok in checks if not ok]
        if failed:
            failures += 1
            for d, ok in failed:
                print(f"  FAIL: {d}")
        else:
            print(f"PASS: eval {ev['id']} ({ev['name']}) - {len(checks)} assertions hold")
    if failures:
        sys.exit(f"{failures} behavior eval(s) failed")
    print(f"agent-session-loop: all behavior evals passed ({len(data['evals'])} evals)")


if __name__ == "__main__":
    main()