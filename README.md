# Practical Codex Skills

> **中文说明**
>
> 这是我 2026 秋招期间给自己写的 4 个 Codex 技能（Skills）。秋招信息又多又乱：今天聊的岗位明天就忘、两个 Offer 各有优劣容易拍脑袋、发个作品集网页还差点把线上版本覆盖了。我把这些反复出现的麻烦各写成一个技能，让 AI 助手按固定流程帮我处理，用顺了就脱敏开源。
>
> 内容全部是通用流程，**不含任何人名、学校、公司、薪资、联系方式或私聊记录**，拿去就能用。
>
> ---

Small, reusable, privacy-safe skills I built for my own job search: keeping messy recruitment facts organized, making offer decisions with a fixed framework, and publishing portfolio sites without accidents.

## Included

- `job-search-memory-copilot`: keep changing job-search facts separated from stable background and dated history.
  （求职记忆管理：把"固定背景 / 带日期的进度 / 已变更的旧信息"分开存，AI 才不会记串）
- `offer-decision-framework`: compare uncertain offers using role fit, evidence, growth, money, location, and timing.
  （Offer 决策：岗位匹配 / 证据 / 成长 / 钱 / 城市 / 时机六个维度打分，不许凭情绪当场拍板）
- `video-portfolio-performance`: review and build mixed landscape/portrait video portfolios with bounded loading cost.
  （横屏竖屏混合作品集的加载性能审查，海报帧 + 按需加载）
- `portfolio-github-workflow`: safely edit and publish a video portfolio or static GitHub Pages site using standard Git transport.
  （安全发布：默认 dry-run，遇到鉴权失败 / 403 / 远端分叉立刻停，不硬覆盖）

## Privacy

These skills are intentionally generic. They contain no personal names, contact details, schools, employers, salaries, addresses, private links, or private conversation history.

## Use

Copy a skill folder into your Codex skills directory and keep the `SKILL.md` filename unchanged. The portfolio publishing skill defaults to a dry-run and stops on authentication, 403, policy, or remote-divergence errors; it does not use the GitHub Contents API or base64 payload uploads.
