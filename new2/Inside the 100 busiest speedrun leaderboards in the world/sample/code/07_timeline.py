"""Verification activity over time — across all top-100 leaderboards.

Markers: ana_25 (monthly verification volume since 2020), ana_26 (the 'last week' breakdown by game).
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
games = pd.read_csv(DATA / "games.csv")
name_by_id = dict(zip(games["game_id"], games["name"]))
runs["date_verified"] = pd.to_datetime(runs["date_verified"], errors="coerce", utc=True)

# --- ana_25: monthly verification volume 2020-01 onward ---
print("=== ana_25 ===")
df = runs.dropna(subset=["date_verified"]).copy()
df["month"] = df["date_verified"].dt.to_period("M").dt.start_time
monthly = df.groupby("month").size()
monthly_recent = monthly[monthly.index >= "2020-01-01"]
print(f"Monthly verifications since 2020-01:")
for m, n in monthly_recent.items():
    print(f"  {m.date()}: {n}")

# --- ana_26: which games drove the last 30 days vs last 365 days ---
print("=== ana_26 ===")
NOW = df["date_verified"].max()
M1 = NOW - pd.Timedelta(days=30)
Y1 = NOW - pd.Timedelta(days=365)
last30 = df[df["date_verified"] >= M1]
last365 = df[df["date_verified"] >= Y1]
g30 = last30.groupby("game_id").size().sort_values(ascending=False).head(15)
g365 = last365.groupby("game_id").size().sort_values(ascending=False).head(15)
print(f"\nTop 15 by runs in last 30 days (total: {len(last30)}):")
for gid, n in g30.items():
    print(f"  {n:>4}  {name_by_id.get(gid, gid)}")
print(f"\nTop 15 by runs in last 365 days (total: {len(last365)}):")
for gid, n in g365.items():
    print(f"  {n:>4}  {name_by_id.get(gid, gid)}")

# --- ana_27: 'birth date' of each leaderboard — date_verified of the very first verified run per game ---
print("=== ana_27 ===")
first = df.groupby("game_id")["date_verified"].min().sort_values(ascending=False).head(20)
print("Newest leaderboards (first verified run within our top-100 cut):")
for gid, d in first.items():
    print(f"  {str(d)[:10]}  {name_by_id.get(gid, gid)}")
print("\nOldest in the top-100 cut:")
oldest = df.groupby("game_id")["date_verified"].min().sort_values(ascending=True).head(10)
for gid, d in oldest.items():
    print(f"  {str(d)[:10]}  {name_by_id.get(gid, gid)}")
