## Story Spine
**Core claim**: The frontier AI labs have compressed the gap between consecutive language-model releases from about four-and-a-half months in 2018 to four days in 2025 — a roughly 30x acceleration that turned model launches from seasonal events into a near-daily drumbeat.
**Tension**: We talk about AI "moving fast" as a vibe. The data says it is a measurable, near-vertical cliff — and it lands precisely on the month ChatGPT shipped.
**Payoff**: The reader leaves understanding that the AI race is not just producing better models but producing them on a fundamentally different clock — fast enough that the act of evaluating a model now takes longer than the interval before the next one arrives.

## Sections

### edt_01: Hook — Every four days
**Evidence**: ana_01 | **Context**: det_01, det_04

[ana_01] In 2018, the world's leading AI labs shipped a notable new language model about once every 132 days — roughly every four-and-a-half months. By 2025, the median gap between consecutive frontier releases was four days. That is a 33-fold acceleration in seven years.

[det_04] The pace is now fast enough to break the institutions built around it. Trackers report the three leading labs updating their flagship models every few weeks rather than every few months, and organizations that once ran six-month evaluation cycles are being forced onto four-week ones — because the top model can change two or three times inside a single quarter.

[editorial] This is the story of a clock speeding up. Not the models getting smarter, which is a different story — but the raw cadence of release, measured in days.

[CHART: ana_01]

### edt_02: The cliff was 2022
**Evidence**: ana_02, ana_04 | **Context**: det_03

[ana_02] The acceleration did not creep. From 2019 to 2021 the median gap held steady between 49 and 68 days. Then it fell off a cliff: 13 days in 2022, 5.5 days in 2023. In two years the interval compressed nearly ninefold.

[det_03] The cliff lands exactly on the ChatGPT year. ChatGPT launched in November 2022 and reached 100 million users in two months, triggering Google's internal "code red," a $10 billion Microsoft bet on OpenAI, and Meta's decision to open-source Llama. The release log shows that competitive panic as a near-vertical drop.

[ana_04] And it was the whole distribution that moved, not a few outliers. In 2019 the average gap (85 days) sat far above the median (51), dragged up by long lulls. By 2025 the two had converged — a mean of under seven days against a median of four. The quiet stretches simply disappeared.

[CHART: ana_02]

### edt_03: Eighteen times the releases
**Evidence**: ana_03 | **Context**: det_05

[ana_03] The mirror image of shrinking gaps is exploding volume. The frontier labs counted three language-model releases in 2018. In 2025 they counted 54 — eighteen times as many. The climb tracks the same inflection: 8 in 2021, 21 in 2022, 33 in 2024.

[det_05] Some of that surge is more labs entering the race, and some is point-releases — the 4.1s, the 4.5s, the "Pro" and "Heavy" and "Thinking" variants — each clearing the notability bar as a separate entry. That is not a measurement artifact so much as the phenomenon itself: labs now ship smaller, more frequent increments. A release in 2025 is a smaller step than a release in 2019, taken far more often.

[CHART: ana_03]

### edt_04: Nobody is sitting still
**Evidence**: ana_06, ana_08 | **Context**: det_06

[ana_06] This is not one hyperactive lab dragging an average down. Every frontier lab tightened its own cadence. Measured on each lab's own release-to-release gaps, OpenAI is the pace-setter at a 21-day median, followed by Alibaba at 36 and Google DeepMind at 58; even the slower-cadence labs like Mistral and xAI are constrained mostly by how recently they entered the race.

[ana_08] OpenAI's own compression is the clearest microcosm: its median gap between releases fell from 108 days through 2022 to just 17 days from 2024 onward — a sixfold tightening inside a single organization.

[CHART: ana_06]

### edt_05: From seasons to weeks — one lab's log
**Evidence**: ana_07 | **Context**: det_04

[ana_07] Read one lab's release log and you can feel the clock change. Anthropic's Claude 2 arrived 119 days after the prior release; Claude 2.1 another 133 days later — seasonal cadence. By late 2025 the gaps were measured in weeks: Claude Sonnet 4.5, then Claude Haiku 4.5 just 16 days behind it, then Claude Opus 4.5 forty days after that.

[ana_07] Twice, the gap hit zero. Claude 3 Opus and Claude 3 Sonnet shipped on the same day; so did Opus 4 and Sonnet 4. A "release" stopped being a single model and became a simultaneous family.

[CHART: ana_07]

### edt_06: When the gap hits zero
**Evidence**: ana_09 | **Context**: det_05

[ana_09] That simultaneity is its own signal. Across the dataset, 25 releases have a gap of zero days — a lab shipping two notable models on the same date. OpenAI accounts for 11 of them. And they cluster in the present: eight same-day launches in 2025 alone, against three or four a year in 2022–2024 and essentially none before 2019.

[editorial] When a lab's gap between its own releases hits zero, the cadence has effectively maxed out. There is no faster than the same day. The frontier is no longer racing to be next; in stretches, it is arriving all at once.

[CHART: ana_09]

### edt_07: The clock that won't slow
**Evidence**: ana_01 | **Context**: det_04, det_05

[editorial] Four days. That is the interval the frontier now keeps — faster than most teams can read a model card, run an eval, and write up the results.

[det_04] The pace has become a barrier to entry in its own right: keeping up is now part of what it means to be a frontier lab. The race is no longer only about who builds the best model. It is about who can keep the drumbeat going.

[det_05, ana_01] Whether four days is a floor or just this year's number is the open question. The curve has bent toward zero for seven straight years, and 2026 — only partway through — is already holding the four-day line.

## Editorial Notes
- 132 days, 4 days, and 33x must be exact in edt_01. Do not round 5.5 to 6 or 33x to 30x in the prose, though the README's "~30x" framing is acceptable as approximate context.
- The 2022 inflection must be tied to ChatGPT (Nov 2022) — that causal anchor is the spine of edt_02.
- Always flag 2026 as a partial year wherever a 2026 count appears (charts in edt_01, edt_03 should mark 2026). The 4-day median for 2026 is fine to state plainly; the COUNTS are partial.
- edt_03 must keep the point-release caveat visible (det_05) — do not let "18x" read as 18x more capability.
- ana_06 per-lab medians for xAI/Mistral/DeepSeek are small-n and pulled up by late entry — the prose already softens this; keep that framing.
- Load-bearing sections: edt_01 (hook), edt_02 (the cliff + causal anchor), edt_05 (the human-scale Claude log).
