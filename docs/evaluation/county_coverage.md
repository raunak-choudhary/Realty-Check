# County coverage: where the county layer hits, where it misses, what to fix

Test write-up from the build, with building identities and record values removed.

Measured 2026-11-14. Read-only for the repo. The work used throwaway scripts: TIGERweb county and incorporated-place polygons covering the kit's extent; every kit property assigned to a county and place (point-in-polygon on the kit's own lat/lon); saved runs scanned for floors, year built and unit-count claims; a live sample of 30 Houston and 30 LA kit properties through `county_record`; HCAD bulk-zip members and residential year and story fields; the off-kit path from Census geocoder to parcel; and live checks of candidate endpoints. The live runs wrote to a redirected sandbox, not the real county caches. The scripts and raw results are not published.

Note: `tools/paper` changed on disk while this ran, and `county.py` went back to `CACHE_VERSION = 2`. The judged-field code paths did not change: `hcad.parcel_at`, `hcad.building_facts`, `la.parcel_at`, `la.parcel_facts` and `la.cofo_stories`. The flood lookup was stubbed out in the sample because it does not affect year, floors or units.

## 1. Kit geography

The kit index has no county field. Its `city` field is a market label: every TX row says Houston and every CA row says Los Angeles. County and city were therefore found by point-in-polygon of the kit lat/lon against TIGERweb polygons (State_County layer 1; Places layer 4). Zip codes were used for the few CA rows that have no coordinates.

| Market | Kit total | County | Count | Buildings / homes |
|---|---|---|---|---|
| Houston | several thousand | Harris | nearly all | about half buildings, half homes |
| | | **Fort Bend** | **a handful (under 1%)** | mostly homes |
| LA | a few thousand | Los Angeles | nearly all | mostly buildings |
| | | no lat/lon (zips in LA County) | a few | homes |

- **No kit properties** are in Montgomery, Brazoria, Galveston, Waller, Orange, Ventura, San Bernardino or Riverside. The TIGERweb query over the CA kit extent returned only Los Angeles County.
- **Places, Houston set:** most are in the City of Houston (a few of them in the Fort Bend part of the city); about a fifth are in unincorporated Harris; the rest, a small share, are in unincorporated Fort Bend, Pasadena, Webster, Nassau Bay and other small cities.
- **Places, LA set:** nearly all are in the City of LA; a few dozen are in unincorporated LA County, West Hollywood, Culver City and other cities.
  - The **few dozen LA properties outside the City of LA** can never get a story count, because the CofO source covers the city only.
- **Routing:** all the Fort Bend points fall inside `hcad.BBOX`, so they go to HCAD. HCAD has no Fort Bend parcels, so each one returns "No Harris County parcel at this point".

## 2. Hit rate today

### 2a. Existing caches and saved runs

- **County cache:** 17 results covering only 7 distinct places.
  - 13 are the demo buildings (Houston demo, LA demo, a downtown LA tower, a NYC tower).
  - 3 are misses: one Houston point with no parcel, one Houston residential parcel with no building data, and one Queens point with no lot.
  - These are too few to give a rate.
- **Saved runs:** 54 runs, of which 23 carry county evidence (19 ok, 4 no_evidence). In 31 runs the county lookup was never called.
  - 20 of the 23 runs with county evidence are the same 3 demo addresses.

### 2b. Live sample

- **Method:** `random.Random(42)`, 30 Houston and 30 LA kit properties (any kind), called as the harness calls them: `county_record(address, kit_lat, kit_lon, city)`.
- **Load:** 108 requests in total, at most 2 per second through `net`'s rate limiter, in one process. Median time per property 0.9 s, with no timeouts.

| | year built | floors | unit count |
|---|---|---|---|
| Houston buildings (16, 1 in Fort Bend) | 15/16 | 14/16 | 12/16 (3 misses are F1 offices, where units do not apply) |
| Houston homes (14, 1 in Fort Bend) | **0/14** | **0/14** | **0/14** |
| **Houston all** | **15/30 (50%)** | **14/30 (47%)** | **12/30 (40%)** |
| LA buildings (24) | 23/24 | 4/24 | 21/24 (3 of these look wrong, see below) |
| LA homes (6) | 5/6 | 2/6 | 5/6 |
| **LA all** | **28/30 (93%)** | **6/30 (20%)** | **26/30 (87%)** |

Year built agrees with the kit record (within 1 year) in 27/27 LA cases and 12/14 Houston cases.

### 2c. Miss reasons, with where each one arises in the code

Counts are field-misses out of 90 per city (30 properties × 3 fields).

| # | Reason | Houston | LA | Where it arises |
|---|---|---|---|---|
| 1 | **Residential account not indexed.** A1 single-family homes and Z4 condos: `building_res.txt` is never read | **39** (13 properties × 3) | 0 | `hcad._build_index` reads only `building_other.txt` and the STC/UNT rows of `fixtures.txt`. `building_facts()` then returns {} and `_houston` says "has no building data on the roll" |
| 2 | **No CofO row**, because the assessor publishes no stories and the City of LA CofO data starts in 2005 and covers the city only | 0 | **24** | `county._la` → `la.cofo_stories`. Dataset 3f9m-afei has 125,771 rows from 2005-01-10 onwards, 99,687 of them with `of_stories` |
| 3 | **Point outside Harris County** (Fort Bend), sent to HCAD by the bounding box | 6 (2 properties) | 0 | `hcad.in_area` uses a generous bounding box. `hcad.parcel_at` returns None, and `_houston` says "No Harris County parcel at this point" |
| 4 | **Office (F1) account:** HCAD has no units for it | 3 | 0 | `building_facts`. Not a real miss, because unit claims do not apply to offices |
| 5 | **New construction not yet on the roll** (2025–26 builds: parcel found but YearBuilt and SQFT are empty) | 0 | 4 | `la.parcel_facts`. One Houston saved run (Home B) is the same case: a vacant lot on the roll |
| 6 | **Commercial-use LA parcel**, Units1-5 = 0 | 0 | 2 | `la.parcel_facts` (warehouse, studio). Not a real miss |
| 7 | **HCAD apartment (B1) with no STC fixture** | 1 | 0 | `building_facts` |

**Wrong rather than missing.** 3 of the 24 LA buildings return unit_count = 1 for buildings of over 30k sq ft. Two of the parcels are "Single" with situs house number 0 and under 1,500 sq ft, so the 40 m fallback picked a sliver or condo lot. The third parcel is a 5+ unit building where Units1 = 1. This is the multi-parcel or condo complex problem: the code takes one AIN and never sums sibling parcels.

**Geocoder misses.** These are rare for kit properties, because the harness passes the kit's own lat/lon. `run.py:do_match` geocodes only when the match has no coordinates, so "fall back to the kit lat/lon" **is already done**. For listings outside the kit, the Census geocoder path was tested on the same 60 addresses:
- The geocoder found **58/60**.
- Its point sits a median **42 m** from the kit point, and more than 40 m away in 31/60 cases.
- `parcel_at` from the geocoded point found **no parcel in 9/29 Houston and 7/29 LA cases (28%)**, and a different parcel in 1 more.
- The cause is that the point lands in the street, beyond the 40 m house-number search.
- An HCAD attribute query on `site_str_num` and `site_str_name` found the parcel for one saved-run miss (Home A).

## 3. Weakest judged field per county, and why

- **Harris County, floors and year for homes (about half of the Houston kit set; 0% hit today).**
  - The HCAD index is built from `building_other.txt`, which covers commercial and apartment accounts only: 70,663 accounts, of which 10,524 have STC stories and 11,807 have units.
  - Year built for homes is in `building_res.txt`: 1,286,508 accounts, 1,286,503 with `date_erected`.
  - Floors for homes are the **`STY` "Story Height Index"** rows in `fixtures.txt`: 1,285,889 accounts with values 1.00 (813k), 2.00 (462k), 3.00 (33k), 1.50 (4k). The index build already streams `fixtures.txt` but keeps only STC and UNT.
  - Tested on the 13 residential misses, these files give **year 13/13** (12/13 equal to the kit) and **STY 13/13**.
  - For Z4 condos, STY is the unit's own story count, not the building's.
  - For apartment buildings Harris is strong: year 15/15, floors 14/15, units 12/12.
- **LA County, floors (20%).**
  - The assessor layer has no story field at all. Floors come only from City of LA Certificates of Occupancy issued since 2005, so pre-2005 buildings (most of the stock) and the non-City properties never get floors.
  - Year (93%) and units (87%) come from the assessor `YearBuilt1` and the sum of `Units1-5`. Units are fragile for condo and multi-parcel complexes.
  - In the judge, floors are decided first by the Vexcel roof height (aerial ranks above county), so the LA floors gap costs a verdict only when Vexcel has no measurement.

## 4. Fixes, ranked by properties gained ÷ effort

| Rank | Fix | Kit properties gained | Effort | Gain / h |
|---|---|---|---|---|
| **1** | **HCAD residential index.** Read `building_res.txt` (`date_erected` of the largest building → year_built) and keep the `STY` rows of `fixtures.txt` (max → stories, only for A1/A2/B2–B4, not Z condos). Set unit_count from the state class (A1 = 1, B2 = 2, B3 = 3, B4 = 4). Rebuild `index_2026.json` once: about 1.29M more accounts, which makes the index larger, so store compact `[year, sty]` pairs. | **Nearly all** Harris kit homes (about half the Houston set) gain year and floors (sample 13/13). Houston year goes from about 50% to about 97% | 2 h, plus 10–15 min of one-time streaming (73 MB + 28 MB compressed, already proved by a probe) | **highest** |
| **2** | **Address-attribute fallback when the point hits no parcel.** HCAD: `where site_str_num=N AND site_str_name LIKE 'NAME%'` (plus `site_zip`). LA: `SitusHouseNo='N' AND SitusStreet LIKE '%NAME%'`. Run it only when `parcel_at` returns None | Kit: about 0, because the kit has lat/lon. **Off-kit listings in Harris and LA: about 28% more parcels found** (16/58 sample). Fixes the Home A saved run when combined with fix 1 | 1 h | high for off-kit listings |
| **3** | **Route Fort Bend to FBCAD.** Endpoint `https://gisweb.fbcad.org/arcgis/rest/services/Hosted/FBCADPublicData/FeatureServer/0/query` (point query). Live: it answered with a `yearbuilt` equal to the kit and `totsqftlvg` for a Fort Bend home; a new 2025 building returned a null year. **No stories or units fields.** Tighten `hcad.in_area` or check FBCAD first for Fort Bend points | **A handful of kit properties** (under 1%), year only. Also covers the Sugar Land, Missouri City and Katy area for off-kit listings | 1 h | low |
| 4 | **LA multi-parcel / condo merge.** When the hit parcel is "Single" with house number 0, or has Units = 1 and 5+ units in use, sum units and pick the year over all parcels within 40 m that share the situs street, or prefer the largest SQFTmain | About 10% of LA buildings (3/24 in the sample) get a correct unit count instead of 1 | 2 h | medium |
| 5 | **LA floors from LARIAC 2014 building heights.** Endpoint `https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/Countywide_Building_Outlines/FeatureServer/1`, field `HEIGHT` in feet. Live on 12 buildings with the same formula as the aerial check: 4/12 exact, 10/12 within ±1. It is an estimate and duplicates the Vexcel aerial, which already outranks county | Most LA kit properties get a rough floors estimate; little verdict gain | 1.5 h | low (quality) |
| 6 | TxGIO StratMap statewide parcels, `https://feature.geographic.texas.gov/arcgis/rest/services/Parcels/stratmap_land_parcels_48_most_recent/MapServer/identify` (`/query` is refused). Has `YEAR_BUILT`, filled for Harris (checked on a sampled home) but **null for Fort Bend and Travis** | 0 kit gain beyond fix 1 | 1 h | ≈0 for the kit |

**Nationwide, outside the kit.** No free source gives authoritative year built, floors and units per building by point.
- **USACE NSI** (`https://nsi.sec.usace.army.mil/nsiapi/structures?bbox=...`) answers keyless, but its values are modelled. For a Houston house its `med_yr_blt` was the census-block median, more than 20 years off the county's year. `num_story` was right, and `occtype` RES3x implies multi-family. Use it only as a labelled estimate, never as a record.
- OSM `building:levels` and `start_date` are sparse.
- Regrid and ATTOM are paid.
- Statewide parcel layers with year built exist (Texas StratMap, above) but are filled per county, unevenly.

## 5. Saved runs: judged claims that ended "can't check"

- **Scope:** 54 runs. The 23 runs with a floors, year-built or unit-count claim hold 48 such claims: 17 floors, 18 year, 13 units.
- **Can't check:** 2 floors claims and 6 year claims, none for units.
- **Because the county had nothing: 6 claims (2 floors, 4 year) in 4 runs:**
  - LA listing: the Census geocoder could not place the address. It is also absent from the LA parcel layer by address.
  - Houston, Home B (new 2025 build): the parcel is a vacant lot on the roll. Floors and year are both can't-check. No fix applies.
  - Houston, Home A: no parcel at the geocoded point, so year is can't-check (floors was decided by the aerial). It is an A1 home, so **fixes 2 and 1 together would have answered it**.
  - Queens: no NYC lot found, so year is can't-check.
- **The other 2 year claims** (one LA building, 2 runs) were treated as marketing phrases. The county was never called.
- Every unit-count claim was decided by the county: 9 confirmed, 3 close, 1 contradicted.
