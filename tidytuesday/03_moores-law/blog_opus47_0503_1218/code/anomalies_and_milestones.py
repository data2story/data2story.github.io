"""Anomalies and milestone chips: residuals to the Moore line, biggest jumps."""
import pandas as pd
import numpy as np
import os

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/03_moores-law'

cpu = pd.read_csv(os.path.join(DATA_DIR, 'cpu.csv'))
gpu = pd.read_csv(os.path.join(DATA_DIR, 'gpu.csv'))

cpu_c = cpu.dropna(subset=['transistor_count', 'date_of_introduction']).copy()
gpu_c = gpu.dropna(subset=['transistor_count', 'date_of_introduction']).copy()

# Compute residuals to a per-family Moore-style fit
def fit_resid(df):
    x = df['date_of_introduction'].astype(float).values
    y = np.log10(df['transistor_count'].astype(float).values)
    slope, intercept = np.polyfit(x, y, 1)
    yhat = slope * x + intercept
    df = df.copy()
    df['log10_pred'] = yhat
    df['log10_actual'] = y
    df['log10_resid'] = y - yhat
    return df, slope, intercept

cpu_c, cs, ci = fit_resid(cpu_c)
gpu_c, gs, gi = fit_resid(gpu_c)

# --- ana_12: Top positive residuals (chips that beat the line) ---
print("=== ana_12 ===")
print("CPU top 10 over-line:")
cols = ['processor', 'date_of_introduction', 'transistor_count', 'log10_resid']
print(cpu_c.sort_values('log10_resid', ascending=False).head(10)[cols].to_string(index=False))
print("\nCPU top 10 under-line:")
print(cpu_c.sort_values('log10_resid').head(10)[cols].to_string(index=False))

print("\nGPU top 10 over-line:")
cols2 = ['processor', 'date_of_introduction', 'transistor_count', 'log10_resid']
print(gpu_c.sort_values('log10_resid', ascending=False).head(10)[cols2].to_string(index=False))

# --- ana_13: Biggest year-over-year multiplicative jumps in CPU max ---
print("=== ana_13 ===")
cpu_max_year = cpu_c.groupby('date_of_introduction')['transistor_count'].max().sort_index()
ratios = cpu_max_year / cpu_max_year.shift(1)
print("CPU year-over-year max ratio (top 10):")
top_ratios = ratios.dropna().sort_values(ascending=False).head(10)
for yr, r in top_ratios.items():
    prev_yr_max = cpu_max_year.shift(1).loc[yr]
    cur_yr_max = cpu_max_year.loc[yr]
    chip = cpu_c[(cpu_c['date_of_introduction']==yr) & (cpu_c['transistor_count']==cur_yr_max)]['processor'].iloc[0]
    print(f"  {int(yr)}: {prev_yr_max:,.0f} -> {cur_yr_max:,.0f}  ({r:.2f}x)  chip: {chip}")

# --- ana_14: How close did Moore's 1965 prediction land? ---
print("=== ana_14 ===")
# Moore (1965): "by 1975 economics may dictate squeezing as many as 65,000 components on a single silicon chip"
# Find what was actually achieved in 1975 (or closest) in the CPU table
predict_year = 1975
predict_count = 65000
near = cpu_c[(cpu_c['date_of_introduction'] >= 1974) & (cpu_c['date_of_introduction'] <= 1976)]
print(f"Moore's 1965 prediction: {predict_count:,} components by {predict_year}")
print(f"\nActual CPUs released 1974-1976:")
print(near[['processor', 'date_of_introduction', 'transistor_count']].to_string(index=False))
# Closest single chip near 65K in 1975 era
# Extrapolate from fit
x_eval = np.array([1975.0])
y_eval = cs * x_eval + ci
pred_from_fit = 10 ** y_eval
print(f"\nFitted CPU log-line predicts at 1975: {pred_from_fit[0]:,.0f}")
# Highest 1975 actual
cpu_1975 = cpu_c[cpu_c['date_of_introduction']==1975]['transistor_count'].max() if (cpu_c['date_of_introduction']==1975).any() else None
print(f"highest 1975 actual: {cpu_1975}")

# --- ana_15: First chip past 1 million / 1 billion transistors ---
print("=== ana_15 ===")
all_c = pd.concat([cpu_c.assign(family='CPU', name=cpu_c['processor']),
                    gpu_c.assign(family='GPU', name=gpu_c['processor'])], ignore_index=True)
all_c = all_c.sort_values('date_of_introduction')
thresholds = [1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10]
for thr in thresholds:
    hit = all_c[all_c['transistor_count'] >= thr]
    if len(hit) > 0:
        first = hit.sort_values('date_of_introduction').iloc[0]
        print(f"  first to reach {thr:>12,.0f} transistors: {int(first['date_of_introduction'])} {first['family']} {first['name']}  ({int(first['transistor_count']):,})")

# --- ana_16: GPU vs CPU per-year max race ---
print("=== ana_16 ===")
cpu_max = cpu_c.groupby('date_of_introduction')['transistor_count'].max()
gpu_max = gpu_c.groupby('date_of_introduction')['transistor_count'].max()
combined = pd.DataFrame({'CPU_max': cpu_max, 'GPU_max': gpu_max}).fillna(0)
combined['gpu_lead'] = combined['GPU_max'] > combined['CPU_max']
years_gpu_lead = combined[combined['gpu_lead']].index.tolist()
years_cpu_lead = combined[~combined['gpu_lead']].index.tolist()
print(f"Years GPU max > CPU max: {len(years_gpu_lead)} years")
if years_gpu_lead:
    print(f"  first GPU lead year: {int(min(years_gpu_lead))}")
    print(f"  last GPU lead year:  {int(max(years_gpu_lead))}")
print(f"Years CPU max >= GPU max: {len(years_cpu_lead)} years")

# --- ana_17: Ratio of largest GPU to largest CPU each year (modern era) ---
print("=== ana_17 ===")
recent = combined[combined.index >= 2010].copy()
recent['gpu_to_cpu_ratio'] = recent['GPU_max'] / recent['CPU_max'].replace(0, np.nan)
print(recent[['CPU_max', 'GPU_max', 'gpu_to_cpu_ratio']].to_string())
