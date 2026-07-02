"""
05_reputation_size.py — the two mechanisms behind the disagreement.
  ana_09 : reputation vs research/citations — reputation-lifted vs output-lifted schools
           (QS Academic-Reputation sub-score & QS-vs-ARWU rank gap; named universities)
  ana_10 : the size-normalisation flip — volume (works_count) vs per-paper impact
           (Michigan/Toronto-type giants vs Caltech/Princeton-type dense schools)
Run from DATA_DIR:  PYTHONUTF8=1 py "<PROJECT_DIR>/code/05_reputation_size.py"
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c  # noqa: E402

m = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "core_master.csv"))
qs = c.load_qs()
# merge QS indicator sub-scores onto the core
qsub = qs[["key", "ar score", "er score", "fsr score", "cpf score", "ifr score", "isr score"]]
m = m.merge(qsub, on="key", how="left")

# --- ana_09: reputation-lifted vs research-lifted (QS vs ARWU rank gap + QS sub-scores) ---
print("=== ana_09 ===")
m["qs_minus_arwu"] = m["qs_rank"] - m["arwu_rank"]   # negative => QS ranks it HIGHER (reputation lift)
cols = ["the_name", "country", "arwu_rank", "qs_rank", "qs_minus_arwu", "ar score", "cpf score", "oa_rank_works"]
clean = m[(m["arwu_rank"] <= 200) & (m["qs_rank"] <= 200)].copy()
print("(clean cut: both ARWU and QS rank <=200, %d schools, avoids tail-band artefacts)" % len(clean))
print("REPUTATION-LIFTED (QS ranks far ABOVE ARWU; survey opinion > measured research):")
print(clean.sort_values("qs_minus_arwu").head(10)[cols].to_string(index=False))
print("\nRESEARCH-LIFTED (ARWU ranks far ABOVE QS; measured research > reputation):")
print(clean.sort_values("qs_minus_arwu", ascending=False).head(10)[cols].to_string(index=False))
# QS's own internal split: Academic Reputation vs Citations-per-Faculty
sub = m.dropna(subset=["ar score", "cpf score"]).copy()
sub["ar_rank"] = sub["ar score"].rank(ascending=False, method="min")
sub["cpf_rank"] = sub["cpf score"].rank(ascending=False, method="min")
sub["ar_minus_cpf"] = sub["ar_rank"] - sub["cpf_rank"]   # positive => citations rank it higher than reputation
from scipy.stats import spearmanr  # noqa: E402
r, _ = spearmanr(sub["ar score"], sub["cpf score"])
print("\nWithin QS itself, Academic-Reputation score vs Citations-per-Faculty score correlate only Spearman=%.3f "
      "(n=%d) — the survey and the citation metric rank schools differently." % (r, len(sub)))
print("Schools QS's CITATION metric lifts most over its REPUTATION metric (research-dense, low name-recognition):")
print(sub.sort_values("ar_minus_cpf", ascending=False).head(6)[
    ["the_name", "ar score", "cpf score"]].to_string(index=False))
print("Schools QS's REPUTATION metric lifts most over its CITATION metric (famous name, thinner per-faculty citations):")
print(sub.sort_values("ar_minus_cpf").head(6)[
    ["the_name", "ar score", "cpf score"]].to_string(index=False))

# --- ana_10: the size-normalisation flip — volume vs per-paper impact ---
print("=== ana_10 ===")
oa = c.load_openalex()
oa = oa.copy()
oa["cites_per_work"] = oa["cited_by_count"] / oa["works_count"]
oa["rank_volume"] = oa["works_count"].rank(ascending=False, method="min").astype(int)
oa["rank_impact"] = oa["cites_per_work"].rank(ascending=False, method="min").astype(int)
oa["flip"] = oa["rank_impact"] - oa["rank_volume"]   # negative => impact rank much better than volume rank
# restrict to a meaningful set (top-120 by volume) so tiny-count outliers don't dominate per-paper
big = oa[oa["rank_volume"] <= 120].copy()
print("Top of the VOLUME order (works_count) — the sprawling giants:")
print(oa.sort_values("rank_volume").head(8)[
    ["institution", "works_count", "cites_per_work", "rank_volume", "rank_impact"]].to_string(index=False))
print("\nTop of the PER-PAPER IMPACT order (cites/work), within the top-120 by volume — the dense schools:")
print(big.sort_values("cites_per_work", ascending=False).head(8)[
    ["institution", "works_count", "cites_per_work", "rank_volume", "rank_impact"]].to_string(index=False))
# the headline flip, named
for name in ["University of Michigan", "University of Toronto", "Harvard University",
             "California Institute of Technology", "Princeton University",
             "Massachusetts Institute of Technology"]:
    row = oa[oa.institution.str.fullmatch(name, case=False, na=False)]
    if len(row):
        r0 = row.iloc[0]
        print(f"{name}: works={int(r0.works_count):>7} (volume #{int(r0.rank_volume):>3}) | "
              f"cites/work={r0.cites_per_work:5.1f} (impact #{int(r0.rank_impact):>3}) | flip {int(r0.flip):+d}")
print("Two_yr_mean_citedness alt per-paper metric — TOP 6 (note Washington=46 is a flagged data artefact):")
print(oa.sort_values("two_yr_mean_citedness", ascending=False).head(6)[
    ["institution", "two_yr_mean_citedness", "works_count"]].to_string(index=False))
