"""Process node and area trends + transistor density.

How quickly did the manufacturing process shrink, and how fast did density rise?
"""
import pandas as pd
import numpy as np
import os

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/03_moores-law'

cpu = pd.read_csv(os.path.join(DATA_DIR, 'cpu.csv'))
gpu = pd.read_csv(os.path.join(DATA_DIR, 'gpu.csv'))

# --- ana_08: Process node decay (CPU) ---
print("=== ana_08 ===")
cpu_pn = cpu.dropna(subset=['process', 'date_of_introduction']).copy()
# Group by year, take min process node available that year
node_by_year = cpu_pn.groupby('date_of_introduction')['process'].min().sort_index()
print("Year | min process (nm)")
for yr, p in node_by_year.items():
    print(f"  {int(yr)} {p}")
# Fold reduction from earliest to latest
first_pn = node_by_year.iloc[0]
last_pn = node_by_year.iloc[-1]
print(f"first year process: {first_pn} nm   last year process: {last_pn} nm   reduction: {first_pn/last_pn:,.0f}x")

# --- ana_09: Density (transistors per mm^2) over time ---
print("=== ana_09 ===")
cpu_d = cpu.dropna(subset=['transistor_count', 'area', 'date_of_introduction']).copy()
cpu_d = cpu_d[cpu_d['area'] > 0]
cpu_d['density'] = cpu_d['transistor_count'] / cpu_d['area']  # transistors per mm^2
density_by_year = cpu_d.groupby('date_of_introduction')['density'].max().sort_index()
print("Year | max density (transistors/mm^2)")
for yr, d in density_by_year.items():
    print(f"  {int(yr)} {d:,.0f}")
print(f"\nmin density {density_by_year.min():,.1f} at year {int(density_by_year.idxmin())}")
print(f"max density {density_by_year.max():,.0f} at year {int(density_by_year.idxmax())}")
print(f"density fold change earliest->latest year: {density_by_year.iloc[-1]/density_by_year.iloc[0]:,.0f}x")

# Slope of log10(density) vs year
x = cpu_d['date_of_introduction'].astype(float).values
y = np.log10(cpu_d['density'].values)
slope, _ = np.polyfit(x, y, 1)
print(f"density log10/yr slope: {slope:.4f}  doubling time: {np.log10(2)/slope:.2f} yr")

# --- ana_10: Area trend — chips getting bigger or staying flat? ---
print("=== ana_10 ===")
area_by_year = cpu_d.groupby('date_of_introduction')['area'].max().sort_index()
print("max area per year (mm^2):")
print(f"  early (1970-1980): {area_by_year[area_by_year.index<=1980].mean():.1f}")
print(f"  middle (1981-2000): {area_by_year[(area_by_year.index>1980)&(area_by_year.index<=2000)].mean():.1f}")
print(f"  recent (2001-2019): {area_by_year[area_by_year.index>2000].mean():.1f}")
print(f"min area in dataset: {cpu_d['area'].min():.0f} mm^2")
print(f"max area in dataset: {cpu_d['area'].max():.0f} mm^2")

# --- ana_11: Designer dominance over time (CPU) ---
print("=== ana_11 ===")
# Top designer share per decade
cpu['decade'] = (cpu['date_of_introduction'] // 10 * 10).astype('Int64')
des_decade = cpu.groupby(['decade', 'designer']).size().unstack(fill_value=0)
print("CPUs by designer per decade (top 6 designers):")
top_des = cpu['designer'].value_counts().head(6).index.tolist()
print(des_decade[top_des])
