## Story Spine

**Core claim**: A transparent Elo-Poisson-Monte-Carlo model, run mid-tournament, makes Argentina the 26.3% favourite to win the 2026 World Cup — but the same model quietly disagrees with the official ranking, and you can re-run it yourself to see how fragile that 26.3% really is.

**Tension**: A single bold number ("Argentina 26.3%") reads like a verdict. It is actually the output of a model with assumptions you can poke — nudge one team's strength and the whole order can flip — and on this tournament's 28 games so far it has been no better than guessing.

**Payoff**: The reader stops treating a forecast as a prophecy. They have run the model, watched the favourite change, seen where it fights the FIFA ranking, and learned to read a probability as a claim that can be argued with — and audited back to the exact code.

**The interactive centerpiece**: The reader PRODUCES the headline. An explorable (`explorable_recompute`, powered by the Analyst's `client_model` = `code/client_model.js`, `window.WC_MODEL.simulate(n, {team: deltaElo})`) shows the published champion bars at rest (Argentina 26.3%, Spain 22.2%, ...). The reader drags a team's Elo slider and presses "re-run"; the in-browser Monte-Carlo recomputes champion odds live and the bars animate to the new distribution, with the delta vs the published number shown. It lands AT the reveal in edt_02 — the reader's own action is how the 26.3% (and its fragility) is first demonstrated, not a widget bolted on after the answer. Drop Argentina's Elo by 100 and Spain becomes favourite; that is the felt realization. The Analyst emitted the `client_model` for ana_01; degrade gracefully to the static published bar chart if JS is off.

## Sections

### edt_01: Hook
**Evidence**: ana_01 | **Context**: det_01, det_08

[ana_01] One number sits on top of the 2026 World Cup: 26.3%. That is the model's estimate, as of 18 June, of the chance that Argentina lifts the trophy — ahead of Spain at 22.2%, France at 14.6% and England at 9.8%. The ladder drops away fast: the top two hold almost half of all the title probability between them, and only 14 of the 48 teams have even a one-in-a-hundred chance.

[ana_01, det_01] It is the broadest World Cup ever — 48 teams, 12 groups, a brand-new Round of 32 — and yet the favourites cluster at the very top. The 26.3% is not a guess about one match; it is the share of 100,000 simulated tournaments, each one playing out every remaining game and the full bracket, that Argentina wins.

[editorial] A number that confident invites a simple question: says who? Before you take it on trust, you should be able to run it yourself.

[MEDIA: image]

### edt_02: Run it yourself
**Evidence**: ana_01 | **Context**: det_03

[ana_01, det_03] The model behind the 26.3% is not a black box. It rates every team with an Elo number built from a century and a half of international results, turns the gap between two teams into expected goals, and then simulates the rest of the tournament tens of thousands of times. Below, the bars show the published odds — Argentina 26.3%, Spain 22.2%, and so on down the field. Now change something.

[ana_01] Drag a team's strength up or down and re-run the simulation. The odds recompute live, in your browser, on the same model that produced the headline. Weaken Argentina by a hundred Elo points — roughly the gap between a top side and a merely good one — and Spain takes over as favourite while Argentina slides toward the chasing pack. The 26.3% was never a fact about the future; it was a reading that moves the moment you touch its inputs.

[INTERACTIVE: ana_01]

[editorial] Which raises the next question. If the number bends that easily, why believe any version of it?

### edt_03: Why believe it
**Evidence**: ana_06 | **Context**: det_03, det_04

[ana_06, det_04] Here is the honest answer, including the part that doesn't flatter the model. Tested on 8,000 historical internationals it had never seen, the model clearly beats a naive baseline that just predicts the average home/draw/away rates: its log-loss is 0.900 against the baseline's 1.062 — about 15% less error — and it calls 58.8% of results correctly versus 48.7%. Fit only on data from before the tournament, it never trained on a single game it is now forecasting.

[ana_06] But on the 28 games of this World Cup already played, the model and the naive baseline are a dead heat: log-loss 1.068 against 1.077, accuracy 50% against 54%. Twenty-eight games is a tiny, upset-prone sample, so this neither vindicates nor sinks the model — it is a caution, not a verdict. The long-run skill is real; the early tournament has simply been noisy.

[CHART: ana_06]

### edt_04: Where the model fights the ranking
**Evidence**: ana_02 | **Context**: det_07

[ana_02, det_07] A model trained on results does not agree with the official FIFA ranking, and the gaps are where the story lives. Its boldest call is Norway: ranked 31st in the world by FIFA, but lifted to the tenth-best chance of winning the whole thing. Colombia is the headline disagreement — FIFA's 13th, the model's fifth, at 6.2%, ahead of Brazil. Australia jumps from 27th to 14th.

[ana_02] The model is just as willing to fade a favourite. Morocco, FIFA's seventh, drops to twelfth; Portugal, fifth in the world, sits seventh here, behind a Colombia side ranked eight places below it. At the very top the two systems shake hands — Argentina is first on both lists, England fourth — but everywhere in the middle they argue. Those arguments are exactly what the slider above lets you settle for yourself.

[CHART: ana_02]
[MEDIA: image]

### edt_05: Money versus merit
**Evidence**: ana_03 | **Context**: det_05

[ana_03, det_05] The transfer market and the model value teams differently, and the cleanest example is Colombia again. France fields the most expensive squad in the tournament, €1.52bn of talent, and the model gives it a 44.4% chance of reaching the semi-finals — about €34m of squad value for each percentage point. Colombia's squad costs €302m, a fifth of France's, yet still earns a 25.2% semi-final chance: just €12m per point, nearly three times more efficient.

[ana_03] At the extremes the gap is starker. Australia buys a semi-final percentage point for €7m; Portugal and Germany, both billion-euro projects, pay €74m and €63m for the same thing and the model rewards them with semi-final chances under 16%. The market pays for names. The model counts results, and the two bills rarely match.

[CHART: ana_03]

### edt_06: The coin still in the air
**Evidence**: ana_04, ana_07 | **Context**: det_02

[ana_04, det_02] For half the field the forecast is barely a forecast. Eight teams are already through to the new Round of 32 in 99% or more of simulations — Argentina, Mexico, Switzerland, Canada and the rest of the locked-in elite. But nine more sit on a genuine knife edge, their chance of reaching the knockouts hovering between 40% and 60%: Senegal at 58.5%, Ghana at 56.7%, Turkey, Algeria, Bosnia & Herzegovina at 48.1%. For them a single result swings everything.

[ana_07, det_02] And even the teams that are certain to advance cannot yet be told who they will play. Because the eight best third-placed teams fill the rest of the bracket, FIFA's rulebook tabulates all 495 ways the groups can shake out, and the simulation averages over every one. Argentina reaches the Round of 32 in essentially every simulation — but its opponent there is still a distribution, not a name.

[CHART: ana_04]

[ana_05] Step back and the broadest World Cup ever still funnels to a familiar few. European and South American teams hold 94.2% of all the title probability between them; the other four confederations split the remaining 5.8%, and every team in the model's top six comes from those same two continents. Forty-eight teams walked in. The trophy, on these numbers, is still being argued over by about a dozen — and the argument is one you can now run yourself.

[CHART: ana_05]

## Editorial Notes
- 26.3% (Argentina), 22.2% (Spain), 14.6% (France), 9.8% (England), 6.2% (Colombia), 3.9% (Brazil) must be EXACT — they are the headline and the explorable's at-rest state.
- edt_02 is the load-bearing section: the explorable centerpiece. It must land at the reveal, recompute live via client_model, and show the published bars at rest. Do not move it after edt_04.
- The "Argentina -100 Elo -> Spain favourite" claim (edt_02) is data-bound via the client_model — the reader produces it; never hardcode the flipped numbers.
- ana_06 (model health) must keep BOTH numbers visible: the 8000-game win AND the 28-game tie. Do not bury the tie; it is the honesty beat.
- Colombia FIFA#13 -> model#5 and Norway FIFA#31 -> model#10 are the load-bearing disagreements; keep ranks exact.
- End on tension (the coin in the air / the argument you can run), not a summary. No marketing language.
