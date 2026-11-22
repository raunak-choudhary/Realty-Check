# Claim reading instability: diagnosis (Building A, a large LA apartment page)

Test write-up from the build, with building identities and record values removed.

Saved runs of the same building page:

| run | time | claims | plan-labelled unit claims | distinct plan facts | unlabelled unit nums | amenity/view/other |
|---|---|---|---|---|---|---|
| Run 1 | 04:30 | 39 | 28 | 24 | 0 | 10 |
| Run 2 | 04:42 | 39 | 28 | 24 | 0 | 10 |
| Run 3 | 09:32 | 23 | 7 | 7 | 3 | 12 |
| Run 4 | 09:57 | 23 | 7 | 7 | 3 | 12 (identical to 09:32: prompt cache hit) |
| Run 5 | 14:51 | 24 | 7 | 7 | 3 | 13 |

(+1 JSON-LD "Studio" bedrooms claim in every run.) The page has 8 floor plans x (beds, baths, size) = 24 plan facts.

## Why 39 vs 24

1. **A deterministic bug, not the model (the main cause, -17 plan claims).** Commit 3c28894 (04:55) added
   `GROUP_RE` (group headings like "One Bedroom" over plan cards) and made any line matching it end the current
   plan block. On this page every card is laid out as `Plan X / Starting base rent / 1 Bed / "/" / 1 Bath / 600-750 Sq Ft`
   (invented values), so the card's own "1 Bed" line ended the card: "1 Bed", "1 Bath" and the size lost their plan label.
   Knock-on effects:
   - the prompt excerpt drops repeated unlabelled lines, so cards 2-8 reached the model with no "1 Bed" /
     "2 Baths" lines (the excerpt showed e.g. `Plan B + Den / Starting base rent $N / 800-850 Sq Ft`).
     The model labelled only what it saw: 7 plan facts instead of 24;
   - the rule layer read 3 unlabelled numbers (a bedroom count from the hero line, a bath count and a size) and
     filled them into the list as unit claims belonging to no plan.
   The 04:30/04:42 runs used the code before that commit (they also carry the old "[JSON-LD] ..." quote).
2. **Duplicates inflated the 39.** The model labelled cards "Plan C + Den" and the rules labelled the same cards
   "Plan C": 28 plan-labelled claims held only 24 distinct facts (three plans' baths and sizes twice).
3. **Free-form model output varies on every fresh call.** 09:32 vs 14:51 (same code family; the prompt differed,
   from code or page-text changes, so the prompt cache missed): a three-item amenity sentence came back as one claim
   vs two separate claims, a "largest rooftop" line as amenity vs amenity + other, and two hero-bullet amenities
   in or out. Controlled re-run of the HEAD extractor
   below: 37 / 34 / 34 claims on one fixed snapshot, only 20 claims in all three runs (union 54).
4. **The page text changes daily**: an "available as soon as" date, a starting price and a count of available units.
   These lines were in the prompt, so the prompt-hash cache missed on any later day and a fresh, different reading
   followed.
5. **The 40 cap.** "Max 40 items" in the prompt plus MAX_CLAIMS=40 in code: on pages with more claims the model
   chose which 40 to return (several other pages sit at exactly 40 in every run).

## Fix (EXTRACTOR_VERSION claims-2026-11-14.2)

- Plan blocks: a "1 Bed" line ends a card only when it is a real group heading (right above a bare-name card).
  Rules now read all 24 Building A plan facts, labelled, with no model.
- Fixed numbered candidate statements (lines; long lines cut into sentences; page order; card label from
  the layout; volatile price/date/availability lines left out), one model call judging each statement.
- Code fixes labels (card label), numeric scope, sq ft range low end, quotes (statement words), short list
  item values (the item's own words), comma amenity lists split by a fixed rule, dedupe on (kind, label, value)
  or on the same record amenity names, page order within rank, record-named features ranked before
  other features under the 40 cap.
- Per-page cache of the final list keyed by version + address + page text without volatile lines + JSON-LD.

## Live check: extractor alone, cache OFF (RC_NO_CACHE=1), 3 runs per page, one model process at a time

| extractor | page | counts | in all 3 runs | union | model calls/run | seconds/run | prompt chars |
|---|---|---|---|---|---|---|---|
| HEAD (old) | Building A | 37, 34, 34 | 20 | 54 | 1 | 21, 18, 19 | 5,503 |
| new | Building A | 40, 40, 40 | 39 | 41 | 1 | 28, 29, 31 | 7,646 |
| HEAD (old) | Building B | 40, 40, 40 | 31 | 49 | 1 | 12, 12, 12 | 2,865 |
| new | Building B | 40, 40, 40 | 35 | 45 | 1 | 13, 14, 14 | 5,035 |

Key = (kind, label, value). New Building A: all 24 plan facts in every run; the only difference is one claim:
one amenity read as parking (runs 1, 3) vs another amenity making the cut (run 2). New Building B
differences are wording of long-sentence features (a hyphen or a space dropped between two words).
Uncapped, the new Building A reading has 56 claims (54 checkable); the cap keeps numbers, then
record-named features, then the rest. With the cache on, a re-run of the same page returns the identical list
with no model call.
