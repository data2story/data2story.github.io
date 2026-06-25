# Stage-3 build note — "Goals so far" section

**Snapshot:** 2026-06-23 · **Files added:** `code/build_goals.py`, `code/goals_2026.json` (this note: `code/_s3_goals_note.md`).
**Read-only:** `index.html` was NOT edited. Cached source snapshot: `code/_of_2026_raw.json` (openfootball 2026, CC0).

Regenerate: `py build_goals.py` (offline, uses the cache) or `py build_goals.py --refresh` (re-pull openfootball first). Output is deterministic (byte-identical re-runs).

---

## 1. Key numbers

### Golden-boot race (2026 WC, 46 played matches, 139 goal events) — openfootball CC0
Own-goals excluded (credited to the conceding player); ties broken alphabetically.

| # | Player | Team | Goals | Open-play | Pens |
|---|--------|------|------:|----------:|-----:|
| 1 | **Lionel Messi** | Argentina | **5** | 5 | 0 |
| 2 | Erling Haaland | Norway | 4 | 4 | 0 |
| 2 | Kylian Mbappé | France | 4 | 4 | 0 |
| 4 | Deniz Undav | Germany | 3 | 3 | 0 |
| 4 | Jonathan David | Canada | 3 | 3 | 0 |

Messi's 5 = a hat-trick vs Algeria (16 Jun; 17', 60', 76') + a brace vs Austria (22 Jun; 38', 90+5') — **all open play, no penalties**. Top-5 leaders are *all* open-play to date.

### Goals-by-minute (2026 WC, n=139, every goal event incl. pens + own-goals)
15-minute buckets; first-half stoppage (`45+N`) folds into 31-45, second-half stoppage (`90+N`) into the dedicated **90+** bucket.

| Bucket | 1-15 | 16-30 | 31-45 | 46-60 | 61-75 | 76-90 | 90+ |
|--------|-----:|------:|------:|------:|------:|------:|----:|
| Goals  | 17 | 20 | 26 | 21 | 19 | 21 | 15 |
| %      | 12.2 | 14.4 | **18.7** | 15.1 | 13.7 | 15.1 | 10.8 |

- Peak bucket = **31-45** (18.7%) — goals cluster just before half-time.
- **Late drama: 25.9% of 2026 goals arrive from the 76th minute on** (15.1% in 76-90, **10.8% in stoppage time alone**). That's the headline pattern.

### Type split (penalty / open-play / own-goal)
| | Open play | Penalty | Own goal | n |
|---|--------:|--------:|---------:|---:|
| **2026 WC** | **89.2%** (124) | 4.3% (6) | 6.5% (9) | 139 |
| Historical base rate | 91.2% (43,496) | 6.8% (3,253) | 1.9% (927) | 47,676 |

So far in 2026, penalties are *rarer* than the long-run norm (4.3% vs 6.8%) and own-goals **3× more frequent** (6.5% vs 1.9%) — a small-sample quirk worth a hedge in prose.

### Who's scoring (top teams, 2026, own-goals not credited to beneficiary)
Germany 9 · Netherlands 7 · Canada 6 · France 6 · Japan 6 · (then Argentina/Brazil/Switzerland 5).

### Historical minute distribution (context, n=47,420 dated goals)
1-15 13.0% · 16-30 14.7% · 31-45 16.8% · 46-60 16.6% · 61-75 17.0% · **76-90 21.5%** · 90+ 0.5%.
**Caveat for any later comparison:** the historical csv codes almost no goals as `90+` (the old source caps most at minute 90), so its 76-90 bucket (21.5%) effectively absorbs stoppage time. openfootball 2026 codes `90+N` explicitly, hence the richer 2026 90+ bucket (10.8%). Compare *"76th-min-on"* totals (2026 25.9% vs hist 22.0%), not the 90+ buckets directly.

---

## 2. Vega-Lite chart spec sketches

Both are written to route straight through the page's existing `embed(id, spec)` helper (lines ~1950-1978 of `index.html`): it injects `spec.background`, `spec.config` (gold theme: `ACCENT="#c9a227"`, `MUTED`, `LINE`, `INK`, `DOWN="#b9603f"`), measures real container width, and renders SVG with `actions:false`. So **omit `config`/`background`** and keep `"width":"container"` — the helper overwrites `spec.width` per paint. Values below are inlined from `goals_2026.json` (a later stage can swap to a `data.url` load + a verify_map entry).

### (a) Golden-boot bar — `goals_goldenboot_chart`
```js
embed("goals_goldenboot_chart", {
  "$schema":"https://vega.github.io/schema/vega-lite/v5.json",
  "width":"container","height":260,
  "title":"2026 World Cup golden boot — goals so far (as of 23 Jun)",
  "data":{"values":[
    {"player":"Lionel Messi","team":"Argentina","goals":5},
    {"player":"Erling Haaland","team":"Norway","goals":4},
    {"player":"Kylian Mbappé","team":"France","goals":4},
    {"player":"Deniz Undav","team":"Germany","goals":3},
    {"player":"Jonathan David","team":"Canada","goals":3}
  ]},
  "encoding":{
    "y":{"field":"player","type":"nominal","sort":"-x","title":null},
    "x":{"field":"goals","type":"quantitative","title":"goals",
         "axis":{"tickMinStep":1}},
    "color":{"condition":{"test":"datum.player === 'Lionel Messi'","value":ACCENT},
             "value":"#5b616e"},
    "tooltip":[{"field":"player"},{"field":"team"},{"field":"goals"}]
  },
  "layer":[
    {"mark":{"type":"bar"}},
    {"mark":{"type":"text","align":"left","dx":4,"color":INK,"font":"system-ui"},
     "encoding":{"text":{"field":"goals"}}}
  ]
});
```
*(Messi highlighted in ACCENT gold; rest muted grey — matches the page's "one hero" visual convention.)*

### (b) Goals-by-minute — `goals_byminute_chart`
```js
embed("goals_byminute_chart", {
  "$schema":"https://vega.github.io/schema/vega-lite/v5.json",
  "width":"container","height":260,
  "title":"When 2026 World Cup goals are scored (n=139)",
  "data":{"values":[
    {"bucket":"1-15","goals":17,"pct":12.2},
    {"bucket":"16-30","goals":20,"pct":14.4},
    {"bucket":"31-45","goals":26,"pct":18.7},
    {"bucket":"46-60","goals":21,"pct":15.1},
    {"bucket":"61-75","goals":19,"pct":13.7},
    {"bucket":"76-90","goals":21,"pct":15.1},
    {"bucket":"90+","goals":15,"pct":10.8}
  ]},
  "encoding":{
    "x":{"field":"bucket","type":"ordinal","title":"minute",
         "sort":["1-15","16-30","31-45","46-60","61-75","76-90","90+"],
         "axis":{"labelAngle":0}},
    "y":{"field":"goals","type":"quantitative","title":"goals"},
    "color":{"condition":{"test":"datum.bucket === '90+'","value":ACCENT},"value":"#5b616e"},
    "tooltip":[{"field":"bucket","title":"minute"},{"field":"goals"},
               {"field":"pct","title":"% of goals"}]
  },
  "mark":{"type":"bar"}
});
```
*(Stoppage-time `90+` bar highlighted to underline the "late drama" line. Optional: overlay a `rule` mark with the historical 76-90 share for a base-rate reference, but mind the 90+ coding caveat above — safest to annotate, not overlay.)*

Needs two empty mount points in the body, e.g.
`<div id="goals_goldenboot_chart" class="chart-container"></div>` and
`<div id="goals_byminute_chart" class="chart-container"></div>` (a later stage adds these; this note does not touch `index.html`).

---

## 3. Draft prose (plain factual — voice to be polished later)

> **The race for the Golden Boot.** With the group stage all but done, Lionel Messi leads the 2026 World Cup scoring chart on five goals — a hat-trick against Algeria and a brace against Austria, every one of them from open play. Erling Haaland and Kylian Mbappé sit a goal back on four apiece, with Germany's Deniz Undav and Canada's Jonathan David on three. None of the front-runners has yet scored from the penalty spot.

> **Goals arrive late.** Across the 139 goals scored so far, the busiest single window is the closing minutes before half-time, but the more striking pattern is at the other end of the clock: better than one in four goals (25.9%) has come from the 76th minute on, and one in nine has landed in stoppage time. Messi's own fifth goal — in the 95th minute against Austria — fits the trend.

> **How the goals are scored.** This tournament has leaned heavily on open play: 89% of goals have come from the run of play, against just 4% from penalties — a touch below the long-run international rate. Own goals have been unusually common at 6.5% of all goals, roughly three times their historical share, though with only 139 goals on the board that gap may yet narrow.

*(All three paragraphs are fully backed by `goals_2026.json`; keep the small-sample hedge in §3's last line.)*

---

## 4. GIF embed plan (demo-only — broadcast-rights-encumbered; accepted stance)

**Honesty caveat (load-bearing):** GIPHY/Tenor surface mostly older / generic football footage. None of the GIFs below is verified to be *2026-match* footage — the clearly-dated one is **2022 World Cup**. Caption them as celebration/atmosphere clips, NOT as "Messi vs Algeria 2026". All direct URLs were HEAD/GET-checked on 2026-06-23 and returned `200 image/gif`. Mandatory attribution string must remain visible per each platform's terms.

| # | Source | Direct embed URL (verified 200) | Source page | Depicts | Attribution (mandatory) |
|---|--------|----------------------------------|-------------|---------|--------------------------|
| G1 | **Tenor** | `https://media.tenor.com/Zynln6qf060AAAAC/goal-messi-world-cup-2022.gif` (HD, ~3.3 MB) · lighter `…AAAAM/…` (~366 KB) | `https://tenor.com/view/goal-messi-world-cup-2022-messi-world-cup-gif-7433725133876876205` | Argentina jersey, "GOAAAAL" celebration (**WC 2022**) | **Via Tenor** |
| G2 | **GIPHY** (FIFA official `@fifa`) | `https://media.giphy.com/media/KH7V8W7fQqCrQoiPYP/giphy.gif` (~4.6 MB) | `https://giphy.com/gifs/fifa-messi-lionel-goal-KH7V8W7fQqCrQoiPYP` | FIFA World Cup goal/celebration, tagged #argentina #messi | **Powered by GIPHY** |
| G3 | **GIPHY** (`@Messifutt10`) | `https://media.giphy.com/media/dl6vzqmawrziEY0D0W/giphy.gif` (~2.3 MB) | `https://giphy.com/gifs/messi-world-cup-wc-ronaldo-dl6vzqmawrziEY0D0W` | Messi World Cup montage (year unspecified) | **Powered by GIPHY** |

GIPHY direct-URL pattern is deterministic: `https://media.giphy.com/media/{ID}/giphy.gif` (also `https://i.giphy.com/{ID}.gif`). Tenor sizes: `…AAAAC` = HD, `…AAAAM` = medium, `…AAAAS` = tiny — pick by weight.

**Recommended use:** G1 (clearly a goal celebration) as the section's lead atmosphere GIF; G2 (official FIFA channel — best provenance) as a secondary. Lazy-load (`loading="lazy"`) given 2-5 MB each. Suggested markup pattern (for a later stage; do NOT add to index.html now):
```html
<figure class="goal-gif">
  <img loading="lazy" src="https://media.tenor.com/Zynln6qf060AAAAM/goal-messi-world-cup-2022.gif"
       alt="Argentina goal celebration (World Cup 2022)">
  <figcaption>Goal celebration, World Cup 2022 — demo clip.
    <a href="https://tenor.com/view/goal-messi-world-cup-2022-messi-world-cup-gif-7433725133876876205">Via Tenor</a>
  </figcaption>
</figure>
```

---

## 5. Provenance notes (for a later verify_map + runnable cell)

Every number traces to one of two sources; the runnable cell can be `code/build_goals.py` itself (offline-deterministic against the committed `_of_2026_raw.json` cache).

| Claim in prose / chart | Computed from | How |
|---|---|---|
| Messi 5 / Haaland 4 / Mbappé 4 / Undav 3 / David 3 | `_of_2026_raw.json` (openfootball CC0) | `build_goals.top_scorers()` — count `goals1`/`goals2` `name` per (player, team), own-goals excluded |
| Messi: hat-trick vs Algeria (17/60/76'), brace vs Austria (38/90+5') | same | match-level goal arrays; minutes verbatim from source |
| 139 goal events / 46 played matches | same | matches with a `score.ft`; flattened `goals1`+`goals2` |
| Goals-by-minute buckets (incl. 90+ = 10.8%, 76th-on = 25.9%) | same | `build_goals.minute_distribution()` + `bucket_for()` (folds `45+N`→31-45, `90+N`→90+) |
| Type split 89.2% / 4.3% / 6.5% | same | `build_goals.type_split()` reads `penalty` / `owngoal` flags |
| Team tally (Germany 9 …) | same | `build_goals.team_tally()` |
| Historical base rate 91.2% / 6.8% / 1.9% and hist minute dist | `phase2/datasets/worldcup_2026/raw/goalscorers.csv` (47,676 rows, READ-ONLY) | `build_goals.historical_base_rate()` — `TRUE/FALSE` → bool; float minutes coerced; ~256 NaN minutes dropped from the minute total |
| GIF clips | Tenor / GIPHY (see §4) | direct media URLs, HEAD/GET 200 on 2026-06-23; demo-only, attribution kept |

**Reproducibility statement for the verify cell:** `goals_2026.json` is regenerated byte-for-byte by `py build_goals.py` from `_of_2026_raw.json` (committed snapshot) + the shared `goalscorers.csv`. Re-run SHA-256 is stable (`1fc7cb65…`). The `--refresh` flag re-pulls the live openfootball URL and (as of 2026-06-23) reproduces the same snapshot bytes.
