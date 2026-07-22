"""One command to run the orchard locally.

    python serve.py

Rebuilds web/apples.json from the Python data, then serves web/ at
http://localhost:8000. Ctrl-C to stop.
"""

from __future__ import annotations

import http.server
import socketserver
from functools import partial
from pathlib import Path

from build import build

PORT = 8000
WEB_DIR = Path(__file__).parent / "web"


def main() -> None:
    out = build()
    print(f"Built {out.name} — {out.parent.name}/ is ready to serve.")
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(WEB_DIR))
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🍎 8-Bit Orchard running at http://localhost:{PORT}  (Ctrl-C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nBye! 🍏")


if __name__ == "__main__":
    main()
