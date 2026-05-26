"""01_profile.py — dataset scale, time range, year-over-year volume.

Produces: ana_01 (dataset scale), ana_02 (year-over-year), ana_03 (per-day volume).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")

# --- ana_01: Dataset scale ---
print("=== ana_01 ===")
n_rows = len(df)
n_complaint_types = df["complaint_type"].nunique()
n_descriptors = df["descriptor"].nunique()
n_zips = df["incident_zip"].nunique()
n_agencies = df["agency"].nunique()
print(f"rows: {n_rows:,}")
print(f"complaint_type values: {n_complaint_types}")
print(f"descriptor values: {n_descriptors}")
print(f"distinct ZIP codes: {n_zips}")
print(f"distinct responding agencies: {n_agencies}")
print(f"date range: {df['created_date'].min()}  to  {df['created_date'].max()}")

# --- ana_02: Year-over-year volume (2023 vs 2024) ---
print("=== ana_02 ===")
df["year"] = df["created_date"].dt.year
yc = df["year"].value_counts().sort_index()
print("Noise complaints per calendar year:")
for y, c in yc.items():
    print(f"  {int(y)}: {c:,}")
delta = yc[2024] - yc[2023]
pct = 100 * delta / yc[2023]
print(f"  Δ (2024 − 2023): {delta:+,}  ({pct:+.1f}%)")
print(f"  daily average 2023: {yc[2023] / 365:.0f}")
print(f"  daily average 2024: {yc[2024] / 366:.0f}  (2024 was a leap year)")

# --- ana_03: Daily volume distribution ---
print("=== ana_03 ===")
df["day"] = df["created_date"].dt.normalize()
daily = df.groupby("day").size()
print(f"total days covered: {len(daily)}")
print(f"average complaints per day: {daily.mean():.0f}")
print(f"median complaints per day:  {daily.median():.0f}")
print(f"min day:    {daily.min()}  on {daily.idxmin().date()}")
print(f"max day:    {daily.max()}  on {daily.idxmax().date()}")
# top 10 noisiest days
print("top 10 noisiest days:")
for d, c in daily.nlargest(10).items():
    print(f"  {d.date()}: {c:>5,}")
