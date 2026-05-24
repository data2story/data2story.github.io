## Story Spine
**Core claim**: Across 49 years and seven orders of magnitude, real chips have followed Gordon Moore's 1975 prediction to within 0.03 of a year — a forecast accuracy almost no other quantitative claim in technology can match.
**Tension**: Moore's Law is dismissed by half the industry as folklore, marketing, or "self-fulfilling prophecy" — yet the dataset shows the slope was empirically right within 1.5%, while inside the same record real warning signs (post-2005 deceleration, GPU/CPU lead trading) sit hidden in plain sight.
**Payoff**: The reader leaves with a working mental picture of which line on the chart is real, which line is the prediction, where Moore was off (1965), where he was nearly perfect (1975), and what *did* slow down even as the transistor count kept climbing.

## Sections

### edt_01: Hook — The forecast that aged
**Evidence**: ana_01, ana_03 | **Context**: det_01, det_02

[ana_01] Empirical CPU doubling time across the dataset is 2.03 years. Moore's 1975 revised prediction was 2.00 years. Forty-eight years, seven orders of magnitude, 170 chips — and the slope deviates by 0.03.

[ana_03] In numbers: the Intel 4004 in 1971 carried 2,250 transistors. The AMD EPYC Rome in 2019 carried 32 billion. A 14.2-million-fold climb, on a curve so steady that a pencil line drawn in 1975 still threads through the points half a century later.

[det_01, editorial] None of this was law in the physical-constants sense. Gordon Moore wrote a four-page article for *Electronics* magazine in April 1965 and drew a straight line through five data points. He projected that "by 1975 economics may dictate squeezing as many as 65,000 components on a single silicon chip." The piece had no formal model. The exponent has held anyway.

[CHART: ana_17]
[MEDIA: image]

### edt_02: The man and the curve
**Evidence**: ana_15 | **Context**: det_01, det_03

[det_01] When the article was published Moore was Director of R&D at Fairchild Semiconductor; he hadn't yet co-founded Intel. The phrase "Moore's Law" wasn't coined for another five years. In 1975, after a decade of new data, he revised the doubling rate from 12 months to 24 — the version that has stuck.

[det_03, ana_15] The first chip on the curve, six years after the prediction, was the Intel 4004: 2,300 transistors at a 10-micron process node, designed by Federico Faggin's team for Busicom's printing calculator. It is the anchor point of the entire CPU dataset — the leftmost dot on every Moore's-Law plot ever published.

[MEDIA: image]

### edt_03: Three families, three slopes
**Evidence**: ana_02, ana_04 | **Context**: det_06

[ana_02] Plot all 326 chips on one chart and three roughly parallel lines emerge — but they are not the same line. CPUs double every 2.03 years, GPUs every 1.85 years, RAM every 1.56 years.

[ana_02, det_06] The differences are mechanical, not magical. RAM is mostly bit cells; doubling capacity directly doubles transistors, so RAM tracks lithography almost one-to-one. CPUs spend their transistor budget on logic complexity, which has historically scaled at exactly the rate Moore drew. GPUs sit in between — until the late 2000s, when parallel arithmetic became the default tool for both graphics and machine learning, and GPU counts started catching CPUs.

[ana_04] By 2017-2018 the families converge: a 21-billion-transistor GPU (Volta), a 23-billion-transistor CPU (GraphCore), and a 137-billion-transistor RAM module are all sitting in roughly the same band on the chart. Before the late 2010s no such band existed.

[CHART: ana_04]
[MEDIA: interactive]

### edt_04: Where Moore was wrong
**Evidence**: ana_09 | **Context**: det_01

[ana_09] The 1965 paper aimed at 65,000 components by 1975. The CPUs that actually shipped in 1975 topped out at 5,000 transistors. The 1976 maximum was 8,500. Moore overshot by a clean order of magnitude — exactly the kind of error any forecaster makes when extrapolating a young exponential.

[det_01, ana_09] In 1975 he halved the doubling rate from 12 months to 24, and the revised line aged into a law. The version most people know — Moore's Law as a steady two-year doubling — is not what the original article said. It is what Moore said *after* checking against a decade of evidence.

[CHART: ana_09]

### edt_05: Where it slowed without anyone noticing
**Evidence**: ana_06 | **Context**: det_04

[ana_06] Split the CPU record at 2005 — the year Dennard scaling collapsed and clock speeds plateaued — and the doubling time stretches: 2.02 years before, 2.51 years after. CAGR drops from 40.9% to 31.8%. GPUs show the same break, even more sharply: 1.62-year doubling before 2005, 2.53 years afterward.

[det_04, ana_06] This slowdown is the consumer reality that almost no Moore's-Law graph shows. After ~2005, transistors kept doubling, but they stopped translating into proportionally faster single-threaded performance. Clock speeds froze around 3-4 GHz. The new transistor budget went into multi-core, GPUs, and AI accelerators — parallelism instead of frequency. The "exponential is still going" story is true; the "your laptop will be twice as fast every two years" story is not.

[CHART: ana_06]

### edt_06: Crossings, jumps, and the chips that beat the line
**Evidence**: ana_10, ana_11, ana_12 | **Context**: det_03

[ana_10] The dataset crosses each power-of-ten transistor milestone roughly every seven years. Past 1,000: Intel 4004, 1971. Past 10,000: Intel 8086, 1978. Past 1 million: Intel i860, 1989. Past 1 billion: dual-core Itanium 2, 2006. Past 10 billion: 32-core SPARC M7, 2015. Seven 10x crossings in 44 years — exactly the rhythm a 2-year doubling produces.

[ana_11] The crossings are not smooth. The single biggest year-over-year jump in the running CPU max came in 1982, when the Intel 80286 leapt 11.65x past the previous high of 11,500 transistors. The Motorola 68020 in 1984 jumped 8.64x. Dual-core Itanium 2 in 2006 jumped 6.80x. The exponential advances in shoves, not glides, and a few well-placed chips do most of the work.

[ana_12] Residuals to the per-family fit reveal two families of outlier. Above the line: Intel's Itanium 2 series (the dual-core Itanium 2 sits +0.95 log-units above its year's predicted count, the largest residual in the CPU record), and SPARC64. Below the line: ARM 9TDMI, ARM 1, ARM 2, ARM Cortex-A9, Atom — chips designed to trade transistor count for power efficiency. The same line that traces the law also separates two design philosophies: maximalist server logic on one side, low-power embedded chips on the other.

[CHART: ana_12]

### edt_07: The Moore line on the data
**Evidence**: ana_16, ana_17 | **Context**: det_01, det_02

[ana_16, ana_17] Drawing Moore's 2-year line through the Intel 4004 at 1971 and projecting it to 2019 gives a predicted 38.6 billion transistors. The actual maximum CPU in 2019 was 32 billion. Moore's prediction overshoots by 21% — within the dataset's own stated 10-20% accuracy band.

[ana_17, editorial] On a single log-scale chart of all 326 named chips, the Moore line passes through the cloud almost like a regression. Forty-eight years apart, the prediction line and the empirical chips meet at the same place — to within one order of magnitude — every year. There is essentially no other public, multi-decade forecast in technology that has held this well. That is the headline finding.

[CHART: ana_16]
[MEDIA: video]

### edt_08: After the dataset
**Evidence**: ana_13 | **Context**: det_05, det_07

[det_05] The International Technology Roadmap for Semiconductors — the global document that effectively codified Moore's Law — released its final report in 2016 and dissolved. The closing report concluded that traditional 2-D scaling would hit an economic wall by 2021, after which the industry would lean on 3-D stacking, advanced packaging, and specialised accelerators rather than simple lithographic shrink.

[det_07] The dataset cuts off in 2019, so it captures the very first chips of the post-ITRS era — Apple's A12X, Nvidia Turing, AMD EPYC Rome — without yet reaching the trillion-transistor wafer-scale chips that arrived afterward. Apple's M1 Ultra in 2022 fused two M1 Max dies on a single interposer for 114 billion transistors. Cerebras's WSE-3 in 2024 is a single piece of silicon with 4 trillion transistors — more than 100 times the count of any chip in this dataset.

[ana_13] Whether the line continues, bends, or transforms is the open question. Inside the 1971-2019 window, though, the answer is settled: the most famous quantitative prediction in modern technology was, on the data, almost exactly right.

## Editorial Notes
- The 2.03 vs 2.00 number must be exact — that is the whole hook
- The 14.2-million-fold change must be cited from the Intel 4004 → AMD EPYC Rome calculation
- Keep the 2005 deceleration finding visible: do not let the "Moore was right" framing crowd it out
- The 1965 prediction overshoot (65,000 vs 5,000-8,500) is essential — it is what makes the 1975 revision the version that aged
- All numbers come from analyst.json content fields; do not approximate
- Caveats from analyst.json (Wikipedia bias, post-2019 cutoff, marketing-name nodes, RAM cell-count) should be woven into the prose rather than footnoted
