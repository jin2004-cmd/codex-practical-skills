# Changelog

All notable changes to this repository are documented here. Every skill carries a `version` field in its `SKILL.md` frontmatter.

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
