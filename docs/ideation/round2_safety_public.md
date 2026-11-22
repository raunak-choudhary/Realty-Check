# Round 2 — Safety, hazard and the public sector

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Independent panel member. Sources read: internal capability notes on the CoStar kit, the Matterport API and the Vexcel API. Web search on 2026-11-13 for evidence. No other ideation memos were read.

Conventions:
- Layer A = CoStar kit, B = Matterport scans, C = Vexcel aerial.
- "[unverified]" = I did not find a source, or the data check has not been run.
- Coverage numbers are quoted from the notes; nothing here was computed by me.
- Web facts come from search-result summaries and one fetched article; I did not open every PDF. Where sources disagreed I say so.

One structural caveat applies to every idea below: **the kit is the set of properties CoStar scanned for marketing** (Apartments.com / LoopNet / Homes.com tours). It is not a census of buildings. It probably under-represents the worst-run and the subsidised stock, which is exactly the stock public agencies care most about. No note measures this bias. It is the first thing to check for any public-sector idea.

---

## (a) Candidate problems

| # | Problem | Who has it | Evidence it is real | Layers |
|---|---|---|---|---|
| 1 | "Worst first" apartment inspection queue: the city can only inspect a fraction of complexes and the new high-risk programme is triggered by citations it has not yet written | Houston Public Works Multi-Family Habitability Division; HFD; the new Apartment Standards Enforcement Committee | March 2026 city briefing: 12 inspectors + 3 seniors, ~1,200 programmatic inspections/yr, 3,300-3,600 311 complaints/yr, exterior and common areas only (https://cohips.houstontx.gov/council/committees/econdev/20260330-joint-hac/Overview-Apartment-Inspection-Ordinance.pdf). 4-year cycle goal for ~4,500 properties (https://pwehelp.houstontx.gov/council/committees/rna/2021_4_13/multifamily_habitability.pdf). High-risk programme passed May 2026, launched July 2026, trigger = 10+ citations in 6 months (https://www.click2houston.com/news/local/2026/07/31/houston-launches-high-risk-apartment-inspection-program-to-target-repeat-safety-violations/) | A + C (B marginal) |
| 2 | Pre-incident plans and access checks for garden-style apartment complexes | Houston Fire Department (operations + Fire Marshal), LAFD | NIOSH F2025-01: three Houston-area ladder-company members burned during primary search in a garden apartment, 7 Jan 2025 (https://www.cdc.gov/niosh/firefighters/programs/pdfs/f202501.pdf). 2006 Houston garden-apartment fire: 30 units lost, security gates hindered access (https://www.firehouse.com/home/news/10504414/on-the-job-a-texas-apartment-cockloft-fire-taxes-houston-firefighters-as-30-units-are-destroyed-in-fast-spreading-inferno). HFD lists blocked fire lanes, dead alarms/sprinklers and limited responder access as the common hazards (click2houston link above). ISO credits annual building familiarisation (https://www.isomitigation.com/newsletter/winter-2013/isos-fire-suppression-rating-schedule-reinvented-and-revised/) | A + B + C |
| 3 | Finding which apartment units can cheaply be made (or already are) accessible, under a court-supervised target | LA Housing Department Accessible Housing Program (AcHP); HUD | ILCSC v. City of LA settlement: 4,000 accessible units in 10 years; HUD VCA 2019: 4,031 units incl. 3,100 retrofits; 700+ covered projects; plaintiffs moved to enforce in 2019 for lack of progress; work still running in 2026 (https://archives.hud.gov/news/2019/pr19-116.cfm, https://cityclerk.lacity.org/onlinedocs/2024/24-0600_misc_pubc.pdf, https://www.disabilityrightsca.org/node/45, https://housing.lacity.gov/wp-content/uploads/2026/07/AcHP-ACCESSIBILITY-COMPLIANCE-INSPECTIONS-and-CERTIFICATION-GUIDELINES-7.2026.pdf) | A + B + C |
| 4 | Zone 0 / defensible-space compliance and AB 38 point-of-sale documentation | LAFD brush clearance unit; sellers in High/Very High fire zones; California FAIR Plan | AB 38 in force since July 2021 (https://www.glendaleca.gov/government/departments/fire-department/fire-prevention/vegetation-management-and-brush-abatement/ab-38-real-estate-disclosure). Board of Forestry approved Zone 0 rules Aug 2026, existing homes phased in (https://wildfiretaskforce.org/california-board-of-forestry-approves-first-in-the-nation-zone-0-defensible-space-regulations/, https://bbklaw.com/resources/la090926-california-board-of-forestry-adopts-emergency-zone-0-regulations-under-ab-3074). FAIR Plan 610,000 policies by June 2025, $1B assessment after the January 2025 fires (https://www.eenews.net/articles/california-leapfrogs-florida-in-us-insurance-risk/) | C + A (B only via the small set of drone/splat models) |
| 5 | Knowing which senior apartment communities will be dangerous in a multi-day outage | Houston Office of Emergency Management; Harris County | After Beryl, about 3 in 4 of ~38 area deaths were seniors, hyperthermia the main cause (https://www.texasstandard.org/stories/hurricane-beryl-deaths-houston-area-seniors-heat-centerpoint-outage/). Independent-living senior apartments have no special regulation; county backup-power mandate excludes them (https://houstonlanding.org/harris-county-unveils-backup-power-mandate-for-nursing-homes-assisted-living-facilities/, https://www.texastribune.org/2025/02/03/texas-seniors-assisted-living-nursing-homes-generators/) | A + C (B weak) |
| 6 | Which rental units cannot hold 82°F without added cooling | LA County Public Health (law, enforcement from Jan 2027, unincorporated areas); City of LA (motion Sept 2025, not law as far as I found) | https://www.planetizen.com/news/2025/08/135759-la-county-adopts-maximum-indoor-temperature-ordinance-protect-renters-extreme, https://spectrumnews1.com/ca/la/politics/2025/09/03/la-city-looks-to-establish-cooling-ordinance-for-rental-units | A + B + C |
| 7 | Apartment pool barriers (fence, gate, direct door access) | Houston Health Department (annual pool permits [unverified against ordinance text]); owners (liability) | 5-year-old drowned at a west Houston apartment pool, July 2025; enclosure rules summarised (https://www.click2houston.com/news/local/2025/07/25/texas-laws-around-apartment-complex-swimming-pools). Statute citations come from law-firm pages, not checked | A + B + C |
| 8 | Unpermitted conversions and bedrooms without emergency escape windows | LADBS code enforcement; LAFD | Deaths in converted garages (https://lafd.org/news/pacoima-garage-fire-kills-one-firefighters-rescue-another, https://abc7.com/post/pacoima-converted-garage-deadly-fire-woman-killed/14583109/). Enforcement fell sharply in 2020 (https://laist.com/news/housing-homelessness/tenants-feel-stranded-as-la-cuts-back-on-unpermitted-housing-enforcement-during-the-pandemic). No current backlog figure found | B + C + A |
| 9 | Soft-story retrofit stragglers | LADBS; owners; tenants | 12,000-14,000 buildings ordered; counts of non-compliant buildings I found are old (https://abc7.com/earthquake-retrofit-northridge-soft-story/5280732). Current number [unverified] | A + C |
| 10 | Post-storm damage counts and displaced-household estimates (Beryl, 2024 derecho, future storms) | Houston OEM; FEMA preliminary damage assessment teams; Texas windstorm pool | Substantial-damage process exists and is paperwork-heavy (https://www.houstonpermittingcenter.org/hpwfmo1036). No backlog figure found | C + A |
| 11 | Ground-floor apartment units exposed to flooding; substantial-damage and elevation evidence | Houston Floodplain Management Office; Harris County Flood Control | Same Houston source; elevation certificate or survey required to contest a determination. Cost per certificate [unverified] | C + A (B weak) |
| 12 | Solar / storage on affordable multifamily roofs | CPUC SOMAH administrator; LADWP; owners | SOMAH up to $100M/yr, storage added 2025 (https://www.cpuc.ca.gov/solar). LADWP territory appears not eligible [unverified], which removes most of the city of LA | C + A |
| 13 | Roof-leak-driven mould and habitability complaints | Houston Health Department; LA County Public Health | UT Law 2018: 2 inspectors citywide for interior health complaints (https://law.utexas.edu/wp-content/uploads/sites/11/2018/02/2018-02-ECDC-FactSheet-HoustonApartments.pdf). Dated | C + A + B |
| 14 | Non-ductile concrete retrofit inventory | LADBS; office/apartment owners | Not searched this round [unverified] | A + C |

---

## (b) Ranking

Scores 1-5. "Real" = how real and costly, weighted by the quality of evidence I actually found. "Fit" = how well the three layers answer it, harshly.

| # | Problem | Real | Fit | Why the fit score, and what is missing |
|---|---|---|---|---|
| 2 | Garden-apartment pre-incident plan + access check | 4 | 4 | Only idea where each layer supplies something the others cannot: A gives stories (near-complete), year built (partial), unit mix, `hasSprinklers` / `sprinklerType` / `buildingConstructionMaterial` (**fill rates not in the notes**); B gives unit floor plans (all sampled models), bedroom positions and door widths where Property Insights exists (a minority of the commercial sample; apartment units look better but unmeasured); C gives the site plan, 4 facades, roof shape/material/solar, DSM height, gates and lanes by eye. Missing: FDC, standpipe, alarm panel, Knox box, shut-offs, attic draft stops; which building a scanned unit sits in |
| 1 | Houston worst-first inspection queue | 5 | 3.5 | The kit holds only part of the roughly 4,000-4,500 complexes citywide. C carries the signal (roof condition 1-5, `roof-defects.*`, history to 2016, post-storm collections). A adds class, year, vacancy (partial), rents (a subset of Houston communities), sale conditions, manager name. B adds almost nothing: scans are staged marketing scans of model units. Selection bias is the main threat. Vexcel per-collection attributes are noisy (the same footprint can vary widely in area between collections) |
| 3 | LA accessible-unit screen (AcHP) | 4 | 3 | B door widths, room width/depth, sill/threshold `lowerElevation`; C ADA-symbol detection (worked in one test); A year built, stories, rent type, unit mix. Missing: clear width vs rough opening (door leaf and stops take ~5 cm), swing, thresholds on the exterior route, grab-bar blocking, kitchen/bath fixture clearances (no object detection). Unknown how many of the 700+ covered projects are in the kit |
| 4 | Wildfire Zone 0 / AB 38 | 5 | 3 | C is on target (`defensible-space.zone1-4-{building,tree}`, tree cover, roof material) but it is a one-layer answer and the sponsor's own suggestion. A adds the sale trigger and year built for the LA listings. B adds something only on the small set of drone/splat models. Number of kit properties inside a Very High zone [unverified] |
| 5 | Senior housing outage risk | 5 | 2.5 | A has a senior lifestyle flag (count not in notes) and stories. C generator detection is untested and `rooftop hvac unit` returned 0. B could size a community room. Thin |
| 7 | Apartment pool barriers | 3 | 3 | C `pool.detected`, `pool.types.*.enclosed.*`; B amenity scans include pools (gate and latch by own vision on panos); A unit mix as a proxy for children. Fence height and latch function are not measurable from the API |
| 8 | Unpermitted conversions / bedroom egress | 3.5 | 3 | B is complete on residential (rooms, windows on most sampled models, sill height); C footprint history; A bed count and sqft. LA listings are few; needs LADBS permit and assessor joins; C footprints are unstable between collections |
| 6 | 82°F cooling readiness | 3 | 2.5 | Not law in the City of LA as far as I found; kit excludes unincorporated county. C `ac-unit.count` is rooftop only; wall and window units need own vision |
| 10 | Post-storm damage and displacement | 4 | 2.5 | C does the work; A converts roofs into units and people. B absent |
| 11 | Flood exposure of ground-floor units | 4 | 2 | DTM gives ground, but finished-floor height above grade is not in any layer; unit-to-floor mapping unverified |
| 13 | Roof leak to mould | 3 | 2 | Scans are clean marketing units; no dated interior evidence |
| 9 | Soft-story stragglers | 3 | 2 | The city already has the inventory and status; layers add little |
| 12 | Multifamily solar | 2.5 | 2 | Programme eligibility likely excludes LADWP territory |
| 14 | Non-ductile concrete | 3 | 1.5 | Evidence not gathered; B and C add little |

---

## (c) Top 3 developed

### Top 1 (my pick) — Pre-incident plan and access check for garden apartments

**The problem in the owner's words.**
"We get dispatched to a 300-unit garden complex at 3 a.m. I need to know, before the engine stops: which gate, does it open, where do I lay in from, is the building sprinklered, is it one long attic, how tall is the eave, and when my truck company goes in for a search in a 2-bedroom unit, where are the bedrooms. Today I find out when I get there."

**What they do today and what it costs.**
- Pre-incident plans are built by fire companies walking each property and drawing it up. The standard (NFPA 1620, now inside NFPA 1660) and ISO's rating schedule expect this to be repeated annually for full credit (https://www.isomitigation.com/newsletter/winter-2013/isos-fire-suppression-rating-schedule-reinvented-and-revised/).
- I found no figure for HFD's or LAFD's coverage or hours per plan. **[unverified]** Fire-officer research papers describe plans that exist but are not useful or reachable for the first-due captain (https://apps.usfa.fema.gov/pdf/efop/efo46305.pdf).
- The cost of not having it is documented case by case: NIOSH F2025-01 (three members burned during primary search in a garden apartment, January 2025; cited factors were delayed water and rapidly changing conditions); the 2006 Houston cockloft fire where pedestrian security gates slowed access and 30 units burned.
- HFD's own description of what it finds at high-risk complexes: blocked fire lanes, broken alarms, non-working sprinklers, limited responder access.

**Fields, by layer.**

| Question on the plan | Layer and field | Coverage |
|---|---|---|
| Occupancy, size, age, storeys | A `propertyType`, `numStoriesAboveGrade`, `constructionEvents[]`, `grossBuildingAreaSquareFeet` | good |
| How many units and bedrooms (people to search for) | A `propertyApartment.models[].{numBeds,numUnits}` | good |
| Sprinklered? construction type? | A `hasSprinklers`, `sprinklerType`, `buildingConstructionMaterial` | **fill rate not in the notes** |
| Senior or student community | A `apartmentLifestyleType` / listing `lifestyleType` | count not in notes |
| On-site manager and after-hours contact | A occupancy tenancies of type OnSitePropertyManagement; `propertyManagementCompanyName`; phones are placeholders in the kit | names only |
| Unit layout per floor-plan type: entry, hallway, bedroom positions, travel distance | B `assets.floorplans` (all sampled), `rooms.classifications` (Bedroom, Bathroom, Hallway), wall graph | plans always; classified rooms on a minority of the commercial sample, all of the residential sample |
| Door and window sizes for entry, VES and rescue | B `openings{type,width,height,lowerElevation}` | a minority of the commercial sample; windows rarer |
| Ceiling height (smoke layer, hose stretch) | B `rooms.ceiling` | a minority of the commercial sample |
| Clubhouse, gym, leasing office interiors | B amenity/common-space scans | by name heuristic |
| Site plan: number of buildings, footprints, which sides are reachable | C `structure.count`, `structures[].footprint.wkt`, ortho at ~6.5 cm | parcel hit most test points; footprints unstable across collections |
| Gates, fire lanes, parked cars in lanes, dead-end drives | C ortho + `elements/detect` (`car` works) | by eye / own CV; `gate` label untested |
| Attic risk: roof shape and material | C `roof-characteristics.shape.value` (gable/hip/flat), `material.class` | present at test points |
| Roof hazards: solar, tarps, structural damage | C `roof-objects.solar.*`, `roof-defects.{tarp,structural-damage}` | present |
| Eave/roof height for ladder choice | C DSM minus DTM | verified at one site; precomputed eave height is null |
| All four facades: breezeways, stair towers, balconies | C `oriented/extract` north/south/east/west | all 4 directions, 2020-2026 |
| Water: hydrants | Public join: City of Houston hydrant layer (https://services.arcgis.com/NummVBqZSIJKUeVR/ArcGIS/rest/services/wHydrant/FeatureServer); pool as static source from C `pool.*` | public, approximate locations |

**What the combination adds.** A alone is a list of attributes with no geometry. C alone is the outside of a complex with no idea what is in it or how a unit is laid out. B alone is an interior with no location on the site. Together they give the three parts of a real pre-plan: what it is (A), how to get to it and around it (C), and what the crew meets behind the door (B). The disagreement checks are where reasoning is needed: A says 3 storeys but DSM says ~9 m or ~14 m; A says sprinklered but year built and type make it unlikely; C says 14 structures in one collection and 9 in another; the gate visible in 2026 imagery was not there in 2022.

**What cannot be answered, and how much it hurts.**
- Fire department connection, standpipes, alarm panel, Knox box, gas and electric shut-offs: not in any layer. This hurts; these are core plan items. The system must leave them as explicit blanks for the company to fill on a short visit. So it shortens the walk; it does not replace it.
- Which building a given unit number is in: scans tie to a floor-plan type, not to a position on the site. Model geolocation is missing on some commercial models and off by tens of metres on others. The plan can say "B2 units are laid out like this", not "unit 1412 is in building 14".
- Draft stops and fire walls in the attic: invisible. Roof shape only says an attic exists.
- Whether the sprinkler system works today: no.
- Scan date and whether the unit was since remodelled: not in the notes.

**Natural action.** (1) A pre-incident plan sheet per complex pushed to the first-due station for review, with blanks marked. (2) A referral to the Fire Marshal's office when aerial evidence shows an apparent access violation (HFD requires 20 ft gates with Knox entry and all parts of a building within 150 ft of an approved access route, per https://www.houstonpermittingcenter.org/sites/g/files/nwywnm431/files/2025-11/Session%201%20-%20Rm%20CD%20-%20Fire%20Access%20Compliance%20-%20HFD%20-.pdf).

**Worked example (structure is real; values marked "illustrative" are not measured).**
Property A, a Houston garden-style complex in the kit, Multifamily. A "2BR, 2BA" floor-plan scan with classified rooms and openings.
The system would conclude something of this form:
- "Garden-style, N storeys per CoStar; DSM eave height H m agrees / disagrees (illustrative). Year built Y. Sprinkler field: empty, so treat as unsprinklered until confirmed."
- "Vexcel 2026: K residential structures, gable roofs, shingle: assume common attic per building. Two vehicle gates on the main road; the east drive is a dead end longer than 150 ft (illustrative): refer to Fire Marshal."
- "2BR plan: entry opens to living room; hallway to the left; bedrooms at the rear, farthest point about D m from the door; narrowest door on the route W m (from `openings`). Bedroom windows: not detected in this scan, check on site."
- "Nearest hydrants from the city layer: two on the main road, none inside the complex (illustrative)."
- "Blanks for the company: FDC, alarm panel, Knox, shut-offs."

**Cheapest check that would kill it.** One pass over the kit's commercial-property records for Houston Multifamily: the non-null rate of `hasSprinklers`, `sprinklerType` and `buildingConstructionMaterial`. If all three are under ~30%, layer A contributes little beyond counts and the idea drops to a two-layer one. Second check, same script: the share of Houston MF properties with at least one scan that has classified rooms (run the room query on ~50 apartment-unit sids). If under ~50%, the "where are the bedrooms" claim only holds as a floor-plan image.

---

### Top 2 — Houston "worst first" apartment inspection queue

**The problem in the owner's words.**
"Council told us to go after the worst complexes first. The ordinance defines worst by citations already written. I have 12 inspectors for about 4,500 properties and I get to roughly 1,200 a year. Tenants in the worst places often do not call 311. I need to know where to send people before the citations exist."

**What they do today and what it costs.**
- Staffing and throughput: 12 inspectors, 3 senior inspectors; ~1,200 programmatic inspections a year; 3,300-3,600 311 complaints a year; inspections cover exteriors and common areas (March 2026 briefing, link in table). At that rate a full cycle is close to four years, which matches the stated 4-year goal.
- The 2018 UT Law study found more than 1,000 complexes without an active certificate of occupancy and too few inspectors for the stock (https://law.utexas.edu/wp-content/uploads/sites/11/2018/02/2018-02-ECDC-FactSheet-HoustonApartments.pdf). Dated, but the 2026 staffing numbers are of the same order.
- The high-risk programme (passed 6 May 2026, launched July 2026) designates a property after 10+ qualifying citations in six months, then requires registration, extra inspections and correction, with daily fines (amounts differ by source: $250-$2,000 or $250-$2,500) (https://communityimpact.com/heights-river-oaks-montrose/government/new-apartment-inspection-program-passes-in-houston-after-almost-a-year-of-discussion/).
- Dollar cost of the status quo to the city or tenants: not found. **[unverified]**

**Fields, by layer.**
- C, per property and per collection back to 2016: `roof-characteristics.condition` (1-5), `roof-defects.{tarp, missing-material, structural-damage, debris, patch, discoloration.water-pooling}.{detected,percent}`, `structure.count`, `vehicles.count`, `pool.*`; ortho and oblique crops as evidence; `oriented/query` lists event collections (a Harvey 2017 set exists at the test point; Beryl or derecho collections were **not checked**).
- A: `buildingClass`, `buildingRating`, year built, unit count, `vacancyPercent`, asking rents and `numUnitsAvailable`, `propertyManagementCompanyName`, sale comps with `saleConditions[]` and recent `soldDate`, `hasSprinklers` (fill unknown).
- B: only as the "as-marketed" interior and the unit layout for the inspector. Marginal. I will not pretend otherwise.
- Public joins: Houston 311 archive (2011-11 to 2024-04) and recent-requests layer (https://mycity2.houstontx.gov/pubgis01/rest/services/311/311_ARCHIVED_CASES/MapServer/0); the city's published high-risk list once it exists; HCAD ownership. No open multi-family violation dataset was found.

**What the combination adds.**
- C alone flags a bad roof. A says whether that roof sits over 40 units or 400, whether the complex is still advertising units at market rent under a tarp, whether it just changed hands or was sold with a distress condition, and who manages it.
- The manager roll-up is the piece neither the ordinance nor 311 gives: the same operator across several properties with the same deterioration pattern. The ordinance designates one property at a time.
- Conflicts the agent has to reason through: a tarp may be a re-roof in progress (check the next collection); blue detections may be a pool cover; a "condition 2" in one collection and "4" in the previous one may be a different footprint being scored; a Class A rating in CoStar with persistent defects from the air; low `vehicles.count` may mean vacancy or a weekday flight.

**What cannot be answered, and how much it hurts.**
- Interior conditions (no heat, sewage, mould, pests, wiring): none. The system ranks on exterior proxies. This is acceptable only because the city's programmatic inspections are themselves exterior-only; it does not help the health-code side.
- Whether roof decay actually predicts citations: untested. This is the whole premise.
- Selection bias: the kit holds marketed, scanned communities. The worst complexes may not be in it at all. This hurts most.
- Kit contacts are placeholders, so the notice cannot be addressed from the kit alone.

**Natural action.** A ranked inspection work list for the division, each entry with an evidence sheet (dated aerial crops, defect history, units affected, operator's other properties), and for the top entries a drafted notice of inspection or a referral to the Apartment Standards Enforcement Committee.

**Worked example (form only; values illustrative).**
"Community X, Houston, Class C, built 1970s, 240 units, managed by Operator Z (who manages 6 other kit properties). Vexcel: tarp detected on buildings 3 and 7 in the 2025 collection and still present in 2026; roof condition 4 in 2022, 2 in 2026; debris detected. CoStar: 12 units currently advertised from $850; vacancy 18%; sold 2023. 311: 9 habitability requests in the last archived year. Two of Operator Z's other properties show the same tarp persistence. Conclusion: schedule programmatic inspection this quarter; inspect Z's two other flagged properties in the same trip. Confidence reduced because the 2025 footprint for building 7 differs from 2026 by a factor of 3."

**Cheapest check that would kill it.** Take the complexes named in Houston news coverage of the ordinance debate (or the city's high-risk list once posted) and look them up in the kit's commercial-property records by address. If almost none are in the kit, the bias is fatal. If some are, pull `property/extract` for 30 of them and 30 random Houston MF properties and compare roof condition and defect flags. No separation means no signal.

---

### Top 3 — Accessible-unit screen for LA's Accessible Housing Program

**The problem in the owner's words.**
"We owe the court and HUD about 4,000 accessible units, 3,100 of them by retrofitting existing ones. Every candidate unit needs a surveyor on site before we know whether it is a $5,000 job or a gut. We also keep a registry so people with disabilities can find units, and it is only as good as the last survey."

**What they do today and what it costs.**
- Obligations: the 2016-17 class settlement (4,000 units in 10 years) and the 2019 HUD agreement (4,031 units; 3,100 retrofits; 15% of new and rehabilitated subsidised units) (https://archives.hud.gov/news/2019/pr19-116.cfm, https://www.hud.gov/sites/dfiles/Main/documents/Fact-Sheet-and-QA-HUD-City-of-Los-Angeles-VCA.pdf).
- Progress: plaintiffs moved to enforce in 2019; a 2023 monitor report expected the retrofit programme to run through 2025 at least; a 2024 city report expected units in process to finish by end of 2026; new inspection and certification guidelines were issued July 2026 (links in table).
- Method: on-site accessibility compliance inspections and certification by specialists. Cost per survey and per retrofit: not found. **[unverified]** The often-quoted $200M programme total was not confirmed by anything I found.

**Fields, by layer.**
- B: `openings{type,width,height,lowerElevation,relativeCenter}` for every doorway on the route entry → bedroom → bathroom → kitchen; the wall graph to build that route; `rooms.classifications`; `rooms.dimensionEstimates{width,depth}` for a 1.5 m turning circle in bathroom and kitchen; defurnished panos for a clear view of floor space; floor plan DXF for the retrofit drawing.
- A: year built (March 1991 is the Fair Housing Act design cut-off), `numStoriesAboveGrade` and elevator presence [field fill unverified], `apartmentRentType` to identify affordable stock [count unverified], unit mix and rents, scan-to-floor-plan link on `models[].attachments[]`.
- C: `elements/detect` "handicap parking symbol" (worked at one test lot), ortho for the route from accessible stalls to the entrance, obliques for steps at entrances.
- Public join: the city's covered-property registry (accesshousingla.org) to mark which kit properties are covered.

**What the combination adds.** B says whether the inside of a unit is close to compliant. C says whether a wheelchair user can get from a marked stall to the door. A says whether the building is covered or post-1991, has the unit type in volume (`numUnits` per plan, so one scan speaks for many units), and what it rents for. A unit that passes inside but sits up a flight of exterior steps is a false positive that only the combination catches.

**What cannot be answered, and how much it hurts.**
- Clear opening vs rough opening: the API width is the opening; a hung door loses several centimetres. Doorways in the sample cluster right at the 32-inch (0.813 m) clear-width line, so many doors will be "too close to call". This hurts: the output is a three-way screen (clearly passes / clearly fails / survey needed), not a certification.
- Fixtures: toilet and sink clearances, counter heights, grab-bar blocking, controls height. No object detection. A vision model on panos could attempt some; unproven.
- Thresholds and slopes on the exterior route: not measurable from ortho.
- Openings exist on a minority of the commercial sample; apartment-unit coverage is not measured.
- Whether covered (subsidised) projects are in the kit at all. If not, the screen still serves the registry and private post-1991 stock, but not the court target.

**Natural action.** A prioritised retrofit candidate list sent to AcHP ("units where every door on the route already exceeds the threshold by a margin and the bathroom fits a turning circle: survey these first"), each with a marked-up floor plan; and registry entries flagged "likely accessible, unverified" for the specialist to confirm.

**Worked example (form only; values illustrative).**
"LA community, built 2009, 5 storeys, 180 units. Plan A1 (1BR, 62 units): entry 0.91 m, bedroom 0.86 m, bathroom 0.76 m, bathroom 1.6 x 2.3 m. One door fails; room size allows a turning circle. Retrofit scope: one door widening per unit. Vexcel: 3 ADA symbols detected in the surface lot on the north side; oblique-south shows level entry at the north lobby. Plan B2: bathroom door 0.80 m, within noise of the line: send surveyor. Recommendation: A1 first, 62 units for one repeated scope."

**Cheapest check that would kill it.** Match the public covered-property list against the kit's commercial-property addresses. Then run the openings query on 50 LA apartment-unit sids from matched (or post-1991) properties. If fewer than half return doorways, or the matched count is near zero, drop it.

---

## Pick

**Top 1, the garden-apartment pre-incident plan and access check**, run in the order given by the Top 2 queue. Reasons:
- It is the only candidate where all three layers each supply something necessary and the gaps can be stated as explicit blanks.
- The owner (HFD) has a live programme launched July 2026 whose stated hazards are access, alarms and sprinklers.
- It ends in two concrete actions: a plan sheet to the first-due station and a Fire Marshal referral.

Its weakness is evidence of scale: I found incidents and standards, not a measured backlog. Top 2 has the best-documented pain but is a two-layer idea with a serious selection-bias risk.

Sources (all accessed 2026-11-13 via search): URLs are inline above.
