"""Stage 1: Dataset profile - shape, time range, scope of every relevant CSV."""
import pandas as pd
import os

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/06_football-managers/output_files"

files = [
    "manager_table_df.csv",
    "manager_ratings_df.csv",
    "manager_all_tenures_performance_df.csv",
    "manager_sequence_overperformance_df.csv",
    "team_season_performance_df.csv",
    "player_ratings_df.csv",
    "expected_points_df.csv",
]

# --- ana_00: file inventory ---
print("=== ana_00 ===")
for f in files:
    path = os.path.join(DATA, f)
    df = pd.read_csv(path, low_memory=False, encoding='latin-1')
    size_mb = os.path.getsize(path) / 1e6
    print(f"{f}: {df.shape[0]} rows x {df.shape[1]} cols  ({size_mb:.2f} MB)")

# --- ana_01: time range & league scope ---
print("\n=== ana_01 ===")
df = pd.read_csv(os.path.join(DATA, "expected_points_df.csv"), low_memory=False, encoding='latin-1')
print("Seasons:", sorted(df['season'].dropna().unique()))
print("Leagues:", sorted(df['league_country'].dropna().unique()))
print(f"Total fixtures: {len(df):,}")
print(f"Date min/max: {df['date'].min()} / {df['date'].max()}")
