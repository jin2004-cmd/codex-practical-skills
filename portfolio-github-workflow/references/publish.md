# Publish safely

- Use standard Git transport; do not use the GitHub Contents API, base64 payloads, generated payload files, or local `/v1/responses` endpoints.
- Commit only intended files, run `scripts/safe_publish.ps1 -RepoPath <repo>` without `-Push`, and run with `-Push` only when deployment is authorized.
- Never force-push, auto-merge, reset, or overwrite a diverged branch. Retry an ordinary transient Git failure at most once; stop on 403, authentication, policy, or blocked-session errors.
