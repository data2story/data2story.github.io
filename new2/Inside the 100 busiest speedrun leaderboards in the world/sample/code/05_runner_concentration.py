"""Runner concentration: top 1% of runners vs all runners — a Lorenz-style story.

Markers: ana_18 (most prolific runners), ana_19 (concentration / Lorenz on runs per runner), ana_20 (multi-game vs single-game runners).
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
players = pd.read_csv(DATA / "players.csv")
games = pd.read_csv(DATA / "games.csv")
name_by_id = dict(zip(games["game_id"], games["name"]))
pname = dict(zip(players["player_id"], players["name"]))
pcountry = dict(zip(players["player_id"], players["country"]))

reg = runs[runs["player_id"].notna()].copy()

# --- ana_18: top 20 most-prolific runners by run count (within top-100 cut) ---
print("=== ana_18 ===")
prolific = reg.groupby("player_id").size().sort_values(ascending=False)
print(f"total runs (registered runners only): {len(reg)}; distinct runners: {len(prolific)}")
print(f"\nTop 20 by run count:")
for pid, n in prolific.head(20).items():
    nm = pname.get(pid, pid)
    co = pcountry.get(pid, "?")
    games_played = reg[reg["player_id"] == pid]["game_id"].nunique()
    print(f"  {n:>4} runs / {games_played:>2} games  {nm}  ({co})")

# --- ana_19: Lorenz-style concentration — what fraction of runs do the top X% of runners contribute? ---
print("=== ana_19 ===")
sorted_counts = prolific.sort_values(ascending=False).values
cum = np.cumsum(sorted_counts)
total_runs = cum[-1]
n_runners = len(sorted_counts)
for pct in [1, 5, 10, 20, 50]:
    k = max(1, int(n_runners * pct / 100))
    share = 100 * cum[k - 1] / total_runs
    print(f"  top {pct:>2}% of runners ({k:>5}) account for {share:5.1f}% of runs")
print(f"\nMedian runs per runner: {int(np.median(sorted_counts))}")
print(f"75th percentile:         {int(np.percentile(sorted_counts, 75))}")
print(f"95th percentile:         {int(np.percentile(sorted_counts, 95))}")
print(f"99th percentile:         {int(np.percentile(sorted_counts, 99))}")
print(f"Max single runner runs:  {int(sorted_counts[0])}")

# Save Lorenz data for the chart (every 1% bucket)
print("\nLorenz curve data (rounded to 1% buckets):")
xs = np.linspace(0, 1, 101)
ys = []
for x in xs:
    k = int(round(x * n_runners))
    if k == 0:
        ys.append(0.0)
    else:
        ys.append(100 * cum[k - 1] / total_runs)
print(f"  X (runner percentile, 0..100): generated 101 points")
print(f"  Y (cumulative run share %):    {ys[:5]} ... {ys[-5:]}")

# --- ana_20: how many distinct games per runner ---
print("=== ana_20 ===")
games_per_runner = reg.groupby("player_id")["game_id"].nunique()
print(f"Mean games per runner: {games_per_runner.mean():.2f}")
print(f"Median games per runner: {int(games_per_runner.median())}")
print(f"Runners with 1 game only:  {(games_per_runner == 1).sum()} ({100*(games_per_runner == 1).mean():4.1f}%)")
print(f"Runners with 2 games:      {(games_per_runner == 2).sum()} ({100*(games_per_runner == 2).mean():4.1f}%)")
print(f"Runners with 3-5 games:    {((games_per_runner >= 3) & (games_per_runner <= 5)).sum()} ({100*((games_per_runner >= 3) & (games_per_runner <= 5)).mean():4.1f}%)")
print(f"Runners with 6+ games:     {(games_per_runner >= 6).sum()} ({100*(games_per_runner >= 6).mean():4.1f}%)")
print(f"Max games one runner does: {int(games_per_runner.max())}")
