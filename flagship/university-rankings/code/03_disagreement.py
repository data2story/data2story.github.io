"""
03_disagreement.py — the spine: how weakly the 4 commercial systems agree.
  ana_04 : pairwise Spearman + Kendall rank correlations (6 pairs) on the 5-way core
  ana_05 : distribution of per-university rank SPREAD (max-min over 4 systems) + swingers/anchors
  ana_06 : each system's top-10 side by side (they crown different #1s)
Run from DATA_DIR:  PYTHONUTF8=1 py "<PROJECT_DIR>/code/03_disagreement.py"
"""
import os
import sys
import pandas as pd
from scipy.stats import spearmanr, kendalltau

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c  # noqa: E402

m = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "core_master.csv"))
SYS = ["the_rank", "arwu_rank", "cwur_rank", "qs_rank"]
LAB = {"the_rank": "THE", "arwu_rank": "ARWU", "cwur_rank": "CWUR", "qs_rank": "QS"}

# --- ana_04: pairwise rank correlations among the 4 commercial systems ---
print("=== ana_04 ===")
rows = []
for i in range(len(SYS)):
    for j in range(i + 1, len(SYS)):
        a, b = SYS[i], SYS[j]
        sub = m[[a, b]].dropna()
        rho, _ = spearmanr(sub[a], sub[b])
        tau, _ = kendalltau(sub[a], sub[b])
        rows.append((LAB[a], LAB[b], len(sub), round(rho, 3), round(tau, 3)))
        print(f"{LAB[a]:>4} vs {LAB[b]:<4}  n={len(sub):3d}  Spearman={rho:.3f}  Kendall={tau:.3f}")
rows_sorted = sorted(rows, key=lambda r: r[3])
print("MOST alike pair (highest Spearman):", rows_sorted[-1][:2], rows_sorted[-1][3])
print("LEAST alike pair (lowest Spearman):", rows_sorted[0][:2], rows_sorted[0][3])
print("Spearman range across the 6 pairs: %.3f to %.3f" % (rows_sorted[0][3], rows_sorted[-1][3]))

# --- ana_05: per-university rank SPREAD (max-min across the 4 systems) + swingers ---
print("=== ana_05 ===")
m["rank_min"] = m[SYS].min(axis=1)
m["rank_max"] = m[SYS].max(axis=1)
m["spread"] = m["rank_max"] - m["rank_min"]
print("Spread distribution over the 218-school core:")
print(m["spread"].describe()[["min", "25%", "50%", "75%", "max"]].round(1).to_dict(),
      "| mean=%.1f" % m["spread"].mean())
cols = ["the_name", "country", "the_rank", "arwu_rank", "cwur_rank", "qs_rank", "oa_rank_works", "spread"]
print("\nBIGGEST swingers (largest max-min rank gap across the 4 systems):")
print(m.sort_values("spread", ascending=False).head(12)[cols].to_string(index=False))
print("\nSMALLEST spread (the anchors the systems agree on):")
print(m.sort_values("spread").head(12)[cols].to_string(index=False))
print("\nNOTE: the raw biggest-spread list is partly inflated by tail BANDS "
      "(THE '351-400', QS '1001-1200' etc. stored at their lower bound).")

# --- ana_05b: RECOGNISABLE swingers (all four ranks clean, i.e. <=200) + named characters ---
print("=== ana_05b ===")
clean = m[(m[SYS].max(axis=1) <= 200)].copy()
print("Schools ranked <=200 by ALL FOUR systems:", len(clean))
print("\nBiggest CLEAN swingers (recognisable schools, no tail-band inflation):")
print(clean.sort_values("spread", ascending=False).head(12)[cols].to_string(index=False))
# named load-bearing characters explicitly
chars = ["california institute technology", "michigan", "california berkeley",
         "princeton", "tsinghua", "peking", "yale", "sao paulo", "tokyo",
         "harvard", "massachusetts institute technology", "oxford"]
named = m[m.key.isin(chars)].copy()
print("\nNamed load-bearing characters (per-system ranks + OpenAlex output rank):")
print(named.sort_values("oa_rank_works")[cols].to_string(index=False))

# --- ana_06: each system's TOP 10 side by side (different #1, different membership) ---
print("=== ana_06 ===")
the = c.load_the(); arwu = c.load_arwu(); cwur = c.load_cwur(); qs = c.load_qs(); oa = c.load_openalex()
def top10(df, namecol, ranksort):
    return df.sort_values(ranksort).head(10)[namecol].tolist()
t10 = {
    "THE 2015": top10(the, "university_name", "rank_num"),
    "ARWU 2015": top10(arwu, "university_name", "rank_num"),
    "CWUR 2015": top10(cwur, "institution", "rank_num"),
    "QS 2023": top10(qs, "institution", "rank_num"),
    "OpenAlex (works)": oa.sort_values("works_count", ascending=False).head(10)["institution"].tolist(),
}
tbl = pd.DataFrame({k: v for k, v in t10.items()})
tbl.index = range(1, 11)
print(tbl.to_string())
print("\n#1 of each table:", {k: v[0] for k, v in t10.items()})
# how much do the top-10 sets overlap?
sets = {k: set(c.normalize_name(x) for x in v) for k, v in t10.items() if k != "OpenAlex (works)"}
inter = set.intersection(*sets.values())
union = set.union(*sets.values())
print("Universities in ALL FOUR commercial top-10s:", len(inter), "of", len(union), "distinct names that appear in any top-10")
