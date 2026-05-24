"""Stage 6: Trajectory data for the canonical exemplars (Ferguson, Klopp, Guardiola, etc.)."""
import pandas as pd
import os
import numpy as np

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/06_football-managers/output_files"

ratings = pd.read_csv(os.path.join(DATA, "manager_ratings_df.csv"), encoding='latin-1')
tenures = pd.read_csv(os.path.join(DATA, "manager_all_tenures_performance_df.csv"), encoding='latin-1')
mtable = pd.read_csv(os.path.join(DATA, "manager_table_df.csv"), encoding='latin-1')

# --- ana_15: Ferguson at Manchester United — full numbers ---
print("=== ana_15 ===")
fer = tenures[tenures['TM_manager_name'].str.contains('Ferguson', na=False)]
print(fer[['TM_manager_name','TM_team_name','TM_manager_start_date','TM_manager_end_date',
           'current_tenure_total_games','current_tenure_total_points',
           'current_tenure_total_expected_points',
           'current_tenure_points_per_game','current_tenure_expected_points_per_game',
           'current_tenure_points_per_game_above_expectation']].to_string(index=False))

# --- ana_16: Klopp at Borussia Dortmund and Liverpool ---
print("\n=== ana_16 ===")
kl = tenures[tenures['TM_manager_name'].str.contains('Klopp', na=False)]
print(kl[['TM_manager_name','TM_team_name','TM_manager_start_date','TM_manager_end_date',
          'current_tenure_total_games','current_tenure_total_points',
          'current_tenure_total_expected_points',
          'current_tenure_points_per_game','current_tenure_expected_points_per_game',
          'current_tenure_points_per_game_above_expectation']].to_string(index=False))

# --- ana_17: Other notable managers' tenure profiles for comparison cards ---
print("\n=== ana_17 ===")
notables = ['Pep Guardiola', 'Jose Mourinho', 'Mauricio Pochettino', 'Diego Simeone',
            'Antonio Conte', 'Carlo Ancelotti', 'Massimiliano Allegri', 'Arsene Wenger',
            'Zinedine Zidane', 'Thomas Tuchel', 'Lucien Favre', 'Maurizio Sarri']
for name in notables:
    sub = tenures[tenures['TM_manager_name'] == name]
    if len(sub) == 0:
        continue
    sub2 = sub.dropna(subset=['current_tenure_total_games']).copy()
    if len(sub2) == 0:
        continue
    for _, r in sub2.iterrows():
        print(f"{name} | {r['TM_team_name']} | games={r['current_tenure_total_games']:.0f} | "
              f"ppg={r['current_tenure_points_per_game']:.3f} | "
              f"exp={r['current_tenure_expected_points_per_game']:.3f} | "
              f"above={r['current_tenure_points_per_game_above_expectation']:+.3f}")

# --- ana_18: Shrinkage example — show Ferguson's career carry-over ---
print("\n=== ana_18 ===")
# from README: 461 games of zero overperformance must be added
# Ferguson: 342 games => carry = 342 / (342 + 461) = 0.426
# 1-season manager: 38 games => carry = 38 / (38 + 461) = 0.0762
import numpy as np
shrink_games = 461
for label, g in [("1 season (38 games)", 38), ("Half a season (19)", 19),
                 ("3 seasons (114)", 114), ("10 seasons (380)", 380),
                 ("Ferguson tenure (342)", 342),
                 ("20 seasons (760)", 760)]:
    carry = g / (g + shrink_games)
    print(f"  {label}: carry = {g}/({g}+{shrink_games}) = {carry:.3f}  ({100*carry:.1f}% of record retained)")
