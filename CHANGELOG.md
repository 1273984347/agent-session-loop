# Changelog

本文件记录 agent-session-loop 的版本演进，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。版本号与 `SKILL.md` 的 `metadata.version` 保持一致。

## [Unreleased]

## [1.0.3] - 2026-09-04

### Fixed
- publish-tessl.yml：TESSL_TOKEN 提升到 job 级 env——step 自身的 env 在它自己的 `if` 求值时尚未应用，原 step 级写法条件恒为 false，配置了 secret 也永远跳过（发布流水线死代码修复）
- GitHub Actions 全部 pin 到 commit SHA（actions/checkout v4/v6、setup-python v5、tesslio/setup-tessl v2），消除可变 tag 的供应链风险
- verdict 禁词自匹配误报：grep 命中先剔除禁词定义行本身再计数（meta-skill 场景禁词清单自匹配 +「OK」子串误报 TOKEN/BROKEN 等），fragment-lint 新增锚点防漂移
- 整合流水线防 ping-pong：Phase 2 的 mem-wrap-up Step 7b 不与 Phase 1 双跑完整 DRL（标 `not-applicable (covered by Phase 1)` 或降级精简 spot-check），收敛后不回触 mem-wrap-up

### Changed
- compatibility 字段如实声明：需要文件系统 + shell（PowerShell/POSIX）+ 文件搜索；无 shell 的纯 Web agent 不支持（原文 "Agent-agnostic" 超前）
- CI 加 windows-latest runner（skills-ref 两步在 Windows 跳过：上游 CLI 静默 exit 1）；lint/eval 步骤三平台覆盖
- .gitignore 补 `__pycache__/` 与 `.mimosa/`
- README（中/英）补 token 成本预期；运行依赖行同步 compatibility 修订

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
