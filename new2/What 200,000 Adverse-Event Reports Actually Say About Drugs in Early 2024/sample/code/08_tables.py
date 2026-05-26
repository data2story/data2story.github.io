"""08_tables.py — generate the chart-ready data_table values referenced in analyst.json.

This script is the canonical reference for every Vega-Lite chart in the blog.
Each table prints with === ana_NN_table === so the programmer can grep for it.
"""
import os, re, json
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:\AI\journalist agent review\phase2\datasets\openfda_faers_2024",
)
sample = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_sample.csv"))
drugs = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_drugs.csv"))
reactions = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_reactions.csv"))


def norm(name):
    if not isinstance(name, str): return ""
    n = name.upper().strip()
    n = re.sub(r"\s*\(.*\)\s*", "", n)
    n = re.sub(r"[\.®™©]", "", n)
    n = re.sub(r"\s+", " ", n)
    return n
drugs["m"] = drugs["medicinalproduct"].apply(norm)

sample["dt"] = pd.to_datetime(sample["receivedate"].astype(str), format="%Y%m%d", errors="coerce")

# ana_06 table — top 25 drugs (any role)
print("=== ana_06_table ===")
top_any = drugs["m"].value_counts().head(25)
total = len(drugs)
for d, n in top_any.items():
    print(f"{d}|{n}|{n/total*100:.2f}")

# ana_07 table — top 25 suspect drugs
print("=== ana_07_table ===")
sus = drugs[drugs["drugcharacterization"] == 1]
top_sus = sus["m"].value_counts().head(25)
total_sus = len(sus)
for d, n in top_sus.items():
    print(f"{d}|{n}|{n/total_sus*100:.2f}")

# ana_08 table — role mix for the top 12 by total
print("=== ana_08_table ===")
top12 = drugs["m"].value_counts().head(12).index.tolist()
for d in top12:
    sub = drugs[drugs["m"] == d]
    s = (sub["drugcharacterization"] == 1).sum()
    c = (sub["drugcharacterization"] == 2).sum()
    i = (sub["drugcharacterization"] == 3).sum()
    print(f"{d}|{s}|{c}|{i}")

# ana_09 table — GLP-1 by generic
print("=== ana_09_table ===")
GLP1 = {
    "Semaglutide (Ozempic / Wegovy / Rybelsus)": ["OZEMPIC", "WEGOVY", "RYBELSUS", "SEMAGLUTIDE"],
    "Tirzepatide (Mounjaro / Zepbound)":        ["MOUNJARO", "ZEPBOUND", "TIRZEPATIDE"],
    "Dulaglutide (Trulicity)":                   ["TRULICITY", "DULAGLUTIDE"],
    "Liraglutide (Victoza / Saxenda)":          ["VICTOZA", "SAXENDA", "LIRAGLUTIDE"],
    "Exenatide (Byetta / Bydureon)":            ["BYETTA", "BYDUREON", "EXENATIDE"],
}
b2g = {b: g for g, bs in GLP1.items() for b in bs}
def gmatch(n):
    if not isinstance(n, str): return None
    nu = n.upper()
    for b, g in b2g.items():
        if b in nu: return g
    return None
drugs["glp1g"] = drugs["m"].apply(gmatch)
glp1 = drugs[drugs["glp1g"].notna()]
for g in GLP1:
    n = (glp1["glp1g"] == g).sum()
    print(f"{g}|{n}")

# ana_12 table — top 30 reactions
print("=== ana_12_table ===")
top_pt = reactions["reactionmeddrapt"].value_counts().head(30)
N_rx = len(reactions)
for pt, n in top_pt.items():
    print(f"{pt}|{n}|{n/N_rx*100:.2f}")

# ana_13 table — concentration curve
print("=== ana_13_table ===")
vc = reactions["reactionmeddrapt"].value_counts()
for N in [10, 25, 50, 100, 250, 500, 1000, 2000, 5000]:
    if len(vc) >= N:
        share = vc.head(N).sum() / N_rx * 100
        print(f"{N}|{share:.2f}")

# ana_14 table — reaction outcome
print("=== ana_14_table ===")
labels = {1: "Recovered / resolved", 2: "Recovering / resolving",
          3: "Not recovered / not resolved", 4: "Recovered with sequelae",
          5: "Fatal", 6: "Unknown"}
out_vc = reactions["reactionoutcome"].value_counts(dropna=False)
for code in [1,2,3,4,5,6]:
    n = int(out_vc.get(code, 0))
    print(f"{labels[code]}|{n}|{n/N_rx*100:.2f}")
miss = int(reactions["reactionoutcome"].isna().sum())
print(f"Missing|{miss}|{miss/N_rx*100:.2f}")

# ana_18 table — seriousness summary
print("=== ana_18_table ===")
N = len(sample)
print(f"All reports|{N}")
print(f"Serious (any)|{int((sample['serious']==1).sum())}")
print(f"Hospitalization|{int((sample['seriousnesshospitalization']==1).sum())}")
print(f"Death|{int((sample['seriousnessdeath']==1).sum())}")

# ana_20 table — top 20 drugs by death_pct (>=200 suspect-reports)
print("=== ana_20_table ===")
report_serious = sample.set_index("safetyreportid")[["serious", "seriousnessdeath", "seriousnesshospitalization"]]
agg = (sus.groupby("m")["safetyreportid"].nunique()
       .reset_index().rename(columns={"safetyreportid": "n_reports"}))
agg = agg[agg["n_reports"] >= 200]
out = []
for d in agg["m"]:
    reports = sus[sus["m"] == d]["safetyreportid"].unique()
    info = report_serious.reindex(reports).dropna(subset=["serious"])
    n = len(info)
    if n == 0: continue
    death = int((info["seriousnessdeath"] == 1).sum())
    hosp = int((info["seriousnesshospitalization"] == 1).sum())
    out.append((d, n, death, hosp, death/n*100, hosp/n*100))
out_df = pd.DataFrame(out, columns=["drug", "n", "death", "hosp", "death_pct", "hosp_pct"])
for r in out_df.sort_values("death_pct", ascending=False).head(20).itertuples():
    print(f"{r.drug}|{r.n}|{r.death}|{r.death_pct:.2f}|{r.hosp}|{r.hosp_pct:.2f}")

# ana_22 table — sex
print("=== ana_22_table ===")
print(f"Female|{int((sample['patient_sex']==2).sum())}")
print(f"Male|{int((sample['patient_sex']==1).sum())}")
print(f"Unknown (0)|{int((sample['patient_sex']==0).sum())}")
print(f"Missing|{int(sample['patient_sex'].isna().sum())}")

# ana_23 table — age bands
print("=== ana_23_table ===")
yrs = sample[(sample["patient_onset_age_unit"] == 801) & sample["patient_onset_age"].notna()].copy()
bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 200]
labels = ["Under 18", "18–29", "30–39", "40–49", "50–59", "60–69", "70–79", "80–89", "90+"]
yrs["band"] = pd.cut(yrs["patient_onset_age"], bins=bins, labels=labels, right=False, include_lowest=True)
for lab in labels:
    n = int((yrs["band"] == lab).sum())
    print(f"{lab}|{n}")

# ana_25 table — top countries by occur
print("=== ana_25_table ===")
occ = sample["occurcountry"].value_counts(dropna=False).head(15)
for c, n in occ.items():
    cs = c if isinstance(c, str) else "Unknown"
    print(f"{cs}|{int(n)}")

# ana_29 table — daily volume
print("=== ana_29_table ===")
daily = sample.groupby(sample["dt"].dt.date).size()
for d, n in daily.items():
    print(f"{d}|{int(n)}")

# ana_30 table — day-of-week
print("=== ana_30_table ===")
sample["dow"] = sample["dt"].dt.day_name()
dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
dow_vc = sample["dow"].value_counts().reindex(dow_order)
for d, n in dow_vc.items():
    print(f"{d}|{int(n)}")

# ana_32 table — GLP-1 brand head-to-head (suspect-only)
print("=== ana_32_table ===")
brands = ["MOUNJARO", "OZEMPIC", "ZEPBOUND", "TRULICITY", "WEGOVY", "RYBELSUS", "VICTOZA", "SAXENDA"]
report_summary = sample.set_index("safetyreportid")[
    ["serious", "seriousnessdeath", "seriousnesshospitalization", "patient_sex", "patient_onset_age",
     "patient_onset_age_unit", "occurcountry"]
]
for b in brands:
    sub = drugs[(drugs["m"] == b) & (drugs["drugcharacterization"] == 1)]
    reports = sub["safetyreportid"].unique()
    info = report_summary.reindex(reports).dropna(subset=["serious"])
    n = len(info)
    if n == 0: continue
    ser = int((info["serious"] == 1).sum())
    dth = int((info["seriousnessdeath"] == 1).sum())
    hsp = int((info["seriousnesshospitalization"] == 1).sum())
    fem = int((info["patient_sex"] == 2).sum())
    mal = int((info["patient_sex"] == 1).sum())
    us  = int((info["occurcountry"] == "US").sum())
    yrs = info[info["patient_onset_age_unit"] == 801]["patient_onset_age"]
    med = yrs.median() if len(yrs) else None
    print(f"{b}|{n}|{ser/n*100:.2f}|{dth/n*100:.2f}|{hsp/n*100:.2f}|{fem/(fem+mal)*100 if (fem+mal) else 0:.2f}|{us/n*100:.2f}|{med}")

# ana_33 table — top 12 reactions per top GLP-1 brand
print("=== ana_33_table ===")
for brand in ["MOUNJARO", "OZEMPIC", "ZEPBOUND", "WEGOVY", "TRULICITY"]:
    rep = set(drugs[(drugs["m"] == brand) & (drugs["drugcharacterization"] == 1)]["safetyreportid"].unique())
    rx = reactions[reactions["safetyreportid"].isin(rep)]
    n_rep = len(rep)
    if n_rep == 0: continue
    for pt, c in rx["reactionmeddrapt"].value_counts().head(12).items():
        print(f"{brand}|{pt}|{c}|{c/n_rep*100:.2f}")

# ana_34 table — top 20 over-represented in GLP-1 reports
print("=== ana_34_table ===")
glp1_reports = set(drugs[drugs["glp1g"].notna()]["safetyreportid"].unique())
glp1_rx = reactions[reactions["safetyreportid"].isin(glp1_reports)]
all_pt = reactions["reactionmeddrapt"].value_counts()
glp1_pt = glp1_rx["reactionmeddrapt"].value_counts()
df_lift = pd.DataFrame({"glp1_count": glp1_pt, "all_count": all_pt}).fillna(0)
df_lift = df_lift[df_lift["glp1_count"] >= 80]
df_lift["glp1_pct"] = df_lift["glp1_count"] / len(glp1_rx) * 100
df_lift["all_pct"] = df_lift["all_count"] / len(reactions) * 100
df_lift["lift"] = df_lift["glp1_pct"] / df_lift["all_pct"]
for r in df_lift.sort_values("lift", ascending=False).head(20).itertuples():
    print(f"{r.Index}|{int(r.glp1_count)}|{r.glp1_pct:.3f}|{r.all_pct:.3f}|{r.lift:.2f}")

# ana_28 table — reporter type
print("=== ana_28_table ===")
report_type_map = {1: "Spontaneous", 2: "Study", 3: "Other", 4: "Not available to sender"}
rt = sample["reporttype"].value_counts(dropna=False)
for code in [1, 2, 3]:
    n = int(rt.get(code, 0))
    print(f"{report_type_map[code]}|{n}")
print(f"Missing|{int(sample['reporttype'].isna().sum())}")
