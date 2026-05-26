"""06_top_named.py — Spotlights on the named heavyweights from Detective."""
import pandas as pd
import numpy as np

df = pd.read_pickle(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_clean_with_family.pkl")

# --- ana_23: Top 5 by mass + their family ---
print("=== ana_23 ===")
top5 = df.dropna(subset=['mass (g)']).sort_values('mass (g)', ascending=False).head(5)
print(top5[['name','mass (g)','family','recclass','fall','year','reclat','reclong']].to_string(index=False))
print("\nAll five families:")
print(top5['family'].value_counts().to_string())

# --- ana_24: How many irons vs non-irons in the top 100 by mass? ---
print("\n=== ana_24 ===")
top100 = df.dropna(subset=['mass (g)']).sort_values('mass (g)', ascending=False).head(100)
print(top100['family'].value_counts().to_string())
print(f"\nShare of top 100 that are iron meteorites: {(top100['family']=='Iron meteorite').sum()}%")

# --- ana_25: Famous meteorites lookup table (linked to det_05..det_10) ---
print("\n=== ana_25 ===")
names_of_interest = ['Hoba', 'Cape York', 'Campo del Cielo', 'Canyon Diablo', 'Armanty', 'Mbozi', 'Agpalilik', 'Bacubirito']
for n in names_of_interest:
    hits = df[df['name'].str.contains(n, case=False, na=False)]
    if len(hits) > 0:
        for _, r in hits.iterrows():
            print(f"{r['name']:30s} mass(g)={r['mass (g)']:>14}  class={r['recclass']:<15} fall={r['fall']:<5} year={r['year']}  lat={r['reclat']}  lon={r['reclong']}")

# --- ana_26: Top 20 by mass — data_table for the leaderboard ---
print("\n=== ana_26 ===")
top20 = df.dropna(subset=['mass (g)']).sort_values('mass (g)', ascending=False).head(20)[['name','mass (g)','family','recclass','fall','year']]
print(top20.to_string(index=False))

# --- ana_27: Number of meteorite Fells per continent-ish region ---
print("\n=== ana_27 ===")
def cont(row):
    lat, lon = row['reclat'], row['reclong']
    if pd.isna(lat): return "Unknown"
    if lat < -60: return "Antarctica"
    if -60 <= lat < 15 and -90 < lon < -30: return "S. America"
    if 15 <= lat <= 75 and -170 < lon < -50: return "N. America"
    if -40 < lat < 38 and -20 < lon < 55: return "Africa"
    if 35 < lat < 75 and -15 < lon < 60: return "Europe"
    if 5 < lat < 75 and 55 <= lon < 180: return "Asia"
    if -50 < lat < 0 and 110 < lon < 180: return "Oceania"
    return "Other"
df['continent'] = df.apply(cont, axis=1)
piv = df.pivot_table(index='continent', columns='fall', values='id', aggfunc='count', fill_value=0)
piv['Total'] = piv.sum(axis=1)
piv = piv.sort_values('Total', ascending=False)
print(piv.to_string())
