# Perspective: data contrarian

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Lens: start from the odd, under-used properties of the data, including its noise and contradictions, then find the person who needs the answer.
Read: the project's capability summary and the team's notes on the CoStar kit, the Matterport API, the Vexcel API, the event rules and the agent framework. Nothing else.
Counts describing the sponsor datasets have been generalised in this public copy. Anything not in the notes is marked **[unverified]**.

---

## (a) Under-used capabilities: the question only each one answers

| Odd capability | Question only this answers | Coverage (from notes) |
|---|---|---|
| Defurnished view, same pano ids and positions as the furnished one | What in this room is movable (furniture) vs fixed? Pixel diff of a pano pair is a free furniture mask, already registered to the mesh frame | Many models, commercial and residential; pano ids/positions matched in every pair sampled |
| Opening `width`, `height`, `lowerElevation` (sill), `relativeCenter`, in metres | Where exactly is each door and window, how big, and how high is the sill above the floor? | Openings on some commercial models, most residential; windows rare in commercial, common in residential; very small widths should be treated as noise |
| `rooms.ceiling{minHeight,maxHeight}` | Real clear height of a room (not the marketed one) | Some commercial, most residential in sample |
| Pano `position`/`rotation` + `geocoordinates` (ENU rotation, translation, altitude) | Which compass direction a window faces, and roughly what elevation the camera stood at | Panos on all sampled models; geocoordinates on most. Altitude accuracy **[unverified]** |
| OBJ mesh / MatterPak `cloud.xyz` | Volumes and depths of anything the API does not classify | Mesh on most sampled models; MatterPak bundle on all sampled |
| Room `tags` (e.g. `unfurnished`, `office`, `lobby`) | Is this suite physically empty right now? | Tags on a large share of rooms |
| Vexcel ortho history 2016-2026 (+ `us-tx-harvey-hurricane-2017` obliques) | Did this building exist / look like this in year X? | Many ortho collections at one Houston test point; obliques all 4 directions 2020-2026; hundreds of raw oriented images there |
| Vexcel DSM / DTM (undocumented) | How tall is the structure really, and what is the grade around it? | Worked at one Houston test point (a tall building and a low structure); centimetre-scale resolution. Hit rate at kit points **[unverified]** |
| Vexcel `property/extract` one feature per collection | How do the vendor's own attributes drift by year (footprint, type, roof)? This is a noise source the agent must adjudicate | Several features per point even with `latest=true`; the same footprint can read very differently by collection |
| `elements/detect` free-text SAM3 on ortho and oblique, per collection | How many cars were on this lot in 2019 vs 2026? | `car` counts differed between ortho and oblique on one test lot. Detection on a historical `collection` **[unverified]** |
| `embedding/extract search-location` | Which other parcels within 2 km look like this one? | ~60 m tiles; look-alikes scored high; a few Houston embedding collections. LA embedding coverage **[unverified]** |
| Tenancy history: `fromDate`, `toDate`, `squareFeetOccupied`, company `numEmployees`, industry (mostly well filled) | How has the population of a building changed over decades, and who left when? | Large tenancy history, mostly office; many current tenancies |
| Lease availabilities `dateOnMarket` | How long has this space failed to lease? | Many spaces; some have been on the market a long time |
| Apartment plan rents + `vacancyPercent` | What a specific floor plan asks, and how empty the community is | Many plans; vacancy on a subset (some values need normalising) |
| Sale comps `saleConditions[]`, `entities[].percentLeased` | What occupancy did the building have at sale? | Many comps; price on part of them |
| Broker / owner names on listings | Who to talk to about a building | `propertyContacts[]` names on a limited set of properties; contact details not usable for outreach |
| **Contradictions between sources** | Which source matches reality for this building, and why do the others differ? | Index vs kit coordinates usually close, some far apart; some PropertyId disagreements; some `buildingHeightInFeet` values out of range; footprint drift above; `numStoriesAboveGrade` nearly always filled vs DSM |
| Kit `constructionEvents[]` year built | Cross with 2016 ortho: was the building already standing (or a dirt lot) when the kit says otherwise? | Year built on many properties. Count of properties built 2016 or later **not counted** |
| Homes `poolType` bit flag vs Vexcel `pool.detected` | Does the MLS listing's pool exist from the air (and vice versa)? | Home listings in the kit; `poolType` fill rate **not given** |

---

## (b) Raw candidates (one line each)

1. **Ground Truth Desk**: an agent that hunts cross-source contradictions (stories vs DSM height, year built vs 2016 ortho, model vs kit coordinates, MLS pool vs aerial pool, GBA vs footprint × stories) and files evidence-backed correction tickets to the data owner. KEPT (#1).
2. **Second Life**: office-to-residential conversion screener that finds "ghost offices" (tenant roster says full; aerial car counts across years, empty-suite scans and 2-year listings say empty) and scores conversion geometry. KEPT (#2).
3. **Load-Out**: moving-company virtual survey; furnished/defurnished pano diff gives a furniture mask and volume, openings and stairs give the path, Vexcel DSM/DTM and obliques give truck staging and grade. KEPT (#3), with an overlap warning.
4. Way Out: bedroom egress-window check (window width/height/sill vs residential egress thresholds) crossed with floor height above grade from DSM/DTM. Dropped: mechanically the same as the excluded listing-vs-reality and accessible-home ideas; Matterport window size is rough opening, not net clear opening, so it cannot make a code claim.
5. Sun & heat exposure per unit: window orientation from pano/geocoordinates × neighbour heights from DSM → hours of direct sun, priced against plan min/max rent spread. Dropped: no per-unit rent in the notes (unit-level rent **[unverified]**); user and consult weak.
6. Off-market look-alike sourcing: embedding `search-location` from a deal the investor liked → look-alike parcels → kit age/class/last-sale filter → letter to owner. Dropped: owner names only on a limited set of properties and contact emails not usable; action reaches nobody real.
7. Harvey then-and-now hotel memo (a small set of Houston hotels, Harvey 2017 obliques, ADR). Dropped: too few properties, overlaps excluded insurer inspection and portfolio monitor.
8. Floor-to-floor forensics: DSM height ÷ stories − scan ceiling height = slab/plenum depth, for MEP retrofit planners. Dropped: ceiling data sparse in the commercial sample; no consultable user.
9. Staging detector: furnished/defurnished diff + furniture style repeated across listings by the same agent → flags staged vs lived-in scans for MLS virtual-staging disclosure. Dropped: defurnished is a Matterport-generated view, so this tests Matterport, not the home; thin Vexcel role.
10. Ghost-parking lender check: kit `parking[].totalSpaces` vs aerial lot area ÷ ~30 m² and car counts across years. Dropped as standalone (lender not consultable); folded into #1 and #2.
11. Elevation-certificate pre-screen (door threshold `lowerElevation` + DTM grade, Harvey imagery). Dropped: too close to excluded flood simulation.

---

## (c) Best three

### 1. Ground Truth Desk (the one I would bet on)

**Pitch.** An agent that treats disagreements between CoStar, Matterport and Vexcel as leads, investigates each one across the other layers until it can say which source matches reality, and files an evidence packet (images, numbers, reasoning) as a correction ticket after a human approves it.

**User and decision.** A property-data research analyst at a commercial real-estate data provider. Decision per record: correct the field, flag for a call to the owner, or dismiss as noise. Second users: the Matterport and Vexcel teams for geolocation and attribute drift.

**Outside pressure.** Sponsors want to see unexpected uses of their data. Records and reality can drift apart across sources: building heights, vacancy values, index coordinates, PropertyId joins, and Vexcel footprints between collections. Every downstream product (comps, rent, valuation) inherits these.

**Fields and what the combination gives.**
- CoStar: `numStoriesAboveGrade`, `buildingHeightInFeet`, `grossBuildingAreaSquareFeet`, `constructionEvents[]` year built, `primaryAddress.latitude/longitude`, `parking[].totalSpaces`, `attachments[].attachmentUri` photos; homes `poolType`, `yearBuilt`.
- Matterport: `models_index.csv` lat/lon vs kit; API `geolocation`; `rooms.ceiling`, panos of top-floor units (to count floor height); `generatedDescription.summary`.
- Vexcel: `dsm/extract` minus `dtm/extract`; `ortho/collections` and `ortho/extract` with `collection` (2016-2026); `property/extract` per collection (`footprint.area`, `building-type.class`, `pool.detected`, `structure.count`); `oriented/extract` obliques to count floors by eye; `elements/detect car`.
- Unique: no single source can say which one matches reality. Stories (kit) vs metres (DSM) vs floors visible in an oblique vs ceiling heights in the scan make a 3-way vote. Year built (kit) vs the 2016 ortho is a check that only exists because Vexcel keeps history.

**Visible reasoning moment.** Lead: kit says a high-rise story count; DSM at kit point gives the height of a low structure. Hypothesis A: the stories field does not match. Agent tests it: pulls the parcel's structures, sees two structures, and the kit point sits on the low one (a garage-like structure, as at the Houston test point). Re-samples DSM inside the tallest structure footprint → a tall building whose height fits the recorded story count. Revision: kit record matches, the conflict came from the coordinate landing on the other structure; it files a coordinate note instead of a height correction. The example is modelled on one Houston test point; whether a high-rise kit record behaves like this is **[unverified]** until the kill test runs.
Second pattern: kit year built 2019; 2016 ortho shows an existing building → check `renovations[]` → hypothesis "redevelopment on same lot" vs "year field does not match" → compare footprints 2016 vs 2026 → decide.

**External action.** After approval, append each ticket to a shared Google Sheet and post a Slack/Discord message to a channel the consulted CoStar or Matterport engineer agreed to watch, with the evidence images attached (no signed URLs; images from local cache, Vexcel attribution kept). Optional: email the packet to that person.

**Harness.** deepagents planner writes `leads.md`; one subagent per source (kit, matterport, vexcel) with isolated context; a "judge" subagent must cite two independent sources before any ticket (forced verification loop); `interrupt_on` the file/post tool (approval gate); filesystem memory `/cases/<propertyId>/` makes it resumable. Second job on the same harness: the Second Life screener below, or a homes pool/roof audit, with new check definitions only.

**Consult this weekend.** CoStar, Matterport and Vexcel engineers are available at the event. Ask one CoStar data/research person and one Matterport person. Geography gap: none for the user, since the business is present; the data is theirs. Evidence: quote + photo at the booth.
Questions: (1) When a researcher finds a stories/height or year-built conflict today, what evidence do they need to change the field, and where does the ticket go? (2) Which of these conflict types is costly to you, and which is noise you already know about? (3) Would you watch a Slack channel / sheet of agent-filed tickets for 12 hours and mark each accepted or rejected?
Risk: judges may see a sponsor as a weaker "real business" than a local shop. State it plainly in the submission.

**2-minute demo.**
0:00 One line: "Three sources describe the same building; they disagree; this agent finds out which one matches reality."
0:15 Run on a 30-property Houston batch from local cache; leads list fills (stories vs DSM, year vs 2016, coordinate drift).
0:40 Open one lead live: plan revises in view (garage vs tower), DSM crop and oblique side by side, floors counted.
1:15 Second lead: year built vs 2016 ortho slider.
1:35 Approval prompt; approve two, reject one with a reason the agent records.
1:50 Slack/Sheet shows the tickets arrive; consulted engineer's reply or quote on screen.

**Biggest risk and cheapest kill test.** Risk: most conflicts are trivial (rounding) or explained by our own join errors, so the demo shows no real record mismatches. Kill test (~1 hour): 50 kit properties, DSM−DTM max inside the parcel vs `numStoriesAboveGrade`; count those off by 3+ floors and check 5 by eye on obliques. Also list kit properties with year built ≥ 2017 and pull the 2016 ortho for 10. If fewer than ~3 genuine mismatches in 60 records, drop to idea 2.

**Confidence: 62.**

---

### 2. Second Life: ghost-office conversion screener

**Pitch.** Find office buildings whose tenant roster says "occupied" but whose physical evidence says "emptying", then check whether their geometry could become apartments, and send a screening packet to the person deciding.

**User and decision.** An adaptive-reuse developer or architect deciding which buildings to approach about conversion. LA has an adaptive-reuse program expanded citywide in 2025 **[unverified]**; Houston has no zoning (well known, not in notes).

**Outside pressure.** Some office space stays on the market for a long time (notes). Apartment asking rents per plan are available nearby for comparison.

**Fields and combination.**
- CoStar: office tenancies (`fromDate`, `toDate`, `squareFeetOccupied`) joined to company-detail `numEmployees`, `businessStatus` (OutOfBusiness); `forLeaseSummary.spaces[]` SF and `dateOnMarket`; office properties in LA and Houston, many with scans; `numStoriesAboveGrade`; apartment-listing plan rents within 400 m; sale comps (office price per SF, cap rate).
- Vexcel: `elements/detect car` on lots and garage roofs per collection (2019-2026); `property/extract` footprint (depth of floor plate); DSM height; obliques for window grid.
- Matterport: suite scans with room tag `unfurnished`, `dimensions.areaFloor`, `ceiling` (sparse in commercial sample), windows (rare in commercial sample: weak).
- Unique: the roster alone says "occupied", aerial alone says "few cars", the scan alone says "one empty suite". Together they estimate whether the building is really emptying, which no CoStar field gives (commercial vacancy rate is absent in the kit).

**Visible reasoning moment.** Roster: 40 current tenants, sum of employees high → hypothesis "occupied, not a candidate". Aerial: car count on the building's lot falls across 2019, 2022, 2026 captures; 30% of available SF has sat for 2+ years; two suite scans tagged `unfurnished`. Revision: roster lags reality (many `toDate` null on tenants whose company is `OutOfBusiness`) → reclassify as candidate. Then geometry check: floor-plate depth from footprint too deep for daylight → downgrade to partial conversion. Thresholds for "too deep" come from the consulted architect, not invented.

**External action.** Email the screening packet (PDF) to the consulted architect/developer and place a calendar hold to review, after approval. Not to brokers (broker contact details not usable).

**Consult.** A local architecture practice or a campus architecture student group with adaptive-reuse interest, reached Saturday by phone/visit **[unverified availability]**; or a developer contact by video call. Geography gap: the screening method is location-independent; we say it is demonstrated on LA/Houston because that is where the data is.
Questions: (1) What three facts make you walk away from a conversion in the first hour? (2) What floor-plate depth / floor-to-floor height do you need? (3) How do you currently learn a building is quietly emptying?

**Demo beats.** Map of LA offices → roster-vs-aerial disagreement list → one building: car-count timeline, empty-suite pano, footprint depth → verdict revised live → approval → email + calendar invite sent.

**Biggest risk / kill test.** Car detection on historical collections may not be supported or comparable (season, shadow; parking garages hide cars). Test: run `car` detect on 5 office lots for 3 collections; if counts are unstable on a known-occupied building, the core signal is noise. Second risk: office Property Insights is weak (windows rare in commercial sample).

**Confidence: 40.**

---

### 3. Load-Out: moving-company virtual survey from furnished/defurnished pairs

**Pitch.** For a home that just sold, estimate the move from the existing scan: the pano diff isolates furniture, the mesh gives its rough volume, openings and stairs give the carry path, and Vexcel gives truck staging, driveway grade and tree obstruction. The mover approves and the agent books the survey call with the customer.

**User and decision.** A small moving company's estimator: which crew size, truck size and special equipment, and is an in-person survey needed?

**Outside pressure.** Movers lose money on under-estimates and lose bids on over-estimates (general knowledge, not from notes). Federal rules on binding estimates and virtual surveys for interstate moves exist **[unverified detail]**.

**Fields and combination.**
- CoStar homes: `status` Sold / Active, `closeDate` within the past year, `bedsMin`, `sqftMin`, `parkingTotal`, `garageSpaces`, features `highlights[]`, agent names.
- Matterport (residential PI on the residential sample): defurnished pairs (many residential models), doorway widths, `Staircase` rooms, mesh, 4k panos.
- Vexcel: DSM−DTM grade between street and door, obliques of the front facade, `tree` detect, `hardscapes.area` (driveway); residential splats with drone photos as a bonus.
- Unique: the defurnished pair at identical poses is a ready furniture mask; nobody else has it.

**Visible reasoning moment.** Hypothesis: 3BR → mover's standard volume. Pair diff finds a fully furnished third bedroom and a piano-sized object upstairs; narrowest doorway on the stair path 0.71 m. Then contradiction: listing status Active and remarks mention staging, so the furniture may be the stager's → the agent asks the customer to confirm instead of quoting, and revises crew size only for confirmed items.

**External action.** SMS/email the customer a confirmation list and book a 15-minute video survey on the mover's calendar, after the mover approves.

**Consult.** A Princeton-area moving company (open Saturdays, callable) or a student-run moving/storage service at Princeton **[unverified that one exists]**. Geography gap: their estimate workflow is the same; we show it on LA/Houston scans and ask them to judge the output on a sample.
Questions: (1) What do you need to know before you quote without visiting? (2) Which access problems cost you most on move day? (3) Would a customer confirmation list from a 3D scan replace your walkthrough call?

**Demo beats.** Sold home → furnished/defurnished slider → masked items → path with 0.71 m door in red → oblique showing driveway and tree → staging flag → approval → SMS and calendar booking sent.

**Biggest risk / kill test.** Defurnished views are generated by Matterport, so the diff may be noisy (generated artefacts, partial removal). Test: diff 3 residential pairs and look at the masks. Second risk: overlap with excluded furniture-fit planner and courier instructions; judges may see it as the same idea.

**Confidence: 33.**

---

## Bet

Ground Truth Desk. It is the only idea whose raw material is the contradictions between the sources themselves, which show up across all three layers, so the agent's reasoning (hypothesis, contradicting source, revision) is forced by the data rather than staged. It uses all three layers on every lead, works on the densest property types, and its user is physically at the hackathon, which removes the Houston/LA vs Princeton gap.
