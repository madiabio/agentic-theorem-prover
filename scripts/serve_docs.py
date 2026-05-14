from __future__ import annotations

import argparse
import functools
import http.server
import socketserver

import build_docs


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


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

    with ReusableTCPServer((args.host, args.port), handler) as server:
        url = f"http://{args.host}:{args.port}/"
        print(f"Serving documentation at {url}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping documentation server.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
