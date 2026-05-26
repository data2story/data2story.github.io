"""02_fell_vs_found.py — The central Fell-vs-Found distinction and its consequences."""
import pandas as pd
import numpy as np

df = pd.read_pickle(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_clean.pkl")

# --- ana_04: Fell vs Found counts (headline) ---
print("=== ana_04 ===")
vc = df['fall'].value_counts()
total = len(df)
print(vc.to_string())
print(f"Fell pct  = {vc.get('Fell',0)/total*100:.2f}%")
print(f"Found pct = {vc.get('Found',0)/total*100:.2f}%")

# --- ana_05: Median + mean mass by fall, log scale ---
print("\n=== ana_05 ===")
m = df.dropna(subset=['mass (g)'])
for label, g in m.groupby('fall'):
    mass = g['mass (g)']
    print(f"{label:6s}  n={len(g):>6,}  median_g={mass.median():>12,.1f}  mean_g={mass.mean():>14,.1f}  geomean_g={np.exp(np.log(mass[mass>0]).mean()):>10.2f}")

# --- ana_06: Year distribution — fell vs found, decade buckets ---
print("\n=== ana_06 ===")
d = df.dropna(subset=['year']).copy()
d['decade'] = (d['year'] // 10 * 10).astype(int)
piv = d.pivot_table(index='decade', columns='fall', values='id', aggfunc='count', fill_value=0)
piv = piv.reindex(columns=['Fell','Found'], fill_value=0)
piv['Total'] = piv.sum(axis=1)
piv = piv[piv['Total'] > 0]
print(piv.to_string())

# Export the decade pivot as a chart-ready table
piv.reset_index().to_csv(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_decade_pivot.csv", index=False)

# --- ana_07: Single-decade share — when did Finds explode? ---
print("\n=== ana_07 ===")
post_1969 = d[d['year'] >= 1970]
pre_1970 = d[d['year'] < 1970]
print(f"Finds before 1970: {int((pre_1970['fall']=='Found').sum()):,}")
print(f"Finds 1970+      : {int((post_1969['fall']=='Found').sum()):,}")
print(f"Share of all Finds (with year) that are post-1969: {(post_1969['fall']=='Found').sum() / (d['fall']=='Found').sum() * 100:.1f}%")
print(f"Fells before 1970: {int((pre_1970['fall']=='Fell').sum()):,}")
print(f"Fells 1970+      : {int((post_1969['fall']=='Fell').sum()):,}")
print(f"Share of all Fells (with year) that are post-1969: {(post_1969['fall']=='Fell').sum() / (d['fall']=='Fell').sum() * 100:.1f}%")
