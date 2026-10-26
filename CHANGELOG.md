# Changelog

All notable changes to this repository are documented here. Every skill carries a `version` field in its `SKILL.md` frontmatter.

## 2026-10-26 — v1.8.0

**Skill 数量不变，仍是 28** —— 本次是升级一个已有 skill，不是新增。

### Added / Changed（`static-site-deploy-verify` 1.1.0 → 1.2.0）

新增**第四轮 · 图像素材**（可选）。起因是首页改版时页面三轮体检全绿、线上也 200，
但用户一句「太难看了」——问题全在图本身，前三轮一项都查不到：

- **ffmpeg crop 超出源尺寸会静默补黑边。** 按记忆写 `crop=2560:1000:0:180`，
  而源实际是 1920×1080，ffmpeg 不报错，直接产出一张 1600×900 里含 **207 行纯黑**的图。
  规则：crop 的 w/h 必须 ≤ 源尺寸，写之前先 `-i` 打一次源尺寸。
- **源片可能自带 letterbox。** crop 参数没错也不行：成片 1080p、内容只有 933 行，
  上下各 70px 黑边。暗色网页会把黑边吃掉，肉眼完全看不出来。
  给出按行亮度剖面定位内容区、再按目标比例回推宽度的可复用代码。
- **选帧要先扫全片再定。** `range(6, duration, 4)` 抽 20+ 帧拼对比图，
  同时算每帧 mean 与顶/底文字峰，再让视觉模型挑。省的是来回返工。
- **截图 OCR 会失真，数字必须回源文件核对。** 实测把「全部 10」读成「全部 5」、
  把「SOP · 过程文档」读成「SOP · 流程文档」。凡截图里读到的数字与专有名词，
  一律 grep 源文件后再改——否则会把对的改错。

### Verified

本次改版实跑：11 个页面 66 条本地相对链接死链 0 / 大小写 0 / 绝对路径泄漏 0；
结构轮 0 问题；内容轮 10 / 5 / 4 / 35 各单值。
首屏图交付前自检 `(rows<26).sum()==0`、mean 106.5。
线上 `?v=` 复测 index.html 与两张 jpg 全 200。

## 2026-10-26 — v1.7.0

**Skill 数量不变，仍是 28** —— 本次是「更正一条错结论 + 升级一个 skill」，不是新增。

### Fixed

- **`cf-pages-deploy` 1.0.0 → 1.1.0：核心结论被实测推翻。**
  v1.0.0 写「生成国内免翻墙可访问的 `*.workers.dev` 地址」「这就是国内免翻墙地址」
  「workers.dev 电信联通秒开」—— 三句全错。2026-10-26 境内**直连、不挂任何代理**实测三个已部署子域，全部超时：

  | 子域 | 解析到 |
  |---|---|
  | `talkcal.jinjiaxin2004.workers.dev` | 173.255.213.90 |
  | `daypilot.jinjiaxin2004.workers.dev` | **31.13.96.195（Meta 的 IP 段，即被劫持）** |
  | `ai-video-portfolio.jinjiaxin2004.workers.dev` | 67.228.235.91 |

  同一时刻 `*.github.io` 184–698 ms 全 200。
  **这个错误有真实代价**：作品集首页三个「在线版（免翻墙）」按钮 + 视频页 12 条成片的
  `<video src>` 全挂在这些子域上 —— 面试官点开一条都播不了，页面还写着"免翻墙"。
  原文不删，加顶部勘误块 + 三处原地更正（`~~删除线~~` 保留原句），并改写 description 与 README 索引行。

### Changed

- **`static-site-deploy-verify` 1.0.0 → 1.1.0：从"推完校验"扩成"发布前后全流程"。**
  新增第一部分「推之前 —— 三轮体检」：
  **链接轮**（本地相对链接 / **大小写一致性** / 绝对路径泄漏 / 外链**绕开本机代理**直连实测）、
  **结构轮**（标签配平 / 重复 id / 锚点目标 / alt / title+viewport / 内联 JS 语法 / rel=noopener）、
  **内容轮**（同一指标多值冲突 / 占位符残留）。
  新增「可达性判定表」（`*.github.io` ✅ / `github.com` 慢且不稳 / `*.workers.dev` ❌ / gh-proxy 只代理 raw）、
  「公开站 ≠ 打包件」的合法差异做法（`.replace()` + `assert count == 1` + 推后 diff 行数对账）、
  以及「CHANGELOG 说改过 ≠ 真的改过」的翻车实录。

### Added

- `static-site-deploy-verify/scripts/preflight_audit.py` —— 上面三轮的可执行版：
  `--root <站点目录>` 一把跑完，`--no-net` 跳过联网，`--json` 机器可读，
  有死链 / 大小写 / JS 语法 / 绝对路径时退出码 1。
  已在本仓作品集（11 页 / 65 条本地链接 / 18 条外链）实跑：**阻断 0 项**。

### Verified this pass

- 11 个页面：标签配平、重复 id、锚点目标、`data-goto` 目标、图片 alt、`<title>`、viewport、
  内联脚本语法、`target=_blank` 的 `rel=noopener` —— 全部 0 问题
- 18 条外链**直连**实测全 200（184–1304 ms）
- 线上 `workers.dev` / `gh-proxy` 计数归零；Pages `built` 后加 `?v=` 复测通过

## 2026-10-25 — v1.6.0

Skill count **25 → 28**.

### Added

- `resume-polish-craft` (v1.0.0) — polish a resume whose content is already right. Leads with the
  rule that failed hardest: **format tasks and content tasks are different tasks**. Asked to mark
  which sentences deserve bold, the previous pass returned eleven deletions instead, which reads as
  destroying approved work. Covers the four-character lead-in (a summary, not a slogan — and four
  characters does not mean "upgrade it into a tidy couplet"), the persona rule for
  non-engineering applications (drop the tech-stack line, keep AI tooling in the skills row),
  one bold per bullet, and the layout-before-content rule: read page margins, font size and line
  spacing and try 10pt / 13pt before deleting a single project.
  Distinct from `resume-jd-matcher` (match against one JD) and `vibecoding-resume-story`
  (turn one project into an entry).
- `personal-tone-writing` (v1.0.0) — write in one specific person's voice. Step 0 is the boundary
  rule, and it exists because of a real failure: asked to retrieve an old script, the search came
  up empty and a fresh one was written in his voice instead — running an original through the voice
  library **is** rewriting it, which defeats the retrieval. Then the punctuation bans
  (dash, colon, semicolon, quotes), the anti-pivot sentence ban (`不是A而是B` more than once reads
  as machine-written), jargon-to-plain-speech, identity-first openings, and the three delivery
  shapes that actively disagree: written-test answers **require** 2-4 typos, spoken scripts and
  internal docs **forbid** them. Spoken scripts fix duration first (4.5-5 chars/second) and must
  land the reverse-play flip inside 5 seconds.
- `session-log-archaeology` (v1.0.0) — dig an original artifact out of the user's own archives, in
  order: dated memory notes → session logs → repo snapshots → workspace logs. Encodes the JSONL
  shape traps that produce silent zero hits (`content` is a top-level field, block type is
  `output_text`, not `text` — reading `obj["message"]["content"]` matches nothing forever), the
  cross-machine gap that makes a session genuinely absent (logs are per machine; a clean afternoon
  gap between two evening blocks means "other machine", not "never written"), and the rule that a
  miss is reported rather than filled with a rewrite.
  Distinct from `session-checkpoint` (writes a checkpoint) and `personal-secretary-memory`
  (maintains the memory base).

### Changed

- `README.md` — job-search chain roll-up **9 → 10** with `resume-polish-craft` inserted after
  `resume-jd-matcher`; three new scenario lines; skill badge and headline recounted from the
  remote listing.

## 2026-10-22 — v1.5.0

Skill count **24 → 25**.

### Added

- `online-assessment-solver` (v1.0.0) — solve a coding question from a timed written test. Leads with
  "the samples are the spec, the prose is not": one sample mismatch kills a hypothesis, so the
  definition is reverse-derived index by index before any code is written. Calls out the equal-element
  pair specifically, because that single pair decides `<=` vs `<` in a monotonic-stack pop and is where
  most wrong answers come from. Ships as zero-dependency code — an empty `class Solution {}` template
  has no `import`, so a hand-written array stack beats `ArrayDeque` and nothing is left as `// TODO`.
  Answers before asking: with a countdown running, an unverified reading is stated inline and answered
  in full, never turned into a clarifying question.
  Distinct from `career-pivot-research` (whether to aim at a role) and `resume-jd-matcher` (one JD).

### Changed

- `interview-debrief` **v1.0.0 → v2.0.0** — split into two modes, because self-debrief and paid
  diagnosis for someone else share almost nothing: consultant mode drops the scoring, drops the
  career-track judgement (that is the client's call, not the report's), and delivers a Word file
  instead of Markdown. Adds the two failure modes that dominate real transcripts — the interviewer
  naming a direction the candidate never enters, and "how I optimised it" offered where "what the
  result was" was asked — plus a four-layer severity ladder and a mandatory four-part finding
  (verbatim line, timestamp, mechanism, one sentence to say next time). Records two tool traps:
  `WebFetch` truncates a Feishu doc at the first large table, and the transcript command lives under
  `note`, not `meeting`. Requires every client name, school and employer to be generalised.
- `workflow-distiller` **v1.0.1 → v2.0.0** — expanded from six lines to the full distillation pass.
  Step 1 is now "check the index on the remote before creating anything", because the dominant failure
  is a duplicate: this release wanted a new interview Skill until the index showed `interview-debrief`
  already existed. Adds the desensitisation table with the leaks that actually happen (names,
  employers, offer status, and — hardest to spot — real client events reused as the Example), the
  "I never verified it ≠ it is wrong" rule that follows from deleting a real number once, and the
  concurrent-session clobber: two pushes an hour apart silently replaced each other, so fetch the file
  shas first and fetch the file back afterwards.

### Fixed

- `README.md` omitted `interview-debrief` entirely — the folder existed with a `SKILL.md` but no index
  entry, no scenario, and no changelog line, making it invisible to anyone browsing. Now listed under
  Job search and folded into the 9-skill application chain.

## 2026-10-21 — v1.4.0

Skill count **22 → 24**.

### Added

- `career-pivot-research` (v1.0.0) — research whether a career pivot is viable *before* rewriting a
  resume for it. Collects 5-8 real JDs with source links, derives three capability tiers
  (minimum bar / full match / beyond), and hunts for the project the user already owns but
  described in the wrong vocabulary. Ships a rewrite table with character-count deltas and a
  study plan whose every day has an acceptance artifact.
  Distinct from `resume-jd-matcher` (one JD, go/no-go) and `job-application-screener` (batch ranking).
- `github-repo-repair-audit` (v1.0.0) — repair and audit an **existing** repo. Leads with
  "verify the remote before you touch anything", because the dominant failure is acting on a
  description that already went stale. Covers byte-level local/remote comparison, the >1 MB
  contents-API limitation, sandbox reproduction, and updating every artifact that quotes a
  number you changed.
  Distinct from `github-repo-launch-polish` (new repo discoverability).

### Changed

- `single-file-html-tool` **v1.0.0 → v1.1.0** — four gates became six. Added gate 6:
  **patching a page that is already online.** Re-generating the whole file drags in template
  drift, encoding and line-ending noise, and produces a diff nobody can review. Patch at byte
  level instead, then prove it by deleting the inserted block and asserting the result equals the
  original byte for byte. Also states when *not* to write an `og:image` at all.
- `resume-jd-matcher` **v1.1.0 → v1.2.0** — added Step 4, the rewrite table, for when the ask is
  「照着 JD 改简历」rather than 「匹配吗」. Per-location rows with original / rewritten / character
  delta / rationale / risk tag, copy buttons, and the rule that every red-row delta ships with a
  compressed alternative. Adds the "find the mislabelled project" step — the highest-leverage move
  in a rewrite, since it needs no invented material.

### Why these two, and not more

Both came from work that was actually finished and re-checked the same day, and neither overlapped
an existing capability (`workflow-distiller`: prefer a focused update to a duplicate). Four smaller
candidates were deliberately **not** promoted — single-occurrence fixes belong in the daily log.

## 2026-10-21 — v1.3.1

### Fixed

- **`personal-secretary-memory`** — the `Example` block carried real employer names and real
  application events carried over from the private copy. Replaced with generic placeholders
  (`A 公司` / `B 公司`, no dates, no employers). This is a public repo; the intro promised
  no names, schools, employers, or salaries, and the example contradicted that promise.
- **`cf-pages-deploy`** — added the missing `version` field. It was the only one of 21 skills
  without it, which breaks any script that reads the field uniformly.
- **`recruiting-source-hunting`** — reworded the "real lesson" note. The lesson is worth keeping;
  recording that the operator was sworn at is not appropriate content for a public repo.

## 2026-10-21 — v1.3.0

### Added

- **`single-file-html-tool`** (`version: 1.0.0`) — build and verify a zero-dependency single-file HTML
  tool. Four gates: seed versioning (`SEED_VERSION` must be bumped whenever seed data changes, or returning
  users silently keep old data), end-to-end field-name consistency (template writes `url`, build emits `u`,
  seed reads `c.u` → every link dropped while all scripts exit 0), static visual affordance for clickable
  elements, and a fake-DOM smoke test. Ships `scripts/fake_dom_smoke.js`, which stubs
  `document`/`localStorage`/`window`/`FileReader` and runs the page script through `new Function`.
  Two recorded gotchas: Node 22 makes `globalThis.navigator` a getter-only property (needs
  `Object.defineProperty`), and replacing `global.URL` wholesale breaks Node's own fs shim.
- **`job-application-tracker`** (`version: 1.0.0`) — status enum for an application ledger, where
  `无岗` / `待查验` must never collapse into `未投`; 100% clickable company names across three visual
  tiers (direct / mailto / search fallback); visited receipts in a separate localStorage key;
  and incremental backup merging with a strict match order (exact → parenthesised short name →
  normalised → bidirectional containment). Ships `scripts/merge_backup.py`.
  Two recorded gotchas: dropping 集团/科技/技术 during normalisation collides `TCL科技` into `TCL`,
  and a company that appears "missing" may actually exist with 0 jobs — backfill, don't insert.
- **`recruiting-source-hunting`** (`version: 1.0.0`) — source tiers for official campus-recruiting
  links and current JDs: company-built job portals > university career sites > third-party job banks >
  search fallback. Rule 0 is to read the structured data you already hold before searching the open web.
  Also records URL parameters that leak referral codes (`recommendCode=`, `spread=`, `?KeyWords=`).
- **`job-application-screener`** (`version: 2.0.0`) — **desensitized public edition of an existing
  private skill.** Batch-screens job listing screenshots: read every image and report the count,
  reverse-look-up the JD, rate fit, then emit a fixed four-section report with referral codes inline.
  Personal paths, real referral codes, and private profile content were removed; see the Setup section.
- **`resume-jd-matcher`** (`version: 1.1.0`) — pre-application resume-to-JD match check, ported from
  a local skill. Ships `scripts/match_resume.py` for hard requirements, keyword coverage, and duplicate lines.

## 2026-10-19 — v1.2.0

### Added

- **`anna-app-publish`** (`version: 1.0.0`) — ship a pure frontend SPA on the Anna AI OS app platform.
  Records the three rules that get a manifest rejected outright: `name`/`version` must never appear
  (Pydantic `extra="forbid"`), `required_executas` may be empty on `schema ≥ 2` bundle-only apps
  (the Console's "at least one Executa" hint is a `schema: 1` leftover), and `apps publish` is not
  the same as going live. Also covers the CSP rewrite: `script-src` has no `'unsafe-inline'` and
  `csp_overrides.script-src` cannot add one, so inline `onclick` handlers must become event delegation.
- **`static-site-deploy-verify`** (`version: 1.0.0`) — one verification pass after any static-site push,
  targeting "I updated it but the site still shows the old version". Five checks: missing pushes,
  local/remote content drift, Service Worker cache lists, HTML references, PWA trinity. The fix for
  version tearing is two steps together — push every drifted file **and** bump `const CACHE` again.
- **`memory-sync-abc`** (`version: 1.0.0`) — one private GitHub repo as the always-latest superset of
  two or more machine-local vaults. Whitelist `.gitignore`, Git Data API fallback when git transport
  is blocked by a proxy, and the rule that local `git log` lies (API-style pushes create no local commit).

### Changed

- Repository title is now **AI 实用 Skill 库 · Practical AI Skills**; README headline and skill badge
  updated from 13 to 16.
- README gains an `App platform publishing` section and four new scenario lines.

### Fixed

- **`cf-pages-deploy` shipped with no CHANGELOG entry.** It was added after v1.1.0, which is why
  v1.1.0 says "the repository now ships 12 skills" while the README badge already said 13. This entry
  records it retroactively; the skill is treated as part of v1.2.0.

### Known gaps

- `cf-pages-deploy/SKILL.md` still has no `version` field in its frontmatter, unlike the other 15 skills.
- Three skills referenced in personal memory are **not** in this repository because their source text
  was never authored here and cannot be reconstructed without inventing content:
  `job-hunt-copilot`, `shanghai-rental-inspection`, `feishu-task-delivery`.
- Skills from other authors (`obsidian-markdown`, `json-canvas` by kepano; `impeccable`; `taste-skill`;
  `remotion-best-practices`; the realestate skill set) are deliberately **not** vendored here — they are
  MIT/upstream work and re-publishing them under this repository would misattribute authorship.

## 2026-10-07 — v1.1.0

### Changed

- **Merged `job-search-memory-copilot` into `personal-secretary-memory`.** Two skills were both
  maintaining dated facts with evidence levels, and the job-search case is a topic area of the
  same memory base, not a separate capability. The three-layer model, the seven rules, and the
  example now live in `personal-secretary-memory/references/job-search.md`; the standalone skill
  folder is removed. The repository now ships 12 skills.
- `personal-secretary-memory` is `version: 1.1.0` and its description points at the new reference.

### Removed

- `job-search-memory-copilot/` (content preserved as `personal-secretary-memory/references/job-search.md`).

## 2026-10-07 — v1.0.2

### Added

- `## Example` in the last four skills that had none: `historical-remotion-film`,
  `remotion-delivery-qa`, `session-checkpoint`, `personal-secretary-memory`.
  All 13 skills now ship at least one worked example.

### Changed

- Those four are now `version: 1.0.2`.

## 2026-10-07 — v1.0.1

### Added

- `## Example` section in the six skills that previously shipped as a bare `SKILL.md`:
  `github-repo-launch-polish`, `job-search-memory-copilot`, `offer-decision-framework`,
  `vibecoding-resume-story`, `video-portfolio-performance`, `workflow-distiller`.
- `README.md`: one line naming the four problems, plus jump links to Install and Scenarios.
- `.gitattributes` so line endings stop being rewritten per checkout.

### Fixed

- Badges linked to `.`; they now point at real anchors (`#contents`, `#install`, `#privacy`).
- `workflow-distiller/SKILL.md` still named `quick_validate.py`. The wording now refers to
  generic skill-creator tooling instead of a script this repository does not ship.

### Changed

- The six skills above are now `version: 1.0.1`. The other seven stay at `1.0.0`.

## 2026-10-07 — v1.0.0 (first tagged baseline)

This release is a documentation and consistency pass over all 13 skills. No skill logic changed.

### Added

- `version: 1.0.0` in the frontmatter of all 13 skills.
- `README.md`: one-line value proposition and badges at the top, "If you only remember three entry points" table, a scenario index of 12 real user situations, a table of contents, and a `Remotion video` section.
- `README.md`: `Before / After` blocks for the LLM output gate and for portfolio publishing.
- `README.md`: one-command install (full clone and single-skill `curl`).
- `llm-output-eval-gate/SKILL.md`: `Before / After` section with a copy-pasteable gate call.
- `CHANGELOG.md` (this file).
- `.github/ISSUE_TEMPLATE/bug-report.md` and `.github/ISSUE_TEMPLATE/skill-request.md`.
- `.github/PULL_REQUEST_TEMPLATE.md`.

### Fixed

- `README.md` omitted two skills entirely (`historical-remotion-film`, `remotion-delivery-qa`) while the repository description advertised Remotion support. Both are now documented.
- `workflow-distiller/SKILL.md` told the reader to run `quick_validate.py`, a script that does not exist in this repository. Reworded to point at local skill-creator tooling.
- `personal-secretary-memory/SKILL.md` did not mention that `scripts/validate_memory.py` requires PyYAML. The dependency is now stated in the skill and in the README install section.
- `llm-output-eval-gate/SKILL.md` pointed at `assets/eval-gate.js`.

### Changed

- `llm-output-eval-gate/assets/eval-gate.js` moved to `llm-output-eval-gate/scripts/eval-gate.js`, matching every other skill where executable code lives in `scripts/`.
- `historical-remotion-film` and `remotion-delivery-qa` descriptions rewritten in English so all 13 descriptions use one language; the Chinese scope notes stay in the skill body.
- Ten skill descriptions gained an explicit negative boundary ("Not for …" or a cross-reference to the neighbouring skill) so unrelated work stops triggering them:
  `github-repo-launch-polish`, `headless-webapp-screenshots`, `job-search-memory-copilot`, `llm-output-eval-gate`, `offer-decision-framework`, `personal-secretary-memory`, `portfolio-github-workflow`, `session-checkpoint`, `vibecoding-resume-story`, `video-portfolio-performance`.

### Known gaps

- Six skills ship as a single `SKILL.md` with no bundled example, script, or reference yet.
- Only `portfolio-github-workflow` ships `agents/openai.yaml` (the ChatGPT-facing interface file).
- No recorded GIF or video demo yet; see the `Before / After` sections for the textual version.
