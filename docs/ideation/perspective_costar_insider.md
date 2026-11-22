# Perspective: CoStar product leader judging the track

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Sources read: the project's capability notes. Two web searches (cited at the bottom). All data observations come from the capability notes. Anything else is marked **[unverified]**.

## (a) Reasoning from this lens

**What CoStar already ships, so a demo of it is not news to me:**
- 3D tours on LoopNet, Apartments.com and Homes.com listings.
- Matterport's own features: defurnish, automatic measurements and floor plans, and AI summaries (`generatedDescription`).
- Property search with filters, and AVMs (Homes.com `latestAVM`).
- Comps, tenant rosters, broker contacts. Vexcel already sells roof condition, defects and pools to insurers.
- Matterport's blog markets "facility passports" for pre-incident planning. These are tagged by hand, one site at a time ([Matterport blog](https://matterport.com/blog/how-to-create-facility-passport)).
- Matterport has written about a film-location database (LocationsHub) using Matterport tours ([Matterport blog](https://matterport.com/blog/locationshub-production-scouting-matterport)).
- So "Matterport for X" alone is not new. What is new is producing the X document automatically, at city scale, from scans that were made for leasing, cross-checked against the aerial and the record.

**What bores me:**
- Chat with a listing.
- Virtual staging.
- A search copilot.
- A site score made from proxies.
- A memo that summarises three APIs.
- Any agent whose "action" is a drafted email to a placeholder contact address.
- Any idea where Matterport is a thumbnail.
- Roof triage. Vexcel's PDF already pitches it.

**What would make me forward it to my VP:**
- A buyer outside brokerage that we do not sell to today. I mean public safety, film/TV and telecom.
- Our "commercial" scans (most of them apartment units) used as a second-life asset.
- The scan's metric geometry (wall graph, openings in metres, ceilings) treated as engineering input, not as pictures.
- Vexcel DSM height and obliques treated as the outside of the same building, in the same coordinate frame.

**The test I apply:** Would the output be a document a third party already has to produce by hand, with a format they already accept? If yes, the action is real and the usefulness is obvious.

**Data reality that shapes my picks:**
- Multifamily is the thick layer: most of the properties and most of the scans.
- Property Insights (rooms, walls, openings) is complete on residential models and on part of the commercial models.
- DSM/DTM works.
- Obliques come from 4 directions, with history back to 2016.
- No source detects objects inside a scan.
- Contact emails in the data are placeholders, so the external action must go to a real consulted person or to a real public system.

## (b) Raw candidates

1. **First-due pre-incident plan generator for fire departments.** Unit scans, building obliques and the record become a one-page tactical pre-plan with labelled sides. **KEEP.**
2. **Film/TV location scout over vacant inventory.** Vacant suites and amenity spaces are treated as shoot locations, with ceiling, power-free clear area, base-camp parking from the air and the property manager from the record. **KEEP.**
3. **In-building radio coverage pre-survey (ERRCS/DAS).** The wall graph and its thickness feed an RF loss model. DSM line-of-sight to towers, and tenant headcount, add the demand side. **KEEP.**
4. **Moving-company volume estimate from furnished vs defurnished pano pairs.** KILLED. The furniture in a scan is staging, not the customer's belongings. It also overlaps "courier instructions" and "furniture-fit".
5. **Appraisal gross-living-area check (ANSI Z765) on homes.** Scan floor area against Vexcel footprint × stories against MLS sqft, with a reconsideration-of-value filing. KILLED. It is the "listing-vs-reality" idea moved to homes, and `areaFloor` is net room area, not GLA.
6. **Apartment amenity rooms as rentable event venues.** KILLED. It is too close to the excluded "Olympics space finder" and "second-hand space hunter".
7. **Resilience hub / cooling-centre designation for Houston outages.** Large amenity rooms, rooftop solar and pools are the inputs. KILLED. Nobody in Houston can be consulted this weekend, and the city decision maker cannot be reached.
8. **EV-charger feasibility for apartment parking.** KILLED. Matterport adds nothing (no electrical room detection), and parking stalls cannot be counted.
9. **Wildfire defensible space for LA homes, with drone splats.** KILLED. The interior scan is irrelevant, it is close to the excluded insurer inspection, and Vexcel already pitches it.
10. **Renovation-draw verification for construction lenders.** KILLED. It is too close to the excluded portfolio condition monitor.
11. **Dispatchable-location (floor/unit) data for 911/MLTS compliance** [regulation details unverified]. KILLED as a standalone idea. It is folded into idea 1 as a unit-locator layer.

## (c) Best three

---

### 1. First-Due: pre-incident plans written from leasing scans and aerial

**Pitch.** For any scanned apartment or office building, the agent writes the one-page pre-incident plan a fire company would otherwise make by walking the building. A human officer approves it, and it is published to the crew's shared pre-plan folder.

**User and obligation.**
- The user is a fire company officer or a department pre-plan coordinator.
- Departments run pre-incident planning programmes. NFPA 1620 is the standard, and ISO's Fire Suppression Rating Schedule gives some credit for pre-fire planning **[unverified, check exact FSRS item]**.
- The decision is whether the plan is ready for crews, and what to verify on the next walkdown.

**Outside pressure.**
- Large apartment complexes are where crews face unfamiliar layouts at night.
- Pre-plan coverage is chronically incomplete because each plan is a manual walkdown **[unverified, ask the consulted department]**.
- Vendors in this space (records-management and pre-plan software) take imagery but not interior geometry **[unverified]**.

**Data layers and what only the combination gives.**
- **CoStar:** `propertyType`, `numStoriesAboveGrade`, year built, GBA, `propertyApartment.models[]` (unit counts by beds, which give an occupant estimate), current tenancies from occupancy + company-detail (a food tenant means a commercial kitchen hazard), parking type (structured vs surface), and `propertyManagementCompanyName` (the after-hours contact field).
- **Matterport:** floor plan per apartment floor-plan type (scans tie to `models[].attachments[]`), wall graph, door openings in metres, ceiling heights, and the defurnished pano for an unobstructed layout view.
  - Output: a "typical unit" search sheet showing the entry door, the bedroom farthest from the entry, and window openings that work as secondary egress (`openings.type=window`, `lowerElevation`, `width`).
- **Vexcel:**
  - Ortho as the site plan: access roads, gates, courtyards.
  - Four obliques, labelled as NFPA sides A/B/C/D. "oblique-north" shows the south facade.
  - DSM−DTM height by wing.
  - `roof-objects.solar` (PV is a firefighter hazard), `skylight.count`, `pool.detected` on the roof.
  - Fire hydrants: SAM3 `fire hydrant` is untested, so the fallback is an LA/Houston open hydrant dataset **[availability unverified]**.
- **The combination:** No single layer tells you which side the apparatus can reach, how tall that side is, and what the unit behind that window looks like inside. Joining them on one address does.

**Visible reasoning moment.**
1. The agent reads the CoStar record: 3 stories, Multifamily. Hypothesis: a garden-style building, ground ladders suffice, no aerial needed.
2. The DSM−DTM profile shows one wing about twice the height of the others.
3. The oblique of that wing shows open-sided parking levels. That is a podium.
4. Revised: "Stories above grade likely excludes the podium. Charlie side is about N m. Aerial apparatus is needed there. Standpipe probable, VERIFY on walkdown." The agent writes this conflict and its evidence to `/memory/conflicts.md`.
5. Second check: the ortho shows an enclosed courtyard with no drivable opening, so the agent moves "apparatus access" from side C to side A and records why.
6. A verification subagent then re-opens each claim. Every height, width and side label must cite a source file or the plan cannot be finalised. Any claim without a source becomes a "VERIFY" item, not a fact.

**External action.**
- After the officer clicks approve in the HITL gate, the agent publishes the PDF pre-plan.
- It then emails the plan to the consulted officer, posts it to a shared Google Drive "Pre-plans" folder (or a Slack channel), and adds a calendar hold for the walkdown that verifies the flagged items.
- The gate shows a diff of the "VERIFY" items before anything leaves the system.

**Harness (deepagents).**
- Tools: `kit.query`, `mp.model_geometry`, `mp.defurnished_pano`, `vx.ortho`, `vx.oblique(side)`, `vx.dsm_profile`, `vx.parcel`, `pdf.render`, `gmail.send`, `drive.upload`, `calendar.hold`.
- Subagents, each with its own isolated context: site-and-access (Vexcel), interior (Matterport), occupancy-and-hazard (CoStar), and verifier.
- Filesystem memory holds `plan.md`, `/evidence/*.png` and `conflicts.md`.
- Each building is a resumable job.
- Second job on the same harness: idea 3, or a "mutual-aid packet" for a whole block.

**Who to consult this weekend (Princeton).**
- **The town fire department** **[names to verify on arrival]**. Volunteer firehouses are often staffed on weekends, so walk in Saturday morning.
- Alternatives: a university fire marshal or environmental health and safety office, and a local first-aid squad.
- **Geography gap, stated honestly:** they will not respond in Houston. We show them a Houston plan and ask them to mark it up as if it were theirs. The evidence is their marked-up printout or a photo of their current pre-plan binder or tablet. The pitch says the method transfers anywhere scans and aerial exist. It does not claim adoption by Houston FD.

**Three questions.**
1. Show me your last pre-plan. Which fields do you fill by walking the building, and which do you never have time to fill?
2. On this Houston printout, what is wrong or missing? Would you trust a height or door width from a scan without a walkdown?
3. Where would this need to land for crews to see it: the MDT/tablet, a binder, or a shared drive? Who approves it?

**Two-minute demo.**
- 0:00-0:15. The firefighter's quote and photo: "pre-plans are a walkdown each."
- 0:15-0:45. The agent runs on one Houston community, with the plan and subagents visible. The DSM profile contradicts "3 stories", and the podium appears in the oblique. The revision is logged.
- 0:45-1:10. Generated plan: sides A-D on the obliques, the site plan with the access arrow, and the typical unit floor plan with the farthest bedroom and secondary-egress windows highlighted. The SDK flies into the unit.
- 1:10-1:35. The verifier strikes an unsourced claim to "VERIFY". The approval gate shows. Approve, and the email lands on the consulted officer's phone and the Drive folder updates.
- 1:35-2:00. The same harness runs a second building unattended, and we close on the line about how many scanned buildings exist (thousands of scanned multifamily properties).

**Self-score.**

| Criterion | Score | Reason |
|---|---|---|
| Data (30) | 26 | Three layers, each doing a job the others cannot; geometry used as geometry |
| Agentic (30) | 24 | Real conflicts (stories vs DSM, access vs courtyard) and a forced verifier |
| Useful (25) | 21 | A real, unfunded manual task; but the buyer is outside CoStar's sales motion |
| Demo (15) | 13 | Obliques, the SDK flythrough and a live email |
| **Total** | **84** | |

**Biggest risk and the cheapest test that kills it.**
- **Risk:** the scanned units do not include the floor-plan types we need, or Property Insights (walls, openings) is missing on the target community's scans. That leaves only the aerial and the record, and the "inside" disappears.
- **Test (1 hour):** pick 10 Houston MF properties with defurnished scans, query rooms/openings/walls on all of their scans, and pull DSM at the kit lat/lon. Kill if fewer than 3 have both full geometry and a usable DSM height.
- **Second risk:** firefighters say "we'd never trust it". Ask question 2 early on Saturday.

**Confidence: 72.**

---

### 2. Call Sheet: a film/TV location scout over the vacant-space inventory

**Pitch.** A location manager describes a scene, for example "a corner office with floor-to-ceiling glass and a skyline view, and space for 30 crew". The agent searches vacant LA office suites and apartment amenity spaces, verifies each candidate against the scan and the aerial, and sends a location-request packet after the scout approves it.

**User and obligation.**
- The user is a location manager or scout on an LA production.
- The decision is which three locations to tech-scout this week.
- Pressure: prep schedules, and FilmLA permits need an address and a parking plan **[FilmLA requirements unverified]**.

**Data layers and the combination.**
- **CoStar:** lease spaces (LA quotes $/SF/mo), `availableOnDate`, `floorName`, `parking[].totalSpaces`, and the property manager and broker names. Some listings have suite tours.
- **Matterport:**
  - `ceiling.maxHeight`, needed for the lighting grid.
  - Room `dimensions` for clear floor area.
  - Window openings, for the "glass wall" check.
  - Defurnished panos, which show an empty set.
- **Vexcel:**
  - Obliques for the facade look and the view direction.
  - DSM to check whether a taller neighbour blocks the claimed view.
  - Ortho plus SAM3 `car` across collections, to find a base-camp lot for trucks.
- **The combination:** whether the view is real (window bearing from the scan's ENU rotation against neighbour heights from the DSM), and whether the trucks fit (aerial).

**Reasoning moment.**
1. Hypothesis: the 14th-floor suite "with views" is the best fit.
2. The window openings sit on the wall facing bearing X. The DSM shows a taller tower about 40 m away on that bearing **[illustrative, to be measured]**.
3. Revised to the 9th-floor suite on the opposite face.
4. Second check: the record lists a large parking count, but the aerial shows a garage, not a surface lot. Base camp has to be off-site, so the agent searches embeddings for "large empty surface parking lot" within 500 m.

**External action.**
- After the scout approves: a location packet (PDF with pano stills, oblique, base-camp map) goes to the consulted student filmmaker by email.
- A row is appended to the shared production "locations" Google Sheet.
- A tech-scout calendar hold is booked.
- Property-manager emails in the data are placeholders, so the request to them is drafted only. We say so on stage.

**Consult.**
- A campus student film group (a campus film society, a student theatre group, or university film students) **[names to verify]**. Their student-film location coordinator is the person to find.
- Their own shoots are in NJ, so the geography gap is large. Mitigation: ask them to brief the agent with a real scene from their current script. Their judgement of the packet format is the evidence.
- Questions:
  1. What do you check on a scout that photos never tell you?
  2. What kills a location after you've fallen for it?
  3. What does a location request to an owner need to contain?

**Demo.** Scene brief, 40 candidate suites, then the view check fails on the DSM and the agent re-ranks. Defurnished pano of the winner, then the base-camp lot on the ortho, then approve, and the Sheet updates live.

**Self-score.**

| Criterion | Score |
|---|---|
| Data (30) | 25 |
| Agentic (30) | 22 |
| Useful (25) | 17 (LocationsHub already exists; vacant-office inventory is novel) |
| Demo (15) | 14 |
| **Total** | **78** |

**Risk.** Ceiling and window data may exist on few office scans (window openings appeared on only a few commercial models in the sample). Cheap test: query the tour listings' scans for ceiling and window openings. Kill if fewer than 10 have both.

**Confidence: 55.**

---

### 3. Dead Zone: an in-building radio coverage pre-survey from the wall graph

**Pitch.** Before an integrator sends a crew with a spectrum analyser, the agent predicts where cellular or emergency-radio signal will fail in a building. It traces paths from the nearest towers through the Vexcel DSM to the facade, applies wall-by-wall loss through the Matterport wall graph, and decides which buildings need a site survey. It then books that survey.

**User and obligation.**
- Users: a DAS/ERRCS integrator, or a property manager whose building must pass emergency-responder radio coverage tests. IFC 510 and NFPA 1225 require them in many jurisdictions **[LA/Houston adoption details unverified]**.
- The decision is which buildings to survey, and where to put the donor antenna.

**Data layers and the combination.**
- **Matterport:** the wall graph with `thickness`, openings, ceiling heights and floors. These give a per-room attenuation estimate.
- **Vexcel:** DSM and DTM give the line-of-sight profile from tower to roof and the clutter from neighbours. `roof-objects` and roof shape give donor-antenna placement.
- **Public data:** FCC Antenna Structure Registration gives tower coordinates and heights **[dataset access to verify]**.
- **CoStar:**
  - Tenant headcount (`numEmployees`, where present), which tells you where coverage matters.
  - Building class, GBA and stories.
  - Parking type: below-grade garages are classic dead zones.
- **The combination:** no single source gives both the outside path and the inside loss.

**Reasoning moment.**
1. Hypothesis: the corner suite facing the tower is fine.
2. The DSM profile shows a taller building blocking the path.
3. The agent re-routes to the next tower, which is on the other side.
4. The interior path then crosses 4 walls, including a thick core wall.
5. The suite is re-classed as a likely dead zone. The plan is revised to survey that floor first and to put the donor antenna on the north roof edge, where `roof-objects` shows free space.

**External action.** After approval, a survey work order is emailed to the consulted contact, a survey slot is booked on the calendar, and the shared survey sheet is updated.

**Consult.**
- A university amateur radio club **[existence and activity to verify]**, plus any university IT/networking staff who are reachable.
- This is weak for the usefulness judge: a club is not the paying business. Evidence would be their critique of the loss model and their quote.
- Questions:
  1. Is wall thickness alone a usable loss proxy without knowing the material?
  2. What would make a survey crew trust a pre-survey?
  3. What does a survey work order contain?

**Demo.** Building, then the tower ray over the DSM, then the floor plan heat map. Blocked path, re-route, re-rank. Approve, and the work order is emailed.

**Self-score.**

| Criterion | Score |
|---|---|
| Data (30) | 26 |
| Agentic (30) | 21 |
| Useful (25) | 15 |
| Demo (15) | 11 |
| **Total** | **73** |

**Risk.** The RF model is our own physics, and an expert may dismiss it. Wall material is unknown. Cheap test: one 30-minute call with the radio club about the loss model.

**Confidence: 40.**

---

## The one I would bet on

**First-Due (idea 1).**
- It sells our data to a buyer CoStar does not serve (public safety).
- It uses each layer for something only that layer can do: interior geometry, outside sides and height, and occupancy and hazards.
- Its conflicts (stories vs DSM, access vs courtyard) come straight from places where records and reality can drift apart.
- Its output is a document a real third party already produces by hand.
- It has the most reachable consult in Princeton on a Saturday: a firehouse.
- Matterport markets hand-tagged "facility passports". Generating them automatically, at city scale, from leasing scans plus Vexcel is the moment that shows the sponsor something new about its own data.

## Sources
- [Matterport: Mutual Aid Ready, facility passports](https://matterport.com/blog/how-to-create-facility-passport)
- [Matterport: LocationsHub production scouting](https://matterport.com/blog/locationshub-production-scouting-matterport)
- [LoopNet: Is your property ready to make a big screen debut?](https://www.loopnet.com/learn/is-your-property-ready-to-make-a-big-screen-debut/608999453)
