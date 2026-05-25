#!/usr/bin/env python3
"""Archive-level rankings + anomalies + AI-slop-era tail check. Run from DATA_DIR.
EXCLUDE 2025-10 (partial) from rankings/growth."""
import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2story-skill/data/arxiv"
arch = pd.read_csv(f"{DATA}/submissions_by_archive.csv")
arch['dt'] = pd.to_datetime(arch['month'])
arch_full = arch.copy()
arch = arch[arch['dt'] < '2025-10-01'].copy()
arch['year'] = arch['dt'].dt.year

# --- ana_18: Top archives by cumulative submissions ---
print("=== ana_18 ===")
tot = arch.groupby('archive')['count'].sum().sort_values(ascending=False)
grand = tot.sum()
print(f"20 archives, grand total (2022-01..2025-09): {int(grand):,}")
for a, v in tot.items():
    print(f"  {a}: {int(v):,} ({v/grand*100:.1f}%)")

# --- ana_19: Archive growth first-12mo vs last-12mo ---
print("=== ana_19 ===")
f12 = arch[(arch['dt']>='2022-01-01')&(arch['dt']<'2023-01-01')].groupby('archive')['count'].sum()
l12 = arch[(arch['dt']>='2024-10-01')&(arch['dt']<'2025-10-01')].groupby('archive')['count'].sum()
gr = pd.DataFrame({'f12':f12,'l12':l12}).fillna(0)
gr['ratio'] = gr['l12']/gr['f12']
print("Archive growth (first 12mo -> last 12mo), sorted:")
for a, r in gr.sort_values('ratio', ascending=False).iterrows():
    print(f"  {a}: {int(r['f12'])} -> {int(r['l12'])} (x{r['ratio']:.2f}, {(r['ratio']-1)*100:+.0f}%)")

# --- ana_20: cs archive is the giant ---
print("=== ana_20 ===")
cs_v = tot.get('cs', 0)
print(f"cs archive: {int(cs_v):,} = {cs_v/grand*100:.1f}% of all submissions")
print(f"cs vs #2 ({tot.index[1]}): {cs_v/tot.iloc[1]:.2f}x larger")

# --- ana_21: 2025-10 truncation anomaly (per-category/archive files) ---
print("=== ana_21 ===")
sep = arch_full[arch_full['month']=='2025-09-01'].set_index('archive')['count']
oct = arch_full[arch_full['month']=='2025-10-01'].set_index('archive')['count']
comp = pd.DataFrame({'2025-09':sep,'2025-10':oct}).fillna(0)
comp['drop_pct'] = (1 - comp['2025-10']/comp['2025-09'])*100
print("Per-archive Sep vs Oct 2025 (showing the truncation):")
print(comp.sort_values('2025-09', ascending=False).head(8).to_string())
print(f"Total 2025-09 = {int(sep.sum())}, total 2025-10 = {int(oct.sum())} ({(1-oct.sum()/sep.sum())*100:.0f}% lower)")
print("=> 2025-10 is a PARTIAL/INCOMPLETE month in per-category & per-archive files; exclude from trends.")

# --- ana_22: Late-tail CS plateau / AI-slop-era check (cs archive monthly) ---
print("=== ana_22 ===")
csm = arch[arch['archive']=='cs'].sort_values('dt')[['month','count']]
print("cs archive monthly, 2025 (full months only):")
for _, r in csm[csm['month']>='2025-01-01'].iterrows():
    print(f"  {r['month'][:7]}: {int(r['count'])}")
# YoY for recent months to see if CS still accelerating
cs2024 = arch[(arch['archive']=='cs')&(arch['dt']>='2024-01-01')&(arch['dt']<'2024-10-01')]['count'].sum()
cs2025 = arch[(arch['archive']=='cs')&(arch['dt']>='2025-01-01')&(arch['dt']<'2025-10-01')]['count'].sum()
print(f"cs Jan-Sep 2024 = {int(cs2024):,}; Jan-Sep 2025 = {int(cs2025):,}; YoY {(cs2025/cs2024-1)*100:+.1f}%")

# --- ana_23: stat.ML / cs cross-listing scale; eess.SY==cs.SY duplication ---
print("=== ana_23 ===")
cat = pd.read_csv(f"{DATA}/submissions_by_category.csv")
cat = cat[pd.to_datetime(cat['month'])<'2025-10-01']
ct = cat.groupby('category')['count'].sum()
# Known mirror pairs (cross-listed identical archives)
for a,b in [('cs.IT','math.IT'),('cs.SY','eess.SY'),('q-fin.EC','econ.GN'),('stat.ML','cs.LG')]:
    print(f"  {a}={int(ct.get(a,0)):,}  vs  {b}={int(ct.get(b,0)):,}")
print("Note: cs.IT/math.IT and cs.SY/eess.SY are mirrored cross-listings (near-identical counts).")
