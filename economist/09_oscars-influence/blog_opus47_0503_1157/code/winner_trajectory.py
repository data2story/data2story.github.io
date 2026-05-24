"""Trajectory of Best Picture winners' annual_share and rank over time, by decade."""
import pandas as pd
import numpy as np

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/09_oscars-influence/movie-counts.csv'
df = pd.read_csv(DATA, encoding='latin-1')

winners = df[df['result'] == 'W'].copy().sort_values('oscars_year')
winners['decade'] = (winners['oscars_year'] // 10) * 10

# --- ana_04: Best Picture winners and their annual_share, every year ---
print("=== ana_04 ===")
print(f"Total BP winners in dataset: {len(winners)}")
print("\nFirst 5:")
print(winners[['movie_name','oscars_year','count','year_rank','annual_share']].head().to_string(index=False))
print("\nLast 5:")
print(winners[['movie_name','oscars_year','count','year_rank','annual_share']].tail().to_string(index=False))
# line 16

# --- ana_05: Decade summary of BP winners' annual_share ---
print("\n=== ana_05 ===")
decade_stats = winners.groupby('decade').agg(
    n=('movie_name', 'count'),
    mean_share=('annual_share', 'mean'),
    median_share=('annual_share', 'median'),
    mean_rank=('year_rank', 'mean'),
    median_rank=('year_rank', 'median'),
    pct_top1=('year_rank', lambda s: (s == 1).mean() * 100),
    pct_top10=('year_rank', lambda s: (s <= 10).mean() * 100),
)
print(decade_stats.to_string())
# line 28

# --- ana_06: How often is the BP winner the most-referenced film of its year? ---
print("\n=== ana_06 ===")
# Simple breakdown
top1 = winners[winners['year_rank'] == 1]
print(f"BP winners that are #1 in their year: {len(top1)} of {len(winners)} ({len(top1)/len(winners)*100:.1f}%)")
# By era
pre1980 = winners[winners['oscars_year'] < 1980]
post1980 = winners[winners['oscars_year'] >= 1980]
print(f"\npre-1980: {(pre1980['year_rank']==1).sum()} of {len(pre1980)} ({(pre1980['year_rank']==1).mean()*100:.1f}%) were #1 in year")
print(f"1980+: {(post1980['year_rank']==1).sum()} of {len(post1980)} ({(post1980['year_rank']==1).mean()*100:.1f}%) were #1 in year")
print(f"\npre-1980 mean annual_share: {pre1980['annual_share'].mean()*100:.1f}%")
print(f"1980+ mean annual_share: {post1980['annual_share'].mean()*100:.1f}%")
# line 41

# --- ana_07: Worst-ranked Best Picture winners (biggest 'misses') ---
print("\n=== ana_07 ===")
biggest_misses = winners.sort_values('year_rank', ascending=False).head(15)
print(biggest_misses[['movie_name','oscars_year','count','year_rank','annual_share']].to_string(index=False))
# line 47

# --- ana_08: Best Picture winners that DID beat their year (#1 ranks) ---
print("\n=== ana_08 ===")
print(top1[['movie_name','oscars_year','count','year_rank','annual_share']].to_string(index=False))
print(f"\nLast year a BP winner was #1 in its year: {top1['oscars_year'].max()}")
# line 53
