# 2026-05-14 - Timestamped Prompt Log Refactor

Date: 2026-05-14

Short title: Timestamped Prompt Log Refactor

Original prompt:
> The prompt maybe shouldnt be in just one file, maybe it should make a log at
> the datetime so that multiple people dont conflict too.

Why it mattered:
This changed the report-context capture workflow from appending all selected
prompts to one shared Markdown file to creating one timestamped Markdown file
per entry. The new structure reduces merge conflicts when multiple people or
agents save report context in parallel, while keeping `prompts.md` as an index
and usage note.

Related files:
- `AGENTS.md`
- `docs/report-context/prompts.md`
- `docs/report-context/prompts/20260514-151400-repo-mcp-config.md`
- `docs/report-context/prompts/20260514-160900-mcp-server-selection-research.md`
- `docs/report-context/prompts/20260514-161451-timestamped-prompt-log-refactor.md`
