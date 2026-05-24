"""Yearly trend analyses: all songs vs top-10, peaks, recent acceleration."""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/06_register/data"

songs = pd.read_csv(os.path.join(DATA_DIR, "songs.csv"))
avg = pd.read_csv(os.path.join(DATA_DIR, "avg.csv")).rename(columns={'avg(register)': 'avg'})
avg_top = pd.read_csv(os.path.join(DATA_DIR, "avg_top.csv"))

# --- ana_year_avg: Yearly average register, all male-led Hot 100 hits ---
print("=== ana_year_avg ===")
print("avg.csv n years:", len(avg))
avg_sorted = avg.sort_values('year').reset_index(drop=True)
print("first 5:")
print(avg_sorted.head())
print("last 5:")
print(avg_sorted.tail())
print("min year + value:", avg_sorted.loc[avg_sorted['avg'].idxmin()].to_dict())
print("max year + value:", avg_sorted.loc[avg_sorted['avg'].idxmax()].to_dict())
print("2019 value:", avg_sorted[avg_sorted['year']==2019]['avg'].iloc[0])
print("range:", avg_sorted['avg'].min(), "to", avg_sorted['avg'].max())

# --- ana_year_top10: Yearly average register, top-10 hits only ---
print("=== ana_year_top10 ===")
top_sorted = avg_top.sort_values('year').reset_index(drop=True)
print("first 5:")
print(top_sorted.head())
print("last 5:")
print(top_sorted.tail())
print("min year + value:", top_sorted.loc[top_sorted['avg'].idxmin()].to_dict())
print("max year + value:", top_sorted.loc[top_sorted['avg'].idxmax()].to_dict())
print("2019 top-10 value:", top_sorted[top_sorted['year']==2019]['avg'].iloc[0])
# Is 2019 the highest?
print("Years where top-10 avg >= 2019 value:")
v2019 = top_sorted[top_sorted['year']==2019]['avg'].iloc[0]
print(top_sorted[top_sorted['avg'] >= v2019])
# Years where top-10 avg >= 7
print("Years where top-10 avg >= 7:")
print(top_sorted[top_sorted['avg'] >= 7])

# --- ana_top10_vs_all_gap: Gap between top-10 register and all-songs register ---
print("=== ana_top10_vs_all_gap ===")
combined = avg_sorted.merge(top_sorted, on='year', suffixes=('_all', '_top10'))
combined['gap'] = combined['avg_top10'] - combined['avg_all']
print(combined.tail(10))
print("max gap:", combined.loc[combined['gap'].idxmax()].to_dict())
print("min gap (most negative):", combined.loc[combined['gap'].idxmin()].to_dict())
print("2019 gap:", combined[combined['year']==2019].iloc[0].to_dict())

# --- ana_year_peak1988: 1988 hair-metal peak (all-songs series) ---
print("=== ana_year_peak1988 ===")
print("All-songs series sorted by avg, top 10:")
print(avg_sorted.nlargest(10, 'avg').to_string(index=False))
# Songs from 1988
s1988 = songs[songs['year']==1988]
print("1988 song count:", len(s1988))
print("1988 mean register:", s1988['register'].mean())
print("1988 register dist:")
print(s1988['register'].value_counts().sort_index())

# --- ana_recent_decade: 2010s rapid rise back from a trough ---
print("=== ana_recent_decade ===")
print("Decade means (all-songs series):")
avg_sorted['decade'] = (avg_sorted['year'] // 10) * 10
print(avg_sorted.groupby('decade')['avg'].agg(['mean','min','max','count']))
print("Top-10 by decade:")
top_sorted['decade'] = (top_sorted['year'] // 10) * 10
print(top_sorted.groupby('decade')['avg'].agg(['mean','min','max','count']))
