"""02_drugs.py — drug-side analysis: ranking, GLP-1 zoom, drug roles."""
import os, re
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:\AI\journalist agent review\phase2\datasets\openfda_faers_2024",
)
drugs = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_drugs.csv"))
sample = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_sample.csv"))


def norm(name):
    if not isinstance(name, str):
        return ""
    n = name.upper().strip()
    n = re.sub(r"\s*\(.*\)\s*", "", n)  # drop parenthetical
    n = re.sub(r"[\.®™©]", "", n)
    n = re.sub(r"\s+", " ", n)
    return n


drugs["medicinalproduct_norm"] = drugs["medicinalproduct"].apply(norm)

# --- ana_06: Top 30 most-reported drug names (any role) ---
print("=== ana_06 ===")
top = drugs["medicinalproduct_norm"].value_counts().head(30)
total_drug_rows = len(drugs)
for name, n in top.items():
    print(f"{name}\t{n:,}\t{n/total_drug_rows*100:.2f}%")
print(f"total drug rows: {total_drug_rows:,}")
print(f"unique drug names (raw): {drugs['medicinalproduct'].nunique():,}")
print(f"unique drug names (normalized): {drugs['medicinalproduct_norm'].nunique():,}")

# --- ana_07: Top 30 SUSPECT drugs (drugcharacterization == 1) ---
print("=== ana_07 ===")
sus = drugs[drugs["drugcharacterization"] == 1]
top_sus = sus["medicinalproduct_norm"].value_counts().head(30)
total_sus = len(sus)
for name, n in top_sus.items():
    print(f"{name}\t{n:,}\t{n/total_sus*100:.2f}%")
print(f"total suspect-drug rows: {total_sus:,}")

# --- ana_08: How often each top drug is the SUSPECT vs Concomitant ---
print("=== ana_08 ===")
top_names = top.index[:20]
rows = []
for n in top_names:
    sub = drugs[drugs["medicinalproduct_norm"] == n]
    total = len(sub)
    role_counts = sub["drugcharacterization"].value_counts()
    suspect = int(role_counts.get(1, 0))
    concomitant = int(role_counts.get(2, 0))
    interacting = int(role_counts.get(3, 0))
    other = total - suspect - concomitant - interacting
    rows.append((n, total, suspect, concomitant, interacting, other,
                 suspect/total*100, concomitant/total*100))
print("drug\ttotal\tsuspect\tconcom\tinteract\tother\tsuspect_pct\tconcom_pct")
for r in rows:
    print("\t".join(str(x) for x in r))

# --- ana_09: GLP-1 receptor agonist family — every brand+generic ---
print("=== ana_09 ===")
GLP1_PATTERNS = {
    "semaglutide": ["OZEMPIC", "WEGOVY", "RYBELSUS", "SEMAGLUTIDE"],
    "tirzepatide": ["MOUNJARO", "ZEPBOUND", "TIRZEPATIDE"],
    "liraglutide": ["VICTOZA", "SAXENDA", "LIRAGLUTIDE"],
    "dulaglutide": ["TRULICITY", "DULAGLUTIDE"],
    "exenatide":   ["BYETTA", "BYDUREON", "EXENATIDE"],
    "lixisenatide": ["LYXUMIA", "ADLYXIN", "LIXISENATIDE"],
}
glp1_brand_to_generic = {}
for gen, brands in GLP1_PATTERNS.items():
    for b in brands:
        glp1_brand_to_generic[b] = gen

def glp1_match(name):
    if not isinstance(name, str):
        return None
    n = name.upper()
    for brand, gen in glp1_brand_to_generic.items():
        if brand in n:
            return gen
    return None

drugs["glp1_generic"] = drugs["medicinalproduct_norm"].apply(glp1_match)
glp1_rows = drugs[drugs["glp1_generic"].notna()]
print(f"GLP-1 drug rows: {len(glp1_rows):,} ({len(glp1_rows)/len(drugs)*100:.2f}% of all drug rows)")
print()
print("By generic:")
by_gen = glp1_rows["glp1_generic"].value_counts()
for g, n in by_gen.items():
    print(f"  {g}: {n:,}")

print()
print("Unique GLP-1 reports (safetyreportid):")
glp1_reports = glp1_rows["safetyreportid"].nunique()
total_reports = sample["safetyreportid"].nunique()
print(f"  GLP-1 reports: {glp1_reports:,} of {total_reports:,} ({glp1_reports/total_reports*100:.2f}%)")

# --- ana_10: Suspect-drug rate per major GLP-1 brand ---
print("=== ana_10 ===")
brand_list = ["OZEMPIC", "WEGOVY", "RYBELSUS", "MOUNJARO", "ZEPBOUND",
              "TRULICITY", "VICTOZA", "SAXENDA", "BYETTA", "BYDUREON"]
for brand in brand_list:
    sub = drugs[drugs["medicinalproduct_norm"] == brand]
    if len(sub) == 0:
        continue
    sus_n = (sub["drugcharacterization"] == 1).sum()
    pct = sus_n / len(sub) * 100
    print(f"{brand}\ttotal={len(sub):,}\tsuspect={sus_n:,}\t{pct:.1f}% suspect")

# --- ana_11: Drug administration route distribution (top 10 codes) ---
print("=== ana_11 ===")
route_codes = {
    "048": "Oral",
    "058": "Subcutaneous",
    "030": "Intramuscular",
    "061": "Topical",
    "041": "Intravenous",
    "045": "Nasal",
    "037": "Inhalation",
    "065": "Transdermal",
    "059": "Sublingual",
}
def fmt_route(r):
    if pd.isna(r):
        return "MISSING"
    s = str(r).zfill(3)
    return f"{s} ({route_codes.get(s, 'other')})"
drugs["route_fmt"] = drugs["drugadministrationroute"].apply(fmt_route)
print(drugs["route_fmt"].value_counts().head(12))
