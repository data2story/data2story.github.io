"""04_seriousness.py — seriousness, death and hospitalization flags."""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:\AI\journalist agent review\phase2\datasets\openfda_faers_2024",
)
sample = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_sample.csv"))
drugs = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_drugs.csv"))

# --- ana_18: Overall seriousness rates ---
print("=== ana_18 ===")
N = len(sample)
serious_n = (sample["serious"] == 1).sum()
notser_n  = (sample["serious"] == 2).sum()
death_n   = (sample["seriousnessdeath"] == 1).sum()
hosp_n    = (sample["seriousnesshospitalization"] == 1).sum()
print(f"total reports: {N:,}")
print(f"serious=1: {serious_n:,} ({serious_n/N*100:.2f}%)")
print(f"serious=2 (not serious): {notser_n:,} ({notser_n/N*100:.2f}%)")
print(f"seriousnessdeath=1: {death_n:,} ({death_n/N*100:.2f}%)")
print(f"seriousnesshospitalization=1: {hosp_n:,} ({hosp_n/N*100:.2f}%)")
print(f"death OR hospitalization: {((sample['seriousnessdeath']==1)|(sample['seriousnesshospitalization']==1)).sum():,}")

# --- ana_19: Seriousness rate per top-20 drug (suspect role only) ---
print("=== ana_19 ===")
import re
def norm(name):
    if not isinstance(name, str): return ""
    n = name.upper().strip()
    n = re.sub(r"\s*\(.*\)\s*", "", n)
    n = re.sub(r"[\.®™©]", "", n)
    n = re.sub(r"\s+", " ", n)
    return n
drugs["m"] = drugs["medicinalproduct"].apply(norm)
sus = drugs[drugs["drugcharacterization"] == 1]
# get top 25 by suspect-rows
top_drugs = sus["m"].value_counts().head(25).index.tolist()
report_serious = sample.set_index("safetyreportid")[["serious", "seriousnessdeath", "seriousnesshospitalization"]]
rows = []
for d in top_drugs:
    reports = sus[sus["m"] == d]["safetyreportid"].unique()
    sub = report_serious.reindex(reports).dropna(subset=["serious"])
    n = len(sub)
    if n == 0:
        continue
    sn = int((sub["serious"] == 1).sum())
    dn = int((sub["seriousnessdeath"] == 1).sum())
    hn = int((sub["seriousnesshospitalization"] == 1).sum())
    rows.append((d, n, sn, dn, hn, sn/n*100, dn/n*100, hn/n*100))
rows.sort(key=lambda r: -r[5])
print("drug\treports\tserious\tdeath\thosp\tserious_pct\tdeath_pct\thosp_pct")
for r in rows:
    print("\t".join(f"{x:.2f}" if isinstance(x, float) else str(x) for x in r))

# --- ana_20: Death-rate hot drugs (require >= 200 suspect-reports to filter noise) ---
print("=== ana_20 ===")
# Build for ALL drugs with >= 200 suspect-reports
agg = (sus.groupby("m")["safetyreportid"].nunique()
       .reset_index().rename(columns={"safetyreportid": "n_reports"}))
agg = agg[agg["n_reports"] >= 200].copy()
# For each: join to seriousness
def stats_for(name):
    reports = sus[sus["m"] == name]["safetyreportid"].unique()
    sub = report_serious.reindex(reports).dropna(subset=["serious"])
    n = len(sub)
    if n == 0: return (0, 0, 0)
    return (n, int((sub["seriousnessdeath"] == 1).sum()),
            int((sub["seriousnesshospitalization"] == 1).sum()))
stats = agg["m"].apply(stats_for)
agg["n"] = stats.apply(lambda x: x[0])
agg["death"] = stats.apply(lambda x: x[1])
agg["hosp"]  = stats.apply(lambda x: x[2])
agg["death_pct"] = agg["death"] / agg["n"] * 100
agg["hosp_pct"]  = agg["hosp"]  / agg["n"] * 100
print("TOP-30 by death_pct (>=200 reports):")
print(agg.sort_values("death_pct", ascending=False).head(30)[
    ["m", "n_reports", "death", "death_pct", "hosp", "hosp_pct"]
].to_string(index=False))

print()
print("TOP-30 by hosp_pct (>=200 reports):")
print(agg.sort_values("hosp_pct", ascending=False).head(30)[
    ["m", "n_reports", "death", "death_pct", "hosp", "hosp_pct"]
].to_string(index=False))

# --- ana_21: How many reports per safetyreportid map to multiple events ---
print("=== ana_21 ===")
# Are reports with more drugs more likely to be serious?
sample["n_drugs_band"] = pd.cut(sample["n_drugs"], bins=[0,1,2,3,5,10,20,2000],
                                labels=["1","2","3","4-5","6-10","11-20","21+"])
ser_by_drugs = sample.groupby("n_drugs_band", observed=True)["serious"].agg(
    n="count", serious=lambda x: (x==1).sum())
ser_by_drugs["pct_serious"] = ser_by_drugs["serious"] / ser_by_drugs["n"] * 100
print(ser_by_drugs.to_string())
