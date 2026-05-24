# What 178,749 Broken Things Tell Us

## Story Spine

**Core claim**: A volunteer-collected ledger of 178,749 repair attempts at Repair Cafes around the world reveals a sharp split in our material culture: the more electronic an object is, the less likely it is to be saved — and a tiny but rising chorus of volunteers is now asking ChatGPT for help.

**Tension**: We treat "broken" as a property of the object, but the data shows it is a property of the design. A trouser leg that needs hemming gets fixed 96% of the time. A printer made by a multinational corporation gets fixed 37% of the time. The difference is not effort. It is access — to a part, to a screw, to a circuit diagram.

**Payoff**: After reading this, "throw it away" should feel like a choice an object's manufacturer made for you, not a verdict about the object itself. And the next time someone says they used ChatGPT to fix a coffee maker, you'll know what year that started showing up in the global data.

## Sections

### edt_01: Hook — The split between sewing and circuits
**Evidence**: ana_04, ana_08, ana_02 | **Context**: det_05

[ana_02] Volunteers at Repair Cafes around the world have logged 178,749 repair attempts since 2015. Sixty-three percent of those items got fully fixed. Another 13% got partly fixed. About a quarter — 43,112 specific objects — were declared dead on arrival.

[ana_04, ana_08] Whether your thing makes it through depends almost entirely on what kind of thing it is. Knives and scissors are saved 97.5% of the time. Trousers, 96.0%. Garden shears, 95.4%. Printers, 36.8%. Electric kettles, 39.9%. The dataset draws a hard line: things you can sharpen, sew, or unscrew end up fixed; things with sealed circuit boards end up in landfill.

[det_05, editorial] This is what planned obsolescence looks like in microcosm. Each of those 178,749 rows is one person's small attempt to reject the throw-away default — and one volunteer's note about whether the object's design let them succeed.

[CHART: ana_04]
[MEDIA: image]

### edt_02: A short history of the fix-it cafe
**Evidence**: ana_06, ana_01 | **Context**: det_01, det_02

[det_01] On 18 October 2009, in a converted theater in Amsterdam-West, a Dutch journalist named Martine Postma held the first Repair Cafe. She had become preoccupied, after the birth of her second child, with how much serviceable stuff Europeans throw out. The fix she invented was social: invite neighbors with broken things, pair them with volunteer fixers, serve coffee.

[det_01, det_02] Sixteen years later there are nearly 3,200 Repair Cafes in more than forty countries. Many log every item they touch into Repair Monitor, the foundation's voluntary dashboard. The TidyTuesday 2026 dataset is the raw row-level export of that dashboard — 447 branches across 25 countries, including the free-text fields where volunteers write what was wrong, what they did, and what stopped them.

[ana_06] Activity has compounded into a hockey stick. Twenty-eight repairs were logged in 2015. By 2019 that grew to 15,491. COVID closures cut volume in half during 2020 and 2021, then growth resumed: 29,406 repairs in 2023, 39,981 in 2024, 45,165 in 2025. Volunteer reach roughly doubles every two years.

[CHART: ana_06]

### edt_03: The two items everyone brings
**Evidence**: ana_03, ana_05 | **Context**: det_06

[ana_03] Two items dominate the door: coffee makers (10,770 attempts) and vacuum cleaners (10,284). After that come trousers (6,769), bicycles (4,887), and sewing machines (4,614). The list is sticky — the foundation reported the same two leaders in their 2018 analysis.

[ana_05, editorial] The Netherlands accounts for 50.8% of all logged repairs in this dataset. Half of those coffee makers are Dutch coffee makers, and the most common Dutch coffee maker is a Senseo. Read the rankings with that in mind: this is what breaks in the rich world, weighted toward the country that invented the cafe.

[CHART: ana_03]

### edt_04: What kills a vacuum cleaner
**Evidence**: ana_21, ana_09, ana_14 | **Context**: det_04, det_06

[ana_21] Take vacuum cleaners. Volunteers logged 10,284 attempts and salvaged 61% of them. Of the failures, the largest single tag is just "No way to fix the product" (7.5%). Right behind it: "Spare parts not available at repair session" (7.3%), "Spare parts too expensive" (6.0%), "Too worn out" (5.9%), and — telling — "No way to open the product" (3.8%). Modern vacuums are built with plastic clips and proprietary screws that resist amateur disassembly.

[ana_09, det_06] Across all 65,999 failed and half-fixed records, the same pattern holds. Spare-parts problems collectively (not at session, not on market, too expensive) account for 9,042 tags — the single largest barrier when grouped together. The 2018 foundation analysis warned about this: in 46% of unsuccessful repairs, the blocker was a non-replaceable broken part. Six years later, parts are still the wall.

[ana_14, det_04] The pattern divides cleanly along electrical lines. In electric tools and electric household appliances, 7-8% of all attempts (not just failed ones) get blocked by missing or expensive parts. In textile, that number is 0.5%. The EU's new Right-to-Repair Directive 2024/1799 — entering force in member states by July 2026 — was written for exactly this asymmetry: it requires manufacturers of covered products to make spare parts and repair information available "within a reasonable time and price."

[CHART: ana_09]

### edt_05: The brand that vacuums won't survive
**Evidence**: ana_16 | **Context**: det_05

[ana_16] Holding the product type fixed and looking just at brands, the gap is stark. Among vacuum cleaners with at least 100 logged attempts, Henry succeeds 69.2% of the time. Miele, 66.0%. Philips, 64.8%. Dyson — the brand most associated with premium price and proprietary design — sits last, at 47.4%, across 1,202 attempts. Among coffee makers, Philips (the Senseo) leads at 59.5%; Braun comes last at 30.9%.

[editorial] Volunteer brand strings are noisy and Dyson units may also skew newer. But the spread — twenty-two percentage points between top and bottom — is too large to wave away as sampling chance. There is a real, measurable cost to design choices that lock fixers out.

[CHART: ana_16]

### edt_06: The vintage rebound
**Evidence**: ana_18, ana_19 | **Context**: det_05

[ana_18] Plot success rate against the item's age and you get a U-shape. Brand-new items (0-1 years old) get fixed 67% of the time. Then success drops, bottoming out around 6-15 years (around 56%). Then it climbs again. Items 21-30 years old are repaired 61% of the time. Items 31-50 years old, 62%. Items over fifty, 63%.

[ana_19] The vintage rebound makes physical sense once you read what those old items are. Of the 14,112 items in the dataset aged twenty years or more, the top categories are sewing machines (1,212), clocks (553), vacuum cleaners (483), radios (471), turntables (356), and bicycles (331). These are pre-throwaway-era objects, made when steel cost less than electronics, with replaceable parts and accessible internals. They were built to last and they are still standing.

[CHART: ana_18]

### edt_07: When fixers ask the chatbot
**Evidence**: ana_12, ana_13 | **Context**: det_07

[ana_12] Volunteers can record where they got their repair information. YouTube has been the dominant external source since the dashboard began — about half a percent of all logged repairs cite it as a source, fairly stable across years. Generative AI is brand new. Zero mentions before September 2023. Two mentions in 2023. Eight in 2024. Fourteen in 2025. Two in the first eight months of 2026.

[ana_13] The verbatim values are revealing. Volunteers wrote it as "chat gpt", "Chat GPT", "CHAT GPT", "chatgpt", "Chat gpt" — six different capitalizations of the same product. Others logged "WWW.OPENai.COM", "AI Perplexity", "perplexity et manuel" (using AI alongside a paper manual), and one even pasted a complete OpenAI conversation share URL. YouTube is named consistently across thousands of rows. AI is so new that volunteers have no agreed-upon name for it.

[editorial] The total volume — 26 AI mentions versus 843 YouTube mentions — is tiny. But this is the first time a volunteer-collected, time-stamped, global dataset has captured the entry of generative AI into the practical toolkit of amateur fixers. The graph is not large; it is just the beginning of one.

[CHART: ana_12]

### edt_08: The trouser test
**Evidence**: ana_20, ana_08 | **Context**: det_05

[ana_20] One of the cleanest stories in the data hides inside the third-most-common item. Trousers and pants got 6,769 attempts, and 96% of them ended in success. Read the defect text and you find out why: "te lang" (615 times), "korter maken" (195), "pijpen te lang" (99), "too long" (87). The dominant trouser "repair" is hemming. People are bringing in clothing to be altered — to fit a body — not because anything is broken.

[ana_08, editorial] This is its own quiet finding. The textile category has a 92.3% success rate, and a sizable share of that is alteration disguised as repair. The line between "fix" and "tailor" turns out to be blurry; the line between "fixable" and "unfixable" is much sharper, and it is drawn by the manufacturer.

[CHART: ana_20]

### edt_09: The voices in the failure column
**Evidence**: ana_23 | **Context**: det_08

[ana_23] The free-text "why we couldn't fix it" field, read in bulk, is unexpectedly moving. A coffee maker: "product is van inferieure kwaliteit, slecht te repareren" — the product is of inferior quality, badly repairable. A printer: "Vital Component Failure. Not available to purchase." A laptop: "Het apparaat is te oud om nog te repareren" — the device is too old to be repaired. A radio: "Schema nodig, niet te vinden" — circuit diagram needed, cannot be found. An amplifier the volunteer dragged into the cafe: "versterker heeft computer die alles checkt, maar wil niet starten, ook vol sigarenrook" — amp has a computer that checks everything but won't start, also full of cigar smoke.

[det_08, editorial] These are not statistics; they are tiny ethnographic field notes. Each row is a small story about a specific object meeting a specific obstacle. The Repair Monitor dataset is rare in capturing this voice at all — manufacturer warranty data never records what the user thinks happened.

[MEDIA: instance]

### edt_10: 2,707 tonnes, and counting
**Evidence**: ana_22 | **Context**: det_03, det_04

[ana_22, det_03] The Repair Cafe Foundation, drawing on a master's-thesis estimate by British researcher Steve Privett, says one successful Repair Cafe fix prevents about 24 kilograms of CO2 emissions — mostly from the manufacture of the replacement that didn't have to be made. Apply that figure to the 112,776 successful repairs in this dataset and you get 2,707 tonnes of CO2 prevented. The cumulative line tracks the volume curve: a tonne by 2015, 213 tonnes by 2018, 1,287 by 2023, 2,594 by 2025.

[det_04, editorial] That is one community-collected sample of one global movement. The foundation estimates the full network — 3,200 cafes — could save more than 8.5 million kilos of CO2 a year if all branches were active. Three months after the most recent rows in this dataset, EU member states must transpose Right-to-Repair Directive 2024/1799 into law. The same volunteers who wrote "Schema nodig, niet te vinden" — circuit diagram needed, cannot be found — finally have a regulator behind them.

[CHART: ana_22]

### edt_11: Close — fixable is a design choice
**Evidence**: ana_15, ana_04 | **Context**: det_05

[ana_15] Volunteers also rate each item on a 1-to-10 repairability scale — easy to fix, hard to fix. The score is monotonic: items rated 1 are fixed 13.7% of the time, items rated 10 are fixed 85.8%. The repairability score is, in effect, a volunteer-given anti-obsolescence rating. It works.

[editorial] If you remember one thing from this dataset, make it this: fixable is not a property of the object. It is a property of the design. Trousers in the 1880s and trousers in the 2020s have the same fixability — needle and thread will hem either of them. A coffee maker in the 1980s and a coffee maker in the 2020s do not. The Repair Cafe data, row by row, is the largest community-collected proof of where that gap is, what it costs us, and which manufacturers are quietly responsible.

[CHART: ana_15]

## Editorial Notes

- The 96% trouser repair rate is load-bearing — keep it visible early.
- The 47.4% Dyson figure must remain exact; do not round to "around 47%" or "below 50%". Same for the Henry 69.2% / Miele 66.0% pairing.
- The "no agreed-upon name for AI" point requires the verbatim variant list be visible — at least three of the six capitalizations of "ChatGPT".
- Keep the Dutch dominance caveat (50.8% NL share) in the country/product paragraphs to anchor honesty.
- The 24 kg CO2 figure comes from a single master's thesis (Steve Privett); we should keep the attribution visible so the reader knows it's an estimate.
- ChatGPT trend uses absolute counts (2 → 8 → 14) — these are tiny but the trajectory matters; do not show a percentage chart that would make it look noise-level.
- The full quote "versterker heeft computer die alles checkt, maar wil niet starten, ook vol sigarenrook" should be presented in original Dutch with translation; it is one of the funniest lines in the dataset.
- ana_07 (repairability distribution histogram), ana_10 (raw multilingual phrases), ana_11 (defect themes) are CUT for editorial focus — they would dilute the story spine.
- ana_17 (country success rates) is also cut; geography is touched obliquely via NL caveat without becoming a section.
