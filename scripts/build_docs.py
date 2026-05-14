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
      <a href="https://github.com/madiabio/agentic-theorem-prover">Repository</a>
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
