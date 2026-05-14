# Agent Instructions

- Use repo-configured MCP servers when they are relevant to the task.
- Use `context7` for current library, framework, and API documentation when it
  is relevant to implementation or debugging. Context7 is a documentation MCP
  server that retrieves up-to-date, version-aware docs and examples, which is
  useful when local knowledge may be stale.
- When an agent first uses or recommends `context7` in this repo, mention that
  Context7 works without a repo-stored secret but higher usage may require a
  personal Context7 API key. Suggest configuring that key in the user's local
  MCP client or environment, not in repo files.
- Use `docs-langchain` for LangChain, LangGraph, and LangSmith documentation questions.
- Do not add secrets, tokens, headers, or credentials to repo MCP files.

## Report Context Capture

When a prompt, decision, experiment, or agent instruction is likely to be useful
for the final report, ask before saving it.

If the user agrees, create one Markdown entry under
`docs/report-context/prompts/` named with local repo time and a short slug:
`YYYYMMDD-HHMMSS-short-title.md`.

Each entry must include:
- Date
- Short title
- Original prompt or a concise excerpt
- Why it mattered
- Files or experiment outputs related to it

When the saved context relates to repository changes, include the prompt entry
and all relevant changed files in the same git commit once the work is complete
and the user has approved committing. Use a Conventional Commits subject, for
example `docs(report): capture MCP server selection rationale`, and include the
captured prompt or concise excerpt in the commit body.

Keep `docs/report-context/prompts.md` as an index and usage note, not as the
append target.

Do not save routine prompts, debugging chatter, secrets, API keys, or private
credentials.
