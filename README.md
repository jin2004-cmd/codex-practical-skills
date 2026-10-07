# Practical Codex Skills

**13 ready-to-use Codex / Claude Agent skills for the four things AI assistants keep getting wrong: mixing up facts, deciding on impulse, overwriting a live site, and shipping unvalidated LLM output.**

Zero dependency · Privacy-safe · Copy one folder and it works.

**四件事**：事实记串 · 决策拍脑袋 · 发布覆盖线上 · LLM 输出没校验。
[跳到安装](#install) · [按场景找 skill](#scenarios)

[![Skills](https://img.shields.io/badge/skills-13-blue)](#contents)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero dependency](https://img.shields.io/badge/runtime%20dependency-none-green)](#install)
[![Privacy](https://img.shields.io/badge/privacy-no%20personal%20data-brightgreen)](#privacy)

> **中文说明**
>
> 这是我 2026 秋招期间给自己写的一组 Codex 技能（Skills）。秋招信息又多又乱：今天聊的岗位明天就忘、两个 Offer 各有优劣容易拍脑袋、发个作品集网页还差点把线上版本覆盖了。我把这些反复出现的麻烦各写成一个技能，让 AI 助手按固定流程帮我处理，用顺了就脱敏开源。
>
> 后来做开源项目和 Remotion 影片时又沉淀了工程向技能：给 AI 输出加质量门、无框架给网页截产品图、把新仓库打磨到能被搜到被 star、Remotion 影片的史料表述与导出验收、以及把 vibecoding 项目写进简历而不失真的方法。
>
> 内容全部是通用流程，**不含任何人名、学校、公司、薪资、联系方式或私聊记录**，拿去就能用。

---

## If you only remember three entry points

| 我想解决什么 | 用哪个 |
|---|---|
| 秋招信息记串、Offer 选不明白、项目是 AI 写的不敢写进简历 | `job-search-memory-copilot` + `offer-decision-framework` + `vibecoding-resume-story` |
| 作品集要改又要发，怕把线上搞挂 | `video-portfolio-performance` 看性能，`portfolio-github-workflow` 负责发布 |
| AI 返回的东西不能直接用、流程想沉淀成技能 | `llm-output-eval-gate` + `workflow-distiller` |

## Scenarios

- 我投了几十家，AI 助手老是记混哪家的进度 → `job-search-memory-copilot`
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

## Contents

- [Job search](#job-search)
- [Portfolio and publishing](#portfolio-and-publishing)
- [Open-source engineering](#open-source-engineering)
- [Remotion video](#remotion-video)
- [Memory and workflow](#memory-and-workflow)

### Job search

- `job-search-memory-copilot`: keep changing job-search facts separated from stable background and dated history.
  （求职记忆管理：把「固定背景 / 带日期的进度 / 已变更的旧信息」分开存，AI 才不会记串）
- `offer-decision-framework`: compare uncertain offers using role fit, evidence, growth, money, location, and timing.
  （Offer 决策：岗位匹配 / 证据 / 成长 / 钱 / 城市 / 时机六个维度打分，不许凭情绪当场拍板）
- `vibecoding-resume-story`: write a resume entry for an AI-assisted project that is impressive but impossible to expose as inflated.
  （vibecoding 项目简历话术：每条都能还原成用户本人下过的需求，数字不虚、分工坦荡）

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

### Remotion video

- `historical-remotion-film`: produce or iterate Remotion films about historical art, museum collections, ancient paintings, and cultural motifs.
  （历史艺术 Remotion 影片：原作保真、史料表述、电影化运动、原创拟音分开处理）
- `remotion-delivery-qa`: run reproducible delivery QA on Remotion MP4 exports.
  （Remotion 导出验收：转场抽帧、全帧技术与文字边界检查、音轨核验、作品与工程双目录归档）

> Remotion 相关只有这两个：做片子用 `historical-remotion-film`，导完验收用 `remotion-delivery-qa`。

### Memory and workflow

- `personal-secretary-memory`: maintain dated personal-assistant memory and prepare a bounded cross-assistant handoff without hard-coded private paths.
- `session-checkpoint`: keep a compact, verifiable continuation checkpoint for long-running assistant projects.
- `workflow-distiller`: turn a repeated, validated process into a narrow reusable Skill without copying secrets or expanding authorization.

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
