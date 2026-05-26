"""08_yoy_delta.py — year-over-year deltas by complaint_type and by borough.

Produces: ana_22 (complaint_type YoY change), ana_23 (borough YoY change).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")
df["year"] = df["created_date"].dt.year

# --- ana_22: complaint_type 2023 vs 2024 ---
print("=== ana_22 ===")
ct = pd.crosstab(df["complaint_type"], df["year"])
ct["Δ"] = ct[2024] - ct[2023]
ct["%Δ"] = (100 * ct["Δ"] / ct[2023]).round(1)
ct = ct.sort_values(2024, ascending=False)
print("Complaint type, 2023 vs 2024:")
print(ct.to_string())

# --- ana_23: borough 2023 vs 2024 ---
print("=== ana_23 ===")
bo = pd.crosstab(df["borough"], df["year"])
bo["Δ"] = bo[2024] - bo[2023]
bo["%Δ"] = (100 * bo["Δ"] / bo[2023]).round(1)
bo = bo.sort_values(2024, ascending=False)
print("Borough, 2023 vs 2024:")
print(bo.to_string())
