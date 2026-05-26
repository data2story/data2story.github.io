"""07_glp1.py — GLP-1 family deep dive: brands, reactions, demographics, seriousness."""
import os, re
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

GLP1 = {
    "semaglutide": ["OZEMPIC", "WEGOVY", "RYBELSUS", "SEMAGLUTIDE"],
    "tirzepatide": ["MOUNJARO", "ZEPBOUND", "TIRZEPATIDE"],
    "liraglutide": ["VICTOZA", "SAXENDA", "LIRAGLUTIDE"],
    "dulaglutide": ["TRULICITY", "DULAGLUTIDE"],
    "exenatide":   ["BYETTA", "BYDUREON", "EXENATIDE"],
}
brand_to_generic = {b: g for g, bs in GLP1.items() for b in bs}

def match(name):
    if not isinstance(name, str): return None
    n = name.upper()
    for b, g in brand_to_generic.items():
        if b in n: return g
    return None

drugs["glp1"] = drugs["m"].apply(match)
glp1_rows = drugs[drugs["glp1"].notna()]
glp1_reports = set(glp1_rows["safetyreportid"].unique())

# --- ana_32: Mounjaro vs Ozempic head-to-head (suspect role) ---
print("=== ana_32 ===")
brands = ["OZEMPIC", "WEGOVY", "RYBELSUS", "MOUNJARO", "ZEPBOUND", "TRULICITY", "VICTOZA", "SAXENDA"]
report_summary = sample.set_index("safetyreportid")[
    ["serious", "seriousnessdeath", "seriousnesshospitalization", "patient_sex", "patient_onset_age", "patient_onset_age_unit", "occurcountry"]
]
rows = []
for b in brands:
    sub = drugs[(drugs["m"] == b) & (drugs["drugcharacterization"] == 1)]
    reports = sub["safetyreportid"].unique()
    info = report_summary.reindex(reports).dropna(subset=["serious"])
    n = len(info)
    if n == 0: continue
    ser = int((info["serious"] == 1).sum())
    death = int((info["seriousnessdeath"] == 1).sum())
    hosp = int((info["seriousnesshospitalization"] == 1).sum())
    female = int((info["patient_sex"] == 2).sum())
    male = int((info["patient_sex"] == 1).sum())
    sex_known = female + male
    us = int((info["occurcountry"] == "US").sum())
    yrs = info[info["patient_onset_age_unit"] == 801]["patient_onset_age"]
    age_known = len(yrs)
    median_age = yrs.median() if len(yrs) else None
    rows.append((b, n, ser, death, hosp,
                 ser/n*100, death/n*100, hosp/n*100,
                 female, male, female/sex_known*100 if sex_known else 0,
                 us, us/n*100,
                 age_known, median_age))
print("brand\treports\tserious\tdeath\thosp\tser%\tdth%\thsp%\tfemale\tmale\tfemale%\tUS\tUS%\tage_known\tmed_age")
for r in rows:
    print("\t".join(f"{x:.2f}" if isinstance(x, float) else str(x) for x in r))

# --- ana_33: Top reactions for Mounjaro & Ozempic ---
print("=== ana_33 ===")
def top_reactions_for(brand, k=20):
    rep = set(drugs[(drugs["m"] == brand) & (drugs["drugcharacterization"] == 1)]["safetyreportid"].unique())
    rx = reactions[reactions["safetyreportid"].isin(rep)]
    n_rep = len(rep)
    if n_rep == 0:
        return n_rep, pd.Series(dtype=int)
    return n_rep, rx["reactionmeddrapt"].value_counts().head(k)

for brand in ["MOUNJARO", "OZEMPIC", "ZEPBOUND", "WEGOVY", "TRULICITY"]:
    n_rep, top = top_reactions_for(brand, k=20)
    print(f"\n--- {brand} (n_reports={n_rep:,}) ---")
    for pt, c in top.items():
        print(f"{pt}\t{c:,}\t{c/n_rep*100:.1f}% of reports")

# --- ana_34: All FAERS reactions vs GLP-1 reactions — over-represented terms ---
print("=== ana_34 ===")
glp1_rx = reactions[reactions["safetyreportid"].isin(glp1_reports)]
print(f"GLP-1 reports: {len(glp1_reports):,}")
print(f"GLP-1 reaction rows: {len(glp1_rx):,}")

# Compute over-representation
all_pt = reactions["reactionmeddrapt"].value_counts()
all_total = len(reactions)
glp1_pt = glp1_rx["reactionmeddrapt"].value_counts()
glp1_total = len(glp1_rx)

df = pd.DataFrame({
    "glp1_count": glp1_pt,
    "all_count": all_pt
}).fillna(0)
df = df[df["glp1_count"] >= 80]  # filter noise
df["glp1_pct"] = df["glp1_count"] / glp1_total * 100
df["all_pct"]  = df["all_count"] / all_total * 100
df["lift"] = df["glp1_pct"] / df["all_pct"]
print("\nTop 30 reactions OVER-represented in GLP-1 reports (lift, requires >=80 GLP-1 occurrences):")
print(df.sort_values("lift", ascending=False).head(30)[["glp1_count", "glp1_pct", "all_pct", "lift"]].round(3).to_string())

# --- ana_35: Sex skew in GLP-1 reports ---
print("=== ana_35 ===")
glp1_sample = sample[sample["safetyreportid"].isin(glp1_reports)]
sex_map = {0: "Unknown", 1: "Male", 2: "Female"}
print("GLP-1 reports sex distribution:")
print(glp1_sample["patient_sex"].value_counts(dropna=False).to_string())
fem_glp1 = (glp1_sample["patient_sex"] == 2).sum()
mal_glp1 = (glp1_sample["patient_sex"] == 1).sum()
print(f"Female: {fem_glp1:,} ({fem_glp1/(fem_glp1+mal_glp1)*100:.1f}% of sex-known)")
print(f"Male:   {mal_glp1:,} ({mal_glp1/(fem_glp1+mal_glp1)*100:.1f}% of sex-known)")

# Compare with overall
total_fem = (sample["patient_sex"] == 2).sum()
total_mal = (sample["patient_sex"] == 1).sum()
print(f"All reports: Female {total_fem/(total_fem+total_mal)*100:.1f}%, Male {total_mal/(total_fem+total_mal)*100:.1f}%")
