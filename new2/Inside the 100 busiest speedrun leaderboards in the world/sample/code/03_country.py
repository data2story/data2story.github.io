"""Country distributions: runners by country, runs by country, where the world records live.

Markers: ana_09 (top countries by runners), ana_10 (top countries by runs), ana_11 (where WRs live).
"""

import argparse
from pathlib import Path
import pandas as pd

DEFAULT_DATA_DIR = r"D:\AI\journalist agent review\phase2\datasets\speedrun_top100"
ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", default=DEFAULT_DATA_DIR)
args = ap.parse_args()
DATA = Path(args.data_dir)

runs = pd.read_csv(DATA / "runs.csv", low_memory=False)
players = pd.read_csv(DATA / "players.csv")
games = pd.read_csv(DATA / "games.csv")
name_by_id = dict(zip(games["game_id"], games["name"]))

# --- ana_09: top countries by distinct registered runners on these leaderboards ---
print("=== ana_09 ===")
reg = runs[runs["player_id"].notna() & runs["player_country"].notna()].copy()
runners_by_country = reg.groupby("player_country")["player_id"].nunique().sort_values(ascending=False)
total_reg_runners = reg["player_id"].nunique()
print(f"distinct registered runners with a country: {total_reg_runners}")
for c, n in runners_by_country.head(20).items():
    print(f"  {n:>5} ({100*n/total_reg_runners:4.1f}%)  {c}")
print(f"... and {(runners_by_country < runners_by_country.head(20).min()).sum()} other countries")

# --- ana_10: top countries by run volume ---
print("=== ana_10 ===")
runs_by_country = runs.groupby("player_country").size().sort_values(ascending=False)
total_runs_with_c = runs_by_country.sum()
print(f"runs with a country: {total_runs_with_c}")
for c, n in runs_by_country.head(20).items():
    print(f"  {n:>5} ({100*n/total_runs_with_c:4.1f}%)  {c}")

# --- ana_11: where the world records live — country of the place=1 runner per category ---
print("=== ana_11 ===")
wrs = runs[runs["place"] == 1].copy()
print(f"total leaderboard rank-1 rows: {len(wrs)}  (one per category; ties share place=1)")
wr_by_country = wrs.groupby("player_country").size().sort_values(ascending=False)
total_wr_country = wr_by_country.sum()
print(f"rank-1 rows with a known country: {total_wr_country}")
for c, n in wr_by_country.head(15).items():
    print(f"  {n:>4} ({100*n/total_wr_country:4.1f}%)  {c}")

# --- ana_12: country breakdown for the Silksong leaderboards (the megalaunch) ---
print("=== ana_12 ===")
silksong_id = "1jp7p6lp"  # actual Silksong ID we'll lookup
silksong_id_lookup = games[games["name"] == "Hollow Knight: Silksong"]["game_id"].iloc[0]
silksong = runs[runs["game_id"] == silksong_id_lookup].copy()
print(f"Silksong runs: {len(silksong)}; distinct runners: {silksong['player_id'].nunique()}")
silk_country = silksong[silksong["player_country"].notna()].groupby("player_country")["player_id"].nunique().sort_values(ascending=False)
for c, n in silk_country.head(15).items():
    print(f"  {n:>4}  {c}")
print(f"\nSilksong game_id: {silksong_id_lookup}")

# --- ana_13: country breakdown for Granny: Legacy (the grinder dynasty) ---
print("=== ana_13 ===")
granny_id = games[games["name"] == "Granny: Legacy"]["game_id"].iloc[0]
granny = runs[runs["game_id"] == granny_id].copy()
print(f"Granny: Legacy runs: {len(granny)}; distinct runners: {granny['player_id'].nunique()}")
gc = granny[granny["player_country"].notna()].groupby("player_country")["player_id"].nunique().sort_values(ascending=False)
for c, n in gc.head(10).items():
    print(f"  {n:>3}  {c}")
print(f"\nGranny: Legacy game_id: {granny_id}")
