"""
simulate.py — Monte-Carlo forecast of the rest of the 2026 World Cup.

Pipeline (all deterministic given the fixed seed, so every probability is reproducible):
  1. Elo as of 2026-06-18 (elo.py, trained strictly on matches before 2026-06-19).
  2. Poisson goal model calibrated on 2002+ internationals (poisson.py).
  3. N Monte-Carlo tournaments:
       - simulate the 44 remaining group matches -> final group tables
         (rank by points, goal difference, goals for, then a random tiebreak;
          full head-to-head is a documented simplification, see caveats)
       - 12 winners + 12 runners-up + the 8 best third-placed teams -> Round of 32
         (third-place slotting uses FIFA Annex C's full 495-combination table)
       - knockout rounds resolved analytically: P(advance) = P(win in 90') +
         P(draw) * Elo win-expectation (the Elo term stands in for extra-time + penalties)
  4. Aggregate -> per-team probabilities (advance, each round, champion) + per-match
     probabilities for the 44 remaining group games.

Outputs (forecast_outputs/): champion_odds.csv, advance_probs.csv, match_probs.csv,
group_forecast.csv, forecast_summary.json.

Usage:  python simulate.py [N]      (default N = 100000)
"""
import sys, json, math
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from pathlib import Path
import numpy as np
import pandas as pd

from elo import compute_elo, rating_table, TODAY_CUTOFF, WC_START, DATA
import poisson as P

OUT = DATA / "forecast_outputs"
SEED = 20260618


def grid_probs(lh, la, maxg=10):
    """Vectorised Poisson-Poisson W/D/L over score grid. lh,la arrays [M] -> pH,pD,pA."""
    lh = np.asarray(lh, dtype=float); la = np.asarray(la, dtype=float)
    ks = np.arange(maxg + 1)
    logfact = np.array([math.lgamma(k + 1) for k in ks])
    ph = np.exp(-lh[:, None] + ks[None, :] * np.log(lh[:, None]) - logfact[None, :])
    pa = np.exp(-la[:, None] + ks[None, :] * np.log(la[:, None]) - logfact[None, :])
    cum = np.cumsum(pa, axis=1)
    below = np.concatenate([np.zeros((len(lh), 1)), cum[:, :-1]], axis=1)   # P(away < i)
    above = np.clip(1.0 - cum, 0, None)                                     # P(away > i)
    pH = (ph * below).sum(1); pD = (ph * pa).sum(1); pA = (ph * above).sum(1)
    s = pH + pD + pA
    return pH / s, pD / s, pA / s


def main(N=100000):
    rng = np.random.default_rng(SEED)
    OUT.mkdir(exist_ok=True)

    # ---- teams, groups, Elo, calibration ----
    tdf = pd.read_csv(DATA / "teams.csv", encoding="utf-8")
    teams = tdf["team"].tolist()
    tidx = {t: i for i, t in enumerate(teams)}
    group_of = dict(zip(tdf["team"], tdf["group"]))
    groups = sorted(tdf["group"].unique())                     # A..L
    gletter_idx = {g: i for i, g in enumerate(groups)}
    elo = rating_table(compute_elo(cutoff=TODAY_CUTOFF), teams)
    elo_arr = np.array([elo[t] for t in teams])
    p = P.calibrate()
    a, b, mu = p["a"], p["b"], p["mu_tot"]

    def lam(eh, ea):                                            # neutral venue (WC)
        sup = a + b * (np.asarray(eh, float) - np.asarray(ea, float))
        return np.clip((mu + sup) / 2, 0.05, None), np.clip((mu - sup) / 2, 0.05, None)

    def p_home_adv(eh, ea):                                     # knockout advance prob
        lh, la = lam(eh, ea)
        pH, pD, _ = grid_probs(lh, la)
        we = 1.0 / (1.0 + 10.0 ** (-(np.asarray(eh, float) - np.asarray(ea, float)) / 400.0))
        return pH + pD * we

    # ---- bracket rules ----
    br = json.loads((DATA / "bracket_rules.json").read_text(encoding="utf-8"))
    r32_slots = br["r32_slots"]
    tree = br["bracket_tree"]
    alloc = br["best_thirds_allocation"]["table"]
    host_matches = [74, 77, 79, 80, 81, 82, 85, 87]
    host_ridx = [m - 73 for m in host_matches]
    # allocation lookup table[bitmask, r32_idx] = group index whose 3rd fills that match (-1 none)
    table = -np.ones((4096, 16), dtype=np.int64)
    for key, val in alloc.items():
        bm = 0
        for ch in key:
            bm |= 1 << (ord(ch) - 65)
        for mid, slot in val["assign"].items():
            table[bm, int(mid) - 73] = ord(str(slot)[-1]) - 65

    # ---- group stage: played baseline ----
    m = pd.read_csv(DATA / "matches.csv", encoding="utf-8")
    gmask = m["stage"] == "group"
    played = m[gmask & (m["status"] == "played")]
    sched = m[gmask & (m["status"] == "scheduled")]
    pts0 = np.zeros(48); gd0 = np.zeros(48); gf0 = np.zeros(48)
    for h, aw, hg, ag in zip(played["home"], played["away"], played["home_goals"], played["away_goals"]):
        hi, ai, hg, ag = tidx[h], tidx[aw], int(hg), int(ag)
        gf0[hi] += hg; gf0[ai] += ag; gd0[hi] += hg - ag; gd0[ai] += ag - hg
        if hg > ag: pts0[hi] += 3
        elif hg == ag: pts0[hi] += 1; pts0[ai] += 1
        else: pts0[ai] += 3

    pts = np.tile(pts0, (N, 1)); gd = np.tile(gd0, (N, 1)); gf = np.tile(gf0, (N, 1))
    for h, aw in zip(sched["home"], sched["away"]):
        hi, ai = tidx[h], tidx[aw]
        lh, la = lam(elo_arr[hi], elo_arr[ai])                  # scalars
        hg = rng.poisson(float(lh), N); ag = rng.poisson(float(la), N)
        gf[:, hi] += hg; gf[:, ai] += ag
        gd[:, hi] += hg - ag; gd[:, ai] += ag - hg
        hw = hg > ag; dr = hg == ag
        pts[:, hi] += np.where(hw, 3, np.where(dr, 1, 0))
        pts[:, ai] += np.where(~hw & ~dr, 3, np.where(dr, 1, 0))

    # ---- rank within each group ----
    def sortkey(idxarr):                                        # idxarr [N,k] team indices
        k = (pts[np.arange(N)[:, None], idxarr] * 10000.0
             + (gd[np.arange(N)[:, None], idxarr] + 100.0) * 100.0
             + gf[np.arange(N)[:, None], idxarr])
        return k + rng.random(idxarr.shape) * 0.5             # random final tiebreak

    winners = {}; runners = {}
    thirds_team = np.zeros((N, 12), dtype=np.int64)
    thirds_key = np.zeros((N, 12))
    fin_counts = {1: np.zeros(48), 2: np.zeros(48), 3: np.zeros(48), 4: np.zeros(48)}
    for g in groups:
        gt = np.array([tidx[t] for t in tdf[tdf["group"] == g]["team"]])
        kk = sortkey(np.tile(gt, (N, 1)))
        order = np.argsort(-kk, axis=1)
        finish = gt[order]                                     # [N,4] team idx ranked 1..4
        winners[g] = finish[:, 0]; runners[g] = finish[:, 1]
        gi = gletter_idx[g]
        thirds_team[:, gi] = finish[:, 2]
        tk = (pts[np.arange(N), finish[:, 2]] * 10000.0
              + (gd[np.arange(N), finish[:, 2]] + 100.0) * 100.0
              + gf[np.arange(N), finish[:, 2]])
        thirds_key[:, gi] = tk + rng.random(N) * 0.5
        for pos in range(4):
            np.add.at(fin_counts[pos + 1], finish[:, pos], 1)

    # ---- best 8 of 12 third-placed ----
    order12 = np.argsort(-thirds_key, axis=1)
    top8 = order12[:, :8]                                       # group indices [N,8]
    bitmask = np.zeros(N, dtype=np.int64)
    for c in range(8):
        bitmask |= (1 << top8[:, c])
    assign_tbl = table[bitmask]                                 # [N,16] group idx per r32 match
    assert (assign_tbl[:, host_ridx] >= 0).all(), "allocation gap: some bitmask missing host assignment"
    third_assigned = np.zeros((N, 16), dtype=np.int64)
    for ridx in host_ridx:
        grp = assign_tbl[:, ridx]
        third_assigned[:, ridx] = thirds_team[np.arange(N), grp]
    best_third_team = thirds_team[np.arange(N)[:, None], top8]  # [N,8] qualifying thirds

    # ---- build R32 participants ----
    def resolve(slot):
        return winners[slot[1]] if slot[0] == "1" else runners[slot[1]]
    r32_home = np.zeros((N, 16), dtype=np.int64)
    r32_away = np.zeros((N, 16), dtype=np.int64)
    for ridx in range(16):
        s = r32_slots[str(73 + ridx)]
        r32_home[:, ridx] = resolve(s["home"])
        r32_away[:, ridx] = third_assigned[:, ridx] if s["away"].startswith("3") else resolve(s["away"])

    # ---- knockout ----
    W = np.zeros((N, 105), dtype=np.int64)
    L = np.zeros((N, 105), dtype=np.int64)
    for ridx in range(16):
        h, aw = r32_home[:, ridx], r32_away[:, ridx]
        padv = p_home_adv(elo_arr[h], elo_arr[aw])
        u = rng.random(N); win = np.where(u < padv, h, aw); los = np.where(u < padv, aw, h)
        W[:, 73 + ridx] = win; L[:, 73 + ridx] = los
    for mid in range(89, 105):
        node = tree[str(mid)]
        def feed(side):
            return W[:, side["from_match"]] if side["take"] == "winner" else L[:, side["from_match"]]
        h, aw = feed(node["home"]), feed(node["away"])
        padv = p_home_adv(elo_arr[h], elo_arr[aw])
        u = rng.random(N); win = np.where(u < padv, h, aw); los = np.where(u < padv, aw, h)
        W[:, mid] = win; L[:, mid] = los

    # ---- aggregate per-team probabilities ----
    def frac(arr):
        return np.bincount(np.ravel(arr), minlength=48) / N
    p_champ = frac(W[:, 104])
    p_final = frac(np.concatenate([W[:, 101], W[:, 102]]))
    p_sf = frac(W[:, 97:101])
    p_qf = frac(W[:, 89:97])
    p_r16 = frac(W[:, 73:89])
    p_ko = frac(np.concatenate([r32_home.ravel(), r32_away.ravel()]))    # reach R32
    p_win = fin_counts[1] / N; p_run = fin_counts[2] / N
    p_third = fin_counts[3] / N; p_fourth = fin_counts[4] / N
    p_best3 = frac(best_third_team)
    exp_pts = pts.mean(axis=0)

    base = pd.DataFrame({
        "team": teams, "group": [group_of[t] for t in teams],
        "elo": elo_arr.round(1), "fifa_rank": tdf["fifa_rank"].values,
        "squad_value_eur_m": tdf["squad_value_eur_m"].values,
        "p_win_group": p_win, "p_runner_up": p_run, "p_third": p_third,
        "p_advance_group": p_win + p_run, "p_best_third": p_best3,
        "p_reach_r32": p_ko, "p_reach_r16": p_r16, "p_reach_qf": p_qf,
        "p_reach_sf": p_sf, "p_reach_final": p_final, "p_champion": p_champ,
        "exp_group_points": exp_pts.round(3),
    }).sort_values("p_champion", ascending=False).reset_index(drop=True)
    for c in [c for c in base.columns if c.startswith("p_")]:
        base[c] = base[c].round(4)

    base.to_csv(OUT / "advance_probs.csv", index=False, encoding="utf-8")
    base[["team", "group", "elo", "fifa_rank", "squad_value_eur_m",
          "p_reach_r16", "p_reach_qf", "p_reach_sf", "p_reach_final", "p_champion"]] \
        .to_csv(OUT / "champion_odds.csv", index=False, encoding="utf-8")
    base[["team", "group", "exp_group_points", "p_win_group", "p_runner_up",
          "p_third", "p_fourth" if False else "p_advance_group", "p_best_third", "p_reach_r32"]] \
        .to_csv(OUT / "group_forecast.csv", index=False, encoding="utf-8")

    # ---- per-match probabilities for the 44 remaining group games (analytic) ----
    rows = []
    for mid, dt, g, h, aw in zip(sched["match_id"], sched["date"], sched["group"], sched["home"], sched["away"]):
        lh, la = lam(elo_arr[tidx[h]], elo_arr[tidx[aw]])
        pH, pD, pA = grid_probs(np.array([float(lh)]), np.array([float(la)]))
        ph_g = np.exp(-float(lh)) * float(lh) ** np.arange(8) / [math.factorial(k) for k in range(8)]
        pa_g = np.exp(-float(la)) * float(la) ** np.arange(8) / [math.factorial(k) for k in range(8)]
        gi, gj = np.unravel_index(np.argmax(np.outer(ph_g, pa_g)), (8, 8))
        rows.append([int(mid), dt, g, h, aw, round(float(pH[0]), 4), round(float(pD[0]), 4),
                     round(float(pA[0]), 4), round(float(lh), 2), round(float(la), 2), f"{gi}-{gj}"])
    pd.DataFrame(rows, columns=["match_id", "date", "group", "home", "away",
                                "p_home_win", "p_draw", "p_away_win",
                                "exp_home_goals", "exp_away_goals", "likely_score"]) \
        .to_csv(OUT / "match_probs.csv", index=False, encoding="utf-8")

    # ---- health check + summary ----
    bt = P.backtest(p)
    frame = P.prematch_frame()
    sk = P.skill_check(p, frame)
    summary = {
        "n_simulations": N, "seed": SEED, "elo_cutoff": TODAY_CUTOFF,
        "as_of": "2026-06-24", "calibration": p,
        "model_health": {
            "large_sample_skill": {"model": sk["model"], "naive": sk["naive"], "n": sk["n"]},
            # all group games played so far, scored from the leak-free pre-tournament Elo
            "backtest_played": {"model": bt["played28"], "naive": bt["naive28"], "n": bt["n28"]},
            "backtest_28_played": {"model": bt["played28"], "naive": bt["naive28"], "n": bt["n28"]},  # legacy key (== backtest_played)
            "note": f"This-tournament backtest now covers all {bt['n28']} played group games (scored from pre-WC Elo); it is still a small, upset-prone sample, so the 8000-match skill check is the reliable read.",
        },
        "champion_top10": base[["team", "p_champion"]].head(10).values.tolist(),
        "caveats": [
            "Group ranking uses points, goal difference, goals for, then a random tiebreak; full head-to-head tiebreakers are not implemented (rarely decisive).",
            "Knockout extra-time/penalties are modelled by an Elo win-expectation term, not simulated minute-by-minute.",
            "All World Cup matches are treated as neutral-venue; host advantage (USA/Canada/Mexico) is not modelled.",
            "Goals are independent Poisson; no Dixon-Coles low-score correction or red-card/injury effects.",
            "Squad market value and FIFA rank are carried for context only; the forecast is driven by Elo.",
        ],
    }
    (OUT / "forecast_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- console report ----
    print(f"=== 2026 World Cup Monte-Carlo forecast (N={N:,}, seed={SEED}) ===")
    print(f"Elo as of {TODAY_CUTOFF} (excl.); Poisson calib n={p['n']}, mu_tot={mu:.2f}\n")
    print(f"{'team':22}{'grp':>4}{'Elo':>7}{'FIFA':>5}{'R16':>7}{'QF':>7}{'SF':>7}{'Final':>7}{'CHAMP':>8}")
    for _, r in base.head(16).iterrows():
        print(f"{r['team']:22}{r['group']:>4}{r['elo']:>7.0f}{int(r['fifa_rank']):>5}"
              f"{r['p_reach_r16']*100:>6.1f}%{r['p_reach_qf']*100:>6.1f}%{r['p_reach_sf']*100:>6.1f}%"
              f"{r['p_reach_final']*100:>6.1f}%{r['p_champion']*100:>7.1f}%")
    print(f"\nchampion prob sum = {p_champ.sum():.3f} (should be 1.000)")
    print(f"reach-R32 sum = {p_ko.sum():.1f} (should be 32)")
    mll, mbr, mac = sk["model"]; nll, nbr, nac = sk["naive"]
    print(f"skill (n={sk['n']}): model LL={mll:.3f}/Acc={mac:.2f}  vs naive LL={nll:.3f}/Acc={nac:.2f}")
    print(f"wrote 5 files to {OUT}")


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    main(N)
