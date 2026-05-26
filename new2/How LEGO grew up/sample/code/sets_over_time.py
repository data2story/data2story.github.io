"""Sets over time — annual introductions, complexity creep, biggest-set arc.

Findings produced:
  ana_02: Annual set introductions
  ana_03: Median + 95th pct + max set size per year
  ana_04: Top 20 largest sets ever
  ana_15: 2003 crisis dip (set introductions before/during/after)
  ana_18: Median set size growth multiple, 1980 vs 2020
"""
from __future__ import annotations
import os
import sys
import pandas as pd

# Force UTF-8 stdout on Windows so set names with accents print without raising.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA = os.environ.get("DATA", r"D:\AI\journalist agent review\phase2\datasets\2016-06-01_lego-database")
sets = pd.read_csv(os.path.join(DATA, "sets.csv"))
themes = pd.read_csv(os.path.join(DATA, "themes.csv"))
sets = sets.merge(themes[["id", "name"]].rename(columns={"id": "theme_id", "name": "theme_name"}),
                  on="theme_id", how="left")
# Cap at 2024 to exclude partial / future-announced years (data goes to 2027)
sets = sets[sets["year"] <= 2024]
sets_p = sets[sets["num_parts"] > 0].copy()

# --- ana_02: Annual set introductions ---
print("=== ana_02 ===")
per_year = sets.groupby("year").size().rename("n_sets")
per_year_with_parts = sets_p.groupby("year").size().rename("n_sets_with_parts")
tbl = pd.concat([per_year, per_year_with_parts], axis=1).fillna(0).astype(int).reset_index()
print(tbl.to_string(index=False))
print()
print(f"max year: {sets['year'].max()}, total years covered: {sets['year'].nunique()}")

# --- ana_03: Median + 95th + max set size per year ---
print("=== ana_03 ===")
agg = sets_p.groupby("year")["num_parts"].agg(["median", "mean",
                                                lambda s: s.quantile(0.95),
                                                "max", "count"]).rename(
    columns={"<lambda_0>": "p95"})
agg = agg.reset_index()
print(agg.to_string(index=False))

# --- ana_04: Top 20 largest sets ever ---
print("=== ana_04 ===")
top20 = sets_p.nlargest(20, "num_parts")[["set_num", "name", "year", "theme_name", "num_parts"]]
print(top20.to_string(index=False))

# --- ana_15: 2003 crisis dip ---
print("=== ana_15 ===")
window = sets_p[sets_p["year"].between(1998, 2010)].groupby("year").size()
print(window.to_string())

# --- ana_18: Set complexity growth ratio ---
print("=== ana_18 ===")
m1980 = sets_p[sets_p["year"] == 1980]["num_parts"].median()
m2020 = sets_p[sets_p["year"] == 2020]["num_parts"].median()
m1990 = sets_p[sets_p["year"] == 1990]["num_parts"].median()
m2010 = sets_p[sets_p["year"] == 2010]["num_parts"].median()
print(f"median 1980: {m1980}")
print(f"median 1990: {m1990}")
print(f"median 2010: {m2010}")
print(f"median 2020: {m2020}")
print(f"ratio 2020/1980: {m2020 / m1980:.2f}x")
print(f"ratio 2020/1990: {m2020 / m1990:.2f}x")

# Decade-average for the narrative
print()
print("decade-averaged median set size:")
sets_p["decade"] = (sets_p["year"] // 10) * 10
decade_med = sets_p.groupby("decade")["num_parts"].median()
print(decade_med.to_string())
