# Ideas Brief: nine ideas, ranked after verification

Pre-build brainstorm memo. Most ideas here were explored and not built; the shipped product is the listing checker described in the README.

*This is the whole decision file for picking the headline idea, about seven minutes to read. Every claim was tested live on Nov 13–14 and counts as PASS only if it was seen working; the ranking is effectiveness × buildability after those tests. Depth is uneven on purpose: ideas 1 and 2 get the full treatment, the tail a few sentences each.*

## 1. The one engine under all nine

Every idea here is the same machine. A building has **declared facts** (what the CoStar record says: stories, units, bedrooms) and **measured facts** (what the Matterport scan and the Vexcel aerial show). The agent compares them, resolves the conflict, applies a written outside rule (a rent limit, a statute, a deadline), and issues paper someone acts on. Carry it as *record says, pictures show, rule decides, paper goes out.* That shape covers your three requirements at once: a real problem, a deepagents harness with one subagent per source (the harness itself was not verified), and two CoStar layers that yield something only together.

The most useful finding cuts across all nine: **records and reality can drift apart, and the kit's parcel number is a clean join key.** On the buildings checked, declared story and unit counts did not always line up with what the pictures and the county records showed. Meanwhile the parcel number matched the county account on nearly all Houston apartments sampled (the same digits key the city's 311 complaints) and matched the assessor on every LA sample. Drift between record and reality is the product; the parcel number is how you prove it.

## 2. The ranked ideas

| # | Idea | Layers that truly combine | PASS/PARTIAL/FAIL/UNTESTED | Biggest gap |
|---|---|---|---|---|
| 1 | LeaseUp Desk (LA) | Records + scan | 10/10/1/2 | Bedroom read was by eye, not scripted |
| 2 | Ground Truth | Records + aerial | 15/14/3/2 | Proven on 3 hand-picked buildings only |
| 3 | Inspection triage (Houston) | Records + aerial | 11/11/2/0 | No inspection results to validate the ranking |
| 4 | SB 721 balcony scope (LA) | Records + aerial + scan stills | 6/9/4/0 | Balcony counts are rough; auto-count failed |
| 5 | Tax appeal packet (LA) | Records only; imagery is colour | 13/6/1/0 | Comparables unadjusted |
| 6 | Fire pre-plan | Records + aerial | 13/10/4/0 | Every protection-system field empty |
| 7 | Flood status (Houston) | Records + aerial footprints | 9/15/4/0 | Buildings in one community rarely differ |
| 8 | ANSI area check (homes) | Scan (aerial is an upper bound) | 21/10/5/0 | Record area is the assessor's number |
| 9 | Right-to-AC (Houston) | Scan stills + 311 text | 7/7/3/0 | Nothing measures working AC |

The tally measures plumbing, not worth: idea 8 has the most PASS rows and ranks eighth.

### 1. LeaseUp Desk: voucher lease-up, LA first

**Who has the problem:** a housing navigator placing a household with a **Housing Choice Voucher** (a federal rent subsidy). A unit only works if rent plus utilities fits the housing authority's **payment standard** (the rent limit by ZIP and bedroom count) and the family's share stays under 40% of adjusted income.

**What the layers do together:** the record gives rent and a declared bedroom count; the scan shows the real one. In one LA building in the kit, a floor plan is listed as 2 beds. As a 2-bed the rent fits under the payment standard and the family share stays under the cap: pass. The scan is titled as a one-bedroom with a den and its panoramas show one bedroom plus a den with only a high narrow window. As a 1-bed the limit drops and the family share rises past the cap: *fail.* A control unit in a second LA building passes both ways. The aerial adds little here; do not oversell it.

**Outside data:** all free and keyless: LA's payment standards (many scan-linked LA plans sit at or under them), its utility allowance PDF, and the federal rule text. **Paper:** a filled Request for Tenancy Approval (HUD-52517) and a landlord email behind an approval gate.

**Still unproven:** the bedroom catch rests on a scan title and stills read by eye; only some sampled scans carry room labels. The kit has no who-pays-utilities field (the one FAIL), the household was invented, the form has 0 fillable fields, and email was untested. Houston lacks a utility schedule. **Build risk:** medium, concentrated in the vision call. Whether a den counts is the authority's call; the app flags, it does not rule.

### 2. Ground Truth: the record-versus-reality correction desk

**What it is:** the engine from Section 1 sold on its own, and the check that powers idea 1. Its user is whoever owns the record; finding them is your part.

**What the layers do together:** at one Houston mid-rise in the kit the record gives one story count, while the unit numbering, the aerial height model and the county roll each point to one more floor. Four sources agree, so the record is corrected by one floor. The same held at a second Houston building and at an LA building (per the city's Certificate of Occupancy). The scan is the weak layer here: it does not report which floor it was taken on.

**Outside data:** keyless and free: the Harris County roll (about 450 MB, pre-load it) and LA's occupancy certificates (recent buildings only). **Paper:** a correction ticket with evidence; filing it is UNTESTED.

**Still unproven:** three hand-picked buildings, no portfolio false-alarm rate, and height alone over-counts by about a floor. **Build risk:** lowest of the nine, because it never depends on a vision model. That makes 1 and 2 close: 1 has the clearer user and paper, 2 is the safer build.

### 3. Inspection triage docket (Houston)

Houston has 16 habitability inspection staff against 3,300–3,600 complaints a year, so the problem is real. Records, multi-year aerials and keyless 311 and county data filled a pre-inspection sheet on 2 of 2 properties; the top-ranked of 20 sampled properties was one where the record's unit count and the county's were far apart, which skews any per-unit complaint rate. The gap that bites: no inspection results are published, so the ranking cannot be validated, and 10 of 20 sampled properties have zero complaints. Scans are model units, so they only decorate.

### 4. SB 721 balcony scope (LA)

California required balcony inspections on wood-frame apartments by January 1, 2026, and LA's free, keyless citation data shows 1,512 such cites, 796 uncleared. The only idea where all three layers work: the parcel joined to the assessor and angled aerials were available on every sample, and scan stills confirmed a balcony on about half of those checked. But counting from the air is rough (an eyeball count on one test building was only approximate) and the automated count failed. No public list shows who complied, and nothing was sent.

### 5. Tax appeal packet (LA only now)

The best plumbing: the LA roll matched nearly all kit properties and the county appeal form filled 16 of 16 fields, with a live deadline of November 30, 2026. Texas is closed until 2027. It ranks fifth because it fails your two-layer test: scans and imagery are supporting colour, not proof, and the comparables are unadjusted (on one downtown tower the roll's value per square foot sat well above the median comparable sale, an indication only). Close to 4: better paper, weaker layers.

### 6–9. The tail

**6. Fire pre-plan.** The exterior half works keyless (hydrants, stations, flood zone), but only about half the fields filled, and every protection-system and utility-shutoff field stayed empty. An earlier kill test called it weak.

**7. Flood status per building.** Federal sources are keyless, but only a few usable communities split yes/no by building, the Texas lease notice's five-year flooding box cannot be filled (Harvey is outside the window), and no scan states its floor.

**8. ANSI area check.** Scan geometry landed close to the assessor's figure on some homes, but the kit's area matches the assessor's on the homes checked, so there is no conflict to find.

**9. Right-to-AC check.** The ordinance is real (compliance about December 17, 2026, computed), but records carry no AC field, counting cooling units from the aerial did not work on the complexes checked, and nothing measures whether AC works.

## 3. The console

Paper first, pixels second. The evidence view borrows the WorldView globe pattern: 25 of 28 checks passed and a keyless stack responded live; Google's photoreal 3D needs billing. The Matterport SDK connected on localhost on 3 of 3 scans, moved to a chosen **sweep** (one camera position) and returned a screenshot, which is the only way the agent can walk a scan. **WebMCP** (tools a web page registers for an agent) is still a Chrome trial, so treat it as optional; your own WebSocket channel is the recommended route, though not yet built.

## 4. Recommendation

Headline **LeaseUp Desk in LA, built on the Ground Truth engine.** Prove three things in the first hours:

1. A scripted vision call reading bedrooms from scan stills. Decide first which model provider may see sponsor images; that is still open.
2. Utility-allowance handling, since the kit has no who-pays field.
3. Stamping text onto the non-fillable HUD-52517.

If the vision test fails, headline the Ground Truth stories check instead. It already passed on three buildings and needs no vision.

*Three threads run through all of this. Declared versus measured is the engine. The parcel number is the join that makes outside data cheap. And a model's eyes are the one unproven part everywhere, which is why the pick is the idea with the clearest paper and the fallback is the one that needs no eyes at all.*
