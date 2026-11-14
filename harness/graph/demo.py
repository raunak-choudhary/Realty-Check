"""python -m harness.graph.demo [--fake] [--no-agent] "<address>"

Prints the run's events as JSON lines for a snapshot built from the synthetic listing text in
tests/graph/listing_fixture.txt. --fake uses the canned synthetic toolbox; --no-agent skips the deep agent.
"""
from __future__ import annotations

import argparse
import json
import sys

from rc_common import REPO

from . import run as run_mod
from .run import run_check
from .toolbox import Toolbox


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m harness.graph.demo")
    ap.add_argument("address", nargs="?", default="100 Example St, Houston, TX 77002")
    ap.add_argument("--fake", action="store_true", help="use the synthetic toolbox (no network)")
    ap.add_argument("--no-agent", action="store_true", help="skip the deep agent; run the fixed plan")
    a = ap.parse_args(argv)
    text = (REPO / "tests" / "graph" / "listing_fixture.txt").read_text(encoding="utf-8")
    snapshot = {"url": "https://example.test/listing", "title": "Synthetic Lofts", "address_text": a.address,
                "text": text, "jsonld": []}
    if a.no_agent:
        run_mod.AGENT_ENABLED = False
    tb = Toolbox.fake() if a.fake else Toolbox.real()
    run_check(snapshot, lambda ev: print(json.dumps(ev), flush=True), tb)
    s = run_mod.LAST_AGENT_STATS
    if s:
        print(json.dumps({k: s.get(k) for k in ("model_calls", "delegations", "parse_failures", "budget_hit", "wall_s")}),
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
