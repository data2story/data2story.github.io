/**
 * Data2Story client models -- Cape Verde: the diaspora nation.
 * Pure JS, zero dependencies, all constants inlined. Everything here is the
 * SAME model / SAME data that produced the published headline numbers
 * (fit_outcome_model.py ana_19; squad_analysis.py ana_09/ana_10), so a live
 * widget recomputes the prose figures exactly.
 *
 * cm_01  matchOdds(rA, rB, aHome)      -- Elo ordered-logit win/draw/loss
 * cm_02  squadTally(countries)         -- squad-builder born-abroad numbers
 *
 * Baselines (untouched widgets must show these):
 *   capeVerdeVsArgentina() -> { win: 3.4, draw: 8.3, loss: 88.3, advance: 7.6 }
 *   squadTally()           -> { players: 15, caps: 414, goals: 33,
 *                               playersPct: 57.7, capsPct: 50.3, goalsPct: 44.0 }
 */

// ---- cm_01: symmetric Elo ordered-logit match-outcome model ---------------
// Fitted on 30,195 internationals 1990-2026 (both teams >=30 prior matches);
// out-of-sample Brier 18.8% better than base rates (fit_outcome_model.py ana_20).
// u = B * ((rA - rB)/SCALE + H*homesign);  homesign: +1 A home, -1 B home, 0 neutral
// P(A wins) = 1 - sigmoid(C - u);  P(A loses) = sigmoid(-C - u);  draw = rest.
// Thresholds are symmetric (+C/-C), so neutral-venue odds don't depend on
// which team is listed first. Fitted home shift H = 0.2965*400 = 119 Elo pts.
const ORDERED_LOGIT = { C: 0.6614, B: 2.0468, H: 0.2965, SCALE: 400 };

// Elo ratings AFTER the 2026 group stage (matches through 2026-06-27), i.e.
// pre-Round-of-32, for all 32 knockout teams. Engine: elo_ratings.py run_elo
// (K 60/50/40/30/20, goal-diff multiplier, +100 home advantage, start 1500).
const RATINGS_PRE_R32 = {
  "Argentina": 2225.0, "Spain": 2208.8, "France": 2186.3, "England": 2108.0,
  "Brazil": 2095.0, "Colombia": 2087.6, "Portugal": 2055.5, "Netherlands": 2047.5,
  "Morocco": 2022.9, "Mexico": 2016.6, "Germany": 1997.3, "Japan": 1994.7,
  "Ecuador": 1994.0, "Switzerland": 1984.5, "Norway": 1982.4, "Croatia": 1969.6,
  "Belgium": 1963.3, "Australia": 1912.5, "Senegal": 1905.2, "Austria": 1904.6,
  "Paraguay": 1902.5, "Algeria": 1890.2, "United States": 1878.9, "Ivory Coast": 1863.3,
  "Egypt": 1860.2, "Canada": 1855.3, "DR Congo": 1819.7, "Sweden": 1809.8,
  "South Africa": 1712.9, "Cape Verde": 1701.6, "Bosnia and Herzegovina": 1690.3,
  "Ghana": 1687.5,
};

const sigmoid = (z) => 1 / (1 + Math.exp(-z));

/** Win/draw/loss probabilities (percent, 1 dp) from team A's perspective.
 *  homesign: +1 if A has real home advantage, -1 if B does, 0 neutral (all
 *  WC2026 venues in the dataset are neutral). For a knockout tie, `draw`
 *  reads as "level after 90 minutes -> extra time". */
function matchOdds(rA, rB, homesign = 0) {
  const { C, B, H, SCALE } = ORDERED_LOGIT;
  const u = B * ((rA - rB) / SCALE + H * homesign);
  const sHi = sigmoid(C - u), sLo = sigmoid(-C - u);
  const r1 = (p) => Math.round(p * 1000) / 10;
  const win = r1(1 - sHi), draw = r1(sHi - sLo), loss = r1(sLo);
  // advance = win + half of draws (treats ET+shootout as a coin flip; stated assumption)
  const advance = Math.round((1 - sHi + 0.5 * (sHi - sLo)) * 1000) / 10;
  return { win, draw, loss, advance };
}

/** The headline: Cape Verde vs Argentina, Miami, 2026-07-03 (neutral). */
function capeVerdeVsArgentina() {
  return matchOdds(RATINGS_PRE_R32["Cape Verde"], RATINGS_PRE_R32["Argentina"], 0);
}

// ---- cm_02: squad-builder (2026 squad by birth country) -------------------
// From squad_2026.csv via squad_analysis.py (ana_09/ana_10). caps/goals are
// career totals at squad announcement. Total squad: 26 players, 823 caps, 75 goals.
const SQUAD_TOTALS = { players: 26, caps: 823, goals: 75 };
const SQUAD_BIRTH = {
  "Cape Verde":    { players: 11, caps: 409, goals: 42, abroad: false },
  "Netherlands":   { players: 6,  caps: 202, goals: 26, abroad: true },
  "Portugal":      { players: 4,  caps: 80,  goals: 4,  abroad: true },
  "France":        { players: 3,  caps: 86,  goals: 3,  abroad: true },
  "Ireland":       { players: 1,  caps: 45,  goals: 0,  abroad: true },
  "United States": { players: 1,  caps: 1,   goals: 0,  abroad: true },
};

/** Tally players/caps/goals for a set of birth countries (default: all five
 *  born-abroad countries). Percentages are of the whole 26-man squad, 1 dp. */
function squadTally(countries) {
  const keys = countries ||
    Object.keys(SQUAD_BIRTH).filter((k) => SQUAD_BIRTH[k].abroad);
  const t = { players: 0, caps: 0, goals: 0 };
  for (const k of keys) {
    const c = SQUAD_BIRTH[k];
    if (!c) continue;
    t.players += c.players; t.caps += c.caps; t.goals += c.goals;
  }
  const pct = (a, b) => Math.round((a / b) * 1000) / 10;
  return { ...t, playersPct: pct(t.players, SQUAD_TOTALS.players),
           capsPct: pct(t.caps, SQUAD_TOTALS.caps),
           goalsPct: pct(t.goals, SQUAD_TOTALS.goals) };
}

// UMD-ish export so the Programmer can inline or import this file as-is.
if (typeof module !== "undefined") {
  module.exports = { ORDERED_LOGIT, RATINGS_PRE_R32, SQUAD_TOTALS, SQUAD_BIRTH,
                     matchOdds, capeVerdeVsArgentina, squadTally };
}
