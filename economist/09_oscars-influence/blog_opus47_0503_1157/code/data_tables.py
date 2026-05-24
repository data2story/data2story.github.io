"""Build chart-ready data tables and dump them as JSON for analyst.json."""
import pandas as pd
import json

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/09_oscars-influence/movie-counts.csv'
df = pd.read_csv(DATA, encoding='latin-1')

# Filter to oscars_year <= 2016 (per Economist's own scope) for stories about BP winners
out = {}

# T1: Best Picture winners over time — full series of (year, share, count, year_rank)
winners = df[df['result'] == 'W'].sort_values('oscars_year')
out['t_winner_series'] = {
    'columns': ['oscars_year', 'movie_name', 'annual_share_pct', 'count', 'year_rank'],
    'rows': [
        [int(r['oscars_year']), r['movie_name'], round(float(r['annual_share'])*100, 2), int(r['count']), int(r['year_rank'])]
        for _, r in winners.iterrows()
    ]
}

# T2: Decade summary — mean share, median rank, % top1, % top10
winners = winners.copy()
winners['decade'] = (winners['oscars_year'] // 10) * 10
dec = winners.groupby('decade').agg(
    n=('movie_name', 'count'),
    mean_share=('annual_share', 'mean'),
    median_share=('annual_share', 'median'),
    median_rank=('year_rank', 'median'),
    pct_top1=('year_rank', lambda s: (s == 1).mean() * 100),
    pct_top10=('year_rank', lambda s: (s <= 10).mean() * 100),
).reset_index()
out['t_decade_summary'] = {
    'columns': ['decade', 'n', 'mean_share_pct', 'median_share_pct', 'median_rank', 'pct_top1', 'pct_top10'],
    'rows': [
        [int(r['decade']), int(r['n']), round(float(r['mean_share'])*100, 2), round(float(r['median_share'])*100, 2),
         float(r['median_rank']), round(float(r['pct_top1']), 1), round(float(r['pct_top10']), 1)]
        for _, r in dec.iterrows()
    ]
}

# T3: For every year, both BP winner and the year's #1 most-referenced film
top1 = df[df['year_rank'] == 1].copy()
yrs = sorted(set(winners['oscars_year']))
rows = []
for y in yrs:
    w = winners[winners['oscars_year'] == y].iloc[0]
    t = top1[top1['oscars_year'] == y]
    if t.empty:
        continue
    t = t.iloc[0]
    rows.append([
        int(y),
        w['movie_name'], round(float(w['annual_share'])*100, 2), int(w['count']),
        t['movie_name'], round(float(t['annual_share'])*100, 2), int(t['count']),
        bool(w['movie_name'] == t['movie_name'])
    ])
out['t_winner_vs_top1'] = {
    'columns': ['oscars_year', 'winner_name', 'winner_share_pct', 'winner_count',
                'top1_name', 'top1_share_pct', 'top1_count', 'winner_is_top1'],
    'rows': rows
}

# T4: Recent era (2007-2016) detail — BP winner + top-3 most-referenced films per year
recent_rows = []
for y in range(2007, 2017):
    sub = df[df['oscars_year'] == y].sort_values('count', ascending=False)
    bp = sub[sub['result'] == 'W']
    if bp.empty:
        continue
    bp_row = bp.iloc[0]
    top3 = sub.head(3)
    top3_list = [{'name': r['movie_name'], 'count': int(r['count']),
                  'result': (r['result'] if isinstance(r['result'], str) else 'X')}
                 for _, r in top3.iterrows()]
    recent_rows.append({
        'year': int(y),
        'bp_winner': bp_row['movie_name'],
        'bp_count': int(bp_row['count']),
        'bp_rank': int(bp_row['year_rank']),
        'bp_share_pct': round(float(bp_row['annual_share'])*100, 2),
        'top3': top3_list,
    })
out['t_recent_detail'] = recent_rows

# T5: Top 20 most-referenced films overall (anchor list)
top20 = df.sort_values('count', ascending=False).head(20)
out['t_top20_overall'] = {
    'columns': ['movie_name', 'release_year', 'oscars_year', 'result', 'count', 'annual_share_pct'],
    'rows': [
        [r['movie_name'], int(r['release_year']), int(r['oscars_year']),
         (r['result'] if isinstance(r['result'], str) else None),
         int(r['count']), round(float(r['annual_share'])*100, 2)]
        for _, r in top20.iterrows()
    ]
}

# T6: Notable BP-winner vs unnominated rival pairs
pairs = [
    (1977, 'Annie Hall', 'Star Wars: Episode IV - A New Hope'),
    (1980, 'Ordinary People', 'Star Wars: Episode V - The Empire Strikes Back'),
    (1960, 'The Apartment', 'Psycho'),
    (1968, 'Oliver!', '2001: A Space Odyssey'),
    (1994, 'Forrest Gump', 'Pulp Fiction'),
    (1989, 'Driving Miss Daisy', 'Batman'),
    (1985, 'Out of Africa', 'Back to the Future'),
    (1984, 'Amadeus', 'The Terminator'),
    (1993, "Schindler's List", 'Jurassic Park'),
    (2008, 'Slumdog Millionaire', 'The Dark Knight'),
    (2015, 'Spotlight', 'Star Wars: Episode VII - The Force Awakens'),
    (2016, 'Moonlight', 'Batman v Superman: Dawn of Justice'),
]
pair_rows = []
for year, winner, rival in pairs:
    w_row = df[(df['oscars_year']==year) & (df['movie_name']==winner)]
    r_row = df[(df['oscars_year']==year) & (df['movie_name']==rival)]
    if r_row.empty:
        r_row = df[(df['release_year']==year) & (df['movie_name']==rival)]
    if w_row.empty or r_row.empty:
        continue
    pair_rows.append([
        int(year),
        winner, int(w_row['count'].iloc[0]),
        rival, int(r_row['count'].iloc[0]),
        round(int(r_row['count'].iloc[0]) / int(w_row['count'].iloc[0]), 2)
    ])
out['t_iconic_pairs'] = {
    'columns': ['year', 'bp_winner', 'winner_count', 'rival', 'rival_count', 'rival_x_factor'],
    'rows': pair_rows
}

# T7: BP winner share-of-top-100 cultural footprint by decade
df['decade'] = (df['oscars_year'] // 10) * 10
by_dec = df.groupby('decade').apply(lambda g: pd.Series({
    'total_count': int(g['count'].sum()),
    'bp_winner_count': int(g.loc[g['result']=='W','count'].sum()),
}), include_groups=False).reset_index()
by_dec['bp_winner_share_pct'] = (by_dec['bp_winner_count'] / by_dec['total_count'] * 100).round(2)
out['t_winner_share_of_top100_by_decade'] = {
    'columns': ['decade', 'total_count', 'bp_winner_count', 'bp_winner_share_pct'],
    'rows': [
        [int(r['decade']), int(r['total_count']), int(r['bp_winner_count']), float(r['bp_winner_share_pct'])]
        for _, r in by_dec.iterrows()
    ]
}

with open('/Users/forrest/Desktop/data2blog/project/economist/09_oscars-influence/blog_opus47_0503_1157/code/data_tables.json', 'w') as f:
    json.dump(out, f, indent=2)

# Quick sanity print
print(f"Wrote {len(out)} tables.")
for k, v in out.items():
    if isinstance(v, dict) and 'rows' in v:
        print(f"  {k}: {len(v['rows'])} rows")
    elif isinstance(v, list):
        print(f"  {k}: {len(v)} entries")
