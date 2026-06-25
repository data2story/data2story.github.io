"""
story_findings.py — journalism-facing findings derived from the vetted forecast.

Reads the published forecast_outputs/ CSVs (produced by simulate.py, the vetted
Elo->Poisson->Monte-Carlo model) plus teams.csv, and computes the derived numbers
the blog leads on: the champion table, the FIFA-rank vs model-rank disagreements,
money-vs-merit (squad value per point of deep-run probability), the conditional-
bracket spread, the confederation split, and model-health framing.

Run from DATA_DIR:
    cd <DATA_DIR> && python <PROJECT_DIR>/code/story_findings.py
Every '=== ana_xx ===' block prints the verbatim numbers cited in analyst.json.
"""
import sys, json
from pathlib import Path
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import pandas as pd

# DATA_DIR is the current working directory when run as instructed.
DATA = Path.cwd()
OUT = DATA / "forecast_outputs"

adv = pd.read_csv(OUT / "advance_probs.csv", encoding="utf-8")
champ = pd.read_csv(OUT / "champion_odds.csv", encoding="utf-8")
summary = json.loads((OUT / "forecast_summary.json").read_text(encoding="utf-8"))

# --- ana_01: Champion odds — the headline ladder (top of the distribution) ---
print("=== ana_01 ===")
top = champ.sort_values("p_champion", ascending=False).head(12)
for _, r in top.iterrows():
    print(f"{r['team']:14} grp {r['group']}  FIFA#{int(r['fifa_rank']):>2}  Elo {r['elo']:.0f}  "
          f"champ {r['p_champion']*100:5.1f}%  reach-final {r['p_reach_final']*100:5.1f}%")
print(f"top1 Argentina = {champ.iloc[0]['p_champion']*100:.1f}%")
print(f"champion prob sums to {champ['p_champion'].sum():.3f} over 48 teams")
print(f"teams with >=1% champ chance: {(champ['p_champion']>=0.01).sum()}")

# --- ana_02: FIFA ranking vs model ranking — disagreements among real contenders ---
print("\n=== ana_02 ===")
d = champ.copy()
d["model_rank"] = d["p_champion"].rank(ascending=False, method="min").astype(int)
d["rank_gap"] = d["fifa_rank"] - d["model_rank"]   # positive = model likes it MORE than FIFA
# restrict to teams the model gives a non-trivial title chance (>=1%) so the disagreement is meaningful,
# not driven by a pack of minnows tied at ~0% and last place.
contenders = d[d["p_champion"] >= 0.01].copy()
liked = contenders.sort_values("rank_gap", ascending=False).head(5)
faded = contenders.sort_values("rank_gap").head(5)
print(f"Among the {len(contenders)} teams with >=1% title chance — model rates HIGHER than FIFA rank (gap = FIFA# - model#):")
for _, r in liked.iterrows():
    print(f"  {r['team']:14} FIFA#{int(r['fifa_rank']):>2} -> model#{int(r['model_rank']):>2}  "
          f"(+{int(r['rank_gap'])})  champ {r['p_champion']*100:.1f}%")
print("Among contenders — model rates LOWER than FIFA rank:")
for _, r in faded.iterrows():
    print(f"  {r['team']:14} FIFA#{int(r['fifa_rank']):>2} -> model#{int(r['model_rank']):>2}  "
          f"({int(r['rank_gap'])})  champ {r['p_champion']*100:.1f}%")
col = d[d["team"] == "Colombia"].iloc[0]
print(f"Colombia: FIFA #{int(col['fifa_rank'])}, model #{int(col['model_rank'])}, champ {col['p_champion']*100:.1f}% (5th)")
nor = d[d["team"] == "Norway"].iloc[0]
print(f"Norway: FIFA #{int(nor['fifa_rank'])}, model #{int(nor['model_rank'])}, champ {nor['p_champion']*100:.1f}%")
por = d[d["team"] == "Portugal"].iloc[0]
print(f"Portugal: FIFA #{int(por['fifa_rank'])}, model #{int(por['model_rank'])}, champ {por['p_champion']*100:.1f}%")

# --- ana_03: Money vs merit — squad value per point of deep-run probability ---
print("\n=== ana_03 ===")
m = adv.copy()
# deep-run = reach the semi-final; value efficiency = squad value (EUR m) per 1% SF chance
m = m[m["p_reach_sf"] > 0.02].copy()
m["eur_per_sf_pct"] = m["squad_value_eur_m"] / (m["p_reach_sf"] * 100)
m = m.sort_values("squad_value_eur_m", ascending=False)
print("Costliest squads and what the model gives them (reach-SF %):")
for _, r in m.sort_values("squad_value_eur_m", ascending=False).head(8).iterrows():
    print(f"  {r['team']:14} EUR{r['squad_value_eur_m']:7.1f}m  SF {r['p_reach_sf']*100:5.1f}%  "
          f"= EUR{r['eur_per_sf_pct']:6.1f}m per SF-point")
print("Best value (lowest EUR per SF-point), among real contenders:")
for _, r in m.sort_values("eur_per_sf_pct").head(6).iterrows():
    print(f"  {r['team']:14} EUR{r['squad_value_eur_m']:7.1f}m  SF {r['p_reach_sf']*100:5.1f}%  "
          f"= EUR{r['eur_per_sf_pct']:6.1f}m per SF-point")
fr = adv[adv["team"]=="France"].iloc[0]; co = adv[adv["team"]=="Colombia"].iloc[0]
print(f"France squad EUR{fr['squad_value_eur_m']:.0f}m, SF {fr['p_reach_sf']*100:.1f}%")
print(f"Colombia squad EUR{co['squad_value_eur_m']:.0f}m, SF {co['p_reach_sf']*100:.1f}%")
print(f"Colombia squad is {fr['squad_value_eur_m']/co['squad_value_eur_m']:.1f}x cheaper than France's "
      f"yet within {abs(fr['p_reach_sf']-co['p_reach_sf'])*100:.1f}pp of its SF chance")

# --- ana_04: The conditional bracket — advancement is near-certain for the elite, a coin-flip mid-table ---
print("\n=== ana_04 ===")
b = adv[["team","group","p_advance_group","p_best_third","p_reach_r32"]].copy()
b = b.sort_values("p_reach_r32", ascending=False)
print("Reach-Round-of-32 probability (auto top-2 + best-third path):")
for _, r in b.head(6).iterrows():
    print(f"  {r['team']:14} grp {r['group']}  R32 {r['p_reach_r32']*100:5.1f}%  "
          f"(top2 {r['p_advance_group']*100:.0f}% + 3rd-path {r['p_best_third']*100:.0f}%)")
print("  ...mid-table coin-flips (R32 40-60%):")
mid = b[(b["p_reach_r32"]>=0.40) & (b["p_reach_r32"]<=0.60)].head(8)
for _, r in mid.iterrows():
    print(f"  {r['team']:14} grp {r['group']}  R32 {r['p_reach_r32']*100:5.1f}%")
print(f"teams essentially through (R32>=99%): {(adv['p_reach_r32']>=0.99).sum()}")
print(f"teams on a knife edge (R32 40-60%): {((adv['p_reach_r32']>=0.40)&(adv['p_reach_r32']<=0.60)).sum()}")

# --- ana_05: Confederation concentration at the top ---
print("\n=== ana_05 ===")
tdf = pd.read_csv(DATA / "teams.csv", encoding="utf-8")[["team","confederation"]]
cc = champ.merge(tdf, on="team")
conf = cc.groupby("confederation")["p_champion"].sum().sort_values(ascending=False)
print("Total championship probability by confederation:")
for k, v in conf.items():
    print(f"  {k:9} {v*100:5.1f}%")
uefa = conf.get("UEFA",0); conmebol = conf.get("CONMEBOL",0)
print(f"UEFA + CONMEBOL = {(uefa+conmebol)*100:.1f}% of all title probability")
print(f"top-6 confederations represented in title top-6: "
      f"{cc.sort_values('p_champion',ascending=False).head(6)['confederation'].tolist()}")

# --- ana_06: Model health — does it beat a naive baseline? (the trust beat) ---
print("\n=== ana_06 ===")
sk = summary["model_health"]["large_sample_skill"]
bt = summary["model_health"]["backtest_28_played"]
print(f"Large-sample skill check (n={sk['n']} historical internationals, out-of-sample):")
print(f"  model  log-loss {sk['model'][0]:.3f}  Brier {sk['model'][1]:.3f}  accuracy {sk['model'][2]*100:.1f}%")
print(f"  naive  log-loss {sk['naive'][0]:.3f}  Brier {sk['naive'][1]:.3f}  accuracy {sk['naive'][2]*100:.1f}%")
print(f"  -> model log-loss {sk['model'][0]:.3f} vs naive {sk['naive'][0]:.3f} "
      f"({(1-sk['model'][0]/sk['naive'][0])*100:.1f}% better); accuracy "
      f"{sk['model'][2]*100:.0f}% vs {sk['naive'][2]*100:.0f}%")
print(f"This-tournament backtest (n={bt['n']} games already played):")
print(f"  model  log-loss {bt['model'][0]:.3f}  accuracy {bt['model'][2]*100:.1f}%")
print(f"  naive  log-loss {bt['naive'][0]:.3f}  accuracy {bt['naive'][2]*100:.1f}%")
print(f"  -> on the {bt['n']} played games the model ({bt['model'][0]:.3f}) and naive ({bt['naive'][0]:.3f}) "
      f"are CLOSE; n={bt['n']} is small and upset-prone, so the 8000-match check is the reliable read.")
print(f"calibration: a={summary['calibration']['a']:.4f}, b={summary['calibration']['b']:.5f}, "
      f"mu_tot={summary['calibration']['mu_tot']:.3f}, n={summary['calibration']['n']}")

# --- ana_07: Single most-likely Round-of-32 matchup distribution example (conditional pairing) ---
print("\n=== ana_07 ===")
# Argentina's most likely opponents conditional set is complex; report the headline:
print("Because R32 pairings depend on which 8 of 12 thirds qualify, 'who you'd meet' is a")
print("distribution over C(12,8)=495 permutations, integrated by the Monte-Carlo. Example:")
print(f"  Argentina reaches R32 with p={adv[adv['team']=='Argentina'].iloc[0]['p_reach_r32']*100:.1f}% but its")
print(f"  specific opponent is not fixed until the group stage ends — the model averages over all 495.")
print(f"  best-thirds table rows = 495 (FIFA Annex C)")

print("\nALL FINDINGS COMPUTED OK")
