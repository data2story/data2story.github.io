## Story Spine
**Core claim**: In early March 2020, the world's COVID-19 case map was less a record of where the virus was than a record of where countries were looking — and tourism flows showed exactly which countries were not looking hard enough.

**Tension**: The official numbers told a comforting story for most of Asia, Africa and Latin America: only a handful of cases. The Economist's tourism model said that comfort was an illusion. Russia and Indonesia, in this reading, were not lucky; they were just blind.

**Payoff**: A simple regression turned the case map into an early-warning system. The countries furthest below the prediction line were the ones to watch — and history would prove most of them right.

## Sections

### edt_01: Hook — A map that already lied
**Evidence**: ana_01 | **Context**: det_01, det_03

[ana_01] On 4 March 2020, the Johns Hopkins dashboard counted 95,124 COVID-19 cases worldwide. China held 80,271 of them. Hubei province by itself held 67,332 — more than 70% of the global total in a single Chinese province. Outside China, only three countries had crossed 2,000 cases: South Korea, Italy and Iran.

[det_01, det_03] Two days later, The Economist published a Graphic Detail piece arguing this map was already wrong. Not the China numbers, which dwarfed everything. The numbers everywhere else — the apparently quiet places where governments were still saying "we have a few imported cases, things are under control."

[editorial] What the piece had was an unusual yardstick: how many Chinese tourists each country had received the previous summer.

[CHART: ana_01]
[MEDIA: image]

### edt_02: The yardstick — Chinese tour groups as a virus-exposure proxy
**Evidence**: ana_03 | **Context**: det_02

[det_02] The Economist's data came from a slightly improbable place. China's Ministry of Culture and Tourism tracks tour-group travellers — both directions — for the top 30 destination/origin countries plus continent residuals. It was the most recent globally consistent measure of who was moving between China and the rest of the world: Q3 2019, the latest quarter available when the analysis ran.

[ana_03] The flows are wildly uneven. Thailand alone saw 1.55 million Chinese tour-group trips in a single quarter — almost twice Japan's 1.25 million. Taiwan, Vietnam, Singapore, Malaysia and Russia each handled between 400,000 and 950,000. The top ten destinations accounted for 74% of all flow.

[editorial] The intuition was simple. If the virus moves with travellers, then the more travellers a country had received, the more cases it should have — controlling, roughly, for how hard each country was looking.

[CHART: ana_03]

### edt_03: The model — what the OECD line says about everyone else
**Evidence**: ana_02 | **Context**: det_05, det_06

[ana_02] Fit a single line through the 34 OECD countries and you get a remarkably clean answer. log(cases+1) = -8.44 + 1.13 × log(tourism). The slope is highly significant (p < 1e-7) and the model explains 59% of the variance in log-cases across OECD members.

[det_05, det_06] The choice to fit only the OECD was deliberate. OECD countries had broadly similar testing infrastructure in early March 2020 — what they reported was, more or less, what they actually saw. Project that line outward to non-OECD countries and you get an "expected" caseload: how many cases each country *would* have if its surveillance worked like an OECD country's. The residual — distance from the line — becomes a surveillance gap.

[CHART: ana_02]

### edt_04: The reveal — who is far below the line
**Evidence**: ana_04, ana_07 | **Context**: det_07

[ana_07] Plotted on a single chart, the answer is immediate. OECD countries cluster around the line. Non-OECD countries scatter widely — and a striking number of them sit far below.

[ana_04] Russia is the most extreme. With 434,000 mean Chinese tour-group flows, the model expected 517 cases on 4 March. The country reported three. Indonesia: 330 expected, two reported. Myanmar: 110 expected, zero. The Philippines, Vietnam and Thailand each reported between 50 and 70 times fewer cases than the OECD-fit line implies.

[det_07, ana_04] These were not obscure countries with tiny tourism. Thailand was the single largest destination of Chinese tour groups in Q3 2019. Vietnam and Indonesia were both in the global top ten. The places best positioned to import early COVID-19 were the places reporting the fewest cases.

[CHART: ana_04]
[MEDIA: map]

### edt_05: The other end — Iran, Italy, Korea
**Evidence**: ana_05 | **Context**: det_04

[ana_05] At the opposite end of the residual list are countries whose case counts are running ahead of their tourism. Iran is the most extreme: 2,922 reported cases against a tourism-implied 12. Italy reports 3,089 against 156. South Korea: 5,621 against 392. These are not surveillance failures — they are countries where the virus had already gone domestic, where local transmission had outpaced anything imports alone could explain.

[det_04] By this point the model is doing two things at once. Below the line: a country where the virus is probably present but invisible to the surveillance system. Above the line: a country where the surveillance system is working but the outbreak has accelerated past what tourism alone seeded.

[CHART: ana_05]

### edt_06: The asymmetry — OECD versus everywhere else
**Evidence**: ana_06 | **Context**: det_06

[ana_06] Step back from individual countries and the systematic gap is unmistakable. The OECD residuals are mean-zero by construction. The 90 non-OECD countries, scored against that same line, average -0.85 log-units below it — equivalent to reporting 43% of what the OECD-pattern would predict. 64% of non-OECD countries sit below the line, against 56% of OECD members.

[editorial] Pour through the residuals and the diagnosis becomes hard to ignore: the early-March case map is shaped less by where the virus is than by who is testing for it.

[CHART: ana_06]

### edt_07: The multiplier — what the model says is missing
**Evidence**: ana_08 | **Context**: det_04, det_07

[ana_08] Read the model literally and the implied under-counts are vast. Russia: 172x. Indonesia: 165x. Myanmar: 110x. Philippines: 69x. Vietnam: 54x. Thailand: 51x. These are not absolute predictions of the truth — but they are estimates of how far the reported numbers are from the tourism-implied baseline.

[det_04] Subsequent peer-reviewed work would land in roughly the same place. A Pulmonology paper using case-fatality ratios estimated that Iran's true caseload was about 34 times its reported total in mid-March, Italy's 73 times, Spain's 161 times. A Science paper estimated 86% of pre-23-January infections in China had gone undocumented. The tourism model, fit on a single morning's data, was pointing in the same direction these much-more-elaborate methods would later confirm.

[det_07] In Indonesia, community transmission would not be officially acknowledged until late March. Iran's hospitals were already overwhelmed when its case count was being reported in the hundreds. The Economist's piece, days before either of those facts became visible, said: look at the residuals.

[CHART: ana_08]

### edt_08: Close — Reading the gaps
**Evidence**: (synthesis) | **Context**: det_05, det_07

[editorial] What was new about the piece was not the regression. It was the framing. Most early-March 2020 reporting treated case counts as a thermometer: a higher number meant a worse outbreak. The Economist's argument was that the thermometer itself was uneven — some countries were holding it under their tongue and others were leaving it in their pocket — and that tourism flows could tell you which was which.

[det_05] Read forwards, the residuals were a bet on what would happen next. The countries furthest below the line, the model implied, were the countries whose first wave was still hidden. Most of them would be in the news within weeks.

[det_07, editorial] The lasting lesson is not the specific multipliers — those are noisy, single-quarter, single-day estimates. It is the move itself: when you cannot measure a thing directly, find a proxy for what *should* be there, fit it on the part of the world that measures well, and read the gap.

## Editorial Notes
- 95,124 (global cases on 4 Mar 2020), 80,271 (China), 67,332 (Hubei) must be exact.
- Regression coefficients (-8.44, 1.13, R-squared 0.59) must be exact.
- Multipliers (172x Russia, 165x Indonesia, etc.) must be exact.
- Iran 2,922; Italy 3,089; South Korea 5,621 — exact.
- The piece must NOT claim the model proves cases were missed — it shows residuals; the framing should be "the model implies" / "the residual suggests".
- Caveats from analyst.json (proxy nature of tour groups, OECD-only fit, reported-numbers limit) should be woven into the body, not footnoted.
- Reference media (ref_wuhan_road.jpg, ref_wuhan_community.jpg) are atmospheric — Designer should use selectively.
