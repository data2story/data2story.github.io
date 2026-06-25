"""
build_accuracy.py - regenerate accuracy_28.json: the per-match scorecard over EVERY
group game played so far, scored from the leak-free PRE-tournament Elo (cutoff=WC_START).

This mirrors poisson.backtest()'s `rows28` methodology exactly (pre-WC Elo, neutral
venue, Poisson-Poisson outcome probabilities) and reproduces the original
accuracy_28.json schema, but extends from the first 28 games to all played group games.

Predictions use ONLY pre-tournament information (Elo trained on matches before
2026-06-11), so the scorecard is an honest out-of-the-gate backtest with no leakage.

Run:  python build_accuracy.py   ->  writes ../code/accuracy_28.json
"""
import sys, json, math
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from pathlib import Path
import pandas as pd

from elo import compute_elo, rating_table, WC_START, DATA
import poisson as P

HERE = Path(__file__).resolve().parent


def likely_score(lh, la, maxg=7):
    """Modal scoreline = argmax over the independent-Poisson score grid (matches simulate.py)."""
    ph = [math.exp(-lh) * lh ** k / math.factorial(k) for k in range(maxg + 1)]
    pa = [math.exp(-la) * la ** k / math.factorial(k) for k in range(maxg + 1)]
    best, bi, bj = -1.0, 0, 0
    for i in range(maxg + 1):
        for j in range(maxg + 1):
            if ph[i] * pa[j] > best:
                best, bi, bj = ph[i] * pa[j], i, j
    return f"{bi}-{bj}"


def main():
    teams = pd.read_csv(DATA / "teams.csv", encoding="utf-8")["team"].tolist()
    elo_pre = rating_table(compute_elo(cutoff=WC_START), teams)   # pre-tournament, leak-free
    p = P.calibrate()

    m = pd.read_csv(DATA / "matches.csv", encoding="utf-8")
    played = m[(m["status"] == "played") & (m["stage"] == "group")].sort_values("match_id")

    rows = []
    model_rows = []          # (pH,pD,pA, actual) for metrics
    for _, r in played.iterrows():
        h, a = r["home"], r["away"]
        hg, ag = int(r["home_goals"]), int(r["away_goals"])
        lh, la = P.lambdas(elo_pre[h], elo_pre[a], True, p)       # neutral
        pH, pD, pA = P.outcome_probs(lh, la)
        pred = "H" if pH >= pD and pH >= pA else ("D" if pD >= pA else "A")
        real = "H" if hg > ag else ("D" if hg == ag else "A")
        rows.append({
            "match_id": int(r["match_id"]), "date": r["date"], "group": r["group"],
            "home": h, "away": a,
            "pred_pH": round(pH, 4), "pred_pD": round(pD, 4), "pred_pA": round(pA, 4),
            "pred_outcome": pred, "pred_likely_score": likely_score(lh, la),
            "real_home_goals": hg, "real_away_goals": ag,
            "real_outcome": real, "hit": pred == real,
        })
        model_rows.append((pH, pD, pA, real))

    # metrics (same definitions as poisson._metrics)
    def metrics(rws):
        eps = 1e-12
        ll = bri = acc = 0.0
        for pH, pD, pA, act in rws:
            pr = {"H": pH, "D": pD, "A": pA}
            ll -= math.log(max(eps, pr[act]))
            onev = {"H": 0.0, "D": 0.0, "A": 0.0}; onev[act] = 1.0
            bri += sum((pr[k] - onev[k]) ** 2 for k in pr)
            best = max(pr, key=pr.get)
            acc += 1.0 if best == act else 0.0
        n = len(rws)
        return {"acc": round(acc / n, 6), "brier": round(bri / n, 6), "log_loss": round(ll / n, 6)}

    base_rate = (0.40, 0.27, 0.33)
    naive_rows = [(*base_rate, r[3]) for r in model_rows]

    # large-sample skill check (8000 historical internationals) - same as poisson.skill_check
    frame = P.prematch_frame()
    sk = P.skill_check(p, frame)
    out = {
        "matches": rows,
        "scorecard": {
            "n": len(rows),
            "model": metrics(model_rows),
            "naive": metrics(naive_rows),
        },
        "large_sample": {
            "n": sk["n"],
            "model": {"acc": sk["model"][2], "brier": sk["model"][1], "log_loss": sk["model"][0]},
            "naive": {"acc": sk["naive"][2], "brier": sk["naive"][1], "log_loss": sk["naive"][0]},
        },
        "methodology": ("Each played group game is predicted from PRE-tournament Elo "
                        "(trained on internationals before 2026-06-11) via the Poisson model, "
                        "at a neutral venue - identical to poisson.backtest(). No leakage: the "
                        "scorecard never uses a game's own result. 'hit' = modal outcome matched."),
        "as_of": "2026-06-24",
    }
    (HERE / "accuracy_28.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    hits = sum(1 for r in rows if r["hit"])
    print(f"wrote accuracy_28.json: n={len(rows)} played group games")
    print(f"  model  acc={out['scorecard']['model']['acc']:.4f} ({hits}/{len(rows)})  "
          f"brier={out['scorecard']['model']['brier']:.4f}  ll={out['scorecard']['model']['log_loss']:.4f}")
    print(f"  naive  acc={out['scorecard']['naive']['acc']:.4f}  "
          f"brier={out['scorecard']['naive']['brier']:.4f}  ll={out['scorecard']['naive']['log_loss']:.4f}")
    print(f"  large-sample (n={sk['n']}): model acc={sk['model'][2]:.4f} vs naive {sk['naive'][2]:.4f}")


if __name__ == "__main__":
    main()
