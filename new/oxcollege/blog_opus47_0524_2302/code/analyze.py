import pandas as pd
import numpy as np
import os, re

DATA = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data', 'oxcollege')
df = pd.read_csv(os.path.join(DATA, 'oxford_colleges.csv'))
cen = pd.read_csv(os.path.join(DATA, 'colleges_by_century.csv'))

# Defunct / non-current set (per README caveats)
DEFUNCT = {
    'Rewley Abbey', 'Gloucester College', 'Durham College', 'Canterbury College',
    'St Mary\'s College', 'Cardinal College', "King Henry VIII's College",
    'Greek College', 'Templeton College', 'Examination Schools', 'St Bernard\'s College, Oxford'
}

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"rows={len(df)} cols={len(df.columns)} cols={list(df.columns)}")
print(f"founded_year range: {df['founded_year'].min()} -> {df['founded_year'].max()}")
print("missing per column:")
print(df.isna().sum())
print(f"blank founded_year: {df['founded_year'].isna().sum()} -> {list(df[df['founded_year'].isna()]['college'])}")

# --- ana_02: Foundations per century (trend) ---
print("=== ana_02 ===")
print(cen.to_string(index=False))

# --- ana_03: The oldest-college trio ---
print("=== ana_03 ===")
oldest = df.dropna(subset=['founded_year']).sort_values('founded_year').head(6)
print(oldest[['college', 'founded_year', 'founder']].to_string(index=False))

# --- ana_04: Span and gaps between foundations ---
print("=== ana_04 ===")
yrs = df.dropna(subset=['founded_year']).copy()
yrs['founded_year'] = yrs['founded_year'].astype(int)
span = yrs['founded_year'].max() - yrs['founded_year'].min()
print(f"earliest={yrs['founded_year'].min()} latest={yrs['founded_year'].max()} span={span} years")
yrs_sorted = yrs.sort_values('founded_year')
gaps = yrs_sorted['founded_year'].diff()
big = yrs_sorted.assign(gap=gaps).nlargest(5, 'gap')[['college', 'founded_year', 'gap']]
print("largest gaps before a foundation:")
print(big.to_string(index=False))

# --- ana_05: Current vs defunct/merged colleges ---
print("=== ana_05 ===")
df['status'] = df['college'].apply(lambda c: 'defunct/merged' if c in DEFUNCT else 'current')
print(df['status'].value_counts())
print("defunct/merged list:")
print(df[df['status']=='defunct/merged'][['college','founded_year']].to_string(index=False))

# --- ana_06: Founder counts (split multi-founder) ---
print("=== ana_06 ===")
founders = []
for f in df['founder'].dropna():
    for part in str(f).split(';'):
        founders.append(part.strip())
fc = pd.Series(founders).value_counts()
print(f"colleges with a recorded founder: {df['founder'].notna().sum()} / {len(df)}")
print(f"distinct founders: {fc.size}")
print(fc[fc>1].to_string())
print("Wolsey & Henry VIII appear in:")
for name in ['Thomas Wolsey','Henry VIII of England']:
    rows = df[df['founder'].fillna('').str.contains(name, regex=False)]['college'].tolist()
    print(f"  {name}: {rows}")

# --- ana_07: Namesake themes (religious vs personal) ---
print("=== ana_07 ===")
relig_terms = ['Mary','Jesus','John the Baptist','All Souls','Holy Trinity','Saint','St ','Hugh','Hilda','Catherine','Peter','Anne','Edmund','Cross','Anthony','Christ']
named = df.dropna(subset=['named_after']).copy()
def theme(x):
    return 'religious/saint' if any(t in x for t in relig_terms) else 'person/place'
named['theme'] = named['named_after'].apply(theme)
print(f"colleges with named_after: {df['named_after'].notna().sum()} / {len(df)}")
print(named['theme'].value_counts())
# by era
named = named.merge(df[['college','founded_year']], on='college', suffixes=('','_y'))
named['era'] = named['founded_year'].apply(lambda y: 'pre-1600' if pd.notna(y) and y<1600 else ('1600-1899' if pd.notna(y) and y<1900 else 'modern (1900+)'))
print(pd.crosstab(named['era'], named['theme']))

# --- ana_08: Founding rate by half-century / waves ---
print("=== ana_08 ===")
yrs['century'] = ((yrs['founded_year']-1)//100 + 1).astype(int)
# waves defined by README
def wave(y):
    if y < 1500: return 'Medieval (1201-1499)'
    if y < 1600: return 'Reformation era (1500-1599)'
    if y < 1800: return 'Quiet centuries (1600-1799)'
    return 'Modern expansion (1800-2019)'
yrs['wave'] = yrs['founded_year'].apply(wave)
wv = yrs.groupby('wave').agg(count=('college','size'), span=('founded_year', lambda s: f"{s.min()}-{s.max()}"))
print(wv.to_string())

# --- ana_09: Website presence as a proxy for survival ---
print("=== ana_09 ===")
df['has_site'] = df['website'].notna()
print(pd.crosstab(df['status'], df['has_site']))

# --- ana_10: Decade-level modern boom 1870-2019 ---
print("=== ana_10 ===")
modern = yrs[yrs['founded_year']>=1800].copy()
modern['decade'] = (modern['founded_year']//10*10).astype(int)
dc = modern.groupby('decade').size()
print(dc.to_string())
print(f"modern foundations 1800+: {len(modern)}")
