"""
simulation_pvals.py — Use The Pudding's pre-computed p-values from
analysis/pvals.csv (1,000-iteration shuffle of each station's 24-hour log
with no avoidance rule applied) to quantify how many stations have observed
women's b2b rates LOWER than chance, and how often the pattern is statistically
significant.
"""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"
pvals = pd.read_csv(os.path.join(DATA_DIR, "analysis", "pvals.csv"))
summary = pd.read_csv(os.path.join(DATA_DIR, "output", "summary.csv"))

# --- ana_20: How many stations have observed b2b women rates significantly below chance ---
print("=== ana_20 ===")
print(f"Stations with permutation p-values: {len(pvals)}")
print()
print("p-value interpretation: probability that an unrestricted shuffle of the")
print("playlist produces a women's b2b rate as low as the observed value.")
print()
sig_05 = (pvals["pval_women"] < 0.05).sum()
sig_01 = (pvals["pval_women"] < 0.01).sum()
sig_001 = (pvals["pval_women"] < 0.001).sum()
zero_p = (pvals["pval_women"] == 0).sum()
print(f"Stations with p < 0.05  (observed rate is implausibly low under chance):  {sig_05} of {len(pvals)}")
print(f"Stations with p < 0.01:  {sig_01} of {len(pvals)}")
print(f"Stations with p < 0.001: {sig_001} of {len(pvals)}")
print(f"Stations with p = 0 (NEVER appeared in 1000 simulations of pure chance): {zero_p} of {len(pvals)}")
print()
print("Distribution of p-values:")
print(pvals["pval_women"].describe())

# --- ana_21: Per-station significance table ---
print("\n=== ana_21 ===")
joined = pvals.merge(summary[["cityName","stationName","b2bWomenSongs_PERCENT","onlyWomenSongs_PERCENT"]],
                     on=["cityName","stationName"])
joined = joined.sort_values("pval_women").reset_index(drop=True)
print("Per-station observed women's b2b rate vs simulation p-value:")
print(joined.to_string(index=False))

# --- ana_22: How would women's b2b rate look at chance? ---
print("\n=== ana_22 ===")
# Expected b2b rate under independence = (share)^2  approximately
expected = (summary["onlyWomenSongs_PERCENT"]/100) ** 2 * 100
observed = summary["b2bWomenSongs_PERCENT"]
ratio = observed / expected
station_compare = summary[["cityName","stationName","onlyWomenSongs_PERCENT","b2bWomenSongs_PERCENT"]].copy()
station_compare["expected_b2b_pct_at_chance"] = expected.round(3)
station_compare["observed_b2b_pct"] = observed.round(3)
station_compare["observed_over_expected"] = ratio.round(3)
station_compare = station_compare.sort_values("observed_over_expected")
print("Observed vs chance-expected women's b2b rate per station:")
print(station_compare.to_string(index=False))
print()
median_ratio = ratio.median()
n_below_chance = (ratio < 1).sum()
print(f"Median observed/expected ratio: {median_ratio:.3f}")
print(f"Stations where observed b2b is BELOW the simple chance expectation: {n_below_chance} of 29")
