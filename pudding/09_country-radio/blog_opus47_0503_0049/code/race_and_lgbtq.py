"""
race_and_lgbtq.py — Race and LGBTQ+ representation in 2022 country radio sample.
"""
import pandas as pd
import os
import glob

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"
summary = pd.read_csv(os.path.join(DATA_DIR, "output", "summary.csv"))

# --- ana_11: Race breakdown of plays ---
print("=== ana_11 ===")
total = summary["total_COUNT"].sum()
white_men = summary["onlyWhiteMenSongs_COUNT"].sum()
white_women = summary["onlyWhiteWomenSongs_COUNT"].sum()
white_mixed = summary["onlyWhiteMixedGenderSongs_COUNT"].sum()
poc_men = summary["onlyPOCMenSongs_COUNT"].sum()
poc_women = summary["onlyPOCWomenSongs_COUNT"].sum()
poc_mixed = summary["onlyPOCMixedSongs_COUNT"].sum()
nonwhite = poc_men + poc_women + poc_mixed
nonwhite_women = poc_women

print(f"Total plays (29 stations, 19 days, 2022): {total:,}")
print(f"  White men:           {white_men:,}  ({white_men/total*100:.2f}%)")
print(f"  White women:         {white_women:,}  ({white_women/total*100:.2f}%)")
print(f"  White mixed-gender:  {white_mixed:,}  ({white_mixed/total*100:.2f}%)")
print(f"  POC men:             {poc_men:,}  ({poc_men/total*100:.2f}%)")
print(f"  POC women:           {poc_women:,}  ({poc_women/total*100:.4f}%)")
print(f"  POC mixed-gender:    {poc_mixed:,}  ({poc_mixed/total*100:.2f}%)")
print(f"  Non-white (overall): {nonwhite:,}  ({nonwhite/total*100:.2f}%)")
print(f"  Non-white women:     {nonwhite_women:,}  ({nonwhite_women/total*100:.4f}%)")

# --- ana_12: Back-to-backs by race ---
print("\n=== ana_12 ===")
b2b_white_men = summary["b2bWhiteMenSongs_COUNT"].sum()
b2b_white_women = summary["b2bWhiteWomenSongs_COUNT"].sum()
b2b_poc_men = summary["b2bPOCMenSongs_COUNT"].sum()
b2b_poc_women = summary["b2bPOCWomenSongs_COUNT"].sum()
b2b_nonwhite = b2b_poc_men + b2b_poc_women + summary["b2bPOCMixedSongs_COUNT"].sum()
b2b_nonwhite_women = b2b_poc_women
print(f"Back-to-back white men:    {b2b_white_men:,}  ({b2b_white_men/total*100:.2f}% of all plays)")
print(f"Back-to-back white women:  {b2b_white_women}  ({b2b_white_women/total*100:.4f}% of all plays)")
print(f"Back-to-back POC men:      {b2b_poc_men}  ({b2b_poc_men/total*100:.4f}% of all plays)")
print(f"Back-to-back POC women:    {b2b_poc_women}  ({b2b_poc_women/total*100:.4f}% of all plays)")
print(f"Back-to-back non-white women anywhere: {b2b_nonwhite_women} (across all 29 stations, 19 days)")

# --- ana_13: LGBTQ representation ---
print("\n=== ana_13 ===")
lgbtq = summary["onlyLGBTQSongs_COUNT"].sum()
straight = summary["onlyStraightSongs_COUNT"].sum()
b2b_lgbtq = summary["b2bLGBTQSongs_COUNT"].sum()
print(f"LGBTQ+ plays: {lgbtq}  ({lgbtq/total*100:.3f}% of all plays)")
print(f"Straight plays: {straight:,}  ({straight/total*100:.2f}%)")
print(f"LGBTQ+ back-to-back plays: {b2b_lgbtq}  (across 29 stations, 19 days, {total:,} songs)")
print(f"Stations with ANY LGBTQ+ play: {(summary['onlyLGBTQSongs_COUNT']>0).sum()} of 29")
print(f"Stations with LGBTQ+ b2b play: {(summary['b2bLGBTQSongs_COUNT']>0).sum()} of 29")

# --- ana_14: Per-station POC women plays ---
print("\n=== ana_14 ===")
poc_w_per_station = summary[["cityName","stationName","total_COUNT","onlyPOCWomenSongs_COUNT","b2bPOCWomenSongs_COUNT"]].copy()
poc_w_per_station = poc_w_per_station.sort_values("onlyPOCWomenSongs_COUNT")
print("Per-station POC women plays (29 stations, 19 days each):")
print(poc_w_per_station.to_string(index=False))

# --- ana_15: Identify the actual artists of color in the raw data ---
print("\n=== ana_15 ===")
raw_files = sorted(glob.glob(os.path.join(DATA_DIR, "input", "*Workbook-Full2022.csv")))
all_rows = []
for f in raw_files:
    df = pd.read_csv(f)
    all_rows.append(df)
raw = pd.concat(all_rows, ignore_index=True)
print(f"Total song-play rows aggregated: {len(raw):,}")

# Filter to non-white women
poc_women_rows = raw[(raw["gender"]=="women") & (raw["race"]!="white")]
print(f"\nPOC women song-play rows: {len(poc_women_rows)}")
print(f"Unique POC women artists in 2022 country-radio dataset:")
print(poc_women_rows.groupby("artist").size().sort_values(ascending=False))

# LGBTQ artists
print(f"\nUnique values in 'genre' column (which encodes orientation in The Pudding's coding):")
print(raw["genre"].value_counts())
