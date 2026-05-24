"""Stage 3: Final manager rating table — projected points added per season after shrinkage."""
import pandas as pd
import os

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/06_football-managers/output_files"

ratings = pd.read_csv(os.path.join(DATA, "manager_ratings_df.csv"), encoding='latin-1')
ratings = ratings.sort_values('ProjPointsAboveAverage', ascending=False).reset_index(drop=True)

# --- ana_05: top 10 currently-employed managers by projected points added per season ---
print("=== ana_05 ===")
top10 = ratings.head(10)[['TM_manager_name', 'CurrentTeam', 'PrevCareerMatches',
                          'PrevCareerAdjPtsAboveExpectation', 'ProjPointsAboveAverage']]
print(top10.to_string(index=False))

# --- ana_06: bottom 5 ---
print("\n=== ana_06 ===")
bot5 = ratings.tail(5)[['TM_manager_name', 'CurrentTeam', 'PrevCareerMatches',
                        'PrevCareerAdjPtsAboveExpectation', 'ProjPointsAboveAverage']]
print(bot5.to_string(index=False))

# --- ana_07: distribution of projected impact for the active board ---
print("\n=== ana_07 ===")
proj = ratings['ProjPointsAboveAverage']
print(f"N currently-employed managers: {len(proj)}")
print(f"Mean projection: {proj.mean():.3f}")
print(f"Median projection: {proj.median():.3f}")
print(f"Std: {proj.std():.3f}")
print(f"Range: [{proj.min():.3f}, {proj.max():.3f}]")
print(f"Top 10% projection threshold: {proj.quantile(0.90):.3f}")
print(f"# with > 1.0 ppg added: {(proj > 1.0).sum()} ({100*(proj > 1.0).mean():.1f}%)")
print(f"# with > 0.5 ppg added: {(proj > 0.5).sum()} ({100*(proj > 0.5).mean():.1f}%)")
print(f"# negative (sub-average): {(proj < 0).sum()} ({100*(proj < 0).mean():.1f}%)")
print(f"# within +/-0.5 ppg added: {((proj.abs() <= 0.5)).sum()} ({100*((proj.abs() <= 0.5)).mean():.1f}%)")
