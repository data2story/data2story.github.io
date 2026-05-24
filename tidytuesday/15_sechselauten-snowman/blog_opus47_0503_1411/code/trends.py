"""Long-run trends in burn duration and Swiss summer temperature.

Outputs ana_10..ana_13 banners.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/15_sechselauten-snowman")
CSV = ROOT / "sechselaeuten.csv"

df = pd.read_csv(CSV)

# --- ana_10: Linear trend in summer mean temperature 1923-2025 ---
print("=== ana_10 ===")
tdf = df.dropna(subset=["tre200m0"]).copy()
slope, intercept, r, p, se = stats.linregress(tdf["year"], tdf["tre200m0"])
print(f"n = {len(tdf)}")
print(f"slope: {slope:.4f} C/year   r = {r:.3f}   p = {p:.2e}")
print(f"100-year warming implied by slope: {slope*100:.2f} C")
# Compare first 30 vs last 30 years
first30 = tdf.head(30)["tre200m0"]
last30 = tdf.tail(30)["tre200m0"]
print(f"first 30 yrs covered ({tdf.head(30)['year'].min()}-{tdf.head(30)['year'].max()}) mean T: {first30.mean():.2f}C")
print(f"last 30 yrs covered ({tdf.tail(30)['year'].min()}-{tdf.tail(30)['year'].max()}) mean T: {last30.mean():.2f}C")
print(f"diff: {last30.mean()-first30.mean():.2f}C")

# --- ana_11: Linear trend in burn duration 1923-2025 ---
print("\n=== ana_11 ===")
ddf = df.dropna(subset=["duration"]).copy()
slope2, intercept2, r2, p2, se2 = stats.linregress(ddf["year"], ddf["duration"])
print(f"n = {len(ddf)}")
print(f"slope: {slope2:.4f} min/year   r = {r2:.3f}   p = {p2:.4f}")
print(f"100-year change implied by slope: {slope2*100:.2f} min")
# decadal means of duration
ddf["decade"] = (ddf["year"] // 10) * 10
dec = ddf.groupby("decade")["duration"].agg(["count", "mean", "median"]).round(2)
print("decadal means/medians:")
print(dec)

# --- ana_12: Year-by-year duration vs T table for charts ---
print("\n=== ana_12 ===")
joint = df.dropna(subset=["duration", "tre200m0"]).copy()
joint["record"] = joint["record"].astype(bool)
print(f"joint rows: {len(joint)}")
# Print compact CSV-like table for inclusion in data_table
for _, r_ in joint.iterrows():
    print(f"{int(r_['year'])},{r_['duration']:.2f},{r_['tre200m0']:.2f},{int(r_['record'])}")

# --- ana_13: Counts of record (>=19C) summers by decade ---
print("\n=== ana_13 ===")
tdf2 = df.dropna(subset=["tre200m0"]).copy()
tdf2["decade"] = (tdf2["year"] // 10) * 10
rec_dec = tdf2.groupby("decade")["record"].agg(["sum", "count"]).rename(columns={"sum": "record_yrs", "count": "total_yrs"})
rec_dec["pct"] = (rec_dec["record_yrs"] / rec_dec["total_yrs"] * 100).round(1)
print(rec_dec)
