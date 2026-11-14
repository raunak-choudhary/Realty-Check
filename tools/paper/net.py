"""Polite HTTP for public, keyless government endpoints: one session, <=2 req/s, 15 s timeouts."""
from __future__ import annotations

import requests

from rc_common import RateLimit

UA = "RealityCheck-hackathon/0.1 (HackPrinceton 2026; public records fact-check; keyless)"
TIMEOUT = 15
_rate = RateLimit(0.5)
_session = requests.Session()
_session.headers["User-Agent"] = UA
calls = 0  # network request counter (tests use it to prove cache hits)


def get(url: str, params: dict | None = None, headers: dict | None = None, stream: bool = False):
    """GET with rate limit and timeout. Raises on HTTP errors."""
    global calls
    _rate.wait()
    calls += 1
    r = _session.get(url, params=params, headers=headers, timeout=TIMEOUT, stream=stream)
    r.raise_for_status()
    return r


def get_json_url(url: str, params: dict | None = None):
    """Return (final query URL, parsed JSON). ArcGIS errors arrive as 200 + {"error": ...}."""
    r = get(url, params)
    d = r.json()
    if isinstance(d, dict) and d.get("error"):
        raise RuntimeError(f"service error: {d['error']}")
    return r.url, d


def head_size(url: str) -> int:
    global calls
    _rate.wait()
    calls += 1
    r = _session.head(url, timeout=TIMEOUT, allow_redirects=True)
    r.raise_for_status()
    return int(r.headers["Content-Length"])
