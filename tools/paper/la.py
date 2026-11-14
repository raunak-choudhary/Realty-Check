"""Los Angeles County: assessor parcel point query (year built, units, main sq ft per building line),
plus City of LA Certificate of Occupancy rows for the number of stories (the assessor has none)."""
from __future__ import annotations

import re

from . import net

PARCELS = "https://public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/0/query"
COFO = "https://data.lacity.org/resource/3f9m-afei.json"
BBOX = (33.65, 34.85, -118.95, -117.60)  # lat_min, lat_max, lon_min, lon_max (LA County, generous)
_FIELDS = ["AIN", "SitusFullAddress", "SitusHouseNo", "SitusStreet", "SitusCity", "UseDescription",
           "Roll_Year"] + [f"{k}{i}" for i in range(1, 6) for k in ("YearBuilt", "Units", "SQFTmain")]


def in_area(lat: float, lon: float) -> bool:
    return BBOX[0] <= lat <= BBOX[1] and BBOX[2] <= lon <= BBOX[3]


def parcel_at(lat: float, lon: float, house_no: str = "") -> tuple[dict | None, str]:
    """Parcel containing the point, when it carries the listing's house number and a building.
    Otherwise look within 40 m for a parcel with the listing's house number, or with the same
    situs address as the hit (a building on a split or corner lot is often a sibling parcel)."""
    base = {"geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint", "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects", "outFields": ",".join(_FIELDS),
            "returnGeometry": "false", "f": "json"}
    url, d = net.get_json_url(PARCELS, base)
    hit = [f["attributes"] for f in d.get("features", [])]
    if hit and hit[0].get("SQFTmain1") and (not house_no or _no(hit[0]) == house_no):
        return hit[0], url
    url2, d = net.get_json_url(PARCELS, {**base, "distance": 40, "units": "esriSRUnit_Meter"})
    near = [f["attributes"] for f in d.get("features", []) if f["attributes"].get("SQFTmain1")]
    for keep in (lambda a: house_no and _no(a) == house_no,
                 lambda a: hit and a.get("SitusFullAddress") == hit[0].get("SitusFullAddress")):
        same = [a for a in near if keep(a)]
        if same:
            return max(same, key=lambda a: a.get("SQFTmain1") or 0), url2
    if hit:
        return hit[0], url
    return None, url2


def _no(a: dict) -> str:
    return str(a.get("SitusHouseNo") or "").strip()


def parcel_facts(p: dict) -> dict:
    obs: dict = {}
    years = [p.get(f"YearBuilt{i}") for i in range(1, 6)]
    years = [int(y) for y in years if y and str(y).strip().isdigit() and int(y) > 1800]
    if years:
        obs["year_built"] = years[0]
    units = sum(int(p.get(f"Units{i}") or 0) for i in range(1, 6))
    if units > 0:
        obs["unit_count"] = units
    sf = sum(int(p.get(f"SQFTmain{i}") or 0) for i in range(1, 6))
    if sf > 0:
        obs["building_sf"] = sf
    return obs


def cofo_stories(house_no: str, street: str) -> tuple[dict | None, str]:
    """Latest City of LA Certificate of Occupancy with a story count at this address (city only).
    Only non-personal columns are selected."""
    num = (house_no or "").strip()
    name = re.sub(r"^(N|S|E|W)\s+", "", (street or "").strip().upper()).split(" ")[0] if street else ""
    if not num.isdigit() or not name:
        return None, ""
    params = {"$select": "cofo_number,cofo_issue_date,pcis_permit,permit_sub_type,of_stories,"
                         "of_residential_dwelling_units,address_start,street_name",
              "$where": f"address_start='{num}' and street_name like '%{name}%'",
              "$order": "cofo_issue_date DESC", "$limit": 10}
    url, rows = net.get_json_url(COFO, params)
    rows = [r for r in rows if r.get("of_stories")]
    return (rows[0] if rows else None), url
