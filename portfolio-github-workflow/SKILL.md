---
name: portfolio-github-workflow
description: Safely inspect, edit, validate, and publish video portfolio or static website changes to an existing GitHub Pages repository. Use for portfolio media updates, layout changes, GitHub-backed webpage edits, or deployment verification.
---

# Portfolio GitHub Workflow

Preserve the existing public URL and repository history while making focused portfolio changes. Treat source media, the Git worktree, and the deployed Pages site as three separate states that must each be verified.

## Before Editing

1. Read the project handoff and repository instructions.
2. Resolve the real worktree with `git rev-parse --show-toplevel`; do not edit an exported copy or an API payload snapshot.
3. Record Git status, remote URL, current commit, public URL, and existing user changes.
4. Inventory requested videos before choosing a layout: filename, dimensions, orientation, duration, codec, and size. Use `ffprobe` when available; otherwise read `videoWidth`, `videoHeight`, and duration in an installed browser.
5. Verify authorship and labels. Do not imply a work is original, fully AI-generated, or independently produced without evidence.

## Media Handling

- Match containers to real media ratios: portrait 9:16 and landscape 16:9. Use `object-fit: contain` when the full frame matters.
- Keep one small poster per video and stable aspect ratios to prevent layout shift.
- Use `preload="none"` below the first viewport. Do not autoplay multiple videos.
- For large or HEVC sources, create a web copy rather than uploading the original. Prefer H.264, AAC, `yuv420p`, and `-movflags +faststart`. Preserve the source outside the repository.
- Keep new files well below GitHub's 100 MB hard limit. Treat 20 MB as a review threshold and reduce size when quality remains acceptable.

## Edit And Validate

- Keep edits scoped to the active repository and preserve unrelated user changes.
- Use real posters and work samples. Do not invent clients, metrics, features, or project claims.
- Validate desktop and narrow mobile layouts, media framing, navigation, anchors, keyboard focus, reduced motion, console errors, broken requests, and at least one actual video playback.
- Capture screenshots before publishing when layout changed materially.
- Review `git diff --check`, `git diff --stat`, and the exact files to be committed.

## Publish Safely

Use standard Git transport. Do not use the GitHub Contents API, base64 request bodies, generated `payload*.json` files, or local Codex `/v1/responses` endpoints to publish repository content.

1. Commit only intended files with a descriptive message.
2. Run `scripts/safe_publish.ps1 -RepoPath <repo>` without `-Push`. It checks the worktree, remote, file sizes, remote ancestry, and performs a dry run.
3. Run it again with `-Push` only when the user's request authorizes deployment.
4. Pass `-Proxy <url>` only when project instructions already identify a working Git proxy. The script applies it to that command only; never write a global proxy setting.
5. Never force-push, auto-merge, reset, or overwrite a diverged remote branch.

Limit network retries to one additional attempt for an ordinary transient Git failure. For HTTP 403, authentication failure, a cyber-security policy block, or a blocked Codex session, stop. Preserve the work and report the exact failure; do not hammer reconnect, weaken security settings, or attempt to bypass policy.

## Verify Deployment

- Fetch the public page with a cache-busting query and confirm the new marker is present.
- Check each new media URL returns HTTP 200 and the expected content type.
- Open the deployed site in a real browser and verify new media actually plays.
- Report commit hash, public URL, checks performed, and remaining limitations.
- Update current-state and event-log files when the project uses them.

Keep intermediate payloads, screenshots, and extracted metadata outside the active repository or in a clearly named archive. This workflow cannot guarantee that a session will never be blocked; it avoids the known risky API and retry patterns and stops cleanly when policy blocks occur.
