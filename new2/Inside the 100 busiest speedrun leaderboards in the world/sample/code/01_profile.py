"""Dataset profile: shapes, time range, missing rates, basic stats.

Run from the dataset directory or with --data-dir.
Markers: ana_01 (sizes), ana_02 (time range), ana_03 (missing rates).
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
players = pd.read_csv(DATA / "players.csv")

# --- ana_01: dataset shape ---
print("=== ana_01 ===")
print(f"games:      rows={len(games):>6} cols={games.shape[1]}")
print(f"categories: rows={len(categories):>6} cols={categories.shape[1]}")
print(f"runs:       rows={len(runs):>6} cols={runs.shape[1]}")
print(f"players:    rows={len(players):>6} cols={players.shape[1]}")
n_pergame_cats = (categories["type"] == "per-game").sum()
print(f"per-game categories: {n_pergame_cats}")
print(f"per-game categories per game (mean): {n_pergame_cats / len(games):.2f}")

# --- ana_02: time range of verifications ---
print("=== ana_02 ===")
verified = pd.to_datetime(runs["date_verified"], errors="coerce", utc=True)
print(f"date_verified min: {verified.min()}")
print(f"date_verified max: {verified.max()}")
print(f"date_verified missing: {verified.isna().sum()} of {len(runs)}")
print(f"runs verified in last 30 days of dataset: {(verified >= verified.max() - pd.Timedelta(days=30)).sum()}")
print(f"runs verified in last 7 days of dataset:  {(verified >= verified.max() - pd.Timedelta(days=7)).sum()}")

# --- ana_03: missing-value rates (runs) ---
print("=== ana_03 ===")
miss = runs.isna().sum().sort_values(ascending=False)
total = len(runs)
print("column missingness (runs):")
for col, n in miss.items():
    if n > 0:
        print(f"  {col:25s} {n:>6} ({100*n/total:5.1f}%)")
print(f"\nrows with a usable player_id (registered): {runs['player_id'].notna().sum()} ({100*runs['player_id'].notna().mean():.1f}%)")
print(f"rows with guest_name (anonymous): {runs['guest_name'].notna().sum()} ({100*runs['guest_name'].notna().mean():.1f}%)")
print(f"rows with video_url: {runs['video_url'].notna().sum()} ({100*runs['video_url'].notna().mean():.1f}%)")
print(f"rows with player_country: {runs['player_country'].notna().sum()} ({100*runs['player_country'].notna().mean():.1f}%)")
