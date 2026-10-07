# Changelog

All notable changes to this repository are documented here. Every skill carries a `version` field in its `SKILL.md` frontmatter.

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
