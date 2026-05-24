"""Stage 4: Year-over-year stability test — does past overperformance predict future?"""
import pandas as pd
import numpy as np
import os
from scipy import stats

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/06_football-managers/output_files"

seq = pd.read_csv(os.path.join(DATA, "manager_sequence_overperformance_df.csv"), encoding='latin-1')
print(f"Total managers in sequence file: {len(seq)}")

# tenure1_overperformance is 1 if positive, else 0; tenure1_above_expectation is the actual ppg figure
# --- ana_08: tenure1 vs tenure2 — among managers with >=2 tenures, does overperformance carry? ---
print("\n=== ana_08 ===")
two = seq.dropna(subset=['tenure1_above_expectation', 'tenure2_above_expectation'])
print(f"Managers with at least 2 tenures: {len(two)}")
print(f"  tenure1 > 0 (overperformed): {(two['tenure1_above_expectation'] > 0).sum()} ({100*(two['tenure1_above_expectation'] > 0).mean():.1f}%)")
print(f"  tenure2 > 0 (overperformed): {(two['tenure2_above_expectation'] > 0).sum()} ({100*(two['tenure2_above_expectation'] > 0).mean():.1f}%)")

# Conditional: of those who overperformed in tenure1, what fraction overperformed in tenure2?
over1 = two[two['tenure1_above_expectation'] > 0]
under1 = two[two['tenure1_above_expectation'] <= 0]
print(f"\nP(over in t2 | over in t1): {(over1['tenure2_above_expectation'] > 0).mean():.3f}  (n={len(over1)})")
print(f"P(over in t2 | under in t1): {(under1['tenure2_above_expectation'] > 0).mean():.3f}  (n={len(under1)})")

# Pearson correlation between tenure1 and tenure2 ppg-above-expectation
r, p = stats.pearsonr(two['tenure1_above_expectation'], two['tenure2_above_expectation'])
print(f"\nPearson r (tenure1 vs tenure2 ppg-above): {r:.3f} (p={p:.3f})")

# --- ana_09: regression-to-the-mean visualization data — bin tenure1 into quartiles, plot mean tenure2 ---
print("\n=== ana_09 ===")
two = two.copy()
two['t1_q'] = pd.qcut(two['tenure1_above_expectation'], 4, labels=['Q1 (worst)','Q2','Q3','Q4 (best)'])
g = two.groupby('t1_q', observed=True)['tenure2_above_expectation'].agg(['mean','count','std']).reset_index()
print(g.to_string(index=False))

# --- ana_10: scatter pairs (tenure1, tenure2) for chart ---
print("\n=== ana_10 ===")
print("Sample of tenure1 vs tenure2 pairs (first 8 and last 4 by tenure1):")
two_sorted = two.sort_values('tenure1_above_expectation')
print(two_sorted[['TM_manager_name','tenure1_above_expectation','tenure2_above_expectation']].head(8).to_string(index=False))
print("...")
print(two_sorted[['TM_manager_name','tenure1_above_expectation','tenure2_above_expectation']].tail(4).to_string(index=False))
print(f"\nTotal pairs available: {len(two_sorted)}")
