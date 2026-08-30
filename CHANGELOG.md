# Changelog

本文件记录 agent-session-loop 的版本演进，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。版本号与 `SKILL.md` 的 `metadata.version` 保持一致。

## [Unreleased]

## [1.0.2] - 2026-08-31

### Fixed
- 出口 ACK 门禁：residual 含 P1+ 或接受残留 → 等人类 `ACK + 风险接受` 才能进 Phase 2（漏洞 6）
- 路径预检 + Grep 空结果判别：占位符使用前强制 `test -e`，预检失败中断问用户（漏洞 7/9/15）
- 安全扫描局限标注：0 发现必须附「正则仅覆盖硬编码格式」注记（漏洞 16）
- 知识层升级复核标记：pattern/heuristic 自动创建标 `review_status: pending`，reviewed 前不作权威规则（漏洞 13）
- 快速模式全否强制留痕：写「本次无新经验（3 问全否）」，不允许跳过不写文件（漏洞 14）

### Added
- LLM 行为 eval（evals/run_behavior_llm.py，发布前手动门禁）
- fragment-lint 交叉引用校验；version-lint 内容漂移软告警
- README badge 改动态 release badge；CI 加 macos-latest runner + skills-ref pin

## [1.0.1] - 2026-08-31

### Fixed
- 跨文件一致性：R0 表面检查补 expected hits 件（对齐 deep-review-loop 4 件套）
- 过拟合警报层 3 描述升级为增强版（P0 反弹 1 轮 / P1 反弹 2 轮 / 持平 4 轮窗口，对齐 deep-review-loop）

### Changed
- 跨平台清理：NEEDS_CONTEXT 信号通用化（去掉 TRAE 平台绑定），compatibility 字段改为 subagent optional
- 新增「无子代理平台的降级模式」：并行 subagent → 串行/主代理分轮内审，独立审查 → 自我对抗（显式标注 `degraded (no-subagent)`），降级 ≠ 跳过
- 四源版本同步（SKILL.md / README / CHANGELOG / marketplace.json）

## [1.0.0] - 2026-08-10 初始发布

### Added
- 审查 → 收尾 → 沉淀三阶段会话生命周期流水线
- 阶段输入输出契约（convergence curve / sediment / 知识层升级）
- 按场景裁剪规则（显式 not-applicable，不允许静默跳过）
- 双语 README（含流水线图）+ 自然语言安装 + 叙事升级
- GitHub Release v1.0.0、Discussions、项目文档（CONTRIBUTING/CoC/SECURITY/CHANGELOG）
