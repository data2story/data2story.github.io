"""WR-progression deep-dive on Hollow Knight: Silksong — the megalaunch case study.

Markers: ana_21 (any% WR progression), ana_22 (run-count by week post-launch),
ana_23 (top Silksong runners), ana_24 (mean time bucketed by week — community improvement curve).
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
cats = pd.read_csv(DATA / "categories.csv")
pname = dict(zip(players["player_id"], players["name"]))
pcountry = dict(zip(players["player_id"], players["country"]))

silksong_id = games[games["name"] == "Hollow Knight: Silksong"]["game_id"].iloc[0]
print(f"Silksong game_id: {silksong_id}")
silk = runs[runs["game_id"] == silksong_id].copy()
silk["date_verified"] = pd.to_datetime(silk["date_verified"], errors="coerce", utc=True)
print(f"Silksong runs: {len(silk)}; distinct runners: {silk['player_id'].nunique()}")
print(f"Categories:")
print(cats[cats["game_id"] == silksong_id][["category_id", "name", "type"]].to_string(index=False))

# Pick the Any% category (longest list)
silk_cat = silk.groupby("category_id").size().sort_values(ascending=False)
print("\nRuns per category:")
for cid, n in silk_cat.items():
    cname = cats[cats["category_id"] == cid]["name"].iloc[0] if (cats["category_id"] == cid).any() else "?"
    print(f"  {n:>4}  {cid}  {cname}")

# Take the largest category — likely Any%
any_cid = silk_cat.index[0]
any_name = cats[cats["category_id"] == any_cid]["name"].iloc[0]
print(f"\n=== Using leading category for WR-progression: {any_name} (id {any_cid}) ===")

any_cat = silk[silk["category_id"] == any_cid].copy()
any_cat = any_cat.dropna(subset=["time_seconds", "date_verified"]).sort_values("date_verified")

# --- ana_21: WR-progression — for each new run, what was the running minimum time? ---
print("=== ana_21 ===")
any_cat["wr_time"] = any_cat["time_seconds"].cummin()
wr_changes = any_cat[any_cat["time_seconds"] == any_cat["wr_time"]].copy()
wr_changes["wr_time_min"] = wr_changes["time_seconds"] / 60
print(f"WR-improving submissions: {len(wr_changes)}")
print(f"{'date':12s}  {'time(sec)':>10}  {'time(min)':>10}  runner")
for _, r in wr_changes.iterrows():
    nm = pname.get(r["player_id"], r["player_id"]) if pd.notna(r["player_id"]) else f"guest:{r['guest_name']}"
    co = pcountry.get(r["player_id"], "?") if pd.notna(r["player_id"]) else ""
    print(f"  {str(r['date_verified'])[:10]:12s}  {r['time_seconds']:>10.0f}  {r['wr_time_min']:>10.2f}  {nm} ({co})")

# --- ana_22: runs per week in the leading category from launch to now ---
print("=== ana_22 ===")
any_cat["week"] = any_cat["date_verified"].dt.to_period("W").dt.start_time
weekly = any_cat.groupby("week").size()
print("Runs per week (any-% category):")
for w, n in weekly.items():
    print(f"  {w.date()}: {n}")

# --- ana_23: top Silksong runners by run count ---
print("=== ana_23 ===")
silk_top = silk.dropna(subset=["player_id"]).groupby("player_id").size().sort_values(ascending=False).head(15)
for pid, n in silk_top.items():
    nm = pname.get(pid, pid); co = pcountry.get(pid, "?")
    best = silk[silk["player_id"] == pid]["time_seconds"].min()
    best_str = f"{best:.0f}s ({best/60:.1f}m)" if pd.notna(best) else "?"
    print(f"  {n:>3} runs  best={best_str}  {nm} ({co})")

# --- ana_24: median run time per week — does the community as a whole get faster? ---
print("=== ana_24 ===")
weekly_med = any_cat.groupby("week")["time_seconds"].median()
for w, t in weekly_med.items():
    print(f"  {w.date()}: median {t:.0f}s ({t/60:.1f}m)  (n={int(weekly.get(w, 0))})")
