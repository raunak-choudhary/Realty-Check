# Two-minute talk track

Realty Check, about 2 minutes, same for video and live demo.

## 1. The hook (15 s)

- "I love to travel. I book a stay the way everyone does. Twelve photos, a paragraph written by the person who wants my money, and I pay."
- "Then I open the door. The room is smaller. The second bedroom is a den with no closet."
- "Same story when you rent, buy a house or lease an office. The person selling writes the listing, and nobody checks it."

## 2. The idea (15 s)

- "The truth is already on file. CoStar has the building record. Matterport has walked the space in 3D. Vexcel has it from the air. The county has the paperwork."
- "Realty Check is a custom agent harness that brings that record to the listing. You get a reality check before you pay."

## 3. The demo (60 s)

- Open a listing. Click the address. "That is all the user does."
- While it runs: "An orchestrator reads every claim on the page. Three agents go and look. One walks the 3D scan, one measures the building from the air, one reads the records."
- Drawer lands: "About a minute. One thing doesn't match. Listed value struck through, value on record beside it, a confidence score, and the source that decided it."
- Open the full report: "Listing says two bedrooms. The scan opens in the exact room. It is a den. You are looking at it yourself, you don't take our word."
- Scroll: "Here is what the listing left out, and the questions to ask before you commit."
- Last page: "Every claim, every source, side by side."

## 4. Why it is a harness, not a chatbot (20 s)

- "Built on LangChain deepagents, and we changed almost every default."
- "We took tools away. Agents can call our six tools and nothing else."
- "Hard limits. 14 model calls, 96 seconds."
- "The model never judges. It gathers evidence. Fixed rules give the verdict."
- "No citation, no verdict. It says 'couldn't check' and stops there."

## 5. Proof it works (10 s)

- "First version flagged 20 mismatches across ten real sites. Most were wrong. After the rule rewrite, the same ten sites gave 2."
- "One check went from 147 seconds to 56."

## 6. Close (10 s)

- "We tested on apartments in Houston and Los Angeles. The harness only needs page text and an address, so short stays, homes for sale and offices are next."
- "Then an API, so a platform can check a listing before it is published."
- "Realty Check. Is this listing what it says?"

## If asked

- **Who pays?** Listing platforms, brokerages, property managers. Wrong listings cost them tours and disputes.
- **Why trust it?** Every verdict links to its proof. A missing record is never counted against the listing.
- **What is the model?** Claude, inside our own harness. It reads and gathers. It never decides.
