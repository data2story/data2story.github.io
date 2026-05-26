"""04_geography.py — Where the meteorites came from, and how it differs between Fells and Founds."""
import pandas as pd
import numpy as np

df = pd.read_pickle(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_clean_with_family.pkl")
geo = df.dropna(subset=['reclat','reclong']).copy()

# --- ana_13: Hemisphere split, Fell vs Found ---
print("=== ana_13 ===")
geo['hemi_ns'] = np.where(geo['reclat'] >= 0, 'Northern', 'Southern')
piv = geo.pivot_table(index='hemi_ns', columns='fall', values='id', aggfunc='count', fill_value=0)
piv['Total'] = piv.sum(axis=1)
print(piv.to_string())

# --- ana_14: Antarctic vs rest of world ---
print("\n=== ana_14 ===")
geo['region'] = np.where(geo['reclat'] < -60, 'Antarctica (lat<-60)', 'Rest of world')
piv = geo.pivot_table(index='region', columns='fall', values='id', aggfunc='count', fill_value=0)
piv['Total'] = piv.sum(axis=1)
piv['%Fell'] = (piv.get('Fell',0) / piv['Total'] * 100).round(3)
print(piv.to_string())
print(f"\nShare of all geocoded Finds that are in Antarctica: {((geo['fall']=='Found') & (geo['reclat']<-60)).sum() / (geo['fall']=='Found').sum() * 100:.1f}%")
print(f"Share of all geocoded Fells that are in Antarctica: {((geo['fall']=='Fell')  & (geo['reclat']<-60)).sum() / max(1,(geo['fall']=='Fell').sum()) * 100:.2f}%")

# --- ana_15: Coarse region buckets (Antarctica vs hot-desert belts vs rest) ---
print("\n=== ana_15 ===")
def region(row):
    lat, lon = row['reclat'], row['reclong']
    if lat < -60: return "Antarctica"
    # Sahara/Sahel: lat 15..32, lon -17..40
    if 15 <= lat <= 32 and -17 <= lon <= 40: return "Sahara/Sahel"
    # Arabian + Oman: lat 16..28, lon 35..60
    if 16 <= lat <= 28 and 35 <= lon <= 60: return "Arabia/Oman"
    # Atacama: lat -30..-15, lon -72..-65
    if -30 <= lat <= -15 and -72 <= lon <= -65: return "Atacama (Chile)"
    # Australia outback: lat -32..-18, lon 115..150
    if -32 <= lat <= -18 and 115 <= lon <= 150: return "Australian outback"
    # Western US (deserts): lat 30..42, lon -120..-100
    if 30 <= lat <= 42 and -120 <= lon <= -100: return "US SW deserts"
    return "Rest of world"

geo['region2'] = geo.apply(region, axis=1)
piv = geo.pivot_table(index='region2', columns='fall', values='id', aggfunc='count', fill_value=0)
piv['Total'] = piv.sum(axis=1)
piv['%Fell'] = (piv.get('Fell',0) / piv['Total'] * 100).round(2)
piv = piv.sort_values('Total', ascending=False)
print(piv.to_string())

# --- ana_16: Lat/lon hex-style binning for the global map (5° cells) ---
print("\n=== ana_16 ===")
g = geo.copy()
g['lat5']  = (g['reclat']  // 5 * 5).astype(int)
g['lon5']  = (g['reclong'] // 5 * 5).astype(int)
hot = g.groupby(['lat5','lon5']).size().sort_values(ascending=False).head(15)
print("Top 15 hottest 5°x5° cells (count of meteorites):")
print(hot.to_string())

# Sample 1000 Fells + 1000 Founds for designer map — keep all Fells, sample Founds
geo[geo['fall']=='Fell'][['name','reclat','reclong','mass (g)','year','family']].to_csv(
    r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_fells_map.csv", index=False
)
geo[geo['fall']=='Found'].sample(n=2000, random_state=0)[['name','reclat','reclong','mass (g)','year','family']].to_csv(
    r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_founds_sample_map.csv", index=False
)
print("\nWrote _fells_map.csv (all Fells) and _founds_sample_map.csv (2000 sample).")
