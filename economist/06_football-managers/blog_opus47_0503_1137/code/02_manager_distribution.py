"""Stage 2: Distribution of manager overperformance — the spine of the story."""
import pandas as pd
import numpy as np
import os

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/06_football-managers/output_files"

# manager_ratings_df: one row per CURRENTLY EMPLOYED manager (the "active" board)
ratings = pd.read_csv(os.path.join(DATA, "manager_ratings_df.csv"), encoding='latin-1')
# manager_all_tenures_performance_df: one row per manager-tenure
tenures = pd.read_csv(os.path.join(DATA, "manager_all_tenures_performance_df.csv"), encoding='latin-1')

# --- ana_02: how many tenures and how many distinct managers in the dataset ---
print("=== ana_02 ===")
print(f"Total manager-tenure rows: {len(tenures)}")
print(f"Distinct managers: {tenures['TM_manager_name'].nunique()}")
print(f"Distinct teams: {tenures['TM_team_name'].nunique()}")
print(f"Currently-employed managers (manager_ratings_df): {len(ratings)}")

# --- ana_03: distribution of points-per-game above expectation, all tenures with >= 38 games ---
print("\n=== ana_03 ===")
# use current_tenure stats
big = tenures.dropna(subset=['current_tenure_total_games', 'current_tenure_points_per_game_above_expectation'])
big = big[big['current_tenure_total_games'] >= 38]
ppg_above = big['current_tenure_points_per_game_above_expectation']
print(f"Tenures with >=38 games: {len(big)}")
print(f"Mean ppg-above-expectation: {ppg_above.mean():.4f}")
print(f"Median ppg-above-expectation: {ppg_above.median():.4f}")
print(f"Std: {ppg_above.std():.4f}")
print(f"5th pct: {ppg_above.quantile(0.05):.4f}")
print(f"95th pct: {ppg_above.quantile(0.95):.4f}")
print(f"Min/Max: {ppg_above.min():.4f} / {ppg_above.max():.4f}")

# Histogram bins for distribution chart
bins = np.arange(-1.0, 1.05, 0.10)
counts, edges = np.histogram(ppg_above, bins=bins)
print("\nHistogram (bin_left, count):")
for c, e in zip(counts, edges[:-1]):
    print(f"  [{e:+.2f}, {e+0.10:+.2f}): {c}")

# How many managers actually clear a meaningful threshold?
print(f"\nTenures with > +0.20 ppg-above-expectation: {(ppg_above > 0.20).sum()} ({100*(ppg_above > 0.20).mean():.1f}%)")
print(f"Tenures with > +0.10 ppg-above-expectation: {(ppg_above > 0.10).sum()} ({100*(ppg_above > 0.10).mean():.1f}%)")
print(f"Tenures within +/-0.10 ppg of expectation: {((ppg_above.abs() <= 0.10)).sum()} ({100*((ppg_above.abs() <= 0.10)).mean():.1f}%)")

# --- ana_04: top 12 and bottom 6 manager-tenures by ppg above expectation ---
print("\n=== ana_04 ===")
top = big.nlargest(12, 'current_tenure_points_per_game_above_expectation')[
    ['TM_manager_name', 'TM_team_name', 'current_tenure_total_games',
     'current_tenure_points_per_game', 'current_tenure_expected_points_per_game',
     'current_tenure_points_per_game_above_expectation']
]
print("TOP 12 (>=38 games):")
print(top.to_string(index=False))

bot = big.nsmallest(6, 'current_tenure_points_per_game_above_expectation')[
    ['TM_manager_name', 'TM_team_name', 'current_tenure_total_games',
     'current_tenure_points_per_game', 'current_tenure_expected_points_per_game',
     'current_tenure_points_per_game_above_expectation']
]
print("\nBOTTOM 6 (>=38 games):")
print(bot.to_string(index=False))
