# Round 2 — problems owned by people with money at risk on buildings

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Independent panel member. Inputs: internal capability notes and notes on the CoStar kit, the Matterport API and the Vexcel API, plus web search. No API calls made. Layers: A = CoStar kit, B = Matterport, C = Vexcel.

Marking: **[unverified]** = I could not confirm it from a primary source or from the notes. **[illustration]** = arithmetic on cited averages, not a measured result.

---

## (a) Candidate problems (16)

| # | Problem | Who owns it | Evidence it is real | Layers |
|---|---|---|---|---|
| 1 | **Over-assessed apartment buildings**: assessed value above market or above comparable buildings; appeal needs comp-by-comp condition evidence | Owners, asset managers, tax agents (and, mirrored, the assessor) | Property tax is 30-40% of Texas apartment operating expenses ([Texas Standard / NAA](https://www.texasstandard.org/?p=147429), [Multifamily Dive](https://www.multifamilydive.com/news/texas-securitized-multifamily-loans-aprtment-distress/824724/)); 516,205 Harris County protests in 2024, 81% filed by agents, per a secondary source ([Harbert](https://www.harbertgroup.com/blog/1065/Texas+Property+Tax+Protest+2026%3A+How+Houston+Homeowners+Win+Reductions+At+Hcad)); LA apartment prices down roughly 20-35% from the 2021 peak ([Commercial Observer](https://commercialobserver.com/2026/07/los-angeles-multifamily-housing-investment-sales-rent/)) while Prop 13 values keep rising 2%/yr | A + C + B + free roll |
| 2 | **Insurance submissions with wrong or missing building facts** (roof age, roof shape/material, construction, stories, sprinklers); missing fields are priced at worst case | Owners, insurance brokers, underwriters | Verisk estimate of ~$1.31B/yr premium leakage from wrong roof age, >25% of roofs wrongly classed as under 15 years, cited by [Archipelago](https://www.onarchipelago.com/blog/why-you-should-pay-closer-attention-to-roof-age-for-commercial-properties); multifamily insurance costs +26% in one year, up to +120% ([NMHC 2023](https://nmhc.org/research-insight/research-report/2023-nmhc-state-of-multifamily-risk-survey-report)) | C + A + B |
| 3 | **Unpermitted / phantom square footage**: listing says more area or bedrooms than the public record; lender, appraiser and buyer must decide what counts | Appraisers, mortgage lenders, buyers, insurers, assessor | Fannie Selling Guide B4-1.3-05 requires the appraiser to explain area discrepancies and the market effect of unpermitted additions ([Fannie Mae](https://selling-guide.fanniemae.com/1032992541)); some lenders refuse to count it ([Sacramento Appraisal Blog](https://sacramentoappraisalblog.com/2016/10/25/the-problem-with-non-permitted-additions-in-real-estate/)). No hard prevalence statistic found | B + C + A + free permits/roll |
| 4 | **Multifamily loan surveillance**: borrower-reported occupancy and condition do not match the property | Lenders, servicers, CMBS/agency investors | Multifamily CMBS delinquency 8.09% in Oct 2026 ([CRE Daily / Trepp](https://www.credaily.com/?p=224934)); Freddie Mac raised unit-inspection and lease-audit samples in 2024 to detect misreporting ([Bisnow](https://bisnow.com/national/news/multifamily/freddie-mac-tightens-lending-rules-in-bid-to-detect-fraud-123826)); Houston: Arbor foreclosed on 3,200 Applesway units, $229M, with rats, roaches and uncollected trash reported ([Bisnow](https://bisnow.com/houston/news/multifamily/229m-multifamily-portfolio-foreclosure-part-of-much-trouble-for-a-texas-investor-118463)) | A + C (+ B weakly) |
| 5 | **Underinsurance (insurance-to-value)**: declared replacement value too low | Owners, lenders (loan covenants), insurers | Kroll: 68% of commercial buildings appraised 2020-21 were underinsured by 25%+, as reported second-hand by [Insurance Business](https://www.insurancebusinessmag.com/us/news/property/most-commercial-property-accounts-arrive-with-a-valuation-gap-584546.aspx) | A + B + C |
| 6 | **Cost segregation**: splitting a purchase into 5/7/15-year components needs counts of paving, pools, landscaping, flooring, cabinets | Owners, corporate real-estate finance, CPAs | Studies cost roughly $5k-$15k for small multifamily (marketing source, [RE Cost Seg](https://www.recostseg.com/post/cost-seg-roi-year-one)); 100% bonus depreciation restored for property acquired after 19 Jan 2025 ([Ankura](https://ankura.com/insights/the-obbb-and-the-benefits-of-a-cost-segregation-study)) | A + B + C |
| 7 | **Did this Houston property flood, and would it again?** | Lenders, buyers, flood insurers | About 65-75% of the 204,000 Harris County homes and apartments flooded by Harvey were outside the 100-year floodplain ([SEJ / Houston Chronicle](https://www.sej.org/node/29491)) | C (2017 Harvey imagery, DTM) + A |
| 8 | **Wildfire insurability of LA hillside homes before escrow closes** | Buyers, lenders, insurers | 13% of California Realtors had a deal fall out of escrow over insurance in 2024, double 2023 ([Insurance Journal](https://www.insurancejournal.com/news/west/2024/10/30/799106.htm)) | C (defensible-space zones) + B (windows) + A |
| 9 | **LA soft-story / seismic risk on apartment loans** | Lenders, buyers, earthquake insurers | Fannie Mae requires scenario expected loss of 20% or less ([Fannie MF Guide](https://mfguide.fanniemae.com/fnmf-pdf/download/4626)); about 14,000 LA buildings on the retrofit list in 2019 ([ABC7](https://abc7.com/earthquake-retrofit-northridge-soft-story/5280732)) | A + C (obliques show tuck-under parking) |
| 10 | **Office "shadow vacancy"**: leased but empty space behind a loan | Office lenders, CMBS investors | Office CMBS delinquency 12.33%, Oct 2026 ([CRE Daily / Trepp](https://www.credaily.com/?p=224934)) | A (tenant roster) + C (cars over time) |
| 11 | **Rent-comparability grid**: appraiser must adjust rent comps for true unit size, finish and amenities without entering them | Appraisers, lenders, acquisition analysts | Standard appraisal practice; no cost figure found **[unverified]** | A + B + C |
| 12 | **Pre-loss condition record for storm claims** | Insurers, owners, public adjusters | Roof claim disputes turn on prior condition; no figure found **[unverified]** | C (history) + B |
| 13 | **Office suite area audit** (rentable SF billed vs usable SF measured) | Lease auditors, corporate tenants | No figure found **[unverified]** | B + A |
| 14 | **Sale-condition verification of comps** (was the comp distressed or run-down at sale date?) | Appraisers, litigation/estate valuers | Follows from non-disclosure in Texas (only a minority of Houston comps in the kit are priced) | A + C |
| 15 | **Unit-count mismatch in LA apartments** (more units operating than permitted) | Lenders, buyers, title | No prevalence figure found **[unverified]** | A + C + free roll |
| 16 | **Hotel collateral condition** | Hotel lenders | Few hotels in the kit, Houston only | A + C |

## (b) Ranking (harsh)

Realness = how costly and how well evidenced. Data fit = can the three layers really answer it at the coverage the notes report.

| # | Problem | Real (1-5) | Fit (1-5) | What is missing |
|---|---|---|---|---|
| 1 | Over-assessment appeal | 4 | 4 | Assessed values are not in the kit (free public roll needed). B is supporting evidence only. Actual rent roll absent. An existing consultant industry already serves large owners |
| 2 | Insurance submission facts | 4 | 4 | Pain has eased since 2024 ([NMHC 2024](https://nmhc.org/news/press-release/2025/nmhc-releases-2024-state-of-multifamily-risk-survey-and-report)). Fill rates of `buildingConstructionMaterial` and `hasSprinklers` not profiled. Roof-age dating from history untested. Vexcel per-collection attributes are noisy |
| 3 | Unpermitted / phantom SF | 3.5 | 4 | Few California listings in the kit; scan area vs listed SF tolerance untested; permits and roll are external; no prevalence number |
| 4 | Loan surveillance | 5 | 3 | No loan data in kit. Scans are marketing scans chosen by the owner (biased toward good units), scan date not known. `vacancyPercent` on only part of multifamily. Car count as occupancy proxy untested |
| 5 | Underinsurance | 4 | 2.5 | No construction cost table in any layer |
| 6 | Cost segregation | 3 | 3 | No object detection in scans (none in the sample), so every interior count needs our own vision; no unit-cost table |
| 7 | Harvey flood history | 4 | 3 | Whether the 2017 raw images show water at kit properties is untested; B adds little |
| 8 | Wildfire insurability | 4 | 2.5 | Few LA listings, unknown share in fire zones; windows on most sampled residential |
| 9 | Soft-story | 4 | 2.5 | B adds nothing; needs our vision on obliques |
| 10 | Office shadow vacancy | 4 | 2 | Garages hide cars; capture weekday/time unknown; few offices in the kit |
| 11 | Rent-comp grid | 3 | 4 | Amenity ids have no names; real but low-stakes |
| 12 | Pre-loss record | 3 | 2.5 | Scan dates unknown; no 2024 oblique collection at the test point |
| 13 | Suite area audit | 3 | 2 | Limited office scans; wall graph on a minority of commercial |
| 14 | Comp sale-condition | 3 | 3 | Two layers only |
| 15 | Unit-count mismatch | 3 | 2 | Cannot see units from the air |
| 16 | Hotel collateral | 2 | 2 | Few properties |

Top 3 developed below: 1, 2, 3. Problem 4 has the worst pain but the layers answer it least honestly.

---

## (c) Top 3 developed

### 1. Over-assessment appeal for apartment buildings (my pick)

**The owner's words.** "My tax bill is my biggest expense line. In Houston the district values my 1978 complex like the renovated one down the road. In LA I bought in 2021 and my assessed value still climbs 2% a year while the market fell. I know I am over-assessed, but the hearing is won by whoever has the better comparison grid, and I cannot go inside the other buildings."

**Today and cost.**
- Texas: owners hire agents on contingency, quoted at 25-50% of first-year savings ([Harbert](https://www.harbertgroup.com/blog/1065/Texas+Property+Tax+Protest+2026%3A+How+Houston+Homeowners+Win+Reductions+At+Hcad), residential figure; commercial terms **[unverified]**). A consultant reports $5B of commercial value reductions in Harris County in 2025 ([O'Connor](https://www.poconnor.com/?p=62515), self-reported).
- LA County: regular appeal window closes 30 Nov 2026 ([LA County AAB](https://lacaab.lacounty.gov/)); decline-in-value review runs 2 Jul-30 Nov ([LA County](https://auditor.lacounty.gov/wp-content/uploads/2025/01/ASSR_PropertyRelief_20241210a.pdf)). That window is open today.
- Texas grounds: market value, or unequal appraisal against the median of comparable properties "appropriately adjusted" (Tax Code 41.43(b)(3); wording from memory, **[unverified]** against current statute; 2025 bills proposed changes, [SB 2063](https://capitol.texas.gov/tlodocs/89R/billtext/html/SB02063S.htm)).

**Fields and what each layer adds.**
- A: `buildingClass`, `buildingRating`, `constructionEvents[]`, units and `grossBuildingAreaSquareFeet` (nearly always filled), `vacancyPercent` (partly filled), rents per floor plan (many communities), sale comps `soldForPrice` / `pricePerUnit` / `capitalizationRateActual` / `saleConditions[]` (multifamily comps; LA mostly priced, Houston a minority), `parcelNumbers[]` (fill rate not profiled). This picks the comparables and builds an income value. In LA the subject's own comp gives its purchase price, so the Prop 13 value can be estimated from the kit alone.
- C: `roof-characteristics.condition`, `roof-defects.*`, pool state, `footprint.area`, DSM minus DTM, and imagery dated near the 1 January valuation date (the Houston 2026 collection at the test point was flown January 2026). This is dated, third-party condition evidence for the subject and for every comp.
- B: unit scans of the subject and of comps (nearly all multifamily properties in the kit scanned): room areas, ceiling heights, and panoramas showing finish level. This is the only way to compare interiors of buildings the owner cannot enter.
- Free join: HCAD bulk files, including `building_other.txt` for commercial ([HCAD](https://hcad.org/hcad-online-services/pdata/), [codebook](https://hcad.org/assets/uploads/pdf/pdataCodebook.pdf)); LA County assessor roll ([data.lacounty.gov](https://data.lacounty.gov/Parcel-/Assessor-Parcels-Data-2006-thru-2017/9trm-uz8i); current-year edition **[unverified]**).
- Combination: A alone says "these are peers on paper". Only B and C let the grid say "the peer has a 2023 roof and renovated interiors; the subject has a condition-2 roof with patching since 2022 and original kitchens", which is the adjustment the hearing turns on.

**Cannot answer.** Actual rent roll and expenses (owner supplies; moderate). The district's own model (minor). Finish grading needs our own vision on panoramas (real work). Scan date unknown, so an interior may predate a renovation (hurts; must be stated). Vexcel attributes vary by collection (must pick and sanity-check).

**Action.** Houston: Notice of Protest plus evidence packet; outside the May window, a 25.25 correction motion (**[unverified]** details). LA: Assessment Appeal Application before 30 November.

**Worked example [illustration].** LA 40-unit Class C building whose kit comp shows a late-2021 purchase at about the then-average $430k/unit, so $17.2M. Factored at 2%/yr for five years: about $19.0M assessed. Kit comps for similar class and age in 2025-26 cluster near $280-350k/unit (range from cited broker reports), so $11-14M. Vexcel shows roof condition 2 with discoloration in the 2025 and 2026 collections; scans show unrenovated units, so no upward adjustment. Conclusion: file for decline in value at about $13M; at roughly 1.2% tax rate (**[unverified]** rate) that is about $70k per year. The system also reports when the evidence conflicts, for example a comp flagged `saleConditions` distress that should be excluded.

**Cheapest kill check.** From the kit only: count LA multifamily properties whose own priced comp is dated 2019-2022 and that have 5 or more priced peer comps dated 2025-2026. If under about 50, the LA case is dead. For Houston: look up HCAD value per unit for 20 kit properties and check whether any sit 15% above their class/age peers.

### 2. Insurance submission facts for apartment communities

**The owner's words.** "My broker sends a spreadsheet of my buildings to the carriers. Half the roof fields are blank or copied from a five-year-old appraisal. The model assumes the worst for every blank, and I pay for it. The underwriter, for their part, does not believe the roof year I typed."

**Today and cost.** Brokers and risk engineers fill the fields by hand from owner emails, old appraisals and paid inspections; aerial-analytics vendors sell roof scores. Missing fields push models to conservative defaults ([Archipelago](https://www.onarchipelago.com/blog/cat-modeling), vendor claim). Completing the fields moves losses in both directions ([Moody's](https://www.moodys.com/web/en/us/insights/insurance/the-last-mile-of-exposure-data-enrichment-where-mapping-makes-the-difference.html)), so this can raise a premium as well as lower it. Inspection cost per site **[unverified]**.

**Fields.**
- C: roof `material.class`, `shape.value` (hip vs gable vs flat), `condition`, `roof-defects.*`, `roof-objects`, tree cover over roof, pool, per-structure footprints; one feature per collection back to 2016 to date a re-roof; DSM height.
- A: year built, `numStoriesAboveGrade` (nearly always filled), `grossBuildingAreaSquareFeet`, units, `buildingConstructionMaterial`, `hasSprinklers` / `sprinklerType` (fill not profiled), `renovations[]` (rarely filled).
- B: ceiling heights and room areas to check declared area; panoramas for sprinkler heads and finish level (our own vision; the API detects no objects).
- Combination: A states what the owner claims, C measures the outside and dates changes, B shows the inside. Disagreements are the product: "stories 3 per CoStar, DSM shows about 12 m; roof declared 2019, imagery shows the same patched membrane 2016-2026".

**Cannot answer.** Wiring, plumbing, electrical panels, fire alarms (not visible; hurts for fire rating). Replacement cost (no cost table). Re-roof dating from history is untested and attributes are noisy (footprint area for one building differed widely between collections).

**Action.** A corrected statement of values with an evidence sheet sent to the broker before renewal, or an underwriter's inspection order for the specific buildings in conflict.

**Worked example [illustration].** Houston 1984 garden community, 14 buildings. CoStar: 2 stories, wood frame. Vexcel 2026: 14 structures, shingle, gable, condition 2-3, tarp detected on 2 buildings in 2025 and 2026, none in 2023. Conclusion: roof covering not replaced since at least 2016 on 12 buildings; 2 buildings have open damage for over a year; send corrected roof fields and flag those 2 for repair before renewal.

**Cheapest kill check.** Pull `property/extract` for 20 Houston communities and see whether roof condition and material are stable across collections for the same structure. If they flip randomly, dating fails.

### 3. Unpermitted or phantom square footage on homes for sale

**The owner's words (appraiser / lender).** "The listing says 2,400 SF and four bedrooms. The county says 1,650 and three. I have to explain the gap, decide whether the extra space is legal, and I am liable if I count it."

**Today and cost.** The appraiser measures on site, searches permit records by hand, and writes an explanation ([Fannie Mae B4-1.3-05](https://selling-guide.fanniemae.com/1032992541)); lenders may refuse to lend on the unpermitted area ([forum report](https://biggerpockets.com/forums/311/topics/983003-appraisal-using-actual-sf-versus-permitted-sf)). At typical LA home prices each disputed 100 SF is tens of thousands of dollars of claimed value **[illustration]**.

**Fields.**
- A: `property.sqftMin`, `bedsMin`, `bathsMin` (nearly always filled), `yearBuilt` (mostly filled), `closePrice` (LA only), `remarks` (mostly filled), `taxes` (partly filled).
- B: `dimensionEstimates.areaIndoor`, room classifications and wall graph (all residential models in the sample): measured interior area and bedroom count.
- C: `structures[].footprint.area` and `structure.count` per collection since 2016, DSM for added storeys, ortho before/after: when the building grew.
- Free join: county roll area and bedrooms; city permit records (LADBS open data, **[unverified]** in this session).
- Combination: B proves the space exists and how big it is; C dates when it appeared; A states what is being sold; the permit record says whether it was approved. No single layer can separate "county record is stale" from "addition built in 2020 with no permit".

**Cannot answer.** Additions before 2016. Interior-only conversions (garage to bedroom) show in B but cannot be dated by C. Scan area vs listing area tolerance is untested. Few California listings in the kit; Houston has more but no sale prices.

**Action.** A discrepancy report to the lender or appraiser with a permit-records request, before closing.

**Worked example [illustration].** LA listing: 2,400 SF, 4 bed. Scan: about 2,310 SF indoor, 4 bedrooms. Roll: 1,650 SF, 3 bed. Vexcel footprint grows between the 2018-19 and 2021 collections; no permit found for that period. Conclusion: about 650 SF built 2019-2021 without a permit on record; treat as unpermitted until the seller produces one.

**Cheapest kill check.** For 20 residential models, compare scan indoor area with listing `sqftMin`. If the spread on ordinary homes exceeds about 10%, the method cannot flag real gaps.

---

## Pick

**Problem 1, over-assessment appeal.** Largest recurring cash cost, a legal filing with a deadline (LA: 30 November 2026), sits on the densest data (the kit's largest set of apartment properties, comps and scans), and the LA version can be tested from the kit in minutes. Its weakness is that the interior scan is supporting evidence, not the core measurement.
