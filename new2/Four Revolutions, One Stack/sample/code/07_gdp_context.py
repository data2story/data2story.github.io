"""World GDP-per-capita context from context__gdp-per-capita-maddison.csv (1 AD-2022)."""
from pathlib import Path
import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(r"D:/AI/journalist agent review/phase2/datasets/energy_revolutions/data")

g = pd.read_csv(DATA_DIR / "context__gdp-per-capita-maddison.csv")
g = g.rename(columns={"GDP per capita": "gdp_pc"})


# --- ana_17: World vs early-modern UK GDP per capita — pre/post 1800 takeoff ---
print("=== ana_17 ===")
# World aggregate only available from 1820 in Maddison 2023; pre-1820 must use country series
# Use UK as the longest continuous series with pre-industrial data
world = g[g.Entity == "World"].dropna(subset=["gdp_pc"]).sort_values("Year").reset_index(drop=True)
uk = g[g.Entity == "United Kingdom"].dropna(subset=["gdp_pc"]).sort_values("Year").reset_index(drop=True)
print(f"World series rows: {len(world)}, year range {int(world.Year.min())}-{int(world.Year.max())}")
print(f"UK series rows: {len(uk)}, year range {int(uk.Year.min())}-{int(uk.Year.max())}")

def nearest(df_, target):
    idx = (df_.Year - target).abs().idxmin()
    return df_.iloc[idx]

print("\nUK GDP/cap (longest continuous pre-industrial series):")
for y in [1252, 1500, 1600, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2022]:
    if not uk.empty:
        n = nearest(uk, y)
        print(f"  target {y}: actual {int(n.Year)} = ${n.gdp_pc:,.0f}")

print("\nWorld GDP/cap (Maddison world aggregate, 1820+):")
for y in [1820, 1850, 1900, 1950, 1970, 2000, 2022]:
    if not world.empty:
        n = nearest(world, y)
        print(f"  target {y}: actual {int(n.Year)} = ${n.gdp_pc:,.0f}")

# Pre vs post 1800 growth comparison using UK
print("\nUK pre- vs post-1800 growth rates:")
uk1500 = float(nearest(uk, 1500).gdp_pc); y1500 = int(nearest(uk, 1500).Year)
uk1800 = float(nearest(uk, 1800).gdp_pc); y1800 = int(nearest(uk, 1800).Year)
uk2022 = float(nearest(uk, 2022).gdp_pc); y2022 = int(nearest(uk, 2022).Year)
import math
pre_yrs = y1800 - y1500
post_yrs = y2022 - y1800
pre_rate = math.log(uk1800 / uk1500) / pre_yrs if pre_yrs else 0
post_rate = math.log(uk2022 / uk1800) / post_yrs if post_yrs else 0
print(f"  UK {y1500} (${uk1500:,.0f}) -> {y1800} (${uk1800:,.0f}): {uk1800/uk1500:.2f}x over {pre_yrs} years, {pre_rate*100:.3f}%/yr continuous")
print(f"  UK {y1800} (${uk1800:,.0f}) -> {y2022} (${uk2022:,.0f}): {uk2022/uk1800:.2f}x over {post_yrs} years, {post_rate*100:.3f}%/yr continuous")
print(f"  Post-1800 growth rate is {post_rate/pre_rate:.1f}x the pre-1800 rate")

# World 1820 -> 2022
w1820 = float(nearest(world, 1820).gdp_pc)
w2022 = float(nearest(world, 2022).gdp_pc)
print(f"\nWorld 1820 (${w1820:,.0f}) -> 2022 (${w2022:,.0f}): {w2022/w1820:.2f}x over {int(world.Year.max())-1820} years")
print(f"  Continuous growth: {math.log(w2022/w1820)/(int(world.Year.max())-1820)*100:.3f}%/yr")
