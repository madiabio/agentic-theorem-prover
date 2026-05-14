# 2026-05-14 - uv Docs Lockfile Rationale

## Date

2026-05-14 16:43:11 Australia/Brisbane

## Short title

uv docs lockfile rationale

## Original prompt or concise excerpt

The user asked why the documentation workflow should use `uv`, then clarified that dependency management needs to work reliably on everyone's computer and that dependency changes should update a lockfile.

## Why it mattered

This decision changed the documentation design from a simple `pip`-based GitHub Pages build to a `pyproject.toml` plus committed `uv.lock` workflow. The CI design should use `uv sync --locked --group docs` so documentation builds fail when dependency metadata and the lockfile diverge.

## Files or experiment outputs related to it

- `docs/superpowers/specs/2026-05-14-python-docserver-github-pages-design.md`
- `docs/superpowers/plans/2026-05-14-python-docserver-github-pages.md`
- Planned: `pyproject.toml`
- Planned: `uv.lock`
- Planned: `.github/workflows/docs.yml`
- Planned: `scripts/build_docs.py`
- Planned: `scripts/serve_docs.py`
