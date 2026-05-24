"""
station_rankings.py — Per-station rankings and aggregate breakdowns of women's airplay
versus back-to-back rates, gender split, and the men's mirror.
"""
import pandas as pd
import numpy as np
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"
summary = pd.read_csv(os.path.join(DATA_DIR, "output", "summary.csv"))

# --- ana_01: Aggregate gender split across all 29 stations ---
print("=== ana_01 ===")
total = summary["total_COUNT"].sum()
women = summary["onlyWomenSongs_COUNT"].sum()
men = summary["onlyMenSongs_COUNT"].sum()
mixed = summary["onlyMixedGenderSongs_COUNT"].sum()
b2b_women = summary["b2bWomenSongs_COUNT"].sum()
b2b_men = summary["b2bMenSongs_COUNT"].sum()
b2b_mixed = summary["b2bMixedGenderSongs_COUNT"].sum()
print(f"Total plays across 29 stations (2022 sample): {total:,}")
print(f"Plays by women only:   {women:,} ({women/total*100:.2f}%)")
print(f"Plays by men only:     {men:,} ({men/total*100:.2f}%)")
print(f"Plays mixed-gender:    {mixed:,} ({mixed/total*100:.2f}%)")
print(f"Back-to-back women:    {b2b_women:,} ({b2b_women/total*100:.2f}% of all plays)")
print(f"Back-to-back men:      {b2b_men:,} ({b2b_men/total*100:.2f}% of all plays)")
print(f"Back-to-back mixed:    {b2b_mixed:,} ({b2b_mixed/total*100:.2f}% of all plays)")

# Ratios
print(f"\nMen's b2b rate is {b2b_men/b2b_women:.0f}x women's b2b rate")
print(f"Men's airplay share is {men/women:.1f}x women's airplay share")
# line ~30

# --- ana_02: Per-station ranking by women's back-to-back share ---
print("\n=== ana_02 ===")
station_rank = summary[[
    "cityName", "stationName", "ownerName",
    "total_COUNT",
    "onlyWomenSongs_COUNT", "onlyWomenSongs_PERCENT",
    "b2bWomenSongs_COUNT",  "b2bWomenSongs_PERCENT",
    "onlyMenSongs_PERCENT", "b2bMenSongs_PERCENT",
]].copy()
station_rank = station_rank.sort_values("b2bWomenSongs_PERCENT").reset_index(drop=True)
print("All 29 stations sorted by women's back-to-back rate (lowest first):")
print(station_rank.to_string(index=False))
# line ~50

# --- ana_03: Distribution of women's b2b rate across stations ---
print("\n=== ana_03 ===")
b2b_w = summary["b2bWomenSongs_PERCENT"]
print(f"Women's b2b rate distribution across 29 stations:")
print(f"  min:    {b2b_w.min():.3f}% ({summary.loc[b2b_w.idxmin(),'cityName']} {summary.loc[b2b_w.idxmin(),'stationName']})")
print(f"  median: {b2b_w.median():.3f}%")
print(f"  mean:   {b2b_w.mean():.3f}%")
print(f"  max:    {b2b_w.max():.3f}% ({summary.loc[b2b_w.idxmax(),'cityName']} {summary.loc[b2b_w.idxmax(),'stationName']})")
print(f"  Stations with b2b rate < 0.5%: {(b2b_w < 0.5).sum()} of 29")
print(f"  Stations with b2b rate < 0.1%: {(b2b_w < 0.1).sum()} of 29")
print(f"  Stations with ZERO women b2b: {(summary['b2bWomenSongs_COUNT']==0).sum()} of 29")
# line ~70

# --- ana_04: Men's vs women's b2b — the asymmetry ---
print("\n=== ana_04 ===")
mw = summary[["stationName", "cityName",
              "b2bMenSongs_PERCENT", "b2bWomenSongs_PERCENT"]].copy()
mw["men_to_women_ratio"] = mw["b2bMenSongs_PERCENT"] / mw["b2bWomenSongs_PERCENT"].replace(0, np.nan)
print(f"Median men's b2b rate: {mw['b2bMenSongs_PERCENT'].median():.2f}%")
print(f"Mean men's b2b rate:   {mw['b2bMenSongs_PERCENT'].mean():.2f}%")
print(f"Median ratio (men_b2b / women_b2b) per station: {mw['men_to_women_ratio'].median():.0f}x")
print(f"Largest single ratio: {mw['men_to_women_ratio'].max():.0f}x ({mw.loc[mw['men_to_women_ratio'].idxmax(),'stationName']})")
# line ~85
