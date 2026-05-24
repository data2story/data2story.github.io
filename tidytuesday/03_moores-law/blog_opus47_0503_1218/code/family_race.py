"""Family race: who leads the absolute transistor count over time?

For every year, find the maximum transistor_count in CPU/GPU/RAM separately,
and compute the running maximum so we can see who has held the crown when.
"""
import pandas as pd
import numpy as np
import os

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/03_moores-law'

cpu = pd.read_csv(os.path.join(DATA_DIR, 'cpu.csv'))
gpu = pd.read_csv(os.path.join(DATA_DIR, 'gpu.csv'))
ram = pd.read_csv(os.path.join(DATA_DIR, 'ram.csv'))

def clean(df, fam, name_col):
    out = df.dropna(subset=['transistor_count', 'date_of_introduction']).copy()
    out['family'] = fam
    out['name'] = out[name_col]
    return out[['name', 'family', 'date_of_introduction', 'transistor_count']]

cpu_c = clean(cpu, 'CPU', 'processor')
gpu_c = clean(gpu, 'GPU', 'processor')
ram_c = clean(ram, 'RAM', 'chip_name')

allc = pd.concat([cpu_c, gpu_c, ram_c], ignore_index=True)
allc['date_of_introduction'] = allc['date_of_introduction'].astype(int)

# --- ana_04: Per-year per-family max transistor count ---
print("=== ana_04 ===")
pivot = (allc.groupby(['date_of_introduction', 'family'])['transistor_count']
         .max().unstack().sort_index())
print(pivot.tail(15))

# Save for designer
pivot_print = pivot.reset_index()
years_full = list(range(int(allc['date_of_introduction'].min()), int(allc['date_of_introduction'].max())+1))
pivot_full = pivot.reindex(years_full)
print(f"\nfull year range: {years_full[0]}-{years_full[-1]}")

# --- ana_05: Crown-holder by year (who has the max overall transistor count?) ---
print("=== ana_05 ===")
crown = []
running = {'CPU': 0, 'GPU': 0, 'RAM': 0}
running_chip = {'CPU': None, 'GPU': None, 'RAM': None}
for yr in years_full:
    ydata = allc[allc['date_of_introduction'] == yr]
    for _, r in ydata.iterrows():
        if r['transistor_count'] > running[r['family']]:
            running[r['family']] = r['transistor_count']
            running_chip[r['family']] = r['name']
    leader_fam = max(running, key=running.get)
    crown.append({'year': yr, 'leader_family': leader_fam, 'leader_chip': running_chip[leader_fam],
                  'leader_tc': running[leader_fam],
                  'cpu_tc': running['CPU'], 'gpu_tc': running['GPU'], 'ram_tc': running['RAM']})
crown_df = pd.DataFrame(crown)
# Print transitions only
prev = None
print("year | leader_family | leader_chip | leader_tc")
for _, row in crown_df.iterrows():
    if row['leader_family'] != prev:
        print(f"{row['year']} | {row['leader_family']:<3} | {row['leader_chip']:<40} | {int(row['leader_tc']):,}")
        prev = row['leader_family']

# --- ana_06: 2019 leaderboard (top 10 across all families) ---
print("=== ana_06 ===")
top10 = allc.sort_values('transistor_count', ascending=False).head(10)
for _, r in top10.iterrows():
    print(f"  {int(r['date_of_introduction'])}  {r['family']:<3}  {int(r['transistor_count']):>14,}  {r['name']}")

# --- ana_07: Era split — pre-2005 vs post-2005 doubling slope (CPU only) ---
print("=== ana_07 ===")
cpu_pre = cpu_c[cpu_c['date_of_introduction'] < 2005]
cpu_post = cpu_c[cpu_c['date_of_introduction'] >= 2005]
for label, sub in [('CPU pre-2005', cpu_pre), ('CPU 2005+', cpu_post)]:
    x = sub['date_of_introduction'].astype(float).values
    y = np.log10(sub['transistor_count'].astype(float).values)
    slope, _ = np.polyfit(x, y, 1)
    dt = np.log10(2) / slope
    print(f"  {label}: n={len(sub)} slope_log10/yr={slope:.4f} doubling={dt:.2f}yr CAGR={(10**slope - 1)*100:.1f}%")

# Same for GPU
gpu_pre = gpu_c[gpu_c['date_of_introduction'] < 2005]
gpu_post = gpu_c[gpu_c['date_of_introduction'] >= 2005]
for label, sub in [('GPU pre-2005', gpu_pre), ('GPU 2005+', gpu_post)]:
    if len(sub) < 3:
        print(f"  {label}: n={len(sub)} (insufficient)")
        continue
    x = sub['date_of_introduction'].astype(float).values
    y = np.log10(sub['transistor_count'].astype(float).values)
    slope, _ = np.polyfit(x, y, 1)
    dt = np.log10(2) / slope
    print(f"  {label}: n={len(sub)} slope_log10/yr={slope:.4f} doubling={dt:.2f}yr CAGR={(10**slope - 1)*100:.1f}%")
