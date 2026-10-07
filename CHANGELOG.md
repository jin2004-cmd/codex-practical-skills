# Changelog

All notable changes to this repository are documented here. Every skill carries a `version` field in its `SKILL.md` frontmatter.

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
