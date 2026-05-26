"""Minifig + parts overview.

Findings produced:
  ana_12: Minifig catalog growth (rows per minifig name year if possible — minifigs.csv has no year, so we approximate via inventory year for any set containing the figure)
  ana_14: Part categories — distribution and how 'specialized' parts grew
  ana_16: Top parts by occurrence across all inventories
"""
from __future__ import annotations
import os
import sys
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA = os.environ.get("DATA", r"D:\AI\journalist agent review\phase2\datasets\2016-06-01_lego-database")

minifigs = pd.read_csv(os.path.join(DATA, "minifigs.csv"))
parts = pd.read_csv(os.path.join(DATA, "parts.csv"))
cats = pd.read_csv(os.path.join(DATA, "part_categories.csv"))
inv = pd.read_csv(os.path.join(DATA, "inventories.csv"))
sets = pd.read_csv(os.path.join(DATA, "sets.csv"))
ip = pd.read_csv(os.path.join(DATA, "inventory_parts.csv"))

# Year for each inventory row via set
latest_inv = inv.sort_values("version").groupby("set_num").tail(1)[["id", "set_num"]]
latest_inv = latest_inv.rename(columns={"id": "inventory_id"})
inv_set_year = latest_inv.merge(sets[["set_num", "year"]], on="set_num", how="left")

# --- ana_12: Minifig catalog (no year column directly) ---
print("=== ana_12 ===")
print(f"Total minifigs in catalog: {len(minifigs):,}")
print(f"Median parts per minifig: {minifigs['num_parts'].median()}")
print(f"Max parts per minifig: {minifigs['num_parts'].max()}")
print("Top 10 most-complex minifigs:")
print(minifigs.nlargest(10, "num_parts")[["fig_num", "name", "num_parts"]].to_string(index=False))

# Estimate minifigs introduced per year via inventory_minifigs would need that file,
# but we can do a rough proxy: count of distinct minifigs appearing in inventory_parts
# of sets in each year (minifig fig_nums are stored as part_num that starts with 'fig-').
# Actually figs are not in inventory_parts. Skip — note this caveat.
print("Note: dataset has no inventory_minifigs file; cannot trace minifig-per-year directly.")

# --- ana_14: Part categories — sets per category, growth ---
print("=== ana_14 ===")
parts_c = parts.merge(cats.rename(columns={"id": "part_cat_id", "name": "cat_name"}),
                      on="part_cat_id", how="left")
cat_count = parts_c.groupby("cat_name").size().rename("n_parts").sort_values(ascending=False)
print(cat_count.head(15).to_string())
print(f"\nTotal part categories: {len(cat_count)}")
print(f"Total distinct parts: {len(parts):,}")

# Part-category growth over time
ipy = ip.merge(inv_set_year[["inventory_id", "year"]], on="inventory_id", how="inner")
ipy = ipy.merge(parts_c[["part_num", "cat_name"]], on="part_num", how="left")
ipy["decade"] = (ipy["year"] // 10) * 10
dec_cat = ipy.groupby(["decade", "cat_name"])["part_num"].nunique().unstack().fillna(0).astype(int)
print("\nDistinct parts (by category) appearing per decade — top 8 categories:")
topcats = cat_count.head(8).index.tolist()
print(dec_cat[topcats].to_string())

# --- ana_16: Top parts by occurrence across all inventories ---
print("=== ana_16 ===")
top_parts = ip.groupby("part_num")["quantity"].sum().sort_values(ascending=False).head(20)
top_parts = top_parts.reset_index().merge(parts_c[["part_num", "name", "cat_name"]],
                                          on="part_num", how="left")
print(top_parts.to_string(index=False))
