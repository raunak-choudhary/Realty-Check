# Round 2 — problems owned by OCCUPANTS (renters, buyers, small tenants, placement caseworkers)

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Independent panel member. Sources read: our internal capability notes and notes on the CoStar kit, the Matterport API and the Vexcel API, plus web search. No API calls made. Layer A = CoStar kit, B = Matterport, C = Vexcel.

Conventions: "[unverified]" = I could not confirm it from a primary source or from our notes. Coverage numbers are quoted from the notes. Nothing here is a measured result of a new probe.

Three data facts shape every score below:

- Door/window/wall-graph data ("Property Insights") is on all sampled residential models but only a minority of commercial ones (doorways fewer still, **windows very rare**). Apartment units live in the commercial folder. Coverage on apartment units specifically is unmeasured.
- No source detects objects inside a scan (no grab bars, smoke alarms, AC units, appliances, elevators). Anything of that kind needs our own vision on panoramas.
- A scan is tied to a floor plan or a model unit, not necessarily to the exact unit a person will be handed. Any per-unit claim is really a per-floor-plan claim.

---

## (a) Candidate problems (16)

| # | Who has it | Problem in one line | Evidence it is real | Layers |
|---|---|---|---|---|
| 1 | Wheelchair/walker users, and the caseworkers, discharge planners and relocation staff who place them | Cannot tell from a listing whether they can physically get in the door, down the hall and into the bathroom; "accessible" filters are self-reported | HUD analysis of the 2011 AHS: under 1% of US units are wheelchair-usable, under 4% "livable" for moderate mobility difficulty (https://www.huduser.gov/PORTAL/sites/default/files/pdf/accessibility-america-housingStock.pdf ; https://nlihc.org/resource/scarcity-accessible-housing-aging-population). Disability is the largest basis of fair-housing complaints: 59.4% of HUD filings in FY2017 (https://www.hud.gov/sites/dfiles/FHEO/images/FHEO_Annual_Report_2017-508c.pdf) | A+B+C |
| 2 | Renters moving to Houston, esp. into ground-floor units; relocation staff choosing for them | Do not know whether the unit sits where water stood in 2017, and landlord disclosure only covers what the landlord "knows" for the last 5 years | Harvey apartment damage estimates ranged from 8,956 units in an early incomplete survey to "as many as 43,000" (https://www.bdcnetwork.com/hurricane-harvey-damaged-fewer-apartments-greater-houston-estimated). Texas Prop. Code 92.0135 disclosure duty and tenant termination right (https://codes.findlaw.com/tx/property-code/prop-sect-92-0135/). Renters policies exclude flood (https://tdi.texas.gov/blog/texas-law-encourages-renters-to-buy-flood-coverage.html) | A+C (+B thin) + public flood data |
| 3 | Housing Choice Voucher holders in LA and their housing navigators | Voucher clock runs out while they chase units that are over the payment standard or the wrong bedroom size | HACLA success rate 63% for people leaving homelessness, 2016-2020 issuances (https://www.hiltonfoundation.org/wp-content/uploads/2022/07/Abt_Voucher-Report_FINAL_7.8.22.pdf). Unused vouchers in LA (https://abc7.com/post/section-8-housing-city-of-los-angeles-hacla-public/13240363/). HACLA sets payment standards by ZIP (https://homeless.lacounty.gov/section-8-payment-standards/) | A+B (+C light) + HUD SAFMR |
| 4 | Long-distance renters signing sight-unseen (job relocations, students, travel nurses) | The scan and the advertised square feet may not describe the unit they get, and nothing shows what is outside the window | 37-41% of renters say they are likely to rent sight-unseen (https://www.apartments.com/grow/learning-center/renter-search-survey-q2-2025); 61% of recent movers report a regret, cost and noise first (2017, https://ycharts.com/news/story/PRN-PH14887-20171013) | A+B+C |
| 5 | Older home buyers / adult children buying for a parent (aging in place) | Need single-level living, a step-free entry and a usable bathroom; listings say "one story" and nothing else | Same HUD/JCHS accessibility evidence as #1 (https://jchs.harvard.edu/sites/default/files/research/files/harvard_jchs_housing_stock_accessibility_scheckler_2022_0.pdf) | A+B+C |
| 6 | Childcare operators looking for licensable space | State rules fix capacity by measured usable indoor and outdoor area; operators sign leases then find capacity is lower than the business plan | Texas: 30 sq ft indoor per child (https://regulations.justia.com/states/texas/title-26/part-1/chapter-746/subchapter-t/division-1/section-746-4201). California: 35 sq ft indoor, 75 sq ft outdoor (https://regulations.justia.com/states/california/title-22/division-12/chapter-1/article-7/section-101238-3 ; https://regulations.justia.com/states/california/title-22/division-12/chapter-1/article-7/section-101238-2) | A+B+C |
| 7 | LA home buyers in or near hillside areas | Cannot tell before making an offer whether the house is insurable outside the FAIR Plan | FAIR Plan residential policies 242,440 (Sep 2021) to 642,010 (Sep 2025); LA County 154,765 (https://www.moneygeek.com/insurance/homeowners/california-wildfire-fair-plan-insurer-retreat/) | A+C |
| 8 | Tenant organisations and legal-aid lawyers | Need dated, third-party evidence that a building has been neglected for years (tarps, roof defects) to support a habitability complaint | [unverified — no source searched]; LA REAP and Houston habitability enforcement exist | A+C (B = marketing scans, weak) |
| 9 | Small businesses / startups leasing an office suite | Pay rent on rentable SF and cannot tell how much is usable, or whether the layout fits their headcount, without paying for a test fit | [unverified — no source searched] | A+B |
| 10 | Elderly and medically fragile renters, Houston | Top-floor units under dark roofs with little tree cover and unknown cooling | [unverified — no source searched]; Texas has no general statewide AC requirement [unverified] | A+C (B needs own vision) |
| 11 | Families with asthmatic children, LA | Bedroom windows that face a freeway at short range | [unverified — no source searched] | A+B+C (windows very rare on commercial scans) |
| 12 | Parents of toddlers choosing an apartment community | Whether the pool is actually enclosed | Vexcel exposes `pool.types.*.enclosed.*`; drowning-risk evidence not searched [unverified] | A+C (+B amenity scans) |
| 13 | People moving large or medical furniture (hospital bed, power chair, piano) | Will it get through the doors and fit | [unverified]; low cost when wrong | B (+A) |
| 14 | LA renters in pre-1978 tuck-under-parking buildings | Is the building soft-story and has it been retrofitted | LA retrofit ordinance exists; public permit data on data.lacity.org [unverified] | A+C + public |
| 15 | Employers, universities, hospitals block-booking housing for staff/students | How many units of the right size are actually available near a workplace, and are they what the photos show | [unverified] | A (+B light) |
| 16 | Refugee resettlement caseworkers, Houston | Must secure housing that meets bedroom/occupancy standards before a family arrives | [unverified]; current arrival volumes are low [unverified] | A+B |

---

## (b) Ranking (1-5; data fit scored harshly)

| # | Problem | Realness / cost | Data fit | What is missing |
|---|---|---|---|---|
| 1 | Accessible-unit verification (apartments + homes) | 5 | 3 (apartments) / 4 (homes) | Doorways on a minority of commercial sample models; no swing, clear width, threshold height flag, grab bars or elevator field for multifamily; scan = floor plan, not the exact unit. Homes: Property Insights on all sampled, but few rentals among the home listings |
| 3 | Voucher pre-screen, LA | 5 | 3 | Rents exist per floor plan (LA communities in the kit, though `minRent` is 0 on many kit-wide) but most inspection failure items (GFCI, smoke alarms) cannot be seen; utility allowances not in the kit; no flag for whether a landlord has leased to voucher holders |
| 2 | Houston ground-floor flood exposure | 4 | 3 | Harvey imagery verified at one test point only; Matterport contributes little (unit floor level is not a clean field); needs public depth/floodplain data to be trustworthy |
| 4 | Sight-unseen listing vs reality | 3 | 4 | Scan area is net room area (in one sampled 2BR model the scanned area was noticeably below the advertised SF), so a tolerance must be calibrated; noise, smell, management quality invisible; no strong end action |
| 5 | Aging-in-place home purchase | 4 | 4 | Small pool (limited home listings, few in CA); no Houston sold prices; essentially a subset of #1 |
| 6 | Childcare licensable capacity | 4 | 2 | Only a handful of DayCare properties; few listings carry a suite scan; commercial rooms come back Void/Other; "usable" area exclusions (halls, kitchens, bathrooms) need a room taxonomy the classifier lacks; fencing not detectable by endpoint |
| 7 | Wildfire insurability, LA buyers | 5 | 2 | Few CA listings, city of LA only; Matterport idle; insurer underwriting rules not public |
| 8 | Tenant-organisation neglect evidence | 4 | 3 | Per-collection roof attributes are noisy (the same footprint can vary widely between collections); interior scans are marketing units, not the neglected ones |
| 12 | Pool enclosure for families | 3 | 3 | Enclosure field untested by us |
| 11 | Freeway-facing bedroom windows | 3 | 2 | Windows very rare on commercial models |
| 9 | Office usable vs rentable SF | 3 | 2 | Few listings with suite tours; office Property Insights weak |
| 10 | Heat exposure | 4 | 2 | No interior cooling data |
| 14 | Soft-story | 3 | 2 | Matterport idle; depends on a public dataset doing the work |
| 15 | Block housing for employers | 3 | 3 | Mostly single-layer |
| 16 | Refugee placement | 3 | 3 | Same mechanics as #3 with a smaller current population |
| 13 | Furniture fit | 2 | 3 | Single-layer, low stakes |

Top 3 developed below: **#1, #3, #2**. (#4 has the best raw data fit but the weakest pain and no natural action; #5 is folded into #1.)

---

## (c) Top 3 developed

### Top 1 — "Can I actually get into this home?" Accessibility verification for people with mobility impairments

**In the owner's words.** "I use a wheelchair. Every listing site has an 'accessible' checkbox that the leasing office ticks. I call, they say 'yes, it's accessible', I travel there, and the bathroom door is too narrow for my chair. I cannot afford to sign a twelve-month lease on a unit I cannot use, and I cannot visit thirty communities." The same sentence is said by hospital discharge planners, independent-living-centre housing staff and corporate relocation staff placing an employee with a disability.

**What they do today and what it costs.**
- Phone each community and ask; visit in person with a tape measure. No sourced figure for hours per search [unverified].
- Supply is the core cost: under 1% of units wheelchair-usable, under 4% livable (HUD, 2011 AHS; links in table). So almost every candidate is a "no", and each "no" currently costs a call or a trip.
- When it goes wrong the remedies are a reasonable-modification request (tenant usually pays in private housing [unverified]) or a fair-housing complaint; disability is the largest complaint basis (59.4% of HUD filings FY2017; a 2026 trade summary reports 54.6% for NFHA data, year unclear [unverified]: https://www.thehabitatgroup.com/articles/9729-report-annual-housing-discrimination-complaints-near-record-high).
- There is a legal yardstick that makes the measurement actionable: multifamily buildings of 4+ units first occupied after March 13, 1991 must have "usable doors" of nominal 32-inch clear width, an accessible route, and usable kitchens and bathrooms; in non-elevator buildings only ground-floor units are covered (https://www.huduser.gov/publications/pdf/fairhousing/fairch3.pdf ; https://www.hud.gov/sites/dfiles/FHEO/documents/The-Fair-Housing-Act-Requirement-3-Usable-Doors-Participant-Workbook.pdf). HUD guidance notes a standard 32-inch door leaf does not give 32 inches clear.

**Fields, by layer.**
- A (CoStar): `constructionEvents[]` eventType 2 (year built) and `numStoriesAboveGrade` decide whether the 1991 rule applies; `propertyApartment.models[].{numBeds,minSquareFeet,attachments[].videoKey}` and `units[].attachments[]` tie a scan to a floor plan; apartment-listing `apartmentModels[].{minRent,maxRent,numUnitsAvailable}` gives price and availability; `residentialProfile.parkingPolicies[]`; `propertyManagementCompanyName` for who receives the letter; `lifestyleType` Senior flag. Homes: `rentMin/rentMax`, `currentPrice`, features `sections[]`/`highlights[]` text.
- B (Matterport): `floors.edges.openings{type,width,height,lowerElevation,relativeCenter}` for every doorway; wall graph to build the entry → bedroom → bathroom route and take the narrowest opening on it; `rooms.classifications` (Bathroom, Bedroom, Hallway, Staircase); room `dimensionEstimates.width/depth` to test a 1.5 m turning circle in the bathroom and hallway widths; `lowerElevation` and floor `sequence` for steps and level changes; 4k panoramas at the narrow door for a second look; defurnished view to see clear floor.
- C (Vexcel): `elements/detect` "handicap parking symbol" (found correctly on a test lot); ortho for the path from accessible stall to the building entrance; DSM minus DTM along that path for grade and for building height versus `numStoriesAboveGrade` (a 3+ storey building with no visible elevator overrun on the roof is a question to ask); obliques of the entrance for steps.

**What the combination adds.** A alone says "built 2004, 3 storeys, 2BR at a given rent". B alone says "narrowest doorway on the bathroom route is X m". C alone says "ADA stalls here, entrance there". Only together do you get the statement that matters: *this available floor plan, in a building the 1991 rule covers, has a measured route from an accessible parking stall to the bathroom whose narrowest point is X, and the rent is Y.* The year-built field turns a measurement into a legal claim; the aerial turns a unit measurement into an arrival route.

**What cannot be answered, and how much it hurts.**
- Clear width versus opening width. The API measures the wall opening. Sample doorway widths cluster around the threshold; 32 inches is 0.813 m. **Many sampled doorways sit close to the threshold**, so most doors will be "ambiguous" unless measurement error is small. This hurts a lot; it forces three bands (clear pass, clear fail, verify) and an honest "verify on site" bucket.
- Coverage: doorways on a minority of commercial sample models. Apartment units specifically unmeasured. If it is 40%, the tool silently covers under half of communities. Hurts a lot for apartments; not at all for homes (all sampled).
- Elevator: no multifamily elevator field in the notes; office has one. An upper-floor unit in a walk-up is a hard fail the data may miss. Partly recoverable from Staircase rooms in common-area scans and from roof overruns, both by own vision.
- Grab bars, roll-in showers, counter heights, door hardware, thresholds: no object detection. Hurts moderately; these are modifiable, door widths and steps are not.
- Scan is of the plan, not the exact unit; ground-floor versus upper-floor instance unknown.
- It must never state "ADA/FHA compliant". It states measurements and which rule would apply.

**Natural action at the end.** (i) A ranked shortlist with the measured route for each, sent to the person or their caseworker; (ii) for each "verify" unit, a drafted question to the named management company asking for the clear width of two specific doors; (iii) where a post-1991 covered unit measures clearly below the rule, a drafted reasonable-modification request citing the measurement, or the facts section of a HUD complaint. Contact emails in the kit are placeholders, so sending is simulated.

**Worked example (what the system would conclude; values not from a new probe).** Property A: a 2BR, 2BA floor plan at a Houston apartment community in the kit, with a scan that has classified rooms and doorway openings. The system would: read year built and storeys from A; if first occupancy is after March 1991 and the plan exists on the ground floor or the building has an elevator, mark the rule as applicable; build the route entry → hallway → primary bathroom from the wall graph; report the narrowest doorway. If that doorway reads, say, 0.71 m, the conclusion is "bathroom doorway fails by about 10 cm at the wall opening; clear width will be smaller; not usable without modification; rule applies / does not apply because built in YYYY". It would then check C for marked accessible stalls on the parcel and the grade from stall to entrance, and write: "Reject for independent wheelchair use; if you still want it, here is the modification request." Year built, the actual narrowest width and the stall count for this property were **not** looked up by me.

**Cheapest check that would kill it.** One script, about 100 Matterport queries: pull `floors.edges.openings` for 100 apartment-unit sids (50 Houston, 50 LA, random). Kill if doorways are present on fewer than about 30% of units, or if two scans of the same floor plan disagree on the same door by more than about 3 cm (because then the 0.81 m threshold cannot be resolved). A second five-minute check: check the kit's commercial-property fields for any elevator field populated on Multifamily.

---

### Top 2 — "Will my voucher run out before I find a unit that qualifies?" Voucher pre-screen for LA navigators

**In the owner's words.** A housing navigator: "My client has a voucher and a deadline. I spend my week calling buildings whose rent turns out to be over the payment standard for that ZIP, or whose 'two-bedroom' the housing authority will not count as two bedrooms. Every dead end costs days we do not have."

**What they do today and what it costs.**
- Search listing sites by hand, compare each rent to the housing authority's ZIP-level schedule, call, tour, submit a Request for Tenancy Approval, wait for inspection.
- Success is far from certain: 63% at HACLA for people leaving homelessness (2016-2020 issuances, Abt/Hilton report); national metro average 69% in HUD's 2000 study (https://www.huduser.gov/Publications/pdf/sec8success.pdf). LA's waitlist drew more than 200,000 applicants (ABC7). A lost voucher is years of subsidy lost.
- Failed initial inspections delay subsidy start until deficiencies are fixed (https://www.hud.gov/sites/dfiles/PIH/documents/HCV_LLGuidebook_Inspections_FULL_chapter.pdf). I found no failure-rate figure [unverified].
- California bars source-of-income discrimination [unverified — not searched]; Texas does not, so this is an LA idea only.

**Fields, by layer.**
- A: apartment-listing `apartmentModels[].{numBeds,numBaths,minRent,maxRent,numUnitsAvailable}` on LA communities; `primaryAddress.postcode` for the ZIP tier; `propertyManagementCompanyName`; `buildingClass`, year built; property `constructionEvents[]`.
- Public join: HUD Small Area FMRs and HACLA's ZIP payment-standard schedule (a summary line gives a 1BR figure of $2,289 effective Aug 2025, tier not stated [unverified]).
- B: `rooms.classifications` Bedroom count versus advertised `numBeds`; room area per bedroom; window openings per bedroom where present; panoramas of kitchen and bath for a vision pass on obvious condition items; scanned area versus advertised SF.
- C: `roof-characteristics.condition`, `roof-defects.{tarp,missing-material,structural-damage}` on the newest collection as an exterior-condition warning; history to see whether a tarp has been there for years.

**What the combination adds.** A plus the public schedule gives "rent is under the standard"; B says "and the bedrooms are real rooms of plausible size"; C says "and the building is not visibly failing from outside". A navigator currently discovers the second and third at the tour or at inspection, after the clock has run.

**What cannot be answered, and how much it hurts.**
- The common inspection failures are small fixtures (GFCI, smoke/CO alarms, water-heater relief valves). None is in any layer. Hurts a lot: the pre-screen can rule out, not rule in.
- Utility allowance and rent-reasonableness determinations are the housing authority's; the kit has no utilities data. Hurts moderately (gross rent is what is tested).
- Bedroom windows: very rare on commercial sample models. The "is the second bedroom a windowless den" test will mostly be unavailable.
- Kit communities are those advertised with 3D scans; kit LA median rents are high for both 1BR and 2BR. If few plans fall under the standard, the shortlist is nearly empty.
- Whether a landlord has leased to voucher holders: absent.

**Natural action.** A pre-filled Request for Tenancy Approval packet for the best two or three units and a message to the management company; plus a note to the client explaining why each rejected unit was rejected.

**Worked example.** A client with a 1-bedroom voucher looking in a given LA ZIP. The system lists every kit floor plan in that ZIP and adjacent ZIPs with `numBeds` = 1, `numUnitsAvailable` > 0 and `minRent` at or below the ZIP's standard; with the kit median above a standard near $2,289 [unverified tier], it would report that most kit one-bedrooms are over the line and name the few that are not. For each survivor it reads the scan: one classified Bedroom of N m², bathroom and kitchen present, scanned area within tolerance of the advertised SF; then C: roof condition score and no tarp in the newest collection. Output: "Three plans qualify on rent; one has a roof tarp visible since 2023, deprioritise; submit packets for the other two."

**Cheapest check that would kill it.** Download HACLA's current schedule, join to LA `apartmentModels` on ZIP and beds, and count plans with `minRent` > 0 at or under the standard and `numUnitsAvailable` > 0. If the count is under roughly 30 plans citywide, the kit simply does not contain the housing this population can use, and the idea is dead regardless of the other layers.

---

### Top 3 — "Did this ground-floor apartment sit in water?" Flood exposure for people moving to Houston

**In the owner's words.** "I'm moving to Houston for work and signing from another state. The ground-floor unit is cheaper. The lease has a flood paragraph that says the landlord 'is not aware' of flooding in the last five years. Harvey was nine years ago and the building has changed hands. I want to know what actually happened here before I put everything I own on that floor."

**What they do today and what it costs.**
- Rely on the lease notice. Texas Prop. Code 92.0135 requires a written notice of floodplain status and of flood damage the landlord knows of in the previous five years (five-year detail from secondary sources; statute text not read by me [unverified]: https://www.greenresidential.com/the-2026-flood-rulebook-for-texas-landlords-a-stage-by-stage-guide-for-houston-and-austin-rentals/). If the landlord violated the section and the tenant suffers substantial loss, the tenant may terminate (FindLaw link in table). A 2017 flood is outside the window; a new owner may truthfully "not know".
- Look at a FEMA map, which shows modelled floodplain, not what happened.
- Cost of being wrong: contents. Standard renters policies exclude flood; an NFIP contents-only policy covers up to $100,000 and is quoted from about $100 a year (https://fema.gov/fr/print/txt/node/330749 ; https://insurify.com/renters-insurance/coverage/flood/). About 85% of Harris County was uninsured for flood at Harvey, owners and renters together (https://victorsteffen.com/article/when-disaster-strikes-national-flood-insurance-program-in-texas/ — weak source [unverified]).
- Scale: 8,956 apartment units in an early incomplete survey; analysts' range up to 43,000 (BDC link). No ground-floor breakdown found.

**Fields, by layer.**
- A: Houston multifamily properties with `primaryAddress` lat/lon, year built, `numStoriesAboveGrade`, `renovations[]` (sparse), floor plans, per-plan rents and availability; sale comps on kit properties with `soldDate` and `saleConditions[]`, giving ownership changes since 2017 (which is why "landlord knows" is weak).
- C: `oriented/query` returned a named storm event collection for Harvey 2017 at the one Houston point tested; `ortho/collections` back to 2016 to see before/after (debris piles, tarps, gutted ground floors, replaced roofs); `dtm/extract` bare-earth elevation at each building versus the nearest channel; `structures[].ground-elevation.value`; DSM for whether ground-floor parking podiums lift the lowest living floor.
- B: unit scans show whether the lowest living floor is at grade or raised (entry `lowerElevation`, stairs up to the door in common-area scans, `geocoordinates.altitude` against DTM); panoramas of ground-floor units and amenity spaces. This layer is thin here.
- Public joins: FEMA National Flood Hazard Layer; FEMA 3 m Harvey depth raster and USGS/HCFCD high-water marks (https://www.hydroshare.org/resource/165e2c3e335d40949dbf501c97827837/ ; https://hydroshare.org/resource/615d426f70cc4346875c725b4b8fdc59/); FEMA building-point damage assessments (https://disasters-geoplatform.hub.arcgis.com/pages/historical-damage-assessment-database).

**What the combination adds.** Public layers say "modelled depth here was D". Vexcel says "and the August/September 2017 image of this building shows water or kerbside debris, and the ground at building 7 is lower than at building 2". CoStar says "and the property sold in 2019, so the current owner's knowledge is second-hand; the available plan is a ground-floor one-bedroom". The conflict between a clean lease notice and physical evidence is the point.

**What cannot be answered, and how much it hurts.**
- Harvey imagery coverage is verified at one point (a single Houston test location). Hurts a lot until checked.
- Interior water height in a specific unit: not observable. Aerial evidence is of the site.
- Which floor the available unit is on: not a clean kit field in the notes. Hurts moderately; the advice becomes "ask for floor 2 or above in buildings X and Y".
- Mitigation since 2017 (drainage works, raised equipment) is invisible.
- Matterport's contribution is small; honestly this is an A + C + public-data idea, and it works only in Houston.

**Natural action.** A drafted written question to the management company asking specifically about 2017 and any event since, referencing the statute's notice; a recommendation to take an upper-floor instance of the same plan with the rent difference stated from A; and an NFIP contents quote request if the person takes the ground floor anyway.

**Worked example.** A Houston garden-style community (2-3 storeys, built before 2017) near a bayou, with a ground-floor one-bedroom available. The system finds the public depth raster shows water at the parcel; pulls the 2017 Harvey collection and the next ortho collection and compares; reads DTM at each building footprint and finds the buildings nearest the channel sit lower than those at the street; finds a sale comp dated after 2017; reads the lease-notice logic. Conclusion: "Site was inundated in 2017 on public and aerial evidence; current owner bought afterwards, so a 'not aware in last five years' notice is consistent with the law and tells you nothing about 2017. Buildings A-C are the low ones. Ask for the same plan on floor 2, or in building F; if you take ground floor, insure contents." No specific property was checked by me.

**Cheapest check that would kill it.** Call `oriented/query` at 20 Houston multifamily kit coordinates and count how many return the 2017 Harvey collection; then intersect all Houston multifamily kit points with the FEMA Harvey depth raster. Kill if fewer than about 30 kit communities are both inside the inundation extent and have 2017 imagery.

---

## Pick

**#1, accessibility verification.** It has the hardest evidence of need, the only case where the interior scan carries a measurement nobody else publishes, a legal rule that depends on a CoStar field (year built) to give the measurement consequence, and an arrival-route role for the aerial layer. Its risk is concentrated in one testable question (doorway coverage and repeatability on apartment units), and the residential-homes subset works even if the apartment answer is bad.
