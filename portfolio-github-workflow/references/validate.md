# Validate changes

- Check desktop and narrow mobile layout, media framing, navigation/anchors, keyboard focus, reduced motion, console errors, broken requests, and at least one real playback.
- Use `git diff --check`, `git diff --stat`, and an exact staged-file review.
- After publishing, fetch the page with a cache-busting query, verify the new marker and each media URL, then report commit, URL, checks, and limitations.
