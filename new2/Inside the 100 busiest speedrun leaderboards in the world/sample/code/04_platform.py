"""Platform mix and emulator share across the top-100.

Markers: ana_14 (overall platform share), ana_15 (emulator share trend over time), ana_16 (per-game platform dominance).
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

# --- ana_14: overall platform share across all 61,797 runs ---
print("=== ana_14 ===")
plat = runs["platform_name"].fillna("(unknown)").value_counts()
total = len(runs)
print(f"distinct platforms: {plat.size}")
for p, n in plat.items():
    print(f"  {n:>5} ({100*n/total:4.1f}%)  {p}")

# --- ana_15: emulator share by year ---
print("=== ana_15 ===")
runs["year"] = runs["date_verified"].dt.year
emu_year = runs.dropna(subset=["year"]).groupby("year").agg(
    total=("run_id", "count"),
    emu=("emulated", "sum"),
)
emu_year["emu_pct"] = 100 * emu_year["emu"] / emu_year["total"]
print(emu_year.to_string())

# --- ana_16: Super Mario 64 platform mix (the canonical N64-era classic) ---
print("=== ana_16 ===")
sm64_id = games[games["name"] == "Super Mario 64"]["game_id"].iloc[0]
sm64 = runs[runs["game_id"] == sm64_id]
sm64_plat = sm64["platform_name"].fillna("(unknown)").value_counts()
sm64_emu = sm64.groupby("platform_name")["emulated"].mean() * 100
print(f"Super Mario 64 runs: {len(sm64)}, distinct platforms: {sm64_plat.size}")
for p, n in sm64_plat.items():
    e = sm64_emu.get(p, float("nan"))
    print(f"  {n:>4} ({100*n/len(sm64):4.1f}%)  {p}  (emu {e:5.1f}%)")
overall_emu_pct = 100 * sm64["emulated"].mean()
print(f"\nOverall SM64 emulator share: {overall_emu_pct:.1f}% ({sm64['emulated'].sum()} of {len(sm64)})")

# --- ana_17: PC vs console vs handheld vs unknown — coarse classification ---
print("=== ana_17 ===")
def classify(p):
    if not isinstance(p, str):
        return "(unknown)"
    p = p.strip()
    if p == "PC":
        return "PC"
    if any(k in p for k in ["Switch", "PlayStation", "PS2", "PS3", "PS4", "PS5", "Xbox", "GameCube", "Wii", "N64", "SNES", "NES", "Mega Drive", "Saturn", "Dreamcast", "Arcade"]):
        return "Console"
    if any(k in p for k in ["Game Boy", "DS", "PSP", "Vita", "3DS"]):
        return "Handheld"
    if any(k in p for k in ["iOS", "iPad", "iPhone", "Android"]):
        return "Mobile"
    if any(k in p for k in ["Web", "Browser", "Flash", "HTML"]):
        return "Web"
    return "Other"

runs["coarse_platform"] = runs["platform_name"].apply(classify)
print(runs["coarse_platform"].value_counts().to_string())
print(f"\nfraction PC: {(runs['coarse_platform'] == 'PC').mean()*100:.1f}%")
