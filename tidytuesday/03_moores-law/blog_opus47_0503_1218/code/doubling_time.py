"""Empirical doubling time per chip family + comparison to Moore's predictions.

Fits log-linear regressions and reports CAGR + doubling time for CPUs, GPUs, RAM.
"""
import pandas as pd
import numpy as np
import os

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/03_moores-law'

cpu = pd.read_csv(os.path.join(DATA_DIR, 'cpu.csv'))
gpu = pd.read_csv(os.path.join(DATA_DIR, 'gpu.csv'))
ram = pd.read_csv(os.path.join(DATA_DIR, 'ram.csv'))

# Strip NA transistor counts and tag the family
def clean(df, family):
    out = df.dropna(subset=['transistor_count', 'date_of_introduction']).copy()
    out['family'] = family
    out['log10_tc'] = np.log10(out['transistor_count'])
    return out[['date_of_introduction', 'transistor_count', 'log10_tc', 'family']]

cpu_c = clean(cpu, 'CPU')
gpu_c = clean(gpu, 'GPU')
ram_c = clean(ram, 'RAM')

# --- ana_01: Empirical doubling time per family ---
print("=== ana_01 ===")
results = []
for fam, df in [('CPU', cpu_c), ('GPU', gpu_c), ('RAM', ram_c)]:
    x = df['date_of_introduction'].values.astype(float)
    y = df['log10_tc'].values
    slope, intercept = np.polyfit(x, y, 1)
    # log10(2) / slope = doubling time in years
    doubling_yr = np.log10(2) / slope
    cagr = (10 ** slope) - 1
    print(f"{fam}: slope_log10/yr={slope:.4f}  doubling={doubling_yr:.2f}yr  CAGR={cagr*100:.1f}%  n={len(df)}  range={int(x.min())}-{int(x.max())}")
    results.append({"family": fam, "slope_log10_per_year": slope, "doubling_years": doubling_yr,
                    "cagr_pct": cagr*100, "n": len(df), "year_min": int(x.min()), "year_max": int(x.max())})

# --- ana_02: Moore's two-year doubling vs empirical (CPU) ---
print("=== ana_02 ===")
# Moore (1975 revision): doubling every 2 years
moore_slope = np.log10(2) / 2.0  # ~0.1505
print(f"Moore's predicted log10/yr slope: {moore_slope:.4f}  (doubling = 2.00 yr, CAGR = 41.4%)")
for r in results:
    diff = r['slope_log10_per_year'] - moore_slope
    print(f"  {r['family']:<3} empirical {r['slope_log10_per_year']:.4f}  diff {diff:+.4f}  doubling diff {r['doubling_years']-2.0:+.2f} yr")

# --- ana_03: Total fold-change across the full record (CPU) ---
print("=== ana_03 ===")
# Earliest CPU and latest CPU in dataset
cpu_first = cpu_c.sort_values('date_of_introduction').iloc[0]
cpu_last = cpu_c.sort_values('date_of_introduction').iloc[-1]
# Find the absolute champion
cpu_max = cpu_c.sort_values('transistor_count').iloc[-1]
cpu_min = cpu_c.sort_values('transistor_count').iloc[0]
print(f"earliest CPU row: {int(cpu_first['date_of_introduction'])}  tc={int(cpu_first['transistor_count'])}")
print(f"latest CPU row:   {int(cpu_last['date_of_introduction'])}  tc={int(cpu_last['transistor_count'])}")
print(f"min tc in CPU:    {int(cpu_min['transistor_count'])}  ({int(cpu_min['date_of_introduction'])})")
print(f"max tc in CPU:    {int(cpu_max['transistor_count'])}  ({int(cpu_max['date_of_introduction'])})")
fold_min_to_max = cpu_max['transistor_count'] / cpu_min['transistor_count']
print(f"fold change min->max in CPU table: {fold_min_to_max:,.0f}x")

# Same for GPU and RAM
for fam, df in [('GPU', gpu_c), ('RAM', ram_c)]:
    f = df.sort_values('date_of_introduction').iloc[0]
    l = df.sort_values('date_of_introduction').iloc[-1]
    mn = df.sort_values('transistor_count').iloc[0]
    mx = df.sort_values('transistor_count').iloc[-1]
    print(f"{fam}: first {int(f['date_of_introduction'])}->{int(f['transistor_count'])}  last {int(l['date_of_introduction'])}->{int(l['transistor_count'])}  min={int(mn['transistor_count'])}  max={int(mx['transistor_count']):,}  fold={mx['transistor_count']/mn['transistor_count']:,.0f}x")
