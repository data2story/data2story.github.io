# Editor — Cape Verde: The Eleventh Island

## Story Spine

**Core claim**: Cape Verde took the reigning world champions to the 111th minute because "Cape Verde" is much bigger than Cape Verde — the team, the money and the nation itself are the diaspora made visible.

**Tension**: Readers assume a national team represents the people who live in a country, and that official statistics can at least count a nation of half a million. Both assumptions fail here — 15 of the 26 players were born abroad, and the UN's own emigration matrix is missing the squad's top birth country entirely. The strictest count in the world cannot see the nation that just held Argentina for 110 minutes.

**Payoff**: The reader stops seeing "plucky minnow" and starts seeing a 500-year emigration system — famine-born, remittance-financed, morna-scored, constitutionally engineered — that finally became visible to everyone for four matches in an American summer. The three-layer counting problem (UN floor / national censuses / heritage estimates) is not a data footnote; it IS the story: even the UN can't fully count this nation.

**The interactive centerpiece**: ana_09, realized as the hero playground (Imagineer concept img_03, `explorable_recompute`, section edt_03). The reader strips birth countries out of the 26-man squad and produces the collapse themselves: remove the five foreign birth countries and 15 players, half the caps (50.3%) and 3 of the 4 World Cup goals vanish — the team that qualified stops existing. It runs on the Analyst's shipped client model (`code/client_model.js:squadTally`, cm_02, node-verified). It lands BEFORE the prose states the 15/26 count; the standfirst and edt_01/edt_02 never give the number away.

**Masthead (working — Copywriter owns final strings)**:
- Working title: *The Eleventh Island*
- Working subtitle: *Cape Verde, the World Cup nation whose people mostly live elsewhere*
- Standfirst intent (primes, never spoils): 527,326 people live on the islands; on 3 July the reigning world champions needed 111 minutes and an own goal to get past them. The country that did it is much bigger than the one on the map — and nobody, not even the UN, can fully count it. Do NOT state the 15/26 squad share, the 27.9-per-100 floor, the zero home-based players, or the 5.1x knockout record in the dek — each is a payoff a widget delivers.
- BGM (site-wide now-playing card): sct_01 "Romance Anónimo" (CC0 Musopen recording, solo guitar — the license-clean sibling of morna's longing), cover sct_02, attribution strings as registered by the Scout. The real morna lives on the page as the verified embeds inst_01 ("Sodade") and inst_03 ("Petit pays"). Mood word: longing/pensive, not celebratory — the spine is sodade, even on a football hook.

---

## Sections

### edt_01: Nine Minutes from History (hook)
**Evidence**: ana_19, ana_14 | **Context**: det_01, det_04, det_02, sct_04

[det_01] On the night of 3 July 2026, at Miami Stadium, Cape Verde — population 527,326 — took Argentina to extra time in the Round of 32 of the World Cup. Lionel Messi opened with a touch and finish in the 29th minute, his 20th World Cup goal. Deroy Duarte squeezed an equaliser into the far corner just before the hour. Lisandro Martínez restored Argentina's lead two minutes into extra time — and in the 103rd minute Sidny Lopes Cabral curled in what Sky Sports called "arguably the goal of the tournament."

[det_01] The winner, in the 111th minute, was not an Argentine strike. Cristian Romero's header from a corner went in off Cape Verde defender Diney Borges — an own goal. Behind them, 40-year-old captain Vozinha made eight saves; the match reports that called him 39 missed his June birthday. Argentina 3–2, after extra time, and the biggest upset in World Cup history died nine minutes short.

[ana_19] Before kick-off, the odds model gave Cape Verde a 3.4% chance of winning in 90 minutes and an 8.3% chance of still being level when they ended. The night landed inside the 8.3% branch — the improbable one — and stayed there until the 111th minute.

[det_04, det_01] Here is the detail that unlocks everything else in this story: both Cape Verde goalscorers were born in Rotterdam. Duarte, raised in Sparta Rotterdam's academy, scored his first-ever international goal the night before his 27th birthday; Lopes Cabral came through FC Twente's youth ranks. Every Cape Verdean goal against the world champions was scored by a son of the Dutch port.

[editorial] Which raises the question this whole piece exists to answer: if the goals come from Rotterdam, whose team is this — and how big, really, is the country it plays for?

[MEDIA: video]
[INSTANCE: inst_02]

### edt_02: What Were the Odds? (evidence)
**Evidence**: ana_19, ana_20, ana_14 | **Context**: det_01, det_02

[ana_14, det_02] The Argentina night was only the last improbability in a tournament built of them. Cape Verde entered the World Cup rated 1654 on our Elo scale, drew 0–0 with Spain, came from behind twice to draw 2–2 with Uruguay, drew 0–0 with Saudi Arabia, and left the group stage unbeaten — three draws, three points, second place, and +45 rating points across the tournament. No team beat Cape Verde in 90 minutes all summer.

[ana_19] The model behind these numbers is deliberately simple and fully public: an ordered-logit fit on Elo difference across 30,195 internationals since 1990, with every constant published and the identical computation shipped as plain JavaScript. From Cape Verde's side it rated the group games at 2.8% (Spain), 11.3% (Uruguay) and 33.4% (Saudi Arabia) chances of victory — and the Argentina tie, across a 523-point rating gap, at 3.4% win / 8.3% level after 90 / 88.3% defeat.

[MEDIA: interactive]

[ana_20] Why believe a model like this? Because it was tested where it hurts: trained only on 1990–2014 and scored on 10,681 later matches it had never seen, it beats base-rate guessing by 18.8% on Brier score, and its calibration holds within 2.5 points in every probability decile — teams it gave a 15.1% chance won 13.7% of the time. What would falsify it is a decile table where longshots won far more often than predicted; that table does not exist here.

[ana_19, ana_14] Two honesty notes belong in plain sight. The 8.3% is the chance of being level after 90 minutes — treating extra time as a coin flip puts Cape Verde's chance of advancing at 7.6%, and the coin flip is an assumption, not a measurement. And the ratings are our own implementation, computed from the full 1872–2026 match record with documented constants; they are not comparable with any published Elo board.

[CHART: ana_14]

### edt_03: Whose Team Is This? (turn — the lead)
**Evidence**: ana_09, ana_10 | **Context**: det_16, det_04, det_05, sct_09, sct_05

[det_05] Maria da Cruz of Schiedam watched the Argentina match the way she watches every one: "When they're not playing I can just watch the game, but when my children play I'm chasing every ball." Her sons Laros and Deroy Duarte grew up being driven to academy training across the Netherlands in a Toyota Starlet that clocked 276,000 kilometres. Five Rotterdam-born players started Cape Verde's World Cup opener against Spain.

[det_16, editorial] Read the squad sheet and it stops looking like a team list and starts looking like a map of somewhere else — Rotterdam, Lisbon, Paris, Dublin, Philadelphia. Before the numbers are given away, take the squad apart yourself: switch off the birth countries and watch what remains.

[MEDIA: interactive]

[ana_09] The count the widget reveals: 15 of Cape Verde's 26 World Cup players — 57.7% — were born outside Cape Verde. Six were born in the Netherlands, four in Portugal, three in France, one in Ireland, one in the United States; the imported share peaks in midfield (8 of 12). The squad's birth map is nearly a map of the emigration itself — with the ironic twist that its top birth country, the Netherlands, does not even appear in the UN's emigration table for Cape Verde.

[ana_10] And the diaspora contingent is not squad padding. The 15 abroad-born players carry 414 of the team's 823 career caps (50.3%), and at this World Cup three of Cape Verde's four goals came from players born abroad — Hélio Varela (born in Portugal) against Uruguay, then both Rotterdam goals in Miami. Duarte's equaliser was his first international goal in 34 caps' worth of waiting.

[ana_10, det_16] The counterweight matters too: this is a fusion, not an imported XI. The all-time cap and goal records both belong to island-born Ryan Mendes (96 caps, 22 goals), the captain is island-born Vozinha, and 11 of the 26 were born on the archipelago. The team is not Cape Verde pretending to be Dutch; it is Cape Verde as it actually exists — scattered.

[CHART: ana_10]

### edt_04: The Machine (evidence)
**Evidence**: ana_11 | **Context**: det_06, sct_08

[det_06] None of this happened by accident. Since 2002 the Cape Verdean federation has systematically recruited among the children of emigrants in Portugal, France, the Netherlands and Ireland — in 2019 the then-coach contacted Shamrock Rovers defender Roberto Lopes on LinkedIn to persuade him to play for his father's islands. Under FIFA rules a dual national who hasn't played a competitive senior match elsewhere is eligible, so Cape Verde's scouts work Europe's academies pitching a country many of their targets have never lived in.

[det_06] The man who fused it into a team is home-grown: Bubista — Pedro Leitão Brito, born on Boa Vista, 21 caps as a centre-back — took over in January 2020, reached consecutive Africa Cup of Nations, delivered the first World Cup qualification in the country's history, and was named CAF Coach of the Year 2025. His job description is the story's thesis: make Portugal-based, Netherlands-based and island-based players one dressing room.

[MEDIA: image]

[editorial] Before reading on, answer one question about this squad: how many of the 26 play their club football in Cape Verde?

[ana_11] The answer is zero. The 26 players are employed in 14 different countries — Portugal hosts seven, Turkey three, and the list runs through Bulgaria, the United States, Cyprus, Russia and on — and not one plays in the domestic league. Cape Verde's World Cup team is an export product top to bottom: even the island-born players professionalised abroad.

### edt_05: The Count with Holes in It (evidence)
**Evidence**: ana_01, ana_02 | **Context**: det_07

[ana_01, det_07] Try to count this nation and you hit the wall immediately. The UN's 2024 bilateral migration matrix — the strictest instrument that exists — records 146,396 people born in Cabo Verde living abroad, and that world total is literally the sum of just 24 named destination countries, with no "other" row. Portugal alone hosts 76,835 (52.5%) and France 34,814 (23.8%): three in four counted emigrants live in one of two countries.

[MEDIA: map]

[ana_01, det_07] Now look at what the matrix cannot see. The Netherlands, the United States, Spain and Senegal have no row at all — not because no Cape Verdeans live there, but because those countries' statistics don't break out small origin groups. The birth countries of seven of the fifteen abroad-born squad players are statistically invisible in the very table that is supposed to measure the emigration. Every number on this map is a floor by construction; the previous UN revision, which did include them, counted 12,601 in the Netherlands and 43,729 in the United States.

[ana_02] Even the floor is climbing fast. The counted stock grew 2.83x between 1990 and 2024 while the home population grew 1.4x; France more than quadrupled (x4.55). The strangest line in the table is Luxembourg: 1,148 to 8,211 (x7.15), almost the entire surge inside a single five-year wave — Cape Verdeans are now 1.21% of Luxembourg's population, the highest density of any destination. A 500-year-old migration is still growing new branches.

[CHART: ana_02]

### edt_06: The Nation of 120 Percent (evidence)
**Evidence**: ana_04, ana_05 | **Context**: det_08, det_09, det_10, det_11, sct_05

[editorial] So how big is the real Cape Verde? Start with the strictest layer and guess before you look: for every 100 people living on the islands, how many counted emigrants — born there, now living abroad — exist somewhere else?

[MEDIA: interactive]

[ana_04] The answer is 27.9 — even on the floor count, with its four missing host countries, the equivalent of 28 in every 100 residents lives abroad, double the ratio of 1990 (13.8). That is 146,396 counted emigrants against 524,877 residents, and it is the strictest of three layers, not the diaspora.

[ana_05] Rank that ratio worldwide and the company is telling: Cabo Verde sits #20 of the 212 origins the World Bank population data covers, and #2 in Sub-Saharan Africa behind only Comoros. Nearly everything above it is a war economy (Syria, Venezuela, South Sudan), a Balkan or Caribbean emigration state (Albania, Bosnia, Jamaica, Guyana), or a microstate — and Cape Verde's true position is higher still, because the four biggest missing hosts are exactly the ones its count omits.

[det_10] The second layer is what national censuses see. Statistics Netherlands counts roughly 23,150 people of Cape Verdean background — nearly double the 12,601 born-in-Cape-Verde migrants the UN's 2019 revision recorded there. About 90% live in and around Rotterdam, where the community began with young men signing onto Dutch ships in the 1960s; in the borough of Delfshaven they are almost one resident in eleven. Half a century later, that settlement pattern is scoring World Cup goals.

[det_08] The third layer is heritage, and in the United States it blows the count open. The American Community Survey finds 106,084 self-reported Cape Verdean Americans (142,570 in the 2024 estimates), concentrated in Massachusetts and Rhode Island — but the US State Department puts Americans of Cape Verdean descent at approximately half a million. The gap is itself history: generations arrived on Portuguese documents before Cape Verde existed as a state, and were folded into other identities the census never unfolded.

[det_09] If the layers feel abstract, Brockton, Massachusetts is not. Nearly one in five residents of the city is Cape Verdean — locals call the diaspora the country's "11th island" — and after each World Cup match thousands filled downtown; when celebrations turned violent, with at least nine people injured in shootings, the mayor imposed a temporary curfew ahead of the Argentina game. An American city adjusted its municipal bylaws around the fixtures of a 527,000-person African archipelago.

[det_11] Cape Verde's own state is built around this arithmetic. Emigrants have voted in national elections since 1992; six seats in parliament are reserved for the diaspora — two each for the Americas, Africa and Europe; and Article 40 of the constitution makes citizenship by origin irrevocable, which is precisely what makes the federation's recruitment machine legally frictionless. The government's own diaspora mapping puts the heritage nation at close to 120% of the resident population: more Cape Verde outside Cape Verde than in it.

[CHART: ana_05]

### edt_07: Sodade — Why They Left (turn)
**Evidence**: ana_03 | **Context**: det_12, det_15, sct_06

[det_12] The emigration was never a lifestyle choice; it began as survival. The Sahelian archipelago suffered eleven major famines between 1580 and 1866, and the two worst of the 20th century — 1941–43 and 1947–48, under Portugal's Estado Novo — killed an estimated 45,000 people while the colonial government failed to send food. The island of São Nicolau lost 28% of its people; Fogo lost 31%.

[det_12] The escape routes are the map from the last section, drawn a century early. From the early 1800s New England whaling ships recruited crews in the islands, making New Bedford, Massachusetts the anchor of Cape Verdean America — the packet schooner Ernestina still exists, and carried immigrants between the islands and New England until 1965. And between 1900 and 1970, about 80,000 Cape Verdeans were shipped as contract labourers to the cocoa plantations of São Tomé — deportation dressed as employment.

[det_15] Out of that history the islands composed their national art form. Morna — voice, guitar, cavaquinho, sung in Creole — was inscribed by UNESCO in 2019 as intangible heritage of humanity; its themes, in UNESCO's own words, are love, departure, separation, reunion and longing. Its emotional core is one untranslatable word: sodade. Its global face was Cesária Évora of Mindelo, and her signature song "Sodade" is addressed to an emigrant bound for São Tomé — the contract-labour route itself, set to music.

[MEDIA: audio]
[INSTANCE: inst_01]

[ana_03] The data holds the song's subject like a fading photograph. Of the 25 destinations in the UN table, São Tomé is the one big community dying out: 4,250 people in 1990 — then the third-largest community counted — declining in every single wave to 1,115 in 2024, a fall of 73.8%. No new migration replaces the deportee generation; the community the song mourns is literally disappearing from the table it took a famine to create.

### edt_08: The Money That Built the Country (evidence)
**Evidence**: ana_06, ana_08, ana_07 | **Context**: det_13, det_14

[ana_06, det_13] What the emigrants sent back became the economy. In 1980, the first year the World Bank measured it, personal remittances were worth 28.2% of Cape Verde's GDP — the all-time peak of the series — and they held an 18–19% plateau through the 1980s and 90s. By 2024 the share was 12.3%, but read the dip correctly: the low of 7.2% in 2010 reflects a denominator transformed by tourism-led growth, not a diaspora gone quiet.

[ana_06] The proof of that reading is 2021. When the pandemic collapsed tourism, the remittance share surged back to 15.3% — the diaspora sent more money precisely when the country needed it most. Dependence receded because the economy grew; the sending never stopped.

[MEDIA: interactive]

[ana_08] Rank Cape Verde against every reporting country, year by year, and its entire economic history reads off one line: #2 in the world in 1980, #2 again in 1994 and 1995, inside the global top ten for 21 consecutive years — then a slide to #40 by 2010 as GDP grew, and a settling at #18 of 160 countries in 2024.

[ana_07, det_14] Even now, that is the top 11% of the world for remittance dependence, in a bracket with Uzbekistan, Jamaica and Haiti. And here is what the money helped buy: in December 2007 Cabo Verde became only the second country in history to graduate from the UN's Least Developed Country list, and fifty years after independence it is an upper-middle-income state with the second-highest life expectancy in Africa. The diaspora is not a footnote to that development story; it is the financing mechanism.

[CHART: ana_06]

### edt_09: The Rise, Measured (evidence)
**Evidence**: ana_12, ana_16, ana_15 | **Context**: det_02, det_06, sct_07

[ana_12] Football tells the same fifty-year story in one curve. On our Elo rating, computed from the full match record, Cape Verde bottomed out at #138 of 198 FIFA-family teams in 1998 — a federation that could barely afford fixtures — then climbed almost monotonically for 25 years: #108 in 2010, #86 in 2014, #64 by July 2026. The all-time peak, 1702, was set during the World Cup itself, on 26 June 2026, the eve of the knockout draw that produced Argentina.

[MEDIA: interactive]

[ana_15] The climb has one perfect emblem. Cape Verde's biggest win ever — 2–0 away in Portugal in 2015, a 440-point upset that ranks #73 of the 33,081 decided matches between established teams — came against the very country that hosts 52% of its counted diaspora. Beating Argentina would have ranked around #25 all-time and #2 among World Cup finals upsets ever, behind only Cameroon–Brazil 2022. They came within nine minutes of it.

[ana_16] Where does that leave them now? As the least-populous team in the entire world top 64: every team rated above Cape Verde comes from a country of at least 1.58 million people, three times its size, and the next smaller country on the board appears only at #79 (Iceland). No national team currently converts so few people into so much rating — because no other team's talent pool is triple its census.

[det_02, sct_07] The qualification that started it all came on 13 October 2025, in Praia: 3–0 over Eswatini, and a country that had never been to a World Cup had won its group.

[CHART: ana_15]

### edt_10: The Eleventh Island (close)
**Evidence**: ana_18, ana_17 | **Context**: det_03, det_14, det_10, sct_03

[ana_17, det_03] Precision matters for the record books, so state it exactly. Cape Verde (527,326 people) is the third-least-populous nation ever to play a World Cup — Curaçao (156,263) took the all-time record a month after Cape Verde qualified, and Iceland 2018 (352,721) sits between them. Only three sub-million nations have ever played the tournament, all since 2018, two of them in 2026: the 48-team expansion opened a door, and small nations are walking through it.

[editorial] But one record belongs to Cape Verde alone, and before it is stated, guess its scale: how many times more populous is the next-smallest country ever to survive a World Cup group stage?

[MEDIA: interactive]

[ana_18] Cape Verde is the smallest nation ever to reach the knockout rounds, and it is not close: the next-smallest advancer in history is Uruguay 1966, at 2.7 million people — 5.1 times larger. The average country at this World Cup has 89 times Cape Verde's population; the largest, the United States, 648 times. Among the tables' honest exclusions, only Northern Ireland's 1982 side (about 1.5 million, outside the population data) would even come second — still three times Cape Verde's size.

[editorial] Since the data snapshot closed on match night: as of 4 July, Cape Verde's tournament is over, and Argentina go on to face Egypt in the Round of 16 on 7 July. A dated note, nothing more — the story this piece tells does not change with the bracket.

[sct_03, det_10] The image to end on is not from Miami and not from Praia. It is the Nieuwe Binnenweg in Rotterdam-West — the diaspora's biggest European street, the neighbourhood that produced both goalscorers — strung end to end with Cape Verdean flags for a World Cup being played an ocean away from both the street and the islands. The eleventh island, dressed for the first tournament its country ever reached.

[det_15, det_14] Morna always knew the nation was bigger than the islands; that is what sodade is for. For four matches in an American summer, the rest of the world could finally see what the song had been counting all along — and the question the tournament leaves behind is the one the UN's matrix still cannot answer: when a nation lives mostly elsewhere, who gets counted the next time it nearly beats the world champions?

[INSTANCE: inst_03]

---

## Editorial Notes

- **LAYER RULE (binding, ana_caveat_01)**: every diaspora number is one of three layers — UN born-in-CV floor (146,396 / 27.9% / all ana_01–ana_05 values), national-census background counts (NL CBS 23,150), heritage/descent estimates (US ~500k, EUDiF ~120%). Never mix layers in one chart, metric or sentence-without-labels. The UN layer's missing hosts (Netherlands, US, Spain, Senegal) must be shown as ghosted/absent, not silently omitted. This is a narrative strength — "even the UN can't fully count this nation" — not a footnote.
- **Guess-before-reveal ordering (binding)**: the interactive placeholders in edt_04 (zero home-based players), edt_06 (27.9 per 100) and edt_10 (5.1x) sit BEFORE the paragraphs that state their answers. The Designer/Programmer must preserve that order; the dek and edt_01–edt_02 must not leak 15/26, 57.7%, zero, 27.9 or 5.1x. The hero's payoff numbers (15/26, 50.3% of caps, 3-of-4 goals) first appear only after the hero widget in edt_03.
- **Exact numbers (do not round or "fix")**: 146,396; 76,835 (52.5%); 34,814 (23.8%); 27.9; 13.8; 15/26 = 57.7%; 414/823 = 50.3%; 33/75 = 44.0%; 3.4 / 8.3 / 88.3 / 7.6; 2.8 / 11.3 / 33.4; 28.2% (1980) / 7.2% (2010) / 15.3% (2021) / 12.3% (2024); #2 of 90; 21 consecutive years; #18 of 160; #20 of 212; 4,250 → 1,115 (−73.8%); 1702 (2026-06-26); #64 of 210; #138 of 198; 527,326; 156,263; 352,721; 5.1x; 89x; 648x; x2.83; x7.15; 1.21%.
- **Vozinha is 40, not 39** (ana_caveat_08): the dataset DOB (1986-06-03) wins over Sky's "39". Prose already handles it; captions must not reintroduce 39.
- **Sidny Lopes Cabral photo (decision)**: NO license-clean, identity-verifiable photo exists (scout gaps). Do not use an unlicensed press photo, do not substitute a lookalike, do not generate or illustrate his likeness (AI-face policy: illustration-of-person is rejected). His goal is represented by the verified FOX highlights embed (inst_02) — moving pictures of the actual goal beat any portrait — and the Rotterdam-scorer visual beat is carried by the identity-gated Deroy Duarte photo (sct_09, inline portrait, not full-bleed).
- **Model honesty sentences must survive to the page** (ana_caveat_04, ana_caveat_09): (1) "our own Elo implementation, not comparable with published boards" and (2) "extra time as a coin flip is an assumption — 7.6% advance" are both in edt_02 prose; do not cut them in layout.
- **ana_05 rank framing** (ana_caveat_02): always "#20 of the 212 WB-covered origins" — Puerto Rico and Somalia are excluded by the population join; never claim a raw world rank.
- **Football data conventions** (ana_caveat_03): scores are ET-inclusive (the match is 3–2, not 2–2+ET), shootouts count as draws, everything is "as of 2026-07-03". Live status (Argentina–Egypt R16) is a compact dated display-only note in edt_10 — never fed to the model, never a headline.
- **Client models already shipped**: hero uses cm_02 `squadTally()` (baseline 15/414/33 = 57.7/50.3/44.0); the odds explorer uses cm_01 `matchOdds()` (baseline 3.4/8.3/88.3/7.6, RATINGS_PRE_R32 covers all 32 knockout teams). No new Analyst work needed.
- **Media notes**: sct_08 (Bubista) is 508×677 — inline portrait only, never hero/full-bleed. sct_09 (Duarte) 581×1024 — inline. Flag PNG set (det_media_07, public domain) is available for the hero widget's country chips and the edt_05 map. Mindelo (det_media_02), Pico do Fogo (det_media_03), Cesária Évora (det_media_01) and Ernestina (sct_06) belong to edt_07's history/culture run; Praia (sct_07) to edt_09; Hard Rock aerial (sct_04) to edt_01; Delfshaven (sct_05) to edt_06; Rotterdam flags (sct_03) is RESERVED as the edt_10 full-circle image — do not spend it earlier.
- **Brockton tone** (det_09): report the curfew and the nine injured factually and briefly; the section's tone stays on the scale and intensity of diaspora identity, not the violence.
- **Cut findings**: ana_13 (decade win rates) is cut — it re-tells ana_12's arc with weaker numbers; do not resurrect it for a spare chart slot.
