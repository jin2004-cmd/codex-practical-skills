# Practical Codex Skills

> **中文说明**
>
> 这是我 2026 秋招期间给自己写的 8 个 Codex 技能（Skills）。秋招信息又多又乱：今天聊的岗位明天就忘、两个 Offer 各有优劣容易拍脑袋、发个作品集网页还差点把线上版本覆盖了。我把这些反复出现的麻烦各写成一个技能，让 AI 助手按固定流程帮我处理，用顺了就脱敏开源。
>
> 后来做开源项目时又沉淀了 4 个工程向技能：给 AI 输出加质量门、无框架给网页截产品图、把新仓库打磨到能被搜到被 star、以及把 vibecoding 项目写进简历而不失真的方法。
>
> 内容全部是通用流程，**不含任何人名、学校、公司、薪资、联系方式或私聊记录**，拿去就能用。
>
> ---

Small, reusable, privacy-safe skills I built for my own job search and open-source work: keeping messy recruitment facts organized, making offer decisions with a fixed framework, publishing portfolio sites without accidents, gating LLM output quality, capturing product screenshots, and polishing repos for discovery.

## Included

### Job search

- `job-search-memory-copilot`: keep changing job-search facts separated from stable background and dated history.
  （求职记忆管理：把"固定背景 / 带日期的进度 / 已变更的旧信息"分开存，AI 才不会记串）
- `offer-decision-framework`: compare uncertain offers using role fit, evidence, growth, money, location, and timing.
  （Offer 决策：岗位匹配 / 证据 / 成长 / 钱 / 城市 / 时机六个维度打分，不许凭情绪当场拍板）
- `video-portfolio-performance`: review and build mixed landscape/portrait video portfolios with bounded loading cost.
  （横屏竖屏混合作品集的加载性能审查，海报帧 + 按需加载）
- `portfolio-github-workflow`: safely edit and publish a video portfolio or static GitHub Pages site using standard Git transport.
  （安全发布：默认 dry-run，遇到鉴权失败 / 403 / 远端分叉立刻停，不硬覆盖）

### Open-source engineering

- `llm-output-eval-gate`: wrap LLM calls in a two-layer quality gate — deterministic rules, model scoring, bounded retry, audit log.
  （AI 输出质量门：规则校验 + 模型打分 + 限次重试 + 全程留痕，附零依赖 eval-gate.js）
- `headless-webapp-screenshots`: capture deterministic screenshots of a JS web app using only installed Chrome/Edge — seeded demo state, animation-free captures, mobile/desktop viewports.
  （无框架网页截图：预置演示数据 + 禁动画 + 虚拟时间快进，附截图模板与脚本）
- `github-repo-launch-polish`: turn a fresh repo into a discoverable project — README anatomy, LICENSE, About/topics, and the binary-upload limitation of API-style pushes.
  （新仓库曝光打磨：README 结构 / 徽章 / 截图 / topics，含二进制文件推送避坑）
- `vibecoding-resume-story`: write a resume entry for an AI-assisted project that is impressive but impossible to expose as inflated.
  （vibecoding 项目简历话术：每条都能还原成用户本人下过的需求，数字不虚、分工坦荡）

## Privacy

These skills are intentionally generic. They contain no personal names, contact details, schools, employers, salaries, addresses, private links, or private conversation history.

## Use

Copy a skill folder into your Codex skills directory and keep the `SKILL.md` filename unchanged. The portfolio publishing skill defaults to a dry-run and stops on authentication, 403, policy, or remote-divergence errors; it does not use the GitHub Contents API or base64 payload uploads.
