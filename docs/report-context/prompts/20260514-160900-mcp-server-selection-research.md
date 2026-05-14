# 2026-05-14 - MCP Server Selection Research

Date: 2026-05-14

Short title: MCP Server Selection Research

Original prompt:
> What MCP servers might be useful to add into this repo? do some research and
> consider the context of this assignment.

Why it mattered:
This captured the rationale for extending MCP support in a way that fits the
assignment: an LLM-guided Isabelle/HOL prover with experiment logs, datasets,
planner/prover workflows, and final-report requirements. The main conclusion
was to prefer low-risk, secret-free documentation/model discovery servers in
repo config, keep authenticated services user-local, and consider a custom
repo-local Isabelle/prover MCP server for the most project-specific value.

Related files and outputs:
- `.agents/mcp.servers.json`
- `scripts/sync_mcp_configs.py`
- `.codex/config.toml`
- `.mcp.json`
- `.vscode/mcp.json`
- `README.md`
- `docs/report-context/prompts.md`
- Research notes: Context7, Hugging Face MCP, LangSmith MCP, GitHub MCP, arXiv
  and Semantic Scholar MCP options, plus MCP security guidance.
