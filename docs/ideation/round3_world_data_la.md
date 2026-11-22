# Round 3 — outside-in: what Los Angeles open data unlocks

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Scope: City of Los Angeles / LA County / California, plus US federal data covering it. Written 2026-11-13/14.
Method: every dataset marked VERIFIED was loaded live (API call returning rows, or page fetched) during this session. No sponsor API calls were made. Overlap numbers marked **[computed]** come from a local test I ran: the LA commercial kit properties and CA home listings (kit lat/lon) were point-queried against the LA County parcel service to get an APN, then matched by APN to city datasets. Web search ran out of budget partway, so some "evidence" links are official pages I fetched directly and a few claims are marked UNVERIFIED.

## 0. Five findings that change the picture

1. **The kit already carries the join key.** `parcelNumbers[]` / `parcelReferences[].parcelNumber` is filled on nearly all kit commercial properties. The kit documentation does not mention it. The format for LA records is unverified (the sample record is Houston), so I tested the fallback instead: kit lat/lon → LA County parcel point query returned a parcel for **nearly all** LA commercial properties and CA homes **[computed]**. Either route gives an APN, and APN is the primary key of LAHD, LADBS and Assessor data.
2. **The Assessor roll is a free per-parcel API.** One call returns use, year built, units, bedrooms/baths, building sqft, 2026 land and improvement values and the Prop 13 base year. "No assessed values" is not a limit in LA.
3. **LAHD publishes building-level enforcement and eviction data keyed by APN.** Eviction notices filed with the city (332,780 rows, updated weekly) match **a majority** of LA multifamily kit properties; many have a 2026 notice **[computed]**. Complaint cases and investigation cases match a similar share; tenant buyouts and code violations match fewer.
4. **SB 721 balcony enforcement is live and visible in the data.** LAHD's inspectors began citing "EXTERIOR ELEVATED ELEMENTS INSPECTION" in January 2026 (3 cites) and have run at about 300 a month since March; 1,450 cites on 1,441 parcels, 759 still uncleared **[computed from dataset cr8f-uc4j]**.
5. **Some outside-in ideas die on overlap.** No kit properties or homes fall inside the Palisades damage-inspection area (none within 40 m of 12,137 DINS points) and only a handful of kit properties are on LAHD's affordable-housing project list **[computed]**. Fire-recovery and accessible-housing-programme ideas are not supported by the sponsor inventory.

Other overlap facts **[computed]**: many kit MF parcels are in the city's RSO (rent-stabilised) parcel layer; many of those with an Assessor year built are pre-1979; some MF parcels and homes sit in the city liquefaction layer; some MF parcels and homes sit in the city Very High Fire Hazard Severity Zone layer; Assessor base year is 2020–2023 on a meaningful number of MF, office and home parcels.

---

## 1. Inventory (37 datasets)

V = verified live this session. U = not verified (reason given). Join key: APN = Assessor parcel number (AIN), ADDR = street address, LL = lat/lon, TRACT/ZIP = area join.

### 1a. City of LA — buildings, housing, enforcement

| # | Dataset | URL | Contents | Join | Update | Access | Status |
|---|---|---|---|---|---|---|---|
| 1 | LADBS Building Permits Issued 2020–present (also 2010–19, pre-2010; separate electrical, mechanical, "submitted" sets) | data.lacity.org/resource/pi9x-tg5x (2010–19: dyxf-7hc4; pre-2010: e67z-kt2n; electrical ysqd-apz7; mechanical 67is-svtd) | Permit no., type/subtype, use, issue date, status, valuation, free-text `work_desc`, EV/solar flags | APN, ADDR, LL | Weekly (refreshed 2026-11-07) | Socrata API/CSV | V — 423,278 rows |
| 2 | LADBS Inspections | data.lacity.org/resource/9w5z-rg2h | Per-inspection type, date, result, permit no. | ADDR, LL, permit no. | Weekly | Socrata | V — 11.9 M rows |
| 3 | LADBS Certificates of Occupancy | data.lacity.org/resource/3f9m-afei | CofO no./date, permit, work description, floor area, stories, zone | APN (book/page/parcel), ADDR | Weekly | Socrata | V — 125,771 rows |
| 4 | LADBS Code Enforcement cases, open and closed | data.lacity.org/resource/u82d-eh7z, /rken-a55j | Case no., type (GENERAL, VEIP, PACE, CNAP…), opened/resolved dates | ADDR, PIN (city parcel id, not APN) | Weekly | Socrata | V — 28,772 open / 829,515 closed. No violation text |
| 5 | LADBS Soft-Story Compliance | data.lacity.org/resource/dqq4-799r | Order date, permit, step 1/2/3 compliance and tolling dates, CofC, finaled | ADDR only | Daily (2026-11-13) | Socrata (filtered view) | V — 12,380 rows |
| 6 | LADBS Non-Ductile Concrete list | LADBS retrofit programme pages | Buildings under Ord. 183893 (25-year programme) | ADDR | — | **No open dataset found.** LADBS page URL I tried returned 404; the list has circulated via records requests | U — treat as not available as open data |
| 7 | EBEWE energy & water benchmarking | data.lacity.org/resource/9yda-i4ya | Compliance status per year, floor area, site/source EUI, ENERGY STAR score, GHG, water use, year built | ADDR, building id (APN column is a fragment, unusable) | Weekly | Socrata | V — 96,151 rows; covers buildings ≥20,000 sq ft |
| 8 | LAHD Code Violations (SCEP + complaint) | data.lacity.org/resource/cr8f-uc4j | Violation type (40+ types incl. smoke detectors, dampness, stair/walk/deck, **exterior elevated elements inspection**), cited date, cleared flag, case type, unit count | APN, ADDR | ~Monthly–quarterly (last 2026-08-03); covers cites from 2025-11 | Socrata | V — 94,399 rows, 12,513 parcels |
| 9 | LAHD Eviction notices (Just Cause Ordinance filings) | data.lacity.org/resource/2u8b-eyuu | Notice date, notice type (3-day, 30-day, 60-day…), at-fault / no-fault | APN, ADDR | Weekly | Socrata | V — 332,780 rows, 33,572 parcels. No rent owed, no unit, no landlord name |
| 10 | LAHD Investigation & Enforcement cases | data.lacity.org/resource/eagk-wq48 | Case type (illegal eviction, unregistered unit, illegal rent increase…), filed/closed | APN, ADDR | ~Monthly | Socrata | V — 123,490 rows |
| 11 | LAHD CCRIS complaint cases | data.lacity.org/resource/ds2y-sb5t | Complaint counts, open complaints, scheduled inspections, dates | APN, ADDR | Weekly | Socrata | V — 326,248 rows |
| 12 | LAHD Tenant Buyout disclosures | data.lacity.org/resource/ci3m-f23k | Filing date, address, **compensation amount** | APN, ADDR | Weekly | Socrata | V — 8,916 rows |
| 13 | LAHD Landlord Declarations (Ellis Act and other no-fault filings) | data.lacity.org/resource/vpax-89xu | Case type: Notice of Intent to Withdraw (3,814), demolition/conversion clearance (3,040), landlord occupancy (2,671), government order… | APN, ADDR | Irregular (last 2026-01-07) | Socrata | V — 11,382 rows |
| 14 | LAHD Affordable Housing Projects 2003–present | data.lacity.org/resource/mymu-zi3s | Project, units, type, funding, developer, manager | APN, ADDR, LL | Monthly | Socrata | V — 616 rows |
| 15 | RSO parcel inventory | services5.arcgis.com/7nsPwEMP38bSkCjy/…/RSOs_20250115/FeatureServer/0 | One point per RSO address with `RSO_Units` | APN, ADDR, LL | Snapshot 2025-01-15 | ArcGIS REST | V — 167,954 points. ZIMAS (zimas.lacity.org) shows RSO status per parcel but is a lookup, not a download |
| 16 | REAP (rent escrow) properties | housing.lacity.gov …/rent-escrow-account-program-dashboard | Buildings in rent escrow | ADDR | — | Dashboard / per-property lookup | U — page exists; no bulk download found |
| 17 | Accessible Housing Programme registry | accesshousingla.org | Accessible/affordable unit listings | ADDR | — | Website search only | V page loads; **no bulk dataset** |
| 18 | MyLA311 service requests (yearly sets) | data.lacity.org/resource/h73f-gn57 (2025); others per year | Request type (bulky items, graffiti, illegal dumping, encampment…), dates, status | ADDR, LL | Last refresh 2026-10-12 | Socrata | V — 423,053 rows in the 2025 set. I did not find a separate 2026 set |
| 19 | Active businesses (Office of Finance) | data.lacity.org/resource/6rrh-rzua | Business name, DBA, address, **6-digit NAICS**, start date | ADDR, LL | Daily | Socrata | V — 632,799 rows. Fills the kit's missing NAICS |
| 20 | LAPD NIBRS offenses (and legacy Crime Data 2020–2024, 2nrs-mtv8) | data.lacity.org/resource/k7nn-b2ep | Offense, date, premise type, block-level address | LL (hundred-block) | Weekly (2026-11-10) | Socrata | V — 516,699 rows |
| 21 | LAFD response metrics | data.lacity.org/resource/n44u-wxe4 | Dispatch timestamps by first-in district | Station district only | 2026-02 | Socrata | V — 8.57 M rows. **No incident address; not joinable to a building** |
| 22 | LAFD brush clearance | vms3.lafd.org; zone polygon at maps.lacity.org/lahub/…/Special_Areas/MapServer/1 | Per-parcel inspection status (lookup), zone boundary (layer) | APN (lookup) / LL (zone) | Seasonal | Lookup site + ArcGIS layer | V page and layer exist; **inspection results are not bulk-downloadable** |
| 23 | City hazard layers: VHFHSZ, liquefaction | maps.lacity.org/lahub/rest/services/Special_Areas/MapServer/11; …/Geotechnical_and_Hydrological_Information/MapServer/5 | Zone polygons | LL point-in-polygon | Static | ArcGIS REST | V — ran a point query for every kit point, 0 errors |
| 24 | ED1 affordable-housing projects; LA28 venues | services5.arcgis.com/7nsPwEMP38bSkCjy/…/ED1projects; …/Unofficial_LA28_Olympic_Venues | 323 ED1 project points; 21 venue points ("unofficial") | LL | Snapshots | ArcGIS REST | V counts. TOC tier layer not found by search — U |
| 25 | LADWP programme data | data.lacity.org (r95y-gwez, 2yrw-q8tw…) | Outages, solar incentive | — | **Stale: last updated 2018–2019** | Socrata | V stale; no current building-level LADWP data found |
| 26 | LADOT traffic counts | data.lacity.org/resource/94wu-3ps3 | Intersection counts | LL | **Stale: 2017** | Socrata | V stale |

### 1b. LA County

| # | Dataset | URL | Contents | Join | Update | Access | Status |
|---|---|---|---|---|---|---|---|
| 27 | Assessor parcels + current roll | public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/0 | Situs address, use, year built, units, beds/baths, building sqft (up to 5 structures), **2026 land/improvement values, base years**, polygon | APN, LL (point-in-parcel), ADDR | Annual roll (Roll_Year 2026) | ArcGIS REST, no key | V — nearly all kit points returned a parcel. Also "Assessor Parcel Summary (Rolls 2006–present)" feature service on data.lacounty.gov (listed, not queried) |
| 28 | Environmental Health restaurant/market inspections and violations | data.lacounty.gov item 19b6607ac82c4512b10811870975dbdc (+ violations 5eaea9f8…) | Facility, address, score, grade, violations, 10/2023–9/2026 | ADDR, name | Quarterly (modified 2026-10-06) | CSV, 24 MB | V metadata |
| 29 | Environmental Health rental-housing habitability and housing routine/complaint inspections | data.lacounty.gov items 88a6faa8…, b5a695fe…, 1e797fec…, ef8667dc… | Inspections and violations | ADDR | Quarterly | CSV (333 KB) | V metadata. Small file; county programme covers mostly non-City-of-LA areas (U) |
| 30 | LARIAC rooftop albedo, tree canopy, impermeable surface, extreme-heat projections | image.gis.lacounty.gov/…/CSO_LARIAC7_BLD_ALBEDO/MapServer/0; Tree_Canopy_Coverage; Extreme Heat FeatureServers | Per-building roof albedo; tract canopy; heat days | LL / building polygon / TRACT | Periodic | ArcGIS REST | V service responds |
| 31 | Homelessness counts (LAHSA) | lahsa.org/data-refresh; county "Persons Experiencing Homelessness" service | Tract/CD-level counts | TRACT | Annual | Dashboard + ArcGIS | V page loads; tract file not downloaded |

### 1c. State and federal

| # | Dataset | URL | Contents | Join | Update | Access | Status |
|---|---|---|---|---|---|---|---|
| 32 | CAL FIRE DINS damage inspections | services1.arcgis.com/jUJYIo9tSA7EHvfZ/…/POSTFIRE_MASTER_DATA_SHARE/FeatureServer/0 | Per-structure damage class, structure type, attributes | LL, ADDR, APN | Per incident | ArcGIS REST | V — 12,137 Palisades points (6,845 destroyed) |
| 33 | CAL FIRE FHSZ | services.gis.ca.gov/arcgis/rest/services/Environment/Fire_Severity_Zones/MapServer | SRA and LRA zones | LL | **Service layers are 2007/2011 vintage**; the 2025 LRA update was not found in this service (OSFM page returned 403) | ArcGIS REST | V old layers; 2025 maps U |
| 34 | CGS seismic hazard zones (liquefaction, landslide, Alquist-Priolo) | gis.conservation.ca.gov/server/rest/services/CGS_Earthquake_Hazard_Zones | Zone polygons | LL | Static | **Token required (HTTP 499)** on the liquefaction service | Not openly queryable today. Use city layer #23 and USGS Qfaults (earthquake.usgs.gov/arcgis/rest/services/haz/Qfaults — V) |
| 35 | FEMA NFHL | hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28 | Flood zone at a point | LL | Continuous | ArcGIS REST | V — returned Zone X for the Hollywood test point |
| 36 | HACLA voucher payment standards | hacla.org/en/about-section-8/payment-standards | Max subsidy rent by ZIP tier (11 tiers) and bedroom count; effective 2026-09-01 | ZIP | When HUD SAFMRs change | PDF | V — e.g. 1BR ranges $1,793 (Tier 1) to $2,870 (Tier 11). HUD SAFMR page loads; the FY2026 xlsx link returned HTML to my client (U) |
| 37 | Other federal/state, briefly | — | — | — | — | — | — |
| | Census ACS / CBP API | api.census.gov | Tract demographics, ZIP business counts | TRACT/ZIP | Annual | **API now returns a "Missing Key" page without a (free) key** | V behaviour; data not pulled |
| | LEHD LODES | lehd.ces.census.gov/data/lodes/LODES8/ca/ | Jobs by block (workplace/residence) | Block | Annual | CSV | V directory lists |
| | HUD LIHTC and assisted multifamily | services.arcgis.com/VTyQ9soqVukalItT/…/LIHTC, …/MULTIFAMILY_PROPERTIES_ASSISTED | Subsidised property points | LL, ADDR | Annual | ArcGIS REST | V services respond. REAC scores file U |
| | CalEnviroScreen 4.0 | services1.arcgis.com/PCHfdHz4GlDNAhBb/…/CalEnviroScreen_4_0_Results_ | Tract pollution/vulnerability scores | TRACT | 2021 release | ArcGIS REST | V |
| | **EPA EJScreen** | epa.gov/ejscreen | — | — | — | **Gone: page returns 404 and the API host does not resolve.** Use CalEnviroScreen | V removed |
| | Caltrans AADT (state highways only) | gisdata-caltrans.opendata.arcgis.com | 2024 traffic volumes at count points | LL | Annual | ArcGIS | V listing. No city-street counts newer than 2017 exist as open data |
| | Metro GTFS | gitlab.com/LACMTA/gtfs_bus (and gtfs_rail) | Stops, routes, schedules | LL | Per service change (2026-02 latest note) | Git | V |
| | CA ABC licences | abc.ca.gov/licensing/licensing-reports | Licence type, status, premises address | ADDR | Daily/weekly reports | Report pages/downloads | V page; file not pulled |
| | SCAQMD facilities (FIND) | aqmd.gov/nav/FIND | Permitted facilities, notices of violation | ADDR | Continuous | Lookup tool, no bulk API found | V page only |
| | NOAA / NWS | api.weather.gov | Forecast grid, alerts at a point | LL | Live | REST | V |
| | OpenStreetMap | overpass-api.de | Building footprints; LA buildings carry `lacounty:ain`, height, units from the county import | LL, **APN** | Continuous | Overpass | V (needs a non-browser User-Agent; GET with a browser UA returned 406) |
| | SB 721 / SB 326 | Health & Safety Code §17973; Civil Code §5551 | Rules, not data: inspection of exterior elevated elements on 3+ unit buildings; first deadline 2026-01-01 for rentals (AB 2579), 2025-01-01 for condos | — | — | Statute (leginfo returned 403 to my client) | Deadline V via search results; **no public registry of who has complied** — the LAHD violation feed (#8) is the only compliance signal |

Not found as open data, stated plainly: SCEP inspection schedule per building; REAP list as a file; LAFD incident addresses; brush-clearance results; non-ductile concrete list; unit-level rents or rent registry; LADWP consumption per building; city-street traffic counts after 2017; school attendance boundaries (only campus points found).

---

## 2. Candidate problems (16)

Sponsor layers: **R** = CoStar record, **S** = Matterport scan, **A** = Vexcel aerial.

| # | Owner | Problem | Evidence it is real | Open data + sponsor | What the join gives that neither side has |
|---|---|---|---|---|---|
| 1 | Apartment owners, their lenders/buyers, LAHD inspectors | SB 721: which buildings have balconies/stairs/walkways that needed inspection by 2026-01-01, and which have no sign of compliance | LAHD cites: 1,450 since Jan 2026, 759 open (dataset #8) | #8, #1, #27 + A (count elements on four facades, staining/tarps over time), S (balcony doors per unit, panoramas onto decks), R (units, stories, construction material, manager) | Scope and priority per building before anyone climbs a ladder; the city only learns of non-compliance when an inspector happens to visit |
| 2 | Property owners who bought at the 2021–22 peak; tax agents | Assessed value above today's market value; appeal window closes 2026-11-30 | lacaab.lacounty.gov (deadline, AAB-100, $46 fee) | #27 + R (sale comps, cap rates, rents, vacancy), A (condition), S (interior quality for comp adjustment) | Roll value per parcel vs comp- and income-indicated value: the over-assessment in dollars, with the evidence packet |
| 3 | Voucher holders; HACLA | Finding a unit under the payment standard before the voucher expires; HACLA must then document rent reasonableness against comparable unassisted units | hacla.org payment standards; 24 CFR 982.507 (rent reasonableness). Local lease-up rate UNVERIFIED | #36, #8/#11 + R (asking rent per floor plan, availability), S (bedroom count, door widths), A (ADA stalls) | A list of actually available plans priced under the standard for that ZIP and bedroom size, with comparables attached |
| 4 | Home buyers, appraisers, lenders; Assessor | Floor area and bedrooms advertised vs permitted vs assessed disagree; unpermitted additions become the buyer's liability | LADBS issues a Residential Property Report at sale (ladbs.org page loads; contents UNVERIFIED); 450 permits since 2020 mention "legalize/unpermitted" (#1) | #27, #1, #3 + S (measured area and room count, full on homes), A (footprint/structure history 2016–2026), R (MLS sqft, beds, remarks) | Four independent measurements of the same house and a permit trail that explains the gap or does not |
| 5 | Tenant-defence lawyers (right-to-counsel triage), LAHD anti-harassment unit | Which buildings are being emptied: notice clusters after a sale, with buyouts and renovation permits | #9 (64,829 notices in 2026), #12, #13 | #9, #12, #13, #1, #15 + R (sale date, manager name, asking rents by plan, vacancy), S (renovated-unit scans), A (construction staging) | Notices per unit by management company and by months-since-sale; LAHD data has no owner, manager or rent |
| 6 | Sellers and buyers of homes in fire zones; insurers | AB 38 defensible-space documentation at sale; Zone 0 (0–5 ft) rules | Some kit homes are in the city VHFHSZ **[computed]**; AB 38 text UNVERIFIED this session | #23, #33, #22 + A (vegetation within 5/30/100 ft, roof material, history), R (active listings), S (window count/size) | A pre-listing compliance read for each for-sale home in the zone |
| 7 | Tenants and LA public health; landlords facing a cooling rule | Which rental buildings have no cooling | County indoor-temperature rule UNVERIFIED | #30, #1 (mechanical permits) + A (`roof-objects.ac-unit.count`, roof material), S (panoramas: wall/window units), R (units, year built) | Units per rooftop condenser and albedo per building; neither tax roll nor permit data says whether units are cooled |
| 8 | Owners of buildings ≥20,000 sq ft; LADBS | EBEWE non-compliance and audit/retro-commissioning scoping | #7 has NOT COMPLIED rows | #7 + R (GBA, tenants, year built), A (roof plant, solar), S (interior) | Which covered buildings are unregistered, and a first-pass audit scope |
| 9 | Buyers/lenders of older apartments | Seismic status: soft-story steps incomplete, liquefaction zone | #5 has step dates and tolling extensions into 2026 | #5, #23 + A (tuck-under parking on obliques), R (year built, comps) | Retrofit status priced into the deal; weak scan role |
| 10 | LAHD SCEP inspectors | Pre-inspection triage of a four-year inspection cycle | #8 violation mix | #8, #11 + S, A | Limited: scans are marketing units, not the units with dampness |
| 11 | Tenants offered a buyout | Is the offer fair against the rent gap to a comparable unit | #12 has compensation amounts | #12, #15, #36 + R (rent for the same bedroom count nearby), S (size) | Offer vs months of rent difference; needs the tenant's own rent |
| 12 | Assessor | New construction that escaped assessment | BOE guidance lists aerial imagery as a discovery source (boe.ca.gov new-construction page, via search) | #27, #1 + A (footprint change by collection), S (area) | Same join as #4 from the government side |
| 13 | Office tenants / brokers | Tenant industry and health of a building's roster | #19 gives NAICS and start dates | #19 + R (tenancies) | Real NAICS on kit tenants; closures from the "all businesses" set |
| 14 | Disabled renters; LAHD accessible-housing programme | Finding or certifying accessible units in covered developments | accesshousingla.org | #14, #17 + S (door widths), A (ADA stalls) | **Killed:** only a handful of kit properties on the LAHD list |
| 15 | Fire survivors; insurers; Assessor (calamity relief) | Proving pre-loss interior and contents | #32 | #32 + S (pre-fire scans), A (before/after) | **Killed:** no kit properties or homes in the damage area |
| 16 | Owners near LA28 venues | Event-period pressure (parking, permits, street works) | #24 | #24, #1 + R, A | Speculative; no owner with a stated cost yet |

---

## 3. Ranking

Realness = how costly and current the problem is. Fit = how much of the answer the data actually supplies on **both** sides (open and sponsor), scored harshly; a layer that only decorates does not count.

| # | Problem | Realness | Fit | Sum | Note |
|---|---|---|---|---|---|
| 2 | Assessment appeal packet | 5 | 4 | 9 | R and open data both fully verified; A and S are supporting evidence only |
| 3 | Voucher lease-up + rent reasonableness | 5 | 4 | 9 | R strong, S moderate, A thin; payment standards are a PDF |
| 1 | SB 721 scope and compliance | 4 | 4 | 8 | All three layers carry weight **if** balcony detection on obliques works (untested) |
| 4 | Area/permit reconciliation at sale | 4 | 4 | 8 | Best scan fit (homes have full geometry); small population |
| 5 | Eviction pressure / renoviction referral | 5 | 3 | 8 | Best open-data hit rate; sponsor side is R only |
| 6 | Fire-zone sale compliance | 4 | 3 | 7 | Some kit homes; current FHSZ maps not confirmed available |
| 12 | Escaped assessment | 3 | 4 | 7 | Same build as #4, different reader |
| 7 | Cooling | 3 | 3 | 6 | Wall units need our own vision |
| 9 | Seismic status in a deal | 4 | 2 | 6 | Address-only join; little for S |
| 13 | Tenant NAICS enrichment | 2 | 4 | 6 | A feature, not a problem |
| 11 | Buyout fairness | 4 | 2 | 6 | Needs data only the tenant has |
| 8 | EBEWE | 2 | 3 | 5 | Low stakes per building |
| 10 | SCEP triage | 3 | 2 | 5 | Scans are of the wrong units |
| 16 | LA28 | 2 | 2 | 4 | — |
| 14, 15 | Accessible programme; fire recovery | 4 | 1 | 5 | Killed on overlap |

---

## 4. Top four, developed

### 4.1 Assessment appeal packet (problem 2) — MY PICK

**Problem, as the owner would say it.** "I bought this building in 2022. My tax bill is still based on what I paid, and I could not sell it for that today. I have until November 30 to file and I need comps the Appeals Board will accept."

**Today and its cost.** In California a purchase resets assessed value to the price paid (the base year), then it rises by up to 2% a year. If market value on the January 1 lien date is lower, the owner can ask for a temporary reduction ("decline in value") by filing with the Assessment Appeals Board: form AAB-100 or online, $46 fee, window July 2 – November 30, 2026 (lacaab.lacounty.gov, fetched). Owners either assemble comps by hand or hire a tax agent, commonly on a share of the saving (share UNVERIFIED). The tax at stake is roughly 1.2% of any reduction per year (LA rate approximate, UNVERIFIED).

**Size in the kit [computed].** A meaningful number of LA multifamily, office and home parcels have a 2020–2023 land base year, i.e. were bought near the price peak.

**Open data.** Assessor parcel service (#27): `Roll_LandValue`, `Roll_ImpValue`, `Roll_LandBaseYear`, `Roll_ImpBaseYear`, `Units1`, `SQFTmain1`, `YearBuilt1`, `UseDescription`. LADBS permits (#1) to see whether new construction has been added to the base since purchase. LAHD #8/#9/#15 for facts that depress value (open violations, RSO status).
**Sponsor fields.** R: sale comps (`soldForPrice`, `soldDate`, `pricePerUnit`, `capitalizationRateActual`, `salePriceStatus`, `saleConditions[]`), the subject's own comp (the purchase that set the base year), apartment rents per plan, `vacancyPercent`, `buildingClass`, year built, units. A: `roof-characteristics.condition`, `roof-defects.*` by collection, obliques. S: panoramas of unit interiors to place the subject against comps on finish quality.

**Reasoning the agent must do.**
- Roll total vs three value indications that will disagree: comparable sales per unit, income approach (asking rents × units × (1 − vacancy) less an expense ratio, capitalised at the comp cap rate), and the subject's own trended purchase price. It has to say which it trusts and why.
- Comp admissibility: sales close to the lien date and not long after it (the 90-days-after rule in Revenue & Taxation Code §402.5 is from memory — UNVERIFIED); exclude non-arm's-length `saleConditions`; drop unconfirmed prices.
- Record conflicts: Assessor units and sqft vs CoStar units and GBA often differ; multi-parcel properties need their APNs summed (kit `parcelNumbers[]` is a list).
- Asking rent is not in-place rent, especially in RSO buildings (many kit MF parcels are in the RSO layer). The agent should discount or flag rather than capitalise asking rents blindly.
- Decide not to file when the indicated value is above the roll value — most parcels with pre-2020 base years.

**Action.** A filled AAB-100 (applicant's opinion of value, parcel, roll year) plus an evidence exhibit: comp grid, income worksheet, dated aerial and interior condition pages. Filed by the owner or agent before November 30.

**Worked example (public data only).** Property A, a mid-sized, older San Fernando Valley apartment parcel with a recent (2020–2023) base year (Assessor API, fetched). Dividing its 2026 roll land plus improvements by its unit count gives a roll value per unit. The agent pulls confirmed 2024–25 sales of San Fernando Valley communities of similar age and size from the kit, takes the median price per unit and cap rate, and runs the income check from the community's plan rents and vacancy. If comps indicate, say, a value 15% lower (illustrative, not measured), the packet claims a reduction of 15% of the roll value and the annual tax effect is about 1.2% of that reduction. If comps indicate more than the roll value per unit, the agent reports "do not file".

**Build (≈28 h, 2 engineers).** APN resolution and multi-parcel roll-up 3 h; roll fetch + candidate screen (base year, use) 2 h; comp selection with admissibility rules 5 h; income approach with RSO flag 4 h; reconciliation and file/don't-file decision with stated reasons 4 h; Vexcel condition exhibit 3 h; Matterport interior exhibit 2 h; AAB-100 fill + PDF packet 3 h; review UI 2 h. **Hardest part:** a value conclusion an appraiser would not laugh at — the comp adjustments and the asking-vs-in-place rent gap.

**Cheapest kill check (1 hour).** For the kit MF parcels with 2020–23 base years, compute roll value per unit and compare with the kit's median confirmed LA `pricePerUnit` for 2024–26 sales. If fewer than about 20 parcels sit more than 10% above comparable sales, there is nothing to appeal.

### 4.2 Voucher lease-up and rent-reasonableness packet (problem 3)

**Problem.** Voucher holder: "I have a limited number of days to find a landlord who will take this, and I don't know which listings are even under my limit." HACLA: every lease-up needs a documented finding that the rent is reasonable against comparable unassisted units (24 CFR 982.507).

**Today and its cost.** Holders search general listing sites, where rent is shown without the ZIP-specific cap; HACLA staff assemble comparables per request. Payment standards are published as a PDF of 11 ZIP tiers by bedroom size, effective 2026-09-01; 1BR ranges $1,793–$2,870 (hacla.org, fetched). Local success rates and search times: UNVERIFIED this session (the HUD study page returned no text).

**Open data.** #36 payment standards (PDF → table) and HACLA utility allowances (not fetched, U); LAHD #8, #11 (open violations and complaints predict a failed inspection); #15 RSO; #20 crime and #37 CalEnviroScreen for the holder's own filters.
**Sponsor fields.** R: `apartmentModels[].{numBeds,minRent,maxRent}`, `numUnitsAvailable`, `propertyManagementCompanyName`, postcode, year built, class; many LA communities carry rents. S: bedroom count from room classification (a "1BR" that scans as a studio changes the cap), door widths and step-free path where openings exist (some commercial scans), panoramas. A: ADA symbols in parking, exterior condition.

**Reasoning.** Gross rent = asking rent + utility allowance for tenant-paid utilities, compared with the cap for the bedroom size the voucher allows, not the unit's. A holder may pay above the cap only up to 40% of adjusted income at initial lease (rule from memory, UNVERIFIED). Advertised bedroom count vs scanned rooms. Comparable selection for the reasonableness finding: same submarket, bedroom count, age band, and unassisted. Placeholder rent values in the kit must be dropped.

**Action.** A Request for Tenancy Approval packet (HUD-52517) pre-filled for the chosen unit, with a three-comparable rent-reasonableness table, sent with the holder's application; plus a shortlist the caseworker can act on.

**Worked example.** Holder with a 1BR voucher wants Hollywood (90028/90038). The agent reads the tier for each ZIP, lists kit communities there with a 1BR plan where `minRent` + allowance ≤ cap and `numUnitsAvailable` > 0, removes any with open LAHD violations on the APN, confirms the plan scans as one bedroom, and prints the three nearest unassisted 1BR comparables with rent and size. Numbers are not filled in here because I did not read kit rents.

**Build.** Payment-standard and allowance tables 3 h; rent normalisation and filter 3 h; LAHD screen by APN 2 h; scan checks (bedrooms, door widths) 5 h; comparable selection 4 h; RFTA and comps PDF 4 h; chat intake and shortlist UI 4 h; aerial ADA check 3 h. **Hardest part:** utility-allowance logic and which utilities each property bills, which the kit may not state.

**Kill check (1 hour).** Count LA plans with rent at or under the payment standard for their ZIP and bedroom size. If almost none are, the product is a list of nothing; if almost all are, the filter adds little and only the packet has value.

### 4.3 SB 721 scope and compliance (problem 1)

**Problem.** Owner: "LAHD cited me for no balcony inspection report. What do I have on this building, how many need to be opened up, and who do I call?" Buyer or lender: "Has this building complied, and what is the exposure?"

**Today and its cost.** State law required a first inspection of exterior elevated elements (balconies, decks, stairs, walkways above 6 ft that rely on wood framing) on rental buildings of 3+ units by 2026-01-01, then every six years (deadline confirmed via search results; element definition and the 15%-sample rule are from memory — UNVERIFIED). There is no registry. LAHD now checks during its routine inspections: 1,450 cites since January 2026, 759 uncleared; some kit multifamily properties already cited **[computed]**. Owners get bids by walking an inspector around; price per element UNVERIFIED.

**Open data.** #8 (the cite, by APN), #1 permits (`work_desc` text: 3,818 permits since 2020 mention balconies, only 11 name SB 721), #27 (units ≥3, year built), #5 soft-story (same wood-frame vintage).
**Sponsor fields.** A: obliques in four directions, free-text detection on obliques for "balcony", "exterior staircase", "walkway"; collection history for staining, tarps, replaced decking; roof defect fields. S: exterior-facing door openings per unit scan and the panorama nearest each, looking onto the deck surface and rail base. R: `buildingConstructionMaterial` (filled; code meanings need the kit's enum), stories, units, year built, manager name, sale comps for buyers.

**Reasoning.** Is the building subject at all (units, framing, any element above 6 ft)? Counts will disagree: detection per facade double-counts corners; scans cover only some units; advertised plans with "balcony" in the name are a third count. Compliance evidence is indirect: no cite is not proof, a permit for "balcony repair" suggests an inspection happened, a cleared cite suggests a report was filed. The agent ranks buildings by exposure (element count × age × visible water staining) and states its confidence.

**Action.** For an owner: an inspection request-for-proposal with element counts per facade and marked-up obliques, plus a reply to the LAHD notice with the booked date. For LAHD or a lender: a ranked list of subject buildings with no compliance evidence.

**Worked example (public data).** Property B, a mid-sized, pre-1979 apartment building (Assessor). An LAHD routine inspection in 2026 cited "exterior elevated elements inspection", uncleared, alongside several other violation types (dataset #8). No LADBS permit since 2020 and no eviction notices on the APN. The aerial step would count balconies and exterior stairs on each facade from 2026 obliques and compare with 2020; the output is the RFP and the reply to LAHD. Whether this building is in the kit was not checked.

**Build.** Subject screen (Assessor + record) 2 h; LAHD and permit evidence by APN 3 h; oblique detection and de-duplication across facades 7 h; scan door/panorama check 4 h; history comparison 3 h; ranking and confidence 3 h; RFP and notice-reply drafting 3 h; UI 3 h. **Hardest part:** reliable element counts from obliques.

**Kill check (30 minutes).** Run `elements/detect` with "balcony" and "exterior staircase" on four obliques of three known balcony buildings. Earlier testing found that several labels returned no detections; if these do too, the aerial layer contributes only pictures and the idea drops to a compliance lookup.

### 4.4 Area and permit reconciliation at sale (problems 4 and 12)

**Problem.** Buyer: "The listing says four bedrooms and 2,400 sq ft. The county says three and 1,650. Which is legal?" Unpermitted space cannot be counted by an appraiser and can be ordered removed after closing.

**Today and its cost.** Buyers find out late, from the appraisal or from the city's property report at sale (LADBS Residential Property Report — page loads, contents UNVERIFIED), and renegotiate or walk. 450 LADBS permits since 2020 are explicitly to legalise prior work.

**Open data.** #27 (`SQFTmain1..5`, `Bedrooms1`, `Bathrooms1`, `YearBuilt1`, `EffectiveYear1`), #1 permits across all three eras, #3 certificates of occupancy (floor area, stories).
**Sponsor fields.** S: room areas and classifications, wall graph, ceiling heights — complete on residential models. A: structure footprints per collection 2016–2026, structure count, DSM height. R: MLS `sqftMin`, `bedsMin`, `bathsMin`, `yearBuilt`, `remarks` ("bonus room", "ADU", "converted garage").

**Reasoning.** Four area figures measure different things: scan net room area, Assessor living area, MLS figure of unknown source, aerial footprint × storeys including garage. The agent must convert before comparing and set a tolerance. Footprints can differ between collections, so growth must be confirmed on imagery. A gap matters only if no permit or CofO explains it; permit text is free-form and addresses include units.

**Action.** A one-page discrepancy report for the buyer's agent with a drafted request to the seller for permits covering the named rooms, and the LADBS records request. From the Assessor's side the same output is a referral for review.

**Worked example.** Not populated: needs kit MLS and scan values. Population **[computed]**: the kit's CA homes with a parcel, mostly single-family; a minority have at least one permit since 2020; a few have a permit mentioning a balcony or deck.

**Build.** Parcel and permit history per home 4 h; scan area roll-up with garage/exterior exclusion 4 h; aerial footprint history with image confirmation 6 h; unit conversion and tolerance calibration 4 h; permit-text matching to rooms 4 h; report and request drafts 3 h; UI 3 h. **Hardest part:** calibrating scan area against Assessor area so that flags are rare and right.

**Kill check (1 hour).** For 50 homes compare scan area, MLS sqft and Assessor `SQFTmain1`. If the three agree within 10% on nearly all, there is nothing to find; if they scatter randomly, the measures are not comparable.

---

## 5. Pick

**4.1, the assessment appeal packet.** It is the only one of the four where every load-bearing input was verified today (roll values by API, base years on kit multifamily parcels, comps with LA prices), it ends in a real filing with a deadline 16 days out, and the result is a dollar figure. Its weakness is that aerial and scan are exhibits, not inputs. If the 30-minute detection test in 4.3 passes, SB 721 is the better use of all three layers and has the freshest enforcement evidence; I would run that test before committing.

## 6. Limits of this document

- Overlap counts use a point-in-parcel join from kit coordinates; multi-parcel properties are matched on one parcel only, so hit rates are lower bounds.
- I did not read kit rents, comps or scans, so no worked example contains a sponsor value.
- Statute details for SB 721, AB 38, §402.5 and the voucher 40% rule are from memory where marked.
- LAHD violation data starts at 2025-11; older history is not in the open file.
