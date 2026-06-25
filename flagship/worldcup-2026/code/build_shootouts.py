"""
build_shootouts.py - quantify how much knockout football is a coin flip.

The forecast model resolves knockout ties ANALYTICALLY: when a simulated match is
level after 90', it assigns the winner from a single win-probability split (see
simulate.py) rather than playing out extra time and penalties kick-by-kick. This
script turns that documented caveat into a verifiable sidebar by measuring, from
677 historical international penalty shootouts (martj42 dataset), how predictable
shootouts actually are.

Three coin-flip checks, each with a simple, honest, reproducible definition:

  1. FIRST-SHOOTER advantage - win rate of the team that took the first kick
     (directly in the data; populated for 256 of 677 shootouts).
  2. FAVOURITE (better team) - win rate of the higher-Elo side, where Elo is
     computed from the full international history STRICTLY BEFORE each shootout's
     date (same eloratings.net rule as the forecast's elo.py; leak-free). This is
     the headline "does the better team win the shootout?" test.
  3. WORLD-CUP subset - the 35 shootouts at the men's FIFA World Cup finals
     (1982-2022), tagged by joining to intl_results_history.csv on date + teams.

Everything is a deterministic function of the two input CSVs - no randomness.

Run:  py build_shootouts.py   ->  writes ../code/shootouts_stats.json
"""
import sys, json
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from math import comb
from pathlib import Path
from collections import defaultdict
import pandas as pd

# Reuse the forecast's own Elo machinery so the "favourite" is defined by the
# exact same rule the rest of the blog uses (no second, divergent Elo).
from elo import load_history, importance, gd_multiplier, BASE, HOME_ADV

HERE = Path(__file__).resolve().parent
SHOOTOUTS = Path(r"D:/AI/journalist agent review/phase2/datasets/worldcup_2026/raw/shootouts.csv")
HIST = HERE.parent / "intl_results_history.csv"     # same file elo.py trains on


# ---------- small stats helpers (exact, dependency-light) ----------
def binom_two_sided_p(k: int, n: int, p: float = 0.5) -> float:
    """Exact two-sided binomial p-value for k successes in n trials under H0: p."""
    pr = [comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    pk = pr[k]
    return float(sum(x for x in pr if x <= pk + 1e-15))


def wilson_ci(k: int, n: int, z: float = 1.96):
    """95% Wilson score interval for a proportion (handles small n / extremes)."""
    p = k / n
    d = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return [round((centre - half) * 100, 1), round((centre + half) * 100, 1)]


def expected_win_prob_from_elo_gap(gap: float, home_adv: float = 0.0) -> float:
    """Regulation (non-shootout) win expectation of the favourite given an Elo gap,
    via the eloratings logistic. Used only for the 'on paper they should win' contrast."""
    return 1.0 / (1.0 + 10.0 ** (-(abs(gap) + home_adv) / 400.0))


def rate(k: int, n: int) -> dict:
    """Bundle a proportion with its CI + two-sided coin-flip p-value."""
    return {
        "won": int(k), "n": int(n),
        "pct": round(k / n * 100, 1),
        "ci95_pct": wilson_ci(k, n),
        "p_vs_50": round(binom_two_sided_p(k, n), 4),
    }


def elo_as_of_each_shootout(sh: pd.DataFrame) -> pd.DataFrame:
    """Attach elo_home / elo_away = each team's Elo from all internationals STRICTLY
    BEFORE the shootout's date (one forward sweep through history; O(H + S))."""
    hist = load_history()  # all matches, no cutoff, date-sorted, scores int
    H = hist.sort_values("date", kind="stable").reset_index(drop=True)
    h_home = H["home_team"].tolist(); h_away = H["away_team"].tolist()
    h_hs = H["home_score"].tolist(); h_as = H["away_score"].tolist()
    h_tour = H["tournament"].tolist(); h_neu = H["neutral"].tolist(); h_date = H["date"].tolist()
    nH = len(H)

    ratings = defaultdict(lambda: BASE)
    sh = sh.sort_values("date", kind="stable").reset_index(drop=True)
    elo_h, elo_a = [], []
    hi = 0
    for _, r in sh.iterrows():
        sdate = r["date"]
        while hi < nH and h_date[hi] < sdate:        # consume matches before this shootout
            rh, ra = ratings[h_home[hi]], ratings[h_away[hi]]
            hadv = 0.0 if bool(h_neu[hi]) else HOME_ADV
            we = 1.0 / (1.0 + 10.0 ** (-((rh + hadv) - ra) / 400.0))
            w = 1.0 if h_hs[hi] > h_as[hi] else (0.5 if h_hs[hi] == h_as[hi] else 0.0)
            delta = importance(h_tour[hi]) * gd_multiplier(h_hs[hi] - h_as[hi]) * (w - we)
            ratings[h_home[hi]] = rh + delta
            ratings[h_away[hi]] = ra - delta
            hi += 1
        elo_h.append(ratings[r["home_team"]])
        elo_a.append(ratings[r["away_team"]])
    sh["elo_home"] = elo_h
    sh["elo_away"] = elo_a
    sh["elo_diff"] = sh["elo_home"] - sh["elo_away"]      # >0 => listed-first team favoured
    return sh


def tag_tournament(sh: pd.DataFrame) -> pd.DataFrame:
    """Recover each shootout's competition by joining to history on (date, {teams})."""
    hist = pd.read_csv(HIST, encoding="utf-8")
    idx = {}
    for d, ht, at, tour in zip(hist["date"], hist["home_team"], hist["away_team"], hist["tournament"]):
        idx.setdefault((d, frozenset((ht, at))), tour)
    sh["tournament"] = [idx.get((d, frozenset((h, a))))
                        for d, h, a in zip(sh["date"], sh["home_team"], sh["away_team"])]
    return sh


def main():
    sh = pd.read_csv(SHOOTOUTS, encoding="utf-8")
    # integrity guards: winner & first_shooter (when present) must be one of the two sides
    assert ((sh["winner"] == sh["home_team"]) | (sh["winner"] == sh["away_team"])).all(), "winner not a participant"
    fs_all = sh[sh["first_shooter"].notna()]
    assert ((fs_all["first_shooter"] == fs_all["home_team"]) |
            (fs_all["first_shooter"] == fs_all["away_team"])).all(), "first_shooter not a participant"

    sh = tag_tournament(sh)
    sh = elo_as_of_each_shootout(sh)
    sh["year"] = pd.to_datetime(sh["date"]).dt.year
    n = len(sh)

    # ---- 1. first-shooter advantage (overall) ----
    fs = sh[sh["first_shooter"].notna()]
    first_shooter = rate(int((fs["first_shooter"] == fs["winner"]).sum()), len(fs))

    # ---- 2. favourite (higher pre-match Elo) ----
    fav_win = int((((sh["elo_diff"] > 0) & (sh["winner"] == sh["home_team"])) |
                   ((sh["elo_diff"] < 0) & (sh["winner"] == sh["away_team"]))).sum())
    # elo_diff is essentially never exactly 0 (continuous), so all n have a defined favourite
    n_tie = int((sh["elo_diff"] == 0).sum())
    favourite = rate(fav_win, n - n_tie)
    favourite["mean_abs_elo_gap"] = round(float(sh["elo_diff"].abs().mean()), 1)
    favourite["median_abs_elo_gap"] = round(float(sh["elo_diff"].abs().median()), 1)
    # what that mean gap "should" buy the favourite in regulation (the contrast)
    favourite["expected_pct_in_regulation"] = round(
        expected_win_prob_from_elo_gap(sh["elo_diff"].abs().mean()) * 100, 1)

    # robustness: restrict to clearer mismatches
    fav_by_gap = []
    for thr in (0, 25, 50, 100, 150):
        sub = sh[sh["elo_diff"].abs() >= thr]
        kk = int((((sub["elo_diff"] > 0) & (sub["winner"] == sub["home_team"])) |
                  ((sub["elo_diff"] < 0) & (sub["winner"] == sub["away_team"]))).sum())
        fav_by_gap.append({
            "min_abs_elo_gap": thr, "n": len(sub),
            "fav_win_pct": round(kk / len(sub) * 100, 1),
            "fav_expected_pct_regulation": round(
                expected_win_prob_from_elo_gap(sub["elo_diff"].abs().mean()) * 100, 1),
        })

    # ---- 3. listed-first ("home") team (confounded by venue; labelled as such) ----
    home_team_rate = rate(int((sh["winner"] == sh["home_team"]).sum()), n)

    # ---- 4. World Cup men's finals subset ----
    wc = sh[sh["tournament"] == "FIFA World Cup"].copy()      # excludes qualifiers + non-FIFA "Viva/CONIFA" cups
    wc_fs = wc[wc["first_shooter"].notna()]
    wc_fav = int((((wc["elo_diff"] > 0) & (wc["winner"] == wc["home_team"])) |
                  ((wc["elo_diff"] < 0) & (wc["winner"] == wc["away_team"]))).sum())
    world_cup = {
        "n": len(wc),
        "date_range": [wc["date"].min(), wc["date"].max()],
        "editions": {int(k): int(v) for k, v in wc["year"].value_counts().sort_index().items()},
        "first_shooter": rate(int((wc_fs["first_shooter"] == wc_fs["winner"]).sum()), len(wc_fs)),
        "favourite": rate(wc_fav, len(wc)),
        "examples": [
            {"date": r["date"], "home": r["home_team"], "away": r["away_team"],
             "winner": r["winner"], "first_shooter": r["first_shooter"]}
            for _, r in wc[wc["date"].isin(["1990-07-04", "2006-07-09", "2022-12-18"])].iterrows()
        ],
    }

    # ---- 5. frequency over time (for the trend chart) ----
    by_decade = {int(d): int(c) for d, c in
                 (sh["year"] // 10 * 10).value_counts().sort_index().items()}
    by_year = {int(y): int(c) for y, c in sh["year"].value_counts().sort_index().items()}

    out = {
        "meta": {
            "source": "shootouts.csv (martj42 international football results) + intl_results_history.csv",
            "total_shootouts": n,
            "date_range": [sh["date"].min(), sh["date"].max()],
            "as_of": "2026-06-24",
            "what_this_measures": (
                "How predictable penalty shootouts are - the part of knockout football the "
                "forecast model resolves analytically (a single win-probability split) instead "
                "of simulating kick-by-kick. Each metric reports the favoured side's win rate "
                "with a 95% Wilson CI and a two-sided binomial p-value against a 50/50 coin flip."),
        },
        "first_shooter": first_shooter,
        "favourite": favourite,
        "favourite_by_elo_gap": fav_by_gap,
        "listed_first_team": {
            **home_team_rate,
            "_caveat": ("'home_team' is the listed-first side; many of these were played at "
                        "neutral venues, so this is NOT a clean home-advantage estimate - read "
                        "it only as a weak ordering artefact, not a venue effect."),
        },
        "world_cup": world_cup,
        "frequency": {"by_decade": by_decade, "by_year": by_year},
        "definitions": {
            "favourite": ("Higher-Elo team, Elo computed from all internationals with date < the "
                          "shootout's date using the eloratings.net rule in elo.py (importance x "
                          "goal-diff multiplier, 100-pt home edge on non-neutral games). Leak-free: "
                          "a shootout never informs its own favourite."),
            "first_shooter": "Team recorded as taking the first penalty (data column; 256/677 known).",
            "win": "Team listed in the 'winner' column (the side that advanced).",
            "world_cup": "tournament == 'FIFA World Cup' after joining to history on date + {teams}; "
                         "excludes qualifiers and non-FIFA tournaments that share the words 'World Cup'.",
            "coin_flip_test": "two-sided exact binomial p-value vs p=0.5; CI = 95% Wilson score.",
        },
    }

    (HERE / "shootouts_stats.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- console summary ----
    print(f"wrote shootouts_stats.json  (n={n} shootouts, {out['meta']['date_range'][0]}..{out['meta']['date_range'][1]})")
    print(f"  first shooter wins : {first_shooter['pct']}%  (CI {first_shooter['ci95_pct']}, p={first_shooter['p_vs_50']}, n={first_shooter['n']})")
    print(f"  FAVOURITE wins     : {favourite['pct']}%  (CI {favourite['ci95_pct']}, p={favourite['p_vs_50']}, n={favourite['n']})")
    print(f"     mean Elo gap {favourite['mean_abs_elo_gap']}  =>  'should' win {favourite['expected_pct_in_regulation']}% in regulation")
    for g in fav_by_gap:
        print(f"     gap>={g['min_abs_elo_gap']:>3}: n={g['n']:>3}  fav {g['fav_win_pct']:>5}%  (vs {g['fav_expected_pct_regulation']}% expected)")
    print(f"  listed-first team  : {home_team_rate['pct']}%  (confounded by venue)")
    print(f"  WORLD CUP finals   : n={world_cup['n']}, first-shooter {world_cup['first_shooter']['pct']}%, favourite {world_cup['favourite']['pct']}%")


if __name__ == "__main__":
    main()
