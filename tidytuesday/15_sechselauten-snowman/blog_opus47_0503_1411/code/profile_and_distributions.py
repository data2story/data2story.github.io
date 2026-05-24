"""Profile the Sechselaeuten dataset and compute the distributional findings.

All ana_xx anchors are marked with === ana_xx === banners around their print
blocks. Run from any working directory; the script resolves the CSV path
relative to its own location.
"""
from pathlib import Path
import json

import numpy as np
import pandas as pd

ROOT = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/15_sechselauten-snowman")
CSV = ROOT / "sechselaeuten.csv"

df = pd.read_csv(CSV)

# --- ana_01: Dataset profile and missingness ---
print("=== ana_01 ===")
print("rows:", len(df))
print("columns:", list(df.columns))
print("year range:", int(df["year"].min()), "to", int(df["year"].max()))
print("nulls per column:")
print(df.isna().sum())
print("years with NA duration:", df.loc[df["duration"].isna(), "year"].tolist())
print("non-null duration rows:", df["duration"].notna().sum())

# --- ana_02: Burn duration distribution and central tendency ---
print("\n=== ana_02 ===")
d = df["duration"].dropna()
print("count:", len(d))
print(f"mean: {d.mean():.2f}  median: {d.median():.2f}  std: {d.std():.2f}")
print(f"min: {d.min():.2f}  max: {d.max():.2f}")
quantiles = d.quantile([0.1, 0.25, 0.5, 0.75, 0.9])
print("quantiles:")
print(quantiles)
# Histogram bins (chart-ready)
bins = [0, 5, 10, 15, 20, 25, 30, 40, 60]
counts, edges = np.histogram(d, bins=bins)
print("histogram bins:", list(zip(edges[:-1], edges[1:], counts)))

# --- ana_03: Extremes - shortest and longest burns ---
print("\n=== ana_03 ===")
sorted_d = df.dropna(subset=["duration"]).sort_values("duration")
print("shortest 5:")
print(sorted_d.head(5)[["year", "duration", "tre200m0", "record"]].to_string(index=False))
print("longest 5:")
print(sorted_d.tail(5)[["year", "duration", "tre200m0", "record"]].to_string(index=False))

# --- ana_04: Summer mean temperature distribution ---
print("\n=== ana_04 ===")
t = df["tre200m0"].dropna()
print(f"count: {len(t)}  mean: {t.mean():.2f}  median: {t.median():.2f}  std: {t.std():.2f}")
print(f"min: {t.min():.2f}  max: {t.max():.2f}")
print("years above 19C (record summers):", int((df["tre200m0"] >= 19).sum()))
records = df.loc[df["record"] == True, ["year", "tre200m0", "duration"]]  # noqa: E712
print("record-summer rows:")
print(records.to_string(index=False))
