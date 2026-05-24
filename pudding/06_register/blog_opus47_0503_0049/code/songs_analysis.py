"""Per-song analyses: extreme registers, top-of-chart skew, year-by-year sample."""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/06_register/data"
songs = pd.read_csv(os.path.join(DATA_DIR, "songs.csv"))

# --- ana_register_dist: full distribution of register across 60 years ---
print("=== ana_register_dist ===")
print("Total songs:", len(songs))
dist = songs['register'].value_counts().sort_index()
total = len(songs)
print("Register histogram:")
for r, c in dist.items():
    print(f"  {r}: {c} ({c/total*100:.1f}%)")
# How many are register 10?
r10 = songs[songs['register']==10]
print(f"register == 10: {len(r10)} songs across {r10['year'].nunique()} years")
print("years with at least one register-10:")
print(r10['year'].value_counts().sort_index().to_string())

# --- ana_register10_examples: which songs scored a 10? ---
print("=== ana_register10_examples ===")
r10_top = r10.sort_values(['year','peak_rank']).head(40)
print(r10_top[['song_title','year','peak_rank','points']].to_string(index=False))

# --- ana_register2_examples: which songs scored a 2? ---
print("=== ana_register2_examples ===")
r2 = songs[songs['register']==2]
print(f"register == 2: {len(r2)} songs")
print(r2.sort_values(['year','peak_rank']).head(15)[['song_title','year','peak_rank']].to_string(index=False))

# --- ana_top10_by_year: best-performing male-led songs and their register ---
print("=== ana_top10_by_year ===")
# Songs that hit #1
no1 = songs[songs['peak_rank']==1].sort_values(['year'])
print(f"songs that hit #1: {len(no1)}")
print("their mean register:", round(no1['register'].mean(),3))
print("year-by-year #1 songs (sample of first/last 10):")
print(no1.head(10)[['song_title','year','register']].to_string(index=False))
print("...")
print(no1.tail(10)[['song_title','year','register']].to_string(index=False))

# --- ana_2019_top_examples: 2019 male-led top-10 songs by register ---
print("=== ana_2019_top_examples ===")
y2019_songs = songs[songs['year']==2019].sort_values('peak_rank')
top10_2019 = y2019_songs[y2019_songs['peak_rank']<=10]
print(f"2019 top-10 male-led: {len(top10_2019)} songs")
print(top10_2019[['song_title','register','peak_rank','points']].to_string(index=False))
print("their mean register:", round(top10_2019['register'].mean(),3))
print("share of 2019 top-10 with register >= 7:")
hi = top10_2019[top10_2019['register']>=7]
print(f"  {len(hi)} of {len(top10_2019)} = {len(hi)/len(top10_2019)*100:.0f}%")

# --- ana_register_share_by_year: share of register>=8 over time ---
print("=== ana_register_share_by_year ===")
songs['hi'] = (songs['register']>=8).astype(int)
yearly = songs.groupby('year').agg(n=('register','size'),
                                   mean=('register','mean'),
                                   pct_hi=('hi','mean')).reset_index()
yearly['pct_hi'] = yearly['pct_hi']*100
print("first 5:")
print(yearly.head().to_string(index=False))
print("last 10:")
print(yearly.tail(10).to_string(index=False))
print("years with pct_hi > 30%:")
print(yearly[yearly['pct_hi']>30].to_string(index=False))

# --- ana_register10_share_top10: how many year-#1s scored 9 or 10? ---
print("=== ana_register10_share_top10 ===")
top10_all = songs[songs['peak_rank']<=10]
top10_yearly = top10_all.groupby('year').agg(n=('register','size'),
                                              mean=('register','mean'),
                                              n9plus=('register', lambda s: (s>=9).sum())).reset_index()
top10_yearly['pct9plus'] = top10_yearly['n9plus']/top10_yearly['n']*100
print("Top-10 share with register >= 9 by decade:")
top10_yearly['decade'] = (top10_yearly['year']//10)*10
print(top10_yearly.groupby('decade')[['mean','pct9plus']].mean().round(2))
print("Years with highest top-10 mean (top 10):")
print(top10_yearly.sort_values('mean', ascending=False).head(10).to_string(index=False))
