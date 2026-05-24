"""Compare eras: how the Best Picture winner's place in pop culture has shrunk."""
import pandas as pd
import numpy as np

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/09_oscars-influence/movie-counts.csv'
df = pd.read_csv(DATA, encoding='latin-1')
winners = df[df['result'] == 'W'].sort_values('oscars_year').reset_index(drop=True)

# --- ana_14: The 16-year drought (2001-2016) ---
print("=== ana_14 ===")
recent = winners[winners['oscars_year'] >= 2001]
print(f"From 2001-2016, {len(recent)} BP winners. None were #1 in their year.")
print(f"Mean year_rank: {recent['year_rank'].mean():.1f}")
print(f"Median year_rank: {recent['year_rank'].median():.1f}")
print(f"Worst rank: {recent['year_rank'].max()} ({recent.loc[recent['year_rank'].idxmax(),'movie_name']})")
print(f"Best rank: {recent['year_rank'].min()} ({recent.loc[recent['year_rank'].idxmin(),'movie_name']})")
print(f"Mean annual_share: {recent['annual_share'].mean()*100:.2f}%")
# line 16

# --- ana_15: For each year, who ACTUALLY won at the box office of pop culture? ---
print("\n=== ana_15 ===")
# For each oscars_year, get top 3 most-referenced films (the 'people's picks'), and the BP winner
# Show the recent decade (2007-2016) most clearly
def cohort(year):
    sub = df[df['oscars_year'] == year].sort_values('count', ascending=False)
    top3 = sub.head(3)
    winner = sub[sub['result'] == 'W']
    return year, top3[['movie_name','count','result']].values.tolist(), winner[['movie_name','count']].values.tolist() if not winner.empty else []

recent_years = list(range(2007, 2017))
for y in recent_years:
    yr, top3, w = cohort(y)
    print(f"\n{yr}: BP winner = {w}")
    for name, cnt, res in top3:
        flag = '*' if res == 'W' else ('n' if res == 'N' else ' ')
        print(f"   [{flag}] {name}  ({cnt} refs)")
# line 35

# --- ana_16: 'People's Best Pictures' — a counter-list of #1 most-referenced film by year ---
print("\n=== ana_16 ===")
peoples = df[df['year_rank'] == 1].sort_values('oscars_year')
peoples = peoples[['oscars_year','movie_name','count','annual_share','result']]
print(f"{len(peoples)} years' #1 films. Of those, BP winner: {(peoples['result']=='W').sum()}, BP nominee: {(peoples['result']=='N').sum()}, never nominated: {peoples['result'].isna().sum()}")
print("\nThe last 30 'People's Best Pictures':")
print(peoples.tail(30).to_string(index=False))
# line 47

# --- ana_17: Decade share of the top 100 references that go to BP winners ---
print("\n=== ana_17 ===")
# Sum total count of BP winners by decade vs total count of all top-100 films by decade
df['decade'] = (df['oscars_year'] // 10) * 10
by_decade = df.groupby('decade').apply(lambda g: pd.Series({
    'total_count': g['count'].sum(),
    'bp_winner_count': g.loc[g['result']=='W','count'].sum(),
}), include_groups=False)
by_decade['bp_winner_share_of_top100'] = by_decade['bp_winner_count'] / by_decade['total_count'] * 100
print(by_decade.to_string())
# line 58

# --- ana_18: Specific iconic snubs — name some recognizable rivalries ---
print("\n=== ana_18 ===")
# Pick standout BP winner vs unnominated film comparisons  for the narrative
iconic_pairs = [
    (1980, 'Ordinary People', 'Star Wars: Episode V - The Empire Strikes Back'),
    (1977, 'Annie Hall', 'Star Wars: Episode IV - A New Hope'),
    (1994, 'Forrest Gump', 'Pulp Fiction'),
    (1990, 'Dances with Wolves', 'Goodfellas'),
    (1998, 'Shakespeare in Love', 'Saving Private Ryan'),
    (1968, 'Oliver!', '2001: A Space Odyssey'),
    (1960, 'The Apartment', 'Psycho'),
    (1976, 'Rocky', 'Taxi Driver'),
]
for year, winner, rival in iconic_pairs:
    w_row = df[(df['oscars_year']==year) & (df['movie_name']==winner)]
    r_row = df[(df['oscars_year']==year) & (df['movie_name']==rival)]
    if w_row.empty or r_row.empty:
        # search release_year
        r_row = df[(df['release_year']==year) & (df['movie_name']==rival)]
    if not w_row.empty and not r_row.empty:
        wc = int(w_row['count'].iloc[0]); rc = int(r_row['count'].iloc[0])
        print(f"  {year}: {winner} ({wc}) vs {rival} ({rc}) -> rival x{rc/wc:.1f}")
# line 75
