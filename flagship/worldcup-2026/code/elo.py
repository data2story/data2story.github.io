"""
elo.py — World-Football Elo ratings computed from the full international-match
history (martj42), using the standard eloratings.net update rule.

R'_home = R_home + K * (W - We)
  We   = 1 / (1 + 10^(-(R_home + H - R_away)/400))   # H = home advantage (0 if neutral)
  W    = 1 win / 0.5 draw / 0 loss (home perspective)
  K    = importance(tournament) * goal_difference_multiplier
Home and away ratings move by +/- the same delta (zero-sum).

The ratings are a deterministic function of (history up to a cutoff date) — no
randomness — so any rating in the forecast traces back to these exact rows + rule.

Usage:
    python elo.py            # prints the WC-48 ratings as of 2026-06-18
Importable:
    from elo import compute_elo, rating_table, MARTJ42_ALIAS
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from collections import defaultdict
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent          # .../worldcup_2026
HIST = DATA / "intl_results_history.csv"

BASE = 1500.0
HOME_ADV = 100.0           # eloratings.net convention; applied only when not neutral
WC_START = "2026-06-11"    # first 2026 WC match
TODAY_CUTOFF = "2026-06-24"  # forecast frontier: train strictly before this date (refreshed 2026-06-24; was 2026-06-23)

# martj42 spells two of the 48 differently from our canonical (openfootball) names.
MARTJ42_ALIAS = {            # canonical -> martj42
    "USA": "United States",
    "Bosnia & Herzegovina": "Bosnia and Herzegovina",
}


def importance(tournament: str) -> float:
    """eloratings.net match-weight by competition tier."""
    t = str(tournament).lower()
    if "world cup" in t and "qual" not in t:
        return 60.0
    if "qualif" in t:
        return 40.0
    if "nations league" in t:
        return 40.0
    if ("friendly" in t) or ("friendship" in t):
        return 20.0
    if any(k in t for k in ("euro", "copa am", "copa america", "african cup", "africa cup",
                            "asian cup", "gold cup", "concacaf championship", "confederations",
                            "nations cup", "oceania nations")) and "qual" not in t:
        return 50.0
    return 30.0


def gd_multiplier(gd: int) -> float:
    a = abs(int(gd))
    if a <= 1:
        return 1.0
    if a == 2:
        return 1.5
    return (11.0 + a) / 8.0


def load_history(cutoff: str | None = None) -> pd.DataFrame:
    df = pd.read_csv(HIST, encoding="utf-8")
    df = df.dropna(subset=["home_score", "away_score"]).copy()
    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)
    df = df.sort_values("date", kind="stable").reset_index(drop=True)
    if cutoff is not None:
        df = df[df["date"] < cutoff].reset_index(drop=True)
    return df


def compute_elo(cutoff: str | None = None, base: float = BASE,
                home_adv: float = HOME_ADV, df: pd.DataFrame | None = None) -> dict:
    """Return {team -> Elo} after processing every match with date < cutoff."""
    if df is None:
        df = load_history(cutoff)
    elif cutoff is not None:
        df = df[df["date"] < cutoff]
    ratings: dict = defaultdict(lambda: base)
    for home, away, hs, as_, tour, neutral in zip(
        df["home_team"], df["away_team"], df["home_score"], df["away_score"],
        df["tournament"], df["neutral"]
    ):
        rh, ra = ratings[home], ratings[away]
        hadv = 0.0 if bool(neutral) else home_adv
        we = 1.0 / (1.0 + 10.0 ** (-((rh + hadv) - ra) / 400.0))
        w = 1.0 if hs > as_ else (0.5 if hs == as_ else 0.0)
        k = importance(tour) * gd_multiplier(hs - as_)
        delta = k * (w - we)
        ratings[home] = rh + delta
        ratings[away] = ra - delta
    return dict(ratings)


def rating_table(ratings: dict, teams: list[str]) -> dict:
    """Map canonical WC team names -> Elo, applying the martj42 alias."""
    out = {}
    for t in teams:
        key = MARTJ42_ALIAS.get(t, t)
        if key not in ratings:
            raise KeyError(f"team not found in Elo ratings: {t} (looked up '{key}')")
        out[t] = ratings[key]
    return out


if __name__ == "__main__":
    teams = pd.read_csv(DATA / "teams.csv", encoding="utf-8")
    wc = teams["team"].tolist()
    elo_now = rating_table(compute_elo(cutoff=TODAY_CUTOFF), wc)
    elo_pre = rating_table(compute_elo(cutoff=WC_START), wc)
    fifa = teams.set_index("team")["fifa_rank"].to_dict()
    print(f"Elo for the 48 WC teams (trained on matches before {TODAY_CUTOFF}):\n")
    print(f"{'rank':>4} {'team':24} {'Elo_now':>8} {'Elo_pre':>8} {'Δ(WC)':>6} {'FIFA#':>5}")
    for i, (t, r) in enumerate(sorted(elo_now.items(), key=lambda kv: -kv[1]), 1):
        d = r - elo_pre[t]
        print(f"{i:>4} {t:24} {r:8.1f} {elo_pre[t]:8.1f} {d:+6.1f} {fifa[t]:>5}")
