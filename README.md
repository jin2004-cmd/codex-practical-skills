# AI 实用 Skill 库 · Practical AI Skills

**28 ready-to-use Codex / Claude Agent skills for the four things AI assistants keep getting wrong: mixing up facts, deciding on impulse, overwriting a live site, and shipping unvalidated LLM output.**

Zero dependency · Privacy-safe · Copy one folder and it works.

**四件事**：事实记串 · 决策拍脑袋 · 发布覆盖线上 · LLM 输出没校验。
[跳到安装](#install) · [按场景找 skill](#scenarios)

[![Skills](https://img.shields.io/badge/skills-28-blue)](#contents)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero dependency](https://img.shields.io/badge/runtime%20dependency-none-green)](#install)
[![Privacy](https://img.shields.io/badge/privacy-no%20personal%20data-brightgreen)](#privacy)

> **中文说明**
>
> 这是我 2026 秋招期间给自己写的一组 Codex 技能（Skills）。秋招信息又多又乱，今天聊的岗位明天就忘，两个 Offer 各有优劣容易拍脑袋，发个作品集网页还差点把线上版本覆盖了。我就把这些反复出现的麻烦各写成一个技能，让 AI 助手按固定流程帮我处理，用顺了就脱敏开源。
>
> 后来做开源项目和 Remotion 影片，又沉淀了一批工程向的技能。给 AI 输出加质量门，无框架给网页截产品图，把新仓库打磨到能被搜到被 star，Remotion 影片的史料表述与导出验收，还有把 vibecoding 项目写进简历但不失真。以及被 GFW 卡住的时候，怎么把 GitHub 静态站镜像到 Cloudflare 的国内可访问域名。
>
> 内容全部是通用流程，**不含任何人名、学校、公司、薪资、联系方式或私聊记录**，拿去就能用。

---

## If you only remember three entry points

| 我想解决什么 | 用哪个 |
|---|---|
| 秋招信息记串、Offer 选不明白、项目是 AI 写的不敢写进简历 | `personal-secretary-memory`（求职层）+ `offer-decision-framework` + `vibecoding-resume-story` |
| 作品集要改又要发，怕把线上搞挂 | `video-portfolio-performance` 看性能，`portfolio-github-workflow` 负责发布 |
| AI 返回的东西不能直接用、流程想沉淀成技能 | `llm-output-eval-gate` + `workflow-distiller` |
| GitHub Pages 国内打不开、要给别人分享 | `cf-pages-deploy` 一键镜像到 Cloudflare |

## Scenarios

- 我投了几十家，AI 助手老是记混哪家的进度 → `personal-secretary-memory`（见 references/job-search.md）
- 两个实习 Offer 不知道选哪个 → `offer-decision-framework`
- 项目是 AI 写的，简历上不敢写「我实现了」 → `vibecoding-resume-story`
- 作品集网页视频太多，手机一打开就卡 → `video-portfolio-performance`
- 要改线上作品集，怕把 GitHub Pages 覆盖 → `portfolio-github-workflow`
- LLM 经常返回格式不对的 JSON，用户直接看到报错 → `llm-output-eval-gate`
- 要给 SPA 截产品图，不想装 Puppeteer → `headless-webapp-screenshots`
- 新仓库没人看，README 不知道怎么写 → `github-repo-launch-polish`
- Remotion 导出的片子要验收，转场抽帧、字幕边缘、音轨都要查 → `remotion-delivery-qa`
- 做历史题材的 Remotion 影片，怕史料说错、原作失真 → `historical-remotion-film`
- 助手换了、上下文断了，怎么接着干 → `session-checkpoint` + `personal-secretary-memory`
- 一个流程重复做了三遍，想变成技能 → `workflow-distiller`
- 面试录音/逐字稿，想看自己哪句话扣分 → `interview-debrief`
- 给别人做付费面试诊断，要交一份能转发的 Word → `interview-debrief`（顾问模式）
- 笔试倒计时里卡在一道算法题上 → `online-assessment-solver`
- 国内打不开 GitHub Pages、想免注册给别人看 → `cf-pages-deploy`
- 改了静态站但线上还是老样子 → `static-site-deploy-verify`
- 要做一个能双击打开、能存数据、能导出的表/台账/看板 → `single-file-html-tool`
- 台账里一堆公司名点不开、或者合并备份并出了重复公司 → `job-application-tracker`
- 不知道某家公司的官方校招投递页在哪、JD 是不是过期的 → `recruiting-source-hunting`
- 要把纯前端网页应用上架到 Anna 应用市场 → `anna-app-publish`
- 两台电脑各有一个记忆库，想合成一份 → `memory-sync-abc`
- 想转一个全新的岗位方向，不知道人家到底要什么 → `career-pivot-research`
- 检修老仓库，却不确定「main 还是旧版」这种说法还成不成立 → `github-repo-repair-audit`
- 简历内容都对了，就是压不进一页、引导词太长、不知道哪句该加粗 → `resume-polish-craft`
- 答案写得像 AI，要换成他本人说话的语气 → `personal-tone-writing`
- 以前写过的稿子、脚本、版本找不到了 → `session-log-archaeology`

## Contents

- [Job search](#job-search)
- [Portfolio and publishing](#portfolio-and-publishing)
- [Open-source engineering](#open-source-engineering)
- [Local tooling](#local-tooling)
- [App platform publishing](#app-platform-publishing)
- [Remotion video](#remotion-video)
- [Memory and workflow](#memory-and-workflow)
- [Deployment](#deployment)

### Job search

- `offer-decision-framework`: compare uncertain offers using role fit, evidence, growth, money, location, and timing.
  （Offer 决策：岗位匹配 / 证据 / 成长 / 钱 / 城市 / 时机六个维度打分，不许凭情绪当场拍板）
- `vibecoding-resume-story`: write a resume entry for an AI-assisted project that is impressive but impossible to expose as inflated.
  （vibecoding 项目简历话术：每条都能还原成用户本人下过的需求，数字不虚、分工坦荡）
- `resume-jd-matcher`: pre-application resume-to-JD match check — machine-check hard requirements and keyword coverage, flag gaps in three tiers, rewrite only from real experience.
  （简历-JD 机检：硬条件 + 关键词覆盖率逐词核验；缺失项分「真没做过 / 做过没写 / 语义同义」三档，只基于真实经历改写）
- `job-application-screener`: screen a batch of job listing screenshots — read every image, reverse-look-up the JD, rate fit, output a fixed four-section report with referral codes inline per job.
  （岗位批量筛选：逐张读图并报总数、反查 JD、评级、四段式输出；内推码必须和岗位写在同一行）
- `recruiting-source-hunting`: find official campus-recruiting links and current JDs — check existing structured data first, then university career sites and company-built portals, cross-verify before writing anything down.
  （校招信息溯源：先查手上的结构化数据有没有现成字段，别绕远路全网搜；单一来源不落笔，搜不到就说搜不到）
- `job-application-tracker`: maintain a single-file application ledger — status enum that never collapses 无岗 into 未投, 100% clickable company links in three visual tiers, visited receipts, and duplicate-safe backup merging.
  （投递台账：状态语义不许合并；每家公司名都必须点得开；增量备份按「精确名→括号内简称→规范化名→双向包含」顺序匹配）
- `interview-debrief`: turn an interview transcript into a structured debrief, in two modes — self mode (own interview, scored, with a career-track judgement) and consultant mode (paid diagnosis for someone else, delivered as a Word report). Covers the two failure modes that dominate real transcripts: the interviewer naming a direction the candidate never enters, and "how I optimised it" being offered where "what the result was" was asked. Every finding carries the verbatim line, its timestamp, and one sentence the person can actually say next time.
  （面试复盘双模式：**自我模式**带评分和赛道判断；**顾问模式**给别人做诊断、交 Word、不做赛道判断。
  核心抓两类错：面试官已经给了方向候选人没切进去；把"讲方法"当成"讲结果"。
  每条必须原话 + 时间戳 + 一句可直接念的改法。客户姓名学校公司一律泛化）
- `online-assessment-solver`: solve a coding question from a timed written test — reverse-derive the true definition from the samples, hand-write zero-dependency code that pastes straight into an empty `class Solution {}` template, verify against every sample index, and name the method-name risk.
  （笔试算法题：**样例才是真正的规格说明**，题面往往是含糊的；相等元素那一对决定栈里用 `<=` 还是 `<`；
  空模板没有 import，用手写数组栈；倒计时在走时先给完整答案再解释三行，不反问）
- `career-pivot-research`: research whether a career pivot is viable before rewriting a resume for it — collect 5-8 real linkable JDs, derive three capability tiers (minimum bar / full match / beyond), find the project the user already owns but described in the wrong vocabulary, then ship a rewrite table with character-count deltas and a study plan with daily acceptance criteria.
  （转岗调研：先搜真实 JD 再谈匹配；三档能力分开看；最大杠杆是「你已经做了但用旧领域词汇描述」的那个项目；改完简历还要给每日可验收的学习计划）

- `resume-polish-craft`: polish a resume whose content is already right — compress pages, tighten
  bullet lead-ins to four characters, pick one sentence per bullet to bold, keep the persona on the
  target function, and read the layout parameters before deleting anything.
  （简历打磨：**标和删是两件事**，让你加粗就别顺手给删改方案；四字就是四字，不许升格成工整对仗；
  投运营岗要弱化工程味，技术栈行删掉但 AI 工具留在技能栏；
  **超页数先查页边距/字号/行距再谈删内容**，项目经历最后才动）
- `personal-tone-writing`: write in one specific person's voice — punctuation bans, the anti-pivot
  sentence ban, jargon translated to plain speech, identity-first openings, and the boundary rule for
  when the voice library must not be applied. Three delivery shapes disagree: written-test answers
  **require** 2-4 typos, spoken scripts and internal docs **forbid** them.
  （个人语气库写作：破折号冒号分号引号全禁；`不是A而是B` 一篇最多一处；术语全禁、条目 3-5 条；
  **他自己的原稿和要你翻出来的旧稿一律不许过语气库**；口播稿按 4.5-5 字/秒先定时长，反串钩子 5 秒内翻脸）

### Portfolio and publishing

- `video-portfolio-performance`: review and build mixed landscape/portrait video portfolios with bounded loading cost.
  （横屏竖屏混合作品集的加载性能审查，海报帧 + 按需加载；只管看，不管发）
- `portfolio-github-workflow`: safely edit and publish a video portfolio or static GitHub Pages site using standard Git transport.
  （安全发布：默认 dry-run，遇到鉴权失败 / 403 / 远端分叉立刻停，不硬覆盖）

> 这两个都针对作品集网站，但分工不同：**看性能、改视觉用 `video-portfolio-performance`，改完要发布用 `portfolio-github-workflow`。**

### Open-source engineering

- `llm-output-eval-gate`: wrap LLM calls in a two-layer quality gate — deterministic rules, model scoring, bounded retry, audit log.
  （AI 输出质量门：规则校验 + 模型打分 + 限次重试 + 全程留痕，附零依赖 `scripts/eval-gate.js`）
- `headless-webapp-screenshots`: capture deterministic screenshots of a JS web app using only installed Chrome/Edge — seeded demo state, animation-free captures, mobile/desktop viewports.
  （无框架网页截图：预置演示数据 + 禁动画 + 虚拟时间快进，附截图模板与脚本）
- `github-repo-launch-polish`: turn a fresh repo into a discoverable project — README anatomy, LICENSE, About/topics, and the binary-upload limitation of API-style pushes.
  （新仓库曝光打磨：README 结构 / 徽章 / 截图 / topics，含二进制文件推送避坑）
- `github-repo-repair-audit`: repair and audit an existing repo — verify what is actually on the remote before acting, compare local vs remote at byte level (sha and size both lie), reproduce a bug in a sandbox before fixing it, and update every artifact that quotes a number you changed.
  （老仓库检修：**先查远端再动手**，任务描述会过期；判定内容一致要下载比字节，sha 和 size 都会骗人；修 bug 先复现；改了数字要回头改所有引用它的地方）

> 这两个都动 GitHub 仓库，但分工不同：**新仓库要被人搜到用 `github-repo-launch-polish`，老仓库要修 bug / 核状态用 `github-repo-repair-audit`。**

### App platform publishing

- `anna-app-publish`: package a pure frontend SPA and ship it on the Anna AI OS app platform — manifest schema choice, the three rules that `extra="forbid"` rejects outright, CSP inline-handler rewrite, bundle upload, and the review-before-publish state machine.
  （Anna 上架：manifest 里**绝不写 name/version**；schema ≥ 2 的纯 UI 应用 Executas 可留空；`script-src` 无 `unsafe-inline`，内联事件必须改事件委托；`apps publish` 不等于上架）

### Remotion video

- `historical-remotion-film`: produce or iterate Remotion films about historical art, museum collections, ancient paintings, and cultural motifs.
  （历史艺术 Remotion 影片：原作保真、史料表述、电影化运动、原创拟音分开处理）
- `remotion-delivery-qa`: run reproducible delivery QA on Remotion MP4 exports.
  （Remotion 导出验收：转场抽帧、全帧技术与文字边界检查、音轨核验、作品与工程双目录归档）

> Remotion 相关只有这两个：做片子用 `historical-remotion-film`，导完验收用 `remotion-delivery-qa`。

### Memory and workflow

- `personal-secretary-memory`: maintain dated personal-assistant memory and prepare a bounded cross-assistant handoff without hard-coded private paths. Job-search tracking is one of its topic areas, see `references/job-search.md`.
- `session-checkpoint`: keep a compact, verifiable continuation checkpoint for long-running assistant projects.
- `workflow-distiller`: turn a repeated, validated process into a narrow reusable Skill — check the remote index first because a duplicate is the dominant failure, distil the failure modes rather than the happy path, desensitise names and employers out of the Example block, and sync README plus CHANGELOG in the same commit. Also covers the silent clobber when two sessions push to the same repo within an hour: fetch the current file shas, build the tree on that base, and fetch the file back afterwards to confirm.
  （沉淀技能：先查远端索引，重复建同类 skill 是最常见的错；**写踩过的坑而不是正确流程**；
  脱敏要查 Example 块里的真人名和雇主名；README 与 CHANGELOG 必须同一次提交改完；
  两个会话并发推送会静默互相覆盖——推送前拉当前 sha，推完再把文件拉回来验一遍）
- `memory-sync-abc`: keep one private GitHub repo as the always-latest superset of two or more machine-local memory vaults — whitelist gitignore, GitHub API fallback when git transport is blocked, and "check the remote, not your local log".
  （多机记忆同步：A/B/C 三库只增不删；代理环境下 git 不通改走 Git Data API；判断线上状态先查远端，本地 git log 会骗人）

- `session-log-archaeology`: dig an original artifact out of the user's own archives — dated memory
  notes, then session logs, then repo snapshots, then workspace logs. Records the JSONL shape traps
  that produce silent zero hits, the cross-machine gap that makes a session genuinely absent, and the
  rule that a miss must be reported rather than filled with a rewrite.
  （会话考古：按「记忆 → 会话 jsonl → 私仓快照 → 工作区日志」顺序找；
  **jsonl 的 content 是顶层字段、block type 是 output_text**，按 message.content 取会一直 0 命中；
  日志按机器存，家侧/公司端有缺口是正常的；**翻不到就直说，不许拿重写填空**）

### Local tooling

- `single-file-html-tool`: build and verify a zero-dependency single-file HTML tool (tracker, ledger, dashboard).
  Covers six gates that decide whether the file actually works: **seed versioning** (bump `SEED_VERSION`
  or existing users keep seeing stale seed data), **end-to-end field-name consistency** (a `url`/`u` mismatch
  silently drops every link while all scripts still exit 0), **static visual affordance** for clickable
  elements (implemented ≠ visible), a **fake-DOM smoke test** that executes the page script for real
  (because `node --check` validates syntax only and cannot catch a first-screen crash), and — when patching
  a page that is already online — a **byte-level minimal insert** proven harmless by deleting the inserted
  block and asserting the result equals the original byte for byte.
  Ships `scripts/fake_dom_smoke.js`.
  （单文件 HTML 工具六道门：种子版本号、字段全链路同名、可点击元素静态可辨、假 DOM 真跑、
  **改已上线页面用字节级插入**、**删掉插入块必须等于原文件**；
  `node --check` 只查语法，抓不到首屏崩溃。附脚手架脚本）

> 求职层共 10 个 skill，按投递链路分工，互不重叠：
> `career-pivot-research` 想转什么方向 → `recruiting-source-hunting` 找链接 →
> `job-application-screener` 决定投不投 → `resume-jd-matcher` 检查简历怎么改 → `resume-polish-craft` 打磨措辞与版面 →
> `job-application-tracker` 记录投了没 → `online-assessment-solver` 过笔试 →
> `interview-debrief` 面完复盘 → `offer-decision-framework` 比较 Offer →
> `vibecoding-resume-story` 把项目写进简历。

### Deployment

- `cf-pages-deploy`: deploy a static GitHub repo to Cloudflare Pages and get a `*.workers.dev` URL with auto-redeploy on push. ⚠️ **Corrected 2026-10-26: `*.workers.dev` is DNS-poisoned in mainland China — direct connections time out.** The v1.0.0 claim of "China-accessible" was wrong and cost a real portfolio: three "no VPN needed" buttons and twelve `<video src>` pointed at it, and none of them opened. Still worth using for auto-redeploy, but the output is for self/VPN use only — host anything you send to an interviewer on `*.github.io`. Records three dead ends (Gitee Pages permanently offline, gh-proxy only proxies raw files, local git push blocked by GFW 443) and the "Missing git connection" front-end cache gotcha.
  （Cloudflare Pages 标准流程：Build command 留空、Root `/`、F5 刷新解 Missing git connection；Gitee Pages / gh-proxy / 本地 git 443 三条死路别再试。**勘误：workers.dev 境内直连不通，别再当"国内镜像"用**）
- `static-site-deploy-verify`: the static-site checklist for **before and after** a push. Before: a three-round preflight (links / structure / content) — dead links, **case-sensitive path mismatches that only break on Linux**, absolute-path leaks, and every external link probed **with the local proxy bypassed** (`ProxyHandler({})`), because "opens through my proxy" is not "opens for them". After: the version-tear pass — missing pushes, local/remote content drift, Service Worker cache lists, HTML references, PWA trinity. Includes a reachability verdict table for mainland China and `scripts/preflight_audit.py`.
  （静态站发布前**三轮体检** + 推完校验：死链/大小写/外链直连实测；"缓存名 bump 了、文件内容还是旧的"版本撕裂；修复必须**推齐文件 + 再 bump 一次 CACHE** 两步一起做）

## Before / After

**LLM output, without and with a gate**

```js
// Before: whatever comes back goes straight to the user
var plan = await callLLM(prompt);
render(plan);

// After: validated, retried, logged
var res = await EvalGate.gate({
  name: "plan", generate: callLLM, validate: rules, judge: score,
  threshold: 7, maxRetries: 2
});
render(res.result);   // 永远有东西可渲染，每次尝试都留日志
```

**Publishing a portfolio site**

```powershell
# Before: push and hope
git push origin main

# After: dry-run first, stop on any auth / 403 / divergence error
./safe_publish.ps1 -DryRun     # 先看清会改什么
./safe_publish.ps1             # 确认无误再真发
```

## Install

```bash
# 全量
git clone https://github.com/jin2004-cmd/codex-practical-skills.git ~/.codex/skills/codex-practical-skills

# 只取一个 skill（以质量门为例）
mkdir -p ~/.codex/skills/llm-output-eval-gate
curl -L https://raw.githubusercontent.com/jin2004-cmd/codex-practical-skills/main/llm-output-eval-gate/SKILL.md \
  -o ~/.codex/skills/llm-output-eval-gate/SKILL.md
```

Or just copy a skill folder into your Codex skills directory and keep the `SKILL.md` filename unchanged. The portfolio publishing skill defaults to a dry-run and stops on authentication, 403, policy, or remote-divergence errors; it does not use the GitHub Contents API or base64 payload uploads.

Runtime note: `personal-secretary-memory/scripts/validate_memory.py` needs PyYAML (`pip install pyyaml`). Everything else is zero dependency.

## Privacy

These skills are intentionally generic. They contain no personal names, contact details, schools, employers, salaries, addresses, private links, or private conversation history.

The memory and workflow skills are genericized exports. They do not contain a user's vault, local state JSON, credentials, company material, or private conversations.

## Contributing

用得上就点个 ⭐，我会按 star 数决定下一批先补哪个方向的 skill。

发现某个 skill 在你的场景里触发不了、跑不通，或者描述跟实际行为对不上，直接开 issue 贴你的输入和期望输出，我一般两天内回。

想贡献自己的 skill：开 issue 用一句话说清场景和触发条件，我帮你判断是新建还是并入已有的（重复能力优先合并，不新增）。

## License

MIT — see [LICENSE](LICENSE).
