"""05_year_trends.py — Time trends: year histograms, ANSMET inflection, oldest records."""
import pandas as pd
import numpy as np

df = pd.read_pickle(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_clean_with_family.pkl")
d = df.dropna(subset=['year']).copy()
d = d[(d['year'] >= 1) & (d['year'] <= 2025)]

# --- ana_17: Earliest 10 recorded meteorites (any fall type) ---
print("=== ana_17 ===")
oldest = d.sort_values('year').head(10)
print(oldest[['name','year','fall','recclass','mass (g)','reclat','reclong']].to_string(index=False))

# --- ana_18: Earliest 10 Fells specifically ---
print("\n=== ana_18 ===")
oldfells = d[d['fall']=='Fell'].sort_values('year').head(10)
print(oldfells[['name','year','recclass','mass (g)','reclat','reclong']].to_string(index=False))

# --- ana_19: Year histogram per decade — Fell, Found, Total ---
print("\n=== ana_19 ===")
d['decade'] = (d['year'] // 10 * 10).astype(int)
piv = d.pivot_table(index='decade', columns='fall', values='id', aggfunc='count', fill_value=0)
piv = piv.reindex(columns=['Fell','Found'], fill_value=0)
piv['Total'] = piv.sum(axis=1)
piv = piv[piv['Total']>0]
print(piv.tail(25).to_string())

# Output to CSV for chart data_table
piv.reset_index().to_csv(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_decade_fellfound.csv", index=False)

# --- ana_20: Annual Fell rate over the modern era (1900-2013) ---
print("\n=== ana_20 ===")
fells_modern = d[(d['fall']=='Fell') & (d['year']>=1900) & (d['year']<=2013)]
yr_counts = fells_modern.groupby(fells_modern['year'].astype(int)).size()
print(f"Years covered: 1900-2013")
print(f"Total observed Fells in that window: {len(fells_modern)}")
print(f"Mean Fells per year: {len(fells_modern)/(2013-1900+1):.2f}")
print(f"Median per year: {yr_counts.median():.1f}")
print(f"Max in any one year: {yr_counts.max()} ({yr_counts.idxmax()})")

# --- ana_21: ANSMET inflection — Founds before vs after 1970 ---
print("\n=== ana_21 ===")
finds = d[d['fall']=='Found']
pre = finds[finds['year']<1970]
post = finds[finds['year']>=1970]
print(f"Finds with year < 1970 : {len(pre):>6,}")
print(f"Finds with year >= 1970: {len(post):>6,}")
print(f"Ratio post/pre         : {len(post)/max(1,len(pre)):.1f}x")
print(f"Finds 1970-2013 mean per year: {len(post)/(2013-1970+1):.1f}")

# --- ana_22: Antarctica vs rest-of-world over time ---
print("\n=== ana_22 ===")
ddf = d.dropna(subset=['reclat'])
ddf = ddf.assign(decade=(ddf['year']//10*10).astype(int), antarctic=ddf['reclat']<-60)
ant_piv = ddf.pivot_table(index='decade', columns='antarctic', values='id', aggfunc='count', fill_value=0)
ant_piv.columns = ['RestOfWorld' if not k else 'Antarctica' for k in ant_piv.columns]
ant_piv['Total'] = ant_piv.sum(axis=1)
ant_piv = ant_piv[ant_piv['Total']>0]
print(ant_piv.tail(20).to_string())
ant_piv.reset_index().to_csv(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_decade_antarctic.csv", index=False)
