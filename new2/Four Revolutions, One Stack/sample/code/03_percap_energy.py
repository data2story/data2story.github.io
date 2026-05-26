"""Per-capita energy use analysis from core__energy-use-per-capita.csv (1965-2024).

Produces ana_09, ana_10.
"""
from pathlib import Path
import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(r"D:/AI/journalist agent review/phase2/datasets/energy_revolutions/data")

pc = pd.read_csv(DATA_DIR / "core__energy-use-per-capita.csv")
pc = pc.rename(columns={"Per capita energy consumption": "kWh_per_capita"})


# --- ana_09: Per-capita energy convergence — selected entities, 1965-2024 ---
print("=== ana_09 ===")
TRACKED = ["World", "United States", "China", "European Union (27)", "India", "Africa"]
tab = pc[pc.Entity.isin(TRACKED)].pivot(index="Year", columns="Entity", values="kWh_per_capita").sort_index()
print(tab.head(3).round(0).to_string())
print("...")
print(tab.tail(3).round(0).to_string())
print(f"\nRows: {len(tab)}; Year range: {tab.index.min()}-{tab.index.max()}")
print("\n(snapshots)")
for y in [1965, 1980, 2000, 2010, 2020, 2024]:
    if y in tab.index:
        row = tab.loc[y].round(0)
        print(f"  {y}: " + ", ".join(f"{ent}={int(v) if pd.notna(v) else 'NA'}" for ent, v in row.items()))

# Specific finding: US per-capita 1965 vs China per-capita 2024
us_1965 = tab.loc[1965, "United States"] if 1965 in tab.index else None
cn_2024 = tab.loc[2024, "China"] if 2024 in tab.index else None
print(f"\nUS 1965: {us_1965:.0f} kWh/cap; China 2024: {cn_2024:.0f} kWh/cap")
print(f"China 2024 / US 1965: {cn_2024/us_1965:.2f}x")


# --- ana_10: 2024 ranking — top 15 per-capita energy users (real countries) ---
print("\n=== ana_10 ===")
y2024 = pc[(pc.Year == 2024) & pc.Code.notna() & pc.Code.str.match(r"^[A-Z]{3}$")]
y2024 = y2024.sort_values("kWh_per_capita", ascending=False).head(15)
print("Top 15 per-capita energy consumers 2024 (country-level):")
for _, r in y2024.iterrows():
    print(f"  {r.Entity:35s}  {r.kWh_per_capita:,.0f} kWh/cap")
