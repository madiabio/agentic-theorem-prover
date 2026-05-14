#!/usr/bin/env python3
"""Generate repo-scoped MCP client configs from one canonical source."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / ".agents" / "mcp.servers.json"
CLAUDE_PATH = ROOT / ".mcp.json"
CODEX_PATH = ROOT / ".codex" / "config.toml"
VSCODE_PATH = ROOT / ".vscode" / "mcp.json"


def load_servers() -> dict[str, dict[str, str]]:
    try:
        data = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing canonical MCP config: {SOURCE_PATH}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {SOURCE_PATH}: {exc}") from None

    if not isinstance(data, dict) or set(data) != {"servers"}:
        raise ValueError('canonical MCP config must contain only a top-level "servers" object')

    servers = data["servers"]
    if not isinstance(servers, dict) or not servers:
        raise ValueError('"servers" must be a non-empty object')

    normalized: dict[str, dict[str, str]] = {}
    for name in sorted(servers):
        config = servers[name]
        if not isinstance(name, str) or not name:
            raise ValueError("server names must be non-empty strings")
        if not isinstance(config, dict) or set(config) != {"url"}:
            raise ValueError(f'server "{name}" must contain only a "url" field')

        url = config["url"]
        if not isinstance(url, str) or not url:
            raise ValueError(f'server "{name}" url must be a non-empty string')

        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f'server "{name}" must use an HTTPS MCP URL')

        normalized[name] = {"url": url}

    return normalized


def json_text(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def toml_string(value: str) -> str:
    return json.dumps(value)


def codex_toml(servers: dict[str, dict[str, str]]) -> str:
    chunks: list[str] = []
    for name, config in servers.items():
        chunks.append(f"[mcp_servers.{name}]\nurl = {toml_string(config['url'])}")
    return "\n\n".join(chunks) + "\n"


def generated_outputs(servers: dict[str, dict[str, str]]) -> dict[Path, str]:
    return {
        CLAUDE_PATH: json_text({"mcpServers": servers}),
        CODEX_PATH: codex_toml(servers),
        VSCODE_PATH: json_text({"servers": servers}),
    }


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def check_outputs(outputs: dict[Path, str]) -> list[Path]:
    stale: list[Path] = []
    for path, expected in outputs.items():
        try:
            actual = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            stale.append(path)
            continue
        if actual != expected:
            stale.append(path)
    return stale


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate client MCP configs from .agents/mcp.servers.json."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if generated MCP configs are stale",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        outputs = generated_outputs(load_servers())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check:
        stale = check_outputs(outputs)
        if stale:
            print("stale MCP config files:", file=sys.stderr)
            for path in stale:
                print(f"  {path.relative_to(ROOT).as_posix()}", file=sys.stderr)
            return 1
        return 0

    write_outputs(outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
