# County ("paper") layer: what it is and how to enrich it

Test write-up from the build, with building identities and record values removed.

Checked 2026-11-14 against the code (`tools/paper/*`, `harness/fill_in.py`, `harness/graph/judge.py`, `server/claim_field.py`), the county cache and a small number of keyless test calls.

## 1. What it is today

There is one entry point, `tools/paper/county.py: county_record(address, lat, lon)`. When the kit gives no coordinates, the address is placed on the map with the **US Census geocoder** (live, keyless). A bounding box then sends the point to one of three sources. Anything outside those boxes returns `no_evidence` with the message "No county source wired for this location yet."

| Area | Source | Access | Fields it reads | Fields that reach `observed` |
|---|---|---|---|---|
| Houston / Harris County | HCAD Parcels MapServer (`gis.hctx.net`) | live, keyless, point query (falls back to parcels within 40 m that share the house number) | HCAD_NUM, site address, state_class, tax_year | parcel_id, parcel_address (state_class appears only in `detail` text) |
| | HCAD certified bulk roll `Real_building_land.zip` | bulk file, read once by HTTP Range and indexed into a local `index_2026.json` (4.5 MB) | `building_other.txt` (date_erected, im_sq_ft, units) and `fixtures.txt` (STC = stories, UNT = units) | stories, year_built, building_sf, unit_count |
| Los Angeles County | LA County Assessor parcel MapServer (`public.gis.lacounty.gov`) | live, keyless, point query plus 40 m fallback | AIN, situs, UseDescription, Roll_Year, YearBuilt1-5, Units1-5, SQFTmain1-5 | year_built, unit_count, building_sf, parcel_id (UseDescription appears only in `detail`) |
| | City of LA Certificates of Occupancy (Socrata `3f9m-afei`) | live, keyless, by address | of_stories, CofO number and date, permit, dwelling units | stories only (City of LA only) |
| New York City | NYC PLUTO (Socrata `64uk-42ks`) | live, keyless, lat/lon box | numfloors, yearbuilt, unitsres, bldgarea | stories, year_built, unit_count, building_sf |
| Houston 311 | `tools/paper/h311.py` (new) | yearly ~270 MB city extract, indexed offline into counts per spot | case type and location only | **not wired**: `county.py` does not call it, and its index does not exist yet |

**Where the fields end up**
- **Judge** (`judge.py`): county evidence can confirm or contradict only **stories, year_built and unit_count**, at rank 1 (below scan and aerial, above the building record). building_sf decides no claim.
- **Fill me in** (`_records`): Year built, Floors and Homes (each only when the page does not say it), Building size, County parcel number, and 311 / complaint counts (keys matching `311|complaint`; none are produced today).
- **Report grid** (`claim_field.source_rows`): year, size, homes, floors, "Published by". It is also ready for land use (key matching `land_use`), owner type (an `owner*` key, shown only as "A company" / "An individual") and counts (`311|complaint|request|violation|incident`). **No county tool emits land use, owner type or counts today**, so those rows are always empty (`docs/DECISIONS.md` says the same).

**Coverage seen in the cache** (8 county results):
- Houston apartment complex: ok (floors, units and year built all found).
- LA: ok (floors from the CofO, units and year built found).
- NYC tower: ok.
- One Houston residential parcel: no building data. Residential accounts are not indexed because `building_res.txt` is never read.
- One Houston point missed every parcel.
- One Queens point found no lot.
- The Princeton, NJ geocode routes nowhere.

Every other city and county returns nothing.

## 2. Gaps

**HCAD live layer**: carries `land_use`, `state_class` (e.g. B2 = multifamily), `Acreage` / `land_sqft` (lot size), `nra` (net rentable area), `CONDO_FLAG`, `new_owner_date` (last sale), market / appraised values, and `owner_name_1` (could become owner type "company"/"individual" only, with the name never stored). None of these are requested except state_class, which never reaches `observed`.

**HCAD bulk roll**: `building_res.txt` (single-family homes and condos) is skipped, so those accounts get "no building data".

**LA parcel layer**: carries `UseType` / `UseDescription` (land use), **`EffectiveYear1-5`** (effective year, a renovation signal), `Bedrooms1-5` / `Bathrooms1-5`, `QualityClass`, `Roll_ImpBaseYear`, `Roll_HomeOwnersExemp`, and lot area from the shape. Only year built, units and sq ft are used. UseDescription goes into `detail` only.

**LA CofO**: `of_residential_dwelling_units` is in `detail` only. Its unit count is never used.

**NYC PLUTO**: `landuse`, `bldgclass`, `ownertype`, `lotarea`, `yearalter1/2` (alteration years) are not selected.

**Houston 311**: the module is written but its index has not been built and nothing calls it.

**Cities**: everything outside Harris County, LA County and NYC returns nothing (the rest of Texas, the SF Bay Area, Chicago and so on). There is no national fallback layer.

## 3. Enrichment options (free, keyless unless noted, checked live 2026-11-14)

| # | Option | What it powers for a renter | Access | Key | Effort | Risk |
|---|---|---|---|---|---|---|
| A | Pass through fields we already fetch or that sit on the same layers: land use (HCAD `land_use`/`state_class`, LA `UseDescription`, PLUTO `landuse`), owner type (HCAD `owner_name_1`, PLUTO `ownertype`, reduced to company/individual in code), lot size, LA `EffectiveYear` and PLUTO `yearalter` ("last major update") | Fills the existing empty grid rows (land use, owner) plus a "Renovated / effective year" fact that checks "newly renovated" | same live endpoints, just more `outFields` / `$select` | n | S (about 1 h) | Low. Owner names must never be cached: compute the type, then drop the name before `evidence()` is written to `paper/county` |
| B | FEMA NFHL flood zone by point (`hazards.fema.gov/.../NFHL/MapServer/28/query`) | New "Flood zone" fact: e.g. "Zone AE, high-risk flood area" vs "X, minimal". Works in every US city the geocoder places, so it gives coverage beyond the three counties. Test: Houston downtown returned X, SFHA false | ArcGIS point query | n | S (1-2 h) | Low. Some counties are unmapped (return "no data"). The service can be slow, so keep the 15 s timeout |
| C | LA City building permits (Socrata `pi9x-tg5x`, `within_circle` or APN) | "Permits since 2020: N, latest <type> in <year>". Checks "renovated", "new kitchens" and similar claims | SODA | n (token optional) | M (2-3 h) | Medium. Only covers 2020 onward. `work_desc` is free text, so show only type, date and count |
| D | LA code enforcement cases (open `u82d-eh7z`, closed `rken-a55j`) | "Open code cases: N" (count only), which feeds the existing `violation` count row | SODA, address match only (no lat/lon or APN) | n | M | Medium. Address-string matching is fragile. Case-type codes are undocumented |
| E | Houston 311 counts (`tools/paper/h311.py`) | "311 requests within 100 m this year: N" (existing `county-311` row) | one ~270 MB offline download, then a local index | n | S to wire, M including the build | Medium. It is a bulk download, which is outside this research task's rules, so the owner has to run it. Counts near a big complex include street issues |
| F | Houston code violations (CKAN `1446a3ec-...`, has an `HCAD` field) | Violation count per account | CKAN datastore | n | S/M | **Stale (last updated 2023-06)**. Low value |
| G | EPA Walkability Index (`geodata.epa.gov/.../WalkabilityIndex/MapServer/0`) | Checks "walkable" claims; "Walkability N / 20" | ArcGIS point | n | S (1 h) | Low, but the data is from 2019/2020 |
| H | FAA airports near point (`services6.arcgis.com/.../US_Airport/FeatureServer/0`) | "Nearest airport N km" as a noise proxy | ArcGIS point + distance | n | S | Low value. It is a proxy, not real noise |
| I | BTS transportation noise map | dB level at the address | MapServer raster | n | L | **High**: identify returns errors, so the only routes are reading pixel colours or a big GeoTIFF |
| J | Census ACS tract median rent (B25064) | "Typical rent in this tract $X" next to the asking rent | api.census.gov | **y (key now enforced, keyless calls are redirected)** | S | Breaks the "no key" rule. Skip, or ship a pre-baked table for 2-3 counties |
| K | LA RSO (rent stabilisation) status | "Rent-stabilised: likely" | no public API (LAHD page blocks bots, ZIMAS backend undocumented) | n/a | - | Rule-based fallback only: City of LA + built on or before 1978-10-01 + 2 or more units means "likely covered by RSO, confirm with LAHD". That is S effort using the year we already have, but mark it "likely" |
| L | Houston permits and Houston certificates of occupancy | none practical | Permits exist only as weekly XLSX files; no open CofO data | - | L | Skip |

## 4. Top 3 by renter value per hour

1. **FEMA flood zone (B).** About 1-2 h. It is a high-value renter fact (insurance, flooding in Houston), works nationwide by point, needs no key, and keeps the county layer useful outside the three counties.
2. **Surface the fields already on the layers we query (A), plus the LA RSO "likely" rule (K-lite).** About 1-2 h. No new endpoints. It fills the land-use and owner-type rows that are already built and always empty, adds lot size and "effective / renovated year" (checks "newly renovated"), and gives LA renters a rent-stabilisation hint.
3. **Wire Houston 311 counts (E)** once its owner has built the index. Otherwise **LA permits since 2020 (C)**. 311 is about 1 h to call from `_houston()` with a key like `requests_311` (the fill-in and grid rows exist already). Permits is about 2-3 h and checks renovation claims in LA.
