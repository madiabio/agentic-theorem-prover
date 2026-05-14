# Report Prompt Context

This file records selected prompts, decisions, and agent instructions that may
be useful when writing the final report. It is intentionally selective; routine
chat, debugging chatter, secrets, API keys, and private credentials should not
be added here.

## 2026-05-14 - Repo MCP Config

Prompt:
> Add repo-scoped MCP configuration so anyone who clones this repository gets
> the same LangChain documentation MCP server for Codex, Claude Code, and VS
> Code/Copilot.

Why it mattered:
This records the decision to make MCP setup reproducible across Codex, Claude
Code, and VS Code/Copilot using one canonical source file with committed native
client configs.

Related files:
- `.agents/mcp.servers.json`
- `scripts/sync_mcp_configs.py`
- `.codex/config.toml`
- `.mcp.json`
- `.vscode/mcp.json`
- `AGENTS.md`
