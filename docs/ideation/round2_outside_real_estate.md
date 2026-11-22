# Round 2 — problems outside real estate

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Independent panel member. Sector: industries other than real estate that would pay for measured interiors + occupants + ten years of aerial views in Houston and Los Angeles.

Sources for data claims: the project's capability notes, its notes on the CoStar kit, the Matterport API and the Vexcel API, and three fill rates I read from the CoStar commercial-property profile (`hasSprinklers` low, `buildingConstructionMaterial` fully populated but value quality not checked, `propertyApartment.elevators[]` sparse). Web evidence was gathered by search on 2026-11-13; where I only saw a search summary and not the primary page, the claim is marked **[search summary]**. Anything with no evidence is marked **[unverified]**.

Layers: A = CoStar kit, B = Matterport scans, C = Vexcel aerial.

---

## (a) Candidate problems

| # | Problem | Who has it | Evidence it is real | Layers |
|---|---|---|---|---|
| 1 | Fire crews arrive at apartment complexes, hotels and offices with no pre-incident plan: no layout, no roof hazards, no height, no access notes | Fire departments (HFD, LAFD), first-due company officers | NIOSH fatality reports repeatedly list missing pre-incident plans as a contributing factor, including a Houston case where the department "did not have detailed pre-incident plans for this structure" ([FireRescue1](https://www.firerescue1.com/niosh/report-preplanning-of-vacant-structures-highlighted-in-death-of-houston-firefighter)); a 2017 Houston controller audit found 526 of 5,000+ apartment buildings fire-inspected in two fiscal years ([Houston Chronicle via PressReader](https://www.pressreader.com/usa/houston-chronicle/20170616/281487866339042)) **[search summary]** | A+B+C |
| 2 | Commercial and apartment insurers price policies on wrong construction, protection and occupancy data, and pay for site surveys to catch it | Commercial property / habitational underwriters, loss-control teams | Verisk: $4.5 billion premium leakage from misclassification; construction class wrong nearly one-third of the time; occupancy changes almost a quarter of the time over a decade ([Verisk](https://www.verisk.com/blog/4-5-billion-in-commercial-property-premium-leakage-due-to-misclassification/), [Verisk](https://www.verisk.com/insurance/visualize/high-and-inside-the-crucial-metrics-commercial-property-underwriters-need-to-avoid-premium-leakage)) **[vendor figures, search summary]**; Davies ran 119,976 on-site commercial loss surveys in 2025 ([Davies](https://davies-group.com/northamerica/how-commercial-loss-control-surveys-reduce-risks-costs-for-insurers/insureds/)); habitational market hardening, State Farm exit from CA apartment policies (~42,000 policies) ([CRC](https://www.crcgroup.com/Tools-Intel/Specialty-Tools-Intel/habitational-market-takes-a-hard-turn-9)) | A+B+C |
| 3 | City has ~4,500 apartment properties, 15 inspectors, and must decide which complexes to inspect first | Houston Permitting Center habitability program; LA code enforcement; tenant organisations; local reporters | Houston: 3 senior + 12 inspectors, ~1,200 programmatic inspections/yr, 3,300-3,600 311 complaints/yr ([City overview, Mar 2026](https://cohips.houstontx.gov/council/committees/econdev/20260330-joint-hac/Overview-Apartment-Inspection-Ordinance.pdf)) **[search summary; PDF did not parse for me]**; UT Law 2018: programmatic inspections do not cover interiors, 28% of complexes lacked a certificate of occupancy ([UT Law](https://law.utexas.edu/wp-content/uploads/sites/11/2018/02/2018-02-ECDC-FactSheet-HoustonApartments.pdf)); high-risk ordinance passed May 2026 ([ABC13](https://abc13.com/post/houston-city-leaders-approve-upgraded-apartment-inspections-cracking-down-high-risk-rentals/19053650/)) | A+C (+B weak) |
| 4 | Patient cannot be discharged home, or equipment is ordered that does not fit, because nobody has measured the doorways and bathroom | Hospital discharge planners, occupational therapists, DME suppliers | OT home assessment requires in-person measurement of doorway widths, turning radii, bathroom; ~1 hour visit; 32 in (81.5 cm) minimum doorway ([carevo guide](https://carevo.com.au/blog/mobility-impairment-home-access-guide-assessors-equipment-installers), [BIDMC](https://bidmc.org/centers-and-departments/rehabilitation-services/inpatient-rehabilitation-services/inpatient-physical-therapy/physical-therapy-interventions/home-safety-assessment)) **[search summary; no US cost figure found]** | B+A (+C weak) |
| 5 | Landlords in LA County must keep rentals at or below 82°F from 2027; county and tenants have no list of buildings likely to fail | LA County Public Health, tenant groups, cooling contractors | Ordinance adopted Aug 2025, enforced from 1 Jan 2027 ([Planetizen](https://www.planetizen.com/news/2025/08/135759-la-county-adopts-maximum-indoor-temperature-ordinance-protect-renters-extreme), [county text](https://file.lacounty.gov/SDSInter/bos/supdocs/205511.pdf)). Applies to unincorporated areas and adopting cities; **City of LA not yet covered**, and the kit is City of LA only | A+B+C |
| 6 | Apartment Wi-Fi / bulk-internet providers need a design and quote per building before they can bid | Managed Wi-Fi operators, ISPs | Vendor model: design, survey and commissioning $34,400 on a 250-unit job (~$138/door); guidance says survey one unit of each type ([Purple](https://www.purple.ai/en-us/guides/managed-wifi-cost-per-door)) **[one vendor's model]** | A+B+C |
| 7 | Renters cannot charge EVs; charging companies and utilities must do a site walk per apartment building | EV charging installers, LADWP/CEC programme managers | UCLA Luskin: install cost in multi-unit buildings is variable and often high ([Luskin](https://innovation.luskin.ucla.edu/wp-content/uploads/2019/03/Overcoming_Barriers_to_EV_Charging_in_MUDs-A_South_Bay_Case_Study.pdf)); feasibility decided by site walk plus electrical capacity estimate ([Peninsula Clean Energy sample](https://www.peninsulacleanenergy.com/wp-content/uploads/2023/09/Sample-Charging-Evaluation-Report.pdf)) | A+C (+B weak) |
| 8 | Furniture and appliance deliveries fail because the item does not fit through the door | Big-and-bulky retailers, last-mile carriers, movers | Large furniture return costs $55-$108 to process; failed attempt can approach cost of original delivery ([vendor blog](https://ecommercefastlane.com/big-and-bulky-returns-pre-purchase-content/), [Bringg](https://www.bringg.com/resources/insights/big-and-bulky-delivery-insights-2026)) **[vendor estimates; no "won't fit" rate found]** | B+A (+C weak) |
| 9 | Lawyers need dated proof of when a roof or site defect began (notice) | Plaintiff and defence litigators, tenant attorneys, insurers | Courts have rejected unauthenticated Google Earth images for notice; insurers already use dated aerial images to deny claims ([HeplerBroom](https://www.heplerbroom.com/blog/illinois-courts-treatment-of-google-earth-images-as-admissible-evidence), [NBC CT](https://www.nbcconnecticut.com/investigations/nbc-ct-responds/eye-in-the-sky-how-a-connecticut-insurance-company-is-using-third-party-data-to-help-deny-claims/3717617/)) | C+A (+B weak) |
| 10 | B2B sellers want to know which companies are moving, growing or shrinking | Office-furniture, IT, telecom, staffing sales teams | **[unverified — no evidence gathered]**. Data: tenancy `fromDate` populated, employees partial, but no revenue, no NAICS | A (+C weak) |
| 11 | Rooftop solar / commercial HVAC replacement lead lists | Solar and HVAC contractors | **[unverified]**. Vexcel's own PDF lists solar potential as a single-layer idea | C+A |
| 12 | Film and TV location scouting in LA (interior look, ceiling height, truck parking) | Location managers | **[unverified — no evidence gathered]** | B+C+A |
| 13 | Janitorial / painting / flooring contractors must walk a space to bid | Commercial cleaning and trade contractors | **[unverified]**. Data: `areaFloor`, `areaWall`, bathroom counts | B+A |
| 14 | Robot and embodied-AI teams need real interiors with ground-truth geometry | Robotics labs | **[unverified as a paid pain]**; public scan datasets already exist, licence for sponsor data unknown | B |
| 15 | Flood exposure of ground-floor units (first-floor height vs ground) | Flood insurers, emergency managers | **[unverified]**. Data: DSM/DTM, `ground-elevation.value`; no finished-floor elevation | C+B+A |

---

## (b) Ranking (1-5, harsh)

| # | Problem | Realness / cost | Data fit | Why the data score |
|---|---|---|---|---|
| 1 | Fire pre-incident plans | 5 | 3.5 | All three layers carry weight. Floor plans on all sampled scans; DSM height verified; roof material, solar, skylights, AC counts per structure. Missing: hydrants, standpipes, alarm panel, shut-offs (none in any layer); `hasSprinklers` sparsely populated; scans are units and amenity rooms, not corridors and stairs |
| 2 | Insurance COPE verification | 4 | 3.5 | Construction fully populated, tenants on most properties, a meaningful number of scanned properties with a current food tenant, roof condition and defects per collection. Missing: wiring, plumbing, loss history, roof age; aerial-only version already sold by aerial vendors |
| 3 | Apartment inspection triage | 4.5 | 3 | Houston MF properties with roof defect history, vacancy, rents, class, sale conditions. Layer B is marketing scans of show units, so it says little about bad conditions |
| 5 | 82°F rule screening | 3.5 | 2 | Window openings on very few commercial sample models; amenity ids have no names so "has AC" is unknown; jurisdiction mismatch with the kit |
| 4 | Discharge / home access | 4 | 2.5 | Doorway widths exist but openings on only a minority of commercial sample models; the patient's own home is in the set only if they live in a scanned floor plan |
| 6 | Apartment Wi-Fi design | 3 | 3 | Wall graph with thickness, unit count, stories; wall material (attenuation) absent; corridors unscanned |
| 7 | EV charging siting | 3.5 | 2.5 | `parking[].totalSpaces` partly populated, cars and lot visible from air; electrical capacity absent, which is the deciding factor |
| 9 | Litigation timelines | 3 | 3 | Ortho collections 2016-2026 with capture dates in XMP; owner names sparse (buyer/seller names rarely present) |
| 8 | Delivery fit | 3 | 2.5 | Same opening coverage limit as #4; no elevator dimensions; elevators field sparse |
| 12 | Film locations | 2 **[unverified]** | 3 | Panos, ceiling heights, hardscape; mostly generic apartments |
| 10 | B2B move signals | 2.5 **[unverified]** | 2.5 | Employees partly populated, no revenue; aerial car counts untested as a signal |
| 11 | Solar / HVAC leads | 2.5 | 3 | Mostly single layer |
| 13 | Trade bids | 2 | 3 | Area fields good; property operations, not a new industry |
| 15 | Flood first-floor | 3 | 2 | No finished-floor elevation; DSM cannot see it |
| 14 | Robotics data | 2 | 2 | No semantic labels (`objectAnnotations` empty in the sampled models) |

---

## (c) Top 3 developed

### 1. Fire pre-incident plans for apartments, hotels and offices (my pick)

**The problem in the owner's words.** "We get toned out to a three-storey garden apartment complex at 2 a.m. I don't know which side the stairs are on, how the units are laid out, whether the roof is flat membrane with dozens of AC units and solar on it, whether my ladder reaches, or whether there is a restaurant on the ground floor. Nobody on my shift has walked it."

**What they do today and what it costs.**
- Crews walk buildings and fill pre-plan forms by hand, or the department buys pre-plan software and still walks. One district logged 1,484 crew hours for 1,019 commercial buildings (about 1.5 h each by my arithmetic) ([FlowMSP](https://flowmsp.com/?p=1464)) **[search summary]**.
- Coverage is poor: the 2017 Houston controller audit reported 526 of 5,000+ apartment buildings inspected by the fire department over two fiscal years (source above).
- Consequence when missing: NIOSH line-of-duty-death reports list lack of pre-incident planning as a contributing factor in multiple cases (New York F2021-10, Texas F2024-06, Georgia F2025-09) ([CDC stacks](https://stacks.cdc.gov/view/cdc/181997/cdc_181997_DS1.pdf), [CDC](https://www.cdc.gov/niosh/firefighters/programs/pdfs/f202509.pdf)) **[search summary; I did not read the full reports]**.
- Rooftop solar blocks vertical ventilation and stays energised ([Fire Engineering](https://www.fireengineering.com/firefighting/the-impact-of-solar-energy-on-firefighting/)).

**Fields that answer it.**

| Pre-plan item | Layer and field | Coverage |
|---|---|---|
| Occupancy type, units, storeys, year built | A: `propertyType`, `propertyApartment.totalNumUnits` (essentially all MF), `numStoriesAboveGrade` near-complete, `constructionEvents[]` | High |
| Construction | A: `buildingConstructionMaterial` | Fully populated; share of Unknown not measured |
| Sprinklers | A: `hasSprinklers`, `sprinklerType` | **Low** |
| Who is inside, special hazards | A: tenancies + company-detail `profile.industryType`, `numEmployees` (partial); food tenants on a number of scanned properties; `apartmentLifestyleType` (Senior, Student) | Most properties have a tenancy |
| Manager to call | A: `propertyManagementCompanyName`; listing `propertyContacts[]` | Names on a subset of listed properties; phone numbers are placeholders |
| Typical unit layout, bedroom positions, door widths | B: `assets.floorplans` (all sampled), `rooms.classifications`, `openings` | Layout always; classified rooms and openings on a minority of the commercial sample |
| Interior views for the crew | B: 4k panos, defurnished pairs | All sampled; 4k on most |
| True height vs ladder reach | C: `dsm/extract` minus `dtm/extract` | Verified at one site |
| Roof hazards | C: `roof-characteristics.material.class`, `shape.value`, `roof-objects.solar`, `skylight.count`, `ac-unit.count`, `roof-defects.*` | Per structure, per collection |
| Access, all four sides | C: four oblique directions, `hardscapes`, `parcel-tree-cover.percent`, ortho | All four in 2020-2026 collections |
| Water source of last resort | C: `pool.detected`, `pool.total-area` | Parcel level |

**What the combination adds.** Aerial gives the outside and the roof; the scan gives the inside layout a search crew needs; CoStar says what the building is and who is in it. The reasoning step is reconciling them: CoStar says 3 storeys, DSM says 15 m; CoStar says Multifamily, tenancy says a restaurant on the ground floor; Vexcel footprints differ by collection (by a wide margin for one building) and the system has to choose.

**What cannot be answered, and how much it hurts.**
- Hydrants, fire department connections, standpipes, alarm panels, gas and electric shut-offs, key boxes: absent from all three layers. Hydrants can come from city GIS **[unverified that both cities publish them]**. The rest still needs a walk. This hurts a lot: the output is a first draft that cuts the walk, not a replacement for it.
- Corridors and stairwells: most properties have a handful of scans of units and amenity rooms, not circulation. The plan gives "typical unit layout", not the building layout.
- Sprinklers at a low fill rate means the field is mostly "unknown".
- Scans may predate renovations.

**Real-world action.** A pre-plan sheet per property, with an "unverified — confirm on walk" list, sent to the station captain for the first-due area; properties ranked so the walk schedule starts with the worst gaps (tall, old, unknown sprinklers, solar roof, senior housing).

**Worked example (composite; the aerial and interior values are from two different verified test sites, not one property).**
- Aerial values are of the kind measured at a Houston high-rise test point: a primary structure roof well above aerial-ladder height (DSM minus ground), garage top deck much lower, roof membrane/flat, mid-range condition, many AC units, pools present, several structures on the parcel.
- Interior values are those of a Houston apartment scan in the kit: 2BR/2BA, a dozen or so classified rooms and openings, a mid-sized unit, a couple of dozen panos.
- The system would conclude for a property with these values: "High-rise, roof beyond aerial ladder reach **[general fire-service knowledge, not sourced here]**; interior attack via stairs. Roof is flat membrane with many AC units — heavy roof load, no vertical ventilation plan. Pool on site. Typical 2BR unit: bedrooms at positions shown on plan; narrowest door on the bedroom route to be read from `openings.width`. Sprinklers: not recorded — confirm on walk. Footprint differs across collections — newest collection used, flagged."

**Cheapest check that would kill it.** Take 50 Houston multifamily kit properties. Count (i) non-Unknown `buildingConstructionMaterial`, (ii) non-null `hasSprinklers`, (iii) at least one scan whose name or tags indicate a corridor, lobby or stair, (iv) a Vexcel parcel returned at the kit coordinate. Then hand one generated sheet to one company officer and ask if it would shorten a walk. If (i)-(iii) are mostly empty or the officer says no, drop it.

---

### 2. Insurance underwriting: checking what the application says against what is there

**The problem in the owner's words.** "The submission says frame construction, fully sprinklered, apartments only, roof replaced 2019. I have forty submissions this week and a survey budget for five. Which five?"

**What they do today and what it costs.**
- They order on-site loss-control surveys after binding (ICAT: within 30-60 days of coverage) ([ICAT](https://icat.com/content/dam/victor/icat/documents/brochures/ICAT-CommercialLossControlBrochure.pdf)); one vendor alone did 119,976 in 2025 (Davies, above). Per-survey price to insurers: **not found**.
- Leakage: Verisk's $4.5 billion over four years; a strip-mall unit labelled retail that was a restaurant is their own example (above) **[vendor figures]**.
- Market context: carriers leaving or restricting apartment business in Texas and California (CRC, above).

**Fields.**
- A: `buildingConstructionMaterial`, `hasSprinklers` (sparse), year built, storeys, `totalNumUnits`; tenancy roster with company industry (cooking exposure: a number of scanned properties with a current food tenant; `spaceUse` Retail tenancies on many properties); sale-comp `saleConditions[]` (deferred maintenance); `vacancyPercent`.
- B: panos of units, kitchens and amenity rooms for an underwriter to view; floor plans; ceiling heights; defurnished pairs. No object detection, so sprinkler heads, stoves and detectors need our own vision on panos.
- C: `roof-characteristics.condition`, `material.class`, `roof-defects.{tarp, missing-material, water-pooling, rust}` per collection since 2016; pool, sport court, playground, trampoline (liability); `defensible-space.zone1-4` (wildfire, LA); DSM height; neighbouring structures.

**What the combination adds.** Aerial roof scoring is already sold to insurers, so layer C alone is not new. The new part is occupancy from the tenant roster checked against the declared class, and an interior view without a visit.

**What cannot be answered.** Wiring, plumbing, heating age; loss runs; roof age (only condition); whether sprinklers exist (sparse field). The submission itself is not in the data, so the demo needs a made-up application to check against — that is a real weakness.

**Action.** A referral: quote as submitted / re-rate for restaurant occupancy / order a survey, with the conflicting evidence listed; plus a question list to the broker.

**Worked example.** Property A, a Los Angeles mixed-use property in the kit: the kit records it as a scanned property with several models and current food-service tenants on the premises. If insured as apartments only, the system flags a cooking occupancy on the premises, pulls the newest Vexcel roof condition and defect percentages for the parcel, compares storeys with DSM height, and recommends a survey. Roof values for this parcel have not been pulled, so no numbers are stated.

**Cheapest kill check.** Ask one commercial underwriter whether a restaurant tenant under apartments changes the rate class; and measure on 30 properties how often the newest and second-newest Vexcel collections disagree on roof condition by more than one point. If the roof score is that unstable, the output is noise.

---

### 3. Deciding which apartment complexes the city inspects first

**The problem in the owner's words.** "We have about fifteen inspectors and roughly 4,500 properties. The new ordinance acts only after ten citations. I want to know which complexes are going bad before the tenth complaint."

**What they do today.** A four-year programmatic cycle (~1,200 inspections a year) plus 3,300-3,600 complaint-driven requests a year; 311 logged 18,000 multifamily habitability complaints 2020-2024 ([Community Impact](https://communityimpact.com/houston/bellaire-meyerland-west-university/government/2025/05/29/a-proposed-ordinance-could-allow-houston-to-inspect-apartments-with-dangerous-housing-conditions/)) **[search summary]**. Programmatic inspections were reported in 2018 not to cover interiors (UT Law, above).

**Fields.**
- C: per-collection `roof-defects.tarp`, `missing-material`, `water-pooling`, `roof-characteristics.condition` from 2016 to 2026; Harvey 2017 collection; `pool` state; `vehicles.count`.
- A: `vacancyPercent`, rent per plan and `numUnitsAvailable`, `buildingClass`, year built, sale comps with `saleConditions[]` and sale dates (ownership turnover), `propertyManagementCompanyName` (group properties by operator).
- B: scan as a dated baseline of what the unit was marketed as; weak.
- Public join: Houston 311 service requests **[dataset availability and address quality unverified]**.

**What the combination adds.** A tarp that persists across three collections, plus rising vacancy, plus a recent sale flagged for deferred maintenance, plus complaints, is a stronger signal than any one of them. Grouping by management company turns one bad roof into a portfolio pattern.

**What cannot be answered.** Interior conditions that drive most complaints (mould, pests, no hot water) are invisible from the air and absent from marketing scans. The kit covers Houston multifamily properties which are those CoStar chose to scan — likely better-run than the worst complexes **[my inference]**. This selection bias is the main risk.

**Action.** A ranked inspection list with an evidence sheet per property, and a notice of inspection drafted for the top ones.

**Worked example.** No property-level roof history has been pulled for a kit apartment, so only the shape can be stated: "Community X, Class C, built 197x, vacancy above the kit median, roof tarp detected in 2022, 2023 and 2025 collections, sold in 2024 — rank high, inspect roof-adjacent top-floor units first."

**Cheapest kill check.** Join the Houston MF kit properties to public 311 habitability complaints by address. If fewer than a few dozen kit properties have any complaints, the kit does not contain the buildings the city cares about and the idea is dead.

---

## Pick

Problem 1, fire pre-incident plans. It is the only candidate where each layer supplies something the others cannot (occupancy, interior layout, roof and height), the cost of the gap is documented in fatality investigations and an audit, and the output goes to a named person who acts on it. Its honest ceiling is "a first draft that shortens the walk"; hydrants, standpipes and shut-offs are not in the data.
