# Perspective: action-first operator

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Read only the project capabilities notes and the hackathon packet. Web searches were run on 2026-11-13. Nothing was submitted anywhere, and no Matterport or Vexcel calls were made.

## (a) Reasoning chain

1. **Start from what can leave the system honestly.** Kit emails and phones are placeholders, not real contacts, so no outreach can go to a kit contact. City complaint and permit portals (Houston 311, MyLA311, LADBS, FilmLA) are real, but filing about a building we don't own or occupy would be a false report or a misuse. So the only actions we can really fire go to **a person who consented this weekend**: the business we consult, or the sponsor engineers on site. Government endpoints can be **staged**: the packet is filled, validated against the portal's field list, and stopped at the submit button with a human approval card.
2. **Then ask which actions need the evidence chain.** An action justifies 3D + aerial + record evidence when its recipient needs (i) inside geometry, (ii) outside or context geometry and (iii) an identity or attribute record, and when those three disagree often enough that reconciling them is the work. Three action types pass:
   - a **pre-incident plan** a fire company files (inside layout plus outside access plus building record);
   - a **record correction** filed with the data owner (the record is contradicted by the air and by the scan);
   - a **location-scout packet** plus a permit draft (the room's look and size, the sun and shadow outside, base-camp space).
3. **What gets cut.** Most "file a form" ideas, such as decline-in-value, tax, insurer and contractor bids, are either excluded or need only one layer.

### Candidate real actions and endpoints

| Action / endpoint | URL | Who receives it | Can a hackathon team honestly trigger it? | Verified? |
|---|---|---|---|---|
| Gmail send (approval-gated) | Gmail API | A consenting person (consulted business, sponsor engineer, teammate) | **Yes, really** | Gmail set up per brief (not tested by me) |
| Google Drive/Docs/Sheets/Slides create plus share | Drive API | Same | **Yes, really** | Connector present in session; not exercised |
| Calendar event (walkthrough or tech-scout hold) | Calendar API | Same | **Yes, really** | Not tested |
| Private GitHub issue (correction ticket) | GitHub API | Repo collaborators (sponsor engineers if invited) | **Yes, really**, but only in a **private** repo, because sponsor data must not go public | Project data-handling rule |
| Houston 311 online service request | houstontx.gov/311 | City of Houston 311 | **Stage only.** It needs an address plus your email and returns an SR number, so it would be a real report about a property we have no standing at. No public Open311 API found | Verified (portal exists, more than 100 online SR types; no API found) |
| MyLA311 | myla311.lacity.gov | City of LA | **Stage only** (same reason). 86-96 request types; some need contact info | Verified (portal exists) |
| LAHD habitability complaint | not located | LA Housing Dept | **Stage only**; route unverified | **Unverified** |
| LADBS Soft-Story Retrofit Program | ladbs.org …/soft-story-retrofit-program; program email inbox | LADBS | **No.** Submittals need a licensed engineer or architect | Verified |
| LAFD Brush Clearance (VMS3 portal, self-inspection step) | lafd.org/fire-zone; fps.lafd.org/fire-services/brush/inspection-process | LAFD Brush Unit | **Stage only.** Owner-only; no self-cert form found | Partly verified |
| HFD high-rise apartment safety plan (LSB Standard 07, high-rise = floor more than 75 ft above fire access) | houstontx.gov/fire/business-information | HFD Life Safety Bureau | **Stage only.** The owner files. Content requirements not read in full | Partly verified (standard exists; contents unverified) |
| HFD inspection scheduling | by phone only ("online scheduling is not available") | HFD Fire Marshal | **No** | Verified (Permitting Center deck) |
| NFPA 1660 Ch.17 pre-incident plan (ex-NFPA 1620): plan development, data collection, plan sketches; Ch.18 construction and site | NFPA standard | Any fire company, as an internal document | **Yes**, delivered by email or Drive to a consenting fire company | Section titles verified; text not read |
| LADWP Consumer Rebate, cool roof ($0.20 or $0.60/SF by SRI tier, over conditioned space; apps due 2026-12-31) | ladwp.com …/consumer-rebate-program | LADWP | **Stage only.** The owner applies after install | Verified from search snippets |
| LADWP CAMR (free assessment, low-income multifamily) | LADWP CAMR brochure | LADWP | **Stage only** (owner) | Verified, exists |
| MyFilmLA permit (up to 5 locations, each with base-camp and crew-parking entries; insurance; non-refundable fee; 3-7 business days) | info.filmla.com/applying-for-a-film-permit | FilmLA | **Stage only.** The fee and insurance block a real submit | Verified |
| LA County RP-87 decline-in-value | assessor.lacounty.gov/decline-in-value | LA County Assessor | Excluded (tax) | Verified, not used |
| CoStar data correction channel | none public found (general phone line only) | CoStar Research | **Really, via on-site CoStar engineers** (email or private issue), with no public form | Public channel **unverified** |

## (b) Raw candidates (10)

1. **Fire pre-incident plan packet for apartment communities.** NFPA 1660 Ch.17-style plan from scan, aerial and record, emailed to a consenting fire company. **KEEP.**
2. **Built-world record-correction agent.** Kit vs Vexcel vs Matterport contradictions become evidence-backed correction tickets filed with the CoStar/Matterport engineers on site. **KEEP.**
3. **Film location-scout agent.** Rooms that match a shot list, with window orientation and DSM shadows for golden hour and base-camp space from the air, delivered as a scout deck plus a staged MyFilmLA draft. **KEEP.**
4. Cool-roof rebate packet for LA multifamily owners. **Dropped:** Vexcel does all the work and the Matterport role is decoration (top-floor ceiling only). The real application happens after install, so nothing fires.
5. Top-floor heat-risk triage for LA renters (dark roof, west windows, no tree cover, no roof AC). **Dropped:** too close to the excluded warehouse-heat idea. The action is only a letter to an owner whose kit email is a placeholder.
6. Tenant habitability complaint packet (LAHD / Houston 311). **Dropped:** scans are listing-time, not the tenant's current condition. Filing would be a false or stale report, and the LAHD route is unverified.
7. Soft-story retrofit triage from obliques (tuck-under parking) plus year built. **Dropped:** LADBS already identified the buildings years ago, a licensed engineer is required, and unit scans don't show the garage.
8. Houston storm board-up cut list from window opening sizes, sent as a lumber quote request. **Dropped:** too close to the excluded contractor bid. Window openings appear on only a few commercial sample models.
9. HFD high-rise safety-plan pre-filler (LSB Std 07). **Merged into 1.** The DSM height vs 75 ft threshold check becomes one reasoning step.
10. Brush-clearance / defensible-space packet for LA hillside homes. **Dropped:** the vegetation is outside, so the interior scan adds nothing. It is also near the PDF's own suggested idea, and the owner-only portal means nothing fires.

---

## (c) Best 3

### Idea 1: PrePlan, a fire pre-incident plan agent for apartment communities

**Pitch.** It builds the pre-incident plan a fire company keeps for each apartment complex, covering access, height, construction, unit layouts and hazards, from scan, aerial and record evidence. It flags where the sources disagree and sends the plan to the company only after an officer approves it.

**User and obligation.** The fire company's pre-plan officer has a duty to keep pre-incident plans current (NFPA 1660 Ch.17, ex-1620). In Houston, owners of buildings over 75 ft also owe HFD a high-rise safety plan (LSB Standard 07).

**Outside-world pressure.** Pre-plans are normally made by walking each building; apartment stock changes; Houston started a High-Risk Apartment Inspection Program in 2026 (news report; scope not verified).

**Data layers and what the combination gives.**
- **Kit:** `numStoriesAboveGrade`, `constructionEvents` (year built), `buildingClass`, `grossBuildingAreaSquareFeet`, `totalNumUnits` / `propertyApartment.models[]`, `parking[]`, kit lat/lon, `residentialProfile.parkingPolicies`.
- **Vexcel:** ortho site sketch, footprints, DSM minus DTM height, obliques of each face (access, gates, garage ramps), `pool.*`, `roof-objects.solar.*` (a PV hazard for ventilation), `hardscapes`, `parcel-tree-cover`.
- **Matterport:** per-floor-plan unit layout (wall graph), doorway widths, ceiling heights, panos for a "what's inside unit type B2" card.
- **The combination.** No single source answers "is this a high-rise, where do we stage, what's inside a typical unit, and is there PV on the roof". The plan only exists once all three are reconciled.

**Visible reasoning moment.**
1. Hypothesis from the kit: `numStoriesAboveGrade` = N, so the building is under 75 ft and needs no high-rise plan.
2. Vexcel DSM minus DTM gives a height that implies more floors, or the roof holds solar arrays the record doesn't mention.
3. The agent checks the obliques of two faces to count floors, decides whether the DSM spike is a parapet or mechanical penthouse (the standard exempts a mechanical-equipment top floor), and revises the classification and the plan sections it has to fill.
4. A second conflict: Matterport geolocation puts a unit scan some distance from the building. The agent re-anchors the scan to the kit coordinates before placing it on the site sketch.

**Exact external action in the demo.** After the officer approves the card, Gmail sends the plan PDF plus a shared Drive folder (site sketch, unit cards, evidence log) to the **consulted fire officer's real address**. Every page is labelled "DEMO: Houston sample property, generated from sponsor data, not for operational use". A Calendar invite proposes a 15-minute review call. Staged only: a filled HFD high-rise plan cover sheet, stopped before any submit.

**Why it's safe and ethical.** The recipient opted in. No city system is touched. The plan contains building geometry, not personal data. Sponsor data goes only to one consenting reviewer, by private share (confirm with CoStar that this is allowed; **unverified**).

**Who to consult this weekend.** The town fire department, reachable in person on Saturday (company names and contacts **unverified**). Or the university fire marshal / EHS office.
- Geography bridge: they pre-plan Princeton apartment complexes. We show the workflow on Houston/LA data because that is where the scans exist, and ask whether the format would work on their buildings with their own scans.
- Three questions:
  1. What does your current pre-plan for an apartment complex contain, and how long does one take to make?
  2. Which fields go stale fastest, and which have burned you on a call?
  3. Would interior unit layouts help or clutter the plan, and what format does your MDT or tablet accept (PDF, image, a specific software)?

**2-minute demo beats.**
1. (0:00-0:15) The officer's quote and the obligation.
2. (0:15-0:45) Pick a Houston community. The planner writes its todo list, and subagents (record, aerial, scan) report back.
3. (0:45-1:15) The conflict card: kit stories vs DSM height, oblique floor count, revised classification. Then the scan re-anchoring.
4. (1:15-1:40) The plan PDF: ortho sketch with staging, roof PV, unit B2 layout with pano.
5. (1:40-2:00) The approval gate, then the email lands on the officer's phone.

**Biggest risk.** Fire officers may say interior unit layouts are irrelevant (all units look alike) and what they need is standpipes, FDCs and hydrants. None of those are in any layer: there is no object detection, and Vexcel found 0 for "light pole"-type queries.

**Cheapest kill test.** A 10-minute call with one fire officer, asking whether they would use a plan that has no hydrant or FDC locations. Plus one `elements/detect "fire hydrant"` call on a kit property.

**Confidence: 55.**

---

### Idea 2: Groundtruth, a record-correction agent for the built-world graph

**Pitch.** The agent audits property records against the building itself. Each time the record, the aerial and the scan disagree (stories, height, coordinates, footprint, unit size, mismatched scan linked), it writes a correction ticket with the evidence attached and files it with the data owner after a human approves.

**User and obligation.** CoStar's research team and Matterport's data team. CoStar sells "census-style" accuracy, and when records and reality drift apart every downstream join is affected. Our own profiling found places where linked ids, model coordinates, height and vacancy fields, and footprint sizes did not line up across sources.

**Outside-world pressure.** Every customer, broker or lender who acts on an out-of-date record. Concretely this weekend: the sponsor engineers on site own these datasets.

**Data layers and what the combination gives.** A record field is a claim, and each claim has a natural witness in another layer:
- stories and height ↔ DSM/DTM plus oblique floor count;
- GBA and footprint ↔ Vexcel footprint on the newest collection;
- `minSquareFeet` / `numBeds` per plan ↔ Matterport `areaFloor` sum plus bedroom classifications;
- model lat/lon ↔ kit lat/lon ↔ Vexcel parcel hit;
- linked scan ↔ the scan's `generatedDescription` and room types vs `propertyType`.

Only the triangulation tells *which* source is out of step. Two agreeing witnesses outvote the third.

**Visible reasoning moment.**
1. Hypothesis: "Record says 3 stories, but DSM height suggests 6, so the record is out of date."
2. The agent pulls a second Vexcel collection and the obliques. The tall pixels are an adjacent tower bleeding into a parcel footprint taken from an older collection.
3. It re-selects the newest collection, re-extracts the height, and gets agreement with the record. The ticket is **withdrawn**, and the log shows why.
4. The next property survives the same check, so the ticket is kept with three witnesses attached.

Withdrawing a ticket is the proof that the agent's verification loop actually works.

**Exact external action in the demo.** After the reviewer approves the card, the agent opens a GitHub issue in a **private** repo shared with the consulted CoStar or Matterport engineer. The issue holds the field, the record value, the witness values, image crops and a confidence score. It also sends a Gmail summary to that engineer.

**Why it's safe and ethical.** The data owner asked for the tickets. Nothing goes public, which matches the sponsor-data rule, and corrections are only proposed, never applied.

**Who to consult this weekend.** CoStar, Matterport and Vexcel engineers are on site all weekend. Ask them in person at the event.
- Geography bridge: none needed, because the business is in the room.
- Track-fit risk: the judges may see a sponsor as a weaker "real business" than a laundromat. Say so plainly.
- Three questions:
  1. How do record corrections reach research today, and what evidence does a researcher need to accept one?
  2. Which fields cost you most when out of date?
  3. Would you rather get 20 high-confidence tickets or 200 ranked ones?

**2-minute demo beats.**
1. (0:00-0:15) "Mismatched ids and scans placed away from their buildings: found by our agent, confirmed by your engineer" (quote).
2. (0:15-0:50) A batch of 20 properties, with the planner and witness subagents in parallel.
3. (0:50-1:20) The withdrawn ticket: hypothesis, second collection, oblique, retraction.
4. (1:20-1:45) A kept ticket: three witnesses side by side (DSM, oblique, scan floor plan).
5. (1:45-2:00) Approval, then the issue appears in the private repo the engineer is watching.

**Biggest risk.** Judges may see it as "data cleaning", not a real-world problem. The CoStar track also asks for something new about the built world, and auditing their own data may read as inward-looking.

**Cheapest kill test.** Ask one CoStar engineer in person: "If we filed evidence-backed correction tickets, would anyone look at them?" A "no" or a shrug kills it.

**Confidence: 60.**

---

### Idea 3: Golden Hour, a location-scout agent

**Pitch.** A low-budget production gives a shot list ("west-facing living room, at least 4 m deep, high ceiling, direct sun at 5 pm, base camp for 2 vans within 50 m"). The agent finds matching apartment units, proves the sun actually reaches the window by casting DSM shadows, and sends a scout deck plus a pre-filled MyFilmLA draft.

**User and obligation.** An indie or student producer, or a location manager. Before any shoot they owe a location list, tech-scout plan and permit (FilmLA: base camp and crew parking listed per location; 3-7 business days to process).

**Outside-world pressure.** Permit lead time, and sunlight. A room that faces west but sits in a neighbour's shadow at 5 pm wastes a shoot day.

**Data layers and what the combination gives.**
- **Matterport:** room `dimensions` and `ceiling`, window openings with `relativeCenter` on the wall graph, rotated to true north through the model's ENU `geocoordinates` (verified on the residential sample; some commercial models lack geolocation), and panos plus defurnished views for the look.
- **Vexcel:** DSM of neighbouring structures for the shadow at the shoot date and time, obliques of the facade to confirm the window, and `hardscapes` / car detection for base-camp space.
- **Kit:** property type, `numStoriesAboveGrade`, unit floor plan link, `propertyManagementCompanyName`.
- **The combination.** Window direction alone (scan) is not light. Light needs the scan's window direction plus the aerial's surrounding heights plus the unit's floor (kit or scan).

**Visible reasoning moment.**
1. Hypothesis: "Unit A, living room window faces 268° (scan), so it gets direct sun at 5 pm."
2. A DSM shadow cast at that sun azimuth and altitude shows a 6-storey neighbour blocking the window below floor 4.
3. The agent checks which floor the unit is on. The scan's floor index is low.
4. It revises: it drops unit A and promotes unit C on a higher floor in the same community, then confirms with an oblique that the window is on that face.

**Exact external action in the demo.** After approval, the agent creates a Google Slides scout deck (pano stills, floor plan, shadow map, base-camp ortho), shares it with the **consulted producer**, and sends a Calendar hold for a tech scout. MyFilmLA is staged only: a JSON/PDF draft with the location, base-camp and crew-parking entries, and no submit, because a fee and insurance are required.

**Why it's safe and ethical.** Only the consenting producer receives it. Nothing goes to FilmLA or to property managers (their kit emails are placeholders anyway). The deck uses listing scans that were already published for marketing.

**Who to consult this weekend.** A campus student film group or a campus film course instructor (group names **unverified**), or an LA-based indie producer reached via LinkedIn or email from the team's network. 18-hour reachability is uncertain.
- Geography bridge: we only find LA locations, so a campus club acts as a proxy user. An LA producer is the honest user, but harder to reach.
- Three questions:
  1. How do you scout today, and what kills a location after you've picked it?
  2. Would sun and shadow at the call time change your pick?
  3. What does a location manager need in a scout packet to say yes?

**2-minute demo beats.**
1. (0:00-0:15) The shot list.
2. (0:15-0:45) Candidates from the scans (rooms, ceilings, window bearings).
3. (0:45-1:20) The shadow cast kills unit A, and unit C is promoted (oblique confirms).
4. (1:20-1:45) The scout deck in Slides and the base-camp ortho.
5. (1:45-2:00) Approval, the share to the producer, and the FilmLA draft shown but not sent.

**Biggest risk.**
- Window `relativeCenter` + ENU rotation → true bearing is unverified. If the rotation convention is off, every bearing is wrong.
- Window openings appear on only a few commercial sample models.
- It may read as a cousin of the excluded "space finder" ideas.

**Cheapest kill test.** Take one residential model with windows, compute the window bearing, and check it against the Vexcel oblique that should show that facade. One hour.

**Confidence: 45.**

---

## Which one to bet on

**Idea 1 (PrePlan)**, provided the 10-minute fire-officer call does not kill it:
- Its action goes to a real, independent, local organization with a duty to keep these plans.
- The "real business" track story is the cleanest: a local public-safety operator, consulted in person in Princeton.
- All three layers carry weight in the deliverable.

**Idea 2** is the safer fallback on data use and on access to the business (the engineers are on site). Its weakness is the "so what" for general judges.

## Sources (web, 2026-11-13)

- [Houston 311 how-to](https://311.houstontx.gov/howtouse.html)
- [MyLA311 FAQ](https://lacity.gov/myla311/myla311-frequently-asked-questions)
- [LADBS Soft-Story](https://ladbs.org/services/core-services/plan-check-permit/plan-check-permit-special-assistance/mandatory-retrofit-programs/soft-story-retrofit-program)
- [LAFD Fire Zone](https://lafd.org/fire-zone)
- [HFD business info](https://houstontx.gov/fire/business-information/index.html)
- [HPC fire access deck](https://www.houstonpermittingcenter.org/sites/g/files/nwywnm431/files/2025-11/Session%201%20-%20Rm%20CD%20-%20Fire%20Access%20Compliance%20-%20HFD%20-.pdf)
- [Houston High-Risk Apartment Inspection Program (news)](https://www.click2houston.com/news/local/2026/07/31/houston-launches-high-risk-apartment-inspection-program-to-target-repeat-safety-violations/)
- [NFPA 1660 overview](https://www.emergent.tech/blog/nfpa-1660)
- [LADWP Consumer Rebate](https://ladwp.com/residential-services/programs-and-rebates-residential/consumer-rebate-program)
- [FilmLA applying](https://info.filmla.com/applying-for-a-film-permit)
- [LA County decline-in-value](https://lacounty.gov/2026/07/30/decline-in-value-review-forms-available-now/)
