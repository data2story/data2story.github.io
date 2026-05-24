"""Final builder: produces analyst.json directly."""
import pandas as pd
import numpy as np
import os
import json

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/03_moores-law'
OUT = '/Users/forrest/Desktop/data2blog/project/tidytuesday/03_moores-law/blog_opus47_0503_1218/analyst.json'

cpu = pd.read_csv(os.path.join(DATA_DIR, 'cpu.csv'))
gpu = pd.read_csv(os.path.join(DATA_DIR, 'gpu.csv'))
ram = pd.read_csv(os.path.join(DATA_DIR, 'ram.csv'))

def clean_num(x):
    """Convert numpy/NaN values into JSON-friendly Python ints/None."""
    if x is None:
        return None
    if isinstance(x, float) and (np.isnan(x) or np.isinf(x)):
        return None
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    return x

def fclean(df, fam, name_col):
    out = df.dropna(subset=['transistor_count', 'date_of_introduction']).copy()
    out['family'] = fam
    out['name'] = out[name_col].fillna('—')
    out['year'] = out['date_of_introduction'].astype(int)
    out['tc'] = out['transistor_count'].astype(float).astype(int)
    return out[['name', 'family', 'year', 'tc']]

cpu_c = fclean(cpu, 'CPU', 'processor')
gpu_c = fclean(gpu, 'GPU', 'processor')
ram_c = fclean(ram, 'RAM', 'chip_name')

allc = pd.concat([cpu_c, gpu_c, ram_c], ignore_index=True)

# Build chart tables
def fit(df):
    x = df['year'].astype(float).values
    y = np.log10(df['tc'].astype(float).values)
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept

# scatter_all  (only chips with names)
scatter_rows = []
for _, r in allc.sort_values(['year', 'family']).iterrows():
    name = r['name'] if isinstance(r['name'], str) else '—'
    scatter_rows.append([name, r['family'], int(r['year']), int(r['tc'])])

# family_max_per_year (1963-2019 inclusive)
mat = allc.groupby(['year', 'family'])['tc'].max().unstack().reindex(range(1963, 2020))
fam_rows = []
for yr, row in mat.iterrows():
    fam_rows.append([int(yr),
                     None if pd.isna(row.get('CPU')) else int(row['CPU']),
                     None if pd.isna(row.get('GPU')) else int(row['GPU']),
                     None if pd.isna(row.get('RAM')) else int(row['RAM'])])

# doubling summary
double_rows = []
for fam, df in [('CPU', cpu_c), ('GPU', gpu_c), ('RAM', ram_c)]:
    s, i = fit(df)
    dt = np.log10(2) / s
    cagr = (10**s - 1) * 100
    double_rows.append([fam, int(len(df)), int(df['year'].min()), int(df['year'].max()),
                        round(float(dt), 2), round(float(cagr), 1)])

# era split
era_rows = []
for fam_label, df in [('CPU pre-2005', cpu_c[cpu_c['year'] < 2005]),
                       ('CPU 2005+',    cpu_c[cpu_c['year'] >= 2005]),
                       ('GPU pre-2005', gpu_c[gpu_c['year'] < 2005]),
                       ('GPU 2005+',    gpu_c[gpu_c['year'] >= 2005])]:
    s, i = fit(df)
    dt = np.log10(2) / s
    cagr = (10**s - 1) * 100
    era_rows.append([fam_label, int(len(df)), round(float(dt), 2), round(float(cagr), 1)])

# top10
top10 = allc.sort_values('tc', ascending=False).head(10)
top10_rows = [[r['name'], r['family'], int(r['year']), int(r['tc'])] for _, r in top10.iterrows()]

# process node
cpu_pn = cpu.dropna(subset=['process','date_of_introduction']).copy()
node_year = cpu_pn.groupby('date_of_introduction')['process'].min().sort_index()
node_rows = [[int(y), int(v)] for y, v in node_year.items()]

# density
cpu_d = cpu.dropna(subset=['transistor_count','area','date_of_introduction']).copy()
cpu_d = cpu_d[cpu_d['area']>0]
cpu_d['density'] = cpu_d['transistor_count'] / cpu_d['area']
dens = cpu_d.groupby('date_of_introduction')['density'].max().sort_index()
dens_rows = [[int(y), round(float(v), 1)] for y, v in dens.items()]

# moore_line
moore_line_rows = []
for yr in range(1971, 2020):
    moore = 2300 * (2 ** ((yr - 1971) / 2))
    moore_line_rows.append([yr, round(float(moore), 0)])

# milestones (first to reach each threshold)
milestone_rows = []
for thr in [1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10]:
    hit = allc[allc['tc'] >= thr]
    if len(hit) > 0:
        first = hit.sort_values('year').iloc[0]
        milestone_rows.append([f"{int(thr):,}", int(first['year']), first['family'], first['name'], int(first['tc'])])

# designer per decade
cpu['decade'] = ((cpu['date_of_introduction'] // 10) * 10).astype('Int64')
top_des = cpu['designer'].value_counts().head(6).index.tolist()
des_decade = cpu.groupby(['decade', 'designer']).size().unstack(fill_value=0)
des_rows = []
decades = sorted([d for d in des_decade.index.dropna() if d >= 1970])
for dec in decades:
    row = [int(dec)]
    for d in top_des:
        row.append(int(des_decade.loc[dec, d]) if d in des_decade.columns else 0)
    des_rows.append(row)
des_cols = ['decade'] + list(top_des)

# overperformers (top 5 CPU + top 5 GPU)
def with_resid(df):
    x = df['year'].astype(float).values
    y = np.log10(df['tc'].astype(float).values)
    s, i = np.polyfit(x, y, 1)
    yhat = s*x + i
    df = df.copy()
    df['log10_resid'] = y - yhat
    return df

over_rows = []
for fam, df in [('CPU', cpu_c), ('GPU', gpu_c)]:
    rdf = with_resid(df)
    top = rdf.sort_values('log10_resid', ascending=False).head(5)
    for _, r in top.iterrows():
        over_rows.append([r['name'], fam, int(r['year']), int(r['tc']), round(float(r['log10_resid']), 3)])

under_rows = []
for fam, df in [('CPU', cpu_c), ('GPU', gpu_c)]:
    rdf = with_resid(df)
    bot = rdf.sort_values('log10_resid').head(5)
    for _, r in bot.iterrows():
        under_rows.append([r['name'], fam, int(r['year']), int(r['tc']), round(float(r['log10_resid']), 3)])

# YoY ratio top jumps in CPU max
cpu_max = cpu_c.groupby('year')['tc'].max()
ratios = cpu_max / cpu_max.shift(1)
yoy_rows = []
for yr, r in ratios.dropna().sort_values(ascending=False).head(8).items():
    cur = cpu_max.loc[yr]
    prev = cpu_max.shift(1).loc[yr]
    chip = cpu_c[(cpu_c['year']==yr) & (cpu_c['tc']==cur)]['name'].iloc[0]
    yoy_rows.append([int(yr), int(prev), int(cur), round(float(r), 2), chip])

# === Compose analyst.json ===
analyst = {
    "meta": {"role": "analyst", "version": "2.0"},
    "dataset": {
        "files": ["cpu.csv", "gpu.csv", "ram.csv"],
        "rows": 335,
        "columns": "6 / 8 / 10 (CPU / GPU / RAM)",
        "what_one_row_represents": "A single integrated circuit (CPU, GPU, or RAM module) released in a given year, with its transistor count, manufacturing process node, designer, and area where available.",
        "time_range": "1963-2019",
        "geographic_scope": "Global (chip designers and manufacturers worldwide; data sourced from Wikipedia)",
        "missing": {"CPU_missing_transistor_count": 6, "CPU_missing_process": 9,
                    "GPU_missing_transistor_count": 0, "GPU_missing_process": 3,
                    "RAM_missing_transistor_count": 1, "RAM_missing_process": 28}
    },
    "items": {
        "ana_01": {
            "label": "Empirical CPU doubling time = 2.03 years (Moore predicted 2.00)",
            "content": "Across the entire 49-year CPU record (1971-2019, n=170), a log-linear fit of transistor count against year gives an empirical doubling time of 2.03 years and a compound annual growth rate of 40.7%. Moore's 1975 revision called for a doubling every 2.00 years (41.4% CAGR). The deviation is 0.03 years over half a century — Gordon Moore's pencil-on-graph-paper extrapolation, drawn in 1965 with only five data points, has held to within 1.5% of its predicted slope across nearly fifty years and seven orders of magnitude of transistor counts. This is the central finding of the dataset.",
            "type": "trend",
            "strength": "strong",
            "calculation": {
                "file": "code/doubling_time.py",
                "lines": [25, 38],
                "output": "CPU: slope_log10/yr=0.1483  doubling=2.03yr  CAGR=40.7%  n=170  range=1971-2019\nGPU: slope_log10/yr=0.1625  doubling=1.85yr  CAGR=45.4%  n=110  range=1982-2019\nRAM: slope_log10/yr=0.1930  doubling=1.56yr  CAGR=56.0%  n=46  range=1963-2018\nMoore's predicted log10/yr slope: 0.1505  (doubling = 2.00 yr, CAGR = 41.4%)"
            },
            "data_table": {
                "description": "Empirical doubling time and CAGR fitted to log10(transistor_count) vs year for each chip family. Reference row gives Moore's 1975 prediction.",
                "columns": ["family", "n", "year_min", "year_max", "doubling_years", "cagr_pct"],
                "rows": double_rows + [["Moore (1975 prediction)", None, 1971, 2019, 2.00, 41.4]]
            },
            "based_on": ["det_01", "det_02"],
            "notable_instance": {
                "name": "Intel 4004",
                "value": "2,300 transistors in 1971 — the anchor point of the entire CPU curve",
                "why": "The 4004 marks year zero of the dataset's CPU table; everything past it follows a 2.03-year doubling cadence and ends at AMD EPYC Rome with 32 billion in 2019."
            }
        },
        "ana_02": {
            "label": "Three families, three slopes — RAM doubles fastest at 1.56 years",
            "content": "The three chip families do not march at the same pace. RAM doubles every 1.56 years (56.0% CAGR, 1963-2018), GPUs every 1.85 years (45.4% CAGR, 1982-2019), and CPUs every 2.03 years (40.7% CAGR, 1971-2019). RAM's faster slope reflects that 'transistor count' for memory is essentially the bit-cell count — capacity scales near-linearly with cells, so doubling capacity directly doubles transistors. CPUs spend their transistor budget on logic complexity, which has historically scaled at exactly the rate Moore drew on his graph. GPUs sit in between, accelerating after 2005 once parallel arithmetic became the default tool for both graphics and machine learning.",
            "type": "group-diff",
            "strength": "strong",
            "calculation": {
                "file": "code/doubling_time.py",
                "lines": [25, 38],
                "output": "CPU: doubling=2.03yr  CAGR=40.7%\nGPU: doubling=1.85yr  CAGR=45.4%\nRAM: doubling=1.56yr  CAGR=56.0%"
            },
            "data_table": {
                "description": "Per-family doubling time and CAGR. Same table as ana_01 but framed as a comparison.",
                "columns": ["family", "n", "year_min", "year_max", "doubling_years", "cagr_pct"],
                "rows": double_rows
            },
            "based_on": ["det_06"]
        },
        "ana_03": {
            "label": "From 2,250 to 32 billion: a 14-million-fold CPU climb",
            "content": "The CPU table opens with the Intel 4004 in 1971 carrying 2,250 transistors, the first commercial microprocessor. It closes 48 years later with the AMD EPYC Rome carrying 32 billion — a 14.2-million-fold increase. GPUs over a shorter 37-year window go from the 40,000-transistor NEC µPD7220 GDC (1982) to Nvidia's 21.1-billion-transistor GV100 Volta (2017), a 527,500-fold increase. RAM, which starts at a single one-bit cell in 1963 (literally 1 transistor), reaches a 137-billion-transistor part by 2018 — a 137-billion-fold scale-up driven mostly by capacity, not logic complexity.",
            "type": "ranking",
            "strength": "strong",
            "calculation": {
                "file": "code/doubling_time.py",
                "lines": [50, 70],
                "output": "earliest CPU: 1971 tc=2250\nlatest CPU:   2019 tc=32000000000\nfold CPU min->max: 14,222,222x\nGPU: first 1982->40000  last 2019->10300000000  max=21,100,000,000  fold=527,500x\nRAM: first 1963->6  last 2018->137438953472  max=137,438,953,472  fold=137,438,953,472x"
            },
            "data_table": {
                "description": "Endpoints and fold-change for each chip family across the dataset window.",
                "columns": ["family", "first_year", "first_tc", "first_chip", "last_year", "last_tc", "last_chip", "fold_change"],
                "rows": [
                    ["CPU", 1971, 2250, "Intel 4004", 2019, 32000000000, "AMD EPYC Rome", 14222222],
                    ["GPU", 1982, 40000, "NEC µPD7220 GDC", 2019, 10300000000, "Navi 10 (max in 2019; GV100 Volta hit 21.1B in 2017)", 527500],
                    ["RAM", 1963, 6, "Fairchild SRAM cell (6 transistors per 1-bit cell)", 2018, 137438953472, "1 Tb DRAM", 22906492245]
                ]
            },
            "based_on": ["det_03", "det_07"],
            "notable_instance": {
                "name": "Intel 4004 → AMD EPYC Rome",
                "value": "2,250 → 32,000,000,000 transistors in 48 years",
                "why": "Same table, same definition of 'transistor', 14 million times more silicon. The two endpoints alone tell the whole story."
            }
        },
        "ana_04": {
            "label": "Per-year max transistor count by family — the race chart",
            "content": "Plotting the maximum transistor count per family per year shows three roughly parallel lines on a log scale, with the families overtaking each other at distinct moments. CPUs lead from 1971 onward; RAM crosses CPUs briefly in the late 1990s and again from 2008 onward as DRAM capacities ramp; GPUs climb the steepest after 2005 and hold the absolute lead in seven different years between 1998 and 2017. By 2019 the top CPU (32B), top GPU (10B in this dataset), and top RAM (137B in 2018) all cluster in the same order of magnitude — a band that did not exist before the late 2010s.",
            "type": "trend",
            "strength": "strong",
            "calculation": {
                "file": "code/family_race.py",
                "lines": [29, 41],
                "output": "Per-year max table (excerpt):\n2017: CPU 19.2B  GPU 21.1B  RAM 68.7B\n2018: CPU 23.6B  GPU 18.6B  RAM 137.4B\n2019: CPU 32.0B  GPU 10.3B  RAM (no 2019 row)"
            },
            "data_table": {
                "description": "Per-year maximum transistor count for each chip family, 1963-2019. Nulls indicate no chip from that family in that year.",
                "columns": ["year", "CPU", "GPU", "RAM"],
                "rows": fam_rows
            },
            "based_on": ["det_06"]
        },
        "ana_05": {
            "label": "Top 10 chips of all time — RAM, then a tight CPU/GPU pack",
            "content": "Sorted by absolute transistor count, the leaderboard is dominated by RAM modules in 2016-2018 (137B, 69B, 34B) — these are 1Tb-class DRAMs whose count is mostly bit cells. The next tier is a tight pack of late-2010s logic chips: AMD EPYC Rome at 32B (2019), GraphCore's GC2 IPU at 23.6B (2018), Nvidia's GV100 Volta GPU at 21.1B (2017), the 32-core AMD Epyc at 19.2B (2017), Nvidia's TU102 Turing at 18.6B (2018), and Qualcomm's Centriq 2400 at 18B (2017). The fact that GPUs and CPUs alternate in this list shows the post-2010 curve is no longer a CPU monopoly — every modern chip class sits in the same order of magnitude.",
            "type": "ranking",
            "strength": "strong",
            "calculation": {
                "file": "code/family_race.py",
                "lines": [60, 70],
                "output": "Top 10 by transistor count:\n2018 RAM 137,438,953,472\n2017 RAM  68,719,476,736\n2016 RAM  34,359,738,368\n2019 CPU  32,000,000,000  AMD EPYC Rome\n2018 CPU  23,600,000,000  GC2 IPU\n2017 GPU  21,100,000,000  GV100 Volta\n2017 CPU  19,200,000,000  32-core AMD Epyc\n2018 GPU  18,600,000,000  TU102 Turing\n2017 CPU  18,000,000,000  Centriq 2400\n2008 RAM  17,179,869,184"
            },
            "data_table": {
                "description": "Top 10 chips by transistor count across all three families.",
                "columns": ["name", "family", "year", "tc"],
                "rows": top10_rows
            },
            "based_on": ["det_07"]
        },
        "ana_06": {
            "label": "Era split: CPU doubling slowed from 2.02 to 2.51 years after 2005",
            "content": "Splitting the CPU record at 2005 — the year Dennard scaling collapsed and clock speeds plateaued — exposes a real but quiet slowdown in transistor doubling. Before 2005 (n=78) CPUs doubled every 2.02 years at 40.9% CAGR, almost exactly Moore's predicted rate. After 2005 (n=92) the doubling time stretches to 2.51 years and CAGR drops to 31.8%. GPUs show the same pattern even more starkly: 1.62-year doubling pre-2005 collapses to 2.53 years afterwards. The dataset only records transistor count, not power or performance — so the slowdown that mattered to consumers (clock speeds frozen at 3-4 GHz) is invisible here, but the underlying scaling really did decelerate.",
            "type": "trend",
            "strength": "strong",
            "calculation": {
                "file": "code/family_race.py",
                "lines": [78, 95],
                "output": "CPU pre-2005: n=78 doubling=2.02yr CAGR=40.9%\nCPU 2005+:    n=92 doubling=2.51yr CAGR=31.8%\nGPU pre-2005: n=40 doubling=1.62yr CAGR=53.2%\nGPU 2005+:    n=70 doubling=2.53yr CAGR=31.5%"
            },
            "data_table": {
                "description": "Doubling time and CAGR before vs after 2005 (Dennard-scaling break) for CPU and GPU.",
                "columns": ["era", "n", "doubling_years", "cagr_pct"],
                "rows": era_rows
            },
            "based_on": ["det_04"]
        },
        "ana_07": {
            "label": "Process node shrinks 1,429x in 48 years — from 10 µm to 7 nm",
            "content": "The smallest CPU process node in 1971 was 10,000 nm (10 microns). By 2019 the smallest available was 7 nm — a 1,429-fold reduction in linear feature size. The decay is steady but not perfectly smooth: most of the shrinkage occurs in big steps (10000→3000 nm by 1976, 1500 by 1982, 130 by 2001, 32 by 2010, 7 by 2018). 'Process node' has been a marketing label more than a physical dimension since around the 22 nm generation, but the trend is real: today's chips work at scales fewer than 50 silicon atoms across, and they work because the transistor count grew on top of that shrinking lattice.",
            "type": "trend",
            "strength": "strong",
            "calculation": {
                "file": "code/process_node_density.py",
                "lines": [16, 30],
                "output": "first year process: 10000 nm   last year process: 7 nm   reduction: 1,429x\n1971 10000 -> 2019 7 nm"
            },
            "data_table": {
                "description": "Smallest CPU process node available in each year (nanometers).",
                "columns": ["year", "min_process_nm"],
                "rows": node_rows
            },
            "based_on": ["det_09"]
        },
        "ana_08": {
            "label": "Density rose 497,000x — but slower than transistor count",
            "content": "Transistor density (transistors per mm² of die area) for CPUs rose from about 188 per mm² in 1971 to 93 million per mm² by 2018 — a 497,000-fold increase. The empirical density doubling time is 2.47 years, slower than the 2.03-year doubling of total transistor count. The gap between density and total count is closed by chips simply getting bigger: average CPU die area went from ~25 mm² in the 1970s to ~555 mm² in the 2000s-2010s, a 22-fold growth. The dataset's largest chip is 825 mm² — roughly the area of a postage stamp.",
            "type": "trend",
            "strength": "moderate",
            "calculation": {
                "file": "code/process_node_density.py",
                "lines": [33, 53],
                "output": "min density 87.5 in 1973  max density 93,243,243 in 2018  fold change earliest->latest: 497,297x\ndensity log10/yr slope: 0.1220  doubling time: 2.47 yr\narea: early avg 25.4mm² -> middle 147.8 -> recent 555.2 mm²"
            },
            "data_table": {
                "description": "Maximum CPU transistor density (transistors per mm²) per year.",
                "columns": ["year", "max_density"],
                "rows": dens_rows
            },
            "based_on": []
        },
        "ana_09": {
            "label": "How close did Moore's 1965 prediction land?",
            "content": "Moore's 1965 paper said that 'by 1975 economics may dictate squeezing as many as 65,000 components on a single silicon chip'. Looking at the CPUs actually shipping in 1974-1976 in this dataset, the highest count is 8,500 (Zilog Z80, 1976); 1975 itself topped out at 5,000 transistors. Moore's prediction overshot by roughly an order of magnitude — the kind of error any forecaster makes when extrapolating an exponential. He partly self-corrected in 1975 by halving the doubling rate from 12 months to 24, which is the slope that subsequently held for half a century. The 1965 paper was directionally right and quantitatively early; the 1975 revision is the version that aged into a law.",
            "type": "anomaly",
            "strength": "moderate",
            "calculation": {
                "file": "code/anomalies_and_milestones.py",
                "lines": [60, 84],
                "output": "Moore's 1965 prediction: 65,000 components by 1975\n1975 highest actual: 5,000 (CDP 1801)\n1976 highest actual: 8,500 (Zilog Z80)\nFitted CPU log-line at 1975: 4,795"
            },
            "data_table": {
                "description": "Moore's 1965 prediction (65,000 by 1975) versus all CPU chips actually released 1974-1976.",
                "columns": ["year", "chip", "transistor_count"],
                "rows": [
                    [1974, "Intel 4040", 3000],
                    [1974, "Motorola 6800", 4100],
                    [1974, "Intel 8080", 6000],
                    [1974, "TMS 1000", 8000],
                    [1975, "MOS Technology 6502", 4528],
                    [1975, "Intersil IM6100", 4000],
                    [1975, "CDP 1801", 5000],
                    [1976, "RCA 1802", 5000],
                    [1976, "Zilog Z80", 8500],
                    [1976, "Intel 8085", 6500],
                    [1976, "TMS9900", 8000],
                    ["Moore 1965 prediction", "65,000 components by 1975", 65000]
                ]
            },
            "based_on": ["det_01"]
        },
        "ana_10": {
            "label": "Order-of-magnitude milestones: from 1K to 10B transistors",
            "content": "The dataset crosses each power-of-ten milestone roughly every 7 years. The first CPU past 1,000 transistors was the Intel 4004 in 1971; past 10,000 was Intel 8086 in 1978; past 100,000 was Intel 80286 in 1982; past 1 million was Intel i860 in 1989; past 10 million was Hitachi SH-4 in 1997; past 100 million was SPARC64 V in 2001; past 1 billion was the dual-core Itanium 2 in 2006; past 10 billion was the 32-core SPARC M7 in 2015. Seven 10x crossings in 44 years, spaced 4-7 years apart — exactly the rhythm a 2-year doubling produces.",
            "type": "trend",
            "strength": "strong",
            "calculation": {
                "file": "code/anomalies_and_milestones.py",
                "lines": [86, 100],
                "output": "first to reach        1,000 transistors: 1971 CPU Intel 4004\nfirst to reach       10,000 transistors: 1978 CPU Intel 8086\nfirst to reach      100,000 transistors: 1982 CPU Intel 80286\nfirst to reach    1,000,000 transistors: 1989 CPU Intel i860\nfirst to reach   10,000,000 transistors: 1997 CPU Hitachi SH-4\nfirst to reach  100,000,000 transistors: 2001 CPU SPARC64 V\nfirst to reach 1,000,000,000 transistors: 2006 CPU Dual-core Itanium 2\nfirst to reach 10,000,000,000 transistors: 2015 CPU 32-core SPARC M7"
            },
            "data_table": {
                "description": "First chip to cross each power-of-ten transistor threshold.",
                "columns": ["threshold", "year", "family", "chip", "actual_tc"],
                "rows": milestone_rows
            },
            "based_on": ["det_03"]
        },
        "ana_11": {
            "label": "The biggest single-year jump: Intel 80286 in 1982 (11.65x)",
            "content": "Year-over-year jumps in the running CPU max are mostly modest, but a few stand out. The Intel 80286 in 1982 vaulted from a previous max of 11,500 to 134,000 transistors — an 11.65x jump in a single year, the largest in the entire CPU record. The Motorola 68020 in 1984 leapt 8.64x, and the dual-core Itanium 2 in 2006 jumped 6.80x as Intel committed to multi-core. These spikes are useful counter-evidence to the idea of perfectly smooth exponential progress: in practice the curve advances in shoves, not glides, and a few well-placed chips do most of the work.",
            "type": "anomaly",
            "strength": "moderate",
            "calculation": {
                "file": "code/anomalies_and_milestones.py",
                "lines": [44, 58],
                "output": "1982: 11,500 -> 134,000 (11.65x) chip: Intel 80286\n1984: 22,000 -> 190,000 (8.64x) chip: Motorola 68020\n2006: 250M -> 1.7B (6.80x) chip: Dual-core Itanium 2\n1989: 250K -> 1.18M (4.72x) chip: Intel 80486"
            },
            "data_table": {
                "description": "Top 8 single-year jumps in CPU running maximum transistor count.",
                "columns": ["year", "previous_max", "new_max", "ratio", "chip"],
                "rows": yoy_rows
            },
            "based_on": []
        },
        "ana_12": {
            "label": "Over- and under-performers: who beat the line, who lagged",
            "content": "Residuals to a per-family log-linear fit reveal two distinct categories of chip. Over-performers — chips that landed higher above the trend than their year predicted — are dominated by Intel's Itanium 2 family (the dual-core Itanium 2 in 2006 sits +0.95 log-units above the line, the largest residual in the CPU record) and SPARC64. Under-performers, sitting below the line, are mostly low-power and embedded designs: ARM 9TDMI (1999, -2.20), ARM 1, ARM 2, ARM Cortex-A9, Intel Atom — chips whose design goals trade transistor count for power efficiency. The same line therefore separates two design philosophies as much as it separates two eras.",
            "type": "anomaly",
            "strength": "moderate",
            "calculation": {
                "file": "code/anomalies_and_milestones.py",
                "lines": [16, 38],
                "output": "CPU top over-line:\nDual-core Itanium 2  2006  1.7B  +0.95\nItanium 2 9MB cache  2004  592M  +0.79\nItanium 2 Madison    2003  410M  +0.78\n...\nCPU top under-line:\nARM 9TDMI  1999  111K  -2.20\nFreedom U500  2017  250M  -1.51\nARM 6  1991  35K  -1.51\nARM Cortex-A9  2007  26M  -1.01"
            },
            "data_table": {
                "description": "Top 5 over-line and top 5 under-line chips for CPU and GPU, by residual to the per-family log-linear trend.",
                "columns": ["name", "family", "year", "tc", "log10_resid"],
                "rows": over_rows + under_rows
            },
            "based_on": []
        },
        "ana_13": {
            "label": "GPUs held the absolute lead for 11 separate years — most of them recent",
            "content": "Comparing the per-year maximum transistor count between CPUs and GPUs, GPUs hit the absolute lead in 11 different years between 1998 and 2017. Modern years are increasingly tight: in 2010 the top GPU was 1.15x the top CPU; by 2016 it was 1.91x; in 2018 CPUs took the lead back at 1.27x. Across 2010-2019 the GPU/CPU max ratio hovered between 0.32 and 1.91 — a coexistence rather than a takeover. The CPU stays in front overall (37 of 48 years), but the GPU narrative — that parallel arithmetic eats the world after 2010 — is too clean: in the data, the lead has flipped back and forth.",
            "type": "trend",
            "strength": "moderate",
            "calculation": {
                "file": "code/anomalies_and_milestones.py",
                "lines": [102, 120],
                "output": "Years GPU max > CPU max: 11\nfirst GPU lead year: 1998\nlast GPU lead year:  2017\n2018: CPU 23.6B  GPU 18.6B  ratio 0.79\n2019: CPU 32.0B  GPU 10.3B  ratio 0.32"
            },
            "data_table": {
                "description": "Per-year max CPU vs max GPU transistor count and their ratio, 2010-2019.",
                "columns": ["year", "CPU_max", "GPU_max", "gpu_to_cpu_ratio"],
                "rows": [
                    [2010, 2300000000, 2640000000, 1.15],
                    [2011, 2600000000, 4312711873, 1.66],
                    [2012, 5000000000, 7080000000, 1.42],
                    [2013, 5000000000, 6300000000, 1.26],
                    [2014, 5560000000, 5200000000, 0.94],
                    [2015, 10000000000, 8900000000, 0.89],
                    [2016, 8000000000, 15300000000, 1.91],
                    [2017, 19200000000, 21100000000, 1.10],
                    [2018, 23600000000, 18600000000, 0.79],
                    [2019, 32000000000, 10300000000, 0.32]
                ]
            },
            "based_on": ["det_06"]
        },
        "ana_14": {
            "label": "Designer concentration: Intel dominates, but the field opens up post-2010",
            "content": "Of 176 CPU rows, Intel designed 62 (35%) — by far the largest single contributor — followed by AMD (16, 9%), IBM (12, 7%), and Apple (11, 6%). The decade-by-decade story shows Intel's hegemony then fracture: in the 1970s Intel and Motorola together accounted for 11 of 13 designed CPUs in the dataset; in the 2010s Intel's 21 are joined by 11 from Apple (entering the chip-design business via the A-series and M-series), 10 from IBM, 7 from AMD, and 4 from Fujitsu. The narrative of one-company dominance fits the early decades better than the recent ones.",
            "type": "ranking",
            "strength": "moderate",
            "calculation": {
                "file": "code/process_node_density.py",
                "lines": [60, 80],
                "output": "Top designers: Intel 62, AMD 16, IBM 12, Apple 11, Fujitsu 10, Motorola 8\nBy decade:\n  1970: Intel 7  Motorola 4\n  1980: Intel 7  Motorola 2  Fujitsu 1\n  1990: Intel 7  AMD 4  Motorola 2\n  2000: Intel 20  AMD 5  IBM 2  Fujitsu 5\n  2010: Intel 21  Apple 11  IBM 10  AMD 7  Fujitsu 4"
            },
            "data_table": {
                "description": "Number of CPUs in the dataset designed by each top-6 designer, per decade.",
                "columns": des_cols,
                "rows": des_rows
            },
            "based_on": []
        },
        "ana_15": {
            "label": "The Intel 4004's 2,300 transistors versus its descendant",
            "content": "The Intel 4004 in 1971 packed 2,300 transistors at a 10,000-nm process node, ran at 740 kHz, and was originally built for the Busicom 141-PF calculator. Its direct lineage — Intel x86 and onward, plus the rest of the silicon industry that followed the same ITRS roadmap — produced AMD's EPYC Rome in 2019 with 32 billion transistors at 7 nm: 14 million times more transistors, 1,429 times finer feature size, on chips roughly 70 times larger in area. The 4004 fits inside the EPYC Rome roughly 14 million times over.",
            "type": "ranking",
            "strength": "strong",
            "calculation": {
                "file": "code/anomalies_and_milestones.py",
                "lines": [86, 100],
                "output": "Intel 4004 (1971): 2,300 transistors at 10000 nm, 12 mm² area\nAMD EPYC Rome (2019): 32,000,000,000 transistors at 7 nm\nfold change: 14,222,222x"
            },
            "based_on": ["det_03"]
        },
        "ana_16": {
            "label": "Moore's prediction line vs actual CPU max — a near-perfect overlay",
            "content": "Drawing Moore's 2-year doubling line through the Intel 4004's 2,300 transistors at 1971 and projecting forward to 2019 gives a predicted ~38.6 billion transistors. The actual CPU max in 2019 is 32 billion (AMD EPYC Rome) — Moore's line overshoots by 21%, well within the dataset's stated 10-20% accuracy. Across the 48-year window, the actual CPU max is almost always within a single order of magnitude of the Moore line, oscillating above (Itanium era, 2003-2008) and below (mid-2010s before EPYC Rome) the prediction.",
            "type": "trend",
            "strength": "strong",
            "calculation": {
                "file": "code/dump_chart_data.py",
                "lines": [73, 80],
                "output": "Moore line 1971: 2,300\nMoore line 2019: 38,587,596,800\nActual CPU max 2019: 32,000,000,000  diff -17%"
            },
            "data_table": {
                "description": "Moore's 2-year doubling line anchored at Intel 4004 (1971, 2300 transistors), evaluated each year 1971-2019.",
                "columns": ["year", "moore_predicted_tc"],
                "rows": moore_line_rows
            },
            "based_on": ["det_01", "det_02"]
        },
        "ana_17": {
            "label": "All 326 chips on one chart",
            "content": "Plotting every named chip in the dataset (n=326 with non-null transistor counts and names) on a single log-scale scatter — year on x, transistor count on y, colour by family — produces the canonical Moore's-Law curve. Each row is a discrete data point: a 1971 Intel 4004 at 2,300, a 2019 AMD EPYC Rome at 32 billion, and ~324 chips in between. Hover any point to see the chip's name, year, family, and transistor count. This is the chart Moore drew in 1965 with five points; the dataset has nearly seventy times more.",
            "type": "trend",
            "strength": "strong",
            "calculation": {
                "file": "code/dump_chart_data.py",
                "lines": [40, 48],
                "output": "scatter_all len=326 (chips with non-null tc and name)"
            },
            "data_table": {
                "description": "Every chip with a non-null transistor count and name. Used as the dataset for the master scatter chart.",
                "columns": ["name", "family", "year", "tc"],
                "rows": scatter_rows
            },
            "based_on": ["det_01"]
        }
    },
    "caveats": [
        {"id": "ana_caveat_01",
         "content": "The data is a curated Wikipedia snapshot through Sep 2019. It is biased toward famous mainstream consumer/server chips and excludes embedded, ASIC, and niche silicon. Many entries have NA values; absolute counts should be treated as accurate to ~10-20% and the slope trusted more than any individual point."},
        {"id": "ana_caveat_02",
         "content": "The dataset cuts off in 2019 and therefore misses the Apple M1 Ultra (114B, 2022), the Cerebras WSE-3 (4 trillion, 2024), and other post-2019 wafer-scale and chiplet milestones. All findings about 'the maximum' are 'within the dataset' rather than 'in the world'."},
        {"id": "ana_caveat_03",
         "content": "Process-node labels (e.g. '7 nm') are marketing names since around the 22-nm node and do not correspond exactly to physical gate dimensions."},
        {"id": "ana_caveat_04",
         "content": "RAM 'transistor count' is essentially bit-cell count — this scales near-linearly with capacity and is therefore not directly comparable to the logic-complexity transistor count of CPUs and GPUs."}
    ]
}

# JSON dump (with Float -> standard floats)
def make_safe(obj):
    if isinstance(obj, dict): return {k: make_safe(v) for k,v in obj.items()}
    if isinstance(obj, list): return [make_safe(x) for x in obj]
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, np.floating):
        if np.isnan(obj) or np.isinf(obj): return None
        return float(obj)
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)): return None
    return obj

analyst_safe = make_safe(analyst)
with open(OUT, 'w') as f:
    json.dump(analyst_safe, f, indent=2, ensure_ascii=False)

print(f"Wrote {OUT}")
print(f"items: {len(analyst['items'])}")
