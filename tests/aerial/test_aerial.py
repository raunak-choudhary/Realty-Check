"""Live (cached) tests for tools.aerial. Skip when RC_PRIVATE_DIR is unset.
Run: RC_PRIVATE_DIR=... .venv/Scripts/python.exe -m pytest tests/aerial -q"""
import json
import os
from pathlib import Path

import pytest

if not os.environ.get("RC_PRIVATE_DIR"):
    pytest.skip("RC_PRIVATE_DIR not set", allow_module_level=True)

from PIL import Image

import rc_common
from tools.aerial import aerial, aerial_images, building_height
from tools.aerial.aerial import stories_from_height

AUSTIN = (29.7460624, -95.3679203)  # 2111 Austin St, Houston (kit 10122224)


def _no_key(obj):
    key = rc_common.secret("VEXCEL_API_KEY")
    assert key not in json.dumps(obj), "API key leaked"  # never print the key


def test_stories_rule():
    assert stories_from_height(23.1) == (6, [6, 7])
    assert stories_from_height(16.2)[0] == 4


def test_height_austin():
    ev = building_height(*AUSTIN)
    assert ev["source"] == "aerial" and ev["status"] == "ok", ev["summary"]
    assert 21 <= ev["observed"]["height_m"] <= 25
    assert ev["observed"]["stories"] == 6
    lo, hi = ev["observed"]["stories_range"]
    assert lo <= 6 <= hi
    _no_key(ev)


def test_images_austin():
    ev = aerial_images(*AUSTIN)
    assert ev["status"] == "ok", ev["summary"]
    cache = rc_common.cache_dir()
    tops = [i for i in ev["images"] if i["caption"].startswith("Top-down")]
    obls = [i for i in ev["images"] if i["caption"].startswith("Angled")]
    assert len(tops) >= 1 and len(obls) >= 1
    for i in ev["images"]:
        p = Path(i["path"])
        assert p.exists() and p.suffix == ".jpg" and cache in p.parents
        assert max(Image.open(p).size) <= 1568
    _no_key(ev)


def test_repeat_calls_are_cached():
    building_height(*AUSTIN)
    aerial_images(*AUSTIN)
    n = aerial.CALLS["n"]
    building_height(*AUSTIN)
    aerial_images(*AUSTIN)
    assert aerial.CALLS["n"] == n


def test_atlantic_no_exception():
    for fn in (building_height, aerial_images):
        ev = fn(0.0, -30.0)
        assert ev["status"] in ("no_evidence", "error")
        assert ev["summary"]
        _no_key(ev)


def test_cached_json_has_no_key():
    key = rc_common.secret("VEXCEL_API_KEY")
    for f in rc_common.cache_dir("aerial").rglob("*.json"):
        assert key not in f.read_text(encoding="utf-8"), f.name
