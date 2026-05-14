# Python Docserver and GitHub Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add locked `uv` dependency management, Rustdoc-like Python API docs, a local docs server, and GitHub Pages deployment.

**Architecture:** Use `pyproject.toml` as the dependency source and commit `uv.lock` as the reproducibility artifact. Use `pdoc` to generate API docs into `site/api`, add a small static landing page at `site/index.html`, and deploy the complete `site/` directory through GitHub Pages Actions.

**Tech Stack:** Python 3.10-3.12, `uv`, `pdoc`, GitHub Actions Pages workflow.

---

## File Structure

- Create `pyproject.toml`: project metadata, Python requirement, dependencies migrated from `requirements.txt`, and docs dependency group.
- Create `uv.lock`: generated lockfile committed to enforce dependency consistency.
- Modify `requirements.txt`: either remove after migration or replace with a short note pointing users to `uv`; keep only if backwards compatibility is required.
- Create `scripts/build_docs.py`: builds the static landing page and generated pdoc API docs into `site/`.
- Create `scripts/serve_docs.py`: serves generated docs locally after building them.
- Create `.github/workflows/docs.yml`: GitHub Pages deployment using `uv sync --locked --group docs`.
- Modify `.gitignore`: ignore generated `site/` and pdoc/cache artifacts.
- Modify `README.md`: document `uv` setup, dependency changes, local docs preview, and Pages deployment.

---

### Task 1: Add `uv` Project Metadata

**Files:**
- Create: `pyproject.toml`
- Modify: `requirements.txt`
- Test: local command verification

- [ ] **Step 1: Create `pyproject.toml`**

Add this file:

```toml
[project]
name = "agentic-theorem-prover"
version = "0.1.0"
description = "A playground for free and lightweight LLM-guided Isabelle/HOL provers."
readme = "README.md"
requires-python = ">=3.10,<3.13"
dependencies = [
    "isabelle-client",
    "scikit-learn",
    "xgboost",
    "joblib",
    "requests",
    "tabulate",
    "fastapi",
    "uvicorn",
    "torch",
]

[dependency-groups]
docs = [
    "pdoc",
]

[tool.uv]
package = false
```

- [ ] **Step 2: Replace `requirements.txt` with a migration note**

Use this content:

```text
# Dependencies are managed with uv.
# Install uv, then run:
#   uv sync
#
# Documentation dependencies:
#   uv sync --group docs
```

- [ ] **Step 3: Generate the lockfile**

Run:

```powershell
uv lock
```

Expected: `uv.lock` is created or updated.

- [ ] **Step 4: Verify the lockfile can sync**

Run:

```powershell
uv sync --locked
```

Expected: command succeeds without modifying `uv.lock`.

---

### Task 2: Add Static Docs Build Script

**Files:**
- Create: `scripts/build_docs.py`
- Test: `uv run python scripts/build_docs.py`

- [ ] **Step 1: Create `scripts/build_docs.py`**

```python
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = REPO_ROOT / "site"
API_DIR = SITE_DIR / "api"
DOC_MODULES = ["planner", "prover", "isabelle_ui.server"]


def _write_landing_page() -> None:
    index_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agentic Theorem Prover Docs</title>
  <style>
    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.55;
      color: #172033;
      background: #f7f8fb;
    }
    main {
      max-width: 880px;
      margin: 0 auto;
      padding: 56px 24px;
    }
    h1 {
      margin: 0 0 12px;
      font-size: clamp(2rem, 4vw, 3.25rem);
      line-height: 1.08;
    }
    p {
      max-width: 680px;
      font-size: 1.05rem;
    }
    nav {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 28px;
    }
    a {
      color: #0b5cad;
      font-weight: 650;
    }
    nav a {
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      background: #fff;
      padding: 10px 14px;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <main>
    <h1>Agentic Theorem Prover Documentation</h1>
    <p>
      Generated documentation for the planner, prover, and Isabelle UI modules.
      The API reference is built from Python docstrings and type hints using pdoc.
    </p>
    <nav aria-label="Documentation links">
      <a href="./api/">API Reference</a>
      <a href="https://github.com/">Repository</a>
    </nav>
  </main>
</body>
</html>
"""
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (SITE_DIR / "index.html").write_text(index_html, encoding="utf-8")


def main() -> int:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)

    _write_landing_page()

    command = [
        sys.executable,
        "-m",
        "pdoc",
        "--output-directory",
        str(API_DIR),
        *DOC_MODULES,
    ]
    subprocess.run(command, cwd=REPO_ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the docs build**

Run:

```powershell
uv sync --group docs
uv run python scripts/build_docs.py
```

Expected: `site/index.html` and `site/api/index.html` exist.

---

### Task 3: Add Local Docs Server

**Files:**
- Create: `scripts/serve_docs.py`
- Test: `uv run python scripts/serve_docs.py`

- [ ] **Step 1: Create `scripts/serve_docs.py`**

```python
from __future__ import annotations

import argparse
import http.server
import socketserver
import functools

import build_docs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and serve project documentation.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args(argv)

    build_docs.main()

    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(build_docs.SITE_DIR),
    )

    with socketserver.TCPServer((args.host, args.port), handler) as server:
        url = f"http://{args.host}:{args.port}/"
        print(f"Serving documentation at {url}")
        server.serve_forever()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the server**

Run:

```powershell
uv run python scripts/serve_docs.py --port 8000
```

Expected: terminal prints `Serving documentation at http://127.0.0.1:8000/`.

---

### Task 4: Add GitHub Pages Workflow

**Files:**
- Create: `.github/workflows/docs.yml`
- Test: workflow syntax review plus local locked build

- [ ] **Step 1: Create `.github/workflows/docs.yml`**

```yaml
name: Documentation

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Set up uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Install dependencies
        run: uv sync --locked --group docs

      - name: Build documentation
        run: uv run python scripts/build_docs.py

      - name: Configure Pages
        uses: actions/configure-pages@v5

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Verify locked local build**

Run:

```powershell
uv sync --locked --group docs
uv run python scripts/build_docs.py
```

Expected: both commands succeed and `uv.lock` is unchanged.

---

### Task 5: Update Ignore Rules and README

**Files:**
- Modify: `.gitignore`
- Modify: `README.md`
- Test: `git status --short`

- [ ] **Step 1: Update `.gitignore`**

Append:

```gitignore

# Generated documentation
site/
.pdoc/
```

- [ ] **Step 2: Update README Python setup**

Replace the pip-based install block in section `1.2 Python setup` with:

```markdown
Install `uv`: https://docs.astral.sh/uv/getting-started/installation/

```bash
uv sync

# If you plan to use CPU-only PyTorch wheels, follow the PyTorch index guidance
# before locking or syncing a CPU-only environment.
```

Dependency changes should be made through `uv` so `uv.lock` stays current:

```bash
uv add requests
uv remove requests
uv lock
```
```

- [ ] **Step 3: Add README documentation section**

Add a section near the usage or project structure docs:

```markdown
## Documentation

This repository uses `pdoc` to generate Python API documentation and `uv` to keep documentation builds reproducible.

Build static docs locally:

```bash
uv sync --group docs
uv run python scripts/build_docs.py
```

Serve docs locally:

```bash
uv run python scripts/serve_docs.py
```

The GitHub Pages workflow builds with `uv sync --locked --group docs`, so dependency metadata and `uv.lock` must be updated together.
```

- [ ] **Step 4: Check generated files are ignored**

Run:

```powershell
git status --short
```

Expected: `site/` is not listed, while source files and `uv.lock` are listed.

---

### Task 6: Final Verification

**Files:**
- Verify all created and modified files

- [ ] **Step 1: Run docs build from the lockfile**

Run:

```powershell
uv sync --locked --group docs
uv run python scripts/build_docs.py
```

Expected: docs build succeeds.

- [ ] **Step 2: Verify expected output files**

Run:

```powershell
Test-Path site\index.html
Test-Path site\api\index.html
```

Expected: both commands print `True`.

- [ ] **Step 3: Review git diff**

Run:

```powershell
git diff -- pyproject.toml requirements.txt scripts/build_docs.py scripts/serve_docs.py .github/workflows/docs.yml .gitignore README.md docs/superpowers/specs/2026-05-14-python-docserver-github-pages-design.md docs/superpowers/plans/2026-05-14-python-docserver-github-pages.md
```

Expected: diff contains only dependency-management, docs-generation, docs workflow, and documentation updates.
