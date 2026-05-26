"""CO2 emissions analysis from core__co2-by-country.csv (1750-2024).

Produces ana_06..ana_08.
"""
from pathlib import Path
import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(r"D:/AI/journalist agent review/phase2/datasets/energy_revolutions/data")

co2 = pd.read_csv(DATA_DIR / "core__co2-by-country.csv")
co2.columns = [c.replace("₂", "2") for c in co2.columns]  # ₂ -> 2
co2 = co2.rename(columns={"Annual CO2 emissions": "CO2"})

world = co2[co2.Entity == "World"].sort_values("Year").reset_index(drop=True)
# Convert to billion tonnes for readability later
world["CO2_Gt"] = world.CO2 / 1e9


# --- ana_06: World CO2 over time, 1750-2024 (decade snapshots + full series) ---
print("=== ana_06 ===")
for y in [1750, 1800, 1850, 1900, 1950, 1970, 1990, 2000, 2010, 2024]:
    r = world[world.Year == y]
    if not r.empty:
        print(f"  {y}: World CO2 = {r.CO2.iloc[0]/1e9:7.3f} Gt/yr  (raw {r.CO2.iloc[0]:.3e})")
print(f"\nFull series rows: {len(world)}, year range {int(world.Year.min())}-{int(world.Year.max())}")
print(f"World CO2 1750 -> 2024: {world.CO2.iloc[0]/1e9:.4f} Gt/yr -> {world.CO2.iloc[-1]/1e9:.2f} Gt/yr  ({world.CO2.iloc[-1]/world.CO2.iloc[0]:.0f}x)")


# --- ana_07: Decoupling check — CO2 per TWh non-biomass primary energy ---
print("\n=== ana_07 ===")
mix = pd.read_csv(DATA_DIR / "core__global-energy-by-source.csv")
fossils = ["Coal", "Oil", "Natural gas"]
non_biomass_cols = ["Coal", "Oil", "Natural gas", "Hydropower", "Nuclear", "Solar", "Wind", "Modern biofuels", "Other renewables"]
mix["non_biomass_TWh"] = mix[non_biomass_cols].sum(axis=1)
mix["fossil_TWh"] = mix[fossils].sum(axis=1)
merged = world.merge(mix[["Year", "non_biomass_TWh", "fossil_TWh"]], on="Year", how="inner")
merged["CO2_per_TWh_nonbiomass"] = merged.CO2 / merged.non_biomass_TWh  # tonnes / TWh
merged["CO2_per_TWh_fossil"] = merged.CO2 / merged.fossil_TWh
print("Year | World CO2 (Gt) | NonBio TWh | CO2/TWh_nonbio (t/TWh) | CO2/TWh_fossil (t/TWh)")
for y in [1850, 1900, 1950, 1970, 1990, 2000, 2010, 2024]:
    r = merged[merged.Year == y]
    if not r.empty:
        a, b, c, d = r.CO2.iloc[0]/1e9, r.non_biomass_TWh.iloc[0], r.CO2_per_TWh_nonbiomass.iloc[0], r.CO2_per_TWh_fossil.iloc[0]
        print(f"  {y}  {a:6.2f}        {b:8.0f}       {c:10.0f}             {d:10.0f}")


# --- ana_08: Top cumulative CO2 emitters 1750-2024 ---
print("\n=== ana_08 ===")
# Drop aggregates (those without Code or with all-caps non-ISO3 codes)
real = co2.copy()
# Keep only rows with a 3-letter Code (real countries) — exclude regions / aggregates
real = real[real.Code.notna() & real.Code.str.match(r"^[A-Z]{3}$") & (real.Code != "OWID_WRL")]
cum = real.groupby("Entity").CO2.sum().sort_values(ascending=False)
total_cum = cum.sum()
print(f"Cumulative country-attributed CO2 1750-2024: {total_cum/1e12:.2f} Tt (trillion tonnes)")
print("\nTop 15 cumulative emitters:")
top15 = cum.head(15)
for ent, val in top15.items():
    pct = val / total_cum * 100
    print(f"  {ent:30s}  {val/1e9:8.1f} Gt   {pct:5.2f}%")
top15_share = top15.sum() / total_cum * 100
print(f"\nTop 15 share: {top15_share:.1f}%")
