"""Build step: turn the Python source of truth into docs/apples.json.

Run directly (``python build.py``) or via ``serve.py``. The front end never
touches Python — it just fetches the generated JSON. (The site lives in
``docs/`` so GitHub Pages can serve it straight from the repo.)
"""

from __future__ import annotations

import json
from pathlib import Path

from data.apples import APPLES, validate

ROOT = Path(__file__).parent
OUT = ROOT / "docs" / "apples.json"


def build() -> Path:
    validate(APPLES)
    payload = {
        "generated_by": "build.py",
        "count": len(APPLES),
        "apples": [a.to_dict() for a in APPLES],
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return OUT


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out.relative_to(ROOT)} ({len(APPLES)} apples).")
