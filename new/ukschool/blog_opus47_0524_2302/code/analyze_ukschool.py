"""
Analysis of the ukschool dataset: Oxford vs Cambridge as producers of notable Britons.
Run from DATA_DIR (the dataset folder) OR pass nothing; paths are resolved relative to this file's expectation.
Usage: python3 analyze_ukschool.py /path/to/data/ukschool
"""
import sys
import pandas as pd
from collections import Counter

DATA = sys.argv[1] if len(sys.argv) > 1 else "/Users/forrest/Desktop/data2blog-skill/data/ukschool"

pm = pd.read_csv(f"{DATA}/uk_prime_ministers.csv")
counts = pd.read_csv(f"{DATA}/pm_count_by_university.csv")
oxb = pd.read_csv(f"{DATA}/oxbridge_comparison.csv")

pm["year"] = pd.to_datetime(pm["term_start"], errors="coerce").dt.year

# --- ana_01: The headline split — Oxford rules politics, Cambridge rules science ---
print("=== ana_01 ===")
print(oxb.to_string(index=False))
ox = oxb[oxb.university == "Oxford"].iloc[0]
cam = oxb[oxb.university == "Cambridge"].iloc[0]
print(f"Oxford PMs {ox.uk_prime_ministers} vs Cambridge {cam.uk_prime_ministers} -> ratio {ox.uk_prime_ministers/cam.uk_prime_ministers:.2f}x")
print(f"Cambridge Nobel {cam.nobel_laureates} vs Oxford {ox.nobel_laureates} -> ratio {cam.nobel_laureates/ox.nobel_laureates:.2f}x")

# --- ana_02: PM classification breakdown (all 59) ---
print("=== ana_02 ===")
print(counts.to_string(index=False))

# --- ana_03: PM classification as shares of 59 ---
print("=== ana_03 ===")
cls = pm["classification"].value_counts()
total = len(pm)
print(f"Total PM rows: {total}")
for k, v in cls.items():
    print(f"{k}: {v} ({100*v/total:.1f}%)")

# --- ana_04: Oxford's post-1937 streak vs Cambridge's drought ---
print("=== ana_04 ===")
# Last Cambridge PM by term_start
cam_pms = pm[pm["classification"].isin(["Cambridge", "Both"])].sort_values("year")
print("Cambridge/Both PMs (last few):")
print(cam_pms[["name", "year", "classification"]].tail(5).to_string(index=False))
last_cam = cam_pms.iloc[-1]
print(f"Last Cambridge-attending PM to take office: {last_cam['name']} ({int(last_cam['year'])})")
# Oxford PMs since 1937
ox_since = pm[(pm.classification == "Oxford") & (pm.year >= 1937)].sort_values("year")
print(f"Oxford PMs taking office in/after 1937: {len(ox_since)}")
# English-university PMs since 1937 and where
since37 = pm[pm.year >= 1937].sort_values("year")
print("All PMs since 1937 with their classification:")
print(since37[["name", "year", "classification"]].to_string(index=False))

# --- ana_05: Oxford PMs over time, by half-century era ---
print("=== ana_05 ===")
def era(y):
    if pd.isna(y): return "Unknown"
    if y < 1800: return "1700s"
    if y < 1850: return "1800-1849"
    if y < 1900: return "1850-1899"
    if y < 1950: return "1900-1949"
    return "1950-present"
pm["era"] = pm["year"].apply(era)
era_order = ["1700s", "1800-1849", "1850-1899", "1900-1949", "1950-present"]
tab = pm.groupby(["era", "classification"]).size().unstack(fill_value=0)
tab = tab.reindex(era_order)
print(tab.to_string())

# --- ana_06: Which colleges feed Prime Ministers ---
print("=== ana_06 ===")
# Oxbridge college keywords; map college -> Oxford/Cambridge handled implicitly. Count college mentions among Oxbridge PMs.
oxbridge_pms = pm[pm.classification.isin(["Oxford", "Cambridge", "Both"])]
college_counter = Counter()
# Known college lists
ox_colleges = ["Christ Church", "Balliol College", "Brasenose College", "Trinity College, Oxford", "Hertford College",
               "University College", "Somerville College", "Jesus College", "Merton College", "Lincoln College",
               "St John's College", "St Hugh's College", "St Edmund Hall", "Pembroke College"]
# To avoid Oxford/Cambridge Trinity ambiguity, count raw college tokens then report top.
for inst in oxbridge_pms["institutions"].dropna():
    for tok in [t.strip() for t in inst.split(";")]:
        if "College" in tok or tok in ("St Edmund Hall",):
            # skip schools that aren't colleges of the universities: Eton College, Harrow handled below
            if tok in ("Eton College", "Harrow School", "Westminster School"):
                continue
            college_counter[tok] += 1
for col, c in college_counter.most_common(12):
    print(f"{col}: {c}")

# --- ana_07: Christ Church specifically — the single most prolific college ---
print("=== ana_07 ===")
cc = pm[pm["institutions"].fillna("").str.contains("Christ Church")]
print(f"PMs who attended Christ Church (Oxford): {len(cc)}")
print(cc[["name", "year"]].to_string(index=False))

# --- ana_08: Eton + Oxford pipeline ---
print("=== ana_08 ===")
eton = pm[pm["institutions"].fillna("").str.contains("Eton College")]
eton_ox = eton[eton.oxford == True]
print(f"PMs who attended Eton: {len(eton)}")
print(f"PMs who attended both Eton AND Oxford: {len(eton_ox)}")
print(eton_ox[["name", "year"]].to_string(index=False))

# --- ana_09: No-university and non-Oxbridge PMs ---
print("=== ana_09 ===")
unknown = pm[pm.classification == "Unknown"]
other = pm[pm.classification == "Other"]
print(f"Unknown/no university recorded: {len(unknown)}")
print(unknown[["name", "year"]].to_string(index=False))
print(f"Other (non-Oxbridge) university: {len(other)}")
print(other[["name", "year", "institutions"]].to_string(index=False))

# --- ana_10: Total notable-alumni coverage (caveated) ---
print("=== ana_10 ===")
print(oxb[["university", "total_alumni_on_wikidata"]].to_string(index=False))
print(f"Oxford coverage exceeds Cambridge by {ox.total_alumni_on_wikidata - cam.total_alumni_on_wikidata} items "
      f"({100*(ox.total_alumni_on_wikidata-cam.total_alumni_on_wikidata)/cam.total_alumni_on_wikidata:.1f}%)")
# PM rate per 10k notable alumni (relative, caveated)
print(f"Oxford PMs per 10k notable alumni: {10000*ox.uk_prime_ministers/ox.total_alumni_on_wikidata:.2f}")
print(f"Cambridge PMs per 10k notable alumni: {10000*cam.uk_prime_ministers/cam.total_alumni_on_wikidata:.2f}")
print(f"Cambridge Nobel per 10k notable alumni: {10000*cam.nobel_laureates/cam.total_alumni_on_wikidata:.2f}")
print(f"Oxford Nobel per 10k notable alumni: {10000*ox.nobel_laureates/ox.total_alumni_on_wikidata:.2f}")
