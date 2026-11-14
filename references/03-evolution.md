# Phase 3：沉淀（Evolution）详案

> 本文件在 Phase 3 激活时读取。双模式复盘：快速模式（3 问自检，任务完成自动）+ 全面模式（11 维度深度分析）。核心是知识层升级（experience → pattern → heuristic → policy）+ 行动项分流。

## 两种模式

| 模式 | 触发 | 深度 | 输出 |
|:---|:---|:---|:---|
| **快速** | 任务完成时自动 | 3 问自检 | experience-log.md |
| **全面** | 手动触发（「全面复盘/周汇总/retro」） | 11 维度分析 | retrospective.md + experience-log |

## 模式 A：快速复盘（任务完成后自动执行）

每个任务完成时，在 git commit 之前执行。

**Step 1：3 问自检**（必须回答，全否也要写出「全否」）：
```
① 有新发现？→ 方法/模式/工具首次使用或优化
② 踩了坑？→ 错误、根因、修复方案
③ 有 Skill 缺口？→ 本该用但没用的 Skill
```

**Step 2：根据答案决定动作**：全否 → **强制写一行「本次无新经验（3 问全否）」到 experience-log.md，不允许跳过不写文件**（Unknown Unknowns 防过滤——自己判断「没学到东西」可能只是不知道自己不知道）；有 → 执行写入：
1. 追加 `<memory_root>/projects/<project-slug>/experience-log.md`（格式：日期/任务/Tags + 发现或踩坑或缺口 + 根因 + 下次怎么做）
2. 有明确规则 → 追加 `experience-quickref.md`（`[编号] [关键词] — [一句话规则]`）
3. 有 Skill 缺口 → 追加 `skill-usage-checklist.md`（`| [Skill名] | [场景] | [为什么没用] |`）

**Step 2.5：反例检查（强制，防坏经验复利）**：本 session 的踩坑若与既有 `knowledge/patterns/` / `knowledge/heuristics/` 规则冲突（按规则执行反而踩坑）→ 触发 Step 4 的「降级铁律」，`counter_examples` 追加本 session 证据 id。Grep knowledge/ 关键词 vs 本 session 踩坑关键词即完成初筛；无 knowledge/ 目录 → 标 `not-applicable`。

**Step 3：模式升级检查**：同类问题 ≥3 次 → 提案升级到 `knowledge/patterns/` 或 `knowledge/heuristics/`

## 模式 B：全面复盘（手动触发）

**Step 1：数据收集（分层读取，避免 token 爆炸）**
- 第一层摘要（必须）：git log --oneline / git diff --stat / experience-log 最后 50 行
- 第二层按需：各维度对应文件（quickref / SKILL.md description / checklist / experience-log / patterns）
- 第三层深度：发现异常时才读全文
- 原则：先读摘要，需要深入再读全文

**Step 2：11 维度分析**

| # | 维度 | 必走 | 核心 |
|:--|:---|:---:|:---|
| 1 | 经验复用梳理 | ✅ | 复用/新增/反复经验 + 量化评分（普适0.4/可迁移0.4/预期0.2，≥4 高价值） |
| 2 | 技能优化评估 | ✅ | 掌握×频率×影响×潜力矩阵 + 3-5 项优先提升 + 计划表 |
| 3 | 未用技能审视 | ✅ | 应没用清单 + 引入可行性论证（结论：建议引入/暂缓/放弃） |
| 4 | 场景沉淀识别 | ✅ | 频率-重要性四象限，Top 20% 立即沉淀 SOP |
| 5 | 问题与预防机制 | ✅ | 5 类问题分类 + 严重度等级（致命/严重强制 5Why） |
| 6 | 工作流优化方案 | ✅ | 流程标注（⏸等待/🔄返工/⚡瓶颈/🤖可自动化/∥可并行） |
| 7 | 问题总结与计划制定 | ✅ | 影响-紧急矩阵统一排序 + 行动计划表 + 经验→规则升级评估 |
| 8 | 元认知反思 | ✅ | 复盘本身的复盘：数据源完整？深度够？结论可执行？ |
| 9 | 一次性工具沉淀 | ✅ 必走 | 4 类决策：skill 候选 / 永久化 / 模板 / 弃用；撞 1 次也走 |
| 10 | 工具链 sub-protocol 反思 | 可选 | 单工具链层撞坑（≥3 次同类才走） |
| 11 | 复盘过程中出现的问题 | ✅ 必走 | 元层兜底：撞坑分类表 + 5Why 元层根因 + 反模式识别 |

**5Why 未知标注（防深度幻觉，维度 5/11 适用）**：当前上下文（代码/日志/memory）无法支撑的层级，禁止编造因果链——写 `[未知：超出当前上下文，需跨 session/人工补充]` 并停止深挖该分支；允许挖到第 N 层即标注未知，**不强制凑满 5 层**，宁缺毋滥（模板详见本包 references/11-dimensions-template.md·自包含副本·权威源 self-evolution）。

**Step 3：生成报告** → `<memory_root>/projects/<project-slug>/<date>/retrospective.md`（11 段结构，每段对应一个维度输出）

**Step 3.5：多件套同步 verify（强制）**——漏任一件 = 复盘未闭环：
1. 复盘主 file（Test-Path 必存在；macOS/Linux：`test -f`）
2. project_memory 更新（Grep 关键词 ≥1）
3. user_profile 更新（如适用）
4. experience-log 备忘段（Grep session 编号 ≥1）
5. E-rule 候选（Grep 新增编号 ≥1）
- verify 失败 → 立即补漏，不要等下次 session

**Step 4：知识层升级（experience → pattern → heuristic → policy）**

| 条件 | 升级动作 |
|:---|:---|
| 同类经验 ≥3 次 + 跨任务 + 根因一致 | 创建 `knowledge/patterns/[name].md`（自动，但标注「待人工复核」） |
| pattern 成功率 >80% + 不引入新问题 | 创建 `knowledge/heuristics/[name].md`（自动，但标注「待人工复核」——成功率是 AI 自评，须人工核实） |
| heuristic 效果显著 | 写入 `knowledge/policies/`（**需人工确认**） |

- **复核标记**：自动创建的 pattern/heuristic 文件 frontmatter 必须含 `review_status: pending`；人工复核通过后改为 `reviewed`。任何自动升级的规则在 `reviewed` 前**不得作为权威规则**驱动后续决策——只作参考候选。
- **溯源与反例字段**：pattern/heuristic frontmatter 必含 `based_on`（支撑它的 experience id 列表）/ `counter_examples`（反例 id 列表，空数组起步）/ `last_verified`（最近一次复用验证日期）/ `reuse_count`（被后续 session 复用次数）。升级门槛（≥3 次 / >80% 成功率）的判定依据必须是这些字段的记录，不允许凭印象升级。
- knowledge/ 文件 frontmatter 标准：name / description / type / id / level / tags / review_status / based_on / counter_examples / last_verified / reuse_count
- 安全规则：只创建新文件不覆盖；已存在 → 追加；policies 一律人工确认

**降级铁律（升级慢、降级快——防坏经验复利）**：
- 任一后续 session 出现反例 → 立即把该 pattern/heuristic 降级回 experience，`counter_examples` 追加反例 id，禁止「记个例外但保留规则」
- `counter_examples` 非空的规则 → 权威性立即失效，等同 `review_status: pending` 之前的状态（只作历史参考，不得作为依据引用）
- 降级动作本身走 sediment 写入协议（Read-before-Edit + Grep-verify-after-Edit），反例来源 session/证据 id 必须可追溯

**Step 5：执行行动计划（按优先级分流）**

| 优先级 | 执行方式 |
|:---|:---|
| P0（崩溃/安全/数据丢失） | 立即自动执行，执行后报告 |
| P1（核心功能失效） | 立即自动执行，执行后报告 |
| P2（体验优化/非核心） | 等用户确认 |
| P3（nice-to-have） | 只记录，不主动执行 |

- 每个动作前：Test-Path 检查（macOS/Linux：`test -e`）→ 存在则 Edit 追加（不覆盖），不存在则 Write 创建
- 动作类型：创建模板 / 更新 Skill（先 Read 再改）/ 追加经验条目 / 更新速查表 / 写入 patterns / heuristics / 更新 checklist

## 维度 9 详案（一次性工具沉淀，必走）

- 与维度 4 区别：维度 4 = 通用场景沉淀（撞 ≥3 才升 pattern）；维度 9 = 工具层产物沉淀（4 类决策，撞 1 也走）
- 沉淀价值评分：高 = P0 critical / 再用频率高 / 协议必走；中 = 单 session 多次复用；低 = 一次性
- 4 类决策：skill 候选（跨 session + 协议化）→ 新 skill；永久化（单项目高频）→ scripts/tools；模板（结构化重复）→ templates/X.md；弃用（一次性）→ 只记录
- Skip：Mode A 时 optional；Mode B 无一次性工具 → 显式标记 NONE 不静默跳过

## 维度 11 详案（复盘过程撞坑，必走）

- 撞坑分类：工具链层 / 协议层 / 流程层 / memory 维护层 / future
- 评分：P0×单次 = 立即整合；P1×N 同类 = 升 E 候选；P0×N 同类 = 升 H 协议
- 反模式：「修完即 OK」不整合 / ad-hoc 加维度不持久化 / 撞 N 次不主动升 H
- 整合路径：撞 1 次 → E 候选；撞 N 次同类 → 升 H 协议

## 单一事实源原则

```
experience-log.md（权威源）→ 每次任务的发现和教训
  ↓
experience-quickref.md（索引）→ 速查表
  ↓
retrospective.md（分析报告）→ 引用 experience-log.md，不重复内容
```

## 边界限制
- 不改变已有 Skills 的核心职责；不自动删除 Skill
- 快速复盘是完成协议的一部分，不可跳过
- dim 9 + dim 11 必走，不可跳过

## 触发条件
- 任务完成（git commit 前自动）→ 快速模式
- 「全面复盘 / 跑一下验收 / 周汇总 / 复盘 / retro」→ 全面模式
