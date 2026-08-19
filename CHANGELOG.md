# Changelog

本文件记录 agent-session-loop 的版本演进，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。版本号与 `SKILL.md` 的 `metadata.version` 保持一致。

## [Unreleased]

### Fixed
- 跨文件一致性：R0 表面检查补 expected hits 件（对齐 deep-review-loop 4 件套）
- 过拟合警报层 3 描述升级为增强版（P0 反弹 1 轮 / P1 反弹 2 轮 / 持平 4 轮窗口，对齐 deep-review-loop）

## [1.0.0] - 2026-08-10 初始发布

### Added
- 审查 → 收尾 → 沉淀三阶段会话生命周期流水线
- 阶段输入输出契约（convergence curve / sediment / 知识层升级）
- 按场景裁剪规则（显式 not-applicable，不允许静默跳过）
- 双语 README（含流水线图）+ 自然语言安装 + 叙事升级
- GitHub Release v1.0.0、Discussions、项目文档（CONTRIBUTING/CoC/SECURITY/CHANGELOG）
