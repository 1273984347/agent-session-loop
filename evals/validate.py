#!/usr/bin/env python3
"""Deterministic structural regression checks for the agent-session-loop skill.

Validates that SKILL.md stays compliant with the Agent Skills standard AND keeps the
session-lifecycle protocol contracts (three-phase pipeline, convergence curve,
verification iron law, work-log schema, knowledge upgrade) intact, plus consistency
between the skill and its eval fixtures. Runs in CI (pure stdlib, no third-party deps).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
EVALS_DIR = ROOT / "evals"

# Trigger markers that must stay in the description (see agentskills.io trigger contract).
EXPLICIT_MARKERS = ("收尾", "wrap up", "复检", "复盘", "retro")

# Protocol phrases that must stay in the SKILL.md body — losing any of these breaks the pipeline.
REQUIRED_PHRASES = (
    "三阶段",          # review → wrap-up → evolution pipeline
    "收敛曲线",         # Phase 1 must output a convergence curve
    "residual",        # >=3 residual risks
    "边际收益",         # anti-overfit layer 2
    "过拟合",          # anti-overfit framing
    "not-applicable",  # explicit pruning, no silent skip
    "验证铁律",         # claims ≠ facts, spot-check required
    "4 段 schema",     # work-log append format
    "sediment",        # experience sedimentation
    "work-log",        # 4-section work log
    "11 维度",         # full retro mode
    "知识层升级",       # experience → pattern → heuristic → policy
    "不编造证据",       # no fabricated evidence
)


def folded_description(frontmatter: str) -> str:
    """Reconstruct the folded description scalar from YAML frontmatter."""
    lines = frontmatter.splitlines()
    captured: list[str] = []
    active = False
    for line in lines:
        if line.startswith("description:"):
            active = True
            continue
        if active and re.match(r"^[a-z][a-z0-9-]*:", line):
            break
        if active:
            captured.append(line.strip())
    return " ".join(part for part in captured if part)


def validate_skill() -> None:
    text = SKILL.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    assert len(parts) == 3, "SKILL.md frontmatter is missing"
    description = folded_description(parts[1])

    # Agent Skills spec hard limits
    assert 1 <= len(description) <= 1024, (
        f"description violates Agent Skills 1024-char limit (got {len(description)})"
    )
    assert len(text.splitlines()) < 500, "SKILL.md exceeds progressive-disclosure 500-line budget"

    # Trigger contract: explicit markers + negative-trigger clause
    for marker in EXPLICIT_MARKERS:
        assert marker in description, f"description lost explicit trigger marker: {marker}"
    assert "Do not trigger" in description, "description lost negative-trigger clause"

    # Protocol contract
    for phrase in REQUIRED_PHRASES:
        assert phrase in text, f"SKILL.md lost protocol phrase: {phrase}"

    # Version metadata (semver)
    assert re.search(r'version: "\d+\.\d+\.\d+"', parts[1]), "version metadata is missing"

    print(f"PASS: SKILL.md ({len(text.splitlines())} lines, description {len(description)} chars)")


def validate_evals() -> None:
    evals = json.loads((EVALS_DIR / "evals.json").read_text(encoding="utf-8"))
    assert evals["skill_name"] == "agent-session-loop", "evals.json targets the wrong skill"
    assert len(evals["evals"]) >= 3, "evals.json needs >=3 behavior evals"
    for e in evals["evals"]:
        assert e["id"] and e["name"] and e["prompt"] and e["expected_output"], (
            f"eval missing required fields: {e.get('name')}"
        )
        assert e["expectations"], f"eval '{e['name']}' has empty expectations"
        for f in e.get("files", []):
            assert (ROOT / f).exists(), f"eval '{e['name']}' fixture missing: {f}"

    trig = json.loads((EVALS_DIR / "trigger-eval.json").read_text(encoding="utf-8"))
    queries = trig["queries"]
    assert len(queries) >= 10, "trigger-eval.json needs >=10 queries"
    assert any(q["should_trigger"] for q in queries), "trigger-eval has no should-trigger queries"
    assert any(not q["should_trigger"] for q in queries), (
        "trigger-eval has no should-not-trigger queries"
    )

    print(f"PASS: evals.json ({len(evals['evals'])} evals) + trigger-eval.json ({len(queries)} queries)")


def main() -> None:
    validate_skill()
    validate_evals()
    print("agent-session-loop: all structural regression checks passed")


if __name__ == "__main__":
    main()