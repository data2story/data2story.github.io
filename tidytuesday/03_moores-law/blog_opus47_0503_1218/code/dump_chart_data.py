"""Print the chart-ready data tables that go into analyst.json data_table fields."""
import pandas as pd
import numpy as np
import os
import json

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/03_moores-law'

cpu = pd.read_csv(os.path.join(DATA_DIR, 'cpu.csv'))
gpu = pd.read_csv(os.path.join(DATA_DIR, 'gpu.csv'))
ram = pd.read_csv(os.path.join(DATA_DIR, 'ram.csv'))

def clean(df, fam, name_col):
    out = df.dropna(subset=['transistor_count', 'date_of_introduction']).copy()
    out['family'] = fam
    out['name'] = out[name_col]
    out['year'] = out['date_of_introduction'].astype(int)
    out['tc'] = out['transistor_count'].astype(float).astype(int)
    return out[['name', 'family', 'year', 'tc']]

cpu_c = clean(cpu, 'CPU', 'processor')
gpu_c = clean(gpu, 'GPU', 'processor')
ram_c = clean(ram, 'RAM', 'chip_name')
allc = pd.concat([cpu_c, gpu_c, ram_c], ignore_index=True)

# ----- TABLE: scatter of every chip with year + family + tc + name -----
print("=== TABLE_scatter_all ===")
rows = []
for _, r in allc.sort_values(['year', 'family']).iterrows():
    rows.append([r['name'], r['family'], int(r['year']), int(r['tc'])])
print(f"len={len(rows)}")
print(rows[:3])
print(rows[-3:])

# Save to a small JSON we can copy into analyst.json
out = {"scatter_all": {"columns": ["name", "family", "year", "tc"], "rows": rows}}

# ----- TABLE: per-year max per family -----
mat = allc.groupby(['year', 'family'])['tc'].max().unstack().sort_index()
mat = mat.reindex(range(allc['year'].min(), allc['year'].max()+1))
fam_rows = []
for yr, row in mat.iterrows():
    fam_rows.append([int(yr),
                     None if pd.isna(row.get('CPU')) else int(row['CPU']),
                     None if pd.isna(row.get('GPU')) else int(row['GPU']),
                     None if pd.isna(row.get('RAM')) else int(row['RAM'])])
out["family_max_per_year"] = {"columns": ["year", "CPU", "GPU", "RAM"], "rows": fam_rows}
print("\n=== TABLE_family_max_per_year ===")
print(f"len={len(fam_rows)}")
print(fam_rows[:5])
print(fam_rows[-5:])

# ----- TABLE: doubling time summary per family -----
def fit(df):
    x = df['year'].astype(float).values
    y = np.log10(df['tc'].astype(float).values)
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept

double_rows = []
for fam, df in [('CPU', cpu_c), ('GPU', gpu_c), ('RAM', ram_c)]:
    s, i = fit(df)
    dt = np.log10(2) / s
    cagr = (10**s - 1) * 100
    double_rows.append([fam, len(df), int(df['year'].min()), int(df['year'].max()),
                        round(dt, 2), round(cagr, 1)])
out["doubling_summary"] = {"columns": ["family", "n", "year_min", "year_max", "doubling_years", "cagr_pct"],
                            "rows": double_rows}
print("\n=== TABLE_doubling_summary ===")
print(double_rows)

# ----- TABLE: era split CPU pre/post 2005 -----
era_rows = []
for fam_label, df in [('CPU pre-2005', cpu_c[cpu_c['year'] < 2005]),
                       ('CPU 2005+', cpu_c[cpu_c['year'] >= 2005]),
                       ('GPU pre-2005', gpu_c[gpu_c['year'] < 2005]),
                       ('GPU 2005+', gpu_c[gpu_c['year'] >= 2005])]:
    if len(df) < 3:
        continue
    s, i = fit(df)
    dt = np.log10(2) / s
    cagr = (10**s - 1) * 100
    era_rows.append([fam_label, len(df), round(dt, 2), round(cagr, 1)])
out["era_split"] = {"columns": ["era", "n", "doubling_years", "cagr_pct"], "rows": era_rows}
print("\n=== TABLE_era_split ===")
print(era_rows)

# ----- TABLE: top 10 chips by transistor count -----
top10 = allc.sort_values('tc', ascending=False).head(10)
top10_rows = [[r['name'], r['family'], int(r['year']), int(r['tc'])] for _, r in top10.iterrows()]
out["top10"] = {"columns": ["name", "family", "year", "tc"], "rows": top10_rows}
print("\n=== TABLE_top10 ===")
for r in top10_rows:
    print(r)

# ----- TABLE: process node min per year (CPU) -----
cpu_pn = cpu.dropna(subset=['process', 'date_of_introduction']).copy()
node_year = cpu_pn.groupby('date_of_introduction')['process'].min().sort_index()
node_rows = [[int(y), int(v)] for y, v in node_year.items()]
out["process_node"] = {"columns": ["year", "min_process_nm"], "rows": node_rows}
print("\n=== TABLE_process_node ===")
print(node_rows[:3], '...', node_rows[-3:])

# ----- TABLE: density per year max (CPU) -----
cpu_d = cpu.dropna(subset=['transistor_count','area','date_of_introduction']).copy()
cpu_d = cpu_d[cpu_d['area']>0]
cpu_d['density'] = cpu_d['transistor_count'] / cpu_d['area']
dens = cpu_d.groupby('date_of_introduction')['density'].max().sort_index()
dens_rows = [[int(y), round(float(v), 1)] for y, v in dens.items()]
out["density"] = {"columns": ["year", "max_density"], "rows": dens_rows}
print("\n=== TABLE_density ===")
print(dens_rows[:3], '...', dens_rows[-3:])

# ----- TABLE: Moore line vs actual (1971-2019) just for CPU -----
# Moore 2-yr doubling line passing through Intel 4004 (1971, 2300)
moore_line_rows = []
for yr in range(1971, 2020):
    moore = 2300 * (2 ** ((yr - 1971) / 2))
    moore_line_rows.append([yr, round(moore, 0)])
out["moore_line"] = {"columns": ["year", "moore_predicted_tc"], "rows": moore_line_rows}
print("\n=== TABLE_moore_line ===")
print(moore_line_rows[:3], '...', moore_line_rows[-3:])

# ----- TABLE: residuals (over-line) top 10 each fam -----
def with_resid(df, fam):
    x = df['year'].astype(float).values
    y = np.log10(df['tc'].astype(float).values)
    s, i = np.polyfit(x, y, 1)
    yhat = s*x + i
    out = df.copy()
    out['log10_resid'] = y - yhat
    out['family'] = fam
    return out

resid_rows = []
for fam, df in [('CPU', cpu_c), ('GPU', gpu_c)]:
    rdf = with_resid(df, fam)
    top = rdf.sort_values('log10_resid', ascending=False).head(5)
    for _, r in top.iterrows():
        resid_rows.append([r['name'], r['family'], int(r['year']), int(r['tc']), round(float(r['log10_resid']), 3)])
out["overperformers"] = {"columns": ["name", "family", "year", "tc", "log10_resid"], "rows": resid_rows}
print("\n=== TABLE_overperformers ===")
for r in resid_rows: print(r)

# ----- TABLE: dataset profile -----
profile_rows = [
    ["CPU", 176, 1970, 2019, 6, 9],
    ["GPU", 112, 1982, 2019, 0, 3],
    ["RAM", 47, 1963, 2018, 1, 28],
]
out["profile"] = {"columns": ["family", "rows", "year_min", "year_max", "missing_tc", "missing_process"], "rows": profile_rows}

with open('/tmp/chart_tables.json', 'w') as f:
    json.dump(out, f, indent=2)
print("\nWrote /tmp/chart_tables.json with all tables")
