"""03_channels.py — channel mix (phone vs online vs mobile vs other) and 2023→2024 shift.

Produces: ana_07 (channel mix overall), ana_08 (channel shift 2023 → 2024).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")
total = len(df)

# --- ana_07: Channel mix overall, 2023 + 2024 combined ---
print("=== ana_07 ===")
ch = df["open_data_channel_type"].value_counts(dropna=False)
print(f"Channel breakdown — all {total:,} noise complaints, 2023 + 2024:")
for label, count in ch.items():
    pct = 100 * count / total
    print(f"  {count:>9,}  {pct:>5.2f}%  {label}")

# --- ana_08: Channel shift, 2023 vs 2024 ---
print("=== ana_08 ===")
df["year"] = df["created_date"].dt.year
ch_y = pd.crosstab(df["open_data_channel_type"], df["year"])
ch_y_pct = ch_y / ch_y.sum() * 100
print("Channel share by year (%):")
for ch_label, row in ch_y_pct.iterrows():
    p23 = row[2023]
    p24 = row[2024]
    delta = p24 - p23
    print(f"  {ch_label:<10}  2023: {p23:5.2f}%   2024: {p24:5.2f}%   Δ {delta:+.2f} pp")
print("\nChannel absolute counts by year:")
for ch_label, row in ch_y.iterrows():
    print(f"  {ch_label:<10}  2023: {row[2023]:>8,}   2024: {row[2024]:>8,}")
