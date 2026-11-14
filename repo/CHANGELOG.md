# Changelog

本文件记录 agent-session-loop 的版本演进，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。版本号与 `SKILL.md` 的 `metadata.version` 保持一致。

## [Unreleased]

## [1.1.0] - 2026-09-05

### Added
- Phase 1 独立性边界（references/01-review.md）：subagent 隔离的是上下文不是认知——证据独立是唯一独立性来源（各自采集，转引视同证据缺失）、一致但证据同源按 1 票计、verifier 分歧升级为 file:line 证据比对、出口 ACK 门禁是认知级盲区的唯一补偿
- 严重度地板分 `scripts/severity_score.py`（外部静态下界，纯 stdlib）：模型定性可上调不可低于地板（P0 凭据/数据丢失信号、P1 崩溃/测试失败信号）；dispute 项强制进 residual risk 并触发出口 ACK 门禁（P2 自动放行通道关闭）；局限显式声明——地板分是下界不是分类器，无信号不得作为降级依据
- Phase 3 反例降级回路（防坏经验复利）：pattern/heuristic frontmatter 新增 `based_on` / `counter_examples` / `last_verified` / `reuse_count` 溯源字段；降级铁律（反例 → 立即降级回 experience，「记个例外但保留规则」禁止）；快速模式新增 Step 2.5 反例检查（与既有 knowledge 规则冲突的踩坑必须触发降级）
- Phase 2 memory audit 新增 knowledge 层健康检查（并 6 面矩阵）：`review_status: pending` 清单 + `counter_examples` 非空失效 + pending 超期 30 天降权「仅历史参考」；毕业判据加前置——`reviewed` 且无反例才能毕业进权威文档
- 5Why 未知标注（防深度幻觉）同步到整合版（references/02-wrap-up.md sediment + references/03-evolution.md 维度 5/11）：证据无法支撑的层级写 `[未知：超出当前上下文]` 停止深挖，不强制凑满，禁止编造因果链（对齐 self-evolution 模板既有规则）
- Failure handling 新增验证命令通用细则：exit code ≠ 0 → 按工具失败处理，不得把命令报错输出解释为业务结论（区分「git 说没 track」与「git 命令报错」）
- 路径预检新增首次运行回显确认：预检通过后向用户回显「平台推断 → 实际路径」映射依据，确认后再启动
- 安全扫描专业工具优先（可选增强）：环境存在 gitleaks / trivy 时先跑专业工具并以输出为主证据，不可用回退 4+1 正则 + 局限标注（降级 ≠ 跳过）

### Changed
- SKILL.md Phase 1 协议：R1a 条目加独立性边界指针；4 层过拟合防护追加严重度地板分（不改「4 层」既定叫法，SVG/博客/联动声明零波及）；Self-Disclosure 增地板分与独立性边界两行
- memory 路径约定补 Linux 显式映射（Claude Code `~/.claude/projects`），注明 `~/` 开头路径在 macOS 与 Linux 通用

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
