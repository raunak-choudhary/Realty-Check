# Perspective: public-interest outsider (societal need)

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Inputs read: the team's capability notes and the event briefing, plus web search on 2026-11-13. No other idea files were read.
Labels: **[src]** = sourced by URL. **[CAP]** = from the team's capability notes. **[unverified]** = untested assumption. **[computed]** = my own arithmetic.

---

## (a) Reasoning chain (short)

1. The data is mostly apartments. Most kit properties are Multifamily, and most linked scans are MF **[CAP]**. So the people outside real estate who matter most here are **renters and the services around them**: tenant organisers, health and heat programmes, fire/EMS and disaster caseworkers. Retail, hotels and industrial are too thin to build on.
2. Two Houston laws passed in summer 2026 create pressure right now, on exactly the building type the kit is dense in:
   - **Right to Air Conditioning ordinance**, passed 12-2 on Aug 19, 2026, with 120 days to comply **[src]** https://texashousers.org/2026/08/25/houston-right-to-ac-ordinance-passed/ . Aug 19 + 120 days is about Dec 17, 2026 **[computed]**. The legal effective date is **[unverified]**.
   - **High-Risk Apartment Inspection Program**: 10 or more qualifying code violations in 6 months triggers registration, extra inspections and fines. HFD is the lead voice **[src]** https://www.click2houston.com/news/local/2026/07/31/houston-launches-high-risk-apartment-inspection-program-to-target-repeat-safety-violations/
3. LA has heat pressure too, but it is weaker for this data:
   - LA County's 82°F maximum indoor temperature rule starts Jan 1, 2027, but only in **unincorporated** areas **[src]** https://www.foxweather.com/lifestyle/la-county-mandates-maximum-indoor-temperatures-for-rentals-starting-in-2027 .
   - The kit covers only the City of LA **[CAP]**, and the city has only asked for a report on adopting the rule (Feb 2026) **[src]** https://www.saje.net/l-a-city-gets-one-step-closer-to-protecting-renters-from-extreme-indoor-heat/ .
   - So **Houston is the stronger stage**. LA is the "second job on the same harness".
4. **What each layer contributes.** CoStar says what a building *claims* to be (year built, class, stories, floor plans, rents, availability, schools). Vexcel shows what the building *looks like from outside*: facades, roof equipment, heights and history. Matterport shows what it *is inside*: windows, rooms, ceiling heights and panoramas. Every idea below sets these three against each other.
5. **Where the external action can go.** Kit contact emails and phones are placeholder contacts **[CAP]**, so no action may target a landlord or broker from the kit. Actions go to the consulted organisation instead: its shared sheet, inbox, calendar or Slack.
6. **The outside-expert consult.** The team is in Princeton and the data is Houston/LA. The honest bridge is a remote call or DM with the Houston organisation, plus an in-person talk with a Princeton group that does the **same job**: tenant organising, EMS, or disaster casework.

---

## (b) Raw candidates (12)

| # | Candidate (one line) | Verdict |
|---|---|---|
| 1 | **Right-to-AC canvass targeter.** Ranks Houston complexes by likelihood that units lack working AC, so tenant organisers knock the right doors before the ~Dec 17 compliance date | **KEEP (Idea 1)** |
| 2 | **Responder premise packet.** A one-page pre-incident plan for large apartment complexes: real heights per building, access, pools, typical unit layout and rescue windows | **KEEP (Idea 2)** |
| 3 | **Fire-displaced household rehousing.** A Red Cross caseworker gets a shortlist of nearby vacant units that fit the family, keep the kids' school and are not themselves hazards | **KEEP (Idea 3)** |
| 4 | Top-floor / west-facing heat-vulnerability triage for health-department wellness checks | Merged into #1. Health departments know *people*, not units, so building-level ranking is the same engine |
| 5 | Zone 0 (5-ft ember-resistant zone) audit for LA homes using splats and drone photos | Killed. Sources conflict on the existing-home compliance date (Feb 2027 vs phased 5-yr) **[src]** https://bbklaw.com/resources/la090926-california-board-of-forestry-adopts-emergency-zone-0-regulations-under-ab-3074 ; only a small number of CA home listings **[CAP]** and their share in fire zones is unknown; no Princeton counterpart to consult |
| 6 | Family-childcare home capacity pre-check: indoor SF per child from scan rooms, outdoor play area and pool hazard from Vexcel | Killed for now. Licensing offices and CCR&Rs are closed on weekends, so the consult is hard, and it partially overlaps the excluded yard finder. Best backup |
| 7 | Refugee-resettlement apartment match (bedroom egress, occupancy, rent) | Killed. Resettlement volume in 2026 is reportedly very low **[unverified]**, and it is the same engine as #3 with a weaker consult |
| 8 | Apartment clubhouses as outage cooling rooms or resilience hubs (post-Beryl) | Killed. There is no backup-power or outage data, and the natural action target (property managers) has placeholder contacts |
| 9 | Weatherization pre-audit packet (envelope, windows, roof) | Killed. Insulation and air leakage are invisible in every layer, NIR is absent **[CAP]**, and the local NJ weatherization nonprofit does not operate in Houston/LA |
| 10 | Lead-hazard pre-screen of pre-1978 housing | Killed. Lead is not visible, so it is only a year-built text filter, which fails the spatial bar |
| 11 | Mold/flood repair-request letters for legal aid | Killed. The evidence would come from the tenant, not the sponsor data |
| 12 | Post-hurricane damage triage for relief groups (Harvey collection) | Killed. Too close to the excluded insurer inspection and portfolio condition monitor |

---

## (c) Best 3 ideas

### Idea 1: Right-to-AC canvass targeter (Houston)

**Pitch.** An agent that tells a Houston tenant organiser which apartment complexes most likely have units without working AC. It shows the visual evidence for each pick and writes the canvass turf straight into the organiser's tracker.

**User and the decision.**
- The user is a tenant-union or community organiser: a Houston tenants union, a housing nonprofit, or a community organising group.
- The ordinance gives owners 120 days, and enforcement depends on tenants calling 311 **[src]** https://spectrumlocalnews.com/tx/austin/news/2026/08/22/houston-passes-new-ac-requirement-for-rental-housing- .
- Organisers have a few volunteer weekends before about Dec 17 **[computed]** and must decide **which complexes to door-knock first** to tell tenants their new right.
- Today this is done from 311 history and word of mouth. In June 2023 there were 184 AC calls, and at least 87 complexes had more than 10 complaints **[src]** https://houstonlanding.org/heat-broken-air-conditioning-drive-seasonal-surge-in-calls-to-houstons-311-system/ .

**Current pressure.**
- Ordinance passed Aug 19, 2026 **[src]** https://texashousers.org/2026/08/25/houston-right-to-ac-ordinance-passed/ .
- Before it, the "window screen exemption" let owners skip cooling **[src]** https://communityimpact.com/houston/heights-river-oaks-montrose/government/2026/08/19/houston-now-requires-air-conditioning-to-be-installed-in-all-rental-units/ .
- Renters were still reporting dead AC in July 2026 **[src]** https://www.click2houston.com/news/local/2026/07/30/houston-renters-say-broken-air-conditioners-leave-them-struggling-through-dangerous-summer-heat/ .

**Data layers and what only the combination gives.**
- **CoStar** (prior): `constructionEvents` year built, `buildingClass`, `numStoriesAboveGrade`, `apartmentModels[].minRent`, `numUnitsAvailable`, `vacancyPercent`, `propertyManagementCompanyName`, kit lat/lon. Houston has the densest MF and rent-community coverage in the kit **[CAP]**.
- **Vexcel** (exterior evidence):
  - `property/extract` `roof-objects.ac-unit.count` **[CAP field]**.
  - Oblique facades in 4 directions, with SAM3 free-text detection of "window air conditioner" on obliques and "air conditioner condenser" on ortho **[unverified labels]**.
  - Roof `material.class`/condition and `parcel-tree-cover.percent` as heat-load context.
  - History back to 2016 to see whether window units appeared or disappeared.
- **Matterport** (interior evidence):
  - Run our own vision model on skybox pano faces to look for wall/window units, ceiling supply registers and thermostats. There is no object detection in the API **[CAP]**.
  - `openings` of type window (width/height) say whether a window unit can even fit.
  - `rooms.dimensions.areaFloor` sizes a portable unit for the know-your-rights sheet.
- **Why the combination matters:**
  - CoStar alone says "old and cheap", which is a weak proxy.
  - Vexcel alone sees window units but cannot tell supplementing from replacing central air.
  - Matterport alone sees one unit at one date.
  - Together they give a per-complex **evidence-graded** call: "likely no central AC", "central AC present", or "unknown, knock".

**Visible reasoning moment.**
1. **H1 (CoStar):** Complex X was built before 1975, is Class C, and has a low 1BR rent, so it is flagged as a likely no-central-AC complex.
2. **Test (Vexcel):** The newest roof has `ac-unit.count` 0, but the oblique-north view (south facade) shows a row of ground condenser pads, and SAM3 finds no window units.
3. **Conflict:** The prior says no AC, but the exterior says central. The agent pulls the Matterport pano of a unit at X and its vision model sees a ceiling supply register and a wall thermostat.
4. **Then it checks the dates:** the scan date versus Vexcel history shows the condensers appeared after the 2019 collection. The building was retrofitted.
5. **Revision:** X drops to "central AC present (retrofit ≥2020)". Complex Y, 1.2 km away, rises: window units appear on facades in 2023 and 2026 obliques, and there is no scan. Y is labelled "evidence: aerial only, door-knock needed."
6. **Forced verification:** every "likely no AC" label needs at least two independent evidence items, or it is downgraded to "unknown".

**External action in the demo (behind approval).** After the organiser clicks approve:
1. **Append** the ranked turf (complex, evidence crops, confidence, door-knock note) to the union's shared **Google Sheet** canvass tracker.
2. **Email** the organiser a turf map plus a one-page know-your-rights handout with 311 instructions.
3. **Create** a calendar event for the canvass shift.

The agent never files 311 itself, because complaints are the tenant's to make. It never claims a building violates the law; it ranks where to ask.

**Who to consult this weekend.**
- **Houston (remote, the real user):**
  - A Houston tenants union (volunteer-run).
  - A Texas housing nonprofit, which named several local tenant, environmental and community groups as coalition partners **[src]** texashousers URL above.
  - Contact by email or Instagram DM Friday night, asking for a 15-min Saturday call. **Unknown whether they reply in 18 h.**
- **Princeton (same job, in person):**
  - A campus graduate-student union or a campus political group (campus housing and labour organisers who run canvasses) **[src]** https://www.dailyprincetonian.com/article/2023/02/princeton-graduate-students-housing-unionization-university .
  - A local housing advocacy group.
  - Ask a canvass lead how they choose turf.
- **Three questions:**
  1. How do you pick which complexes to knock today, and what makes a wasted shift?
  2. What evidence would make you trust a "likely no AC" flag: photo, 311 count, tenant tip?
  3. Where does your turf list live (sheet, Action Network, Slack), and who approves it?
- **Evidence:** a screenshot of the DM/call, or a quote from the canvass lead.

**Main track:** Healthcare (heat illness, a public-health challenge).

**2-minute demo beats.**
- 0:00-0:15. The ordinance headline and "120 days". The organiser types: "Plan Saturday's turf in 77036/77074" **[ZIPs illustrative]**.
- 0:15-0:40. The planner splits work across subagents (prior / aerial / interior). The map fills with candidates.
- 0:40-1:15. The reasoning moment on complex X: prior, then condenser pads in the oblique, then the pano register, then dated by Vexcel history, then down-ranked. Complex Y rises on window-unit detections in 2023 and 2026 obliques.
- 1:15-1:40. The verification log: three labels downgraded for single evidence.
- 1:40-2:00. Approve, then the shared sheet updates live, the email lands and the calendar invite appears. Close: "same harness, swap the rule pack, LA City next."

**Biggest risk and the cheapest kill test.**
- **Risk:** the kit's MF set is marketed, scanned communities, which may almost all have central AC, so there are few positives. And SAM3 may not detect window units.
- **Kill test (about 1 h):**
  - Take the 20 oldest, lowest-rent Houston MF kit properties. Pull the oblique for each and run SAM3 "window air conditioner" and "air conditioner".
  - Eyeball 5 Matterport panos.
  - **Kill** if fewer than 3 of 20 show any window units by eye *and* SAM3 finds none.

**Confidence: 60.**

---

### Idea 2: Responder premise packet for large apartment complexes

**Pitch.** For any Houston or LA apartment complex, the agent builds the one-page pre-incident plan a fire or EMS crew wishes they had. It covers true height per building, podium garages, access and pools, plus a typical-unit layout with rescue-window sizes. It reconciles the records against the aerial view, flags what it could not confirm, and pushes the packet to the crew.

**User and the obligation.**
- The users are HFD company officers and fire inspectors working the High-Risk Apartment Inspection Program, and the EMS crews who must find a patient in a 20-building garden complex at night.
- Today pre-plans are hand-drawn or missing, and records like "3 stories" are trusted as given.

**Current pressure.**
- Houston's High-Risk Apartment Inspection Program (10+ violations in 6 months) **[src]** click2houston Jul 31 2026 URL above.
- First-ever apartment inspection ordinance work at Council **[src]** https://communityimpact.com/houston/heights-river-oaks-montrose/government/2026/04/01/houston-moving-toward-first-ever-apartment-inspection-ordinance .
- Repeated displacing complex fires in 2026: Jan 1 Bayou West (60 displaced), Jan 15 north Houston (10 units), Oct Westwood (12 units) **[src]** https://abc13.com/post/60-people-displaced-fireworks-started-large-fire-bayou-west-condominiums-sw-houston-new-years-day-hfd-says/18338204/ , https://www.fox26houston.com/news/houston-apartment-fire-westwood-2026-october .

**Data layers and the combination.**
- **Vexcel:**
  - DSM minus DTM height per footprint (worked in an early test on a tall building and a low structure) **[CAP]**.
  - Footprints and building count from `property/extract`.
  - Obliques for access drives and gates; `pool.*`; SAM3 "gate" and "fire hydrant" **[unverified labels]**.
  - Ortho for fire-lane layout.
- **CoStar:** `numStoriesAboveGrade`, total units, floor plans with `numUnits`, `parking[].parkingType` (structured vs surface), year built, `propertyContacts` (names only).
- **Matterport:**
  - Per-floor-plan scan (tied via `models[].attachments[]`) **[CAP]**, giving the floor plan image, bedroom positions (`classifications`), and `openings` windows with width/height/`lowerElevation` (sill height for rescue-window sizing).
  - The defurnished view for a clear layout image.
- **Combination:** records say how big and how tall, the aerial says which building is how tall and how to get in, and the scan says where the bedrooms and windows are inside the typical unit. No single layer gives a crew all three.

**Visible reasoning moment.**
1. **H1 (CoStar):** `numStoriesAboveGrade` = 3, so the plan says ground ladders are enough.
2. **Test (Vexcel DSM−DTM per footprint):** Building C reads about 16 m **[illustrative]**, which does not fit 3 residential floors.
3. **New hypothesis:** a podium over a garage. CoStar `parkingType` is structured, and the oblique shows garage openings at grade. Confirmed.
4. **Revision:** the packet marks building C as "3 residential over garage, ~5 levels to roof". The 3-story claim is shown struck through, with both sources cited.
5. **Second conflict:** a unit scan's geolocation is about 120 m from the kit point (scan and kit locations can sit well apart **[CAP]**). The agent refuses to assign that scan to a building and labels it "typical unit, building unknown" instead of guessing.

**External action (behind approval).** Render the packet to PDF, then **email** it to the station or inspector list, or **post** it to the crew's Slack/Teams channel. A shared-drive upload is also possible. The approval gate shows each unresolved conflict before it is sent.

**Who to consult this weekend (best physical access of the three).**
- **A local first-aid squad.** A staffed EMS squad with long-running student volunteer members **[src]** https://dailyprincetonian.com/article/2024/12/princeton-features-student-perspectives-working-volunteering-off-campus . Find a student member through campus networks and ask the duty crew chief for 10 minutes.
- **The town fire department's volunteer companies.**
- **The university fire marshal / EHS office.**
- **Houston:** HFD Fire Marshal Life Safety Bureau, Apartment/Hotel/Motel inspection team **[src]** https://houstontx.gov/fire/HFMO/inspectionteams.html (email only; reply unlikely by Sunday).
- **Three questions:**
  1. On a call to a large complex, what costs you the most minutes: finding the building, the gate, the stair, or the unit?
  2. What would you actually open en route (one page? a map? on the MDT?), and what would you ignore?
  3. Has wrong building info ever changed your tactics (stories, garage, pool)?

**Main track:** Healthcare (EMS delivery and response time).

**2-minute demo beats.**
- 0:00-0:15. A complex fire photo (news) and the question "what did the crew know?"
- 0:15-0:45. The agent enumerates buildings from Vexcel footprints. A DSM height ribbon shows building C as the outlier.
- 0:45-1:10. The conflict and revision (3 stories becomes podium), with the oblique as proof.
- 1:10-1:35. The Matterport typical unit: bedrooms and rescue windows highlighted, in the defurnished view. The scan with the 120 m geolocation offset is refused.
- 1:35-2:00. Approve, then the PDF is emailed and posted to Slack. Close: "same harness → schools/childcare sites next."

**Biggest risk and the cheapest kill test.**
- **Risk:** the crew's real pain is building numbering and unit-to-building wayfinding, and building numbers are in **no layer** **[CAP: absent]**. Open address-point data may or may not label buildings **[unverified]**.
- **Kill test (30 min):**
  - Ask one first-aid squad member what costs time.
  - Check whether Houston or LA open GIS address points carry building/unit numbers for 3 kit complexes.
  - **Reshape or kill** if numbering is the whole pain and no open data carries it.

**Confidence: 50.**

---

### Idea 3: Fire-displaced household rehousing shortlist (Red Cross caseworker)

**Pitch.** Hours after an apartment fire, a disaster caseworker enters the family's profile. The agent returns 3 available units nearby that fit the family, keep the kids in their school and are not themselves hazard properties. Each comes with the floor plan and defurnished walkthrough, and the shortlist goes to the caseworker's case sheet and calendar.

**User and the decision.**
- The users are American Red Cross Disaster Action Team caseworkers (Houston chapter) and the housing-navigation nonprofits they hand off to.
- After the Jan 1, 2026 Bayou West fire, the Red Cross "worked with management to find vacant or sister-property units" **[src]** https://www.fox26houston.com/news/houston-fire-fireworks-2026-new-years-bayou-west-condominiums . Today this is done by phone.

**Current pressure.** Frequent displacing complex fires in Houston through 2026: Jan 1, Jan 15, May 5 (6 families), Jun 10 (6 families), Oct 16 (12 units) **[src]** https://www.click2houston.com/news/local/2026/01/15/10-units-destroyed-in-large-apartment-fire-in-north-houston , https://abc13.com/post/firefighters-respond-apartment-fire-south-loop-houston-department-says/19270530/ .

**Data layers and the combination.**
- **CoStar:**
  - `apartmentModels[].{numBeds,minRent,maxRent}` and `numUnitsAvailable` **[CAP]**.
  - `residentialProfile.schools[]` **[CAP]** to keep school continuity.
  - `propertyManagementCompanyName` for **sister properties** of the burned complex, plus `petPolicies[]` and `parkingPolicies[]`.
- **Matterport:** the plan-linked scan, with `rooms.classifications` (is the "2nd bedroom" a bedroom?), bedroom `openings` windows, the defurnished view for the family, and `ceiling`.
- **Vexcel:** the burned complex before and after (newest collection) to confirm scale, and each candidate's `roof-defects.tarp`/`missing-material` and history, so a family is not sent to a complex with its own fire or roof damage.

**Visible reasoning moment.**
1. **H1 (CoStar):** a sister property under the same management company, 2 km away, has `numUnitsAvailable` > 0 on a 2BR plan within budget and serves the same elementary school. The agent proposes it.
2. **Test (Matterport):** the plan's scan classifies the second room as Office/Den and shows no window opening in it. For a family of 5 needing 2 sleeping rooms, it fails.
3. **Revise:** the next candidate is a 2BR elsewhere. Its scan confirms two bedrooms with windows, but Vexcel's newest collection shows a tarp on one building's roof that was absent in the prior one. The agent flags it and does not drop it outright; the note reads "ask which building."
4. **Third candidate:** passes all checks. The final list is ranked with the evidence attached.

**External action (behind approval).** **Email** the shortlist PDF to the caseworker, **append** it to the shared case-tracking sheet, and **create calendar holds** for walk-throughs. The agent never emails leasing offices, because kit contacts are placeholders **[CAP]**.

**Who to consult this weekend.**
- The American Red Cross regional chapter: a local Disaster Action Team volunteer or the disaster programme manager (they respond to home fires on weekends **[unverified for this weekend]**).
- A local housing nonprofit that rehouses at-risk families.
- A regional family-homelessness nonprofit.
- Any student who volunteers with Red Cross DAT, found via the campus volunteer-service office **[src]** https://www.princeton.edu/news/2018/06/18/princeton-university-volunteers-help-build-habitat-humanity-homes .
- **Three questions:**
  1. In the first 72 h after a fire, what decides where a family sleeps next, and who makes the calls?
  2. Which constraints break placements most: school, bedrooms, pets, budget, distance to work?
  3. Where do you track cases today, and would a caseworker approve a pushed shortlist?

**Main track:** Healthcare (housing stability after disaster), a weaker fit. Business & Enterprise is the alternative.

**2-minute demo beats.**
- 0:00-0:15. The Vexcel before/after of a burned complex.
- 0:15-0:35. The caseworker enters: family of 5, 2 kids at school S, budget B, 1 dog.
- 0:35-1:15. The reasoning chain: the sister property is rejected on the den, the tarp is flagged, the third candidate passes.
- 1:15-1:40. The defurnished walkthrough of the winner.
- 1:40-2:00. Approve, then the email, sheet row and calendar holds go out.

**Biggest risk and the cheapest kill test.**
- **Risk 1:** overlap with the excluded "apartment listing-vs-reality" (the plan-vs-scan check). The difference is that the user is a disaster caseworker and the core is matching under constraints, but judges may see it as the same thing.
- **Risk 2:** `numUnitsAvailable` is a listing snapshot, not live availability.
- **Risk 3:** the count of floor plans with a linked scan is unmeasured **[CAP]**.
- **Kill test (45 min):** count Houston MF properties that have a plan-linked scan *and* `numUnitsAvailable` > 0 *and* schools. **Kill** if fewer than about 50.

**Confidence: 45.**

---

## The one I would bet on: Idea 1 (Right-to-AC canvass targeter)

- It has the only **hard, current, dated** pressure: a law passed Aug 19, 2026, with about Dec 17 as the compliance horizon **[computed]**.
- It is in Houston, where the MF data is densest.
- Its users (local tenant organisers and housing nonprofits) publicly fought for this law and will now organise around it.
- The reasoning moment is genuinely visual and three-way, and it holds up to scrutiny: the CoStar prior is overturned by aerial condensers, which are then dated by Vexcel history and confirmed by the interior pano.
- The action (turf into the union's sheet, email, calendar) is the organiser's real workflow and does not touch placeholder kit contacts.

**Its weak point** is the positive rate among scanned, marketed complexes. Run the 1-hour kill test before committing.
