# What Kills Small-Plane Pilots

Fifteen years of NTSB findings, 2010-2024.

## Story Spine

**Core claim**: The story of general-aviation accidents in the United States is the gap between what is *common* and what is *lethal* — engine failures show up in nearly a quarter of NTSB investigations but kill 13% of the people they involve, while spatial disorientation appears in fewer than 2% of investigations and kills 95% of them.

**Tension**: Most pilots are trained to fear an engine quitting at low altitude. Most news coverage focuses on the spectacular multi-fatality crashes. Neither is the thing the data says you should worry most about.

**Payoff**: After reading, a non-pilot understands the actual geometry of small-plane risk in the United States — what the National Transportation Safety Board has been writing in its own words for fifteen years about how people die in light airplanes, and why three conditions (instrument weather, night, maneuvering) explain more than half of every death in the dataset.

---

## Sections

### edt_01: Hook — the 95% number

**Evidence**: ana_18, ana_04, ana_20 | **Context**: det_06, det_09

[ana_18] In the National Transportation Safety Board's published findings for 17,525 small-airplane accidents between 2010 and 2024, one cause-language pattern stands out from everything else. When NTSB investigators wrote that a pilot lost spatial orientation — usually inside a cloud or at night without visible horizon — the result was a fatality 95.0% of the time. That phrase shows up in only 298 of the agency's probable-cause reports. It carries 558 of the period's roughly 3,200 deaths.

[ana_18, ana_20] Engine failure, by contrast, is the thing pilots are explicitly trained to fear. It shows up in 3,876 NTSB reports — almost a quarter of the dataset. And it is fatal 12.7% of the time. The crowd of small-aircraft accidents the public sees on local news as a "plane went down" is mostly forced landings into fields and trees, not these. The kind of accident that kills almost everyone aboard is rare, specific, and largely invisible to the general reader.

[ana_04, det_09] The headline shape: 17.9% of the aircraft involved in NTSB-investigated Part-91 accidents over 15 years had at least one fatality. The other 82% killed no one. The story is in the gap between those two numbers — what makes an accident land in the 18% versus the 82%.

[CHART: ana_18]
[MEDIA: image]

---

### edt_02: What you're looking at

**Evidence**: ana_01, ana_06, ana_12 | **Context**: det_01, det_02

[ana_01, det_01] The dataset is the NTSB's complete public Aviation Accident Database, filtered to civil flights conducted under 14 CFR Part 91 — the regulatory regime for non-commercial small-aircraft flying, the private side of American aviation — between January 1, 2010 and December 31, 2024. Each row is the formal output of a federal accident investigation; the narratives field is the agency's actual probable-cause language, not a journalist's summary. Coverage on the structural fields a reader needs is essentially complete, and 98.5% of events have a probable-cause text attached.

[ana_06] The fleet is overwhelmingly fixed-wing airplanes — 88% — with helicopters next at 7% and a long tail of gliders, balloons, weight-shift trikes, gyrocopters, ultralights and powered-parachutes filling out the rest. When you hear someone say "small-plane crash," nine times out of ten they mean a single-engine piston airplane, often a Cessna or a Piper of a certain age.

[ana_12, det_02] What this is *not* is commercial aviation. American airlines have flown for years on end without a passenger fatality on U.S. soil. Part 91 has not. Most of the small-plane crashes that show up in local news happen here — under a regulatory regime that more closely resembles driving a car than catching a flight on Delta, with a single pilot, no second-in-command, weather decisions made by the person flying the airplane, and a personal-flying mission in nearly three out of four cases.

[CHART: ana_06]

---

### edt_03: The fifteen-year trend

**Evidence**: ana_02, ana_03 | **Context**: det_03

[ana_02, det_03] Across the fifteen-year window, the total number of investigated Part-91 accidents fell from 1,344 in 2010 to 1,038 in 2024 — a 22.8% drop. The share that were fatal stayed roughly flat at 15-21%, with 2024's 15.2% the lowest in the series. The decline is real but it is mostly fewer accidents happening, not crashes that would once have been fatal becoming survivable. The FAA's industry benchmark moved in the same direction — fatal accidents per 100,000 flight hours fell from 1.27 in 2001 to roughly 0.65 in 2023 — a slow grind of compounding safety improvement spread across pilots, airframes, training, and avionics.

[ana_03] The seasonality is sneaky. Total accidents peak in July (2,113 in fifteen Julys) and bottom out in December (953) — pilots simply fly more in the summer. But the *share* of accidents that kill someone runs the opposite direction: December (22.4%), November (21.3%) and January (19.4%) are the worst three months for fatal share, exactly when daylight is short and instrument-condition weather is common. The chart that makes this work is one with months on the x-axis and two series: counts as bars, fatal share as a line. They cross.

[CHART: ana_02]

---

### edt_04: Common vs. lethal — the centerpiece

**Evidence**: ana_18, ana_19 | **Context**: det_05, det_06

[ana_18] If you put every probable-cause language pattern on a chart where the x-axis is "how often does this appear in NTSB findings?" and the y-axis is "when it appears, how often does someone die?", four clusters emerge. In the upper-left — rare and almost always fatal — sit spatial disorientation (95% fatal share), structural failure or in-flight breakup (86%), controlled flight into terrain (85%), stall-spin combinations (82%), and alcohol or drug impairment (82%). In the upper-right — common and very often fatal — sit pure loss of control in-flight (1,646 events / 51% fatal) and aerodynamic stall (1,420 / 50%). In the lower-right — common but mostly survivable — sit engine failure (3,876 / 13%), landing-phase accidents (6,940 / 4%), and runway excursions (990 / less than 1%). The lower-left is empty, because the NTSB does not investigate trivial accidents.

[ana_18, ana_19] What this shape tells you is that the things that kill GA pilots are not the things that make a runway useless. The plane that veers off the centerline at touchdown will be in the database tomorrow morning; the people in it will not. The plane that the pilot loses spatial orientation in over a cloud deck at night will be in the database, and so will the obituaries. Phase-of-flight reinforces this: landing mentions are 40% of cause-text coverage but 4% fatal, takeoff mentions 15% / 18% fatal, and maneuvering is 5% of mentions but 55% fatal. Where in a flight the airplane stops behaving as the pilot expected matters as much as why.

[ana_18, det_06] The "loss of control in-flight" cluster — LOC-I in the aviation-safety acronym — is what the NTSB and the General Aviation Joint Steering Committee have spent two decades chasing on their Most Wanted Lists. The 1,646 events of straight LOC-I, plus the 1,420 aerodynamic stalls, plus the 235 stall-spins, plus the 298 spatial-disorientation cases — these patterns overlap heavily but, taken together, account for over 1,800 of the 3,165 fatal aircraft-row entries in the dataset. More than half of all deaths in fifteen years are concentrated in fewer than ten language patterns.

[CHART: ana_18]

---

### edt_05: VFR into IMC

**Evidence**: ana_15, ana_16 | **Context**: det_05

[ana_15] Only 4.1% of investigated accidents — 712 events — happen in instrument meteorological conditions (clouds, fog, severely reduced visibility). But of those 712, 462 are fatal. The fatal share in IMC is 64.9%, against 15.4% in VMC. The ratio inside the dataset is 4.2×; the per-flight-hour ratio in the aviation-safety literature is closer to 14×, because most GA pilots fly almost no IMC. The accidents that happen in clouds are very nearly five times more likely to kill someone than the ones that happen in clear air.

[ana_16, det_05] The most dangerous specific combination is the one the NTSB has been warning about for decades: a pilot flying under visual flight rules ends up in instrument conditions. Structurally — weather logged as IMC, flight plan filed as anything other than IFR — there are 336 such events in the dataset. 72.9% are fatal. With no flight plan filed at all (NONE), 275 events and a 74.5% fatal share. With a filed VFR plan, 27 events and 66.7% fatal. The 1954 University of Illinois study that found non-instrument-rated pilots lose control in 178 seconds of entering cloud is sixty years old; the data says it is still describing what happens.

[ana_16] What the same chart shows, almost as an afterthought, is that the comparable IMC-with-IFR-plan case — instrument-rated pilot flying on an IFR plan, still in IMC — is fatal 58% of the time. Instrument flying does not make IMC safe in absolute terms. It makes it survivable enough that airline-scale operations work. The gap between IFR-in-IMC and VFR-in-IMC is the difference between a system designed for clouds and a system improvised in clouds.

[CHART: ana_16]

---

### edt_06: After dark

**Evidence**: ana_17 | **Context**: det_06

[ana_17] Ninety percent of investigated accidents happen in daylight, with a 16.2% fatal share. The night sub-bucket is 6.4% of accidents (1,119 events combined) but its fatal share is 37.4% — 2.3× the daylight rate. Inside night, the difference between an ordinary lit-up night and a dark night without moon or ground lights is even sharper: the "dark night" subcategory (NDRK, 313 events) is 55.6% fatal. A "bright" moonlit night is 9.5% — actually safer than the daytime baseline.

[ana_17, det_06] Dawn and dusk twilight are not worse than full daylight in fatal share (17.7% and 18.3%). The pattern that emerges is not about low ambient light per se but about the absence of visible reference outside the cockpit — exactly the conditions in which spatial disorientation occurs. Looking back at edt_04: spatial disorientation appears in 95% of cases that involve it as a fatal, and the conditions that produce it are the same conditions you see in this chart's worst bar.

[CHART: ana_17]

---

### edt_07: The geography of the data, and Alaska

**Evidence**: ana_13, ana_14 | **Context**: det_07

[ana_13] California (1,575 events), Texas (1,513), and Florida (1,385) lead the absolute counts, in roughly the order their GA fleets size them. Alaska is fourth with 1,016 events — 5.8% of the U.S. dataset, despite having less than 1% of the country's population. That is roughly seven to eight times the lower-48 per-capita rate, consistent with longstanding NTSB and academic findings that Alaska's accident rate per flight hour is approximately double the national rate.

[ana_14, det_07] But here the data does something the Detective-stage research did not predict. Alaska's per-accident fatal share is only 9.6% — about half the lower-48 rate of 18.2%. Said differently: Alaska has roughly twice the rate of accidents and roughly half the rate of fatal outcomes per accident. The likely explanation, given the conditions described in det_07, is what bush-flying communities have always understood: a lot of Alaskan GA flying is short-distance, low-altitude, low-speed work onto unimproved strips, ridges, sandbars, and water. Those crashes ruin airframes; they often spare the people inside. The state has more accidents and more survivable ones, both for the same reason.

[MEDIA: map]

---

### edt_08: The fleet that won't quit

**Evidence**: ana_07, ana_09, ana_11 | **Context**: det_04, det_08

[ana_07, det_08] Three manufacturers account for half of every accident: Cessna 27.3%, Piper 16.8%, Beech 6.3%. The Cessna 172 alone, in its various dash-letter variants, accounts for over 1,800 events — a function of the airplane being the most-built civilian aircraft in history (over 44,000 produced since 1956). Fatal share within accidents, though, is highest among the high-performance singles: Beech, Cirrus, and Mooney each cluster around 26-28% fatal — well above Cessna's 13.8% — consistent with their faster cruise speeds and tighter handling margins.

[ana_09, det_04] One contrast worth being careful about is the homebuilt premium. Outside research (det_04) puts the experimental / amateur-built fatal accident rate per flight hour at roughly four times the certificated rate. The fatal share *inside* this dataset's accidents is 22.2% for homebuilts and 17.3% for factory aircraft — a 1.28× ratio. These are different statistics: the 4× per-hour ratio includes both higher accident frequency *and* higher severity-per-accident; the 1.28× ratio is just the severity-per-accident leg of it. Both are real, both are higher than baseline, but the headline number to use depends on the question. For "how dangerous is buying a homebuilt?" the per-hour number applies. For "if a homebuilt crashes, how does it compare to a factory plane crashing?" the per-accident number is right.

[ana_11] The fleet itself is older than almost any other class of operational machinery in U.S. consumer life. The median aircraft in an NTSB-investigated accident in 2010-2024 is 39 years old. 46% are over forty. 27% are over fifty. New piston singles have been priced out of casual ownership since roughly 2000, and well-maintained airframes from the 1960s and 70s are still flying — and still crashing. This is not a fleet that will be turned over by attrition. The safety improvements that matter are the ones that work on what is already in the air.

[CHART: ana_09]

---

### edt_09: What it adds up to

**Evidence**: ana_18, ana_19, ana_20 | **Context**: det_06, det_09

[ana_19, ana_18] Three numbers do most of the work. Maneuvering: 5% of cause-text mentions, 55% fatal. Night-dark: 1.8% of accidents, 56% fatal. IMC with no IFR plan: 1.6% of accidents, 75% fatal. None of them is the kind of thing that appears in pilot conversations about engine reliability or airframe maintenance. They are about decisions — to keep flying into deteriorating visibility, to take off into a night with no moon, to follow the road at low altitude to see something on the ground. The crashes that kill people are largely the crashes the pilot chose to set up.

[ana_20] The single deadliest event in the dataset is the July 2016 hot-air-balloon crash near Lockhart, Texas — sixteen people, on a sightseeing flight that took off in fog. The NTSB's published probable cause begins: "The pilot's pattern of poor decision-making that led to the initial launch, continued flight in fog and above clouds, and descent near or through clouds that decreased the pilot's ability to see and avoid obstacles." It is a single sentence that contains most of what this analysis has found.

[editorial] The next-most-deadly events follow similar patterns at smaller scales: an "aggressive takeoff maneuver, which resulted in an accelerated stall and subsequent loss of control at an altitude that was too low for recovery." A failure "to maintain airplane control following a reduction of thrust in the left engine during takeoff." A pilot's "inadequate decision" to continue. These are the federal investigators' words, not interpretations stacked on top. They are what the database actually says.

[ana_18, det_06, det_09] Common is not lethal and lethal is not common. Engine failures are common and survivable; spatial disorientation is rare and almost certain to kill. The story for the next decade of GA safety improvement — the one the NTSB has been writing in its Most Wanted Lists since at least 2014 — is whether anything can be done about the rare-and-lethal upper-left corner of the chart. The lower-right corner has already, slowly, given way to fewer accidents and lower per-hour rates. The upper-left is still there.

[MEDIA: image]

---

## Editorial Notes

- **Lead finding is ana_18** (the cause-language taxonomy chart). It is the single best representation of the core claim and should anchor edt_04 as the centerpiece chart. The Designer should ensure this chart is the most striking visual in the piece — a quadrant plot with frequency × fatality % is the right encoding.
- **Numbers that must remain exact**: 95% (spatial disorientation fatal share), 12.7% (engine failure fatal share), 17,525 (distinct events), 3,165 (fatal aircraft-rows), 72.9% (VFR-into-IMC fatal share), 55% (maneuvering fatal share), 39 years (median fleet age), 16 (deaths in Lockhart balloon crash). Do not round.
- **Caveats that must remain visible**: the per-hour vs per-accident distinction for the homebuilt finding (edt_08, ana_caveat_03); the structural definition of VFR-into-IMC (edt_05, ana_caveat_04); the empty phase_flt_spec column and that phase signals come from text (edt_04 footnote-style; ana_caveat_01).
- **The Lockhart NTSB quote (edt_09)** must appear verbatim — it is the climactic line of the piece. Do not paraphrase.
- **Tone**: matter-of-fact, federal-document register, not sensational. The numbers carry the weight; do not embellish with adjectives like "tragic," "devastating," "shocking." The NTSB doesn't and the piece shouldn't.
- **Cut from analysis**: ana_05 (damage distribution — substantial = 88.6%) is too uniform to chart; ana_08 (top model strings) is interesting tabularly but not chartable cleanly; ana_10 (engine count) is supporting only — covered in passing in edt_04. ana_03 (seasonality) is downgraded to a prose mention in edt_03 — the chart slot in that section goes to ana_02 instead.
- **Final paragraph rule**: end on the "upper-left is still there" line. Do not append a summary or a call-to-action.
