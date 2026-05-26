"""07_helicopter_icecream.py — two niche complaint streams: helicopter + ice cream truck.

Produces: ana_19 (helicopter 2023 vs 2024 growth, monthly), ana_20 (helicopter
borough hotspots), ana_21 (ice cream truck enforcement reality).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")
df["created_date"] = pd.to_datetime(df["created_date"])
df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")
df["year"] = df["created_date"].dt.year
df["month"] = df["created_date"].dt.month

# --- ana_19: Helicopter complaints by month, 2023 vs 2024 ---
print("=== ana_19 ===")
heli = df[df["complaint_type"] == "Noise - Helicopter"]
print(f"Total helicopter-noise complaints, 2023+2024: {len(heli):,}")
heli_y = heli["year"].value_counts().sort_index()
print(f"  2023: {int(heli_y.get(2023, 0)):,}")
print(f"  2024: {int(heli_y.get(2024, 0)):,}")
print(f"  Δ: {int(heli_y.get(2024, 0) - heli_y.get(2023, 0)):+,}   ({100*(heli_y.get(2024,0)-heli_y.get(2023,0))/heli_y.get(2023,1):+.1f}%)")
heli_month = heli.groupby(["year", "month"]).size().unstack("year").fillna(0).astype(int)
print("\nMonthly helicopter complaints, 2023 vs 2024:")
print(heli_month.to_string())

# --- ana_20: Helicopter borough hotspots ---
print("=== ana_20 ===")
heli_bo = heli["borough"].value_counts(dropna=False)
total_heli = len(heli)
for label, count in heli_bo.items():
    print(f"  {count:>7,}  {100*count/total_heli:>5.2f}%  {label}")

# top zips for helicopter
print("\nTop 15 ZIPs for helicopter complaints:")
zip_h = heli.dropna(subset=["incident_zip"]).copy()
zip_h["incident_zip"] = zip_h["incident_zip"].str.zfill(5)
zh_counts = zip_h["incident_zip"].value_counts().head(15)
for z, c in zh_counts.items():
    b = zip_h.loc[zip_h["incident_zip"] == z, "borough"].mode()
    b_str = str(b.iloc[0]) if len(b) else "?"
    print(f"  {z}  {c:>5,}  {b_str}")

# --- ana_21: Ice cream truck enforcement reality ---
print("=== ana_21 ===")
ice = df[df["descriptor"].astype(str) == "Noise, Ice Cream Truck (NR4)"]
print(f"Ice-cream-truck complaints, 2023+2024: {len(ice):,}")
print(f"  agency split:")
for label, count in ice["agency"].value_counts().items():
    print(f"     {count:>5,}  {label}")
# resolution_description for ice cream truck
print("\nTop resolution_description for ice cream truck complaints:")
top_res = ice["resolution_description"].fillna("(no text)").value_counts().head(10)
for r, c in top_res.items():
    snip = (r[:100] + "...") if len(r) > 100 else r
    print(f"  {c:>4,}  {snip}")

# how many actually issued a summons
res_low = ice["resolution_description"].fillna("").str.lower()
sum_mask = res_low.str.contains("issued a summons|issued a violation", na=False, regex=True)
n_summons = int(sum_mask.sum())
print(f"\nresolved with 'issued a summons/violation': {n_summons:,} / {len(ice):,}  ({100*n_summons/max(len(ice),1):.2f}%)")
