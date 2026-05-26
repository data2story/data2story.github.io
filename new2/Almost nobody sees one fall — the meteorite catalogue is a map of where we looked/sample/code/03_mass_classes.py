"""03_mass_classes.py — Mass distribution and recclass family grouping."""
import pandas as pd
import numpy as np
import re

df = pd.read_pickle(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_clean.pkl")

# --- ana_08: Mass distribution — log buckets across all rows ---
print("=== ana_08 ===")
m = df['mass (g)'].dropna()
m = m[m > 0]
bins = [1e-3, 1, 10, 100, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8]
labels = ["<1g", "1-10g", "10-100g", "100g-1kg", "1-10kg", "10-100kg", "100kg-1t", "1-10t", "10-100t"]
buck = pd.cut(m, bins=bins, labels=labels, include_lowest=True)
b_counts = buck.value_counts().reindex(labels, fill_value=0)
print(b_counts.to_string())
print(f"\nmedian g = {m.median():.2f}")
print(f"mean   g = {m.mean():.2f}")
print(f"geomean g= {np.exp(np.log(m).mean()):.2f}")
print(f"95th pct = {m.quantile(0.95):.2f}")
print(f"99th pct = {m.quantile(0.99):.2f}")
print(f"max      = {m.max():.0f}")

# --- ana_09: Top 20 heaviest meteorites ---
print("\n=== ana_09 ===")
top20 = df.dropna(subset=['mass (g)']).sort_values('mass (g)', ascending=False).head(20)
print(top20[['name','mass (g)','fall','year','recclass','reclat','reclong']].to_string(index=False))

# --- ana_10: recclass family grouping ---
print("\n=== ana_10 ===")
def family(rc: str) -> str:
    if not isinstance(rc, str): return "Unknown"
    s = rc.strip()
    if s.lower().startswith("iron"): return "Iron meteorite"
    if "pallasite" in s.lower() or "mesosiderite" in s.lower(): return "Stony-iron"
    # HED — howardites/eucrites/diogenites and lunar/martian achondrites
    sl = s.lower()
    if any(k in sl for k in ["howardite","eucrite","diogenite"]): return "Achondrite — HED"
    if "lunar" in sl: return "Achondrite — Lunar"
    if "martian" in sl or "shergottite" in sl or "nakhlite" in sl or "chassignite" in sl: return "Achondrite — Martian"
    if any(k in sl for k in ["aubrite","ureilite","acapulcoite","lodranite","brachinite","angrite","winonaite"]):
        return "Achondrite — Primitive/Other"
    # Carbonaceous chondrites: CI, CM, CO, CV, CR, CK, CH, CB, CL plus C-unknown
    if re.match(r"^C[A-Z]?[0-9]?", s): return "Chondrite — Carbonaceous"
    # Enstatite chondrites
    if re.match(r"^E[HL]?[0-9]?", s) and not s.startswith("Eucrite"): return "Chondrite — Enstatite"
    # R/K chondrites
    if re.match(r"^R[0-9]", s): return "Chondrite — Rumuruti (R)"
    if re.match(r"^K[0-9]?", s) and "kakangari" in sl: return "Chondrite — Kakangari (K)"
    # Ordinary chondrites — H/L/LL with optional petrologic type
    if re.match(r"^(H|L|LL)([0-9](/[0-9])?)?(-an)?$", s, re.IGNORECASE): return "Chondrite — Ordinary"
    if re.match(r"^(H|L|LL)[0-9]?", s): return "Chondrite — Ordinary"
    if "chondrite" in sl: return "Chondrite — Other"
    if sl in ("unknown","relict ow","relict h?"): return "Unknown"
    return "Other / Ungrouped"

df['family'] = df['recclass'].apply(family)
fam_counts = df['family'].value_counts()
print(fam_counts.to_string())
total = fam_counts.sum()
print("\nPercentages:")
print((fam_counts / total * 100).round(2).to_string())

# --- ana_11: Median mass by family ---
print("\n=== ana_11 ===")
mm = df.dropna(subset=['mass (g)']).copy()
mm = mm[mm['mass (g)'] > 0]
grp = mm.groupby('family')['mass (g)'].agg(['count','median','mean'])
grp['median'] = grp['median'].round(2)
grp['mean'] = grp['mean'].round(2)
print(grp.sort_values('count', ascending=False).to_string())

# --- ana_12: Family by fall (count) ---
print("\n=== ana_12 ===")
piv = df.pivot_table(index='family', columns='fall', values='id', aggfunc='count', fill_value=0)
piv['Total'] = piv.sum(axis=1)
piv['%Fell'] = (piv.get('Fell',0) / piv['Total'] * 100).round(2)
piv = piv.sort_values('Total', ascending=False)
print(piv.to_string())

df.to_pickle(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_clean_with_family.pkl")
