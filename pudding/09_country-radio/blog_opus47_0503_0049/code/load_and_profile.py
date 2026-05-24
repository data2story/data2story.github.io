"""
load_and_profile.py — Stage 0 of analysis: load raw + summary data and produce a dataset profile.

Inputs:
  - DATA_DIR/output/summary.csv         (one row per station)
  - DATA_DIR/output/daySummary.csv      (one row per station per sampled date)
  - DATA_DIR/input/{city}_{station}-FM-Workbook-Full2022.csv  (one row per song play)
  - DATA_DIR/analysis/pvals.csv         (per-station permutation p-values from The Pudding's R simulation)
"""
import pandas as pd
import os
import glob

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"

# --- ana_00: Dataset profile ---
print("=== ana_00 ===")
summary = pd.read_csv(os.path.join(DATA_DIR, "output", "summary.csv"))
day_summary = pd.read_csv(os.path.join(DATA_DIR, "output", "daySummary.csv"))
pvals = pd.read_csv(os.path.join(DATA_DIR, "analysis", "pvals.csv"))

raw_files = sorted(glob.glob(os.path.join(DATA_DIR, "input", "*Workbook-Full2022.csv")))

print(f"Stations in summary.csv: {len(summary)}")
print(f"Day-station rows in daySummary.csv: {len(day_summary)}")
print(f"Stations with permutation p-values: {len(pvals)}")
print(f"Raw per-station song-log files: {len(raw_files)}")
print(f"Summary columns: {len(summary.columns)}")
print(f"Cities sampled: {summary['cityName'].nunique()}")
print(f"Owners sampled: {summary['ownerName'].nunique()}")

# Total songs across all stations in 2022 sample
total_songs = int(summary["total_COUNT"].sum())
print(f"Total songs across the 29-station 2022 sample: {total_songs:,}")

# Total dates per station (from daySummary)
dates_per_station = day_summary.groupby("stationName").size()
print(f"Dates sampled per station: min={dates_per_station.min()}, max={dates_per_station.max()}, median={int(dates_per_station.median())}")
print(f"Unique dates in dataset: {day_summary['date'].nunique()}")

# A quick scan of a single raw file to verify schema
sample_raw = pd.read_csv(raw_files[0])
print("\nSample raw schema (Austin KASE-FM):")
print(f"  rows: {len(sample_raw)}")
print(f"  columns: {list(sample_raw.columns)}")
print(f"  date range: {sample_raw['date'].min()} to {sample_raw['date'].max()}")
print(f"  unique artists: {sample_raw['artist'].nunique()}")

# Save tidy summary for downstream scripts
summary.to_csv("/tmp/_summary.csv", index=False)
day_summary.to_csv("/tmp/_daySummary.csv", index=False)
pvals.to_csv("/tmp/_pvals.csv", index=False)
