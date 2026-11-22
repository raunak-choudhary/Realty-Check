# "1 Bed" vs "3 bedrooms + den": diagnosis

Test write-up from the build, with building identities and record values removed.

Run: one saved run (harness `real`, finished 04:31, Building A, a large LA apartment page with many kit floor plans,
39 claims). Plan names and scan titles below are relabelled (Plan B, Plan C, ...) and sizes are invented. Bed and bath
counts are kept only as an example of the mechanism. Offline only: no network, no new run.

## What the saved run said

Claim `c17`: kind `bedrooms`, value 1, label `Plan B`, quote "1 Bed".
Verdict: **contradicted**, found "3 bedrooms + den", source scan,
"Listing says 1 bedroom. The 3D scan shows 3 bedrooms + den. The building record says 1."

## Which evidence it was paired with

The scan evidence the judge used for `c17`:

- a `model_id`, and a `model_name` of the form "Building A - Plan B - 1 Bed / 2 Bath plus Den",
  `observed.plan` = "Plan B" (and a copy tagged "Plan B + Den")
- `room_labels` with three spaces labelled "Bedroom", plus a kitchen, two bathrooms and one unlabelled space
- `bedrooms` 3 (counted from those labels; no `counts_from: model_name`)
- record evidence for the same claim: plan "Plan B", kit_plan "Plan B + Den", 1 bed, 2 baths, the plan's size.
- The kit files this scan id under "Plan B + Den" itself (`matterport_model_id`).

So **the pairing was right**: the claim is about Plan B and the scan is Plan B's own scan (record-filed, and its
title names Plan B, 1 bed). It was not a scan of a 3-bed plan. The building's only 3-bed plans have no scan at all.

## Code path that produced the mismatch

Reproduced exactly: the judge as of commit 5c0b7ae (the code the run used, extracted with `git archive` and run
offline) gives the same verdict and `found` text as the saved run for all unit claims (`SAME-AS-SAVED` on every row).

In that judge:
1. `_usable` kept the scan (plan tag "Plan B" == claim label) and the record.
2. `winner = sorted(usable, key=RANK)[0]`: scan ranks above record, so the scan won.
3. `found = observed.bedrooms` = 3, i.e. the **room-label count** (the den and two other spaces were labelled
   "Bedroom" in the scan). There was no rule against trusting label counts then.
4. `" + den"` was appended because the title contains "plus Den" (`re.search(r"\bden\b", model_name)`).
5. `round(3) != round(1)` -> `contradicted`.

The same mechanism made 8 of the run's 9 hard mismatches (example counts): c4/c15 "0 bathrooms" (labels all "Other"),
c9 "5 bedrooms" (2-bed plan), c14 "0 bedrooms + den", c17 "3 bedrooms + den", c19 "2 bedrooms + den",
c20 "1 bathroom", c26 "3 bedrooms" (2-bed plan).

Root cause: **scan room-label counts treated as fact**, plus "+ den" read from the title making it look like a
different kind of home. The room-label rule was fixed after this run (commit 54ff71c, "Judge: cut false alarms",
CONTRACT: label counts may contradict only when the scan's title or the plan's record gives the same count).

## Wrong-pairing paths that were still open (fixed now)

The hypothesis (a claim about one plan judged against a scan of another) did not cause this run's mismatch, but
three paths could produce it on a multi-plan page; they are closed in this change:

1. **Page metadata listing several kinds of home** (`harness/claims/extract.py`, `_jsonld_from`): this run's
   claim `c13` is "0 bedrooms" for the community name, read from JSON-LD `numberOfRooms: [0, 1, 2, ...]`.
   `to_number(list)` took the first (lowest) number. Here it ended "not in the building's records"; with a scan
   linked to that label it would have been a 0-bed claim against a real scan. Now a list or min/max range with
   more than one value gives no claim (one distinct value still does).
2. **A scan linked to a plan whose own title names another plan code** (kit misfiling or a loose link):
   `judge._other_plan` sets it aside for that plan's bed / bath / size claims ("titled '... Plan X ...', which
   names another floor plan, so it was not used for this plan"); the record decides, else can't check.
3. **Plan names that state different kinds of home** were the "same plan" by prefix (`_same_plan("1 Bed",
   "1 Bed + Den")` was True). Now two names that both state a bed count / den and disagree are different plans.

Already correct before this change (verified by new tests): unnamed unit claims are confirm-or-can't-check only;
a scan without a plan tag never decides a labelled claim; type-level links (`check_type_claim`) only confirm or
can't check; `link_plan` never attaches a 3-bed plan's scan to a 1-bed / studio / community-name label.

## Re-judged offline (current judge + this change), same saved evidence

A re-judge script used `link_plan` / `check_type_claim` for type-level labels, then `judge`. Labels are relabelled,
sizes are invented, and bed and bath counts are an example.

| claim | label | kind | saved verdict | now |
|---|---|---|---|---|
| c4 | Plan C + Den | baths 2 | contradicted (0 baths) | confirmed (title "2 Bath"; labels not relied on) |
| c9 | Plan E | beds 2 | contradicted (5 beds) | confirmed (title "2 Bed") |
| c10 | Plan E | 700 sq ft | contradicted (1,150 measured) | contradicted (unchanged, see risks) |
| c11 | Plan F | 1,000 sq ft | confirmed | close (800 measured, 20% smaller; later band change) |
| c14 | Plan C | beds 1 | contradicted (0 + den) | confirmed ("1 bedroom + den" from title) |
| c15 | Plan C | baths 2 | contradicted (0) | confirmed |
| **c17** | **Plan B** | **beds 1** | **contradicted (3 + den)** | **confirmed**: "The 3D scan is titled '... Plan B - 1 Bed / 2 Bath plus Den', which gives 1 bedroom + den. Its room labels count 3 bedrooms, which we do not rely on. The building record also says 1." |
| c19 | Plan D | beds 1 | contradicted (2 + den) | confirmed |
| c20 | Plan D | baths 2 | contradicted (1) | confirmed |
| c26 | Plan F | beds 2 | contradicted (3) | confirmed |

All other unit claims unchanged. Hard mismatches: 9 -> 1 (c10). With the extractor change the
JSON-LD "0 bedrooms" claim (c13) would no longer be produced at all.

## Open risks

- c10: Plan E's own scan (title "Plan E - 2 Bed / 2 Bath") measures about 1.6 times the size listed and in the
  record, and its labels count 5 bedrooms. Linked by record and title, so by the rules it stays a size mismatch;
  the scan may cover more than the unit. Not a pairing issue; left for a decision.
- Unnamed unit claims ("1 Bed" with no plan name) can never be a mismatch, even on a true single-unit page,
  because the judge has no single-unit signal. Needs a run-level flag (run.py / claims), not owned here.
- `server/claim_field.py` runs `judge` per source without `type_verdict`; type-level plan claims rely on
  `type_evidence` not carrying a single size there. Not changed.
