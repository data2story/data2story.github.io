## Story Spine
**Core claim**: Across 15 seasons in Europe's top leagues, almost every football manager performs within a hair's breadth of what their squad's quality already predicts — and the few who genuinely lift their teams are the rare exception, not the rule fans imagine.

**Tension**: Hire-and-fire fever assumes managers are the decisive variable. The data refuses to grant most of them any measurable edge over an interchangeable league-average coach.

**Payoff**: The reader leaves convinced that football's manager-cult — the boardroom panic, the £10m severances, the talk-radio convulsions — is mostly aimed at the wrong target.

## Sections

### edt_01: The miracle that wasn't a miracle
**Evidence**: ana_12, ana_03 | **Context**: det_07

[ana_12] Leicester City won the 2015-16 Premier League title beating their FIFA-rating-based forecast by 1.07 points per game — about 41 extra league points across the season, the most extreme single-season over-performance in 15 years of big-five-league data.

[ana_03, det_07] But pull back to the full distribution of 502 manager-tenures of at least one full season, and Leicester is a curiosity, not the rule. The average manager added 0.04 points per game above what player skill predicted — statistically indistinguishable from luck. The 5th-to-95th-percentile range of overperformance runs only from -0.24 to +0.34 points per game. Almost half of all tenures sit within 0.10 of zero.

[CHART: ana_03]
[MEDIA: video]

### edt_02: A model the betting markets respect
**Evidence**: ana_01 | **Context**: det_01, det_02, det_08

[ana_01, det_02] To know whether a manager is over- or under-performing, you first need to know what their squad ought to achieve. The Economist built a forecast using EA's FIFA video-game ratings — the only public skill estimate covering more than a decade — and ran it across 27,390 league fixtures from 2004 to 2019. Players were z-scored within position group, exponentiated to capture the non-linear gap between an elite and a merely good footballer, and fed into a per-league logistic regression that predicted home wins, draws and away wins.

[ana_01, det_08] The result is a forecast that, on average, misses each team's seasonal points total by about 7.3 points across all 1,470 team-seasons in the sample. For comparison, preseason betting markets — the wisdom of millions of staked pounds — produce average errors only fractionally smaller, around 8 points for English campaigns. The correlation between expected and actual points-per-game across all team-seasons is 0.80. The benchmark is real.

[CHART: ana_01]

### edt_03: The leaderboard nobody expects
**Evidence**: ana_04 | **Context**: det_06

[ana_04] Now sort every full-season-or-longer manager tenure by points-per-game above expectation. The leaderboard is dominated not by household names but by short, brilliant interruptions. Abelardo's 42-game stretch at Deportivo Alavés tops the list at +0.57 ppg. Ralph Hasenhüttl's 68 games at RB Leipzig follow at +0.55. Two Luciano Spalletti tenures, a Ralf Rangnick stint, a Felix Magath title at Wolfsburg — these are the names that out-performed.

[ana_04] Claudio Ranieri's title-winning Leicester tenure appears sixth on the leaderboard at +0.47 ppg, slightly below the leader. Even the most celebrated overachievement of the decade looks, on this metric, like a slightly louder version of a dozen lesser-known runs. Below the very top, the curve flattens fast: by tenure 12 you are at +0.41, only 0.05 ppg below first place.

[CHART: ana_04]

### edt_04: The killer test — past performance, future job
**Evidence**: ana_08, ana_09 | **Context**: det_04, det_07

[ana_08, det_04] The hardest question a coach's CV faces is whether their record at one club predicts their record at the next. Among 222 managers in this dataset who had at least two distinct tenures, the correlation between first-tenure and second-tenure points-per-game above expectation is 0.04 — statistically indistinguishable from no relationship at all (p = 0.54). Of managers who over-performed in tenure one, only 45% over-performed in tenure two. Of those who under-performed, 37% over-performed at the next club. Both numbers hover around a coin flip.

[ana_09] Split the same managers into quartiles by their first-tenure result, and watch what happens at the next club. Every group, including the very top, collapses back toward zero. The bottom quartile (mean -0.4 ppg in tenure one) ended tenure two at -0.04. The top quartile (mean +0.3) ended at -0.001. The apparent good and bad coaches of round one converge in round two — regression to the mean in its purest visible form.

[CHART: ana_09]
[MEDIA: interactive]

### edt_05: Why a single season tells you almost nothing
**Evidence**: ana_18 | **Context**: det_06, det_07

[ana_18, det_07] The Economist's modellers found, by optimising for forecast accuracy, that the best prediction of a manager's future impact requires adding 461 games of league-average performance to his actual record before drawing any conclusions. That is a brutal multiplier: a coach with a single 38-game season retains only 7.6% of his record after shrinkage. A three-season tenure retains a fifth. Ten seasons gets you to 45%. Twenty seasons of work — 760 games — reaches just 62%. Effectively, the data refuses to hear a manager's voice clearly until he has worked for two decades.

[ana_18, det_06] This is what makes Sir Alex Ferguson exceptional in the technical sense. Ferguson logged 342 league games at Manchester United inside the data window, averaging 2.25 points per game versus 2.09 expected — only +0.159 above expectation, but he kept producing it for a quarter of a century. His tenure retains 43% of its weight after shrinkage. Most managers, the model says, simply do not exist long enough to be heard above the noise.

[CHART: ana_18]
[MEDIA: image]

### edt_06: Klopp, the textbook
**Evidence**: ana_16 | **Context**: det_09

[ana_16, det_09] Jürgen Klopp's career across three clubs reads like the textbook over-performance trajectory the rest of this analysis insists is rare. At Mainz 05 (2001-08, 102 covered games) he edged 0.05 ppg above expectation. At Borussia Dortmund (2008-15, 238 games) he leapt to +0.18 ppg — the spine of the original Economist piece's third chart. At Liverpool (from October 2015, 126 games covered) he rose again to +0.31. The line goes only one way, and each step rests on enough games to drown out luck.

[CHART: ana_16]

### edt_07: The famous-name table is not what you think
**Evidence**: ana_17 | **Context**: det_06

[ana_17, det_06] The same lens makes other reputations look thinner. Pep Guardiola's three tenures at Barcelona, Bayern and Manchester City all post positive margins, but only modestly — +0.11, +0.08, +0.28. Diego Simeone is consistently elite at Atlético (+0.26 over 267 games). Antonio Conte's two Juventus stints are spectacular (+0.44, +0.38). Mauricio Pochettino climbed from -0.02 at Espanyol to +0.30 at Tottenham.

[ana_17] Carlo Ancelotti is the surprise. Across his AC Milan, Chelsea, PSG, Real Madrid and Bayern tenures the model rates him between -0.27 and +0.03 ppg above expectation — a man with a cabinet of Champions League trophies, and on this metric a roughly average coach paired with a string of elite squads. The data is not telling you Ancelotti is bad. It is telling you that *given the players he had*, an average coach would have done about as well.

[CHART: ana_17]
[MEDIA: image]

### edt_08: The active board, projected
**Evidence**: ana_05, ana_07 | **Context**: det_05

[ana_05] Apply the shrinkage formula to every working manager in late 2018 and you get a table of projected points-added per season. Lucien Favre tops it at +3.76, followed by Rudi Garcia (+3.40), Diego Simeone (+3.27), Maurizio Sarri (+3.04). Klopp lands sixth at +2.85, Tuchel seventh at +2.79. Every name on this top-10 list rests on at least 100 prior career matches; most on more than 250.

[ana_07, det_05] Look at the rest of the population, though. Of 596 working managers, 432 — roughly three in four — project as below average. Just 44 (7.4%) project as adding more than one point per season; only 74 clear half a point. Half the entire population sits within ±0.5 points-per-season of league-average, a margin so small it would be invisible to a fan's eye across a 38-game campaign.

[CHART: ana_05]
[MEDIA: interactive]

### edt_09: What this data does, and does not, say
**Evidence**: | **Context**: det_05, det_07

[editorial] None of this proves managers do not matter. It proves that the variation between managers, given the players they actually inherit, is small relative to the variation that comes from squad quality alone. A few coaches — Ferguson, Klopp, Simeone, Conte at his peak — show up as outliers strong enough to clear regression to the mean. Most do not.

[det_05, det_07] What this challenges is the industry's reflexive logic of dismissal. Premier League clubs paid more than £90 million in manager severance in 2018-19 alone. The data here suggests that the new boss is, on the evidence, almost always indistinguishable from the old one. The post-sacking 'bounce' that fans cite is largely the team's underlying quality reasserting itself — exactly what would have happened anyway. Hiring and firing has become football's most expensive ritual aimed at one of its smallest variables.

## Editorial Notes
- 0.04, 0.159, 0.310, 461, 7.4%, 72.5%, 45%, 0.04 (correlation), 1.07, 7.27 must all be exact, not rounded.
- The Klopp progression Mainz → Dortmund → Liverpool must read with all three numbers in order.
- Carlo Ancelotti's negative margins must stay visible — they are core to the surprise of section edt_07.
- The 461-games shrinkage number is load-bearing; do not paraphrase it as "many games".
- The hook (edt_01) leads with Leicester *first*, then immediately undercuts it with the distribution; do not reorder.
- Section edt_09 is the only "editorial" closer; it does not reference a specific ana_xx finding.
