#!/usr/bin/env python3
"""Profiling + full-history (1991-) submissions & downloads analysis.
Run from DATA_DIR. All findings prefixed `=== ana_xx ===`."""
import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2story-skill/data/arxiv"

sub_cat = pd.read_csv(f"{DATA}/submissions_by_category.csv")
sub_arch = pd.read_csv(f"{DATA}/submissions_by_archive.csv")
hist = pd.read_csv(f"{DATA}/get_monthly_submissions.csv")
dls = pd.read_csv(f"{DATA}/get_monthly_downloads.csv")

# --- profile: dataset shapes ---
print("=== profile ===")
for name, df in [("submissions_by_category", sub_cat), ("submissions_by_archive", sub_arch),
                 ("get_monthly_submissions", hist), ("get_monthly_downloads", dls)]:
    print(f"{name}: rows={len(df)} cols={list(df.columns)}")
    print("  nulls:", df.isnull().sum().to_dict())
print("cat groups:", sorted(sub_cat['group'].unique()))
print("n categories:", sub_cat['category'].nunique())
print("n archives:", sub_arch['archive'].nunique())
print("cat month range:", sub_cat['month'].min(), sub_cat['month'].max())
print("arch month range:", sub_arch['month'].min(), sub_arch['month'].max())
print("hist month range:", hist['month'].min(), hist['month'].max())
print("dls month range:", dls['month'].min(), dls['month'].max())

# parse dates
hist['dt'] = pd.to_datetime(hist['month'])
hist['year'] = hist['dt'].dt.year
dls['dt'] = pd.to_datetime(dls['month'])
dls['year'] = dls['dt'].dt.year

# --- ana_01: Full-history growth arc 1991-2025 ---
print("=== ana_01 ===")
# annual totals; exclude partial final year 2026 from "complete year" framing
yr = hist.groupby('year')['submissions'].sum()
print("Annual submission totals (full history):")
for y, v in yr.items():
    print(f"  {y}: {int(v)}")
print(f"First month 1991-07: {int(hist[hist['month']=='1991-07']['submissions'].iloc[0])}")
print(f"2024 total: {int(yr.get(2024,0))}")
# milestone crossings (cumulative)
hist_sorted = hist.sort_values('dt').copy()
hist_sorted['cum'] = hist_sorted['submissions'].cumsum()
for milestone in [500_000, 1_000_000, 2_000_000, 2_500_000]:
    cross = hist_sorted[hist_sorted['cum'] >= milestone]
    if len(cross):
        r = cross.iloc[0]
        print(f"  cumulative {milestone:,} crossed at {r['month']} (cum={int(r['cum']):,})")
print(f"Total cumulative submissions through {hist_sorted['month'].iloc[-1]}: {int(hist_sorted['cum'].iloc[-1]):,}")

# --- ana_02: CAGR of monthly submission rate ---
print("=== ana_02 ===")
# use complete calendar years only for CAGR (1992 first full year, 2025 last full year)
full_yr = yr[(yr.index >= 1992) & (yr.index <= 2025)]
start_y, end_y = 1992, 2025
v0, v1 = full_yr[start_y], full_yr[end_y]
n = end_y - start_y
cagr = (v1/v0)**(1/n) - 1
print(f"{start_y} annual={int(v0)}, {end_y} annual={int(v1)}, years={n}")
print(f"CAGR {start_y}-{end_y}: {cagr*100:.2f}%")
# also recent-era CAGR 2010-2025
v0b, v1b = full_yr[2010], full_yr[2025]
cagr2 = (v1b/v0b)**(1/(2025-2010)) - 1
print(f"2010 annual={int(v0b)}, 2025 annual={int(v1b)}, CAGR 2010-2025: {cagr2*100:.2f}%")
# decade snapshots
print("Decade snapshots (annual submissions):")
for y in [1992, 2000, 2010, 2020, 2024, 2025]:
    print(f"  {y}: {int(full_yr.get(y, yr.get(y, 0)))}")

# --- ana_03: 20,000/month and 24k milestone (monthly rate) ---
print("=== ana_03 ===")
hist['mavg'] = hist['submissions']
over20k = hist[(hist['submissions'] >= 20000) & (hist['dt'] < '2026-01-01')].sort_values('dt')
print(f"First month >= 20,000 submissions: {over20k.iloc[0]['month']} = {int(over20k.iloc[0]['submissions'])}")
print("Peak single months (top 8, excl 2026):")
top_months = hist[hist['dt'] < '2026-01-01'].nlargest(8, 'submissions')[['month','submissions']]
for _, r in top_months.iterrows():
    print(f"  {r['month']}: {int(r['submissions'])}")

# --- ana_04: COVID-19 inflection in full-history series (2020) ---
print("=== ana_04 ===")
m2019 = hist[(hist['dt']>='2019-01-01')&(hist['dt']<'2020-01-01')]['submissions'].mean()
m2020 = hist[(hist['dt']>='2020-01-01')&(hist['dt']<'2021-01-01')]['submissions'].mean()
print(f"2019 monthly avg: {m2019:.0f}; 2020 monthly avg: {m2020:.0f}; YoY: {(m2020/m2019-1)*100:+.1f}%")
# month-over-month look at early 2020
e2020 = hist[(hist['dt']>='2019-10-01')&(hist['dt']<='2020-08-01')][['month','submissions']]
print("Late-2019 to mid-2020 monthly:")
for _, r in e2020.iterrows():
    print(f"  {r['month']}: {int(r['submissions'])}")

# --- ana_05: Downloads growth 1994-2025 (demand) ---
print("=== ana_05 ===")
# DATA QUALITY: downloads file has a 14-month gap (2023-12 .. 2024-12 missing).
dls_sorted = dls.sort_values('dt')
prev=None; gaps=[]
for _,r in dls_sorted.iterrows():
    if prev is not None:
        g=(r['dt'].year-prev.year)*12+(r['dt'].month-prev.month)
        if g>1: gaps.append((prev.strftime('%Y-%m'), r['dt'].strftime('%Y-%m'), g-1))
    prev=r['dt']
print("Download series gaps (months missing):", gaps)
dyr = dls.groupby('year')['downloads'].sum()
# years with full 12 months only, for annual totals
ymon = dls.groupby('year')['month'].nunique()
print("Annual downloads (selected COMPLETE years):")
for y in [1994, 2000, 2010, 2015, 2020, 2023, 2025]:
    if y in dyr.index:
        print(f"  {y}: {int(dyr[y]):,} ({ymon[y]} months)")
print(f"First nonzero month: {dls[dls['downloads']>0].iloc[0]['month']} = {int(dls[dls['downloads']>0].iloc[0]['downloads'])}")
# recent monthly download scale (2025, complete)
recent_dl = dls[(dls['dt']>='2025-01-01')&(dls['dt']<'2026-01-01')][['month','downloads']]
print(f"Mean monthly downloads 2025: {recent_dl['downloads'].mean():,.0f}")
print(f"Peak month: {dls.loc[dls['downloads'].idxmax(),'month']} = {int(dls['downloads'].max()):,}")

# --- ana_06: Downloads-vs-submissions relationship ---
print("=== ana_06 ===")
# align on month over overlapping range
mh = hist[['month','submissions']].copy()
md = dls[['month','downloads']].copy()
merged = mh.merge(md, on='month', how='inner')
merged['dt'] = pd.to_datetime(merged['month'])
# downloads per submission ratio over time
merged['dl_per_sub'] = merged['downloads'] / merged['submissions']
corr = merged[['submissions','downloads']].corr().iloc[0,1]
print(f"Overlapping months: {len(merged)} ({merged['month'].min()}..{merged['month'].max()})")
print(f"Pearson corr(submissions, downloads): {corr:.3f}")
# log corr
lc = np.corrcoef(np.log(merged['submissions'].clip(lower=1)), np.log(merged['downloads'].clip(lower=1)))[0,1]
print(f"Log-log corr: {lc:.3f}")
for y in [2000, 2010, 2020, 2024]:
    sub = merged[merged['dt'].dt.year==y]
    if len(sub):
        print(f"  {y}: avg downloads/submission = {sub['dl_per_sub'].mean():.1f}")

# --- ana_07: Seasonality / month-of-year effect (submissions) ---
print("=== ana_07 ===")
# use full complete years 2015-2024 to avoid early sparse + partial tail
seas = hist[(hist['dt']>='2015-01-01')&(hist['dt']<'2025-01-01')].copy()
seas['moy'] = seas['dt'].dt.month
seas['yr'] = seas['dt'].dt.year
# normalize each month by that year's mean to remove trend, then average by month-of-year
seas['yr_mean'] = seas.groupby('yr')['submissions'].transform('mean')
seas['idx'] = seas['submissions'] / seas['yr_mean']
moy = seas.groupby('moy')['idx'].mean()
print("Month-of-year seasonal index (1.0 = avg month), 2015-2024:")
names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
for m in range(1,13):
    print(f"  {names[m]}: {moy[m]:.3f}")
print(f"Highest: {names[moy.idxmax()]} ({moy.max():.3f}); Lowest: {names[moy.idxmin()]} ({moy.min():.3f})")

# --- ana_08: 2025-10 truncation flag (full-history sanity) ---
print("=== ana_08 ===")
oct25 = hist[hist['month']=='2025-10']['submissions']
sep25 = hist[hist['month']=='2025-09']['submissions']
print(f"2025-09 full-history submissions: {int(sep25.iloc[0]) if len(sep25) else 'NA'}")
print(f"2025-10 full-history submissions: {int(oct25.iloc[0]) if len(oct25) else 'NA'}")
print("Note: per-CATEGORY/ARCHIVE files truncate at 2025-10 with tiny counts; full-history file continues to 2026-05.")
print("per-archive 2025-10 sum:", int(sub_arch[sub_arch['month']=='2025-10-01']['count'].sum()))
print("per-archive 2025-09 sum:", int(sub_arch[sub_arch['month']=='2025-09-01']['count'].sum()))

# --- ana_09: historical_delta is small noise ---
print("=== ana_09 ===")
hd = hist['historical_delta']
print(f"historical_delta: min={hd.min()}, max={hd.max()}, mean={hd.mean():.2f}, abs-mean={hd.abs().mean():.2f}")
print(f"share of months with |delta|>50: {(hd.abs()>50).mean()*100:.1f}%")
print(f"|delta| as % of submissions (median): {(hd.abs()/hist['submissions'].clip(lower=1)*100).median():.3f}%")
