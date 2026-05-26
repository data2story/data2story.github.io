"""ana_01: Dataset profile — file counts, row counts, schemas, year range.

Run from repository root. Reads CSVs from the dataset directory passed as DATA.
"""
from __future__ import annotations
import os
import sys
import pandas as pd

DATA = os.environ.get("DATA", r"D:\AI\journalist agent review\phase2\datasets\2016-06-01_lego-database")

files = [
    "sets.csv", "themes.csv", "colors.csv", "parts.csv", "part_categories.csv",
    "inventories.csv", "inventory_parts.csv", "inventory_sets.csv", "minifigs.csv",
]

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
rows = []
for fn in files:
    p = os.path.join(DATA, fn)
    df = pd.read_csv(p)
    rows.append((fn, len(df), len(df.columns), ",".join(df.columns)))
    print(f"{fn:30s}  rows={len(df):>10,}  cols={len(df.columns):>2}  | {','.join(df.columns)}")
print()

# Year range from sets.csv
sets = pd.read_csv(os.path.join(DATA, "sets.csv"))
sets_with_parts = sets[sets["num_parts"] > 0]
print(f"sets total rows: {len(sets):,}")
print(f"sets with num_parts>0: {len(sets_with_parts):,}")
print(f"year min/max: {sets['year'].min()} / {sets['year'].max()}")
print(f"sets per year (head 5, tail 5):")
print(sets.groupby("year").size().head())
print(sets.groupby("year").size().tail())
