# Perspective: agent-harness architect (deepagents judge lens)

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Sources read: the team's capability notes, the event briefing, and the team's notes on deepagents. Two web searches (Princeton student film clubs; LADBS permit data). Every data observation below comes from the team's capability notes. Anything I did not verify is marked **[unverified]**.

---

## (a) Reasoning chain

A deepagents judge asks one question: would a single prompt with tools fail here, and can you show it failing? A harness earns its keep when the problem has one or more of these shapes:

1. **Batch with transferable lessons.** Building 1 teaches something, such as a source quirk, that has to change how building 50 is handled. This needs filesystem memory that persists across runs, and an eval where run 2 beats run 1.
2. **Conflicting sources with no single truth.** Several sources disagree and none settles the question on its own. The kit data has exactly this:
   - Vexcel returns several features per parcel even with `latest=true`, and footprints for one building can vary widely between them.
   - Vexcel calculated roof height can vary widely for one building.
   - `buildingHeightInFeet` contains outlier values.
   - Index coordinates can sit some distance from the building.
   - The `costar_property_id` link between a scan and a record does not always point to the same building.

   A plain agent picks whichever value it reads first. A harness needs an evidence ledger, an adjudicator and an independent verifier.
3. **Context too large for one window.** Each candidate needs dozens of panoramas, floor plans, obliques and DSM tiles. Subagents with isolated context should read the pixels and return only a verdict.
4. **Measurement from pixels checked against records.** Examples: DSM minus DTM height against `numStoriesAboveGrade`, scan `areaFloor` against advertised square feet, and window bearing from the scan against neighbouring buildings in the DSM. A verifier that can only use a different source cannot be skipped.
5. **A case that pauses for a person.** An outside party has to answer before the case can close, so the run must checkpoint, survive the wait and resume on the same `thread_id`.
6. **Advocate against critic.** One subagent argues for a candidate and another argues against it with different tools, so the harness can show who won and why.
7. **Side effects behind gates.** Every outward action goes through `interrupt_on` with approve, edit or reject, an idempotency key and an actions log.

I generated ideas from these shapes first. Then I filtered them through the track's real-business requirement, which is a real business consulted this weekend from Princeton, and through the exclusion list.

---

## (b) Raw candidates

| # | Candidate | Verdict |
|---|---|---|
| 1 | **Ground-Truth Desk.** A batch agent reconciles CoStar property records (stories, height, GBA, year built, pool, parking) against Vexcel and Matterport. It learns source quirks into memory and files verification tickets. | **KEEP (best 3)** |
| 2 | **Film/photo location scout.** It turns a script brief into scouted vacant units and amenity spaces, using pano look, ceiling, doors, window bearing, basecamp parking and owner contact. Director feedback goes into memory. | **KEEP (best 3)** |
| 3 | **Back-structure / ADU legality check.** It tests a listing's claim of a "guest house / ADU" against Vexcel history, the scan's kitchen/bath and public permits. It pauses for the listing agent's answer. | **KEEP (best 3)**, with an overlap caveat |
| 4 | Sun-hours per apartment unit, from scan windows georeferenced against Vexcel DSM obstructions, for leasing offices | Dropped. This is a deterministic geometry pipeline, not an agent problem, so a harness adds little. Kept as a tool idea inside #2. |
| 5 | Multifamily rooftop-solar prospector with owner outreach | Dropped. Matterport plays no role, the PDF pitches this idea to every team, and the work is mostly a scoring pipeline. |
| 6 | Summer-intern housing scout for Princeton students going to LA/Houston | Dropped. It is an apartment finder, which overlaps the excluded hunter, finder and listing-vs-reality ideas, and it needs commute and traffic data that does not exist. |
| 7 | Unregistered short-term-rental detector for LA enforcement | Dropped. It targets private individuals, so the ethics fail. |
| 8 | Lender construction-draw verifier from Vexcel history | Dropped. A limited number of ortho collections over 10 years is too coarse to verify monthly draws. |
| 9 | "Ghost tenant" detector: an occupancy record says occupied, but the scan, the listing and empty-lot car counts say vacant | Folded into #1 as its second job |
| 10 | EV-charger siting and rebate pre-application for apartment garages | Dropped. There is no stall count or lot polygon, and the rebate forms are too heavy to file in 30 h. |
| 11 | Off-market acquisition sourcing (long hold + defects + vacancy, then owner letters) | Dropped. It overlaps the excluded due-diligence and portfolio-monitor ideas, and owner names exist on only a minority of comps. |
| 12 | Unit turnover make-ready scoping from defurnished scans | Dropped. It is the excluded contractor bid from a scan. |

---

## (c) Best 3

### Idea 1 — Ground-Truth Desk: a self-improving record reconciler for building data

**Pitch.** The agent works through a batch of buildings. For each, it measures what the air and the scan say about the building and compares that with the record. It decides which source to trust using rules it learned on earlier buildings. It then files verification tickets with a call script for the researcher.

**User and obligation.** The users are data stewards and researchers at CoStar, whose product is the record. The secondary user is any landlord whose listing data on an aggregator is out of date. The decision is which records to correct, which to escalate for a phone verification and which to leave alone.

**Outside-world pressure.** Brokers, lenders and appraisers price from these fields. Records and reality can drift apart, and the kit already shows outlier values in fields such as `buildingHeightInFeet` and `vacancyPercent`. Researcher time is the scarce resource, so tickets must be precise and ranked.

**Data layers, and what only the combination gives.**
- CoStar fields: `numStoriesAboveGrade`, `buildingHeightInFeet`, `grossBuildingAreaSquareFeet`, `constructionEvents[]` (year built), `parking[].totalSpaces`, pet/amenity policies, `lotSize`.
- Vexcel: DSM minus DTM height, `footprint.area` per collection, `pool.*`, `vehicles.count`, and the ortho collection history from 2016-2026, which shows when the building appeared.
- Matterport: `rooms.ceiling` heights, `Floor.data` count, pool or amenity scan names, and `areaFloor`.
- The combination produces something no single source can. Vexcel gives building height. The scan gives floor-to-floor height (ceiling plus a slab allowance). Together they estimate stories, which can be checked against the record. Vexcel footprint times stories estimates GBA. If the record says year built 2019 but a 2016 ortho shows the building, that is a contradiction no single layer can detect.

**Harness design.**
- **Tool layer.** Every tool returns `{data, source, record_id, retrieved_at}`.
  - `kit_get(property_id)`
  - `vexcel_parcel(lat,lon, collection?)`
  - `vexcel_dsm_height(polygon)`
  - `vexcel_ortho(polygon, collection)`
  - `vexcel_detect(polygon, label)`
  - `mp_model(sid, fields)`
  - `mp_floors_ceilings(sid)`
  - `file_ticket(...)`, `post_slack(...)`, `append_sheet(...)` (actions)
- **Subagents.** All run in isolated mode.
  - `air_surveyor`: Vexcel tools only. It writes `/evidence/vexcel/<pid>.json`.
  - `scan_surveyor`: Matterport tools only. It reads many models per property.
  - `record_reader`: kit only.
  - `adjudicator`: reads the ledger only and proposes a truth with confidence.
  - `verifier`: given a claim, it may use only a source *other* than the one that produced the claim. It returns VERIFIED, CONTRADICTED or UNKNOWN.
  - `ticket_writer`: produces the ticket and the call script.
- **Memory.**
  - `/memories/AGENTS.md` holds source-trust rules learned during runs. Example rule: "Vexcel footprints differ by collection; use the newest, then reject it if it is more than 3x the median of the others."
  - `/memories/quirks/<market>.md` holds market-specific notes, such as "Houston comps are non-disclosure".
  - `/memories/false_alarms.md` is fed from researcher rejections.
  - The `/memories/` route is backed by `StoreBackend`, so it persists across runs.
- **Per-run files.** `/work/plan.md`, `/ledger.jsonl` and `/work/hypotheses.md`.
- **Verifier.** `RubricMiddleware` blocks completion unless every ticket cites two or more independent sources and states its tolerance. A custom pre-completion middleware refuses a ticket whose only evidence comes from the claim's own source.
- **Approval gates.** `interrupt_on` covers `file_ticket`, `post_slack` and `append_sheet`, with approve, edit or reject. An idempotency key on (property_id, field) stops a resumed batch from double-filing. A `SqliteSaver` checkpointer lets a 50-building batch resume after a crash or a rejection.
- **What a single-prompt agent gets wrong.**
  - It trusts the first Vexcel feature it reads, which is any one of several.
  - It takes `latest=true` at face value.
  - It reports height as roof elevation without subtracting DTM.
  - It treats an implausibly low calculated height as real.
  - Its context overflows after about 5 buildings of panos and features.
  - It forgets on building 40 the quirk it learned on building 3.
- **Second job on the same harness: tenancy verification ("ghost tenant").** It asks whether the occupancy record says a tenant is current while a listing advertises the same suite and the lot is empty across collections. This reuses the same tools and adjudicator. The new code is a `listing_reader` subagent and a new rubric.
- **Eval that proves the harness beats a plain agent.**
  - Take N kit properties and inject known corruptions into a copy of the records: stories ±k, year built shifted, pool flag flipped, GBA ×10. Mark the remaining records "unverified-clean".
  - Score precision and recall on the injected errors, and the false-ticket rate on clean records.
  - Compare four setups with the model held fixed: (a) one agent with all tools, (b) the harness without memory, (c) the harness run cold, and (d) the harness run 2 with learned memory.
  - The measured number is the drop in false tickets from run 1 to run 2, produced by the memory file. **Numbers are not produced yet.**

**Visible reasoning moment.**
1. The hypothesis, from the record: 4 stories.
2. The air surveyor says the DSM height is consistent with about 6 stories, so the agent flags a mismatch with the record.
3. The scan surveyor reports a 3.9 m ceiling in a lobby or amenity scan.
4. The adjudicator revises: a tall podium or retail ground floor explains the extra height, so the claim is downgraded to UNKNOWN.
5. The agent writes a new rule to memory: "Do not convert height to stories using a residential floor height when the scan shows a tall ground floor."
6. Building 12 later uses that rule and does not raise the false alarm.

The specific numbers in this example are illustrative. A real case still has to be found.

**External action in the demo.** After approval, the agent creates GitHub issues (or posts to a Slack channel) in a "research queue". The demo can also append rows to a shared Google Sheet that the consulted person can open live. The emails in the kit are placeholder contacts, so the agent never emails a property manager. The researcher's call script is the deliverable.

**Who to consult this weekend.** CoStar, Matterport or Vexcel engineers and data people on site at the event. That is a real business, a named person and role, and a quote or photo for evidence. Geography is not a problem because CoStar owns the Houston/LA data.

The risk is that track judges may see a sponsor-as-client as gaming the track. A backup is a Princeton landlord or property manager who lists on Apartments.com (a CoStar site) and can say what out-of-date listing fields cost them **[unverified who]**.

Three questions to ask:
1. How does a record get corrected today: who notices, who calls, and how long does it take?
2. Which fields, when out of date, generate the most complaints from brokers or lenders?
3. What would a ticket need to contain for you to act on it without re-researching?

**2-minute demo beats.**
- 0:00-0:15: A batch of 20 properties appears. The todos list shows in deep-agents-ui.
- 0:15-0:50: The surveyor subagent cards fan out and the ledger fills. The contradiction appears, followed by the revision and the memory write.
- 0:50-1:10: Building 12 uses the new rule, shown side by side with the memory file.
- 1:10-1:30: The approval card appears, someone edits one ticket and approves it, and the GitHub issue or Sheet row lands.
- 1:30-2:00: The eval table: plain agent against harness, and run 1 against run 2.

**Biggest risk and cheapest kill test.** Real disagreements may be rare or uninteresting, leaving only injected errors. The kill test takes about 2 hours: pull DSM minus DTM height for about 30 kit multifamily properties and compare it with `numStoriesAboveGrade`. Then compare the earliest ortho collection with `constructionEvents` year built. If fewer than about 3 real disagreements survive a sanity check, the pitch weakens to a synthetic benchmark.

**Confidence: 62.** It has the strongest harness and eval story, and the two required layers are solid. Track fit is the soft spot.

---

### Idea 2 — Location Scout: script brief to shootable vacant spaces, with a director's taste in memory

**Pitch.** A director writes a brief such as: "a cramped 2BR with west light for a sunset breakup scene; a lobby with a high ceiling; a place to park a grip truck". The agent scouts vacant apartment units and amenity spaces in LA or Houston. It reads the scans and the air, argues for and against each candidate, and sends an approved location inquiry and a recce calendar hold.

**User and obligation.** The users are location managers and scouts on low-budget productions, plus student filmmakers. They must commit to a location shortlist before a prep deadline. Every wrong recce wastes a day of crew time.

**Outside-world pressure.** The shoot date is fixed. The space must be vacant, which in this data means `numUnitsAvailable` > 0, an available office suite or a defurnished scan. Owners have to say yes. Ceilings, doors and parking constrain gear.

**Data layers, and what only the combination gives.**
- Matterport:
  - Panos and skyboxes give the look.
  - Defurnished views show the empty room the art department will dress.
  - `ceiling` heights matter for lighting.
  - Doorway widths matter for carts and dollies.
  - Window openings and positions, together with `geocoordinates` ENU rotation, give the bearing of each window.
- Vexcel:
  - The DSM shows whether a neighbouring building blocks the west light.
  - Obliques show the exterior establishing shot.
  - The ortho and `car` detection across collections show whether a lot nearby can hold the basecamp.
- CoStar:
  - Vacancy and availability: `numUnitsAvailable`, `forLeaseSummary.spaces[]`, `availableOnDate`.
  - Year built and building class, which proxy for the "period look".
  - `propertyManagementCompanyName` and the listing contacts.
- The combination does something no scout can do remotely today. It can say that a window faces west *and* is not blocked by the 12-storey building next door, *and* that the unit is vacant, *and* that a truck can park within view.

**Harness design.**
- **Tools.**
  - `kit_search(filters)`
  - `mp_search(query)` and `mp_model(sid)`
  - `mp_pano_faces(sid, pano)`, which re-queries because links expire after about 5 min
  - `mp_defurnished(sid)`
  - `window_bearings(sid)`, a geometry tool
  - `vexcel_dsm_obstruction(lat,lon,bearing)`
  - `vexcel_oblique(dir)`
  - `vexcel_detect("car")`
  - `send_email`, `make_ics`, `post_discord` (actions)
- **Subagents.** All run in isolated context, because each candidate means about 20-40 pano faces.
  - `scout` runs one per candidate in parallel. It writes `/evidence/<sid>/look.md` with the pano ids it cited.
  - `advocate` argues for a candidate against the brief.
  - `logistics_critic` argues against it, using only Vexcel and door/ceiling tools.
  - `light_verifier` checks the claim "west light" with the window bearing and DSM obstruction. It may not use the pano description.
  - `outreach_writer` drafts the inquiry.
- **Memory.**
  - `/memories/directors/<name>.md` holds taste learned from rejections, such as "rejected glossy Class A new builds; prefers pre-1990 buildingClass B/C".
  - `/memories/AGENTS.md` holds data quirks, such as "re-query skybox links; ENU rotation missing on part of commercial".
  - `/work/brief.md`, `/work/shortlist.md` and `/ledger.jsonl` hold the per-run working state.
- **Verifier.** The rubric requires every shortlisted location to cite at least 1 pano id, 1 Vexcel product and 1 kit record. A "light" claim also needs the `light_verifier` verdict.
- **Gates.** `interrupt_on` covers `send_email`, `make_ics` and `post_discord`. The thread pauses for the director to mark each shortlist photo "yes" or "no". That feedback becomes memory, and the run resumes with a re-plan.
- **What a single-prompt agent gets wrong.**
  - It believes `generatedDescription.summary` ("bright, sunny kitchen") over geometry.
  - It cannot hold 10 candidates' panos in context.
  - It forgets the director's rejections the next day.
  - It never checks a truck lot.
- **Second job on the same harness.** A student-org event-venue scout ("amenity room for 40 people, ceiling ≥ 3 m, parking"), which needs a new brief schema and rubric only. A real-estate marketing photo-shot planner also fits.
- **Eval.**
  - Build 10 written briefs with hand-labelled acceptable and unacceptable candidates (labelled by the team from panos).
  - Measure precision@3 of the shortlist and the rate of "light claim contradicted by geometry".
  - Compare the plain agent with the harness, then run 2 against run 1 after injecting 3 director rejections, measuring whether rejected traits disappear from the shortlist.

**Visible reasoning moment.**
1. A scout proposes unit X because the summary and panos read "bright, big windows".
2. `window_bearings` says the living-room windows face roughly north-west.
3. `vexcel_dsm_obstruction` finds a taller structure about 20 m west **[illustrative]**.
4. The light verifier returns CONTRADICTED.
5. The `logistics_critic` adds that the ceiling is 2.4 m, which is tight for overhead lighting.
6. The orchestrator drops X, re-plans toward higher floors with west openings, and promotes unit Y, whose defurnished pano shows an empty room that matches the brief.

**External action in the demo.**
- With approval, the agent emails the location inquiry with the pano screenshot, oblique, door and ceiling sheet. Kit contacts are placeholder contacts, so the email goes to the consulted student producer as the stand-in requester, or to the team's own inbox addressed "to: property manager [name from kit]".
- It also sends a `.ics` recce hold to the director.
- It posts the shortlist to the club's Discord or Slack.

**Who to consult this weekend.** A campus student film club whose staff handle location bookings for several student films a semester. A student club qualifies under the track's real-business requirement. The plan is to DM the club's board or production lead on Saturday morning and meet in person, then get a quote and a photo with the person's name and role. Contact names are **[unverified]**.

Bridging the geography honestly: the club scouts in Princeton, not LA. We would consult on the workflow, its failure points and what a booking inquiry needs. We would say plainly that the demo runs on LA data because that is where the scans are. A secondary contact is a university alumni network for the film industry **[unverified it is still active]** for a 10-minute call with an LA location professional.

Three questions to ask:
1. What has gone wrong on a booked location that you could have caught from photos?
2. What do you need to know before you contact an owner?
3. How do you capture the director's no's today?

**2-minute demo beats.**
- 0:00-0:20: The brief is typed and the todos appear.
- 0:20-0:50: Four scout cards run in parallel and pano thumbnails land in `/evidence`.
- 0:50-1:15: The light contradiction is shown with the DSM overlay, followed by the re-plan.
- 1:15-1:35: The Showcase SDK flies into unit Y, the view toggles to defurnished, then the oblique exterior shows.
- 1:35-1:50: The director rejects one candidate, memory updates and the re-run drops similar candidates.
- 1:50-2:00: The approval card appears, the email and calendar invite land, and the eval row is shown.

**Biggest risk and cheapest kill test.** The risk is window bearing. It depends on ENU rotation and window openings, which were present on most residential models but few commercial models in the sample. Apartment units are filed under "commercial", and their coverage is unmeasured.

The kill test takes about 1.5 hours. Take 10 multifamily unit scans that have window openings and compute window bearings from the ENU rotation. Check them by eye against the Vexcel ortho building edges. If fewer than about 7 of 10 line up, drop the light claim and keep look, ceiling and logistics. The idea survives, but it loses its best moment.

**Confidence: 58.** It is the most surprising use of the sponsors' data and heavy on all three layers. Track fit is honest but indirect. The geometry work is real.

---

### Idea 3 — Back-House Check: is that "guest house" a legal dwelling?

**Pitch.** For a home listed with a "guest house / ADU / garage apartment", the agent builds a dated story of the back structure. Vexcel history shows when it appeared. The scan shows whether it holds a kitchen and a bath. Public permit records show what was permitted. The agent then sends the listing agent an approved question, pauses and resumes when the answer arrives.

**User and obligation.** The users are a buyer's agent or a residential appraiser. Appraisers generally cannot count unpermitted living area the same way, and buyers inherit enforcement risk. The decision is whether to price the back unit as legal income or as storage, and what to demand before closing.

**Outside-world pressure.** There is a closing or appraisal due date and a written disclosure request. Money is at stake on the rent the unit can legally earn.

**Overlap caveat.** This idea shares the "claim against reality" pattern with the excluded apartment listing-vs-reality idea. It differs in property type (homes), in the evidence (permits and imagery history) and in the user (appraiser or buyer's agent). The orchestrator should judge whether that is distinct enough.

**Data layers.**
- CoStar MLS homes: `remarks`, features `highlights[].text`, `yearBuilt`, `sqftMin`, `agents[]`. There are CA and TX listings.
- Matterport residential: full Property Insights, room classifications on a 36-label vocabulary (kitchen, bathroom), `Floor.data`, exterior doorways, and `areaFloor` of the back structure.
- Vexcel: per-collection `structure` footprints and ortho history from 2016-2026, which give the year the structure appeared. Obliques show a separate entrance.
- Public data: LA building permit data on the City's open data portal, per LADBS. The dataset and its fields are **[unverified]**. Houston permit data is also **[unverified]**.
- The combination turns "it appeared between 2018 and 2020, it has a kitchen, and the only permit is a garage" into one dated, cited finding.

**Harness design.**
- **Tools.** `mls_get`, `mp_rooms`, `mp_exterior_doors`, `vexcel_structures_by_collection`, `vexcel_ortho(collection)`, `permits_search(address)`, `send_email`, `make_pdf`.
- **Subagents.**
  - `history_reader`: Vexcel only. It builds the structure timeline.
  - `interior_reader`: Matterport only. It finds which scan floor or rooms belong to the back structure.
  - `permit_clerk`: public data only. It learns permit vocabulary.
  - `prosecutor` and `defender`: the defender looks for innocent explanations, such as a permitted conversion or a permit filed under another address.
  - `verifier`.
- **Memory.**
  - `/memories/permit_vocab/<city>.md` holds learned search terms ("ADU", "JADU", "garage conversion", "accessory") and false hits.
  - `/memories/AGENTS.md` holds rules such as "Vexcel footprints vary by collection; require 2 consecutive collections before declaring 'appeared'".
- **Long-running and resumable.** The thread is checkpointed when the agent emails the listing agent. A reply (simulated live in the demo) resumes it with `Command(resume=...)`, and the agent re-plans.
- **Gates.** `interrupt_on` covers `send_email` and the final PDF release.
- **What a single prompt gets wrong.**
  - It takes the MLS remarks as truth.
  - It reads one Vexcel collection and declares "new".
  - It runs one permit search with one term and calls an empty result proof.
  - It cannot wait days for a reply.
- **Second job.** An "unpermitted addition" check for main-house square footage: scan `areaFloor` against MLS `sqftMin`, footprint growth across collections, and permits. It uses the same tools.
- **Eval.**
  - Hand-label 10-15 listings that mention a back unit as permitted, unpermitted or unknown.
  - Score the correct label and the false "unpermitted" accusations.
  - Compare plain agent and harness, and run 1 against run 2 once memory holds the permit vocabulary.

**Visible reasoning moment.**
1. The remarks say "permitted ADU", which is hypothesis H1.
2. History shows the structure appearing between two collections.
3. The permit clerk's first search ("ADU") returns nothing, and the prosecutor says it is unpermitted.
4. The defender makes the clerk retry with the garage-conversion vocabulary from memory, which finds a permit of a different type.
5. The interior reader shows a kitchen.
6. The revised claim is "permitted as a garage, used as a dwelling, so ask".
7. The agent sends an approved email, pauses, then resumes on the reply.

**External action.** It emails a disclosure question to the "listing agent", which is the team's address because kit contacts are placeholder contacts, after approval. It also emails a PDF memo to the appraiser.

**Who to consult.** An independent residential appraiser or a buyer's agent in Princeton or Mercer County, phoned or visited Saturday morning, for example at a local brokerage office. Names are **[unverified]**. The geography bridge is that permit-versus-reality checks are the same workflow in NJ, and the demo runs on LA because that is where scans and imagery exist.

Three questions to ask:
1. How do you check whether an accessory unit is permitted today, and how long does it take?
2. What evidence would you accept in a work file?
3. What happens to the appraisal when it is not permitted?

**Demo beats.**
- 0:00-0:20: The listing is shown and the plan appears.
- 0:20-0:55: A timeline slider runs through the 2016 to 2026 orthos and the structure appears.
- 0:55-1:15: The scan shows the kitchen in the back structure.
- 1:15-1:35: The permit miss, then the vocabulary retry and the hit, then the revised claim.
- 1:35-1:50: The approval card appears and the email is sent. The thread shows "paused".
- 1:50-2:00: A reply is pasted in, the run resumes and the memo is finalised.

**Biggest risk and cheapest kill test.** Too few scanned listings may have a back unit. The kill test takes about 1 hour: grep the remarks and highlights of the CA and TX listings for "guest house|ADU|casita|garage apartment|back house", join them to scans, and check how many scan the back structure. Then confirm that the LA permit dataset is queryable by address. If fewer than about 5 usable cases exist, kill the idea.

**Confidence: 45.** The pause/resume shape and the reasoning moment are excellent. Data volume, permit-data access and overlap with an excluded idea are real risks.

---

## The one I would bet on

**Idea 1, Ground-Truth Desk**, by the harness lens. It is the only one where every harness primitive is *forced* by the data:
- It is a batch, so memory has to carry lessons across buildings.
- The documented source noise forces an adjudicator and an other-source verifier.
- The pano and DSM volume forces isolated subagents.
- Researcher approval forces gates.
- Injected-corruption evals give a clean "harness beats plain agent, run 2 beats run 1" number with the model held fixed.

Its weak spot is track fit. If the orchestrator weights track fit and the CoStar "wow" factor more than the LangChain prize, pick Idea 2. It reuses about 70% of the same tool layer (kit, Vexcel and Matterport tools, the ledger and the verifier pattern), so the harness could ship both as job 1 and job 2.

Sources for the web facts used: [LADBS ADU / permit records](https://ladbs.org/adu), [dbs.lacity.gov](https://dbs.lacity.gov/?page=0).
