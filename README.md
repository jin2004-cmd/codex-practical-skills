# AI 实用 Skill 库 · Practical AI Skills

**21 ready-to-use Codex / Claude Agent skills for the four things AI assistants keep getting wrong: mixing up facts, deciding on impulse, overwriting a live site, and shipping unvalidated LLM output.**

Zero dependency · Privacy-safe · Copy one folder and it works.

**四件事**：事实记串 · 决策拍脑袋 · 发布覆盖线上 · LLM 输出没校验。
[跳到安装](#install) · [按场景找 skill](#scenarios)

[![Skills](https://img.shields.io/badge/skills-21-blue)](#contents)
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
- 国内打不开 GitHub Pages、想免注册给别人看 → `cf-pages-deploy`
- 改了静态站但线上还是老样子 → `static-site-deploy-verify`
- 要做一个能双击打开、能存数据、能导出的表/台账/看板 → `single-file-html-tool`
- 台账里一堆公司名点不开、或者合并备份并出了重复公司 → `job-application-tracker`
- 不知道某家公司的官方校招投递页在哪、JD 是不是过期的 → `recruiting-source-hunting`
- 要把纯前端网页应用上架到 Anna 应用市场 → `anna-app-publish`
- 两台电脑各有一个记忆库，想合成一份 → `memory-sync-abc`

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
- `workflow-distiller`: turn a repeated, validated process into a narrow reusable Skill without copying secrets or expanding authorization.
- `memory-sync-abc`: keep one private GitHub repo as the always-latest superset of two or more machine-local memory vaults — whitelist gitignore, GitHub API fallback when git transport is blocked, and "check the remote, not your local log".
  （多机记忆同步：A/B/C 三库只增不删；代理环境下 git 不通改走 Git Data API；判断线上状态先查远端，本地 git log 会骗人）

### Local tooling

- `single-file-html-tool`: build and verify a zero-dependency single-file HTML tool (tracker, ledger, dashboard).
  Covers four gates that decide whether the file actually works: **seed versioning** (bump `SEED_VERSION`
  or existing users keep seeing stale seed data), **end-to-end field-name consistency** (a `url`/`u` mismatch
  silently drops every link while all scripts still exit 0), **static visual affordance** for clickable
  elements (implemented ≠ visible), and a **fake-DOM smoke test** that executes the page script for real,
  because `node --check` validates syntax only and cannot catch a first-screen crash.
  Ships `scripts/fake_dom_smoke.js`.
  （单文件 HTML 工具四道门：种子版本号、字段全链路同名、可点击元素静态可辨、假 DOM 真跑；
  `node --check` 只查语法，抓不到首屏崩溃。附脚手架脚本）

> 求职层共 6 个 skill，按投递链路分工，互不重叠：
> `recruiting-source-hunting` 找链接 → `job-application-screener` 决定投不投 →
> `resume-jd-matcher` 检查简历怎么改 → `job-application-tracker` 记录投了没 →
> `offer-decision-framework` 比较 Offer → `vibecoding-resume-story` 把项目写进简历。

### Deployment

- `cf-pages-deploy`: deploy a static GitHub repo to Cloudflare Pages and get a China-accessible `*.workers.dev` URL with auto-redeploy on push. Records three dead ends (Gitee Pages permanently offline, gh-proxy only proxies raw files, local git push blocked by GFW 443) and the "Missing git connection" front-end cache gotcha.
  （Cloudflare Pages 国内镜像标准流程：Build command 留空、Root `/`、F5 刷新解 Missing git connection；Gitee Pages / gh-proxy / 本地 git 443 三条死路别再试）
- `static-site-deploy-verify`: after any static-site push, run one pass that catches "I updated it but the site still shows the old version" — missing pushes, local/remote content drift, Service Worker cache lists, HTML references, and PWA trinity.
  （静态站推完校验：专治"缓存名 bump 了、文件内容还是旧的"版本撕裂；修复必须**推齐文件 + 再 bump 一次 CACHE** 两步一起做）

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
