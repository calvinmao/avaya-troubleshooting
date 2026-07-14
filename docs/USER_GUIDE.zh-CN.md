# avaya-troubleshooting · 使用指南

> 版本 2.0.0 · 简体中文 · English: [USER_GUIDE.md](USER_GUIDE.md)

本指南面向 Avaya 技术支持工程师,教你如何安装并日常使用
`avaya-troubleshooting` 这个 Claude Code 插件。假设你在真实
Service Request(SR)排障工作中,把 Claude Code 当作诊断助手。

如果你还想搞清楚**为什么**插件要这么设计(5×5×3 知识方法论),
请重点读第 3 节 *核心概念*;想了解改造历史,看
`docs/reform/PLAN.md`。

---

## 目录

1. [介绍](#1-介绍)
2. [快速上手](#2-快速上手)
3. [核心概念](#3-核心概念)
4. [日常工作流 — 接 SR](#4-日常工作流--接-sr)
5. [日常工作流 — 关 SR](#5-日常工作流--关-sr)
6. [辅助命令](#6-辅助命令)
7. [季度维护](#7-季度维护)
8. [新增内容](#8-新增内容)
9. [贡献 / 开发](#9-贡献--开发)
10. [常见问题 FAQ](#10-常见问题-faq)
11. [附录](#11-附录)

---

## 1. 介绍

### 1.1 这个插件做什么

`avaya-troubleshooting` 是一个 Claude Code 插件,把 Claude Code
变成一位资深 Avaya UC/CC 排障专家。当你把 SR 症状、trace 片段、
或者 getlogs 输出粘进 Claude,插件会:

1. **自动激活** —— 基于 Avaya 产品名/关键词触发。
2. **渐进加载** —— 只加载匹配症状域的 reference 文件(不是
   全部 7,851 行)。
3. **自动附带 L-NNN lessons** —— 把先前 SR 沉淀的经验一并带入
   当下会话,让你继承团队历史知识。
4. **应用 16 条核心诊断不变量** —— UCID 提取、`deviceIDType`、
   `SA9114/SA9124`、证书变更三动作 等,在每个域的诊断中都会被
   自动应用。

### 1.2 本指南读者定位

- **首次使用者**:按顺序读第 1–5 节。
- **偶尔使用 / 复习**:速览第 3 节,再把 4–7 节当参考手册用。
- **KB 维护者 / 贡献者**:重点读第 7–9 节,涵盖季度 GC、内容
  创作、CI 机制。

### 1.3 5×5×3 架构一图看懂

知识库沿三个正交维度组织:

```
5 层存储 × 5 种类型 × 3 级成熟度
    L1 现场层             fact 事实型             draft   草稿
    L2 流程层             process 流程型          verified 已验证
    L3 沉淀库             decision 决策型         canonical 规范化
    L4 规范层             experience 经验型
    L5 战略层             pattern 模式型
```

每个知识文件都在 YAML frontmatter 里声明自己在三个维度上的位置,
使得工程师和 CI 都能对其进行系统性推理。完整模型见第 3 节。

---

## 2. 快速上手

### 2.1 前置条件

- **Claude Code** 已安装(PATH 里能找到 `claude` 命令)。
- **Anthropic 账号** 有 API 访问权限(Claude Code 会处理)。
- **Git** 用于 clone 和更新。
- **Python 3.9+**(仅当你想在本地跑 lint / evals 时需要,可选)。
- **本地 plugins marketplace** 已注册插件目录路径(见 2.2)。

### 2.2 安装

**方式 A — 从 calvinmao 组织 clone**(推荐大多数人):

```bash
# 选一个位置放本地 Claude Code 插件
mkdir -p ~/.claude/plugins/local
cd ~/.claude/plugins/local
git clone https://github.com/calvinmao/avaya-troubleshooting.git
cd avaya-troubleshooting
```

**方式 B — 团队内部 fork / 镜像**(推荐团队使用):

```bash
git clone <团队内部 git 地址> avaya-troubleshooting
cd avaya-troubleshooting
```

在你的 `~/.claude/settings.json` 里把插件注册到本地 marketplace
(按团队约定的模式做,一次配好)。然后在 Claude Code 里:

```
/plugin install avaya-troubleshooting@local-plugins
```

重启 Claude Code 让插件生效。

### 2.3 首次验证

问 Claude 一个域相关问题,看它加载了哪些文件来验证插件是否激活:

```
JTAPI 在 park 事件里对 getCalledAddress() 返回 null,
应该套哪条不变量?
```

预期行为:

- Claude 会读 `skills/avaya-debug/references/diagnostic-principles.md`
  (always-loaded 基线)。
- Claude 会读 `skills/avaya-debug/references/aes-cti-jtapi.md`
  (被 AES/JTAPI 关键词匹配)。
- Claude 会读 `skills/avaya-debug/lessons/aes-cti-jtapi.md`
  (伴随 reference 自动加载的 lessons)。
- Claude 回答会引用不变量 #11(JTAPI `null` 返回是符合 spec 的),
  并指向 Javadoc 引用。

如果 Claude 没激活插件,看 [10.1 节](#101-插件不激活)。

### 2.4 可选:安装 git hooks 和开发工具

如果你打算修改 KB(写或改 lessons/references),装 pre-commit 和
post-commit hooks:

```bash
# 在插件目录下执行
./scripts/install-git-hooks.sh          # post-commit hook(Obsidian 同步 marker)
pip install pre-commit PyYAML
pre-commit install                       # 每次 commit 前跑 lint + evals
```

---

## 3. 核心概念

不看这一节也能用插件,但理解这五个概念,才能玩转第 5–7 节的
维护工作流。

### 3.1 渐进加载

`skills/avaya-debug/SKILL.md` 是一张**路由表**,不是知识本身。
当你提到 "AACC",Claude 只加载 `references/contact-center.md` +
`lessons/contact-center.md`,不会加载另外 15 个域文件。这样既
节省 context token,也防止跨域污染。

Always-loaded 基线:`references/diagnostic-principles.md` 和
`lessons/diagnostic-principles.md`(16 条核心不变量,任何域都
适用)。

### 3.2 五层存储 L1–L5

| 层 | 用途 | 生命周期 | 存放位置 |
|----|------|---------|---------|
| **L1 现场层** | 单 SR 现场:症状路由、工作笔记、假设链 | 一个 SR | `skills/avaya-debug/triage/` |
| **L2 流程层** | 可复用 playbook、日志收集命令、slash 命令 | 月级 | `commands/`, `skills/avaya-debug/references/log-collection.md` |
| **L3 沉淀库** | 关闭 SR 后沉淀的、证据锚定的 L-NNN lessons | 年级,可变 | `skills/avaya-debug/lessons/` |
| **L4 规范层** | 域权威 references 和诊断不变量 | 年级,精心维护 | `skills/avaya-debug/references/` |
| **L5 战略层** | 长期设计决策和跨产品架构 | 半永久 | `CLAUDE.md`, `AGENTS.md`, `docs/reform/` |

**经验法则**:知识随时间**向上流动**。L1 triage 笔记通过
`/avaya-learn` 毕业成 L3 lessons;L3 lessons 通过 promotion 毕业
成 L4 references。

### 3.3 五种知识类型

每条 L-NNN lesson 都要声明自己的 `type:` 字段:

| 类型 | 含义 | 典型场景 |
|------|------|---------|
| `fact` 事实型 | 客观不变量,可对照文档验证 | "AEP 8.1.2.2 与 POM 4.0.2.x 不兼容(PSN006373u)" |
| `process` 流程型 | 分步骤"怎么做 X" | POM 日志收集命令、证书更换流程 |
| `decision` 决策型 | "为什么要这么做" —— 框架化或判断类的知识 | 怎么向客户解释 APC/POM 可靠性不对等 |
| `experience` 经验型 | 单 SR 现场捕获的发现 | "SM SessionManager.log 在 POM 负载下 1h 内轮转" |
| `pattern` 模式型 | 从多次观察提炼出的可复用诊断规则 | "信令正常 + 媒体缺失 = SBC 故障类(三种成因)" |

`type` 字段暗示了知识的复用方式 —— `pattern` 和 `decision` 类型
最容易在未来 SR 里复用,所以它们是晋升的强候选。

### 3.4 三级成熟度 M1/M2/M3

每条 L-NNN 都带一个 `maturity:` 字段,取三个值之一:

| 等级 | 含义 | 你应该怎么用 |
|------|------|-------------|
| **`draft` 草稿** | 单 SR 发现,未交叉验证 | 只作诊断提示;**不要**盲目套到客户身上;需要 senior review |
| **`verified` 已验证** | 在 ≥2 个 SR 中复现,或识别出可泛化的代码路径/trace 字符串/config 字段,或已被 promote 进 references | 可信任地直接应用 |
| **`canonical` 规范化** | 通过把 lesson 内容 promote 到 `references/*.md` 达成。lesson 条目留在 `lessons/` 作为审计存根。 | 放心引用;这是团队的官方立场 |

**为什么重要**:当 Claude 遇到两条互相矛盾的 lessons(比如老的
`draft` 说 "CM B2BUA 缺陷";新的 `verified` 说 "SBC 媒体面失败"),
成熟度标签告诉你信哪一条。

### 3.5 晋升(promotion)和降级(demotion)

**晋升**(`draft` → `verified` → 进 `references/`)由 `/avaya-learn`
在满足晋升规则时提议:

- **(a)** 在 **≥2 个 SR** 中复现,或
- **(b)** 识别出**代码路径、trace 字符串或 config 字段**,可以
  泛化到单个客户环境之外。

**降级**发生在新 SR 关闭时推翻了先前 `verified` 的 lesson(2026 年
6 月 SR 1-23647477802 就是这样)。这条 lesson 会:

- 降回 `maturity: draft`
- `promotion.status` 改为 `rejected`,`promotion.note` 里写明
  推翻它的 SR 编号
- 正文改写,反映纠正后的理解

lesson **不会被删掉** —— 拒绝本身就是可持久的教训,能防止未来
再犯同类错误。

---

## 4. 日常工作流 — 接 SR

### 4.1 启动一个会话

在插件目录(或任何项目 —— 插件装好后是 user-scoped 的)打开
Claude Code,运行:

```
/avaya-sr <SR 编号> <一行症状>
```

例:

```
/avaya-sr 00123456 AES 在 EC_PARK 事件里对 outbound 调用返回 null calledAddress
```

这会启动一个**结构化会话**,包含:

- 会话头(SR 编号 / 产品 / 症状)
- 开放事项表(状态 / 事项 / 负责人)
- Claude 根据你的症状字符串自动加载匹配的 reference + lessons

### 4.2 症状 triage(可选但推荐)

如果 Claude 自动匹配的域感觉不对,或者症状模糊,手动查阅
**L1 症状目录**:

- 读 `skills/avaya-debug/triage/symptom-catalog.md` —— 比 SKILL.md
  更细粒度的症状 → 域映射,每条附带*第一诊断动作*
- 读 `skills/avaya-debug/triage/README.md` 了解 L1 层的角色

对严重/长周期 SR,把 `skills/avaya-debug/triage/session-template.md`
里的模板复制到你的工作笔记,边排障边填写。这份结构化笔记就是
`/avaya-learn` 在关单时读取、用来提取 L-NNN 条目的原材料。

### 4.3 排障调查

一边收集一边把证据粘进对话:

- traceSM / traceSBC 片段
- `list trace vector <N>` 输出
- getlogs / pcap 发现
- CM `display` 命令输出
- 厂商回复

插件加载后 Claude 的默认行为:

- **引用具体的 L-NNN lesson**,例:*"根据 `lessons/sip-voice-quality.md`
  L-002(SR 1-23647477802, 2026-06-04),先跑 RTP 包计数再做信令
  分析。"*
- **应用诊断不变量**,例:*"不变量 #4 说,null 地址出现时先查
  `SA9114`/`SA9124`,再深挖 JTAPI。"*
- **拒绝过度结论** —— 如果某一层缺乏证据,它会把 gap 标为开放
  事项,而不是猜。

### 4.4 维护假设链

对非平凡的 SR,在工作笔记里维护一条编号的假设链:

```
H1 (2026-07-14): CM B2BUA 未成功传递 Replaces
  - 证据:SBC 侧 dialog 里 CSeq:2 INVITE 缺失
  - 测试:跑 RTP 包计数分析
  - 结果:INVALIDATES —— CM→SBC = 208 RTP, SBC→CM = 0 RTP
           媒体面失败,不是信令面

H2 (2026-07-14): SBC RTP 中继失败
  - ...
```

**关键纪律**(源于 `diagnostic-principles.md` L-002):H1 被推翻时,
**完整废弃它** —— 不要在 H2 里保留 H1 的碎片。被拒绝的链条本身
就是关单时 L-NNN 捕获的学习材料。

### 4.5 生成 SR 报告

当你有足够证据起草正式回复,运行:

```
/avaya-report
```

Claude 会生成一份结构化报告,包含:

- 问题陈述
- 证据(带时间戳和来源)
- 分层分析(CM → AES → 应用等)
- 根因(带证据锚点)
- 建议处置方案
- 开放事项
- 厂商 escalation 段(如需)
- 引用的所有 L-NNN lessons

报告结尾会有一句提示:*"从本次会话中捕获 lesson?运行
`/avaya-learn`。"*

---

## 5. 日常工作流 — 关 SR

关 SR 是知识沉淀的关键节点。**这是插件长期价值最重要的一步。**

### 5.1 运行 `/avaya-learn`

```
/avaya-learn                          # 扫描整个会话
/avaya-learn AES                      # 提示:分类模糊时优先归 AES 域
```

`/avaya-learn` 按顺序执行五步:

#### 步骤 1 — 扫描会话

Claude 重读对话,找证据锚定的发现:

- 你反应过的 trace 字符串
- grep 或反编译出的代码路径
- 检查过的 config 字段
- 消除歧义的 Javadoc / Release Note 引用
- 关闭开放事项的厂商回复
- 令人惊讶的经验观察

它会跳过:常规确认、客户闲聊、已经文档化的通用 Avaya 事实、一次性
的环境古怪。

#### 步骤 2 — 分域归类

每个候选按 SKILL.md 里同款的触发词表分域。若一条发现跨两个域
(如 AES + logs),会存两次并交叉引用。

#### 步骤 3 — 起草 L-NNN 条目

Claude 用 **YAML frontmatter 块 + Markdown 正文** 起草每条条目:

```markdown
---
id: L-007
layer: L3
type: experience              # fact | process | decision | experience | pattern
maturity: draft               # 首次捕获时总是 draft
versions:
  - "AEP 8.1.x"
provenance:
  sr: "1-23647477802"
  date: "2026-07-14"
promotion:
  status: pending
  target: null
  date: null
  note: null
owner: "@你的 github 用户名"
---

## L-007 — <一行症状>

- **Symptom**: ...
- **Evidence**: ...
- **Root cause**: ...
- **Fix / workaround**: ...
```

**字段推断规则**(Claude 会自动遵循):

- `type`:单 SR 捕获默认 `experience`;若发现是可复用诊断规则,
  升级为 `pattern`。
- `versions`:从 Evidence 文本里提取(如 "AEP 8.1.2.2"、"POM
  4.0.x")。找不到则填 `[TBD]`。
- `maturity`:首次捕获**总是** `draft`。promotion 是单独一步。

Claude 会把所有草稿列表化呈现,包括被拒绝的候选和理由:

```
发现 3 条候选 lesson:
[1] aes-cti-jtapi → L-007 — 症状 X
[2] log-collection → L-012 — 症状 Y
[3] (已拒绝) — 症状 Z — 一次性,无可复用模式
```

#### 步骤 4 — 保存已批准的 lessons

告诉 Claude 保存哪些(比如"保存 1 和 2,跳过 3")。Claude 会:

1. 检查是否已有匹配 Symptom/Evidence 的条目(幂等性)。
2. 把新条目追加到 `lessons/<domain>.md`。
3. 如果这是首条,更新文件级 `last_reviewed` 日期。
4. 用 L-NNN ID 列表确认已保存。

#### 步骤 5 — 提议 promotion(如符合)

对每条满足晋升规则(≥2 SR 或可泛化代码/trace/flag)的已保存
lesson,Claude 会:

1. 读匹配的 `references/<domain>.md`,定位到合适的段落。
2. 起草一条具体的编辑 —— 通常是在现有 header 下新增一个 bullet,
   风格和 SKILL.md 一样密集。
3. 展示 diff,问你:**"是否现在把 L-NNN promote 进
   references/<domain>.md?"**
4. 批准后:应用编辑到 reference,并更新 lesson 的 YAML frontmatter:
   - `maturity: draft` → `maturity: verified`
   - `promotion.status: pending` → `promoted`
   - `promotion.target` → anchor
   - `promotion.date` → 今天
5. 拒绝后:设 `promotion.status: rejected`,`promotion.note` 里
   记一行原因。`maturity` 保持 `draft`。

### 5.2 Commit + push

`/avaya-learn` 只写文件,不 commit。review diff 后:

```bash
git add skills/avaya-debug/
git commit -m "feat(lessons): capture L-007 from SR 00123456"
git push
```

如果装了 pre-commit hook,本地会跑 lint。CI 会在 push 时再跑一次,
schema 破了会阻断合并到 master。

### 5.3 处理降级(根因被推翻)

如果新 SR 推翻了先前 `verified` 的 lesson,**不要**默默改 body。
按以下流程:

1. 打开被推翻的 L-NNN frontmatter。
2. 设 `maturity: draft`(降级)。
3. 设 `promotion.status: rejected`, `promotion.date: <今天>`,
   `promotion.note: "invalidated by SR <新 SR 编号> — <一行原因>"`。
4. 改写 body 反映纠正后的理解,在 Evidence 字段引用推翻它的 SR。
5. 如果这条 lesson 曾被 promote 进 `references/`,那次 promotion
   也要审计:改写或移除已 promote 的内容,在 lesson 的
   `promotion.note` 里记录变更。

这正是 SR 1-23647477802 KB hygiene commit 遵循的模式 ——
用 `git log --grep="B2BUA"` 能看到那次 commit 作为参考。

---

## 6. 辅助命令

### 6.1 `/avaya-logs <product>`

打印指定产品的确切日志收集命令,附带每份输出要看什么。

```
/avaya-logs AACC
/avaya-logs Recording
/avaya-logs AES
```

在向客户要日志之前用这个 —— 省时间(客户第一次就发对文件)
又显示你对产品的掌控力。

### 6.2 `/avaya-report`

第 4.5 节已覆盖。会话中的任何时候都能跑 —— 报告反映当下上下文里
的证据快照。

### 6.3 子代理:`avaya-debugger`

对长的并行 trace 分析,可以让 Claude Code 的 `Agent` 工具派发
一个专业子代理,它拥有和主 skill 一样的 Avaya 专业能力:

```
请派发 avaya-debugger 子代理,grep 这个 500 MB pcap 里所有
Call-ID 匹配 d6c229d2* 的 SIP dialog,按 dialog 返回 CSeq
分布。
```

这样把耗时的 trace 解析卸载到独立 context 里,主对话保持在
综合分析层。

---

## 7. 季度维护

季度跑一次 `/avaya-gc`(或每积累 10+ 条新 lessons 后跑一次)。
它是 **read-and-propose 模式** —— 每一处改动都需要按发现逐项批准。

### 7.1 什么时候跑

- 季度初(按日历触发)。
- `/avaya-learn` 密集使用后(积累 10+ 条 L-NNN)。
- 触及多个域的重要 SR 关闭后。
- 内部培训或 KB 分享会前(保证干净)。

### 7.2 七步工作流

```
/avaya-gc                        # 交互式,全域
/avaya-gc --dry-run              # 只报告,不问批准
/avaya-gc --domain=aes-cti-jtapi # 限制到单个域
```

七步交互式工作流:

| 步骤 | 做什么 | 你的动作 |
|------|--------|---------|
| 1 | 扫 `pending` L-NNN 里满足晋升条件的(≥2 SR 或可泛化) | 批准 promote / 推迟 / 拒绝并注明原因 |
| 2 | 标出 `last_reviewed` > 6 个月的 references | 标记今天已 review / 推迟 / 排入内容 review 队列 |
| 3 | 检测跨 references 的重复/近似 invariants | 合并 / 保留两份并交叉引用 / 不算重复 |
| 4 | 已 promoted lessons 的 post-promotion 清理 —— 折叠为审计存根 | 折叠(默认)/ 保留完整 / 完全移除(罕见) |
| 5 | 检测 SKILL.md 触发词没有对应 A-NNN case 覆盖的 | 起草新 eval / 推迟 / 无需 |
| 6 | 刷新 `staleness_risks`(新增新出现的、移除已实现的) | 按 reference 批准 |
| 7 | 扫 `versions: [TBD]` 条目,提议从 Evidence 文本回填 | 应用建议 / 换值 / 推迟 |

结尾给出汇总:

```
季度 GC 完成:
- Promoted: 3 条 lessons
- Marked reviewed: 8 个 references
- Merged duplicates: 1 条 invariant
- Collapsed to audit stub: 2 条 lessons
- TBD versions backfilled: 5 条
```

### 7.3 安全不变量

- L-NNN ID 一旦分配就**不可变** —— 所有引用都依赖 ID 稳定。
- 折叠已 promoted lesson 为审计存根时,保留 frontmatter 和
  `## L-NNN` heading 不动;只把 body 替换成指向 promoted 段的
  pointer。
- 永不移除 `rejected` lesson —— 拒绝本身就是可持久的教训。

---

## 8. 新增内容

### 8.1 手动添加一条 L-NNN(不走完整 SR)

如果你有一个发现,够资格作为 lesson,但当时没在会话里捕获,可以
手动加:

1. 打开 `skills/avaya-debug/lessons/<domain>.md`。
2. 找现有最高的 `L-NNN`(`grep ^## L-`);用下一个数字,补零 3 位。
3. 按 `skills/avaya-debug/lessons/README.md` 里的模板添加 YAML
   frontmatter 块 + `## L-NNN` heading + body。
4. 更新文件级 `last_reviewed` 为今天。
5. Commit —— pre-commit lint 会验证 frontmatter。

### 8.2 添加新域

如果一个新 Avaya 产品/技术需要独立 reference(罕见):

1. 创建 `skills/avaya-debug/references/<new-domain>.md`,带 YAML
   frontmatter 头(参考任何现有 reference 作为模板)。
2. 创建 `skills/avaya-debug/lessons/<new-domain>.md` 作为 stub,
   带域默认 frontmatter(参考 `lessons/aes-cti-jtapi.md`)。
3. 在 `skills/avaya-debug/SKILL.md` 加一行路由,带触发关键词。
4. 在 `skills/avaya-debug/lessons/README.md` 的 Files 表加一行。
5. 在 `evals/activation.md` 加 `### <新域>` 子表,含 Should-Trigger
   A-NNN cases。
6. 跑 `python3 scripts/lint_metadata.py` 和 `python3
   scripts/run_evals.py --mode a` 验证。

### 8.3 添加新的 activation eval case

发现某个真实客户 prompt **本应**触发 skill 但只是勉强触发时:

1. 打开 `evals/activation.md`。
2. 在正确的域的 "Should-Trigger Cases" 子表下加一行:
   `| A-NNN | "<prompt>" | <expected-ref>.md | <notes> |`。
3. 在该域 ID 范围内单调编号。
4. 跑 `python3 scripts/run_evals.py` —— 若 case 失败,扩展
   SKILL.md 的触发关键词以覆盖新说法。

---

## 9. 贡献 / 开发

### 9.1 仓库布局(简版)

```
skills/avaya-debug/     # 主 skill;SKILL.md 是路由表
  triage/               # L1 会话工件
  references/           # L4 域权威知识
  lessons/              # L3 现场捕获 L-NNN
commands/               # slash 命令
agents/                 # 子代理定义
evals/                  # activation + output-quality 测试 case
scripts/                # lint_metadata.py, run_evals.py, install-git-hooks.sh
scripts/hooks/          # 版本控制里的 git hooks
.github/workflows/      # CI: knowledge-lint.yml (auto), eval-full.yml (manual)
docs/reform/            # 改造历史 + schema 定义
docs/                   # 本指南
```

### 9.2 本地 pre-commit 配置

```bash
pip install pre-commit PyYAML
pre-commit install
```

之后每次 `git commit` 前会本地跑 `scripts/lint_metadata.py` 和
`scripts/run_evals.py --mode a`。需要绕过用 `git commit
--no-verify`(但 push 时 CI 还会抓到)。

### 9.3 手动跑 lint / evals

```bash
python3 scripts/lint_metadata.py                    # 全库 lint
python3 scripts/lint_metadata.py --verbose          # 显示 OK 行
python3 scripts/lint_metadata.py --domain=aes-cti-jtapi  # 单域

python3 scripts/run_evals.py                        # mode A(离线)
python3 scripts/run_evals.py --verbose              # verbose mode A
python3 scripts/run_evals.py --mode b               # mode B(需 API key)
```

### 9.4 CI workflows

`.github/workflows/` 里两个 workflow:

- **`knowledge-lint.yml`** —— 触及 `skills/`, `evals/`, 或
  `scripts/` 的每次 push 和 PR 都会跑。两个 job:
  - Frontmatter 结构 lint(来自 `lint_metadata.py`)
  - Activation 覆盖检查(来自 `run_evals.py --mode a`)
  任一 job 失败会阻断合并到 master。
- **`eval-full.yml`** —— 仅手动触发(Actions tab → Run workflow)。
  跑 mode B(LLM 打分)。消耗 API tokens,所以设为 opt-in。需要
  仓库 secret 里配置 `ANTHROPIC_API_KEY`。

### 9.5 Git hooks (post-commit)

`scripts/hooks/post-commit` hook 在本地有 `claude-obsidian` vault
时,写入一个同步 marker,让 vault 自己的 SessionStart hook 在你
下次开 Claude Code 时提示重新 ingest 插件内容。

Hook 跨平台:按 WSL / Git Bash / Windows 原生 / Linux 的顺序探测
候选路径。找不到 vault 时静默跳过。用
`AVAYA_KB_MARKER_DIR=/path/to/.vault-meta` 覆盖路径。

安装:

```bash
./scripts/install-git-hooks.sh          # 交互式
./scripts/install-git-hooks.sh --force  # 无提示覆盖
```

---

## 10. 常见问题 FAQ

### 10.1 插件不激活

**症状**:你提了 Avaya 产品,但 Claude 似乎没加载任何 reference 文件。

**检查步骤**:

1. 确认插件已装:`/plugin` —— 应看到 enabled。
2. 重启 Claude Code(插件只在启动时加载)。
3. 试更强的触发关键词:不要说"电话系统",而是"AACC"或"AES"
   或"SIP one-way audio"。完整触发词表见 SKILL.md。
4. 如果某个特定 prompt 应该激活但没激活,按 8.3 节加一个
   A-NNN case 到 `evals/activation.md`,并扩展 SKILL.md 触发词。

### 10.2 加载了错误的 reference

**症状**:skill 激活了,但加载的是错误域的 reference(比如加载
了 contact-center 而不是 sip-voice-quality)。

**检查步骤**:

1. 读 `skills/avaya-debug/triage/symptom-catalog.md` —— 细粒度
   症状目录常常能消除 SKILL.md 粗粒度触发表搞不清的情况。
2. 在 prompt 里加明确的产品名。
3. 如果一类 prompt 持续加载错域,更新 SKILL.md 路由表 —— 把
   模糊触发词移到正确的域(或者拆成两行)。

### 10.3 `scripts/lint_metadata.py` 失败

**症状**:输出 `FAIL <file>.md: <error>`;exit code 1。

**常见原因**:

| 错误 | 修复 |
|------|------|
| `no file-level YAML frontmatter block found` | 文件缺文件顶部的 `---...---` 块;按 `docs/reform/schema.md` 补一个。 |
| `id 'L-XXX' does not match heading 'L-YYY'` | frontmatter 里的 `id:` 必须和下面 `## L-NNN` heading 完全匹配。 |
| `id 'L-XXX' not monotonically increasing` | 你加的新 L-NNN ID 小于已有的;用下一个未用 ID。 |
| `promotion.status=promoted requires non-null promotion.target` | 填 `promotion.target` 为 `"references/<file>.md#<anchor>"`。 |
| `layer 'X' not in [L1, L2, L3, L4, L5]` | 拼错或用错层;lessons 默认 L3,references 默认 L4。 |

### 10.4 `scripts/run_evals.py --mode a` 报覆盖 gap

**症状**:`FAIL A-NNN: <prompt> — expected reference X (0 matching triggers among N)`。

**修复**:扩展 SKILL.md 里 reference X 的路由行,加一个 prompt 里
出现的关键词。示例:A-070 最初失败,因为 prompt 说 "disk usage"
但 SKILL.md 只列了 "disk full"。修复是给 log-collection.md 触发
词表加 "disk usage" 和 "/var/log"。

### 10.5 Push 报凭据错误(WSL)

**症状**:`fatal: could not read Password for '<url>': No such
device or address` 或 `Password authentication is not supported
for Git operations`。

**修复(一次性配置)**:让 WSL 里的 git 指向 Windows 侧的 Git
Credential Manager:

```bash
git config --global credential.helper '!"/mnt/c/Program Files/Git/mingw64/bin/git-credential-manager.exe"'
```

如果 Windows GCM 里没缓存有效的 OAuth token,先从 Windows Git
Bash 侧 push 一次 —— GCM 会弹浏览器 OAuth,缓存一个新 token。之后
WSL push 就通了。

### 10.6 Post-commit hook 报错

**症状**:`git commit` 后出现关于 `C:/claude-obsidian/.vault-meta/
...: No such file or directory` 的警告。

**修复**:你的 `.git/hooks/post-commit` 是老的硬编码版本。重新
安装跨平台版:

```bash
./scripts/install-git-hooks.sh --force
```

---

## 11. 附录

### 11.1 术语表

| 术语 | 定义 |
|------|------|
| **5×5×3** | 知识方法论:5 层存储 × 5 种类型 × 3 级成熟度 |
| **L-NNN** | Lesson 标识,每文件内单调编号(L-001, L-002, …)。一旦分配不可变。 |
| **L1–L5** | 存储层(现场 / 流程 / 沉淀库 / 规范 / 战略) |
| **M1–M3** | 成熟度 —— `draft`, `verified`, `canonical` |
| **Promotion 晋升** | 把 `draft` lesson 通过纳入 `references/*.md` 提升为 `verified` |
| **Demotion 降级** | 把 `verified` lesson 因为新 SR 推翻而回退到 `draft` |
| **渐进加载** | SKILL.md 作为路由表,只加载匹配域的 reference/lesson 文件的模式 |
| **SR** | Service Request —— 触发会话的 Avaya 客户工单 |
| **SKILL.md** | 在 `skills/avaya-debug/SKILL.md` 的路由表 + 核心 skill 指令 |
| **frontmatter** | 文件顶部(或每条 L-NNN 前)的 YAML 块,声明机器可解析的元数据 |
| **canonical** | 内容存活在 `references/` —— 团队的官方立场 |
| **GC** | Garbage collection —— `/avaya-gc` 的季度清理工作流 |

### 11.2 文件地图(什么在哪里)

| 关注点 | 文件 |
|--------|------|
| Skill 路由表 | `skills/avaya-debug/SKILL.md` |
| 核心不变量(always loaded) | `skills/avaya-debug/references/diagnostic-principles.md` |
| 域 references(L4) | `skills/avaya-debug/references/<domain>.md` × 15 |
| 现场 lessons(L3) | `skills/avaya-debug/lessons/<domain>.md` × 16 |
| L1 triage 层 | `skills/avaya-debug/triage/{README,symptom-catalog,session-template}.md` |
| Slash 命令(L2) | `commands/avaya-{sr,report,logs,learn,gc}.md` |
| 子代理 | `agents/avaya-debugger.md` |
| Activation evals | `evals/activation.md` |
| Output-quality evals | `evals/output-quality.md` |
| Metadata lint | `scripts/lint_metadata.py` |
| Eval harness | `scripts/run_evals.py` |
| Git hooks(版本控制里) | `scripts/hooks/` + `scripts/install-git-hooks.sh` |
| CI workflows | `.github/workflows/knowledge-lint.yml`, `eval-full.yml` |
| Pre-commit 配置 | `.pre-commit-config.yaml` |
| 改造历史 | `docs/reform/PLAN.md` |
| Frontmatter schema | `docs/reform/schema.md` |
| 插件身份 | `.claude-plugin/plugin.json` |
| Claude Code 指引 | `CLAUDE.md` |
| Codex 指引 | `AGENTS.md` |
| 高层介绍 | `README.md` |

### 11.3 L-NNN YAML schema(速查)

```yaml
---
id: L-NNN                    # 必须匹配下面的 ## L-NNN heading
layer: L3                    # L1 | L2 | L3 | L4 | L5(lessons 默认 L3)
type: experience             # fact | process | decision | experience | pattern
maturity: draft              # draft | verified | canonical
versions:                    # 适用版本;不确定填 [TBD]
  - "AEP 8.1.x"
provenance:
  sr: "1-23647477802"        # SR 编号(字符串)
  date: "2026-07-14"         # 捕获日期(ISO)
promotion:
  status: pending            # pending | promoted | rejected
  target: null               # promoted 时:"references/<file>.md#<anchor>"
  date: null                 # promoted 或 rejected 时:ISO 日期
  note: null                 # 可选自由文本
owner: "@github 用户名"
---
```

### 11.4 References 文件 frontmatter(速查)

```yaml
---
title: "<可读的标题>"
layer: L4
scope: "<一行 scope 描述>"
maturity: canonical
applicable_versions:
  - "AES 10.x"
  - "AES 8.1.x"
last_reviewed: "2026-06-03"
owner: "avaya-debug skill"
staleness_risks:
  - "<风险 1>"
  - "<风险 2>"
related_docs:
  - "diagnostic-principles.md"
  - "lessons/aes-cti-jtapi.md"
---
```

### 11.5 相关文档

- `CLAUDE.md` —— Claude Code 指引(也涵盖 5×5×3 概览)
- `AGENTS.md` —— Codex 指引(镜像 CLAUDE.md)
- `README.md` —— 高层插件介绍
- `docs/reform/PLAN.md` —— 产出 v2.0.0 的六阶段改造
- `docs/reform/schema.md` —— YAML frontmatter 契约
- `skills/avaya-debug/lessons/README.md` —— L-NNN 模板和晋升规则
- `skills/avaya-debug/triage/README.md` —— L1 层说明

---

*指南版本 1.0 — 2026-07-14。问题请到
https://github.com/calvinmao/avaya-troubleshooting/issues 反馈。*
