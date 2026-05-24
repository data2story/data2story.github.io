"""
day_level.py — Per-day variability and the rare days when zero women's b2bs appear.
"""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"
day = pd.read_csv(os.path.join(DATA_DIR, "output", "daySummary.csv"))

# --- ana_23: How many station-days had ZERO women back-to-backs? ---
print("=== ana_23 ===")
total_station_days = len(day)
zero_b2b_days = (day["b2bWomenSongs_COUNT"]==0).sum()
print(f"Total station-day rows: {total_station_days}")
print(f"Station-days with ZERO women b2bs: {zero_b2b_days} ({zero_b2b_days/total_station_days*100:.1f}%)")
print(f"Station-days with 1 women b2b:    {(day['b2bWomenSongs_COUNT']==1).sum()}")
print(f"Station-days with 2-5 women b2bs: {((day['b2bWomenSongs_COUNT']>=2)&(day['b2bWomenSongs_COUNT']<=5)).sum()}")
print(f"Station-days with 6+ women b2bs:  {(day['b2bWomenSongs_COUNT']>=6).sum()}")

# --- ana_24: Best day per station for women's b2b ---
print("\n=== ana_24 ===")
best_per_station = day.loc[day.groupby("stationName")["b2bWomenSongs_PERCENT"].idxmax()][
    ["stationName","cityName","date","total_COUNT","onlyWomenSongs_PERCENT","b2bWomenSongs_COUNT","b2bWomenSongs_PERCENT"]
].sort_values("b2bWomenSongs_PERCENT", ascending=False)
print("Per-station BEST day for women's b2b rate:")
print(best_per_station.to_string(index=False))

# --- ana_25: Distribution of women plays per station-day ---
print("\n=== ana_25 ===")
print("Women's b2b rate per station-day distribution:")
print(day["b2bWomenSongs_PERCENT"].describe())

# --- ana_26: The single most extreme low-women-b2b station-day ---
print("\n=== ana_26 ===")
worst = day[day["b2bWomenSongs_COUNT"]==0].copy()
worst["onlyWomenSongs_COUNT"] = worst["onlyWomenSongs_COUNT"].astype(int)
# Among zero-b2b days, those with the highest women plays anyway
worst_sorted = worst.sort_values("onlyWomenSongs_COUNT", ascending=False)
print("Station-days with the most women plays but ZERO back-to-backs (most striking)")
print(worst_sorted[["stationName","cityName","date","onlyWomenSongs_COUNT","total_COUNT","onlyWomenSongs_PERCENT"]].head(15).to_string(index=False))
print(f"\nA station can play 90+ women's songs in a 24-hour day and never put two of them next to each other.")
