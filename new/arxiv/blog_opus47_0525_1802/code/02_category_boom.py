#!/usr/bin/env python3
"""Per-category + per-group analysis 2022-2025: the AI/CS boom, rankings,
growth, concentration, composition. Run from DATA_DIR.
CAVEAT: per-category file truncates at 2025-10 (partial month) -> EXCLUDE 2025-10
from all growth/trend/ranking claims. Use 2025-09 as last complete month."""
import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2story-skill/data/arxiv"
cat = pd.read_csv(f"{DATA}/submissions_by_category.csv")
cat['dt'] = pd.to_datetime(cat['month'])
# EXCLUDE partial 2025-10
cat = cat[cat['dt'] < '2025-10-01'].copy()
cat['year'] = cat['dt'].dt.year
cat['group_clean'] = cat['group'].str.replace('grp_', '', regex=False)

LAST_FULL = '2025-09'  # last complete month

# --- ana_10: Top categories by total submissions (2022-01..2025-09) ---
print("=== ana_10 ===")
tot = cat.groupby('category')['count'].sum().sort_values(ascending=False)
grand = tot.sum()
print(f"Grand total submissions (155 cats, 2022-01..2025-09): {int(grand):,}")
print("Top 20 categories by cumulative submissions:")
for c, v in tot.head(20).items():
    print(f"  {c}: {int(v):,} ({v/grand*100:.1f}%)")
print("Bottom 10 categories:")
for c, v in tot.tail(10).items():
    print(f"  {c}: {int(v):,}")

# --- ana_11: Concentration - top 10 share ---
print("=== ana_11 ===")
top10share = tot.head(10).sum()/grand*100
top4share = tot.head(4).sum()/grand*100
print(f"Top 10 of 155 categories account for {top10share:.1f}% of all submissions")
print(f"Top 4 (cs.LG/CV/CL/AI?) account for {top4share:.1f}%")
cumshare = (tot.cumsum()/grand*100)
for k in [1,3,5,10,20,50]:
    print(f"  top {k}: {cumshare.iloc[k-1]:.1f}% cumulative")
print(f"Top 4 categories: {list(tot.head(4).index)}")

# --- ana_12: The big-4 CS/AI categories growth 2022 vs 2025 ---
print("=== ana_12 ===")
def monthly(c):
    return cat[cat['category']==c].set_index('month')['count']
ai_cats = ['cs.LG','cs.CV','cs.CL','cs.AI']
print("Big-4 AI categories: first full-year (2022) vs 12mo ending 2025-09")
# annualized: sum of 12 months 2022-01..2022-12 vs 2024-10..2025-09
for c in ai_cats:
    m = monthly(c)
    y2022 = cat[(cat['category']==c)&(cat['dt']>='2022-01-01')&(cat['dt']<'2023-01-01')]['count'].sum()
    last12 = cat[(cat['category']==c)&(cat['dt']>='2024-10-01')&(cat['dt']<'2025-10-01')]['count'].sum()
    jan22 = m.get('2022-01-01', np.nan)
    sep25 = m.get('2025-09-01', np.nan)
    print(f"  {c}: 2022 annual={int(y2022):,}, last-12mo={int(last12):,}, growth x{last12/y2022:.2f}; "
          f"Jan2022={int(jan22)} -> Sep2025={int(sep25)} (x{sep25/jan22:.2f})")

# --- ana_13: Ranking of single biggest months for AI cats ---
print("=== ana_13 ===")
oct24 = cat[cat['month']=='2024-10-01'].groupby('category')['count'].sum().sort_values(ascending=False)
print("Top categories in Oct 2024 (benchmark month from det_05):")
for c, v in oct24.head(6).items():
    print(f"  {c}: {int(v)}")
print(f"cs.LG+cs.CV+cs.CL Oct 2024 sum: {int(oct24[['cs.LG','cs.CV','cs.CL']].sum())}")
# peak month per big-4
print("Peak single month per big-4 (excl 2025-10):")
for c in ai_cats:
    m = cat[cat['category']==c]
    pk = m.loc[m['count'].idxmax()]
    print(f"  {c}: {pk['month']} = {int(pk['count'])}")

# --- ana_14: Fastest-growing categories (2022 vs 2025, min volume) ---
print("=== ana_14 ===")
# compare annualized first 12mo vs last 12mo, require >=500 in first window
first12 = cat[(cat['dt']>='2022-01-01')&(cat['dt']<'2023-01-01')].groupby('category')['count'].sum()
last12 = cat[(cat['dt']>='2024-10-01')&(cat['dt']<'2025-10-01')].groupby('category')['count'].sum()
growth = pd.DataFrame({'first12':first12,'last12':last12}).fillna(0)
growth = growth[growth['first12']>=300]  # filter tiny
growth['ratio'] = growth['last12']/growth['first12']
growth['pct'] = (growth['ratio']-1)*100
print("Fastest-growing categories (first-12mo>=300), top 15 by ratio:")
for c, r in growth.sort_values('ratio', ascending=False).head(15).iterrows():
    print(f"  {c}: {int(r['first12'])} -> {int(r['last12'])} (x{r['ratio']:.2f}, {r['pct']:+.0f}%)")
print("Flattest / declining categories (bottom 12 by ratio):")
for c, r in growth.sort_values('ratio').head(12).iterrows():
    print(f"  {c}: {int(r['first12'])} -> {int(r['last12'])} (x{r['ratio']:.2f}, {r['pct']:+.0f}%)")

# --- ana_15: Group-level composition over time ---
print("=== ana_15 ===")
grp_yr = cat.groupby(['group_clean','year'])['count'].sum().unstack(fill_value=0)
print("Group annual totals (2025 excludes Oct):")
print(grp_yr.to_string())
# group share in 2022 vs 2025 (annualized: use first 12mo vs last 12mo)
g_first = cat[(cat['dt']>='2022-01-01')&(cat['dt']<'2023-01-01')].groupby('group_clean')['count'].sum()
g_last = cat[(cat['dt']>='2024-10-01')&(cat['dt']<'2025-10-01')].groupby('group_clean')['count'].sum()
print("\nGroup share-of-total: first 12mo (2022) vs last 12mo (2024-10..2025-09):")
gf_sh = g_first/g_first.sum()*100
gl_sh = g_last/g_last.sum()*100
for g in g_first.sort_values(ascending=False).index:
    print(f"  {g}: {gf_sh[g]:.1f}% -> {gl_sh[g]:.1f}% ({gl_sh[g]-gf_sh[g]:+.1f}pp); vol {int(g_first[g])} -> {int(g_last[g])} (x{g_last[g]/g_first[g]:.2f})")

# --- ana_16: CS share-of-total trajectory (monthly) ---
print("=== ana_16 ===")
mon_grp = cat.groupby(['month','group_clean'])['count'].sum().unstack(fill_value=0)
mon_tot = mon_grp.sum(axis=1)
cs_share = mon_grp['cs']/mon_tot*100
print("CS share of monthly submissions (quarterly samples):")
for m in ['2022-01-01','2022-07-01','2023-01-01','2023-07-01','2024-01-01','2024-07-01','2025-01-01','2025-09-01']:
    if m in cs_share.index:
        print(f"  {m[:7]}: {cs_share[m]:.1f}%")
print(f"CS share min={cs_share.min():.1f}% max={cs_share.max():.1f}%")

# --- ana_17: cs.LG dethrones older leaders (is CS #1 every category?) ---
print("=== ana_17 ===")
# rank of categories within full window vs share of physics-era leaders
print("Top category each group (cumulative):")
for g in sorted(cat['group_clean'].unique()):
    sub = cat[cat['group_clean']==g].groupby('category')['count'].sum().sort_values(ascending=False)
    print(f"  {g}: #1 {sub.index[0]} ({int(sub.iloc[0]):,})")
