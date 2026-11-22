# Live check of build e6a3d82 (2026-11-14)

Test write-up from the build, with building identities and record values removed.

Local server answered at once (/ gives 404, /check streams). Server error log tail: clean uvicorn start, no traceback.
Runs went one at a time through POST /check. Per run, throwaway scripts kept the full event stream with arrival times, a summary and the report HTML.

**Inputs (caveat):** saved runs do not keep page text (the snapshot keeps url/title/address/candidates only). So for a, b and c the text and JSON-LD were rebuilt from saved DOM dumps of the pages, with url/title/address/candidates taken from the saved run. The text is close to the extension's `innerText`, but it is not byte-identical, so the claims cache missed and the model extracted the claims fresh.
- d = **SYNTHETIC unit page.** Building A, an invented unit number. The kit row gives a studio with its own plan and its own scan. The page plants 2 beds / 2 baths / 1,100 sq ft.
- e = **RECONSTRUCTED** Houston single-family page (Home A): address plus the claim quotes of an earlier saved run.

## Results

Counts are confirmed / doesn't match / close / couldn't check.

| run | listing | time (wall / done.timing) | 1st verdict | counts now | counts before (run) | done, no error | confidence on mismatches; none on confirmed | aerial `observed.property` | "In Vexcel property data" verdicts | county | fill_in aerial rows | unit checks | report 200 + `id=compare` | no "…" in table | forbidden words / names |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a | Building C, Houston (listing site 1) | 46.0 / 44.0 s | 45.3 s | 20/15/3/2 | 35/1/2/2 | PASS | PASS (18/18) | PASS (nothing present) | none (pool confirmed by the building record + photo) | year, floors, units, parcel_match point, owner company | aerial-view only: correct, since nothing is present | n/a | PASS (41 rows) | **FAIL** (1 cell) | PASS |
| b | Building A, LA (listing site 2) | 72.8 / 72.5 s | 72.2 s | 18/1/2/17 | 15/0/0/9; 38 claims vs 24 | PASS | PASS (3/3) | PASS (pool area and count present) | an indoor spa claim → "Not in Vexcel property data" (cant_check) | year and units; stories, units_estimated and parcel_match all absent | aerial-trees; aerial-features left out because the pool is named by a claim (correct) | n/a | PASS (39 rows) | **FAIL** (4 cells) | PASS |
| c | Building B, Houston (listing site 3), pool claim | 69.4 / 69.3 s | 69.0 s | 14/0/0/26 | 16/0/1/23 | PASS (2 scan-vision evidence errors, see 8) | n/a (no mismatches); none on confirmed | PASS (no pool) | none; pool confirmed by photo with a soft note that property data can miss pools | year, floors, units, parcel_match point, owner company | aerial-trees | n/a | PASS (41 rows) | PASS | PASS ("Owner (county)" = "A company") |
| d | **SYNTHETIC** Building A unit | 59.0 / 58.8 s | 58.9 s | 0/3/0/2 | none | PASS | PASS (3/3: High 97, High 83, Medium 63) | PASS | none | as b | aerial-features ("May have N pools…"), aerial-trees | PASS: single_unit true, unit number read, unit_row evidence, scan_of "unit"; planted beds/baths/size all caught with neutral wording | PASS (6 rows) | PASS | PASS |
| e | **RECONSTRUCTED** Home A, Houston (single-family) | 27.4 / 27.2 s | 27.2 s | 2/0/0/21 | 0/1/0/22 | PASS | n/a | none: Vexcel property/extract answers 404 (no coverage); silently left out | none | year, floors, units, parcel_match address, owner individual; no beds/baths/sq ft | aerial-view only | n/a | PASS (24 rows) | **FAIL** (1 cell) | PASS |

The forbidden-word scan (accusatory words) over every verdict claimed / found / reason, confidence why, and fill_in label / value / note found nothing in any run. Owner text appears only as "A company" / "An individual". Management-company rows are company names.

## Bugs and oddities

1. **[HIGH] A plan label shared by many plans gets linked to one plan by its first size, which makes false mismatches** (run a).
   - The extractor labelled the claims with the page's descriptor line (a "1/1 with ..." or "2/2 with ..." finish line) instead of the plan codes printed on the line above. 11 plans share the first label, with sizes spread over about 300 sq ft.
   - `tools/kit/plan_match.py` (`listing_facts`) keeps the **first** area_sqft for the label. `link_plan` (in its size branch) then links the whole label to plan A (the smallest) "by size".
   - So 11 size claims are contradicted against plan A's size, and 3 more under the second label against a single plan's scan: 14 contradicted and 1 close, on confidence up to Medium 71.
   - The reason contradicts itself (invented sizes): "Listing says 880 sq ft. … plan A has 560 sq ft, 36% smaller. Matched to the building's plan A by size."
   - The earlier run (with extension text) labelled by plan code and had 1 mismatch. The linker should not resolve to one plan a label that carries several different sizes.
2. **"Listing says" cell cut with "…"** at 40 characters: `server/claim_field.py` (`_short`). The full text is only in `title`.
   - a: 1 cell (a laundry line).
   - b: 4 cells (long amenity and view sentences).
   - e: 1 cell (a parking line).
   - Source cells were never cut.
3. **An implausible scan decides over a record that agrees with the listing** (b).
   - Plan E (record size = listing) is contradicted by its scan "Plan E - 2 Bed / 2 Bath", which measures about 1.6 times that size and whose labels give **5 bedrooms**. Confidence is Medium 49, decided_by scan.
   - Plan F is close (scan about 20% under the listing; record about equal to the listing).
   - Scan floor area is used even when the same scan's labels are absurd.
4. **The unit page's size is decided by the scan, not the unit row** (d).
   - Found the scan's size (the scan linked to the unit is really its plan's scan) against the row's written size.
   - The scan is 46% above the row, which is the opposite of the usual ~11% under. The verdict direction is right, but the number shown is the weaker one.
5. **Fill-in wording / count** (d): aerial-features reads "May have N pools (about N sq ft in all) (seen in one survey)".
   - Vexcel gives a `pool.count` above 1 for a single high-rise.
   - The value has two parentheticals in a row.
6. **An indoor spa is mapped to the outdoor hot-tub flag** (b): an indoor spa amenity → found "Not in Vexcel property data" (cant_check). The outcome is harmless, but the property-data cell / wording does not apply to an indoor service.
7. **Verdicts all arrive in one burst at the end.** Time to first verdict ≈ total time (45 / 72 / 69 / 59 / 27 s). Nothing streams early.
8. **The time budget cut the vision check on scan stills** (c): 2 scan evidences with status error, "vision model on scan stills, confidence 0.0; skipped: the run's time budget is nearly used up".
9. **Step wording:** "Checking the floor plan this unit: its scan or record." (a, b). Source: `harness/graph/run.py` (`f"Checking the floor plan {name}: …"`).
10. **Stories on a single-family home** (e):
    - Vexcel elevation gives a height that reads as "about 3 floors" for a 1-story ranch. County wins, so the claim is confirmed (an improvement on the earlier false mismatch).
    - The reason says "The Vexcel aerial photo shows 3", but that number comes from elevation data, not the photo.
11. **Vexcel property data has no coverage at the e point** (property/extract 404). The run leaves it out with no evidence or step saying "no coverage" (by design, `harness/graph/run.py`).
12. **LA county evidence has no `stories`, `parcel_match`, `units_estimated` or `owner_type` keys** (b, d). They are absent, not false. The unit count was not flagged as estimated.
13. **Saved runs do not keep `text` / `jsonld`**, so a listing cannot be re-submitted exactly. Comparisons with earlier counts are partly confounded by fresh claim extraction (b: 38 claims vs 24).
