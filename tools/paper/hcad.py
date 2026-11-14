"""Harris County (Houston): HCAD parcel point query -> HCAD certified bulk roll (building data per account).

The live parcel layer has no building fields, so the building facts come from HCAD's public bulk
download Real_building_land.zip. Only two members are read (fixtures.txt ~28 MB and
building_other.txt ~7 MB compressed) with HTTP Range requests, once; the result is a small
per-account index cached under rc_cache/paper/hcad/.
"""
from __future__ import annotations

import datetime
import json
import struct
import threading
import zlib

from rc_common import cache_dir

from . import net

PARCELS = "https://www.gis.hctx.net/arcgis/rest/services/HCAD/Parcels/MapServer/0/query"
ZIP_URL = "https://download.hcad.org/data/CAMA/{year}/Real_building_land.zip"
BBOX = (29.45, 30.20, -96.00, -94.85)  # lat_min, lat_max, lon_min, lon_max (Harris County, generous)
_lock = threading.Lock()


def in_area(lat: float, lon: float) -> bool:
    return BBOX[0] <= lat <= BBOX[1] and BBOX[2] <= lon <= BBOX[3]


def parcel_at(lat: float, lon: float, house_no: str = "") -> tuple[dict | None, str]:
    """Return (parcel attributes or None, query URL). Owner fields are never requested.
    If the point misses a parcel or hits one with another house number (geocoded points often sit
    on the street), take a parcel within 40 m that has the listing's house number."""
    params = {"geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint", "inSR": 4326,
              "spatialRel": "esriSpatialRelIntersects", "returnGeometry": "false", "f": "json",
              "outFields": "HCAD_NUM,acct_num,site_str_num,site_str_name,site_str_sfx,site_zip,"
                           "state_class,tax_year"}
    url, d = net.get_json_url(PARCELS, params)
    hit = [f["attributes"] for f in d.get("features", [])]
    if hit and (not house_no or str(hit[0].get("site_str_num") or "").strip() == house_no):
        return hit[0], url
    if house_no:
        url2, d = net.get_json_url(PARCELS, {**params, "distance": 40, "units": "esriSRUnit_Meter"})
        same = [f["attributes"] for f in d.get("features", [])
                if str(f["attributes"].get("site_str_num") or "").strip() == house_no]
        if same:
            return same[0], url2
    return (hit[0] if hit else None), url


# ---------- bulk roll index ----------

def _zip_members(url: str) -> dict[str, tuple[int, int]]:
    """name -> (local header offset, compressed size), read from the zip's central directory."""
    size = net.head_size(url)
    tail = net.get(url, headers={"Range": f"bytes={max(0, size - 65536)}-{size - 1}"}).content
    e = tail.rfind(b"PK\x05\x06")
    cd_size, cd_off = struct.unpack("<II", tail[e + 12:e + 20])
    cd = net.get(url, headers={"Range": f"bytes={cd_off}-{cd_off + cd_size - 1}"}).content
    out, p = {}, 0
    while cd[p:p + 4] == b"PK\x01\x02":
        csize = struct.unpack("<I", cd[p + 20:p + 24])[0]
        n, m, k = struct.unpack("<HHH", cd[p + 28:p + 34])
        off = struct.unpack("<I", cd[p + 42:p + 46])[0]
        out[cd[p + 46:p + 46 + n].decode()] = (off, csize)
        p += 46 + n + m + k
    return out


def _member_lines(url: str, off: int, csize: int):
    """Stream one deflated zip member over HTTP Range and yield its text lines."""
    lh = net.get(url, headers={"Range": f"bytes={off}-{off + 29}"}).content
    n, m = struct.unpack("<HH", lh[26:30])
    start = off + 30 + n + m
    r = net.get(url, headers={"Range": f"bytes={start}-{start + csize - 1}"}, stream=True)
    dec, buf = zlib.decompressobj(-15), b""
    for chunk in r.iter_content(1 << 20):
        buf += dec.decompress(chunk)
        lines = buf.split(b"\n")
        buf = lines.pop()
        for line in lines:
            yield line.decode("latin-1").rstrip("\r")
    buf += dec.flush()
    if buf:
        yield buf.decode("latin-1").rstrip("\r")


def _num(s: str) -> float:
    try:
        return float(s.strip() or 0)
    except ValueError:
        return 0.0


def _build_index(url: str) -> dict:
    members = _zip_members(url)
    idx: dict[str, dict] = {}
    # building_other.txt: commercial / apartment buildings, one row per building
    rows = _member_lines(url, *members["building_other.txt"])
    cols = next(rows).split("\t")
    a, b, de, sf, un = (cols.index(c) for c in ("acct", "bld_num", "date_erected", "im_sq_ft", "units"))
    for line in rows:
        f = line.split("\t")
        if len(f) <= max(a, b, de, sf, un):
            continue
        r = idx.setdefault(f[a].strip(), {})
        r.setdefault("blds", []).append([int(_num(f[de])), int(_num(f[sf])), int(_num(f[un]))])
    # fixtures.txt: per-building fixture rows; STC = '# Stories', UNT = units
    rows = _member_lines(url, *members["fixtures.txt"])
    cols = next(rows).split("\t")
    a, b, t, u = (cols.index(c) for c in ("acct", "bld_num", "type", "units"))
    for line in rows:
        f = line.split("\t")
        if len(f) <= max(a, b, t, u):
            continue
        typ = f[t].strip()
        if typ in ("STC", "UNT"):
            r = idx.setdefault(f[a].strip(), {})
            r.setdefault(typ, {})[f[b].strip()] = _num(f[u])
    return idx


def _index() -> tuple[dict, str]:
    """Load (or build once) the per-account index for the newest published roll year."""
    with _lock:
        d = cache_dir("paper", "hcad")
        this_year = datetime.date.today().year
        for year in (this_year, this_year - 1):
            p = d / f"index_{year}.json"
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8")), ZIP_URL.format(year=year)
        last = None
        for year in (this_year, this_year - 1):
            url = ZIP_URL.format(year=year)
            try:
                idx = _build_index(url)
            except Exception as e:  # year not published yet -> try previous
                last = e
                continue
            p = d / f"index_{year}.json"
            p.write_text(json.dumps(idx, separators=(",", ":")), encoding="utf-8")
            return idx, url
        raise RuntimeError(f"HCAD bulk roll unavailable: {last}")


def building_facts(acct: str) -> tuple[dict, str]:
    """Return (observed facts for this account, bulk zip URL). Only fields HCAD publishes."""
    idx, url = _index()
    r = idx.get(acct.strip()) or {}
    obs: dict = {}
    if r.get("STC"):
        obs["stories"] = int(max(r["STC"].values()))
    blds = r.get("blds") or []
    if blds:
        main = max(blds, key=lambda x: x[1])
        if main[0] > 1800:
            obs["year_built"] = main[0]
        sf = sum(x[1] for x in blds)
        if sf > 0:
            obs["building_sf"] = sf
        units = max(x[2] for x in blds)  # building_other.units is per account, repeated per row
        if units > 0:
            obs["unit_count"] = units
    if "unit_count" not in obs and r.get("UNT"):
        n = int(sum(r["UNT"].values()))
        if n > 0:
            obs["unit_count"] = n
    return obs, url
