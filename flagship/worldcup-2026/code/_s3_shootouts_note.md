# Section 3 build-note — Knockout realism / penalty shootouts

**Files produced (in `code/`):** `build_shootouts.py` (regenerates from source, deterministic, byte-identical on re-run), `shootouts_stats.json` (documented keys).

**Sources (read-only):**
- `phase2/datasets/worldcup_2026/raw/shootouts.csv` — 678 historical international penalty shootouts, 1967–2026 (martj42). Columns: `date, home_team, away_team, winner, first_shooter`. `first_shooter` known for 256/678; `winner` and `first_shooter` always one of the two listed sides (asserted in the build).
- `intl_results_history.csv` (the blog's own Elo training file, 49,477 matches) — used to (a) compute each shootout's pre-match Elo favourite via the forecast's own `elo.py`, and (b) tag each shootout's tournament by joining on `date` + `{teams}`.

---

## 1. Headline numbers

| Metric | Value | 95% CI (Wilson) | vs coin flip |
|---|---|---|---|
| **Favourite (higher pre-match Elo) wins the shootout** | **53.7 %** (364/678) | [49.9 %, 57.4 %] | p = 0.060 |
| First shooter wins | 53.1 % (136/256) | [47.0 %, 59.1 %] | p = 0.35 |
| Listed-first ("home") team wins | 54.1 % (367/678) | [50.4 %, 57.8 %] | p = 0.035 *(venue-confounded — see caveat)* |
| **World Cup finals subset** | n = 35 (1982–2022) | — | — |
| · first shooter wins (WC) | 48.6 % (17/35) | [33.0 %, 64.4 %] | p = 1.00 |
| · favourite wins (WC) | 57.1 % (20/35) | [40.9 %, 72.0 %] | p = 0.50 |

**The cleanest coin-flip framing (use this as the section's anchor stat):**

> Across 678 international shootouts, the **better team on paper won just 53.7 %** of the time — barely better than tossing a coin. And these were not close matchups: the favourites carried an **average Elo edge of 114 points, the kind of gap that wins about 66 % of matches in normal play**. The advantage almost completely evaporates once the game goes to penalties. Tighten the filter to only the *lopsided* ties — favourites who would win roughly **3 in 4** games in regulation (Elo gap ≥ 150) — and they still win the shootout only **55.7 %** of the time.

**The "advantage evaporates" ladder (the single most persuasive number set — drives the chart):**

| Pre-match Elo gap | n | Favourite *should* win in regulation | Favourite *actually* wins the shootout |
|---|---|---|---|
| any (≥ 0) | 678 | 65.8 % | **53.7 %** |
| ≥ 25 | 565 | 68.4 % | 54.2 % |
| ≥ 50 | 473 | 70.7 % | 53.3 % |
| ≥ 100 | 321 | 75.0 % | 52.6 % |
| ≥ 150 | 201 | 79.1 % | **55.7 %** |

The regulation column climbs steeply; the shootout column stays pinned near 50 %. That gap *is* the coin-flip.

**Frequency / trend (by decade):** 1970s 38 → 1980s 97 → 1990s 126 → 2000s 144 → 2010s 153 → 2020s 119 (partial decade). Shootouts have become steadily more common as more knockout competitions adopted them. (Per-year counts are in `frequency.by_year` if a finer time axis is wanted.)

---

## 2. Recommended Vega-Lite chart spec sketch (for `embedChart()` / the page's `embed()` helper)

The page wires charts through `embed("<id>", {spec})` (index.html ~line 1950). Specs use `"width":"container"`, inline `data.values`, `$schema` v5, and the JS color constants `ACCENT="#c9a227"`, `MUTED`, `DOWN="#b9603f"`, `INK`, `LINE`. The helper injects `config` (axis/legend/title theme) and a responsive width, so the spec below intentionally omits those.

**Primary chart — "the advantage evaporates" (favourite: expected-in-regulation vs actual-in-shootout, by Elo gap).** This is the most rhetorically effective view: two series, the model's regulation expectation pulling away while the shootout reality stays flat near 50.

```js
// des_shootout_chart — favourite win% expected (regulation) vs actual (shootout), by Elo gap
embed("des_shootout_chart", {
  "$schema":"https://vega.github.io/schema/vega-lite/v5.json",
  "width":"container","height":300,
  "title":"When the game goes to penalties, the better team's edge nearly vanishes",
  "data":{"values":[
    {"gap":"any","n":678,"who":"Expected in regulation","pct":65.8},
    {"gap":"any","n":678,"who":"Actual in shootout","pct":53.7},
    {"gap":"≥25","n":565,"who":"Expected in regulation","pct":68.4},
    {"gap":"≥25","n":565,"who":"Actual in shootout","pct":54.2},
    {"gap":"≥50","n":473,"who":"Expected in regulation","pct":70.7},
    {"gap":"≥50","n":473,"who":"Actual in shootout","pct":53.3},
    {"gap":"≥100","n":321,"who":"Expected in regulation","pct":75.0},
    {"gap":"≥100","n":321,"who":"Actual in shootout","pct":52.6},
    {"gap":"≥150","n":201,"who":"Expected in regulation","pct":79.1},
    {"gap":"≥150","n":201,"who":"Actual in shootout","pct":55.7}
  ]},
  "encoding":{
    "x":{"field":"gap","type":"ordinal","title":"pre-match Elo gap of the favourite",
         "sort":["any","≥25","≥50","≥100","≥150"],"axis":{"labelAngle":0}},
    "y":{"field":"pct","type":"quantitative","title":"favourite win %","scale":{"domain":[40,85]}},
    "color":{"field":"who","type":"nominal","scale":{"range":[MUTED,ACCENT]},"title":null},
    "tooltip":[{"field":"gap","title":"Elo gap"},{"field":"who"},
               {"field":"pct","title":"win %"},{"field":"n","title":"shootouts"}]
  },
  "layer":[
    {"mark":{"type":"line","point":true,"strokeWidth":2.5}},
    {"mark":{"type":"rule","strokeDash":[4,4],"color":"#5b616e"},
     "encoding":{"y":{"datum":50}}}   // 50% coin-flip reference
  ]
});
```

The dashed 50 % rule makes the "Actual in shootout" line read instantly as hugging the coin-flip.

**Alternate / simpler chart — first-shooter win rate vs 50 % (single bar + reference rule).** Use if a smaller, one-glance figure is preferred:

```js
embed("des_firstshooter_chart", {
  "$schema":"https://vega.github.io/schema/vega-lite/v5.json",
  "width":"container","height":220,
  "title":"First-shooter advantage is small — and disappears at the World Cup",
  "data":{"values":[
    {"sample":"All shootouts (n=256)","pct":53.1},
    {"sample":"World Cup finals (n=35)","pct":48.6}
  ]},
  "encoding":{
    "x":{"field":"pct","type":"quantitative","title":"first shooter win %","scale":{"domain":[0,70]}},
    "y":{"field":"sample","type":"nominal","title":null},
    "color":{"condition":{"test":"datum.pct >= 50","value":ACCENT},"value":DOWN},
    "tooltip":[{"field":"sample"},{"field":"pct","title":"first-shooter win %"}]
  },
  "layer":[
    {"mark":{"type":"bar"}},
    {"mark":{"type":"rule","color":"#5b616e"},"encoding":{"x":{"datum":50}}}
  ]
});
```

**Optional third — frequency over time** (`frequency.by_decade`): a simple bar of shootout counts per decade if the section wants to establish "this keeps happening". Lower priority; the two above carry the argument.

---

## 3. Draft prose (2–3 short factual paragraphs)

> **The one knockout the model refuses to predict.** Every probability on this page comes from simulating matches — but our simulation stops at the final whistle. When a knockout tie is level after 90 minutes, the model does not play out extra time and penalties kick by kick; it splits the tie with a single win-probability number and moves on. That is a deliberate simplification, and the data says it is a forgivable one, because the thing we are skipping is very close to a coin toss.

> We checked it against 678 real international penalty shootouts going back to 1967. The **higher-rated team — the "favourite" by the same Elo we use everywhere else — won just 53.7 %** of them. These were not toss-ups on paper: the favourites averaged a 114-point Elo edge, worth about a **66 % win rate in normal play**. Once the match reached penalties, almost all of that edge disappeared. Even among the most one-sided pairings, where the stronger side would win roughly three games in four, the shootout win rate barely moved off 50 %. The team that takes the first kick wins **53.1 %** of the time overall — and at the **World Cup finals specifically, the first shooter has won just 17 of 35 (48.6 %)**, slightly *less* than half.

> So the model's analytic shortcut is not hiding a systematic bias; it is declining to forecast something that is, by the historical record, mostly luck. When you see two contenders meet in a simulated round of 16 and the odds read close to even, remember that if it goes the distance, the real thing would be close to even too — Argentina lifted the 2022 trophy on penalties after France shot first, and that is exactly the kind of near-coin-flip this section is about.

*(All bolded figures are keys in `shootouts_stats.json`; prose uses only computed values. Trim to taste — paragraphs 1+2 alone carry the point if space is tight.)*

---

## 4. Provenance notes (for a later `verify_map` entry + runnable cell)

Mirror the existing `verify/verify_map.json` schema (`kind`, `title`, `claim`, `cell_id`, `code_file`, `code_lines`, `code`, `data_preview`). Suggested entries:

- **`ana_shootout_favourite`** (the headline)
  - `kind`: `"computation"`
  - `claim`: "Across 678 international penalty shootouts (1967–2026), the higher pre-match-Elo team won 53.7 % (364/678; 95 % CI 49.9–57.4 %; two-sided binomial p = 0.06 vs 50 %). The favourites averaged a 114-point Elo edge (≈ 66 % regulation win expectation), so penalties erase most of the better team's advantage."
  - `code_file`: `code/build_shootouts.py`; `code_lines`: the `# ---- 2. favourite` block in `main()` (the `fav_win` computation + `expected_win_prob_from_elo_gap`).
  - `data_source`: `shootouts.csv` + `intl_results_history.csv`; output key `favourite` in `shootouts_stats.json`.
  - `data_preview`: the `favourite_by_elo_gap` table (gap, n, expected %, actual %).

- **`ana_first_shooter`**
  - `claim`: "The team shooting first won 53.1 % of the 256 shootouts with a recorded first kicker (95 % CI 47.0–59.1 %, p = 0.35) — and only 48.6 % (17/35) at the men's World Cup finals."
  - `code_lines`: the `# ---- 1. first-shooter` and `# ---- 4. World Cup` blocks.
  - output keys `first_shooter`, `world_cup.first_shooter`.

**Computation definitions (verbatim, for the verify cell's prose):**
- **Favourite** = team with the higher Elo, where Elo is computed by `elo.py`'s eloratings.net rule over every international with `date < shootout_date` (importance × goal-difference multiplier; +100 home edge only on non-neutral games). The sweep in `elo_as_of_each_shootout()` advances the rating state match-by-match and freezes both teams' ratings just before each shootout, so **a shootout never informs its own favourite** (leak-free, identical engine to the rest of the forecast).
- **First shooter / winner** = the `first_shooter` / `winner` columns of `shootouts.csv` (each asserted to be one of the two participating teams).
- **World Cup subset** = `tournament == "FIFA World Cup"` after joining each shootout to `intl_results_history.csv` on `(date, {home, away})`; this excludes World Cup *qualifiers* and non-FIFA tournaments that contain the words "World Cup" (e.g. the 2009 "Viva World Cup", CONIFA). 35 shootouts result, 1982–2022; 1 minor non-FIFA shootout (Saare County v Åland Islands, 2011) does not match a tournament and is excluded.
- **Coin-flip test** = two-sided *exact* binomial p-value against p = 0.5; **CI** = 95 % Wilson score interval. Both are dependency-light closed forms in `build_shootouts.py` (`binom_two_sided_p`, `wilson_ci`), so a runnable cell reproduces every number without scipy.
- **"Expected in regulation"** = the eloratings logistic `1 / (1 + 10^(−gap/400))` evaluated at the favourites' mean Elo gap (neutral, no home term) — the honest "what that gap buys in normal play" baseline the shootout figure is contrasted against. It is a regulation-win expectation, **not** a claim about extra-time.

**Honesty caveats (keep these explicit wherever the numbers appear):**
1. The favourite result is *near* significance (p ≈ 0.06), not a clean null — phrase as "barely above a coin flip / mostly luck", never "exactly 50/50" or "no skill at all". A real ~3-point edge is plausible.
2. The **listed-first team 54.1 % (p = 0.035)** is venue-confounded — many "home_team" rows are neutral-site matches, so do **not** present it as a home-advantage effect; it is kept in the JSON only for completeness with an inline `_caveat`.
3. `first_shooter` is missing for 422/678 shootouts (known mostly for more recent / major matches), so the 53.1 % first-shooter figure is on the 256-row subset, not the full corpus — stated as such.
4. The WC subset (n = 35) is small; its CIs are wide ([41–72 %] for the favourite). Use it as colour ("even at the World Cup…"), and lean on the full 678-shootout sample for the statistical claim.
