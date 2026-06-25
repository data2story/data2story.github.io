# Section-3 build note — "Is 30.8% a lot?" historical base-rate anchor

**Question the section answers:** the model says Argentina **30.8%**. A reader's
instinct is "favourites always flop." Does the history back that instinct? The
anchor: historically the **pre-tournament favourite wins only ~23%** of World
Cups, so 30.8% reads as **above** the long-run favourite hit-rate — a
slightly-stronger-than-usual favourite, not a lock.

Files this note accompanies:
- `code/build_historical.py` — regenerates the from-table facts deterministically.
- `code/historical_favourites.json` — computed facts + the cited base rate (with source).

---

## 1. Key numbers

### Computed from the table (`historical_wc_summary.csv`, 22 men's WCs 1930–2022)
Reproducible — re-running `py code/build_historical.py` gives byte-identical output.

| Fact | Value | Note |
|---|---|---|
| Tournaments in table | **22** (1930–2022) | |
| Distinct champion **labels** | **9** | raw labels in the column |
| Distinct champion **nations** | **8** | after merging "West Germany"→"Germany" (same nation) |
| **Top-3 nations' share of titles** | **13 / 22 = 59.1%** | Brazil 5, Italy 4, Germany 4 |
| Repeat champions (≥2 titles) | **6 nations hold 20 / 22 = 90.9%** | Brazil 5, Italy 4, Germany 4, Argentina 3, Uruguay 2, France 2 |
| **Host-nation wins** | **6 / 22 = 27.3%** | 1930 URU, 1934 ITA, 1966 ENG, 1974 W.GER, 1978 ARG, 1998 FRA |

**Cleanest 2–3 to feature** (highest signal, lowest caveat):
1. **Only 8 nations have ever won** the 22 editions — the trophy is extraordinarily concentrated.
2. **The top 3 nations alone hold 13 of 22 titles (59%)** — winning is a repeat business for a tiny club.
3. **The host wins about 27% of the time** — a useful sanity reference: even *home advantage* historically converts barely more than a quarter of the time, which makes a non-host 30.8% favourite look strong.

> Provenance caveat to keep honest: the 9→8 merge (West Germany = Germany) is a
> light editorial judgment, **not** something the bare table asserts. The JSON
> reports BOTH counts (`distinct_champion_labels` = 9, `distinct_champion_nations`
> = 8) so the runnable cell can show the raw 9 and explain the merge.

### Cited — external, NOT from our table
> **~23%.** "Favourites tend to win about 23% of the time, based on FIFA's review
> of the previous 22 men's tournaments. The listed World Cup favourites have won
> the trophy only five times over the years."

- **Figure:** ~23% (favourite wins ≈ 5 of 22).
- **Sharper corroborating detail:** of editions **since 1966** (when pre-tournament
  odds were first recorded), the **shortest-price** favourite won only **3 times** —
  West Germany 1974, Brazil 1994, Spain 2010.
- **Primary source:** FIFA — *"What happened to the FIFA World Cup favourites?"*
  `https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/what-happened-to-the-fifa-world-cup-favourites`
- **Secondary (independent restatement + the "3 since 1966" detail):**
  European Gaming Industry News — *"50+ World Cup betting statistics: Trends &
  records (2026)"* `https://europeangaming.eu/portal/world-cup-betting-statistics/`
- **Accessed:** 2026-06-24.

> Why two sources: FIFA is the origin of the ~23% wording, but its article body is
> JS-rendered and could not be machine-fetched verbatim; the europeangaming page
> restates the same FIFA figure (and adds the shortest-price detail) and is the
> citable text mirror. Cite FIFA as the claim's origin; europeangaming as the
> accessible corroboration.

### The comparison the section lands
- Argentina model probability: **30.8%** (from the simulation, *not* this table).
- Long-run favourite hit-rate: **~23%** (cited).
- **Δ = +7.8 percentage points above the historical favourite rate.**

---

## 2. Vega-Lite chart spec sketch (for the page's `embedChart()` / `embed()` helper)

The page's helper signature is `embed("<dom-id>", <vega-lite-spec>)` (see
`index.html` ~line 1980; it injects width, theme, `actions:false`, SVG renderer).
Use `"width":"container"`, give the host `<div class="chart-container wbleed"
id="des_hist_favourite" data-des="des_hist_favourite" data-ana="ana_XX">`, and
tag it with whichever `data-ana` id the Section-3 analysis block gets (so the
Verify layer can wire it).

**Recommended primary chart — the 30.8% vs ~23% bar (lands the thesis directly):**

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "width": "container", "height": 220,
  "title": "Argentina's 30.8% vs the long-run favourite win-rate",
  "data": {"values": [
    {"label": "Historical favourite win-rate", "pct": 23, "kind": "cited"},
    {"label": "Model: Argentina 2026", "pct": 30.8, "kind": "model"}
  ]},
  "encoding": {
    "y": {"field": "label", "type": "nominal", "title": null, "sort": "-x",
          "axis": {"labelLimit": 320}},
    "x": {"field": "pct", "type": "quantitative",
          "title": "Chance of winning the World Cup (%)",
          "scale": {"domain": [0, 40]}},
    "color": {"field": "kind", "type": "nominal",
              "scale": {"domain": ["cited", "model"], "range": ["#5b616e", "#c8102e"]},
              "legend": null}
  },
  "layer": [
    {"mark": {"type": "bar"}},
    {"mark": {"type": "text", "align": "left", "dx": 6, "color": "#1a1a1a"},
     "encoding": {"text": {"field": "pct", "type": "quantitative", "format": ".1f"}}}
  ]
}
```
A vertical rule at `x:23` over the champions chart (below) is a nice alternative
way to show "the model clears the historical bar."

**Optional secondary chart — title concentration (champions by nation):**

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "width": "container", "height": 260,
  "title": "Eight nations, 22 trophies — the World Cup is a repeat business",
  "data": {"values": [
    {"nation": "Brazil", "titles": 5}, {"nation": "Italy", "titles": 4},
    {"nation": "Germany", "titles": 4}, {"nation": "Argentina", "titles": 3},
    {"nation": "Uruguay", "titles": 2}, {"nation": "France", "titles": 2},
    {"nation": "England", "titles": 1}, {"nation": "Spain", "titles": 1}
  ]},
  "encoding": {
    "x": {"field": "nation", "type": "nominal", "sort": "-y", "title": null,
          "axis": {"labelAngle": 0}},
    "y": {"field": "titles", "type": "quantitative", "title": "World Cup titles",
          "axis": {"tickMinStep": 1}},
    "color": {"value": "#c8102e"},
    "tooltip": [{"field": "nation"}, {"field": "titles"}]
  },
  "mark": {"type": "bar"}
}
```
> Data values above are mirrored from `historical_favourites.json`
> (`framing` + `computed_from_table.champions_by_nation`); keep them in sync if the
> table changes. "Germany" = West Germany + Germany merged.

---

## 3. Draft prose (2–3 short paragraphs)

> So the model says Argentina, at **30.8%**, is the team to beat. The instinct that
> follows is almost reflexive: favourites flop. And the history is unkind to
> favourites — by FIFA's own count across the 22 men's World Cups, the
> pre-tournament favourite has lifted the trophy only about **23%** of the time,
> five tournaments out of twenty-two. Since 1966, when pre-tournament odds were
> first recorded, the *shortest-priced* team has gone on to win it just three
> times: West Germany in 1974, Brazil in 1994, Spain in 2010. Backing the favourite
> has, more often than not, been a way to lose money.

> Read against that bar, 30.8% is not the lock it might sound like — but it is not
> timid either. It sits a clear **eight points above** the long-run favourite
> hit-rate. The model is not claiming Argentina is destined to win; it is claiming
> Argentina is a *slightly stronger-than-usual* favourite. The honest translation
> is "more likely than any other single team, and a little more likely than the
> typical favourite — but still odds-against."

> The deeper reason the number stays under one-in-three is that winning a World Cup
> is a closed shop. Only **eight nations** have ever won one, and just **three of
> them** — Brazil, Italy and Germany — account for **13 of the 22 titles**. Even
> home advantage, which sounds decisive, has converted only about **27%** of the
> time (six host winners in twenty-two). In a tournament this concentrated and this
> upset-prone, a transparent model that puts one team near a third of the title
> probability is making a strong call, not a safe one.

---

## 4. Provenance notes (for the later `verify_map`)

Keep the two kinds strictly separate — this is the blog's whole thesis.

| Claim in the prose / chart | Kind | verify_map entry |
|---|---|---|
| 8 distinct champion nations (9 raw labels) | **computed** | **runnable cell** → `build_historical.py` / `computed_from_table.distinct_champion_nations` (cell prints 9 labels, shows the W.Germany→Germany merge → 8) |
| Top-3 nations hold 13/22 = 59% | **computed** | **runnable cell** → `computed_from_table.top3_share` |
| Repeat champions hold 20/22 = 91% | **computed** | **runnable cell** → `computed_from_table.repeat_champions` |
| Host wins 6/22 = 27% | **computed** | **runnable cell** → `computed_from_table.host_wins` |
| Champions-by-nation chart values | **computed** | same cell as above (`champions_by_nation`) |
| **~23% favourite win-rate; 5 of 22; "3 since 1966"** | **cited** | **fact entry** (click-to-source), NOT a cell → `cited_favourite_base_rate` (FIFA primary URL + europeangaming secondary; verbatim quote stored) |
| Argentina 30.8% | **external model output** | already wired to the simulation elsewhere on the page (`ana_01`); restate, do not recompute here. `model_headline` in the JSON is for framing only. |
| Δ = +7.8 pp ("eight points above") | **derived from one computed-elsewhere + one cited number** | label it transparently — it is `30.8 − 23`. Either present as plain arithmetic in the cell, or footnote that one input (30.8) is the model's and one (23) is cited. Do NOT present it as a single "computed-from-table" fact. |

**Hard rule for whoever wires this:** every number that traces back to
`historical_wc_summary.csv` gets a runnable cell (it reproduces); the ~23% does
**not** — it is external and gets a sourced fact entry. Never let the ~23% sit in
a "Run in your browser" cell as if we computed it.
