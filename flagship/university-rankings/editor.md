# Working title (Copywriter finalizes)
**Who Is the Best University in the World? Pick a Number.**

**Standfirst / dek** (primes the question, does not spoil the reveal):
Four of the world's biggest university rankings can't agree on who is #1 — and a neutral, survey-free referee crowns yet another school none of them do. So who is really best? It turns out that depends entirely on what you decide to count. Move the dial yourself and find out.

---

## Story Spine

**Core claim**: "Best university" is a weighting choice, not a fact — four global rankings disagree, and even the neutral OpenAlex research-output referee crowns a different order, so no table is simply right; each measures a different definition of "best".

**Tension**: Readers treat a #1 ranking as objective truth. In reality the four systems correlate only 0.60–0.85, crown four different champions (Caltech / Harvard / MIT / Michigan), and swing the same school tens of places (Peking is 12th in QS but 101st in ARWU).

**Payoff**: The reader manufactures Oxford, MIT, or Michigan as world #1 from the SAME data just by moving the weights — then discovers that even the "objective" referee doesn't vindicate any single table.

**Interactive centerpiece**: `ana_12` — the reweighter — built as the hero explorable (`concept_ref: img_01`, `explorable_recompute`) in `edt_06`. The reader produces the "who's #1?" answer themselves; the hero renders and is used *before* the prose names Oxford/MIT/Michigan.

---

## Sections

### edt_01: Hook — Four tables, four champions
**Evidence**: ana_06, ana_05b | **Context**: det_08, det_09, sct_bgm

[ana_06, det_08] Ask four of the world's biggest university rankings who is #1 and you get four different answers. Times Higher Education's 2015 table crowns Caltech; Shanghai's ARWU and the CWUR both crown Harvard; QS's 2023 edition crowns MIT. Four tables, four champions — and that is before a neutral referee has even weighed in.

[ana_06] Only five universities — Harvard, Stanford, MIT, Cambridge and Oxford — appear in all four commercial top-tens. The other ten seats, out of fifteen names that reach any top-ten, shuffle from list to list. The tables cannot agree on the ten best, let alone the one.

[ana_05b, det_13] And the disagreement is not confined to the podium. Peking University sits 12th in QS but 101st in ARWU — an 89-place swing for a single school, in the same year of data, turning only on what each table chooses to count.

[det_09] This is not an academic parlour game. In QS's own survey, 23.5% of prospective students said a university's ranking was the single most important factor in where they applied, and 19.6% said it shaped which country they studied in. A weighting choice made by three or four private companies moves students, tuition and national policy.

[editorial] So who is actually best? Before you scroll on, guess who each table puts at #1.

[CHART: ana_06]
[MEDIA: interactive]
[MEDIA: audio]

### edt_02: How far apart are they?
**Evidence**: ana_04, ana_05 | **Context**: det_08

[ana_04, det_08] Across the 218 universities all four systems rank, their pairwise agreement runs from a Spearman correlation of just 0.599 to 0.853 — correlated, but far from agreeing, exactly the 0.7–0.8 band the academic literature reports. The two research-only tables, ARWU and CWUR, agree most (0.853); survey-driven QS and research-only CWUR agree least (0.599).

[ana_05] Agreement is tight only at the very summit. Stanford varies by just two places across the four tables, Cambridge and Chicago by three, MIT by five. Drop below the top handful and the gaps explode: the median university swings 122 places between its best and worst ranking, and the average swing is 158.

[ana_04] QS is the systematic outlier. Its three weakest correlations — with CWUR (0.599), ARWU (0.647) and THE (0.735) — are the three lowest of all six pairs. The table that leans hardest on reputation surveys is the one that agrees least with everyone else.

[CHART: ana_04]

### edt_03: The swingers — same school, tens of places apart
**Evidence**: ana_05b | **Context**: det_13

[ana_05b, det_13] Restrict the comparison to the 92 schools every table ranks inside its top 200 — so no tail-band padding inflates the gaps — and the biggest movers are household names. Fudan swings 161 places (193rd in THE, 34th in QS); the Australian National University and the University of Hong Kong swing 149 apiece.

[ana_05b] Peking and Tsinghua are the cleanest illustrations. QS ranks Peking 12th and Tsinghua 14th; ARWU — which counts Nobel prizes and highly-cited papers, not reputation — ranks both 101st, roughly 90 places lower. The universities did not change between the two tables; the definition of "best" did.

[ana_05b, det_13] The swing runs both ways. Berkeley is 4th in ARWU's research order but 27th in QS. Caltech tops THE at #1 yet ranks only 82nd by OpenAlex's raw output count — tiny, but citation-dense. Each is the same institution seen through a different lens.

[editorial] Pick a famous school and guess how far apart the tables place it, before you see the real spread.

[CHART: ana_05b]
[MEDIA: image]
[MEDIA: interactive]

### edt_04: Why they disagree — the weighting dial
**Evidence**: ana_02 | **Context**: det_02, det_03, det_04, det_05, det_06, det_07

[ana_02, det_02, det_07] The tables disagree because they measure different things, and the split is mechanical. Reputation surveys — academics and employers polled on who they rate — make up 50% of a QS score (40% academic, 10% employer). They are about a third of a THE score. In ARWU and CWUR they are zero.

[ana_02, det_03, det_04, det_05] The rest is measured output, weighted differently again. THE puts 30% on field-normalised citations, which is why citation-dense Caltech can top it; ARWU rides on Nobel and Fields laureates and Nature/Science papers; CWUR uses no surveys and no university-submitted data at all. Along a perception-to-output axis, the four tables fan out from QS through THE to ARWU and CWUR.

[ana_02, det_06] Beyond all four sits OpenAlex, an open index of more than 200 million research works with zero reputation weighting — pure output. It is the neutral yardstick this story keeps returning to.

[editorial] How much of a QS ranking do you think is just surveyed opinion? Guess, then see the breakdown.

[CHART: ana_02]
[MEDIA: interactive]

### edt_05: The survey and the microscope disagree
**Evidence**: ana_09 | **Context**: det_02, det_04, det_13

[ana_09, det_02] Inside QS itself, the reputation-survey score and the citations-per-faculty score barely track each other — they correlate just 0.421 across the 218 schools. The crowd's opinion and the citation count disagree about who is good.

[ana_09, det_04] That gap has a geography. Against ARWU's research order, QS's survey lifts reputation-rich Asia-Pacific names far up the table — Hong Kong from 151st to 21st, NUS from 101st to 11th, Peking from 101st to 12th. Run it the other way and research-heavy US schools rise instead: Vanderbilt is 53rd in ARWU but 199th in QS, Maryland 43rd against 164th.

[ana_09, det_13] Neither order is wrong. One rewards being widely admired; the other rewards measured research. They are simply answering different questions and calling both answers "rank".

[CHART: ana_09]

### edt_06: So you decide — set the weights yourself
**Evidence**: ana_12 | **Context**: det_02, det_03, det_07, det_13

[editorial] If "best" is really a weighting choice, then the honest thing is to hand you the dial. Every one of the 218 universities below carries five real 0–100 scores — reputation, citations, teaching, international outlook and raw output. Move the weights and the whole table re-ranks live, on the same audited model that produced the numbers in this article.

[ana_12] The presets alone crown three different schools. Weight everything equally and Oxford finishes first (87.02). Weight it like QS, heavy on reputation, and MIT wins (96.25). Weight it like ARWU, on output, and Michigan takes the top (100.0). Same 218 universities, same underlying data, three different world #1s — produced by nothing but where you set the sliders.

[ana_12, det_13] No table is lying. Each published ranking is just a slider position someone else chose for you. The number-one university is not a fact waiting to be discovered; it is an answer you get to configure.

[CHART: ana_12]
[MEDIA: interactive]

### edt_07: The neutral referee doesn't settle it either
**Evidence**: ana_08, ana_07 | **Context**: det_06

[ana_08, det_06] You might expect a neutral, survey-free referee to end the argument. OpenAlex does the opposite. Rank its institutions by raw output and Michigan wins; by total citations, Harvard; by h-index, the University of Washington. Three neutral lenses, three more different #1s — none of them matching Caltech, Harvard or MIT.

[ana_08] Michigan is the emblem. It is first in the world by research volume, yet its best finish in any commercial table is 17th. The neutral referee crowns a school no ranking company will.

[ana_07] And no commercial table is simply "measuring output" either. Correlated against OpenAlex, the research-only ARWU tracks it most closely (0.876 against h-index) and survey-heavy QS least (0.636) — but even the tightest fit, 0.88, is far from a perfect 1.0. The referee vindicates no single table; it just adds more orderings to the pile.

[CHART: ana_07]
[MEDIA: image]
[MEDIA: interactive]

### edt_08: The size trap — papers or impact?
**Evidence**: ana_10 | **Context**: det_13

[ana_10, det_13] Even inside that one neutral database, a single further choice flips everything: do you count papers, or impact per paper? Michigan is #1 in the world by raw volume — some 980,000 works — but divide citations by papers and it falls to 332nd. A 331-place drop from one normalisation decision.

[ana_10] The small, dense schools do the reverse. Caltech is 82nd by volume but 13th per paper; Princeton 104th and 24th; MIT 35th and 3rd. Harvard is the rare giant that is both big and dense — 2nd by volume and 1st per paper — which is why it keeps surfacing near the top whatever you measure.

[editorial] Guess where the world's #1-by-volume university lands once you switch to impact per paper.

[CHART: ana_10]
[MEDIA: interactive]

### edt_09: Why believe this — the disagreement survives holding the year fixed
**Evidence**: ana_11 | **Context**: det_14

[ana_11, det_14] One honest objection has to be dealt with: the tables are not all from the same year. THE, ARWU and CWUR here are 2015 editions, while QS is 2023 and OpenAlex was fetched in 2026, attached as recent-state overlays rather than same-year snapshots. Could the disagreement just be a time gap dressed up as a methodology gap?

[ana_11] No. Hold the year fixed — compare only the three 2015 tables, on the 285 schools they share — and they still agree only at a mean Spearman of 0.782, nowhere near 1.0. The disagreement is real within a single year; it is about method, not the calendar.

[ana_11] What this does not settle is the exact size of QS's gap. Because QS is eight years newer than the 2015 trio, its lower average agreement of 0.660 mixes a genuine methodology difference with an eight-year drift — so read that figure as an upper bound on how far QS's method alone diverges, not a clean measurement of it.

[CHART: ana_11]

### edt_10: Look up your own university
**Evidence**: ana_13 | **Context**: det_09

[ana_13] All of this is easier to feel with a school you actually care about. Each of the 218 common-core universities carries its own five verdicts — its rank in THE, ARWU, CWUR and QS, plus OpenAlex — and its own cross-system spread.

[ana_13] Berkeley swings 23 places between the tables, Caltech 11, Michigan just 8, Peking a full 89. Look yours up and see how far the rankings move it.

[MEDIA: interactive]

### edt_11: What "best" actually means
**Evidence**: ana_12 | **Context**: det_10, det_11, det_12, det_09

[det_10, det_11] A single ranking is only a snapshot of one methodology, and even that is unstable. When QS overhauled its formula in 2024 — cutting the academic-reputation weight from 40% to 30% — universities moved dozens of places without changing at all. When Columbia was found to have submitted false data to another ranking, it fell from 2nd to 18th overnight.

[det_12] The ranked elite increasingly agree. In 2023, led by Yale and Harvard, dozens of top US law and medical schools boycotted the rankings that flatter them, arguing that a single weighted score measures the wrong things.

[ana_12, det_09] The lesson is not that rankings are worthless — it is that "best" is a question you have to finish yourself. Every table has already answered it for you, quietly, by choosing what to count. Now that you have watched the champion change under your own hand, the only honest #1 is the one whose weighting you would be willing to defend.

### edt_12: About the data
**Evidence**: ana_01, ana_03 | **Context**: det_01, det_14

[ana_01, det_01] The story aligns four commercial ranking systems — THE (2011–2016), ARWU (2005–2015), CWUR (2012–2015) and QS (2023) — against OpenAlex, an open research-output index fetched on 24 June 2026. The cleanest cross-system edition year is 2015; QS and OpenAlex attach as recent-state overlays.

[ana_03] The five tables are matched by a normalised institution name into a common core of 218 universities. That is slightly larger than the dataset's own stated ~189 because the matcher recovers more true name variants (Michigan–Ann Arbor, ETH Zurich, UCL); the exact figure is matcher-dependent, so treat ~200 as the scale, not a precise constant.

[editorial] Every number in this article is recomputed from the raw files by the code behind it, and can be re-run in the verify layer.

## Editorial Notes

- **Load-bearing spine**: edt_06 is the centerpiece. The hero reweighter (`img_01`/`ana_12`) must render and be usable *before* the paragraph that names Oxford (87.02) / MIT (96.25) / Michigan (100.0) — the reader should be able to produce a champion themselves before the prose states one. The explorable recomputes on the Analyst's audited `client_model` (`reweightRankings`), so the widget's live #1 and the prose figures are two readouts of one model.
- **Standfirst must not pre-spoil**: the dek sets up "who's really #1? — you can decide" and may name the four *published* champions (that is the edt_01 hook, ana_06), but must NOT state that the reweighter yields Oxford/MIT/Michigan. Keep that trio for edt_06.
- **Era-mismatch is mandatory visible prose** (edt_09, tagged `[ana_11, det_14]`): one clear sentence that the clean cross-system year is 2015 while QS is 2023 and OpenAlex is current overlays. Do not cut it to a stray clause.
- **Validation gets its own beat** (edt_09): the 2015-trio mean Spearman 0.782 is the "why believe this" passage; state honestly that QS's 0.660 is an UPPER bound conflated with the ~8-year span — never sell a QS-vs-2015 gap as pure methodology.
- **Exact numbers, do not round**: four champions Caltech / Harvard / Harvard / MIT / Michigan; correlations 0.599–0.853; median spread 122 (122.5); Peking 12 vs 101 (89); QS reputation 50% vs ARWU/CWUR 0%; QS internal AR-vs-CPF 0.421; ARWU-vs-OpenAlex 0.876 / QS 0.636; Michigan works #1 → per-paper impact #332 (+331); preset #1s Oxford 87.02 / MIT 96.25 / Michigan 100.0; 2015 trio 0.782, QS 0.660; Columbia 2 → 18; QS reputation 40% → 30%; 23.5% / 19.6%.
- **QS legacy weights caveat** (edt_04): the QS 2023 edition uses the pre-2024 legacy formula (Academic Reputation 40%); its reputation-heaviness is specific to this edition.
- **Band-free swingers only** (edt_03): use the ana_05b set (schools ranked ≤200 by all four systems). Do not use the raw "biggest swingers" (George Mason 850, etc.) in the story — those are tail-band artefacts.
- **ana_01b is not reader-facing** (cut): the data-quality quirks (band collapsing, tied ranks, the Washington two_yr_mean_citedness anomaly, CWUR rank-direction) belong to the verify/methods layer, not body prose.
- **Media**: BGM `sct_bgm` (John Field nocturne) is the mandatory top-of-article now-playing card in edt_01. Campus imagery feeds the cinematic scroll and the context sections — edt_03 uses Peking (det_media_08), Tsinghua (det_media_07), Berkeley (det_media_09), Caltech (det_media_06); edt_07 uses Michigan (det_media_10), Toronto (sct_toronto), UCL (sct_ucl), Washington (sct_washington). Additional verified covers available: Princeton (sct_princeton), ETH Zurich (sct_eth, ultra-wide), Tokyo (sct_tokyo), Harvard/Oxford/Cambridge crests (det_media_01/02/03), Stanford (det_media_05).
