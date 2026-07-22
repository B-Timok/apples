"""One command to run the orchard locally.

    python serve.py            # serves on the first free port from 8000
    python serve.py 8080       # start looking from 8080 instead
    PORT=9000 python serve.py  # or set it via the environment

Rebuilds docs/apples.json from the Python data, then serves docs/. Ctrl-C to stop.
"""

from __future__ import annotations

import http.server
import os
import socket
import socketserver
import sys
from functools import partial
from pathlib import Path

from build import build

DEFAULT_PORT = int(os.environ.get("PORT", 8000))
PORT_TRIES = 20  # if the port is busy, hop upward this many times
WEB_DIR = Path(__file__).parent / "docs"


class Server(socketserver.TCPServer):
    # Let a just-restarted server reclaim a socket still in TIME_WAIT.
    allow_reuse_address = True


def serve(start_port: int) -> None:
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(WEB_DIR))
    for port in range(start_port, start_port + PORT_TRIES):
        try:
            httpd = Server(("", port), handler)
        except OSError as err:
            if err.errno == socket.errno.EADDRINUSE:
                print(f"Port {port} is busy, trying {port + 1}...")
                continue
            raise
        with httpd:
            print(f"🍎 8-Bit Orchard running at http://localhost:{port}  (Ctrl-C to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nBye! 🍏")
            return
    raise SystemExit(
        f"Couldn't find a free port in {start_port}-{start_port + PORT_TRIES - 1}. "
        "Stop the other server or pass a different port: python serve.py 8100"
    )


def main() -> None:
    out = build()
    print(f"Built {out.name} — {out.parent.name}/ is ready to serve.")
    start_port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    serve(start_port)


if __name__ == "__main__":
    main()
