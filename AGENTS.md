# Agent Instructions

- Use repo-configured MCP servers when they are relevant to the task.
- Use `docs-langchain` for LangChain, LangGraph, and LangSmith documentation questions.
- Do not add secrets, tokens, headers, or credentials to repo MCP files.

## Report Context Capture

When a prompt, decision, experiment, or agent instruction is likely to be useful
for the final report, ask before saving it.

If the user agrees, append an entry to `docs/report-context/prompts.md` with:
- Date
- Short title
- Original prompt or a concise excerpt
- Why it mattered
- Files or experiment outputs related to it

Do not save routine prompts, debugging chatter, secrets, API keys, or private
credentials.
