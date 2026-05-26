"""Final supporting numbers needed for analyst.json chart data:
- ana_28: what game drove the 2026-03 peak month
- ana_29: precise Lorenz curve points (10 buckets) for the chart
- ana_30: monthly verifications condensed to chart-ready form (since 2020-01)
"""
import argparse
from pathlib import Path
import numpy as np
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

# --- ana_28: drivers of the 2026-03 peak month ---
print("=== ana_28 ===")
mar = runs[(runs["date_verified"] >= "2026-03-01") & (runs["date_verified"] < "2026-04-01")]
print(f"2026-03 total: {len(mar)}")
g = mar.groupby("game_id").size().sort_values(ascending=False).head(15)
for gid, n in g.items():
    print(f"  {n:>4} ({100*n/len(mar):4.1f}%)  {name_by_id.get(gid, gid)}")

# --- ana_29: Lorenz points at chart-ready percentiles ---
print("=== ana_29 ===")
reg = runs[runs["player_id"].notna()].copy()
counts = reg.groupby("player_id").size().sort_values(ascending=False).values
cum = np.cumsum(counts); total = cum[-1]; n_runners = len(counts)
buckets = [0, 1, 2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]
print(f"runner percentile -> cumulative run share")
for pct in buckets:
    k = int(round(pct/100 * n_runners))
    if k == 0:
        share = 0.0
    else:
        share = 100 * cum[k-1] / total
    print(f"  {pct:>3}%  {share:5.1f}%")

# --- ana_30: monthly verification series 2020-01 to 2026-05 (compact) ---
print("=== ana_30 ===")
df = runs.dropna(subset=["date_verified"]).copy()
df["month"] = df["date_verified"].dt.to_period("M").dt.start_time
monthly = df.groupby("month").size()
monthly = monthly[monthly.index >= "2020-01-01"]
for m, n in monthly.items():
    print(f"  {m.strftime('%Y-%m')}\t{n}")

# --- ana_31: Granny: Legacy monthly profile from leaderboard birth (2025-02) ---
print("=== ana_31 ===")
granny_id = games[games["name"] == "Granny: Legacy"]["game_id"].iloc[0]
gr = runs[runs["game_id"] == granny_id].copy()
gr["month"] = gr["date_verified"].dt.to_period("M").dt.start_time
gm = gr.groupby("month").size()
for m, n in gm.items():
    print(f"  {m.strftime('%Y-%m')}\t{n}")
