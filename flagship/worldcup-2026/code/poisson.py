"""
poisson.py — turn an Elo difference into a scoreline distribution, and calibrate
that mapping on historical internationals.

Model: each side's goals ~ independent Poisson.
  supremacy(de) = a + b*de       (de = effective Elo diff, incl. home advantage)
  total         = mu_tot         (mean goals per match, fitted)
  lambda_home   = (mu_tot + supremacy)/2 ,  lambda_away = (mu_tot - supremacy)/2
a, b, mu_tot are fitted by least squares / mean on matches since `calib_start`,
using each match's PRE-match Elo (replayed chronologically — no look-ahead).

Match win/draw/loss probabilities come from the Poisson-Poisson score grid.
A Dixon-Coles low-score correction is left as a documented refinement (see caveats).

Usage:
    python poisson.py        # calibrate + print params + backtest (28 played + 44 held-out)
Importable:
    from poisson import calibrate, lambdas, outcome_probs
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from collections import defaultdict
from math import exp, factorial
from pathlib import Path
import numpy as np
import pandas as pd

from elo import (load_history, importance, gd_multiplier, compute_elo, rating_table,
                 BASE, HOME_ADV, WC_START, TODAY_CUTOFF, HIST, DATA, MARTJ42_ALIAS)

CANON_FROM_MARTJ42 = {v: k for k, v in MARTJ42_ALIAS.items()}


def prematch_frame(cutoff: str = TODAY_CUTOFF, calib_start: str = "2002-01-01") -> pd.DataFrame:
    """Replay history < cutoff; record each match's pre-match effective Elo diff `de`
    plus the actual scoreline, for matches on/after calib_start."""
    df = load_history(cutoff)
    ratings: dict = defaultdict(lambda: BASE)
    de_list, hs_list, as_list = [], [], []
    for home, away, hs, as_, tour, neutral, date in zip(
        df["home_team"], df["away_team"], df["home_score"], df["away_score"],
        df["tournament"], df["neutral"], df["date"]
    ):
        rh, ra = ratings[home], ratings[away]
        hadv = 0.0 if bool(neutral) else HOME_ADV
        de = (rh + hadv) - ra
        if date >= calib_start:
            de_list.append(de); hs_list.append(hs); as_list.append(as_)
        we = 1.0 / (1.0 + 10.0 ** (-de / 400.0))
        w = 1.0 if hs > as_ else (0.5 if hs == as_ else 0.0)
        delta = importance(tour) * gd_multiplier(hs - as_) * (w - we)
        ratings[home] = rh + delta
        ratings[away] = ra - delta
    return pd.DataFrame({"de": de_list, "hs": hs_list, "as": as_list})


def calibrate(cutoff: str = TODAY_CUTOFF, calib_start: str = "2002-01-01",
              frame: pd.DataFrame | None = None) -> dict:
    f = prematch_frame(cutoff, calib_start) if frame is None else frame
    sup = (f["hs"] - f["as"]).to_numpy(dtype=float)
    de = f["de"].to_numpy(dtype=float)
    b, a = np.polyfit(de, sup, 1)            # supremacy = a + b*de
    mu_tot = float((f["hs"] + f["as"]).mean())
    return {"a": float(a), "b": float(b), "mu_tot": mu_tot, "n": int(len(f)),
            "calib_start": calib_start, "cutoff": cutoff}


def lambdas(elo_h: float, elo_a: float, neutral: bool, p: dict, home_adv: float = HOME_ADV):
    de = (elo_h + (0.0 if neutral else home_adv)) - elo_a
    sup = p["a"] + p["b"] * de
    lh = max(0.05, (p["mu_tot"] + sup) / 2.0)
    la = max(0.05, (p["mu_tot"] - sup) / 2.0)
    return lh, la


def outcome_probs(lh: float, la: float, maxg: int = 12):
    ph = [exp(-lh) * lh ** k / factorial(k) for k in range(maxg + 1)]
    pa = [exp(-la) * la ** k / factorial(k) for k in range(maxg + 1)]
    pH = pD = pA = 0.0
    for i in range(maxg + 1):
        for j in range(maxg + 1):
            pij = ph[i] * pa[j]
            if i > j:
                pH += pij
            elif i == j:
                pD += pij
            else:
                pA += pij
    s = pH + pD + pA
    return pH / s, pD / s, pA / s


# ----------------------------- backtest (health check) -----------------------------

def _metrics(rows):
    """rows: list of (pH,pD,pA, actual in {'H','D','A'}). Returns logloss, brier, acc."""
    eps = 1e-12
    ll = bri = acc = 0.0
    for pH, pD, pA, act in rows:
        p = {"H": pH, "D": pD, "A": pA}
        ll -= np.log(max(eps, p[act]))
        onev = {"H": 0.0, "D": 0.0, "A": 0.0}; onev[act] = 1.0
        bri += sum((p[k] - onev[k]) ** 2 for k in p)
        pred = max(p, key=p.get)
        acc += 1.0 if pred == act else 0.0
    n = len(rows)
    return ll / n, bri / n, acc / n


def _result_char(hg, ag):
    return "H" if hg > ag else ("D" if hg == ag else "A")


def skill_check(p, frame, n=8000, seed=0):
    """Large-sample skill estimate: score the model's W/D/L probs against actuals over a
    random sample of the calibration matches, vs the naive base-rate. With only 3 fitted
    params over 23k matches, in-sample optimism is negligible — this is a fair skill read."""
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(frame), size=min(n, len(frame)), replace=False)
    de = frame["de"].to_numpy()[idx]
    hs = frame["hs"].to_numpy()[idx]
    as_ = frame["as"].to_numpy()[idx]
    rows, naive = [], []
    base_rate = (0.40, 0.27, 0.33)
    for d, h, a in zip(de, hs, as_):
        sup = p["a"] + p["b"] * d
        lh = max(0.05, (p["mu_tot"] + sup) / 2.0); la = max(0.05, (p["mu_tot"] - sup) / 2.0)
        pH, pD, pA = outcome_probs(lh, la)
        act = _result_char(h, a)
        rows.append((pH, pD, pA, act)); naive.append((*base_rate, act))
    return {"model": _metrics(rows), "naive": _metrics(naive), "n": len(rows)}


def backtest(p):
    teams = pd.read_csv(DATA / "teams.csv", encoding="utf-8")["team"].tolist()
    elo_pre = rating_table(compute_elo(cutoff=WC_START), teams)       # before any WC game
    elo_now = rating_table(compute_elo(cutoff=TODAY_CUTOFF), teams)   # as of 2026-06-18

    # (1) the 28 already-played group games, predicted from PRE-tournament Elo (neutral)
    m = pd.read_csv(DATA / "matches.csv", encoding="utf-8")
    played = m[(m["status"] == "played") & (m["stage"] == "group")]
    rows28 = []
    for h, a, hg, ag in zip(played["home"], played["away"], played["home_goals"], played["away_goals"]):
        pH, pD, pA = outcome_probs(*lambdas(elo_pre[h], elo_pre[a], True, p))
        rows28.append((pH, pD, pA, _result_char(int(hg), int(ag))))

    # (2) the 44 held-out group games (2026-06-19..27), predicted from as-of-06-18 Elo,
    #     actuals taken from martj42 (which were EXCLUDED from training) -> true out-of-sample
    full = pd.read_csv(HIST, encoding="utf-8")
    fut = full[(full["tournament"].astype(str).str.contains("World Cup", case=False, na=False))
               & (~full["tournament"].astype(str).str.contains("qual", case=False, na=False))
               & (full["date"] >= "2026-06-19") & (full["date"] <= "2026-06-27")].copy()
    fut = fut.dropna(subset=["home_score", "away_score"])
    rows44 = []
    for h, a, hg, ag in zip(fut["home_team"], fut["away_team"], fut["home_score"], fut["away_score"]):
        hc = CANON_FROM_MARTJ42.get(h, h); ac = CANON_FROM_MARTJ42.get(a, a)
        if hc not in elo_now or ac not in elo_now:
            continue
        pH, pD, pA = outcome_probs(*lambdas(elo_now[hc], elo_now[ac], True, p))
        rows44.append((pH, pD, pA, _result_char(int(hg), int(ag))))

    # naive baseline for context: fixed base rates (home/draw/away) ignoring strength
    base_rate = (0.40, 0.27, 0.33)
    naive28 = [(*base_rate, r[3]) for r in rows28]
    return {
        "played28": _metrics(rows28),
        "heldout44": _metrics(rows44) if rows44 else None,
        "naive28": _metrics(naive28),
        "n28": len(rows28), "n44": len(rows44),
    }


if __name__ == "__main__":
    frame = prematch_frame()
    p = calibrate(frame=frame)
    print(f"calibration (n={p['n']} matches since {p['calib_start']}):")
    print(f"  supremacy = {p['a']:+.4f} {p['b']:+.5f}*de   mu_tot = {p['mu_tot']:.3f}")
    # sanity: a strong fav (+200 Elo, neutral) lambdas
    lh, la = lambdas(2100, 1700, True, p)
    pH, pD, pA = outcome_probs(lh, la)
    print(f"  example +400 Elo edge (neutral): lambda {lh:.2f}-{la:.2f}  ->  W/D/L {pH:.2f}/{pD:.2f}/{pA:.2f}")
    lh, la = lambdas(1900, 1900, True, p)
    pH, pD, pA = outcome_probs(lh, la)
    print(f"  example even match (neutral):    lambda {lh:.2f}-{la:.2f}  ->  W/D/L {pH:.2f}/{pD:.2f}/{pA:.2f}")
    sk = skill_check(p, frame)
    mll, mbr, mac = sk["model"]; nll, nbr, nac = sk["naive"]
    print(f"\nLarge-sample skill (n={sk['n']} historical matches):")
    print(f"  model:       LL={mll:.3f} Brier={mbr:.3f} Acc={mac:.2f}")
    print(f"  naive base:  LL={nll:.3f} Brier={nbr:.3f} Acc={nac:.2f}")
    print(f"  -> model improvement: LL {nll-mll:+.3f}, Acc {mac-nac:+.2f}")

    bt = backtest(p)
    print("\nBacktest (log-loss / Brier / accuracy; lower LL+Brier better):")
    ll, br, ac = bt["played28"]; print(f"  28 played (from pre-WC Elo): LL={ll:.3f} Brier={br:.3f} Acc={ac:.2f}  (n={bt['n28']})")
    ll, br, ac = bt["naive28"];  print(f"  28 played (naive base-rate): LL={ll:.3f} Brier={br:.3f} Acc={ac:.2f}")
    if bt["heldout44"]:
        ll, br, ac = bt["heldout44"]; print(f"  44 held-out (true OOS):      LL={ll:.3f} Brier={br:.3f} Acc={ac:.2f}  (n={bt['n44']})")
