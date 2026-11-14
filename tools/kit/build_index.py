"""Read the CoStar kit zip once and write a compact property index under cache_dir("kit").

Run: python -m tools.kit.build_index
"""
from __future__ import annotations

import io
import json
from pathlib import Path

import rc_common
from tools.kit.normalize import zip5

INDEX_NAME = "index.json"
INDEX_VERSION = 2
MATTERPORT_TYPES = (36, 234)  # ExternalReferenceType: MatterportScan, MatterportStreamingKey
CONSTRUCTION_COMPLETE = 2     # ConstructionEventType


def index_path() -> Path:
    return rc_common.cache_dir("kit") / INDEX_NAME


def kit_zip_path() -> Path:
    try:
        p = Path(rc_common.secret("COSTAR_KIT_ZIP"))
        if not p.is_absolute():
            p = rc_common.private_dir() / p
        if p.exists():
            return p
    except RuntimeError:
        pass
    p = rc_common.private_dir() / "resources" / "costar" / "costar-hackathon-kit.zip"
    if not p.exists():
        raise RuntimeError("CoStar kit zip not found (set COSTAR_KIT_ZIP in the private .env)")
    return p


def _rows(z, name: str):
    with z.open(name) as f:
        for line in io.TextIOWrapper(f, encoding="utf-8"):
            if line.strip():
                yield json.loads(line)


def _mp_keys(attachments, field: str = "videoExternalReferenceType") -> list[str]:
    out = []
    for a in attachments or []:
        k = a.get("videoKey")
        if a.get(field) in MATTERPORT_TYPES and k and k not in out:
            out.append(k)
    return out


def _num(v):
    return None if v is None else int(v) if float(v).is_integer() else float(v)


def _clean_name(s):
    return " ".join(str(s).split()) if s else None


def _addr_key(a: dict, zip_field: str) -> dict:
    """Address parts used for matching (street name stays raw; the matcher normalizes it at load)."""
    def n(x):
        try:
            return int(str(x).strip())
        except (TypeError, ValueError):
            return None
    lo = n(a.get("streetNumber"))
    hi = n(a.get("streetNumberEndRange")) or lo
    if lo is not None and hi is not None and hi < lo:
        lo, hi = hi, lo
    return {"num_lo": lo, "num_hi": hi, "street_name": a.get("streetName") or "",
            "zip": zip5(a.get(zip_field)), "city": (a.get("city") or "").strip().lower(),
            "lat": a.get("latitude"), "lon": a.get("longitude")}


def _display(a: dict, zip_field: str) -> str:
    street = " ".join(str(x) for x in (a.get("streetNumber"), a.get("streetDirection") or a.get("streetDirPrefix"),
                                        a.get("streetName"), a.get("streetType"),
                                        a.get("streetSuffix") or a.get("streetDirSuffix")) if x)
    z = zip5(a.get(zip_field)) or ""
    return f"{street}, {a.get('city') or ''}, {a.get('state') or ''} {z}".strip()


def _building(r: dict, listing: dict | None) -> dict:
    pa = r.get("primaryAddress") or {}
    apt = r.get("propertyApartment") or {}
    year = next((e.get("year") for e in r.get("constructionEvents") or []
                 if e.get("eventType") == CONSTRUCTION_COMPLETE and e.get("year")), None)
    if year is None and listing:
        year = listing.get("yearBuilt")
    units = apt.get("totalNumUnits")
    if units is None and listing:
        units = listing.get("totalNumUnits")
    floorplans, seen = [], set()
    mp_all = _mp_keys(r.get("attachments"))
    for m in apt.get("models") or []:
        keys = _mp_keys(m.get("attachments"))
        for u in m.get("units") or []:
            keys += [k for k in _mp_keys(u.get("attachments")) if k not in keys]
        mp_all += [k for k in keys if k not in mp_all]
        seen.add(m.get("id"))
        floorplans.append({"name": _clean_name(m.get("modelName")), "beds": _num(m.get("numBeds")),
                           "baths": _num(m.get("numBaths")), "sqft": _num(m.get("minSquareFeet")),
                           "matterport_model_id": keys[0] if keys else None})
    for u in apt.get("units") or []:
        mp_all += [k for k in _mp_keys(u.get("attachments")) if k not in mp_all]
    for m in (listing or {}).get("apartmentModels") or []:
        if m.get("id") not in seen:
            floorplans.append({"name": _clean_name(m.get("name")), "beds": _num(m.get("numBeds")),
                               "baths": _num(m.get("numBaths")), "sqft": _num(m.get("minSquareFeet")),
                               "matterport_model_id": None})
    addrs = [pa] + [a for a in r.get("addresses") or [] if a.get("id") != pa.get("id")]
    return {"property_id": str(r["id"]), "kind": "building",
            "name": r.get("buildingName") or (listing or {}).get("buildingName"),
            "address": _display(pa, "postcode"), "city": pa.get("city"), "state": pa.get("state"),
            "lat": pa.get("latitude"), "lon": pa.get("longitude"),
            "keys": [_addr_key(a, "postcode") for a in addrs],
            "record": {"stories": r.get("numStoriesAboveGrade"), "year_built": year, "unit_count": units,
                       "building_sf": _num(r.get("grossBuildingAreaSquareFeet"))},
            "floorplans": floorplans, "matterport_model_ids": mp_all}


def _home(r: dict) -> dict:
    p = r.get("property") or {}
    a = p.get("address") or {}
    keys = _mp_keys(r.get("media"), "externalReferenceType")
    unit = a.get("unitNumber")
    return {"property_id": str(r["id"]), "kind": "home", "name": a.get("buildingName"),
            "address": _display(a, "zip") + (f" (unit {unit})" if unit else ""), "unit": unit,
            "city": a.get("city"), "state": a.get("state"), "lat": a.get("latitude"), "lon": a.get("longitude"),
            "keys": [_addr_key(a, "zip")],
            "record": {"stories": None, "year_built": p.get("yearBuilt"), "unit_count": None, "building_sf": None},
            "floorplans": [{"name": f"Unit {unit}" if unit else "Home", "beds": _num(p.get("bedsMax")),
                            "baths": _num(p.get("bathsMax")), "sqft": _num(p.get("sqftMin")),
                            "matterport_model_id": keys[0] if keys else None}],
            "matterport_model_ids": keys}


def build() -> dict:
    import pyzipper
    z = pyzipper.AESZipFile(kit_zip_path())
    z.setpassword(rc_common.secret("COSTAR_ZIP_PASSWORD").encode())
    listings = {r["propertyId"]: r for r in _rows(z, "data/apartment-listing.jsonl")}
    props = [_building(r, listings.get(r["id"])) for r in _rows(z, "data/commercial-property.jsonl")]
    props += [_home(r) for r in _rows(z, "data/residential-listings.jsonl")]
    return {"version": INDEX_VERSION, "properties": props}


def write_index() -> Path:
    path = index_path()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(build(), separators=(",", ":")), encoding="utf-8")
    tmp.replace(path)
    return path


def main() -> None:
    path = write_index()
    props = json.loads(path.read_text(encoding="utf-8"))["properties"]
    b = [p for p in props if p["kind"] == "building"]
    print(f"wrote {len(props)} properties ({len(b)} buildings, {len(props) - len(b)} homes)")
    print("buildings with stories:", sum(p["record"]["stories"] is not None for p in b),
          "| with floorplans:", sum(bool(p["floorplans"]) for p in b),
          "| with Matterport ids:", sum(bool(p["matterport_model_ids"]) for p in b),
          "| floorplans with Matterport id:", sum(f["matterport_model_id"] is not None for p in b for f in p["floorplans"]))
    print("homes with Matterport ids:", sum(bool(p["matterport_model_ids"]) for p in props if p["kind"] == "home"))


if __name__ == "__main__":
    main()
