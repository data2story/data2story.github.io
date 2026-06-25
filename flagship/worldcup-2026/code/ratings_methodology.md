# Player Ratings — Methodology & Provenance

**Output:** `code/ratings.json` — EA-style 0–99 cards for 38 marquee players across the
forecast's top teams.
**Builder:** `code/build_ratings.py` (deterministic; re-run with
`PYTHONUTF8=1 python code/build_ratings.py`).
**Per-player raw inputs (audit trail):** `code/_sb_player_raw.json` — every per-90 metric
that feeds a StatsBomb card.

This page's thesis is that **every number is traceable to its inputs**. These cards are
not FIFA/EA's proprietary ratings and not reputation scores. Each one is computed from
named public data by the formulas below. No attribute value is ever hand-set or invented:
if the data to support a value is missing, the player is dropped to the weaker lineage or
excluded — never guessed.

---

## 1. Two data lineages, one shared 0–99 scale

Each card records `provenance`:

| lineage | who | what it's built from |
|---|---|---|
| `statsbomb` | 30 players who appear in StatsBomb Open Data for **UEFA Euro 2024** or **Copa América 2024** | per-90 event metrics aggregated from the raw event feed |
| `public_index` | 8 stars **outside** that coverage (Norway, USA, Mexico, Morocco, Japan) | international goals + team squad value + a documented position archetype |

The two lineages produce different *raw* numbers, so they are made comparable by ranking
**every player in the pool together** on each attribute and mapping to one 50–99 band
(Section 4). That shared percentile step is what lets a StatsBomb card and a public-index
card sit side by side honestly.

**Split:** 30 `statsbomb` / 8 `public_index` (of 38). One targeted player, **Cole Palmer**,
logged only 88 sub minutes at Euro 2024 — below the 180-minute stability gate — and was
**dropped rather than estimated**.

---

## 2. The six attributes (EA-style) + Overall

`pace, shooting, passing, dribbling, defending, physical`, plus a position-weighted
`overall`. `pace` carries `"is_proxy": true` on every card (Section 5).

### 2a. StatsBomb lineage — raw attribute formulas

All inputs are per-90 values from a player's Euro 2024 / Copa 2024 minutes
(`code/_sb_player_raw.json`). Non-penalty (np) shooting only; penalties excluded.

```
shooting  = 0.45·npxg/90 + 0.35·np_goals/90 + 0.20·(np_shots/90 ÷ 4)
passing   = 0.40·pass_completion% + 0.35·(xA/90 ÷ 0.3) + 0.25·(progressive_passes/90 ÷ 8)
dribbling = 0.45·(take_ons/90 · take_on_success%) + 0.30·(progressive_carries/90 ÷ 8)
                                                   + 0.25·take_on_success%
defending = 0.55·POSITION_DEFENSIVE_PRIOR
          + 0.45·[0.45·((tackles+interceptions)/90 ÷ 4) + 0.30·(pressures/90 ÷ 20)
                                                         + 0.25·(recoveries/90 ÷ 8)]
physical  = 0.40·aerial_win% + 0.25·(aerial_duels/90 ÷ 4) + 0.20·(recoveries/90 ÷ 8)
                                                          + 0.15·((height_cm − 165) ÷ 30)
pace      = 0.55·POSITION_PACE_PRIOR + 0.45·(progressive_carry_distance/90 ÷ 250)   [PROXY]
```

How each StatsBomb metric is derived from the raw event feed:

- **npxg/90, np_goals/90, np_shots/90** — `Shot` events with `shot.type ≠ "Penalty"`;
  `statsbomb_xg` summed; goals where `shot.outcome = "Goal"`.
- **pass_completion%** — `Pass` events; a pass is complete when it has **no** `pass.outcome`
  (StatsBomb records an outcome only on failure).
- **xA/90** — exact pass→shot linkage: for each `Shot`, its `shot.key_pass_id` is matched
  back to the passer, who is credited that shot's `statsbomb_xg`. (Not a coarse "assists"
  count.)
- **progressive_passes/90** — passes advancing the ball ≥15 m toward goal and ending at
  pitch-x ≥ 60.
- **take_ons/90, take_on_success%** — `Dribble` events; success where
  `dribble.outcome = "Complete"`.
- **progressive_carries/90, progressive_carry_distance/90** — `Carry` events advancing
  pitch-x ≥ 5 m; distance = forward x-gain.
- **(tackles+interceptions)/90, pressures/90, recoveries/90** — `Duel`(Tackle),
  `Interception`, `Pressure`, `Ball Recovery` events.
- **aerial_win%, aerial_duels/90** — aerial **wins** counted from the `aerial_won` flag on
  `Clearance`/`Shot`/`Pass`/`Miscontrol`; aerial **losses** from `Duel`(Aerial Lost).

**Why `defending` and `pace` blend in a position prior.** The pool is attacker-heavy, so
ranking raw defensive *workrate* alone made high-pressing wingers out-"Defend" centre-backs
(elite CBs intercept and position rather than rack up tackles), and ranking ball-carry
distance alone made non-carrying box strikers read "slow". For these two role-sensitive
attributes only, the data signal is blended with a documented per-position prior
(`ARCH[position]` in the builder) so the value reflects role while still moving with the
data. `shooting`, `passing`, `dribbling`, `physical` are **purely data-driven** (no
archetype mixed in; height is a recorded fact, not a prior).

### 2b. public_index lineage — formula

For players with no StatsBomb coverage, start from a documented position archetype and tilt
it by the only player-level / team-level signals available:

```
base[attr] = ARCH[position][attr]                       # documented 0–1 prior per position
base      ·= 0.92 + 0.16·value_norm                     # team squad-value tilt  (weak proxy)
base[shooting] ·= 0.90 + min(0.22, 0.06·√(intl_goals)/3)   if goals>0 else ·0.85
base[physical] = 0.7·base[physical] + 0.3·((height_cm−165)/30)
```

- **intl_goals** — count of that player's goals for their nation in
  `datasets/raw/goalscorers.csv` (recorded in each card's `source_refs`). This is the one
  *player-level* signal; it tilts **shooting only**. (A pure creator such as Ødegaard has 0
  goals there — expected; the archetype carries his passing/dribbling.)
- **value_norm** — the player's **team** squad market value from
  `reference/squad_values.csv`, min–max normalized across the 48 squads. This is a
  **team-level proxy, not a player-level value**, and is labelled as such on every
  public-index card. A player-level Transfermarkt mirror (Kaggle `davidcariboo/player-scores`)
  was the preferred source but was not pulled for this build; the team-value proxy is the
  documented fallback.

`ARCH` position priors (raw 0–1, before tilts) are listed verbatim in `build_ratings.py`.

### 2c. Overall

Position-weighted blend of the six **scaled** attributes:

```
overall = Σ_attr  scaled_attr · POS_WEIGHTS[position][attr]      (weights sum to 1.0)
```

`POS_WEIGHTS` (e.g. ST shooting 0.34, CB defending 0.40, W dribbling 0.26) are listed in
full in `build_ratings.py`.

---

## 3. What the StatsBomb numbers mean (and don't)

A `statsbomb` card reflects **only that player's Euro 2024 / Copa 2024 minutes** — a single
tournament, small samples (a 180-minute floor, most players 4–7 matches). So tournament form
shows through: a player who under-performed his club reputation that summer reads lower here,
and a Golden-Boot run reads higher. That is the point — the number traces to the matches we
aggregated, not to a reputation. Examples that audit out cleanly:

- **Lautaro Martínez** SHO 99 ← 5 non-penalty goals in 11 shots at Copa 2024 (his
  Golden-Boot tally; independently re-counted from the raw events).
- **James Rodríguez** PAS 99 ← 0.38 xA/90, the tournament's top creator.
- **Lamine Yamal** SHO 75 ← 1 goal from 18 shots (low conversion as a teenage wide creator),
  but PAS 95 from 0.37 xA/90.

---

## 4. Normalization — percentile rank → 50–99 band

For each of the six attributes independently:

1. Pool **all 38 players** (both lineages) on that attribute's raw value.
2. Compute each player's **percentile rank** (ties share the average rank).
3. Map percentile *p* ∈ [0,1] linearly to **`50 + 49·p`**, rounded to an integer.

So within this pool the weakest on an attribute = 50, the strongest = 99, the median ≈ 74.
This is a **relative ranking inside this 38-player elite pool**, not an absolute scale — a
50 means "lowest among these stars on this metric", not "poor footballer". Overall is then
the position-weighted blend of the six scaled values, so it lands in a similar band
(observed range 64–88).

---

## 5. The Pace proxy (flagged)

There is **no clean pace/sprint-speed source** in any of these feeds. `pace` is therefore a
**proxy** and every card marks `attributes.pace.is_proxy = true`:

- `statsbomb`: progressive ball-carry **distance** per 90 (how far a player drives with the
  ball), blended 45/55 with the position pace prior.
- `public_index`: the position pace prior, tilted by team value.

Carry-distance correlates with but is **not** top speed — it under-rates pure box poachers
who score without carrying (e.g. a target striker) and over-rates deep carriers. Read `pace`
as "on-ball forward drive / role-typical speed", and treat it as the softest number on the
card.

---

## 6. Sources, licences & attribution

| source | used for | licence / status |
|---|---|---|
| **StatsBomb Open Data** — `github.com/statsbomb/open-data` (UEFA Euro 2024 `competition_id=55, season_id=282`; Copa América 2024 `competition_id=223, season_id=282`) | all `statsbomb` per-90 metrics | Free for **non-commercial** use under the **StatsBomb Open Data User Agreement**. **Attribution + the StatsBomb logo are required** wherever these data are shown. |
| `datasets/raw/goalscorers.csv` (international goals, via the public men's-international results dataset) | `public_index` shooting tilt | CC0 / public-domain factual data |
| `datasets/reference/squad_values.csv` (Transfermarkt squad values via PlanetFootball, snapshot 2026-06-14) | `public_index` team-value proxy | factual figures, attribution requested; **team-level**, used as a stated proxy |
| `datasets/forecast_outputs/champion_odds.csv` (this project's Elo→Poisson→Monte-Carlo model) | `team_p_reach_sf`, `team_p_champion` on each card | this project |
| Player age / club / position / height | card labels; height feeds the Physical term | editorial facts, recorded per card |

### Required when these cards are published

> **Data provided by StatsBomb.** Player event metrics for the `statsbomb`-lineage cards are
> derived from **StatsBomb Open Data** (UEFA Euro 2024, Copa América 2024) and are used under
> the StatsBomb Open Data User Agreement for **non-commercial** purposes.
> **The StatsBomb logo must be displayed** alongside any visualization built on these data.

(The logo ships in the StatsBomb open-data repo under `img/`/`logos/`; place it on or beside
the player-cards section.) International-goal and squad-value figures are credited to their
sources in the table above; each card's `source_refs[]` names the exact inputs used.

---

## 7. `ratings.json` schema

```jsonc
{
  "name": "Lautaro Martínez",
  "team": "Argentina",
  "position": "ST",            // GK/CB/FB/DM/CM/AM/W/ST
  "age": 28,
  "club": "Inter Milan",       // plain text
  "overall": 74,
  "attributes": {
    "pace":      { "value": 54, "is_proxy": true },   // proxy flag on pace only
    "shooting":  { "value": 99 },
    "passing":   { "value": 50 },
    "dribbling": { "value": 55 },
    "defending": { "value": 83 },
    "physical":  { "value": 75 }
  },
  "provenance": "statsbomb",                          // or "public_index"
  "source_refs": [ /* exact competitions / inputs used for THIS player */ ],
  "team_p_reach_sf": 0.5705,                          // for the stars-vs-deep-run chart
  "team_p_champion": 0.2631,
  "statsbomb_minutes": 224.7                          // present on statsbomb cards only
}
```

`team_p_reach_sf` and `team_p_champion` come straight from `champion_odds.csv`, so the
"stars vs deep-run" chart plots a player's individual rating against their team's simulated
tournament ceiling.

---

## 8. Reproduce

```bash
PYTHONUTF8=1 python code/build_ratings.py
```

The script fetches StatsBomb match/lineup/event JSON on demand (cached locally during a run,
then discarded), aggregates the per-90 metrics, joins the public CSVs, normalizes, and writes
`code/ratings.json` + `code/_sb_player_raw.json`. Deterministic: same inputs → same cards.
