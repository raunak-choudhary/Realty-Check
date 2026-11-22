# Perspective: skeptical judge and demo director

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Read only: the team's data-capability notes, the hackathon information, and skims of the deepagents and Matterport SDK documentation. Every data fact below comes from the capability notes. Anything else is marked **[unverified]**.

---

## (a) Reasoning chain

1. **What the judge actually gets.** About 2 minutes at a table, three or more judges in a row, 80+ teams. The judge remembers at most one image and one surprise. Most agent demos are a chat box, a spinner and a markdown report, and those all blur together.
2. **What sticks:**
   - something physical-feeling: a 3D interior and the aerial of the same building, side by side;
   - the agent visibly changing its mind;
   - something arriving on the judge's own device.

   I design that moment first, then check that a real person needs it.
3. **Clichés to avoid:**
   - "chat with your property";
   - an AI virtual-tour Q&A (on Devpost, "AI Virtual Tour" tried to pull images out of Matterport tours);
   - virtual staging;
   - "the agent drafts an email to a broker". Broker emails in the kit are placeholders, so that email can never really be sent;
   - the sponsor PDF's own ideas (roof triage, solar potential, wildfire defensible space, find-more-like-this). CoStar judges have seen their own list;
   - the AI tutor or AI workspace pattern. The past HackPrinceton winner I could find was an AI learning workspace that also won Amazon's Practical AI prize (season not confirmed). Main-track judges reward a clear human beneficiary, which is the "Charity" criterion.
4. **Past real-estate hackathon winners** (NAR 2018 KW Labs room tagging, Anywhere 2024 offer-comparison tool, eXp 2024 OpenAI apps) were agent-productivity tools. None fused interior 3D with aerial. That fusion is the opening CoStar's track asks for: an unexpected use of its data.
5. **The constraints that kill most ideas:**
   - Contact info in the kit is placeholder data, so the external action has to go to a real person we consulted or to the judge. It cannot go to a CoStar contact.
   - Scans are mostly apartment units and amenity rooms (most kit-linked scans are Multifamily).
   - Detailed geometry is complete on residential models and on only some commercial ones.
   - The Peri track needs a real business in Princeton this weekend, while the data is in Houston and LA. The honest bridge is a user whose workflow is the same everywhere: the consultee reviews our Houston/LA output as if it were their own district.
6. **The spatial facts with the most leverage:**
   - DSM minus DTM gives real building height (measured on a tall building), to set against `numStoriesAboveGrade`.
   - Four oblique directions match how fire crews already name building sides (A/B/C/D).
   - Window openings have `width`, `height` and `lowerElevation` (windows on most residential sample models).
   - Imagery history back to 2016 shows things added later, such as `roof-objects.solar.*`.
   - Defurnished views exist.

   Together these point at **emergency pre-incident planning**. It is a real, public-good workflow that is underdone, nobody at a real-estate hackathon builds it, and the user (a volunteer fire or rescue squad) is reachable in Princeton this weekend.

---

## (b) Raw candidates

| # | Candidate (one line) | Status / kill reason |
|---|---|---|
| 1 | **Pre-incident plan agent** for fire/EMS: builds the building "pre-plan" (sides A-D from obliques, true height from DSM, roof hazards such as solar, sleeping rooms and rescue-window sizes from the scan, occupancy from CoStar units). Pushes it to the crew's phones after an officer approves | **KEEP (bet)** |
| 2 | **Film/photo location scout** for LA: matches a script page (west light at golden hour, ceiling for lighting, empty room) to scanned units and amenity spaces; checks crew parking and base camp from ortho; sends the request and books a tech-scout hold | **KEEP** |
| 3 | **Group event venue check** for a Princeton alumni/club event in Houston or LA: the claimed capacity is checked against occupant load (scan area ÷ code factor), the count of exit doorways, and the drop-off zone from the air. Sends the inquiry and a calendar hold, and posts a poll to the club | **KEEP** (and doubles as the "second job" on the harness for #1) |
| 4 | Fixed-wireless ISP line-of-sight: DSM rooftop-to-window LoS plus unit window openings, then books an install | Killed: no consultee reachable this weekend, the Peri track fit is weak. A good spatial idea worth parking |
| 5 | Fair rent split between roommates from room area, windows and private bath (scan) plus plan rent (CoStar) | Killed: Vexcel would be decoration, and it sits close to the excluded apartment ideas |
| 6 | Mural/blank-wall finder for LA arts nonprofits using obliques, with the owner from CoStar | Killed: owner contacts are placeholders or missing, Matterport goes unused, and the reasoning is shallow |
| 7 | Intern housing for Princeton students going to Houston/LA | Killed: too close to the excluded apartment listing-vs-reality and space-hunter ideas |
| 8 | HVAC tonnage and rooftop-unit quote (aerial `ac-unit.count` plus scan volume) | Killed: too close to the excluded contractor bid from scan |
| 9 | Hurricane-season resident outreach in Houston using Harvey-2017 imagery | Killed: overlaps the excluded flood simulation and condition monitor |
| 10 | Wildfire defensible-space audit for LA homes | Killed: a cliché straight from the sponsor PDF, and the interior adds little |
| 11 | Census/canvass route planner for apartment complexes | Killed: no gate or entrance data, and no real consultee |

---

## (c) Best three

### Idea 1: PREPLAN, a pre-incident planning agent for fire and rescue crews (MY BET)

**Pitch.** The agent builds the one-page pre-incident plan a fire or rescue crew should have before they pull up to a building. It checks the building record against what the aerial imagery and the 3D scan show, and after the officer approves, it pushes the plan to the crew's phones.

**User and their obligation.**
- The user is a company officer or pre-plan coordinator at a volunteer fire company or rescue squad.
- Departments are expected to keep pre-incident plans for target occupancies such as multifamily buildings. NFPA 1620 is the standard. **[unverified: how it is applied locally, and whether ISO ratings credit it]**
- Volunteers do this by hand, if they do it at all.
- The decision is which buildings get a pre-plan, and what goes on it: aerial or standpipe operations, which side to stage on, roof hazards, and where people sleep.

**Outside-world pressure.**
- A fire does not wait.
- Records go stale. A building gets rooftop solar after the record was written, a garage is added, or the story count no longer matches the building. Records and reality can drift apart.
- The crew needs the true picture before arrival, not during it.

**Data layers, and what only the combination gives.**
- **CoStar:**
  - `numStoriesAboveGrade`;
  - `constructionEvents` (year built);
  - `propertyApartment.totalNumUnits` and floor plans (occupant estimate);
  - `parking[]`;
  - `residentialProfile`;
  - `propertyContacts[]` with the property manager's name. The names are real; the email and phone are not used.
- **Vexcel:**
  - DSM/DTM true height;
  - four obliques labelled as sides A-D;
  - `roof-objects.solar.*`, `skylight.count` and `roof-characteristics`;
  - `pool.detected` (a static water source);
  - `car` detection to show staging space at the newest collection;
  - collection history to say when something appeared.
- **Matterport:**
  - unit layout with bedroom classifications, so the plan knows where people sleep;
  - window openings `width/height/lowerElevation`, to judge whether a window can serve as a rescue/bailout opening;
  - doorway widths, for stretcher egress;
  - defurnished panos give a clean view of an interior layout.
- **What only the combination gives:**
  - Height alone means nothing; set against stories it exposes a record that has drifted.
  - A window size alone means nothing; set against the floor's height above grade (from DSM and stories), it tells you whether a ground ladder reaches it.
  - A record alone cannot know about solar panels added in 2023.

**The visible reasoning moment.**
- **Hypothesis.** From CoStar: the building has N stories, so the plan is ground-ladder rescue on side A.
- **Test.** The verifier subagent pulls DSM minus DTM, and the measured roof height implies more floors than the record says. **[demo building to be chosen when pre-running; the size of the conflict is unknown until measured]**
- **Revision.** The plan switches to aerial/standpipe and drops the ground-ladder note.
- **Second conflict.** No solar is recorded, but the 2025 collection shows `solar` while the 2018 collection did not. The agent adds "PV on roof: no vertical ventilation over array" and attaches the oblique.

On screen, a "hypothesis ledger" panel shows each claim, its source, a red strike-through when it is contradicted, and the evidence thumbnail: the DSM profile, oblique crops before and after, and the SDK camera flying to the bedroom window, with its measured sill height and size overlaid.

**External action in the demo.**
1. The officer clicks "Approve & distribute".
2. The judge has typed their phone number or email into a field, or scanned a QR code, at the start.
3. The judge's phone receives an SMS or email: "Pre-plan ready: [address], sides A-D, PV hazard, sleeping rooms floor 2-4", with a link to the published one-page plan.
4. The same approval appends a row to the company's shared pre-plan Google Sheet.

The judge holds the output in their own hand. Twilio and the Google Sheets API are standard. **[SMS trial accounts can only text verified numbers. Email is the safe fallback.]**

**Who to consult this weekend, and three questions.**
- **First choice:** a local first-aid squad, or the town fire department. **[unverified: whether either is reachable on a weekend. Both are walkable or phoneable.]**
- **Backup:** a student-run campus EMS group (it would qualify as a student org **[unverified that one exists in this form]**), or the university's EHS / fire marshal's office.
- **The Peri track's "business" wording is a risk for a public agency.** A volunteer squad is a nonprofit organisation; state this plainly.
- **Bridging the geography:** we show them a Houston or LA pre-plan and ask them to critique it as if it were in their district. The workflow is the same everywhere, and the data only covers Houston and LA. A Houston Fire Department or LAFD contact would be better if anyone on the team has one.
- **Evidence:** a photo of their current paper pre-plan form (with permission), or a quote.
- **Q1:** What is on your pre-plan today, and how many of your target buildings actually have one?
- **Q2:** When you pull up, what have you been wrong about before (height, roof, where people are)?
- **Q3:** Who approves a pre-plan, and how does it reach the rig: binder, tablet, or text?

**2-minute script.**
- **0-15 s:** "Firefighters are supposed to pre-plan buildings. Volunteers rarely can." Then the consulted squad's own words about their pre-plans. Judge enters their phone number.
- **15-30 s:** Split screen. Matterport 3D of a unit on the left, Vexcel ortho on the right with the A/B/C/D sides drawn. The agent's plan (todo list) is visible.
- **30-60 s:** Resume a pre-run checkpoint. The hypothesis ledger fills. The DSM verifier subagent returns, a line turns red, and the plan rewrites itself. Then the solar 2018 vs 2025 oblique flip.
- **60-80 s:** The SDK flies to a bedroom window. Its size and sill height are overlaid, and the agent marks it as a rescue window or not. The camera cuts back to the plan.
- **80-100 s:** The approval gate shows a diff of exactly what will be sent. Click approve. The judge's phone buzzes. Show the sheet row.
- **100-120 s:** "Same harness, second job." Run the venue-capacity check (Idea 3) on the same tools in 10 seconds from a checkpoint. Close with "Imagery © Vexcel".

**20-second hooks.**
- **CoStar:** "Your record says N stories; your own aerial DSM says more, and your scans show where people sleep. We turn the three layers into the document a fire crew reads on the way, and the conflicts between them are the point."
- **Peri track:** "We walked into a local rescue squad and saw how they keep pre-plans today. The officer approves, the crew's phones get it. Here is their critique of our first version and what we changed."
- **LangChain:** "deepagents with source subagents, each with isolated context, a verifier subagent that has to confirm every claim, a hypothesis ledger in the virtual filesystem, `interrupt_on` before any send, and checkpoint resume. Here is a second job running on the same harness."
- **Amazon:** "Practical AI that acts. It reasons across imagery and 3D, revises when the data disagrees, and delivers to a phone. One click from a volunteer."
- **Main track (Charity/Utility):** "Volunteer firefighters show up to buildings they have never seen. This gives them the inside, the roof and the hazards before they arrive."

**Live vs pre-run.**
- **Pre-run:** the full agent run on two or three buildings, with Vexcel and Matterport calls cached locally, because signed links expire after about 5 minutes. Saved as a LangGraph checkpoint taken just before the verifier step.
- **Live:** resume from that checkpoint (the verifier step, the ledger update and the plan rewrite), the SDK fly-to (localhost only), the approval click, and the SMS/email and sheet write.
- **Optional live:** a fresh run on a new address, kept in the background.

**Biggest risk, and the cheapest kill test.**
- **Risk:** an apartment-unit scan is one unit, not the building core (stairs, standpipes). Also, the DSM height on the chosen buildings may simply agree with the record, which would mean no conflict to show. A third point: a fire officer might call a pre-plan without stairwells useless.
- **Kill test (1 hour):**
  1. Take 20 Multifamily kit properties that have scans.
  2. Pull DSM/DTM and compute height divided by an assumed 3-3.5 m per floor, then compare with `numStoriesAboveGrade`. Count the real mismatches.
  3. Pull `roof-objects.solar` across collections and count solar that appears in newer collections.
  4. Phone the squad and ask Q1 and Q3.
- If there are no mismatches and no added solar, the reasoning moment is staged, and the idea should be dropped.

**Confidence:** 62.

---

### Idea 2: SCOUT, an LA location-scout agent

**Pitch.** Give it a script page, such as "INT. APARTMENT – golden hour, west light, 2 actors + dolly". It finds scanned LA spaces that physically fit, proves the light and the space, and books the tech-scout once the producer approves.

**User and their decision.**
- An indie or student producer, or a location manager.
- The decision is which locations to scout in person this week, given a fixed number of scout days.

**Outside-world pressure.** The shoot dates are fixed, scout days are expensive, and photos mislead about ceiling height and light.

**Data layers.**
- **Matterport:**
  - ceiling `min/maxHeight` (lighting clearance);
  - room `areaFloor`;
  - window openings, with their position on the wall graph;
  - model `geocoordinates` rotation, which gives window bearing so west light can be checked. **[unverified that the rotation is north-referenced; some commercial models have no geolocation]**
  - defurnished view (an empty set);
  - panos for the mood board.
- **Vexcel:**
  - obliques for the exterior look;
  - ortho `hardscapes` and `car` detection for crew parking and base camp;
  - DSM of neighbours, to see whether a taller building shades the west windows at golden hour (computed from sun angle). **[the shading computation is ours, untested]**
- **CoStar:**
  - year built (period look);
  - `buildingClass`;
  - the property manager's name;
  - amenity scans (amenity/common spaces).

**Reasoning moment.**
- The listing photo and the plan name suggest "sunset view", and the agent hypothesises west light.
- The wall graph plus geo-rotation shows the windows face roughly east, or the DSM shows a taller neighbour to the west.
- The agent rejects the space and promotes the second-ranked unit. The ledger shows the computed sun path against the window bearing.

**External action.**
- On approval, it sends a location request email to the consulted producer's real address (not the placeholder kit contact) with the shot sheet PDF.
- It creates a Google Calendar tech-scout hold.
- In the demo, the judge is invited to the calendar event.

**Consult.**
- A campus student film/theatre group (for example a campus theatre group or a student film society **[names unverified]**), or a local photographer who rents locations.
- **Geography gap:** honestly weak. The bridge is that they critique the LA shortlist as a pre-production exercise. A Princeton alum working in LA production would be better, if reachable.
- **Q1:** What killed a location you scouted in person?
- **Q2:** What do you check first from photos?
- **Q3:** How do you request permission and book a scout?

**2-minute script.**
- **0-15 s:** The script page goes in.
- **15-45 s:** The agent's plan, and candidates from the scans.
- **45-75 s:** The rejection, with sun-path versus window-bearing evidence. The SDK flies to the winning window, and the defurnished toggle shows the empty room.
- **75-95 s:** The ortho shows the base camp area, with the car count as staging evidence.
- **95-115 s:** Approve; the judge's calendar invite arrives.
- **115-120 s:** Close.

**Hooks.**
- **CoStar:** "Your scans know which way a window faces and how high the ceiling is. We sell that to Hollywood."
- **Peri track:** the consulted producer's story of a day lost to a location with a low ceiling, and what they asked for.
- **LangChain:** a subagent per constraint (light, space, logistics), each with its own verifier.
- **Amazon:** turns a creative brief into a booked scout.
- **Main:** Entertainment track fit.

**Live vs pre-run.**
- **Pre-run:** candidate generation and the sun/DSM computation.
- **Live:** resume at the rejection, then the SDK, the approval and the calendar invite.

**Risk and kill test.**
- **Risk:** the scan's orientation may not be north-referenced.
- **Kill test (30 min):** for 5 residential models, compare the window-wall bearing from geo-rotation with the building edges on the Vexcel ortho. If they don't line up, the light claim dies, and with it the hook.

**Confidence:** 45. The Peri track fit and the geography are weak, and the hook rests on one unverified frame transform.

---

### Idea 3: HEADCOUNT, a venue capacity and egress check for a club event

**Pitch.** A Princeton club or alumni group plans an event in Houston or LA. The agent checks whether a candidate venue, such as a hotel event room or a building amenity room, can legally and comfortably hold the group. It then sends the inquiry, holds the date and polls the members.

**User and their decision.** A student org or alumni-association event chair picking a venue for a fixed headcount.

**Pressure.** The event date and RSVP count. Overfilled rooms are a code and safety problem. The advertised capacity is marketing.

**Data layers.**
- **Matterport:**
  - room `areaFloor`, which feeds an occupant-load calculation using the building-code area per person (our formula from the public IBC table **[unverified factor choice]**);
  - the number and width of doorway openings out of the room, for the egress check;
  - ceiling height;
  - defurnished pano for layout.
- **Vexcel:**
  - ortho and obliques for the drop-off curb and garage;
  - `car` detection at the newest collection as a parking-pressure signal (a snapshot, stated as such).
- **CoStar:**
  - hotels (mostly in Houston, with ADR);
  - amenity spaces in Multifamily;
  - `parking[].totalSpaces` and `parkingRatio`;
  - year built.

**Reasoning moment.**
- The venue page or name implies room for 120; the hypothesis is that it fits.
- The scan area gives an occupant load below that, and only one doorway is at least 0.81 m wide.
- The agent revises: split into two rooms, or move to the second candidate. The ledger shows the calculation.

**Action.** On approval, it emails the venue inquiry to the club chair's real address, holds the date in the club calendar, and posts a poll ("Venue A vs B") to the club Slack or Discord. The judge sees the poll post appear.

**Consult.**
- Any Princeton student org planning an off-campus event, or a regional Princeton alumni association officer in Houston or LA **[unverified who is reachable]**. Student orgs qualify for the Peri track explicitly.
- **Geography bridge:** an alumni event in Houston or LA is natively in-geography if the consultee is an alum there.
- **Q1:** How do you pick a venue today?
- **Q2:** Has a room ever been too small or turned you away?
- **Q3:** Who signs off, and where does the decision get announced?

**Script.**
- **0-15 s:** The event brief.
- **15-45 s:** The plan and the candidates.
- **45-75 s:** The capacity conflict and revision, with the SDK showing the room and its doorways highlighted.
- **75-95 s:** Aerial drop-off check.
- **95-115 s:** Approve; the Slack poll appears and the calendar hold lands.
- **115-120 s:** Close.

**Hooks.**
- **CoStar:** "Square footage on a listing vs measured floor area in the scan vs the curb from the air."
- **Peri track:** the consulted club choosing its venue with our agent.
- **LangChain:** the same harness as PREPLAN, reused with new skills only.
- **Amazon:** a group-coordination agent (one of Amazon's own listed examples).
- **Main:** utility for every student org.

**Live vs pre-run.** Same as Idea 1: resume at the verifier step from a checkpoint.

**Risk and kill test.**
- **Risk:** hotel and amenity scans may lack room geometry (commercial Property Insights coverage is partial).
- **Kill test (30 min):** query 20 hotel and amenity models for `rooms.dimensions.areaFloor` and `openings`.
- This idea also overlaps with the excluded accessibility and furniture checks only through door widths. Keep that framing about egress capacity.

**Confidence:** 40 as a standalone project; 70 as the "second job" demo inside PREPLAN.

---

## Harness note (all three)

The harness is a deepagents `create_deep_agent` with these parts:

- **Tool layer:** `costar.*`, `vexcel.{ortho,oblique,dsm,dtm,property,detect}`, `mp.{model,openings,rooms,pano}`, `sdk.flyTo` (via a localhost bridge), and `act.{sms,email,calendar,sheet,slack}`.
- **Subagents with isolated context:** `records`, `aerial`, `interior` and `verifier`.
- **Planning:** `TodoListMiddleware`, which is opt-in in 0.7.x.
- **Ledger:** `/ledger/*.json` in a `FilesystemBackend`.
- **Forced verification:** a rule that no claim can enter the plan unless the verifier has confirmed it against a second source.
- **Approval gate:** `interrupt_on` for every `act.*` tool.
- **Resume:** a checkpointer.
- **Swapping jobs:** done with a new skill file and a new output template.
