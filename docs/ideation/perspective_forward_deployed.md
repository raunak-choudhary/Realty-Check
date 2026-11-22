# Perspective: forward deployed engineer (Peri track lens)

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

Web searches done 2026-11-13; every business fact below carries its source, and anything not confirmed is marked **[unverified]**. Data observations come only from our own survey of the sponsor data.

---

## (a) Reasoning chain

1. **Start from who will actually answer us between Sat 9 AM and Sun 8 AM.** The Peri track asks for a business name, a named person with a role, and one piece of evidence. A customer who does not reply by Saturday evening is no customer at all.
2. **The data only covers Houston and LA city limits.** Vexcel returns 403 at Princeton. A Princeton business can only be an honest customer if one of these holds:
   - (i) it does exactly the same regulated or standard job as the Houston/LA user, so its workflow transfers one-to-one (national rules such as Fannie Mae ANSI GLA, or standard industry practice such as the weekly apartment market survey);
   - (ii) it is part of a company with assets in the kit;
   - (iii) it is the data owner itself.
   I score anything else as not a real customer.
3. **"Adoptable on Monday"** means the Monday user must be in Houston or LA (or be CoStar). The Princeton consult only validates the workflow. I say this openly in every pitch instead of hiding it.
4. **Pick workflows where the three layers disagree in normal operation.** That makes the agent's reasoning necessary rather than staged. Good sources of disagreement:
   - outlier kit fields (implausible values in `buildingHeightInFeet`, `vacancyPercent` and rent);
   - index coordinates far from the kit location on some models;
   - `costar_property_id` mismatched on some models;
   - Vexcel footprints that differ by orders of magnitude for the same building across collections;
   - MLS square feet vs scan area.
5. **Prefer the property types where the data is thick:** Multifamily (the largest share of properties and scans) and homes (many residential models with full Property Insights, most also defurnished). Retail and restaurants are out (very few GeneralRetail properties), so the town's main-street shops are out as data customers however reachable they are.

### Reachable customer types, honestly rated for this Saturday

| Customer type | Example (source) | How to reach on Sat | Reachability | Honest bridge to Houston/LA data? |
|---|---|---|---|---|
| CoStar / Matterport / Vexcel staff at the event | CoStar engineers on site all weekend | Walk up at the event | **High** | **Yes, they own the data.** Risk: the Peri track may see a sponsor as a soft customer |
| Apartment leasing offices in the kit (Houston/LA) | Any kit community; real phone from the public web (kit phone numbers are placeholder 555 numbers) | Phone, Sat 10 AM-5 PM local is typical **[unverified per property]** | Medium (they are busy with tours; expect many calls per interview) | **Yes, the customer is a kit property** |
| Princeton-area apartment leasing office | A leasing office of a national apartment operator's Princeton community. Published hours conflict between the operator's own pages | Walk in (near downtown Princeton) | High | Same job (weekly market survey). Whether the operator's LA communities are in the kit is **[unverified]** |
| Princeton residential appraisers | A local residential valuation firm; independent certified residential appraisers (from public appraiser directories) | Phone or email; Saturday hours **[unverified]** | Medium | Same job under the same national Fannie Mae ANSI rule |
| Houston apartment locators | Several Houston apartment-locator firms; some list Saturday hours in directory listings | Phone or text, Saturday | **High** (they want leads and work weekends) | Yes, they are Houston businesses |
| Houston STR managers | Houston short-term-rental management companies (from a public directory search) | Phone (they answer guests on weekends) | Medium-high | Yes, but the kit has no STR data |
| Houston/LA proptech startups | e.g. a Houston apartment market-survey company | LinkedIn DM / email | Low-medium on a weekend | Yes |
| Main-street shops and restaurants | — | Walk in | High | **No.** The data is thin and covers no Princeton site |
| University offices (EHS, housing, athletics) | — | Mostly closed Saturday | Low | No |
| Student clubs / other hackers | — | At the event | High | No building workflow in Houston/LA, so not a real customer |

---

## (b) Raw candidates

| # | Candidate (one line) | Verdict |
|---|---|---|
| 1 | **Conflict Desk.** A record-conflict triage agent for CoStar Research: cross-checks kit vs Matterport vs Vexcel per property and files evidence-backed fix tickets plus verification requests | **KEEP (top 3)** |
| 2 | **ANSI Check.** An ANSI Z765 GLA and site-verification addendum for desktop/hybrid appraisals of Houston/LA homes, built from scan + footprint + DSM | **KEEP (top 3)** |
| 3 | **Comp Survey Copilot.** A weekly apartment market survey that normalizes comps by scanned unit area, verifies amenities from the air and spots new lease-up competitors in imagery history | **KEEP (top 3)** |
| 4 | Houston locator tour packet: shortlist + referral registration email to each property + tour booking | Dropped. Too close to the excluded renter-side finders and listing-vs-reality; the locator's commission registration is the only new part |
| 5 | Houston STR registration and max-occupancy packet (bedroom egress from window `lowerElevation`/width/height) | Dropped. The kit has no STR records; the registration is mostly paperwork; the spatial part is one check |
| 6 | Mover virtual survey: furnished-minus-defurnished pano diff as a furniture inventory, truck parking from obliques | Dropped. Overlaps the excluded contractor-bid-from-scan and furniture-fit; listing furniture is often staging |
| 7 | HVAC Manual J from scan: register the wall graph to the Vexcel footprint to get each window's compass orientation, then compute load | Dropped. A contractor bid in another trade, and next to warehouse heat. **Reuse the registration trick inside #2** |
| 8 | Princeton realtor outbound relocation referral matcher (pick the Houston/LA destination agent from kit `agents[]`) | Dropped. Weak spatial component; the value is the relationship, not the data |
| 9 | Princeton team travel to Houston: hotel RFP that sizes meeting rooms from hotel scans and finds coach drop-off in obliques | Dropped. No verified Princeton trip to Houston (not-a-real-customer risk); few hotels in the kit |
| 10 | Office tenant emergency evacuation map from suite scans + Vexcel assembly point | Dropped. Suite scans rarely cover whole floors; office Property Insights coverage is weaker than for residential |
| 11 | Main-street restaurant expansion helper | Dropped. Retail/restaurant data is thin, and site selection is excluded |
| 12 | Matterport index link repair (fix the null or mismatched `costar_property_id`) as a standalone product | Folded into #1 as its second job on the same harness |

---

## (c) Best 3

### 1. Conflict Desk: evidence-backed data-correction tickets for CoStar Research

**Pitch:** an agent picks a Houston/LA property and tests every claim in the CoStar record against the scan and the sky. It writes the conflicts it cannot explain away into a verification ticket with picture evidence, and after approval files the ticket and emails the property manager a confirmation request.

**User and obligation.**
- User: a CoStar research analyst or data-quality owner.
- Obligation: CoStar sells the record as researched and verified, so fields that drift from reality are something they have to find and fix.

**Pressure.** Records and reality can drift apart, and the kit already contains the kinds of conflicts the agent would catch:
- implausible outliers in `buildingHeightInFeet`;
- out-of-range `vacancyPercent` values;
- placeholder rent values;
- placeholder MLS values;
- index model coordinates far from the kit location on some models;
- `costar_property_id` missing or mismatched on some commercial models.

Every downstream user (brokers, lenders, appraisers) inherits these conflicts.

**Data and what the combination gives.**
- Kit: `numStoriesAboveGrade`, `buildingHeightInFeet`, `constructionEvents[]` (year built), `propertyType`, `parking[].totalSpaces`, lat/lon, `propertyApartment.models[]`.
- Matterport: rooms and classifications, `ceiling`, `generatedDescription.summary`, `address`/`geolocation`, panos.
- Vexcel: DSM minus DTM height, `property/extract` per collection (footprint, `pool.*`, `vehicles.count`), the ortho collection history back to 2016, and obliques.

No single layer can tell a typo from reality. Two independent layers agreeing against the third is what lets the agent assign blame.

**Visible reasoning moment.**
1. The record says N stories and a `buildingHeightInFeet` that is out of range (an outlier of the kind listed above).
2. *Hypothesis:* the height field was entered inconsistently and the stories are right.
3. The DSM-DTM height over the footprint is about N × 3-3.5 m, which supports it.
4. *Second conflict:* `constructionEvents` gives year built Y, but the 2016 ortho collection already shows a finished roof on the parcel.
5. *Hypothesis:* the year does not match.
6. *Counter-check:* the oblique from the oldest collection shows cranes or bare slab, so the building was under construction and year built Y is fine. The agent withdraws the ticket line and logs why.
7. *Third conflict:* a scan whose index coordinate is 1 km off.
8. *Hypothesis:* the scan is mislinked.
9. *Test:* the Matterport `address` and the room mix (apartment-unit classifications vs `propertyType`) match the kit property, so the record holds and the index coordinate is off. The ticket is re-targeted to the index, not to the property.

**External action.** After human approval:
- post the ticket (field, current value, proposed value, evidence crops, confidence) to a shared Google Sheet or Slack channel the consulted CoStar person agreed to watch;
- optionally email the property's real manager (public contact, not the placeholder kit email) asking them to confirm the year built and story count.

The approval gate shows the exact text before anything is sent.

**Who to consult this weekend.**
- CoStar engineers at the event, in person.
- Ask them to introduce you to someone who owns research data quality or the Matterport-to-CoStar linkage.
- Get the name and role in writing (a chat DM screenshot).

**5 questions:**
1. When a field is out of date today, who finds it and how? Customer complaint, researcher call or automated rule?
2. What evidence does a researcher need before changing a field: a call, a photo, two sources?
3. Which fields hurt most when out of date: year built, stories, size or parking?
4. Where do fix tickets live? Can we post to it, or to a mirror sheet, this weekend?
5. Who owns the Matterport ↔ CoStar link, and how are mislinks fixed now?

**Evidence to capture:**
- a chat screenshot of the quote, with name and role;
- a photo at the sponsor booth (with permission);
- their reply on a filed ticket.

**2-minute demo:**
- 0:00 The problem, with three real record conflicts from the kit on screen.
- 0:20 Pick a property; the planner writes its checklist to a file.
- 0:35 Subagents report back from the kit, Matterport and Vexcel.
- 0:55 The year-built hypothesis is raised and then withdrawn on the oblique.
- 1:15 Height and mislink conflicts are confirmed with the DSM profile and the scan room mix.
- 1:35 The approval gate; the ticket lands in the shared sheet or Slack live.
- 1:50 Second job on the same harness: batch-scan 50 properties for mislinks.

**Harness fit.**
- Subagents per layer, each with its own context.
- Filesystem memory: one `property/<id>/claims.json` per property.
- Forced verification: no ticket line without two layers agreeing.
- Resumable batch.
- Second job (index link repair) reuses the same tools.

**Biggest risk.** Peri-track judges may read "the sponsor" as not a real forward-deployed customer, and the conflicts found may be too few or too boring.

**Cheapest kill test (1 hour):**
- Run DSM height vs stories and the 2016-ortho year-built check on 20 kit properties.
- Ask one CoStar engineer at the event whether they would want those tickets.
- If fewer than 2 real conflicts are found, or the engineer says "we already catch this", kill it.

**Confidence: 62.** It has the best data and agentic fit and the easiest customer; the Peri-track risk holds it back.

---

### 2. ANSI Check: GLA and site-verification addendum for desktop and hybrid appraisals

**Pitch:** given a Houston/LA home with a Matterport tour, the agent produces the computer-generated floor plan with ANSI Z765-2021 GLA calculations that a desktop appraiser must attach. It reconciles that against MLS square feet, the aerial footprint and DSM stories, and flags additions that cannot be explained.

**User and obligation.**
- A residential appraiser or property-data collector on Fannie Mae work, using the Fannie Mae ANSI fact sheet (March 2022; [fact sheet PDF](https://www.nysar.com/wp-content/uploads/2022/04/Fannie_Mae_ANSI_Fact_Sheet_updated_033122.pdf)):
  - appraisals with interior and exterior inspections must use ANSI Z765-2021 for GLA;
  - "All footprint sketches and floor plans must be computer-generated ... show the calculations";
  - desktop appraisals require a floor plan, which Fannie expects to "commonly receive ... from a third party";
  - ANSI is "encouraged" but not required on desktops.
- Value Acceptance + Property Data requires an ANSI-compliant floor plan ([homebuyer.com summary of B4-1.4-11](https://homebuyer.com/guidelines/fannie-mae/value-acceptance-property-data-b4-1-4-11)).

**Pressure.** The fact sheet's ANSI rules are geometric, and the scan carries most of the needed geometry:
- "Finished areas must have a ceiling height of at least 7'";
- sloped rooms need at least 50% at 7' or more and no counted part under 5';
- "Staircases are included in the GLA of the floor from which they descend";
- "The GLA calculation does not include openings to the floor below, e.g., two-story foyers."

Doing this by hand from a tour is slow and error-prone.

**Data and what the combination gives.**
- Matterport (residential: full Property Insights on the samples checked):
  - `rooms.dimensions.areaFloor` and classifications;
  - `ceiling{minHeight,maxHeight}` for the 7'/5' rules and to detect double-height foyers;
  - wall-graph `thickness` and the floor plan at 100 px/m.
- Vexcel:
  - per-structure `footprint.area` from the newest collection;
  - DSM-DTM for stories;
  - pools and outbuildings;
  - ortho history back to 2016 to see when a rear addition or ADU appeared.
- Kit homes: `property.sqftMin`, `bedsMin`, `yearBuilt`, `remarks`; LA `closePrice` for context only (Houston has none).

The interior scan gives net room areas but not the exterior face. The aerial gives the exterior outline but not ceilings or which floor is finished. Only together do they approximate ANSI exterior-dimension GLA.

**Visible reasoning moment.**
1. The MLS says about 2,400 sqft (example shape, not a kit number).
2. Scan rooms sum to S. Adding interior and exterior wall thickness gives G.
3. The Vexcel footprint × 2 stories (from DSM) gives F, which is much larger than G.
4. *Hypothesis A:* the attached garage is inside the footprint. Test: a room labelled Garage, or an unscanned rectangle adjoining the garage-door side in the oblique, accounts for about F−G. Partly confirmed.
5. A gap remains. *Hypothesis B:* MLS counted the open-to-below area. Test: a foyer room has `ceiling.maxHeight` about 5 m and no upper-floor room above it. ANSI says exclude it, so the agent revises the upper-floor area down.
6. *Residual check:* the 2016 ortho shows a smaller rear outline than 2026. A rear room was added after 2016, so the agent flags "verify permit". It does not conclude it is unpermitted.

**External action.** After approval:
- email the appraiser (or upload to their shared folder) a PDF addendum: the floor plan, a per-floor GLA table with ANSI declarations, a conflict list and evidence crops;
- at the appraiser's choice, a short "please confirm" email to the listing agent.

**Who to consult.**
- **Princeton (same job):**
  - a local residential valuation firm;
  - an independent certified residential appraiser nearby.
  - Saturday availability for both is **[unverified]**: phone Saturday morning and leave a callback.
- **Houston/LA (Monday user):** find a TALCB-licensed (Texas) or California residential appraiser who does desktop or hybrid work via LinkedIn or the appraisal subcommittee registry. None was found by name in our search **[unverified]**.

**5 questions:**
1. How do you get the floor plan on a desktop or hybrid job today, who makes it, and what does it cost in time or money?
2. Which ANSI rules trip you up most: ceilings, stairs, open-to-below or garages?
3. When MLS sqft and your number disagree, what evidence settles it for the underwriter?
4. Would you use aerial history to flag additions, or is that out of scope or a liability?
5. What format would you accept on Monday: PDF, a sketch-software import (DXF?) or something else?

**Evidence:** a phone-call note plus a direct quote (with permission), and a photo of their current sketch tool if met in person.

**2-minute demo:**
- 0:00 The ANSI rule card from the fact sheet.
- 0:15 Pick an LA home; subagents pull the scan, the aerial and the MLS record.
- 0:35 Floor plan with per-room ceiling shading (red under 7').
- 0:55 The F vs G vs MLS conflict; garage hypothesis, then the foyer exclusion.
- 1:20 2016 → 2026 ortho slider shows the rear addition.
- 1:35 Approval gate; the addendum is emailed.
- 1:50 Second job on the same harness: the listing agent's pre-listing sqft check.

**Biggest risk.**
- Matterport `areaFloor` is net and per room. Exterior-wall thickness is unknown, and the Vexcel footprint can differ between collections, so G and F may be too noisy to reconcile.
- No appraiser may answer on Saturday.

**Cheapest kill test (45 min):** take 5 residential models with a kit `sqftMin`. Compute the sum of `areaFloor`, the newest-collection footprint and the DSM stories. If the scan sum vs MLS spread is unexplainably wide on most of them, or the footprints are unusable, kill the reconciliation and keep only the ANSI ceiling and stair rules.

**Confidence: 58.**

---

### 3. Comp Survey Copilot: weekly apartment market survey with ground truth from scans and sky

**Pitch:** for a Houston/LA apartment community, the agent runs the weekly competitor survey that leasing managers mostly still do by phone:
- it pulls comp rents and availability per floor plan;
- it normalizes them by the scanned unit area;
- it verifies amenities from the air (the kit has amenity ids but no names);
- it spots new lease-up buildings in imagery history that are missing from the comp set;
- then it updates the shared survey sheet and emails the regional manager.

**User and obligation.** The community or leasing manager.
- An MRI Software survey found that for more than half of apartment managers, "phone calls continue to be the primary method" for surveys.
- Survey frequency was spread evenly between weekly and monthly.
- Over half said surveys take more than an hour per property per month ([MRI](https://www.mrisoftware.com/blog/survey-results-multifamily-market-data-collection-practices/)).

**Pressure.** Pricing decisions are made weekly, and new lease-ups with concessions pull prospects away. **Overlap warning:** this sits near the excluded "rent audit". The difference is the user (the operator pricing its own units) and the aerial and scan verification. Paid incumbents exist (market-survey software and data companies), so the edge has to be the spatial checks.

**Data and what the combination gives.**
- Kit apartment-listing: `apartmentModels[].minRent/maxRent/numUnitsAvailable`, `vacancyPercent`, `propertyManagementCompanyName`, plan-level scan keys.
- Matterport: unit `areaFloor` per plan, so $/scanned m², not $/advertised SF; also pool and fitness amenity scans by model name.
- Vexcel:
  - `pool.detected` per collection;
  - covered parking and garage from obliques;
  - new structures between collections within the comp radius;
  - embedding search for "apartment under construction" (search-text tested; scores relative only).

**Visible reasoning moment.**
1. Comp X's 2BR is $Y cheaper.
2. *Hypothesis:* we are overpriced, so recommend a cut.
3. *Check:*
   - the comp's scanned 2BR area is smaller, so $/area is about equal;
   - Vexcel `pool.detected` is true in older collections but false in the newest, and the oblique shows the pool drained or fenced.
4. *Revision:* do not cut. The comp is discounting a smaller unit with a pool out of service. The agent adds "ask about the pool" to the call list.
5. *Plan change:* ortho history shows a large new mid-rise 400 m away that is absent from the comp set. If it is in the kit, the agent adds it as a comp; if not, it flags it for a phone call.

**External action.** After approval:
- append this week's row to a Google Sheet the manager owns (shared with us);
- email the regional manager the summary;
- optionally send survey-request emails to the comps' leasing offices (common practice in the industry).

**Who to consult.**
- A Princeton-area leasing office of a national apartment operator. Walk in Saturday; published hours conflict, so phone first. Same job, and the operator has LA assets (kit membership **[unverified]**).
- **Plus the Monday user:** phone 10-20 kit communities in Houston on Saturday (use the public number, not the kit's placeholder 555 numbers) and ask for the manager.
- Optional: a Houston market-survey company via LinkedIn as an expert check.

**5 questions:**
1. Walk me through last week's survey: which comps, how they were collected, how long it took.
2. What did you get wrong last time: concessions, a unit size, an amenity that was down?
3. How do you decide when a new building joins the comp set?
4. Who sees the survey and where does it live: a sheet, Yardi, an email?
5. If this ran every Monday at 8 AM, what would make you trust it?

**Evidence:** a photo of the printed or on-screen survey grid (redacted, with permission), a quote with name and role, and a call log.

**2-minute demo:**
- 0:00 The manager's grid.
- 0:15 The agent plans the survey for one Houston kit community.
- 0:30 Comps pulled; the cheaper-comp hypothesis.
- 0:50 Scan area normalization plus the pool out of service in Vexcel history; the recommendation flips.
- 1:15 The new lease-up found in the 2023→2026 ortho and added to the set.
- 1:35 Approval; the sheet row appears and the email is sent.
- 1:50 Second job on the same harness: monthly owner report.

**Biggest risk.**
- Near-overlap with the excluded rent audit.
- Leasing offices may not take a 10-minute call on a busy Saturday.
- `pool.detected` may be too noisy across collections.

**Cheapest kill test (1 hour):**
- Call 5 Houston kit communities between 10 AM and 12 PM local.
- In parallel, pull `pool.detected` across collections for 10 kit properties.
- If no one talks, or the pool flags flip randomly, kill it.

**Confidence: 45.**

---

## The one I would bet on

**Conflict Desk (#1).** It is the only idea where:
- the customer is guaranteed reachable on Saturday (at the event);
- the Monday user and the data geography are the same, with no Princeton bridge to defend;
- the reasoning is native to the data: real conflicts are already observed in the kit (mismatched ids, index coordinates far off, implausible heights).

Its weakness is the Peri track's "real business" spirit. Mitigation:
- Consult a named CoStar data-quality or research person, not just an engineer.
- Get a quote that this is a real weekly workflow.
- Keep ANSI Check (#2) as the backup if the team decides a sponsor customer is too soft for the Peri track.
