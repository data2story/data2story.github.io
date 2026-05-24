"""
owners.py — Owner-level rollup. Are some companies more skewed than others?
"""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"
summary = pd.read_csv(os.path.join(DATA_DIR, "output", "summary.csv"))

# --- ana_27: Stations and total plays per owner ---
print("=== ana_27 ===")
owner_groups = summary.groupby("ownerName").agg(
    n_stations=("stationName", "count"),
    total_plays=("total_COUNT", "sum"),
    women_plays=("onlyWomenSongs_COUNT", "sum"),
    b2b_women=("b2bWomenSongs_COUNT", "sum"),
    men_plays=("onlyMenSongs_COUNT", "sum"),
    b2b_men=("b2bMenSongs_COUNT", "sum"),
)
owner_groups["women_share_pct"] = (owner_groups["women_plays"]/owner_groups["total_plays"]*100).round(2)
owner_groups["women_b2b_pct"] = (owner_groups["b2b_women"]/owner_groups["total_plays"]*100).round(3)
owner_groups["men_b2b_pct"] = (owner_groups["b2b_men"]/owner_groups["total_plays"]*100).round(2)
owner_groups = owner_groups.sort_values("women_b2b_pct")
print("Per-owner aggregates:")
print(owner_groups.to_string())
