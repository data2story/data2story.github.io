"""Per-game leaderboard activity: who has the most runs, the most active runners, the most recent verifications.

Markers: ana_04 (top by total runs), ana_05 (top by active runners last-90d), ana_06 (top by verification activity 30d), ana_07 (category fragmentation).
"""

import argparse
from pathlib import Path

import pandas as pd

DEFAULT_DATA_DIR = r"D:\AI\journalist agent review\phase2\datasets\speedrun_top100"

ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", default=DEFAULT_DATA_DIR)
args = ap.parse_args()
DATA = Path(args.data_dir)

games = pd.read_csv(DATA / "games.csv")
categories = pd.read_csv(DATA / "categories.csv")
runs = pd.read_csv(DATA / "runs.csv", low_memory=False)

runs["date_verified"] = pd.to_datetime(runs["date_verified"], errors="coerce", utc=True)
NOW = runs["date_verified"].max()
W30 = NOW - pd.Timedelta(days=30)
W90 = NOW - pd.Timedelta(days=90)
W7 = NOW - pd.Timedelta(days=7)

name_by_id = dict(zip(games["game_id"], games["name"]))

# --- ana_04: top 25 games by total verified runs (lifetime within top-100 cut) ---
print("=== ana_04 ===")
total = runs.groupby("game_id").size().sort_values(ascending=False)
for game_id, n in total.head(25).items():
    print(f"  {n:>5}  {name_by_id.get(game_id, game_id)}")

# --- ana_05: top 25 by distinct active runners in the last 90 days ---
print("=== ana_05 ===")
recent = runs[runs["date_verified"] >= W90].copy()
recent = recent[recent["player_id"].notna()]
active = recent.groupby("game_id")["player_id"].nunique().sort_values(ascending=False)
for game_id, n in active.head(25).items():
    print(f"  {n:>4}  {name_by_id.get(game_id, game_id)}")

# --- ana_06: top 25 by verifications in the last 30 days ---
print("=== ana_06 ===")
last30 = runs[runs["date_verified"] >= W30]
v30 = last30.groupby("game_id").size().sort_values(ascending=False)
for game_id, n in v30.head(25).items():
    print(f"  {n:>4}  {name_by_id.get(game_id, game_id)}")

# --- ana_07: category fragmentation — how many distinct categories per game ---
print("=== ana_07 ===")
pergame = categories[categories["type"] == "per-game"]
catcounts = pergame.groupby("game_id").size().sort_values(ascending=False)
print(f"per-game categories: {len(pergame)} across {pergame['game_id'].nunique()} games")
print(f"mean: {catcounts.mean():.2f}, median: {catcounts.median():.0f}, max: {catcounts.max()}, min: {catcounts.min()}")
print("\nTop 10 by category count:")
for gid, n in catcounts.head(10).items():
    print(f"  {n:>3}  {name_by_id.get(gid, gid)}")
print("\nBottom 5 (single category):")
for gid, n in catcounts.tail(5).items():
    print(f"  {n:>3}  {name_by_id.get(gid, gid)}")
print(f"\nGames with exactly 1 category: {(catcounts == 1).sum()}")
print(f"Games with >= 10 categories:   {(catcounts >= 10).sum()}")

# --- ana_08: runs in last 7 days vs last 30 days vs all-time, by game (top 15) ---
print("=== ana_08 ===")
last7 = runs[runs["date_verified"] >= W7]
v7 = last7.groupby("game_id").size()
top15 = v30.head(15).index.tolist()
print(f"{'game':50s}  7d   30d   total")
for gid in top15:
    name = name_by_id.get(gid, gid)[:48]
    print(f"  {name:48s} {v7.get(gid,0):>3}  {v30.get(gid,0):>4}  {total.get(gid,0):>6}")
