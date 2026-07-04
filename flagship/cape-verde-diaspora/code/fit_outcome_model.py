"""
Data2Story Analyst -- Elo win/draw/loss model + backtest + the Argentina question.

ana_19  What were Cape Verde's chances against Argentina? (symmetric ordered logit)
ana_20  VALIDATION: out-of-sample backtest 2015-2026 vs naive baselines

MODEL (all constants published, reproducible in a browser -- see client_model.js):
  u = B * ( (rA - rB)/400 + H * homesign )   homesign: +1 A at home, -1 B at
                                             home, 0 neutral venue
  P(A wins)  = 1 - sigmoid(C - u)
  P(A loses) = sigmoid(-C - u)
  P(draw)    = sigmoid(C - u) - sigmoid(-C - u)
  SYMMETRIC thresholds (+C/-C) with the home effect as a fitted shift H, so a
  neutral-venue prediction is invariant to which side is "listed home" -- the
  right property for a World Cup match on neutral ground. (A plain ordered
  logit with free thresholds encodes a listed-home bias; rejected for that.)
  Ratings from elo_ratings.run_elo (same engine as every other Elo number here).
  Fit sample: matches 1990-01-01 .. 2026-07-03, both teams >= 30 prior matches,
  outcomes read from the home side (y in {loss, draw, win}).
  Fit: full-batch gradient descent on the exact NLL gradient, fixed 8000 steps,
  lr 0.3, init (C, B, H) = (0.6, 2.0, 0.25). Deterministic (no RNG).
  Published params are ROUNDED to 4 dp; headline probabilities are recomputed
  FROM the rounded params and 1-dp ratings, so client_model.js agrees exactly.

KNOWN LABEL CAVEAT: knockout matches enter with their extra-time score and
shootouts count as draws (dataset convention), so "draw" for historical KO
matches means "level after 120 minutes". For a knockout fixture, P(draw) is
read as P(the match reaches extra time / stays level in 90') -- approximate.

Run:  py fit_outcome_model.py     (PYTHONUTF8=1; deterministic, local files only)
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elo_ratings import load_played, run_elo  # same Elo engine, single source

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def probs(C, B, H, x, homesign):
    """[P(A loses), P(draw), P(A wins)]; x = (rA-rB)/400, homesign in {-1,0,1}."""
    u = B * (x + H * homesign)
    s_hi, s_lo = sigmoid(C - u), sigmoid(-C - u)
    return np.stack([s_lo, s_hi - s_lo, 1 - s_hi], axis=-1)

def fit_symmetric(x, home, y, steps=8000, lr=0.3):
    """x = (pre_home - pre_away)/400; home = 1 if real home advantage else 0;
    y from the home side: 0 loss, 1 draw, 2 win. Returns (C, B, H, meanNLL)."""
    C, B, H = 0.6, 2.0, 0.25
    n = len(x)
    for _ in range(steps):
        u = B * (x + H * home)
        s1, s0 = sigmoid(C - u), sigmoid(-C - u)
        p_draw = np.clip(s1 - s0, 1e-12, None)
        # d logP / dC and d logP / du per outcome class
        dC = np.where(y == 0, -(1 - s0),
             np.where(y == 2, -s1, (s1 * (1 - s1) + s0 * (1 - s0)) / p_draw))
        du = np.where(y == 0, -(1 - s0),
             np.where(y == 2, s1, (-s1 * (1 - s1) + s0 * (1 - s0)) / p_draw))
        # NLL gradients (negative mean of logP gradients)
        g_C = -dC.mean()
        g_B = -(du * (x + H * home)).mean()
        g_H = -(du * B * home).mean()
        C -= lr * g_C; B -= lr * g_B; H -= lr * g_H
    p = probs(C, B, H, x, home)
    nll = -np.log(np.clip(p[np.arange(n), y], 1e-12, None)).mean()
    return C, B, H, nll

df = load_played()
elo, R, N, LAST = run_elo(df)
m = elo[(elo.date >= "1990-01-01") & (elo.n_home >= 30) & (elo.n_away >= 30)].copy()
m["x"] = (m.pre_home - m.pre_away) / 400
m["home"] = (~m.neutral).astype(float)
m["y"] = np.select([m.home_score < m.away_score, m.home_score == m.away_score], [0, 1], 2)
print(f"fit sample: {len(m):,} matches 1990-01-01..{m.date.max()} "
      f"(both teams >=30 prior matches)")
print(f"outcome base rates (home side): win {(m.y == 2).mean() * 100:.1f}%, "
      f"draw {(m.y == 1).mean() * 100:.1f}%, loss {(m.y == 0).mean() * 100:.1f}%")

# --- ana_19: what were Cape Verde's chances against Argentina? ---
print("=== ana_19 ===")
C, B, H, nll = fit_symmetric(m.x.values, m.home.values, m.y.values)
print(f"fitted params (full sample): C={C:.4f} B={B:.4f} H={H:.4f} "
      f"(home shift = {H * 400:.0f} Elo points; mean NLL {nll:.4f})")
C_, B_, H_ = round(C, 4), round(B, 4), round(H, 4)
print(f"PUBLISHED (rounded, inlined in client_model.js): C={C_} B={B_} H={H_}, SCALE=400")
arg = elo[(elo.date == "2026-07-03") & (elo.away_team == "Cape Verde")].iloc[0]
# ratings rounded to 1 dp -- the SAME values inlined in client_model.js, so the
# browser recomputation agrees with the published numbers by construction
r_arg, r_cpv = round(arg.pre_home, 1), round(arg.pre_away, 1)
print(f"pre-match ratings 2026-07-03 (neutral venue): "
      f"Argentina {r_arg}, Cape Verde {r_cpv} (gap {r_arg - r_cpv:.1f})")
p_loss_cv, p_draw_cv, p_win_cv = probs(C_, B_, H_, np.array([(r_cpv - r_arg) / 400]), 0)[0]
print(f"model, from Cape Verde's side: win in 90' {p_win_cv * 100:.1f}%, "
      f"level after 90' (reach extra time) {p_draw_cv * 100:.1f}%, "
      f"lose in 90' {p_loss_cv * 100:.1f}%")
print(f"P(advance) if a level match is a coin flip (assumption): "
      f"{(p_win_cv + 0.5 * p_draw_cv) * 100:.1f}%")
# symmetry sanity: identical from Argentina's side
pa = probs(C_, B_, H_, np.array([(r_arg - r_cpv) / 400]), 0)[0]
assert abs(pa[0] - p_win_cv) < 1e-12 and abs(pa[1] - p_draw_cv) < 1e-12
print("side-swap symmetry check: PASS (neutral venue, listed side irrelevant)")
# the same model across Cape Verde's whole tournament, for the record
for _, r_ in elo[(elo.tournament == "FIFA World Cup") & (elo.date >= "2026-06-01")
                 & ((elo.home_team == "Cape Verde") | (elo.away_team == "Cape Verde"))].iterrows():
    cv_home = r_.home_team == "Cape Verde"
    rcv = round(r_.pre_home if cv_home else r_.pre_away, 1)
    ropp = round(r_.pre_away if cv_home else r_.pre_home, 1)
    pl, pd_, pw = probs(C_, B_, H_, np.array([(rcv - ropp) / 400]), 0)[0]
    res = f"{int(r_.home_score)}-{int(r_.away_score)}"
    opp = r_.away_team if cv_home else r_.home_team
    print(f"  {r_.date} vs {opp} ({res}): P(CV win)={pw * 100:.1f}% "
          f"P(draw)={pd_ * 100:.1f}% P(CV loss)={pl * 100:.1f}%")

# --- ana_20: out-of-sample backtest 2015-2026 ---
print("=== ana_20 ===")
train, test = m[m.date < "2015-01-01"], m[m.date >= "2015-01-01"]
Ct, Bt, Ht, nll_tr = fit_symmetric(train.x.values, train.home.values, train.y.values)
print(f"train: {len(train):,} matches (1990-2014), params C={Ct:.4f} B={Bt:.4f} H={Ht:.4f}")
print(f"test : {len(test):,} matches (2015-2026), fully out-of-sample")
p_test = probs(Ct, Bt, Ht, test.x.values, test.home.values)
onehot = np.eye(3)[test.y.values]
brier_model = ((p_test - onehot) ** 2).sum(axis=1).mean()
base = np.array([(train.y == 0).mean(), (train.y == 1).mean(), (train.y == 2).mean()])
brier_base = ((base - onehot) ** 2).sum(axis=1).mean()
ll_model = -np.log(np.clip(p_test[np.arange(len(test)), test.y.values], 1e-12, None)).mean()
ll_base = -np.log(base[test.y.values]).mean()
print(f"3-class Brier: model {brier_model:.4f} vs base-rate baseline {brier_base:.4f} "
      f"({(1 - brier_model / brier_base) * 100:.1f}% better)")
print(f"log-loss    : model {ll_model:.4f} vs baseline {ll_base:.4f} "
      f"({(1 - ll_model / ll_base) * 100:.1f}% better)")
# Elo expectancy itself (W in {0,.5,1} vs We), same holdout
we = 1 / (10 ** (-(test.pre_home + 100 * test.home - test.pre_away) / 400) + 1)
w = np.select([test.home_score > test.away_score,
               test.home_score == test.away_score], [1.0, 0.5], 0.0)
print(f"Elo expectancy Brier (W vs We): {((we - w) ** 2).mean():.4f} vs "
      f"constant-0.5 baseline {((0.5 - w) ** 2).mean():.4f}")
# calibration: predicted home-win deciles vs observed home-win rate
dec = pd.DataFrame({"p": p_test[:, 2], "won": (test.y == 2).values})
dec["bin"] = np.clip((dec.p * 10).astype(int), 0, 9)
cal = dec.groupby("bin").agg(n=("won", "size"), pred=("p", "mean"),
                             actual=("won", "mean")).round(3)
print("calibration (predicted home-win prob decile vs observed, test set):")
print(cal.to_string())
gap = (cal.pred - cal.actual).abs().max()
print(f"max |predicted - observed| across bins: {gap:.3f}")
print("LEVEL VALIDATED: per-match outcome probabilities, out-of-sample 2015-2026.")
print("The ana_19 headline (Cape Verde's chance in ONE match vs Argentina) is a")
print("per-match probability at exactly this level; no tournament-level or")
print("multi-match aggregate is claimed or validated.")

# constants for client_model.js: pre-R32 snapshot (ratings after 2026-06-27)
print("=== client_model constants ===")
df27 = df[df.date <= "2026-06-27"]
_, R27, N27, _ = run_elo(df27)
wc26 = df[(df.tournament == "FIFA World Cup") & (df.date.str.startswith("2026"))]
cnt = pd.concat([wc26.home_team, wc26.away_team]).value_counts()
r32 = sorted(cnt[cnt >= 4].index)  # the 32 teams that reached the R32
print(f"R32 teams: {len(r32)}")
for t in r32:
    print(f"  {t}: {R27[t]:.1f}")
