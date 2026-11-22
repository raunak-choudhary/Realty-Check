# Perspective: first-principles thinker

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Inputs read: the team's capability notes and the event briefing. Web search was used only to check that outside datasets and consultable organisations exist. Anything not checked is marked **[unverified]**.

## (a) Reasoning chain

1. **The primitive.** Someone must commit money, people or safety to a building **they are not standing in**, and must do it before they can visit. Today they close the gap in one of three ways: (i) a site visit, which costs time and travel, (ii) a phone or video walkthrough from the occupant, which is slow and depends on the occupant, or (iii) a guess plus a contingency margin, which is how it goes wrong.
2. **The facts that cannot be reduced further.**
   - Inside: room sizes, door and window openings, number of floors, where people sleep.
   - Outside: height, roof, access for vehicles, what stands next to the building, water sources.
   - Record: what the building is, how many units, who manages it, when it was built.
   The kit holds all three layers for the same address. That only matters if the user's decision needs at least two of them at once.
3. **Who has a recurring version of the decision, and something in the outside world forcing it?**
   - **People who respond to buildings:** fire departments write pre-incident plans (NFPA 1620) for buildings they will enter blind, at night, under smoke. The pressure is life safety.
   - **People who move things into or out of buildings:** movers quote a binding or not-to-exceed price for a building they have not seen. Underquoting loses money and overquoting loses the job.
   - **People who rent buildings for a few days:** film and photo productions scout locations. The pressure is a fixed shoot date.
4. **What ends the workflow.** A plan handed to the crew, a quote sent to the customer, an inquiry sent to the property manager. Every idea below ends in one of these, behind an approval gate.
5. **What the data cannot do.** It has no traffic, no demographics and no object detection inside scans. Commercial Property Insights coverage is partial. Most scans are of apartment units, not of hallways or stairs. So each idea is built on apartment-unit geometry plus the parcel seen from the air, which is where the data is densest.

## (b) Raw candidates

| # | Candidate | Verdict |
|---|---|---|
| 1 | **Fire pre-incident plan builder**: unit geometry, rescue windows, height, roof hazards, hydrants | **KEEP** |
| 2 | **Remote moving-quote surveyor**: floors, carry distance, truck parking, door widths, room count | **KEEP** |
| 3 | **Film/photo location scout**: room size, ceiling, window light direction, basecamp parking, manager contact | **KEEP** |
| 4 | Fair rent split between roommates from room area, windows and DSM shading | Drop. No business to consult under the Peri track, and the action (a Splitwise or sheet post) is weak |
| 5 | LA soft-story retrofit / SB 721 balcony-inspection screener from obliques plus year built | Drop. No consultable user near Princeton; too close to the excluded insurer inspection and portfolio monitor |
| 6 | Rooftop solar lead generation for MF owners | Drop. Matterport adds nothing, and it is the sponsor PDF's own idea |
| 7 | Fiber ISP multi-dwelling make-ready survey | Drop. Riser and telecom rooms are not in the scans; no local ISP to consult |
| 8 | EMS stretcher-path planner (door widths plus elevator plus parking) | Merge into #1 as a module. Doors are on units only, not the egress path |
| 9 | Pest-control or HVAC service-route quoting from roof AC count plus unit count | Drop. Vexcel `rooftop hvac unit` returned 0; `ac-unit.count` exists but the interior adds little |
| 10 | Wedding and event venue scout | Drop. The data has almost no venue-type scans (no restaurant or event taxonomy) |

## (c) Best 3

---

### 1. PrePlan: an agent that drafts fire pre-incident plans

**Pitch.** Give it an address in Houston or LA and it drafts an NFPA 1620-style pre-incident plan for a multifamily building: height and floors, unit layout, where the bedrooms are, which windows are big enough for rescue, roof hazards, the nearest hydrants and water. It shows every place where the sources disagree, and it sends the plan to the company officer only after a human approves.

- **User and obligation.** The fire marshal or company officer responsible for preplans in their district. NFPA 1620 recommends preplans for target hazards such as multifamily buildings. Many volunteer and combination departments treat preplanning as "when time permits" (Fire Engineering, see sources).
- **Outside pressure.** Life safety. The town's own fire department has a volunteer shortage and moved to a paid/volunteer combination (Town Topics, 2019; a 2024 article). Preplans are labor someone has to find time for.
- **Data layers and what the combination gives.**
  - CoStar: `propertyType`, `numStoriesAboveGrade`, `constructionEvents` (year built), `propertyApartment.totalNumUnits`/`models[].numBeds`, `parking[]`, property manager name on listings.
  - Matterport (unit scans): `rooms.classifications` to find bedrooms. `openings` gives windows by `width`, `height` and `lowerElevation`, which identify rescue windows by sill height and size. `floors` gives the floor count inside the scan, and `ceiling` gives ceiling heights.
  - Vexcel: DSM minus DTM for real height; `roof-objects.solar.*` because solar panels are a ventilation and shock hazard; `pool.detected` as a drafting water source; obliques for exterior stairs and gates; `elements/detect` "fire hydrant" **[label untested]**.
  - Open data: Houston Water hydrant layer (`wHydrant` FeatureServer) and LA County Fire's hydrant layer, which is non-authoritative and approximate. The City of LA layer is **[unverified]**.
  - **What only the combination gives.** The record says what the building should be. The air says how tall it really is and what is on the roof. The scan says where people sleep and which windows a ladder can use. No single layer answers "where do we put the ladder, and to which room."
- **Visible reasoning moment.**
  - CoStar says `numStoriesAboveGrade` = 3.
  - DSM minus DTM says the roof sits at a height that implies more floors.
  - Hypothesis A: the record and the building have drifted apart. Hypothesis B: there is a parking podium or a mechanical penthouse.
  - The agent pulls the south oblique and sees a ground-level garage, then checks `parking[].parkingType` to confirm it.
  - It revises: "3 residential floors over 1 parking level. Ground ladders reach the floor 2 bedroom windows only from the east side, where there is no garage." It then flags the bedrooms whose windows have a sill too high or an opening too small as "interior rescue only."
  - Second conflict: the open-data hydrant is 60 m away, but SAM3 detects one at the curb that the layer does not list. The plan reports both, with confidence, and asks the human which to trust.
  - (The specific numbers in this example are placeholders until real buildings are run.)
- **External action.** After approval, the plan PDF (map, oblique, floor plan with bedrooms and rescue windows marked) is emailed to the officer, or posted to a shared drive or a Slack channel. The second job on the same harness is to **re-check every plan when a new Vexcel collection lands** and send a diff.
- **Who to consult and how the geography gap is bridged.**
  - The town fire department (combination volunteer/paid), which has a university associate-member program for staff volunteers. A student volunteer firefighter is also possible; the student newspaper has covered student volunteer firefighting, so a student contact is **[unverified]** but likely.
  - A town firehouse can be walked to on Saturday, or the university fire marshal (Environmental Health & Safety) can be reached.
  - The gap: the problem and the plan format are the same in New Jersey and in Houston or LA. They review a generated plan for a Houston building and mark what they would use. Vexcel returns 403 for Princeton, and we say so plainly.
  - Three questions:
    1. What is on your preplan template today, and which fields take the longest to fill?
    2. Would you trust aerial height and roof-solar flags, and in what form do they need to arrive (PDF, tablet, CAD) so the crew actually opens them?
    3. Show us one preplan. Which three facts on it did you need and not have the last time you went into a building?
- **2-minute demo.**
  - 0:00-0:15: The problem, with a quote from the Princeton officer.
  - 0:15-0:45: Enter an LA MF address. The plan panel fills as the agent works: record, then DSM, then oblique.
  - 0:45-1:15: The height conflict appears; the agent forms hypotheses, pulls the oblique, and revises. The SDK flies to a bedroom and highlights its rescue window.
  - 1:15-1:40: The hydrant conflict. The human picks the source to trust at the approval gate.
  - 1:40-2:00: Approve; the email with the PDF arrives on screen.
- **Biggest risk.** Unit scans are of single apartments, not the corridor or stair. The plan would show a typical unit, not the egress path. Also, the officer may say height and roof flags are not what they lack.
- **Cheapest test that kills it.** Show the Princeton officer a hand-made mock (one page: oblique, DSM height, one unit floor plan with rescue windows marked). If they say "we don't use unit layouts," pivot or drop. Second test: in 20 minutes, check that 10 MF buildings have unit scans with `openings` that include windows.
- **Confidence: 62.**

---

### 2. QuoteWalk: an agent that surveys a home remotely for a moving quote

**Pitch.** A mover has to quote a move without a site visit. The agent reads the origin building from the record, the scan and the air: the floor the unit is on, the walk-up or elevator, how far the crew carries from where the truck can park, door widths, rooms and furnishing level. It drafts the estimate line items with a written reason for each, and sends the quote after the estimator approves.

- **User and decision.** The estimator at a local moving company, who quotes many jobs a week. The local office of a national moving franchise says its in-person consultations have moved to virtual walkthroughs over FaceTime, Zoom or Google Duo (web search). That is the exact gap this idea fills.
- **Outside pressure.** Quotes are competitive and time-boxed. A missed long carry or stair fee comes out of margin, and in NJ public movers are regulated (the regulation is linked from that mover's page).
- **Data layers and what the combination gives.**
  - CoStar: `numStoriesAboveGrade`, `apartmentStyleType` (garden, mid-rise, high-rise), `parking[]`, plan `numBeds`/`minSquareFeet`, property manager name (for the loading-dock or elevator booking).
  - Matterport: room count and areas, `openings` door widths, `floors`, and furnished panos for an item-volume estimate. The volume estimate needs our own vision model, which is a risk.
  - Vexcel: ortho for truck parking (curb versus lot), the distance from the curb to the building entry, obliques for exterior stairs, and `car` detection for how full the lot is.
  - **What only the combination gives.** Carry distance and stair count come from the record plus the air. Volume and door clearance come from the scan. A mover needs all of them in one quote.
- **Visible reasoning moment.**
  - The record says garden style with 2 stories, so the agent assumes a ground-floor or one-flight carry.
  - The scan's floor index shows the unit on floor 2. The oblique shows an exterior stair on the far side from the lot entrance, and the ortho shows the nearest open curb is behind the building.
  - It revises: adds a stair line and a long-carry line, and reasons that a 26 ft truck cannot enter the lot (gate seen in the oblique).
  - Then a door the scan measures under 0.75 m conflicts with the "sectional sofa" seen in the pano. It adds a "disassembly" line and a question to the customer.
- **External action.** After approval, the agent emails the quote PDF to the customer, or books a confirmation call on a calendar.
- **Who to consult and how the geography gap is bridged.**
  - The local office of a national moving franchise (reachable by phone Saturday), or a local independent mover.
  - The gap: their quoting process is the same nationally. They price one of our LA/Houston units using our packet and compare it with their usual virtual walkthrough.
  - Three questions:
    1. What do you ask on a virtual walkthrough, and which answers turn out wrong most often?
    2. What do stairs, long carry and truck access each add to a quote, and how do you decide them today?
    3. Would you send a quote built from this packet, or only use it to prepare the call?
- **2-minute demo.** Customer address in, then the record, scan and air come in one at a time; the conflict and revision; the line-item quote with reasons; approve; the email is sent.
- **Biggest risk.** Item-volume estimation from furnished panos is our own computer vision and could be badly wrong. Also, scans exist only for listed units, so the customer's own unit is unlikely to be scanned. The honest framing is "a scan of the same floor plan," joined through `models[].attachments`.
- **Cheapest test that kills it.** Ask the mover: "If I give you floor, stair, carry distance and door widths but no inventory, is that worth anything?" If no, drop it.
- **Confidence: 55.**

---

### 3. ScoutLine: an agent that shortlists film and photo locations and sends the inquiries

**Pitch.** A production describes a scene, for example "a cramped 1970s 2BR, west window with late-afternoon light, room for a camera dolly, a crew basecamp nearby." The agent searches LA/Houston scans and records. It tests each candidate against the brief with interior geometry, the sun and shade from the DSM, and parking seen from the air. Once a human approves, it sends a location inquiry to each property manager named in the kit.

- **User and decision.** A location scout or producer choosing where to shoot. LA is the core market for film.
- **Outside pressure.** A fixed shoot date and a crew day-rate. Scouts drive to many places to reject most of them.
- **Data layers and what the combination gives.**
  - CoStar: year built, `apartmentStyleType`, property manager on listings, `parking[]`.
  - Matterport: room `dimensions` and `ceiling` (camera and dolly clearance); window `openings` and the pano rotation (which way each window faces, using `geocoordinates` rotation); defurnished views ("empty set" for the art department); SDK screenshots as a lookbook.
  - Vexcel: DSM of the buildings next door (does anything block the low western sun?), ortho/oblique for basecamp parking area and facade look.
  - **What only the combination gives.** The scan says a window exists and faces west. The DSM says whether the sun reaches it. The record says who to ask.
- **Visible reasoning moment.**
  - The scan shows a large window, and the pano rotation puts it facing west, so the hypothesis is "golden-hour light."
  - The DSM shows a taller structure about 15 m west **[illustrative]**. The agent computes the sun angle for the shoot date and finds the window shaded at that hour.
  - It rejects the unit and promotes candidate #4, then checks #4's basecamp. The ortho shows a large surface lot, but the `car` count in the newest collection says the lot is full most of the time. It flags a parking risk and asks the human.
- **External action.** After approval, location inquiry emails go to property managers. Kit emails are placeholders on an example domain, so the demo sends to a team inbox standing in for them and says so. The lookbook page is published.
- **Who to consult.** A campus student film group, or a local indie production **[name unverified]**. Questions:
  1. What brief do you get, and what kills a location on the first visit?
  2. Would sun and shade at the shoot hour change your shortlist?
  3. Who do you contact first, and what does that first message need to say?
- **2-minute demo.** Brief in; 20 candidates narrowed to 5; the sun conflict and the revision; the lookbook of SDK screenshots plus the defurnished room; approve; the inquiries are sent.
- **Biggest risk.** The Peri-track user (a student film group shooting in NJ) does not need LA locations. The fit is weak, and window orientation from scan rotation is untested.
- **Cheapest test that kills it.** Compute one window bearing from `geocoordinates` and check it against the oblique by eye. If they disagree, the hero metric dies.
- **Confidence: 40.**

---

## Bet

**PrePlan (#1).**
- Of the three, it has the strongest outside pressure (life safety, a recurring duty), and the users who own the problem are within walking distance this weekend.
- Every layer is load-bearing:
  - the record gives what the building should be;
  - the DSM, oblique and roof objects give what it is;
  - the scan gives bedrooms and rescue windows;
  - open hydrant data gives water.
- Conflicts between those layers are common, so the reasoning moment is real, not staged.
- The second job on the same harness (re-check plans when a new Vexcel collection lands) is nearly free.

Run the kill test (the Princeton officer reviews a mock) Saturday morning before building.

## Sources (web checks)

- Houston hydrant layer: https://services.arcgis.com/NummVBqZSIJKUeVR/ArcGIS/rest/services/wHydrant/FeatureServer
- LA County Fire hydrants (non-authoritative): https://services.arcgis.com/RmCCgQtiZLDCtblq/ArcGIS/rest/services/LACoFD_Fire_Hydrants/FeatureServer
- Town fire department volunteer shortage (local news): https://towntopics.com/?p=44750 ; https://communitynews.org/?p=318147
- University associate-member firefighters: https://www.princeton.edu/news/2013/01/03/university-volunteer-firefighters-help-campus-and-community
- Preplanning in volunteer departments: https://www.fireengineering.com/firefighting/the-professional-volunteer-fire-department-part-9-preplanning/
