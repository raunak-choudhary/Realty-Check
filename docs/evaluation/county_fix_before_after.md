# Houston county coverage after the HCAD residential index and address fallback

Test write-up from the build, with building identities and record values removed.

Measured 2026-11-14. This follows up `county_coverage.md` (fixes 1 and 2 for Harris County). The live sample is the same draw as the coverage study (`random.Random(42)`, the same 30 Houston kit properties), called through `county.county_record`. Pass 1 gives the kit lat/lon. Pass 2 gives no lat/lon, so the Census geocoder is used. The final run used `RC_NO_CACHE=1`, with the caches redirected to a sandbox. The scripts and raw results are not published.

## Code change

- **`tools/paper/hcad.py`, `INDEX_VERSION = 2`.**
  - The index build now also streams `building_res.txt`. For each account it keeps the main (largest `im_sq_ft`) building's `date_erected` and property use code.
  - It keeps the `fixtures.txt` STY ("Story Height Index") rows that were discarded before: the STY of the main building, or the account maximum if that building has none.
  - The residential data goes to `res_2026.bin`, a sorted fixed-width file (13 bytes per account) searched in place, so nothing is loaded.
  - Unit count is set only where the building type fixes it: A1 = 1, B2 = 2, B3 = 3, B4 = 4.
  - Floors are given only for A1, A2, B2–B4 and E1. For condo units (Z*, A4), STY is the unit's own count, not the building's, so condos get **year built only**.
- **`tools/paper/county.py`, `CACHE_VERSION = 3`.** This bump also covers the LA `parcel_facts` change.
  - New Houston address fallback, used when the point finds no parcel or a parcel with another house number. It queries the HCAD parcel layer by house number and street. It accepts a parcel only when exactly one account matches number + street (+ zip when both sides have one) and lies within 1 km of the point (250 m if the point did hit another parcel). Several accounts → rejected, never guessed.
  - Evidence from the fallback carries `parcel_match: "address"`, "Parcel matched by address." in the summary, and the address query in the detail.
- **Build:** 78 s, 9 requests. The old index was backed up beside it before replacing. Nothing was deleted.

| | Before | After |
|---|---|---|
| Files | `index_2026.json` 4.55 MB | `index_2026.json` 4.55 MB + `res_2026.bin` 16.7 MB |
| Cold `_index()` load | 0.31 s (JSON parse) | 0.28 s (JSON parse; the residential file is not loaded) |
| One residential lookup | n/a | about 2 ms cold, under 1 ms warm |

The 13 residential accounts from the study's probe give the same year and STY as the probe did: 13/13 years, 11/11 A1 floors. The 2 Z4 condos get year only.

## Live sample: 30 Houston kit properties, kit lat/lon (the harness path)

| | year built | floors | unit count |
|---|---|---|---|
| Houston buildings (16), before | 15/16 | 14/16 | 12/16 |
| Houston buildings (16), after | 15/16 | 14/16 | 12/16 |
| **Houston homes (14), before** | **0/14** | **0/14** | **0/14** |
| **Houston homes (14), after** | **13/14** | **11/14** | **11/14** |
| **Houston all, before** | **15/30 (50%)** | **14/30 (47%)** | **12/30 (40%)** |
| **Houston all, after** | **28/30 (93%)** | **25/30 (83%)** | **23/30 (77%)** |

- **Home misses that remain:**
  - 1 Fort Bend home has no HCAD parcel (fix 3 in `county_coverage.md`, not done).
  - 2 Z4 condos get year but, by design, no floors or units, because their STY and unit count describe the unit, not the building.
- **Agreement with the kit:** home year built is within 1 year of the kit record in 12/13 (the exception is 2 years off). The kit has no stories for these homes to compare against.
- **Speed:** median about 0.5 s per property; 35 requests for 30 properties.

## Off-kit path: Census geocoder point, no kit lat/lon

| | year built | floors | unit count |
|---|---|---|---|
| Houston buildings (16) | 14/16 | 13/16 | 11/16 |
| Houston homes (14) | 12/14 | 10/14 | 10/14 |
| Houston all | 26/30 | 23/30 | 21/30 |

- **What the address fallback recovers:** the study found 9/29 Houston geocoded points with no parcel. The fallback recovers **6 of the 9**: 3 homes, 3 buildings.
- **No wrong parcels:** all 6 are the same account the kit point gives.
- **The 3 not recovered:**
  - 2 are in Fort Bend (outside HCAD).
  - 1 is a listing that says "St" while the roll says "Rd". It was rejected on purpose, because the street does not match.
- The one remaining miss besides these is a geocoder failure ("could not place this address").

## Not done

- **Wrong-parcel guard (unit count 1 on a tiny lot for a big building):** skipped. `county_record(address, lat, lon, city)` gets no hint of the expected unit count or building name, so there is nothing to check against.
- **Condo floors:** not given, for the reason above.
- **Fort Bend routing (FBCAD):** not in scope.
