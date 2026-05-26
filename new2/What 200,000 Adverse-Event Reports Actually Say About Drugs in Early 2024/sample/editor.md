# What 200,000 Adverse-Event Reports Actually Say About Drugs in Early 2024

## Story Spine
**Core claim**: FAERS is less a record of what drugs do to people than a record of which drugs the world is paying attention to — and in early 2024 the world was paying very specific attention to one thing.

**Tension**: The press narrative says Ozempic is at the center of a drug-safety storm. The data says Mounjaro is, and that the loudest complaint in the entire dataset is not a side effect — it's that the drug was used the wrong way.

**Payoff**: Reading FAERS as a scoreboard of medical danger gets the story wrong twice over: once because the database is a megaphone for reporting behaviour rather than a meter of real-world risk, and once because the actual signal in the 2024 slice — Mounjaro's pen-handling complaints, Dupixent's biologic injection issues, a thick layer of "drug didn't work" filings — is much weirder than the headlines suggest.

## Sections

### edt_01: The top complaint isn't medical

**Evidence**: ana_12, ana_15 | **Context**: det_03, det_04

[ana_12] Among 597,802 adverse-reaction rows in FAERS for the first seven weeks of 2024, the single most-reported MedDRA Preferred Term is not nausea, not pain, not death. It is "Off label use" — 14,801 mentions, 2.48% of all reaction rows. The next two terms are "Drug ineffective" (11,335) and "Death" itself logged as a reaction (9,356). The first recognisably medical symptom — "Fatigue" — appears in fourth place.

[ana_15] Fully 1.8% of every single report in the dataset is one person filing one complaint: that the drug did not work. No symptom, no event, no outcome — just "Drug ineffective" and nothing else. That is 3,554 reports out of 200,000, and another 7,683 reports that mention "Drug ineffective" alongside something else.

[det_03, det_04] FAERS is fed by anyone who notices a problem — patients writing in to MedWatch, hospital safety officers, drug manufacturers fulfilling mandatory reporting, clinical-trial sites. Many of those reports are not medical at all. They describe how the drug was used, whether it worked, whether the right dose came out of the pen. The database's loudest signal is paperwork, not pharmacology.

[CHART: ana_12]
[MEDIA: interactive]

### edt_02: What FAERS is, and what its biggest numbers actually mean

**Evidence**: ana_18, ana_03, ana_04 | **Context**: det_01, det_02, det_04, det_08

[det_01, det_02] FAERS is the FDA's central post-market surveillance database. Anyone with a story about a drug — a patient who developed a rash, a clinician who saw an unexpected outcome, a manufacturer required by law to forward a complaint — can submit a report. Every report names a patient (age, sex, country), one or more drugs (each marked as Suspect, Concomitant, or Interacting), and one or more reactions described in MedDRA, the standardized vocabulary used by drug regulators worldwide. The full 2024 universe is roughly 1.32 million reports.

[det_08, ana_03] The slice in front of us is 200,000 reports drawn chronologically through the OpenFDA API — Jan 1 through Feb 23 only, the first 54 days of 2024. About 15% of the year's volume sits in this snapshot. The patient fields are sparser than you would hope: age is missing 40% of the time, sex 16%, country of occurrence 11%. The seriousness flag is almost always present.

[ana_18, ana_04] Half the reports — 52.5% — are tagged "serious", an extraordinarily high rate by epidemiological standards. Nine percent record a death. A fifth involve a hospitalization. None of this means the drugs are killing or hospitalising people at those rates. It means the events that get reported to FAERS skew strongly toward the events worth reporting: hospital workups, life-threatening reactions, adverse outcomes severe enough that someone wrote them down.

[det_04] FAERS has no denominator. The database does not know how many patients took each drug. A report count cannot be divided by a prescription count, and the FDA itself states that the system is for "generating hypotheses about potential safety signals," not for measuring rates.

[CHART: ana_18]

### edt_03: Dupixent and Mounjaro are tied for #1

**Evidence**: ana_06, ana_07, ana_08 | **Context**: det_05

[ana_06] Across all 776,793 drug appearances in the dataset, Dupixent — dupilumab, an injectable biologic for atopic dermatitis and asthma — is the most-reported product, with 15,027 mentions and 1.93% of every drug row. Mounjaro (tirzepatide, the type-2-diabetes blockbuster from Eli Lilly) is the closest possible second at 14,908 mentions and 1.92%. The two are separated by 119 rows out of three-quarters of a million.

[ana_07] When the analysis is narrowed to drugs marked as the suspect product — the drug the reporter thinks caused the event — Dupixent still edges out Mounjaro, 14,916 to 14,742. Together they make up just under 6% of all suspect-drug rows in the dataset. The remaining top of the list is recognisable to anyone who works in pharmacovigilance: Xolair, Repatha, Cabometyx, methotrexate, Rituximab, Humira — the immunology and oncology biologics that have anchored FAERS for years.

[ana_08] Behind that ranking is a sharper diagnostic. Some drugs are almost always the suspect when they appear: Dupixent 99.3% suspect, Mounjaro 98.9%, Xolair 99.1%, Cabometyx 99.8%. Others are almost never the suspect — aspirin is the suspect in only 15.8% of its appearances, atorvastatin in 21.7%, acetaminophen in 49.0%. Those drugs show up because the patient was taking them at the time, not because they are blamed for anything. A drug's headline count is half story, half background noise; the role mix tells you which.

[CHART: ana_06]

### edt_04: The GLP-1 surge is real, but the spotlight is on the wrong drug

**Evidence**: ana_09, ana_32 | **Context**: det_05

[det_05, ana_09] The press story of 2024 has been Ozempic — semaglutide, the GLP-1 receptor agonist that became a household word for weight loss. In the FAERS sample, however, Ozempic ranks 21st by total mentions. The dominant GLP-1 drug is Mounjaro at 14,908 rows, with 3,077 more for its sibling Zepbound (tirzepatide approved for obesity in November 2023). Pooled across brands, tirzepatide produces 18,035 drug rows; semaglutide (Ozempic + Wegovy + Rybelsus) produces 5,425. The newer drug outruns the famous one by a factor of 3.3.

[ana_32] The eight major GLP-1 brand names produce a head-to-head table that looks nothing like a single drug class. Mounjaro: 3,159 suspect-reports, 11% tagged serious, 0.7% involving a death. Ozempic: 2,493 suspect-reports, 32% serious, 0.6% death. Zepbound: 718 suspect-reports, 2.5% serious, zero deaths. Wegovy and Saxenda — both indicated for weight loss — show the strongest female skew (82% and 88% female of sex-known reports). The diabetes-indicated brands skew older (median age 63 for Ozempic, Rybelsus, Trulicity); the obesity-indicated brands skew younger (47 for Wegovy, 49 for Zepbound, 45.5 for Saxenda).

[editorial] Two drugs that share an active ingredient — Mounjaro and Zepbound, both tirzepatide — generate the gentlest seriousness profiles in the dataset. The same active ingredient, marketed for diabetes by physicians (Mounjaro) versus marketed for weight loss directly to consumers (Zepbound), produces reports that look mild by FAERS standards. It is almost certainly a reporter-community effect: weight-loss patients filing reports through manufacturer pharmacovigilance hotlines, mostly about misfiring pens, not hospitalisations.

[CHART: ana_32]

### edt_05: Mounjaro's complaints are about the pen; Ozempic's are about the body

**Evidence**: ana_33, ana_34 | **Context**: det_05

[ana_33] The top reactions for Mounjaro and Ozempic look almost like reports from different drugs. Mounjaro's top complaint is "Incorrect dose administered" — 21.7% of all Mounjaro reports — followed by "Injection site pain" (14.5%), "Off label use" (12.5%), and only then "Nausea" (9.9%). Zepbound's top complaints are even more device-focused: "Incorrect dose administered" 21.4%, "Accidental underdose" 16.4%, "Injection site pain" 13.6%. Ozempic looks like a different drug. Its top reactions are "Nausea" (16.2%), "Vomiting" (9.3%), "Diarrhoea" (9.2%), "Constipation" (7.6%), "Decreased appetite" (6.8%). The body is the complaint, not the syringe.

[ana_34] Stepping back across all 10,056 GLP-1 reports, the reactions most over-represented in the class versus the dataset average tell the underlying story. "Impaired gastric emptying" appears 14.8 times more often in GLP-1 reports than would be expected from base rates. "Pancreatitis" — a long-recognised GLP-1 risk — appears 8.4 times more often. "Glycosylated haemoglobin increased" appears 9.7 times more often, meaning some patients are complaining the drug failed to bring their HbA1c down. And then, in the same ranked list: "Weight loss poor" (18.5x lift) and "Increased appetite" (11.1x). The paradox of the class shows up directly — both the patients whose appetite vanishes and the patients whose appetite returns are writing in.

[CHART: ana_34]

### edt_06: The actual death-rate hotspots are nowhere near the headlines

**Evidence**: ana_20, ana_16 | **Context**: det_04

[ana_20] Filtering to drugs with at least 200 suspect-reports and ranking by share of reports involving a death produces a list that has almost nothing to do with weight-loss drugs. The top entries: methamphetamine (93.5% of its suspect-reports involve a death), alcohol (89.4%), fentanyl (71.9%), diphenhydramine (70.9%), trazodone (69.1%), cocaine (66.1%), oxycodone (57.9%). These are not signals that prescribed drugs are killing patients. They are reports filed after toxicology found the substance present at the time of death — overdose cases, polypharmacy mortality, drug-related fatalities being routed into FAERS because a drug was named in the chart. Notably absent from the top thirty: any GLP-1 drug.

[ana_16, det_04] Among the 39,213 reactions explicitly tagged with a Fatal outcome, the most common identifiable cause of death is "Completed suicide" (1,602 rows, 4.1% of fatal reactions). It is followed by "Toxicity to various agents" (2.7%), "Drug abuse" (2.2%), cardio-respiratory arrest, pneumonia, cardiac arrest, sepsis. FAERS death numbers are real, but they are death-from-anything-while-on-a-drug numbers — they are not a leaderboard of drugs that kill.

[CHART: ana_20]

### edt_07: Who files, when, and from where

**Evidence**: ana_22, ana_25, ana_28, ana_29, ana_30 | **Context**: det_06

[ana_22] FAERS reports skew strongly female. Of reports with a known patient sex, 59.5% are about women and 40.5% are about men — a 1.47:1 ratio. The skew shows up in every drug analysed individually: Wegovy 82% female, Dupixent's autoimmune-leaning population female-dominated, even Mounjaro 74% female despite the underlying diabetic population being roughly balanced.

[ana_25, det_06] Where the events happen is, overwhelmingly, the United States. 60.3% of reports describe an event that occurred in the US; the next closest is Canada at 5.1%, then the UK at 3.5%, Japan at 3.3%, France at 3.3%. The 99.9% match between event country and reporter country shows that FAERS is fed locally — clinicians and patients in each country file about events in their own country, and manufacturers forward those reports through their pharmacovigilance teams. The US dominance is not because Americans get more adverse events; it is because Americans are far more likely to file a report when they have one.

[ana_28] Eighty-one percent of reports come in through spontaneous channels — the canonical patient/clinician/manufacturer-forwarded route. Sixteen percent come from clinical studies, three percent from "Other" channels (literature, surveys). The Study channel is small but disproportionately serious: oncology-trial safety reports come through it.

[ana_29, ana_30] The data has a heartbeat. Across the 54-day window, weekdays receive an average of 35,000–40,000 reports while weekends crater to 5,500 (Saturday) and 8,200 (Sunday). On every Saturday and Sunday the count drops 80–90% from the surrounding Friday. Adverse events do not stop happening on weekends. The reporting infrastructure does. FAERS is not a real-time monitor; it is a five-day-a-week intake queue.

[CHART: ana_29]
[MEDIA: map]

### edt_08: How to read the next FAERS headline

**Evidence**: ana_18, ana_29 | **Context**: det_04, det_07

[editorial] The two findings that survive every caveat are these. First: the top "adverse reaction" in the database is not a medical event, it is "Off label use" — and the second is "Drug ineffective". Second: the GLP-1 brand at the centre of the next round of headlines is much more likely to be Mounjaro than Ozempic, because Mounjaro is generating three times more reports already, and most of those reports are about pen handling, not pharmacology.

[det_04, ana_18] Every number in this blog is a count of reports, not a count of events. FAERS is a megaphone, not a measurement. A drug that has been in the news collects more reports for the same underlying rate. A drug whose patients are old, female, and U.S.-based collects more reports per prescription than one whose patients are not. A drug whose pen is hard to use collects more "Incorrect dose administered" reports than one whose pen is not.

[det_07, editorial] The FDA itself reads FAERS this way. Each quarter the agency publishes a list of "Potential Signals of Serious Risks/New Safety Information" identified from these reports — sometimes only dozens of cases — that warrant closer investigation. The signals trigger label changes, dose warnings, drug-safety communications. Nothing in FAERS is causation, but everything in FAERS is a question worth asking.

[editorial] Read the next news cycle about an "adverse event database surge" with the structure in mind. A spike in reports means someone is filing them — a regulator put out a warning, a class-action lawyer ran an ad, a TV doctor mentioned the drug. The events behind the reports may or may not have changed. The reporting always has.

## Editorial Notes
- Exact numbers required: 14,801 (Off label use), 11,335 (Drug ineffective), 200,000 (sample), 15,027 vs 14,908 (Dupixent vs Mounjaro), 18,035 vs 5,425 (tirzepatide vs semaglutide), 11.02% vs 32.01% (Mounjaro vs Ozempic serious), 3,554 (Drug-ineffective-only reports), 60.3% (US event share)
- Time-window caveat (Jan 1 – Feb 23) must appear in edt_02
- No-denominator caveat must appear in edt_02 and again in edt_08
- Never imply causation. Every comparison is about reports, not events.
- The Mounjaro/Ozempic comparison is THE story; do not bury it under demographics.
- Editorial position: FAERS as a megaphone (a reporting behaviour signal), not a measurement (a medical risk signal). This frame should be present in edt_01, edt_02, edt_06, and edt_08.
