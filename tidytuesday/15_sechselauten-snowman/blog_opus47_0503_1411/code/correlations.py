"""Test the folk-science claim: does burn duration correlate with summer climate?

Outputs ana_05..ana_09 banners.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/15_sechselauten-snowman")
CSV = ROOT / "sechselaeuten.csv"

df = pd.read_csv(CSV).dropna(subset=["duration"])  # only years where the snowman spoke

vars_ = {
    "tre200m0": "summer mean temperature (deg C)",
    "tre200mn": "summer absolute min temp (deg C)",
    "tre200mx": "summer absolute max temp (deg C)",
    "sre000m0": "summer total sunshine (hours)",
    "sremaxmv": "summer sunshine % of possible max",
    "rre150m0": "summer total precipitation (mm)",
}

# --- ana_05: Pearson correlations between burn duration and each climate variable ---
print("=== ana_05 ===")
print(f"n = {len(df)} years (NA durations dropped)")
print(f"{'variable':<12}{'description':<48}{'r':>8}{'p':>10}")
rows = []
for col, desc in vars_.items():
    r, p = stats.pearsonr(df["duration"], df[col])
    print(f"{col:<12}{desc:<48}{r:>8.3f}{p:>10.4f}")
    rows.append((col, desc, round(float(r), 3), round(float(p), 4)))
print()

# --- ana_06: Spearman rank correlations (robust to outliers) ---
print("=== ana_06 ===")
print(f"{'variable':<12}{'description':<48}{'rho':>8}{'p':>10}")
for col, desc in vars_.items():
    rho, p = stats.spearmanr(df["duration"], df[col])
    print(f"{col:<12}{desc:<48}{rho:>8.3f}{p:>10.4f}")
print()

# --- ana_07: How well does the folk rule (faster = hotter) classify record summers? ---
print("=== ana_07 ===")
# A "fast" burn = below the median duration. Folk rule predicts those years should be hotter.
median_dur = df["duration"].median()
fast = df[df["duration"] < median_dur]
slow = df[df["duration"] >= median_dur]
print(f"median duration cutoff: {median_dur:.2f} min")
print(f"fast burns (n={len(fast)}): mean summer T = {fast['tre200m0'].mean():.2f}C, record summers = {fast['record'].sum()}/{len(fast)}")
print(f"slow burns (n={len(slow)}): mean summer T = {slow['tre200m0'].mean():.2f}C, record summers = {slow['record'].sum()}/{len(slow)}")
print(f"diff in mean T (fast - slow): {fast['tre200m0'].mean() - slow['tre200m0'].mean():.3f}C")
t_test = stats.ttest_ind(fast["tre200m0"], slow["tre200m0"], equal_var=False)
print(f"Welch t-test on mean summer T: t={t_test.statistic:.2f}, p={t_test.pvalue:.4f}")

# --- ana_08: Confusion matrix - folk rule "fast = record" vs reality ---
print("\n=== ana_08 ===")
df["folk_predicts_hot"] = df["duration"] < median_dur
ct = pd.crosstab(df["folk_predicts_hot"], df["record"], rownames=["folk says hot"], colnames=["actual record summer"])
print(ct)
total = len(df)
correct = int(ct.loc[True, True]) + int(ct.loc[False, False])
print(f"agreement: {correct}/{total} = {correct/total*100:.1f}%")
# Compare against base rate of always predicting "not record"
base = (df["record"] == False).sum()  # noqa: E712
print(f"base-rate accuracy of always saying 'not record': {base}/{total} = {base/total*100:.1f}%")

# --- ana_09: 2003 vs 2022 vs 2023 - the celebrity case studies ---
print("\n=== ana_09 ===")
celeb_years = [1974, 2003, 2015, 2018, 2019, 2022, 2023, 2025]
for y in celeb_years:
    row = df[df["year"] == y]
    if not row.empty:
        d_ = row["duration"].iloc[0]
        t_ = row["tre200m0"].iloc[0]
        rec = row["record"].iloc[0]
        print(f"{y}: duration {d_:.2f} min, summer T {t_:.2f}C, record={rec}")
