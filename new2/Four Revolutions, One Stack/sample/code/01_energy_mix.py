"""Energy mix analysis from core__global-energy-by-source.csv (World, 1800-2024).

Produces ana_01..ana_05.
Runnable from anywhere — uses absolute DATA_DIR.
"""
from pathlib import Path
import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")  # Windows console

DATA_DIR = Path(r"D:/AI/journalist agent review/phase2/datasets/energy_revolutions/data")

df = pd.read_csv(DATA_DIR / "core__global-energy-by-source.csv")
df = df.sort_values("Year").reset_index(drop=True)

FUEL_COLS = [
    "Traditional biomass", "Coal", "Oil", "Natural gas", "Hydropower",
    "Nuclear", "Solar", "Wind", "Modern biofuels", "Other renewables",
]
df["Total"] = df[FUEL_COLS].sum(axis=1)


# --- ana_01: Global energy mix 1800-2024 (all fuels, all years) ---
print("=== ana_01 ===")
mix = df[["Year"] + FUEL_COLS + ["Total"]].copy()
print(mix.head(3).to_string(index=False))
print("...")
print(mix.tail(3).to_string(index=False))
print(f"Rows: {len(mix)}, Year range: {int(mix.Year.min())}-{int(mix.Year.max())}")
print(f"Total energy 1800: {df.Total.iloc[0]:.0f} TWh")
print(f"Total energy 1900: {df.loc[df.Year == 1900, 'Total'].iloc[0]:.0f} TWh")
print(f"Total energy 2000: {df.loc[df.Year == 2000, 'Total'].iloc[0]:.0f} TWh")
print(f"Total energy 2024: {df.Total.iloc[-1]:.0f} TWh")
print(f"Multiplier 1800 -> 2024: {df.Total.iloc[-1] / df.Total.iloc[0]:.1f}x")


# --- ana_02: Fuel onset year (first non-zero year per source) ---
print("\n=== ana_02 ===")
onset = []
for col in FUEL_COLS:
    nonzero = df.loc[df[col] > 0, "Year"]
    yr = int(nonzero.iloc[0]) if len(nonzero) else None
    val0 = df.loc[df[col] > 0, col].iloc[0] if len(nonzero) else None
    onset.append((col, yr, val0))
onset.sort(key=lambda x: x[1] or 9999)
for fuel, yr, val in onset:
    print(f"  {fuel:25s} first non-zero: {yr}  (start value: {val:.2f} TWh)" if val else f"  {fuel:25s} all zero")


# --- ana_03: Coal trajectory — share + TWh, with peak year ---
print("\n=== ana_03 ===")
coal_share = (df["Coal"] / df["Total"]) * 100
coal_tab = pd.DataFrame({"Year": df.Year, "Coal_TWh": df.Coal.round(1), "Coal_share_pct": coal_share.round(2)})
peak_idx = coal_share.idxmax()
print(f"Coal peak share: {coal_share.iloc[peak_idx]:.2f}% in {int(df.Year.iloc[peak_idx])}")
print(f"Coal absolute peak (TWh): {df.Coal.max():.0f} in {int(df.Year.iloc[df.Coal.idxmax()])}")
for y in [1800, 1850, 1900, 1950, 2000, 2024]:
    row = df[df.Year == y]
    if not row.empty:
        i = row.index[0]
        print(f"  {y}: Coal = {df.Coal.iloc[i]:.0f} TWh  ({coal_share.iloc[i]:.2f}%)")


# --- ana_04: Total fossil (coal + oil + gas) trajectory ---
print("\n=== ana_04 ===")
fossil = df[["Coal", "Oil", "Natural gas"]].sum(axis=1)
fossil_share = (fossil / df["Total"]) * 100
peak_fs_idx = fossil_share.idxmax()
print(f"Peak fossil share: {fossil_share.iloc[peak_fs_idx]:.2f}% in {int(df.Year.iloc[peak_fs_idx])}")
for y in [1800, 1850, 1900, 1950, 1970, 1990, 2000, 2010, 2024]:
    row = df[df.Year == y]
    if not row.empty:
        i = row.index[0]
        print(f"  {y}: Fossil = {fossil.iloc[i]:.0f} TWh  ({fossil_share.iloc[i]:.2f}%)  [coal {df.Coal.iloc[i]:.0f}, oil {df.Oil.iloc[i]:.0f}, gas {df['Natural gas'].iloc[i]:.0f}]")


# --- ana_05: Solar + Wind takeoff post-2000 ---
print("\n=== ana_05 ===")
solar_wind = df["Solar"] + df["Wind"]
sw_share = (solar_wind / df["Total"]) * 100
for y in [1990, 2000, 2005, 2010, 2015, 2020, 2024]:
    row = df[df.Year == y]
    if not row.empty:
        i = row.index[0]
        print(f"  {y}: Solar+Wind = {solar_wind.iloc[i]:7.1f} TWh ({sw_share.iloc[i]:5.2f}% of primary)  [solar {df.Solar.iloc[i]:.1f}, wind {df.Wind.iloc[i]:.1f}]")

# Per-source decade table for later editorial use
print("\n(reference) per-decade snapshot:")
snap = df[df.Year.isin([1800, 1850, 1900, 1950, 1970, 1990, 2000, 2010, 2024])][["Year"] + FUEL_COLS]
print(snap.to_string(index=False))
