"""Stage 2 Analyst — load + profile.

Reads bands.csv and boys.csv from the dataset and prints summary stats
that feed analyst.json items ana_01 .. ana_05.
"""
import csv
import os
from collections import Counter

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/12_boybands"


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


bands = load_csv(os.path.join(DATA_DIR, "bands.csv"))
boys = load_csv(os.path.join(DATA_DIR, "boys.csv"))

# --- ana_01: dataset shape ---
print("=== ana_01 ===")
print(f"bands rows: {len(bands)}")
print(f"boys rows:  {len(boys)}")
print(f"bands cols: {list(bands[0].keys())}")
print(f"boys cols:  {list(boys[0].keys())}")
years = sorted({r["highest_pos_date"][:4] for r in bands if r["highest_pos_date"]})
print(f"year range: {years[0]} – {years[-1]}")
size_counter = Counter(r["band"] for r in boys)
sizes = list(size_counter.values())
print(f"band size: min={min(sizes)}, max={max(sizes)}, mean={sum(sizes)/len(sizes):.2f}, median={sorted(sizes)[len(sizes)//2]}")

# --- ana_02: charting peak — distribution of highest_pos ---
print("\n=== ana_02 ===")
peaks = [int(r["highest_pos"]) for r in bands]
buckets = {"#1": 0, "#2-#5": 0, "#6-#10": 0, "#11-#25": 0, "#26-#50": 0, "#51-#100": 0}
for p in peaks:
    if p == 1:
        buckets["#1"] += 1
    elif p <= 5:
        buckets["#2-#5"] += 1
    elif p <= 10:
        buckets["#6-#10"] += 1
    elif p <= 25:
        buckets["#11-#25"] += 1
    elif p <= 50:
        buckets["#26-#50"] += 1
    else:
        buckets["#51-#100"] += 1
for k, v in buckets.items():
    print(f"  {k:9s}: {v:3d}  ({v/len(bands)*100:.1f}%)")
n1 = buckets["#1"]
print(f"\n# bands that hit #1: {n1} ({n1/len(bands)*100:.1f}%)")
top10 = buckets["#1"] + buckets["#2-#5"] + buckets["#6-#10"]
print(f"# bands that hit top 10: {top10} ({top10/len(bands)*100:.1f}%)")

# --- ana_03: dance speed split ---
print("\n=== ana_03 ===")
ds = Counter(r["danceSpeed"] for r in bands)
for k, v in ds.most_common():
    print(f"  {k:6s}: {v:3d} ({v/len(bands)*100:.1f}%)")

# --- ana_04: featuring artist split ---
print("\n=== ana_04 ===")
ft = Counter(r["featuring_artist"] for r in bands)
for k, v in ft.most_common():
    print(f"  {k:4s}: {v:3d} ({v/len(bands)*100:.1f}%)")

# --- ana_05: bands per release year ---
print("\n=== ana_05 ===")
by_year = Counter(int(r["highest_pos_date"][:4]) for r in bands)
for y in sorted(by_year):
    print(f"  {y}: {by_year[y]}")
print(f"peak year: {max(by_year, key=by_year.get)} with {max(by_year.values())} bands")
print(f"total years covered (with at least 1 band): {len(by_year)}")

# Bucket by 5-year era
era = {"1980-84": 0, "1985-89": 0, "1990-94": 0, "1995-99": 0, "2000-04": 0, "2005-09": 0, "2010-14": 0, "2015-18": 0}
for y, c in by_year.items():
    if y < 1985:
        era["1980-84"] += c
    elif y < 1990:
        era["1985-89"] += c
    elif y < 1995:
        era["1990-94"] += c
    elif y < 2000:
        era["1995-99"] += c
    elif y < 2005:
        era["2000-04"] += c
    elif y < 2010:
        era["2005-09"] += c
    elif y < 2015:
        era["2010-14"] += c
    else:
        era["2015-18"] += c
print("\nBands by 5-year era:")
for k, v in era.items():
    print(f"  {k}: {v}")
