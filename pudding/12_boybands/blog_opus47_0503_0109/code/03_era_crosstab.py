"""Stage 2 Analyst — appearance broken down by era.

Joins boys.csv with bands.csv on band name to get a release-year per member,
then computes era-specific appearance stats (frosted-tip rate by era,
suit vs. jeans, instruments, dance speed, etc.).
"""
import csv
import os
from collections import Counter, defaultdict

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/12_boybands"

with open(os.path.join(DATA_DIR, "bands.csv"), encoding="utf-8") as f:
    bands = list(csv.DictReader(f))
with open(os.path.join(DATA_DIR, "boys.csv"), encoding="utf-8") as f:
    boys = list(csv.DictReader(f))

# Map band name -> year of highest_pos_date
band_year = {b["band"]: int(b["highest_pos_date"][:4]) for b in bands}
band_dance = {b["band"]: b["danceSpeed"] for b in bands}
band_pos = {b["band"]: int(b["highest_pos"]) for b in bands}


def era_label(y):
    if y < 1990:
        return "1980s (1980-1989)"
    if y < 1995:
        return "Early 1990s (1990-1994)"
    if y < 2000:
        return "Late 1990s (1995-1999)"
    if y < 2005:
        return "Early 2000s (2000-2004)"
    if y < 2010:
        return "Late 2000s (2005-2009)"
    if y < 2015:
        return "Early 2010s (2010-2014)"
    return "Late 2010s (2015-2018)"


# attach era to each member
for r in boys:
    yr = band_year.get(r["band"])
    r["_year"] = yr
    r["_era"] = era_label(yr) if yr else "?"

ERAS = [
    "1980s (1980-1989)",
    "Early 1990s (1990-1994)",
    "Late 1990s (1995-1999)",
    "Early 2000s (2000-2004)",
    "Late 2000s (2005-2009)",
    "Early 2010s (2010-2014)",
    "Late 2010s (2015-2018)",
]
era_counts = Counter(r["_era"] for r in boys)
print("Members per era:")
for e in ERAS:
    print(f"  {e}: {era_counts.get(e,0)}")
TOTAL = len(boys)


def era_pct(field, value, members):
    """Among members in this era, what % match field == value (or token in field)."""
    if not members:
        return 0.0
    n = sum(1 for r in members if value in (r[field] or "").split(","))
    return n / len(members) * 100


# --- ana_17: frosted tips by era ---
print("\n=== ana_17 ===")
print("Frosted tips (any color) by era:")
print("era,members,yes,red,green,total_frosted,pct_yes")
rows_table = []
for e in ERAS:
    members = [r for r in boys if r["_era"] == e]
    n = len(members)
    yes = sum(1 for r in members if r["hair_frosted"] == "yes")
    red = sum(1 for r in members if r["hair_frosted"] == "red")
    green = sum(1 for r in members if r["hair_frosted"] == "green")
    pct = (yes / n * 100) if n else 0
    print(f"  {e}: members={n}, yes={yes} ({pct:.1f}%), red={red}, green={green}")

# --- ana_18: suit vs jeans by era ---
print("\n=== ana_18 ===")
print("Bottom-style mix by era:")
for e in ERAS:
    members = [r for r in boys if r["_era"] == e]
    n = len(members)
    if not n:
        continue
    dp = sum(1 for r in members if r["bottom_style"] == "dress pants")
    jn = sum(1 for r in members if r["bottom_style"] in ("jeans", "acid wash jeans"))
    other = n - dp - jn
    print(f"  {e}: dress pants {dp}/{n} ({dp/n*100:.0f}%), jeans {jn}/{n} ({jn/n*100:.0f}%), other {other}")

# --- ana_19: hair length by era ---
print("\n=== ana_19 ===")
for e in ERAS:
    members = [r for r in boys if r["_era"] == e]
    n = len(members)
    if not n:
        continue
    short = sum(1 for r in members if r["hair_length"] == "short")
    med = sum(1 for r in members if r["hair_length"] == "medium")
    lon = sum(1 for r in members if r["hair_length"] == "long")
    print(f"  {e}: short {short/n*100:.0f}% / medium {med/n*100:.0f}% / long {lon/n*100:.0f}%")

# --- ana_20: instruments by era ---
print("\n=== ana_20 ===")
for e in ERAS:
    members = [r for r in boys if r["_era"] == e]
    n = len(members)
    if not n:
        continue
    plays = sum(1 for r in members if r["instrument"])
    print(f"  {e}: plays-instrument {plays}/{n} ({plays/n*100:.0f}%)")

# --- ana_21: skin tone by era ---
print("\n=== ana_21 ===")
for e in ERAS:
    members = [r for r in boys if r["_era"] == e]
    n = len(members)
    if not n:
        continue
    light = sum(1 for r in members if r["skin"] == "light")
    md = sum(1 for r in members if r["skin"] in ("medium-dark", "dark"))
    print(f"  {e}: light {light}/{n} ({light/n*100:.0f}%); medium-dark+dark {md}/{n} ({md/n*100:.0f}%)")

# --- ana_22: skin tone by dance speed ---
print("\n=== ana_22 ===")
print("Skin tone by danceSpeed:")
for ds in ("pop", "slow"):
    members = [r for r in boys if band_dance.get(r["band"]) == ds]
    n = len(members)
    if not n:
        continue
    light = sum(1 for r in members if r["skin"] == "light")
    ml = sum(1 for r in members if r["skin"] == "medium-light")
    md = sum(1 for r in members if r["skin"] == "medium-dark")
    dk = sum(1 for r in members if r["skin"] == "dark")
    m = sum(1 for r in members if r["skin"] == "medium")
    print(f"  {ds}: members={n}, light={light/n*100:.0f}%, medium-light={ml/n*100:.0f}%, medium={m/n*100:.0f}%, medium-dark={md/n*100:.0f}%, dark={dk/n*100:.0f}%")

# --- ana_23: top wear by danceSpeed (suit vs jeans) ---
print("\n=== ana_23 ===")
for ds in ("pop", "slow"):
    members = [r for r in boys if band_dance.get(r["band"]) == ds]
    n = len(members)
    if not n:
        continue
    suit = sum(1 for r in members if "suit jacket" in (r["top_style"] or ""))
    print(f"  {ds}: suit-jacket-tops {suit}/{n} ({suit/n*100:.0f}%)")

# --- ana_24: average band size by era ---
print("\n=== ana_24 ===")
band_size = Counter(r["band"] for r in boys)
for e in ERAS:
    bands_in_era = [b for b in bands if era_label(int(b["highest_pos_date"][:4])) == e]
    if not bands_in_era:
        continue
    sizes = [band_size[b["band"]] for b in bands_in_era]
    print(f"  {e}: bands={len(sizes)}, mean members={sum(sizes)/len(sizes):.2f}")

# --- ana_25: lineage / family-tree-style flagged groups ---
print("\n=== ana_25 ===")
lineage = {
    "New Edition (parent)": ["New Edition", "Bell Biv DeVoe"],
    "Lou Pearlman empire": ["Backstreet Boys", "NSYNC", "O-Town", "LFO"],
    "Motown Records (Boyz II Men/IMx)": ["Boyz II Men", "IMx"],
    "Disney/Tween-TV": ["Jonas Brothers", "Big Time Rush", "Mindless Behavior"],
    "British/Irish import": ["Take That", "BBMak", "Westlife", "5ive", "Brother Beyond"],
    "K-pop / Latin import": ["BTS", "Aventura", "Menudo", "Son by Four"],
    "Reality-TV pop": ["One Direction", "The Wanted", "5 Seconds of Summer"],
}
for k, names in lineage.items():
    found = [n for n in names if n in band_year]
    print(f"  {k}: {found}")

# --- ana_26: # of bands per peak position bucket ---
print("\n=== ana_26 ===")
n1 = [b for b in bands if int(b["highest_pos"]) == 1]
print(f"Bands that hit #1 ({len(n1)}):")
for b in sorted(n1, key=lambda b: b["highest_pos_date"]):
    print(f"  {b['highest_pos_date']}  {b['band']:30s}  '{b['highest_song']}'  ({b['danceSpeed']})")
