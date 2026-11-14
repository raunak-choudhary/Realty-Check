"""Shared helpers. Owned by the orchestrator; do not edit from a module task."""
from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent


def private_dir() -> Path:
    """Private driver folder: sponsor kit, .env with keys. Never inside this repo."""
    p = os.environ.get("RC_PRIVATE_DIR")
    if not p:
        raise RuntimeError("RC_PRIVATE_DIR is not set")
    return Path(p)


def cache_dir(*parts: str) -> Path:
    """Folder under <private>/rc_cache/, created on demand. All sponsor data and images go here."""
    d = private_dir() / "rc_cache"
    for part in parts:
        d = d / part
    d.mkdir(parents=True, exist_ok=True)
    return d


_ENV: dict[str, str] | None = None


def secret(name: str) -> str:
    """Read one value from <private>/.env. Never log or return it inside evidence."""
    global _ENV
    if _ENV is None:
        _ENV = {}
        for line in (private_dir() / ".env").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                _ENV[k.strip()] = v.strip().strip('"').strip("'")
    if name not in _ENV:
        raise RuntimeError(f"{name} missing from private .env")
    return _ENV[name]


class RateLimit:
    """Blocks so calls are at least min_gap_s apart (thread-safe)."""

    def __init__(self, min_gap_s: float = 0.6):
        self.gap, self.last, self.lock = min_gap_s, 0.0, threading.Lock()

    def wait(self) -> None:
        with self.lock:
            d = self.gap - (time.monotonic() - self.last)
            if d > 0:
                time.sleep(d)
            self.last = time.monotonic()


def evidence(source: str, status: str, summary: str, observed: dict[str, Any] | None = None,
             images: list[dict[str, str]] | None = None, detail: str = "") -> dict[str, Any]:
    """Build an Evidence record (docs/CONTRACT.md section 2.4)."""
    assert source in ("record", "scan", "aerial", "county"), source
    assert status in ("ok", "no_evidence", "error"), status
    return {"source": source, "status": status, "summary": summary, "observed": observed or {},
            "images": images or [], "detail": detail}


def cached_json(path: Path, build):
    """Return JSON at path, or call build(), save and return it."""
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    obj = build()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1), encoding="utf-8")
    return obj
