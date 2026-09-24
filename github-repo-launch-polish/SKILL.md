---
name: github-repo-launch-polish
description: Turn a freshly pushed code repository into a discoverable, star-ready open-source project. Use when a repo has code but a bare README, no license, no screenshots, no topics, or when preparing a personal project for public exposure and portfolio use.
---

# GitHub Repo Launch Polish

A repo with good code and a bare README gets no stars. Exposure on GitHub comes from search metadata (description, topics, English keywords) and from a README that proves the project works in five seconds.

## README Anatomy (in order)

1. **Centered hero**: name, one-line slogan, what it is in one sentence, badges (live demo, license, stack, PRs welcome via shields.io `for-the-badge` style), quick nav links.
2. **Live demo link** in the hero and again in quick start. A clickable product beats any description.
3. **Screenshot table**: desktop and mobile side by side, real captures of the product's best screen and its differentiating feature. Use the `headless-webapp-screenshots` skill to produce them.
4. **What/why**: the pain point in two sentences, then the one thing this project does differently.
5. **The differentiator with a diagram**: an ASCII flow of the core mechanism (pipeline, state machine, data flow). This is what gets quoted.
6. **Features, quick start, tech stack, project structure, roadmap, contributing.**
7. **English summary section**: one paragraph + demo link. GitHub search and most readers index on English; a Chinese-only README is invisible internationally.
8. **Star call-to-action** at the bottom, one line, centered.

## Repository Metadata (manual, 2 minutes)

MCP/GitHub connectors used for file pushes cannot set these; do them in the web UI and never skip them:

- **About description**: one sentence, front-load English keywords (`AI daily planner with LLM output evaluation`), then Chinese.
- **Website**: tick "Use your GitHub Pages website" when Pages is enabled.
- **Topics**: 8-10 tags mixing domain and stack, e.g. `ai-agent` `llm` `evaluation` `productivity` `vanilla-javascript` `pwa`. Topics are how GitHub search surfaces small repos.

## License

Add a `LICENSE` file (MIT for personal portfolio projects, copyright line = GitHub username + year). No license means "all rights reserved" — many people will not star or fork.

## Publishing Files — Known Limitation

Text files push fine through connector/Contents-API style tools. **Binary files (PNG, GIF, fonts) do not**: the content string is stored as-is, so base64 text lands in the repo as literal text and the image is broken. Verified behavior — do not retry it.

- Push binaries via real Git transport, or drag the folder into the repo's web upload UI (`/upload/main`).
- If a probe was used to test behavior, delete probe files afterwards (`docs/.probe.txt`, `docs/_probe.png` style leftovers make a repo look sloppy).
- After pushing README references to images, open the repo page and confirm every image renders.

## Final Checklist

- [ ] README renders with zero broken images or badge links
- [ ] LICENSE present and linked from README
- [ ] About description + website + topics set
- [ ] Live demo link works from a logged-out / incognito browser
- [ ] No secrets, personal data, employer names, or internal URLs anywhere in the tree (grep for them)
