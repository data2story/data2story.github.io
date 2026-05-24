"""Venue load + geographic clustering."""
import pandas as pd

DATA_PATH = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/06_winter-olympics-2026/schedule.csv"
df = pd.read_csv(DATA_PATH)

# Approximate lat/long for each venue cluster
VENUES = {
    "Milano Ice Skating Arena": ("Milan", 45.46, 9.19),
    "Milano Rho Ice Hockey Arena": ("Milan", 45.52, 9.05),
    "Milano Santagiulia Ice Hockey Arena": ("Milan", 45.43, 9.24),
    "Milano Speed Skating Stadium": ("Milan", 45.46, 9.19),
    "Cortina Curling Olympic Stadium": ("Cortina", 46.54, 12.13),
    "Cortina Sliding Centre": ("Cortina", 46.54, 12.13),
    "Tofane Alpine Skiing Centre": ("Cortina", 46.55, 12.10),
    "Anterselva Biathlon Arena": ("Anterselva", 46.85, 12.10),
    "Stelvio Ski Centre": ("Bormio", 46.47, 10.37),
    "Livigno Snow Park": ("Livigno", 46.54, 10.13),
    "Livigno Aerials & Moguls Park": ("Livigno", 46.54, 10.14),
    "Tesero Cross-Country Skiing Stadium": ("Val di Fiemme", 46.29, 11.51),
    "Predazzo Ski Jumping Stadium": ("Val di Fiemme", 46.31, 11.60),
}

# --- ana_11: events per venue ---
print("=== ana_11 ===")
v = df.groupby('venue_name').agg(
    total=('event_code','count'),
    medal=('is_medal_event','sum'),
    days=('date', 'nunique'),
).sort_values('total', ascending=False)
print(v.to_string())
print(f"\nVenue NA count: {df['venue_name'].isna().sum()}")
print(f"Top venue: {v.index[0]} with {v.iloc[0]['total']} sessions")

# --- ana_12: events per cluster (Milan / Cortina / Bormio / Livigno / etc) ---
print("\n=== ana_12 ===")
df['cluster'] = df['venue_name'].map(lambda x: VENUES.get(x, (None,))[0])
cl = df.groupby('cluster').agg(
    total=('event_code','count'),
    medal=('is_medal_event','sum'),
    venues=('venue_name','nunique'),
).sort_values('total', ascending=False)
print(cl.to_string())

# --- ana_13: medal-event vs total split, per cluster ---
print("\n=== ana_13 ===")
cl['medal_pct'] = (cl['medal']/cl['total']*100).round(1)
print(cl.to_string())

# --- ana_14: 'NA' / placeholder venue rows ---
print("\n=== ana_14 ===")
na_rows = df[df['venue_name'].isna()]
print(f"Rows with missing venue: {len(na_rows)}")
print(na_rows['discipline_name'].value_counts().head(5))
print(na_rows[['date','discipline_name','event_description','venue_code']].head(10).to_string(index=False))
