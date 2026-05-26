"""Moore's law analysis from core__transistors-per-chip.csv (1971-2021)."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(r"D:/AI/journalist agent review/phase2/datasets/energy_revolutions/data")

m = pd.read_csv(DATA_DIR / "core__transistors-per-chip.csv")
m = m.rename(columns={"Transistors per microprocessor": "transistors"})
m = m.sort_values("Year").reset_index(drop=True)


# --- ana_15: Transistor count over time + doubling time pre/post-2010 ---
print("=== ana_15 ===")
print(f"Rows: {len(m)}; Year range: {int(m.Year.min())}-{int(m.Year.max())}")
print("Selected milestones:")
for y in [1971, 1985, 2000, 2010, 2015, 2021]:
    near = m[m.Year == y]
    if not near.empty:
        print(f"  {y}: {int(near.transistors.iloc[0]):,} transistors")
print(f"  ALL: 1971 first = {int(m.transistors.iloc[0]):,}; 2021 last = {int(m.transistors.iloc[-1]):,}")
mult = m.transistors.iloc[-1] / m.transistors.iloc[0]
print(f"  Multiplier 1971->2021: {mult:.2e}x")

# Doubling time pre-2010 vs post-2010
pre = m[m.Year < 2010]
post = m[m.Year >= 2010]

def doubling(df_):
    b, a = np.polyfit(df_.Year.astype(float), np.log10(df_.transistors), 1)
    dt = np.log10(2) / b if b > 0 else float("inf")
    return b, dt

if len(pre) >= 2:
    b_pre, dt_pre = doubling(pre)
    print(f"Pre-2010 ({len(pre)} pts): log10 slope = {b_pre:.4f}/yr  =>  doubling time = {dt_pre*12:.1f} months")
if len(post) >= 2:
    b_post, dt_post = doubling(post)
    print(f"Post-2010 ({len(post)} pts): log10 slope = {b_post:.4f}/yr  =>  doubling time = {dt_post*12:.1f} months")
    print(f"Slowdown factor: post/pre = {dt_post/dt_pre:.2f}x (>1 means slowing)")

# Print all rows for chart-ready data
print("\n(reference) All chips in series:")
print(m[["Year", "transistors"]].to_string(index=False))
