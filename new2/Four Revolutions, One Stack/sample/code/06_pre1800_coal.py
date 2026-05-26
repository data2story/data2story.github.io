"""Pre-Watt English coal analysis from context__uk-industrial-production-1270-1870.csv."""
from pathlib import Path
import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(r"D:/AI/journalist agent review/phase2/datasets/energy_revolutions/data")

uk = pd.read_csv(DATA_DIR / "context__uk-industrial-production-1270-1870.csv")
uk = uk.sort_values("Year").reset_index(drop=True)
# Drop the duplicate-header artifact col_9
keep = [c for c in uk.columns if c != "col_9"]
uk = uk[keep]


# --- ana_16: English coal output 1500-1800 (origin story of the 1st revolution) ---
print("=== ana_16 ===")
coal = uk[["Year", "Coal"]].dropna().reset_index(drop=True)
print(f"English coal series: {len(coal)} rows, year range {int(coal.Year.min())}-{int(coal.Year.max())}")
print("Snapshots (BoE-indexed units; pre-modern reconstruction):")
def nearest_row(target):
    idx = (coal.Year - target).abs().idxmin()
    return coal.iloc[idx]
for y in [1500, 1600, 1700, 1750, 1800, 1850, 1870]:
    nearest = nearest_row(y)
    print(f"  ~{y}: Coal = {nearest.Coal:.3f}  (actual year shown: {int(nearest.Year)})")

# Growth multipliers — use nearest-available years
v_start = nearest_row(1500).Coal  # may snap forward to first available
v_1700 = nearest_row(1700).Coal
v_1800 = nearest_row(1800).Coal
print(f"\nstart -> 1700 multiplier: {v_1700/v_start:.1f}x (pre-Watt growth)")
print(f"1700 -> 1800 multiplier: {v_1800/v_1700:.1f}x (Watt era)")
print(f"start -> 1800 multiplier: {v_1800/v_start:.1f}x (full span)")

# Print full data for chart-ready use
print("\n(reference) Quarter-century snapshots:")
for y in range(1500, 1880, 25):
    near = nearest_row(y)
    print(f"  target {y}: actual {int(near.Year)} Coal = {near.Coal:.3f}")
