"""For each year, find the most-referenced film and compare to the actual Best Picture winner."""
import pandas as pd
import numpy as np

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/09_oscars-influence/movie-counts.csv'
df = pd.read_csv(DATA, encoding='latin-1')

# --- ana_09: Top 1 film per year vs Best Picture winner of that year ---
# 'Best Picture year' is oscars_year. The dataset only has oscars years where someone won, but we
# also have other films in those years. Find the #1 film per oscars_year and the BP winner.
print("=== ana_09 ===")
top1_by_year = df.loc[df['year_rank'] == 1, ['movie_name','oscars_year','count','annual_share','result']].copy()
winners = df[df['result'] == 'W'][['movie_name','oscars_year','count','annual_share','year_rank']].rename(
    columns={'movie_name':'winner_name','count':'winner_count','annual_share':'winner_share','year_rank':'winner_rank'}
)
merged = winners.merge(top1_by_year, on='oscars_year', how='left', suffixes=('_w','_t'))
merged = merged.rename(columns={'movie_name':'top1_name','count':'top1_count','annual_share':'top1_share','result':'top1_result'})
merged = merged[['oscars_year','winner_name','winner_count','winner_share','winner_rank','top1_name','top1_count','top1_share','top1_result']]
merged['winner_was_top1'] = merged['winner_name'] == merged['top1_name']
print(f"Years where winner was the #1 film: {merged['winner_was_top1'].sum()}/{len(merged)}")
print("\nAll BP winners with their year's #1 film (most recent first):")
print(merged.sort_values('oscars_year', ascending=False).head(25).to_string(index=False))
# line 24

# --- ana_10: For every year, the most-referenced non-nominated film vs BP winner ---
print("\n=== ana_10 ===")
# In each oscars_year that has a winner, find the most-referenced film that was NOT nominated for BP.
def top_unnominated(year):
    sub = df[(df['oscars_year'] == year) & (df['result'].isna())]
    if sub.empty:
        return None
    return sub.sort_values('count', ascending=False).iloc[0]

unnoms = []
for _, w in winners.iterrows():
    yr = w['oscars_year']
    t = top_unnominated(yr)
    if t is None:
        continue
    unnoms.append({
        'oscars_year': yr,
        'winner': w['winner_name'],
        'winner_count': w['winner_count'],
        'top_unnom': t['movie_name'],
        'top_unnom_count': t['count'],
        'gap': t['count'] - w['winner_count'],
    })
unnoms_df = pd.DataFrame(unnoms).sort_values('oscars_year')
big_gaps = unnoms_df.sort_values('gap', ascending=False).head(20)
print("Top 20 'snubs' — biggest gap where the year's most-referenced unnominated film beat the BP winner:")
print(big_gaps.to_string(index=False))
print(f"\nIn how many years did an unnominated film out-reference the BP winner? {(unnoms_df['gap'] > 0).sum()} of {len(unnoms_df)}")
# line 47

# --- ana_11: Annual share of BP winners over time, full series ---
print("\n=== ana_11 ===")
ts = winners[['oscars_year','winner_name','winner_share','winner_count','winner_rank']].sort_values('oscars_year')
ts['decade'] = (ts['oscars_year'] // 10) * 10
print(ts.to_string(index=False))
# line 53

# --- ana_12: Top 20 most-referenced films overall ---
print("\n=== ana_12 ===")
top_overall = df.sort_values('count', ascending=False).head(20)[['movie_name','release_year','oscars_year','result','count','year_rank','annual_share']]
print(top_overall.to_string(index=False))
# line 59

# --- ana_13: Casablanca's 1943 dominance ---
print("\n=== ana_13 ===")
casa = df[(df['oscars_year'] == 1943)].sort_values('count', ascending=False).head(8)
print(casa[['movie_name','count','annual_share','result','year_rank']].to_string(index=False))
# line 64
