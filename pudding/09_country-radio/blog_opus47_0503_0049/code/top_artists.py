"""
top_artists.py — Top artists in the 'current' bucket: which women / men dominate
contemporary country radio?  Quantifies the bottleneck for women specifically.
"""
import pandas as pd
import os, glob

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"
raw_files = sorted(glob.glob(os.path.join(DATA_DIR, "input", "*Workbook-Full2022.csv")))
raw = pd.concat([pd.read_csv(f) for f in raw_files], ignore_index=True)

# --- ana_16: Top current women — concentration in three artists ---
print("=== ana_16 ===")
women = raw[raw["gender"]=="women"]
current_women = women[women["grc"]=="C"]
total_current_women = len(current_women)
women_artist_counts = current_women.groupby("artist").size().sort_values(ascending=False)
top10_w = women_artist_counts.head(10)
top3_w = women_artist_counts.head(3)
print(f"Total current-bucket women plays in 2022 sample: {total_current_women}")
print(f"Unique women artists in current rotation: {women_artist_counts.shape[0]}")
print(f"\nTop 10 current women artists:")
for artist, count in top10_w.items():
    print(f"  {artist:30s} {count:>4}  ({count/total_current_women*100:5.1f}%)")
print(f"\nTop 3 current women artists account for {top3_w.sum()} / {total_current_women} = {top3_w.sum()/total_current_women*100:.1f}% of current women's plays")
# line ~25

# --- ana_17: Top current men — much flatter distribution ---
print("\n=== ana_17 ===")
men = raw[raw["gender"]=="men"]
current_men = men[men["grc"]=="C"]
total_current_men = len(current_men)
men_artist_counts = current_men.groupby("artist").size().sort_values(ascending=False)
top10_m = men_artist_counts.head(10)
top3_m = men_artist_counts.head(3)
print(f"Total current-bucket men plays: {total_current_men}")
print(f"Unique men artists in current rotation: {men_artist_counts.shape[0]}")
print(f"\nTop 10 current men artists:")
for artist, count in top10_m.items():
    print(f"  {artist:30s} {count:>4}  ({count/total_current_men*100:5.1f}%)")
print(f"\nTop 3 current men artists account for {top3_m.sum()} / {total_current_men} = {top3_m.sum()/total_current_men*100:.1f}% of current men's plays")
print(f"\nConcentration ratio: women's top-3 dominance is {top3_w.sum()/total_current_women / (top3_m.sum()/total_current_men):.2f}x men's")

# --- ana_18: All POC women in the 2022 dataset ---
print("\n=== ana_18 ===")
poc_women = raw[(raw["gender"]=="women") & (raw["race"]!="white")]
print(f"All POC women plays in 2022 (across 29 stations, 19 days): {len(poc_women)}")
print(f"Unique POC women artists:")
for artist, count in poc_women.groupby("artist").size().sort_values(ascending=False).items():
    print(f"  {artist:25s} {count} plays")

# What stations played them?
print(f"\nStations that played any POC woman:")
poc_w_by_station = poc_women.groupby("station").size().sort_values(ascending=False)
print(poc_w_by_station.to_string())
print(f"\nStations with ZERO POC women plays: {29 - len(poc_w_by_station)} of 29")

# --- ana_19: All artists in the dataset (overall scale) ---
print("\n=== ana_19 ===")
all_artists = raw.groupby("artist").size().sort_values(ascending=False)
print(f"Total unique artists across all 29 stations, 19 days: {len(all_artists)}")
women_artists = women.groupby("artist").size()
men_artists = men.groupby("artist").size()
print(f"Unique women artists: {len(women_artists)}")
print(f"Unique men artists:   {len(men_artists)}")
print(f"Top 20 most-played artists overall:")
for artist, count in all_artists.head(20).items():
    g = raw[raw["artist"]==artist]["gender"].iloc[0]
    r = raw[raw["artist"]==artist]["race"].iloc[0]
    print(f"  {artist:30s}  {count:>4}  gender={g}  race={r}")
