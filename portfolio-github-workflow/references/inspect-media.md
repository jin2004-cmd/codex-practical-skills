# Inspect and media handling

- Read the handoff and repository instructions, then record status, remote, commit, and public URL.
- Inventory each requested video: filename, dimensions, orientation, duration, codec, and size. Prefer `ffprobe`; otherwise use an installed browser's `videoWidth`, `videoHeight`, and duration.
- Match portrait media to 9:16 and landscape media to 16:9. Use `contain` when the full frame matters.
- Keep one small poster per video, stable aspect ratios, `preload="none"` below the first viewport, and no multiple autoplay videos.
- For large or HEVC sources, create an H.264/AAC web copy with faststart and preserve the original outside the repository. Treat 20 MB as a review threshold and never approach GitHub's 100 MB hard limit.
