"""Live (cached) tests for tools.paper. Skip when RC_PRIVATE_DIR is unset (the cache lives there).
Run: RC_PRIVATE_DIR=... .venv/Scripts/python.exe -m pytest tests/paper -q
First Houston run builds the HCAD index once (~45 s); later runs read the cache."""
import json
import os

import pytest

if not os.environ.get("RC_PRIVATE_DIR"):
    pytest.skip("RC_PRIVATE_DIR not set", allow_module_level=True)

from tools.paper import county_record, geocode
from tools.paper import net

AUSTIN = "2111 Austin St, Houston, TX 77002"
AUSTIN_LL = (29.7460624, -95.3679203)
STEARNS = "1265 S Stearns Dr, Los Angeles, CA 90035"  # verified in ext_la.json (AIN 5087016035)
STEARNS_LL = (34.052619, -118.3711303)
PRINCETON = "100 Nassau St, Princeton, NJ 08542"


def _shape(ev):
    assert set(ev) == {"source", "status", "summary", "observed", "images", "detail"}
    assert ev["source"] == "county"
    json.dumps(ev)


def test_geocode_austin():
    g = geocode(AUSTIN)
    assert g and abs(g["lat"] - 29.75) < 0.01 and abs(g["lon"] + 95.37) < 0.01
    assert "AUSTIN" in g["matched_address"].upper()


def test_houston_austin_six_stories():
    ev = county_record(AUSTIN, *AUSTIN_LL, "Houston")
    _shape(ev)
    assert ev["status"] == "ok", ev
    o = ev["observed"]
    assert o["stories"] == 6
    assert o["parcel_id"] == "0022630020001"
    assert o["year_built"] == 2019 and o["unit_count"] == 216
    assert o["source_url"].startswith("https://") and "6 floors" in ev["summary"]


def test_houston_from_geocode_only():
    ev = county_record(AUSTIN, None, None, "Houston")
    assert ev["status"] == "ok" and ev["observed"]["stories"] == 6, ev


def test_la_stearns():
    ev = county_record(STEARNS, *STEARNS_LL, "Los Angeles")
    _shape(ev)
    assert ev["status"] == "ok", ev
    o = ev["observed"]
    assert o["parcel_id"] == "5087016035"
    assert o["year_built"] == 2020 and o["unit_count"] == 48
    assert o.get("stories") == 6  # City of LA Certificate of Occupancy of_stories


def test_nyc_pluto():
    ev = county_record("350 5th Ave, New York, NY 10118", 40.7484514, -73.9857117, "New York")
    _shape(ev)
    assert ev["status"] == "ok", ev
    assert ev["observed"]["stories"] == 102 and ev["observed"]["year_built"] == 1931


def test_princeton_no_evidence():
    for ev in (county_record(PRINCETON, 40.3487, -74.6593, "Princeton"),
               county_record(PRINCETON, None, None, "Princeton")):
        _shape(ev)
        assert ev["status"] == "no_evidence"
    assert ev["summary"] == "No county source wired for this location yet."


def test_second_call_zero_network(monkeypatch):
    county_record(AUSTIN, *AUSTIN_LL, "Houston")
    county_record(STEARNS, *STEARNS_LL, "Los Angeles")
    geocode(AUSTIN)

    def boom(*a, **k):
        raise AssertionError("network call on a cached request")
    monkeypatch.setattr(net, "get", boom)
    monkeypatch.setattr(net, "head_size", boom)
    before = net.calls
    assert county_record(AUSTIN, *AUSTIN_LL, "Houston")["status"] == "ok"
    assert county_record(STEARNS, *STEARNS_LL, "Los Angeles")["status"] == "ok"
    assert geocode(AUSTIN)
    assert net.calls == before


def test_network_failure_is_error_not_raise(monkeypatch):
    def down(*a, **k):
        raise ConnectionError("simulated outage")
    monkeypatch.setattr(net, "get", down)
    ev = county_record("999 Nowhere St, Houston, TX", 29.70123, -95.40123, "Houston")
    _shape(ev)
    assert ev["status"] == "error"
    monkeypatch.undo()
