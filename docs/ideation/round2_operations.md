# Round 2 — Operations sector (people who operate, maintain, build or service buildings)

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Independent panel member. Inputs read: internal capability notes and notes on the CoStar kit, the Matterport API and the Vexcel API. No API calls made. Web evidence is from one round of searches on 2026-11-13; most cost figures come from vendor or trade pages and are marked as such. Anything I could not source is marked **[unverified]**. Arithmetic I did myself is marked **[computed]**.

Layers: **A** = CoStar kit, **B** = Matterport scans, **C** = Vexcel aerial.

---

## (a) Candidate problems (15)

| # | Who has it | Problem | Evidence it is real | Layers |
|---|---|---|---|---|
| 1 | Regional apartment operator / asset manager (Houston first) | Which roofs across the portfolio to replace first, what it will cost, and how to prove pre-storm condition when the insurer says "wear and tear" | Houston apartment owner sued its insurer over a >$2.4M Beryl underpayment; insurer's stated reason was wear and tear on the existing roof (https://www.insurancebusinessmag.com/us/news/risk-compliance-legal/apartment-owners-lawsuit-accuses-topa-of-underpaying-hurricane-beryl-claim-584035.aspx). 881-unit Greenspoint complex lost 56% of value after derecho + Beryl damage (https://www.bisnow.com/news/houston/multifamily/houston-apartment-complex-loses-more-than-half-its-value-after-storm-damage-128590). Carriers underwrite on roof condition and maintenance history (https://www.multihousingnews.com/managing-insurance-costs-as-climate-risk-rises/) | A + C, B minor |
| 2 | Apartment property manager, renovation manager, flooring/paint vendor | Scoping and pricing a unit turn or a value-add interior program needs a measure visit per floor plan; budgets slip | Turn cost roughly $1,500–$3,500 per unit for most operators, ~$3,900 average in one survey; turnover 40–50%/yr; 34–41 vacant days per turn (https://rets.ai/blog/turnover-multifamily-expense-nobody-budgets-correctly, https://www.lessen.com/resources/the-hidden-cost-of-a-slow-make-ready, NAA turnover deck https://naahq.org/sites/default/files/2025-03/01a.%20Apartment%20Turnover%202025.pdf). Value-add budgets ran 20–30% over 2021–22 underwriting (https://apers.app/learn/asset-classes/multifamily/value-add-multifamily-renovation-premium-modeling) — all secondary/vendor sources | B + A, C minor |
| 3 | LA apartment owner / manager; balcony inspectors and waterproofing contractors | California SB 721: every 3+ unit building must have its wood-framed elevated balconies, decks, stairs and walkways inspected; quoting needs a count of those elements per building | Statutory. Deadline extended to Jan 1 2026 by AB 2579; penalties cited at $100–$500/day; inspection quoted at $300–$500 per element or $65–$125 per unit (https://rimkus.com/article/california-balcony-inspection/, https://www.goodlifemgmt.com/blog/californias-balcony-inspection-law/, https://members.aagla.org/news/balcony-and-e3-inspections-compliance-and-beyond). No public compliance-rate number found | A + B + C |
| 4 | Office landlord / leasing team | Second-generation suites sit vacant; decide per suite: lease as-is, light refresh, or demolish and build a spec suite | In the kit itself, many lease listings sit on market for a long time. Spec suite build cost rose from ~$85 to ~$140/SF; second-gen space averages 12 months free rent vs 3 for spec (https://allwork.space/2025/10/tenants-flock-to-prebuilt-office-suites-while-landlords-struggle-with-costs/, https://www.connectcre.com/stories/spec-suites-or-tenant-buildouts-whats-more-cost-effective/). JLL fit-out average $295/SF (https://www.jll.com/en-us/guides/us-canada-office-fit-out-cost-guide-2025) | A + B, C minor |
| 5 | LA office/retail/hotel owner, facility manager, striping contractor | Accessible-parking exposure: too few or badly marked accessible stalls triggers Unruh/ADA suits | $4,000 statutory damages per violation plus fees; California is about 40% of US ADA suits; 2024 C.D. Cal. complaints allege parking signage and slope defects (https://www.mondaq.com/unitedstates/trials-appeals-compensation/1669712/ada-preparedness-series-california-is-the-epicenter-of-ada-serial-litigation, https://calmatters.org/justice/2023/03/california-disabled-access-lawsuits/) | A + C, B minor |
| 6 | Commercial roofer, HVAC contractor (vendor side of #1) | Finding and qualifying buildings worth a sales call; today it is door-knocking and paid aerial reports | Commercial reroof $5–$14/SF installed (https://www.thumbtack.com/p/commercial-roof-replacement-cost); RTU life 15–20 years per Lennox/ASHRAE, R-22 production ended 2020 (https://www.lennox.com/commercial/blog/resources-repair-or-replace-key-factors-to-consider-for-commercial-hvac-systems). Lead-qualification cost itself **[unverified]** | A + C |
| 7 | Acquirer, lender, PCA engineer | Desk pre-screen before paying for a Property Condition Assessment and replacement-reserve schedule | Fannie Mae requires a PCA for each property (Form 4099) and publishes Estimated Useful Life tables (https://multifamily.fanniemae.com/media/document/pdf/appendix-f-estimated-useful-life-tables, https://multifamily.fanniemae.com/media/36771/display). PCA fee **[unverified]** — no price found | A + B + C |
| 8 | Houston apartment owner after a storm | Assemble the claim file: pre-loss roof and interior condition, post-loss damage, lost rent | Same sources as #1; Beryl insured losses $2–3B (https://amp.insurancejournal.com/news/southcentral/2024/07/19/784786.htm) | A + B + C |
| 9 | Houston apartment operator | Avoid designation under the High-Risk Rental Building Program (10+ citations in 6 months → registration, mandatory inspection, published address) | Council approved May 6 2026 (https://communityimpact.com/heights-river-oaks-montrose/government/new-apartment-inspection-program-passes-in-houston-after-almost-a-year-of-discussion/) | A + C + public 311 data |
| 10 | LA owner of a building ≥20,000 SF; energy auditor | EBEWE: annual benchmarking plus audit/retro-commissioning every 5 years | LADBS ordinance (https://dbs.lacity.gov/sites/default/files/efs/forms/pc17/ebewe-ordinances.pdf); penalty figure is vendor-quoted only | A + C, B minor |
| 11 | Janitorial contractor | Bidding needs cleanable SF by area type; today a walkthrough with a measuring wheel | BSCAI: subtract non-cleaned areas, underpricing is the common error (https://www.bscai.org/Inside-Cleaning/Full-Article/5-tips-for-how-to-bid-on-a-commercial-cleaning-contract) | B + A |
| 12 | Movers, furniture/appliance delivery | Will it fit through the doors; where does the truck park | No cost evidence found **[unverified]** | B + C, A minor |
| 13 | Solar / EV-charging installer | Qualify roofs and lots, find the decision-maker | No LA existing-multifamily EV mandate confirmed in my search **[unverified]** | A + C |
| 14 | Landscaping, tree, pool, paving vendors | Bid by area without a site visit | No cost evidence found **[unverified]** | C + A |
| 15 | Wireless/fibre carrier site acquisition | Find tall roofs with a reachable owner | No evidence searched | A + C |

---

## (b) Ranking (1–5; data fit scored harshly)

| # | Problem | Realness / cost | Data fit | Why the data-fit score |
|---|---|---|---|---|
| 1 | Apartment roof triage + pre-loss baseline | 4 | 4 | C: roof condition 1–5, material, defect flags and history 2016–2026 are verified, but only at a handful of test points and per-collection values are noisy (the same footprint varied widely across collections). A: a large multifamily set with units, stories nearly always filled, year built, rents on most communities. B is weak: scans are tied to a floor plan, not to a building. No roof install date anywhere |
| 2 | Unit turn / renovation takeoff | 3 | 4 | B: `dimensions.areaFloor` on every sampled commercial model, wall graph and openings on a minority of commercial (appears complete on apartment units, unmeasured). A: floor plans with `numUnits`, rents per plan on most communities. No fixture, cabinet or finish data (object detection found none). C adds little |
| 3 | SB 721 element count and inspection scope (LA) | 3 | 3 | All three layers contribute, but the key step — counting balconies in obliques with `elements/detect` — is untested; fill rate of `buildingConstructionMaterial` is unmeasured; "Balcony" is in the room vocabulary but did not appear in the commercial sample. LA only |
| 4 | Office suite reuse vs spec | 5 | 2 | Few listings carry suite tours; office Property Insights coverage is weak; commercial rooms come back Void/Other; lease expiration on a small share of current tenancies; no commercial vacancy stats |
| 6 | Roofer / HVAC lead qualification | 3 | 4 | Same data as #1; owner names only on a minority of properties with listings; emails and phones are placeholders; `rooftop hvac unit` detection returned 0, though precomputed `ac-unit.count` works |
| 8 | Storm claim file | 4 | 3 | Houston collections 2023 and 2025/2026 bracket July 2024, plus a Harvey 2017 set. Scan capture dates are unknown, so "interior before the loss" is unproven. Event-driven; Beryl is now over two years old |
| 7 | PCA desk pre-screen | 4 | 3 | Quantities are available; component ages are not (`renovations[]` sparsely filled) |
| 5 | Accessible-parking exposure | 4 (CA) | 2 | ADA symbol detection verified at one lot; no stall count from any endpoint; `parking[].totalSpaces` only partly filled; LA non-apartment stock in the kit is small |
| 9 | Houston high-risk rental | 3 | 2 | Needs 311 data as the core; our layers are supporting |
| 10 | EBEWE targeting | 3 | 2 | GBA identifies covered buildings; nothing on energy use |
| 11 | Janitorial bidding | 2 | 2 | Office models exist; no floor-surface type |
| 12 | Movers | 2 | 3 | Door widths complete on residential only |
| 13 | Solar / EV | 3 | 2 | No stall count, no electrical data |
| 14 | Grounds/pool/paving vendors | 2 | 3 | Areas exist; low stakes |
| 15 | Wireless siting | 2 | 2 | No Matterport role |

Top 6 by combined score: #1 (8), #2 (7), #4 (7), #6 (7), #8 (7), #7 (7), then #3 (6). I develop #1, #2 and #3. I skip #4 despite the highest realness because the data fit is a 2: the suites that are vacant are mostly not the suites that are scanned. #6, #7 and #8 are the same evidence as #1 seen by a different reader, so they are folded into #1 as alternative end actions.

---

## (c) Top 3 developed

### 1. Roof triage and pre-loss baseline for an apartment portfolio (my pick)

**The problem in the owner's words.** "I run 30 garden communities in Houston. Each has 10 to 25 buildings. I do not know which roofs will fail next, I cannot afford to reroof all of them, and when a storm comes the carrier tells me the damage was already there. I need a ranked list, a budget, and a dated record of what each roof looked like before the storm."

**What they do today and what it costs.**
- A roofer or roof consultant walks each property; reserve numbers come from a PCA done at purchase or refinance. PCA fee **[unverified]**.
- Reroofing runs $5–$14/SF installed, tear-off adds $1–$3/SF (https://www.thumbtack.com/p/commercial-roof-replacement-cost — contractor-marketplace figures).
- The cost of having no baseline is the denied claim: the >$2.4M Beryl dispute above turned on "wear and tear to the existing roof".

**Fields.**
- C: `property/extract` per structure — `footprint.area`, `roof-characteristics.condition` (1–5), `material.class`, `shape.value`, `roof-defects.{tarp, missing-material, patch, debris, structural-damage, rust, discoloration.water-pooling}.{detected, percent}`, `roof-objects.ac-unit.count` — one feature per collection, so a condition series per building. `ortho/extract` with `collection` for dated before/after crops; `oriented/extract` for eaves and fascia; `dsm/extract` for ponding on flat roofs **[unverified that DSM resolves ponding]**.
- A: `propertyManagementCompanyName` (defines the portfolio), `propertyApartment.models[].numUnits`, `numStoriesAboveGrade` (share of units directly under a roof), `constructionEvents[]` year built, `renovations[]`, `buildingClass`, apartment-listing `minRent`/`maxRent` per plan and `vacancyPercent` (rent at risk under each roof), sale comps `soldDate` and `saleConditions[]` (deferred maintenance flag; a recent sale means a new owner with a capital budget).
- B: panoramas and `ceiling` on scanned units for ceiling-stain evidence by our own vision model; `geocoordinates` to guess which building a scan sits in **[unverified]**.
- Public join: Houston weekly permit summaries and LADBS permit data for reroof permits, which would give a roof age; HCAD building records (https://hcad.org/pdata/pdata-gis-downloads.html). Whether reroof permits can be matched to apartment buildings is **[unverified]**.

**What the combination adds.** C alone gives a condition score per roof. A turns it into a decision: rent and units at stake under each roof, age against expected life, who operates it, whether it just sold. The history series separates slow decay (wear) from a step change between two dated collections (event), which is exactly the disputed question in a claim.

**What cannot be answered and how much it hurts.**
- Roof install date: absent. Hurts the reserve schedule; partly recoverable from a visible material or colour change between collections, or from permits.
- Leaks, deck moisture, membrane seams: not visible from the air. The output is a triage list for inspection, not a condition certification.
- Scan-to-building mapping is unproven, so B is corroboration on a few units at best.
- Attribute noise across collections is large. The system has to check each value against the ortho before trusting it.

**Reasoning over conflicting evidence.** Newest collection says condition 2, the one before says 4: read both orthos, check whether the footprint is the same building, check for a tarp or patch, check whether the material class changed (reroof), then decide between decay, storm, reroof or classifier error.

**End action.** (i) A scope sheet per building sent to three roofers as an RFP: roof area, material, shape, defect map, access notes. (ii) A dated baseline dossier attached to the insurance renewal submission. (iii) After an event, the same dossier becomes the pre-loss exhibit in a proof of loss.

**Worked example.** The only parcel with verified attributes is a Houston hotel in the kit (used here as a stand-in for method). Newest collection: a large flat membrane primary structure with a mid-range condition score and many AC units. Older collections report the same primary footprint at much smaller sizes, and one run labels it `single_family`. The system would reject the small footprints against the ortho, keep the large one, and price a full replacement at roof area × $5–$14/SF **[computed]**. With a mid-range condition and no defect flags it would rank this roof "monitor, no RFP" and file the newest ortho as the baseline. For a typical Houston garden community the same steps run per building, weighted by rent: at a typical Houston 2BR rent, each 2BR unit under a failed roof puts twelve months of that rent at risk **[computed]**.

**Cheapest kill check.** Run `property/extract` on 50 Houston multifamily kit coordinates. Kill if (a) fewer than about 70% return per-building structures for the community, or (b) the two newest collections disagree on condition by 2 or more points on most buildings with no visible change in the ortho.

---

### 2. Unit-turn and renovation takeoff from the scan

**The problem in the owner's words.** "Before I can order flooring or get a paint price, someone has to go measure the unit. For a renovation program across 12 floor plans I pay for a measure of each, the numbers disagree with the marketing square footage, and my budget is wrong before we start."

**What they do today and what it costs.** Vendor measure visits or an in-house tape measure; quantities kept in spreadsheets per floor plan. Turn cost and vacancy-day figures as in the table above (vendor-sourced). LVP $2.50–$5.00/SF installed, carpet $3.50–$6.50/SF (https://www.flooringclarity.com/apartment-carpet-replacement-costs-options-practices/ and a vendor blog). I found no source for the cost or delay of the measure visit itself **[unverified]** — this is the weak point of the realness score. Operators who have owned a community for years already have these numbers; the pain is real mainly at acquisition, at the start of a value-add program, and for vendors bidding on a property they have not seen.

**Fields.**
- B: `rooms.dimensions.{areaFloor, areaWall, width, depth, height}`, `rooms.classifications` (Kitchen, Bathroom, Bedroom — split wet and dry flooring), `floors.edges.openings{type, width, height}` (door and window counts and sizes for blinds, doors, trim), `ceiling`, the DXF floor plan, and the defurnished view to see floors and walls without furniture.
- A: `propertyApartment.models[].{numBeds, numBaths, minSquareFeet, maxSquareFeet, numUnits}` with scan keys on `models[].attachments[]` and `units[].attachments[]`; apartment-listing `apartmentModels[].{minRent, maxRent, numUnitsAvailable}`; `vacancyPercent`.
- C (minor): building count and footprints for exterior paint; `hardscapes` and `vehicles.count` for staging and dumpster placement.

**What the combination adds.** B gives quantities for one unit. A multiplies them by the unit count per plan to give a community-wide bill of quantities, and gives the rent per plan to test whether the spend pays back. A also supplies the check: scan area against advertised area.

**What cannot be answered and how much it hurts.**
- Current finishes, cabinet runs, countertop length, appliance count: no object detection. Needs our own vision on panoramas. Hurts a lot for kitchens and baths, which are most of a renovation budget.
- One scan per plan represents every unit of that plan; unit-level damage is unknown. Fine for a renovation program, wrong for a single damaged turn.
- `areaFloor` is net room area, not leasable SF; the ratio is uncalibrated.
- Number of floor plans with a linked scan: not counted.

**End action.** A purchase order or bid request to the flooring and paint vendors with quantities per plan, and a renovation budget line per plan for the owner's approval.

**Worked example.** A 2BR/2BA apartment-unit scan from a Houston community in the kit: classified rooms, door and window openings, and a scan area a little under the advertised SF **[computed]** — consistent with net-of-walls area, so not a mismatch flag. Whole-unit LVP at $2.50–$3.75/SF is scan area × that range **[computed]**; multiplied by that plan's `numUnits` gives the program line. The system would also list door and window openings for blinds and note that kitchen and bath scope needs a panorama review.

**Cheapest kill check.** On 100 apartment-unit scans, compute sum of `areaFloor` ÷ advertised `minSquareFeet`. Kill if the spread is wider than about ±10% around its median, or if fewer than about 60% have the wall graph and openings.

---

### 3. SB 721 element count and inspection scope (LA apartments)

**The problem in the owner's words.** "State law says my balconies, exterior stairs and walkways have to be inspected. The inspector quotes per balcony or per unit and wants a site visit to count them. I own eight buildings and I do not know which are covered, how many elements each has, or what it will cost."

**What they do today and what it costs.** An inspector or engineer walks the property to count and classify elements before quoting. Quoted prices: $300–$500 per element, or $65–$125 per unit; penalties $100–$500/day; repairs cost far more than inspection (vendor and trade sources above). The law covers buildings with 3+ units and elements more than 6 ft above ground that rely on wood framing, with a sample of each element type inspected and a 6-year cycle (from the statute as I recall it, Health & Safety Code §17973 — **[verify before relying on it]**). The first deadline passed on Jan 1 2026; I found no figure for how many buildings remain uninspected, which caps the realness score at 3.

**Fields.**
- A: LA multifamily properties, `propertyApartment` unit counts (3+ test), `numStoriesAboveGrade` (elements above 6 ft), `buildingConstructionMaterial` (wood frame test; fill rate unmeasured), `constructionEvents[]` year built, `propertyManagementCompanyName`, listing `propertyContacts[]` names where present.
- C: `oriented/extract` in four directions to see every facade; `elements/detect` with labels such as "balcony", "exterior staircase", "exterior walkway" on obliques (untested); `structures[].footprint` for building count; history to see whether balconies were rebuilt.
- B: rooms classified `Balcony` or `Patio` with `areaFloor`; the doorway opening onto the balcony with `lowerElevation` (threshold height, a waterproofing indicator); panoramas of deck surface, railing and soffit for visible staining or cracking by our own vision.

**What the combination adds.** A decides whether the law applies. C counts and types the elements per building, which sets the sample size and the price. B gives the close-up no aerial view has: deck surface, threshold and railing condition on the scanned units. None of the three can scope the job alone.

**What cannot be answered and how much it hurts.**
- Whether the framing is wood: A's field may be empty or coarse; obliques cannot see inside a soffit. Hurts — it decides applicability.
- Hidden rot: the statute requires a qualified inspector; this system only scopes and prioritises.
- Interior-courtyard elements may be hidden in obliques.
- Balcony detection accuracy is unknown.

**End action.** An inspection order sent to a qualified inspector with the element schedule per building and a price range, and a notice to the owner listing which buildings appear covered and which elements look worst.

**Worked example.** Property A, an LA multifamily building in the kit with several unit scans. The system would confirm 3+ units and stories from A, pull four obliques, count stacked balconies per facade, reconcile the count against the balcony rooms in those scans (a 3-bed plan with a balcony room in the scan but no balcony visible on the facade means a courtyard-facing unit), and output for example "N elements of 2 types, sample of X, estimated inspection cost N × $300–$500". The actual numbers are not known without running it.

**Cheapest kill check.** Run `elements/detect` "balcony" on obliques for 20 LA multifamily properties and compare with a hand count. Kill if the count is off by more than about 25% on most. Also measure the fill rate of `buildingConstructionMaterial` on LA multifamily; if mostly empty, applicability cannot be decided.

---

## Pick

**#1, roof triage and pre-loss baseline for an apartment portfolio.** It has the strongest sourced cost evidence (a $2.4M claim dispute that turned on pre-loss roof condition, a 56% value loss), it uses fields that are verified to exist on the property type that makes up most of the kit, and the multi-collection disagreement in Vexcel is a real reasoning problem rather than a staged one. Its honest weakness is that Matterport contributes little; if three-layer depth matters more than problem size, #3 is the candidate where each layer is necessary, but it rests on an untested detection step and is LA-only.
