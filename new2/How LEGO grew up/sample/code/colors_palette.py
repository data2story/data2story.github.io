"""Color palette evolution — annual unique colors, the 2004 'bley' shift, top colors by use.

Findings produced:
  ana_05: Distinct colors used per year (palette growth)
  ana_06: The 2004 bley shift — old gray vs new gray inventory_parts use
  ana_13: Color first-seen / last-seen — which colors retired and when
  ana_17: Top colors by total quantity across all inventories
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

colors = pd.read_csv(os.path.join(DATA, "colors.csv"))
parts = pd.read_csv(os.path.join(DATA, "parts.csv"))
inventories = pd.read_csv(os.path.join(DATA, "inventories.csv"))
sets = pd.read_csv(os.path.join(DATA, "sets.csv"))
ip = pd.read_csv(os.path.join(DATA, "inventory_parts.csv"))

# Build year per inventory row (use latest inventory version per set, then attribute to set's year)
latest_inv = inventories.sort_values("version").groupby("set_num").tail(1)[["id", "set_num"]]
latest_inv = latest_inv.rename(columns={"id": "inventory_id"})
inv_set_year = latest_inv.merge(sets[["set_num", "year"]], on="set_num", how="left")
ip_y = ip.merge(inv_set_year[["inventory_id", "year"]], on="inventory_id", how="inner")
# remove the [Unknown] color (-1) and cap at 2024 (data goes to 2027 with partial years)
ip_y = ip_y[(ip_y["color_id"] != -1) & (ip_y["year"] <= 2024)]

# --- ana_05: Distinct colors used per year ---
print("=== ana_05 ===")
per_year_colors = ip_y.groupby("year")["color_id"].nunique().rename("n_unique_colors")
print(per_year_colors.to_string())

# --- ana_13: First-seen / last-seen for each color ---
print("=== ana_13 ===")
yrs = ip_y.groupby("color_id")["year"].agg(["min", "max", "count"]).reset_index()
yrs = yrs.merge(colors[["id", "name", "rgb", "is_trans"]].rename(columns={"id": "color_id"}),
                on="color_id", how="left")
yrs = yrs.rename(columns={"min": "first_year", "max": "last_year", "count": "n_rows"})
# Retired = last_year < 2020 (i.e. no use in recent years)
yrs["retired"] = yrs["last_year"] < 2020
print(f"Total colors observed in inventory_parts: {len(yrs)}")
print(f"'Retired' (last seen before 2020): {yrs['retired'].sum()}")
print("\n10 oldest still-active colors:")
active = yrs[~yrs["retired"]].sort_values("first_year")
print(active.head(10).to_string(index=False))
print("\n10 most recently retired colors (last_year):")
retired = yrs[yrs["retired"]].sort_values("last_year", ascending=False)
print(retired.head(10).to_string(index=False))

# --- ana_06: 2004 bley shift — old gray vs new gray ---
print("=== ana_06 ===")
# Rebrickable color IDs (verified against colors.csv):
#   7  = Light Gray (old, 1954-2007)        | 71 = Light Bluish Gray (new, 2002-)
#   8  = Dark Gray (old, 1978-2006)         | 72 = Dark Bluish Gray (new, 1999-)
#   6  = Brown (old, 1974-2006)             | 70 = Reddish Brown (new, 2003-)
focus_ids = {7: "Light Gray (old)", 8: "Dark Gray (old)",
             71: "Light Bluish Gray (new)", 72: "Dark Bluish Gray (new)",
             6: "Brown (old)", 70: "Reddish Brown (new)"}
fc = ip_y[ip_y["color_id"].isin(focus_ids.keys())].copy()
fc["color_name"] = fc["color_id"].map(focus_ids)
shift = fc.groupby(["year", "color_name"])["quantity"].sum().unstack().fillna(0).astype(int)
# keep 1990-2024
shift = shift[(shift.index >= 1990) & (shift.index <= 2024)]
print(shift.to_string())

# --- ana_17: Top colors by total quantity across inventories (overall, all-time) ---
print("=== ana_17 ===")
totals = ip[ip["color_id"] != -1].groupby("color_id")["quantity"].sum().sort_values(ascending=False)
totals = totals.reset_index().merge(colors[["id", "name", "rgb", "is_trans"]].rename(
    columns={"id": "color_id"}), on="color_id", how="left")
totals.columns = ["color_id", "total_qty", "name", "rgb", "is_trans"]
print(totals.head(20).to_string(index=False))

# Save palette growth as decade summary for chart
print("=== palette_growth_decade ===")
ip_y["decade"] = (ip_y["year"] // 10) * 10
dec_palette = ip_y.groupby("decade")["color_id"].nunique()
print(dec_palette.to_string())
