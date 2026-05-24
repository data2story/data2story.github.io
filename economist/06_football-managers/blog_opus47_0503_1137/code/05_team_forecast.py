"""Stage 5: Team-season expected vs actual points — confirms the forecast is unbiased."""
import pandas as pd
import numpy as np
import os
from scipy import stats

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/06_football-managers/output_files"

ts = pd.read_csv(os.path.join(DATA, "team_season_performance_df.csv"), encoding='latin-1')

# --- ana_11: forecast accuracy — mean absolute error in points-per-team-per-season ---
print("=== ana_11 ===")
ts['err_per_game'] = ts['points_per_game'] - ts['expected_points_per_game']
ts['err_per_season'] = ts['err_per_game'] * ts['total_games']
print(f"Total team-seasons: {len(ts)}")
print(f"Mean absolute error per season: {ts['err_per_season'].abs().mean():.2f} points")
print(f"Median absolute error per season: {ts['err_per_season'].abs().median():.2f}")
print(f"By league:")
for lg, grp in ts.groupby('league_country'):
    mae = (grp['err_per_game'] * grp['total_games']).abs().mean()
    print(f"  {lg}: MAE={mae:.2f}, n={len(grp)}")

# --- ana_12: most-overperforming and most-underperforming team-seasons ---
print("\n=== ana_12 ===")
ts['ppga'] = ts['points_per_game_above_expectation']
top = ts.nlargest(8, 'ppga')[['league_country','season','team','total_points','total_expected_points','ppga']]
print("TOP 8 team-seasons (most over):")
print(top.to_string(index=False))
bot = ts.nsmallest(5, 'ppga')[['league_country','season','team','total_points','total_expected_points','ppga']]
print("\nBOTTOM 5 team-seasons (most under):")
print(bot.to_string(index=False))

# --- ana_13: league counts + total team-seasons summary ---
print("\n=== ana_13 ===")
print("Team-seasons per league:")
print(ts['league_country'].value_counts())

# --- ana_14: scatter data — actual vs expected points per game, per team-season ---
print("\n=== ana_14 ===")
print("Range of expected_points_per_game:", ts['expected_points_per_game'].min(), "-", ts['expected_points_per_game'].max())
print("Range of points_per_game:", ts['points_per_game'].min(), "-", ts['points_per_game'].max())
print(f"Pearson r (expected vs actual): {stats.pearsonr(ts['expected_points_per_game'], ts['points_per_game'])[0]:.3f}")
