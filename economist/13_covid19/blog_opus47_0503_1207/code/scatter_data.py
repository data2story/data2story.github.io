"""Stage 2 - Analyst: extract chart-ready data tables for the blog."""
import pandas as pd
import numpy as np
import json

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/13_covid19"
pred = pd.read_csv(f"{DATA}/PredictedCases.csv")
cov = pd.read_csv(f"{DATA}/covid_cases_and_covariates_march_4_selected.csv")

# Need mean tour count for each country (the x axis the original chart used)
cov['mean_tour'] = (cov['outbound_tour_groups_Q3_2019_improved'] +
                    cov['inbound_tour_groups_Q3_2019_1_improved']) / 2

merged = pred.merge(cov[['country', 'mean_tour', 'continent']], on='country', how='left')

# --- ana_07: Full scatter — every country's tourism vs reported cases ---
print("=== ana_07 ===")
print("Scatter data (124 rows, country, mean_tour, cases, oecd, predicted_cases, residual_log, continent)")
sample = merged.sort_values('mean_tour', ascending=False).head(20)
for _, r in sample.iterrows():
    print(f"  {r['country']:25s}  tour={int(r['mean_tour']):>10,}  cases={int(r['cases']):>6,}  oecd={r['oecd']}  resid={r['NoPopModResidualLogCases']:+.2f}")

# --- ana_08: 'Hidden cases' multiplier table for the worst under-detectors ---
print("\n=== ana_08 ===")
print("Top 12 under-detectors with their predicted-vs-reported multiplier:")
under = merged[merged['NoPopModPredictedCases'] >= 50].sort_values('NoPopModResidualLogCases').head(12).copy()
under['multiplier'] = under['NoPopModPredictedCases'] / np.maximum(under['cases'], 1)
print(f"{'Country':25s}  {'Reported':>9s}  {'Predicted':>10s}  {'Multiplier':>11s}")
for _, r in under.iterrows():
    print(f"  {r['country']:23s}  {int(r['cases']):>9,}  {r['NoPopModPredictedCases']:>10.0f}  {r['multiplier']:>10.1f}x")

# Save chart-ready JSON-friendly tables for analyst.json
out = {}
out['scatter'] = [
    {
        'country': r['country'],
        'mean_tour': float(r['mean_tour']),
        'cases': int(r['cases']),
        'oecd': bool(r['oecd']),
        'predicted_cases': float(r['NoPopModPredictedCases']),
        'residual_log': float(r['NoPopModResidualLogCases']),
        'continent': r['continent'],
    }
    for _, r in merged.iterrows()
]

# Regression line data: predicted = exp(-8.4363 + 1.1313 * log(tour))
xs = np.logspace(0, np.log10(merged['mean_tour'].max()), 50)
out['regression_line'] = [
    {
        'mean_tour': float(x),
        'predicted_cases': float(np.exp(-8.4363 + 1.1313 * np.log(max(x, 1)))),
    }
    for x in xs
]

print(f"\nWrote {len(out['scatter'])} scatter rows and {len(out['regression_line'])} reg-line rows.")
print("Sample regression line points:")
for p in out['regression_line'][::10]:
    print(f"  tour={p['mean_tour']:>10.0f}  predicted_cases={p['predicted_cases']:>10.2f}")
