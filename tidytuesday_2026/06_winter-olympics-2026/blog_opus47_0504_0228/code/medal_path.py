"""Sankey-style medal-path data: cluster -> discipline -> medal_event_count."""
import pandas as pd

DATA_PATH = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/06_winter-olympics-2026/schedule.csv"
df = pd.read_csv(DATA_PATH)

VENUES = {
    "Milano Ice Skating Arena": "Milan",
    "Milano Rho Ice Hockey Arena": "Milan",
    "Milano Santagiulia Ice Hockey Arena": "Milan",
    "Milano Speed Skating Stadium": "Milan",
    "Cortina Curling Olympic Stadium": "Cortina",
    "Cortina Sliding Centre": "Cortina",
    "Tofane Alpine Skiing Centre": "Cortina",
    "Anterselva Biathlon Arena": "Anterselva",
    "Stelvio Ski Centre": "Bormio",
    "Livigno Snow Park": "Livigno",
    "Livigno Aerials & Moguls Park": "Livigno",
    "Tesero Cross-Country Skiing Stadium": "Val di Fiemme",
    "Predazzo Ski Jumping Stadium": "Val di Fiemme",
}
df['cluster'] = df['venue_name'].map(VENUES).fillna("Unassigned")

# --- ana_15: cluster -> discipline -> medal events (sankey source) ---
print("=== ana_15 ===")
medals = df[df['is_medal_event']==True]
sankey = medals.groupby(['cluster','discipline_name']).size().reset_index(name='medal_count')
sankey = sankey.sort_values(['cluster','medal_count'], ascending=[True,False])
print(sankey.to_string(index=False))
print(f"\nTotal medal events: {sankey['medal_count'].sum()}")

# --- ana_16: schedule density - first half vs second half ---
print("\n=== ana_16 ===")
df['date_dt'] = pd.to_datetime(df['date'])
mid = pd.Timestamp('2026-02-13')
first = df[df['date_dt'] < mid]
second = df[df['date_dt'] >= mid]
print(f"First half (Feb 4-12): {len(first)} events, {first['is_medal_event'].sum()} medal")
print(f"Second half (Feb 13-22): {len(second)} events, {second['is_medal_event'].sum()} medal")
print(f"Medal-share first: {first['is_medal_event'].mean()*100:.1f}%")
print(f"Medal-share second: {second['is_medal_event'].mean()*100:.1f}%")

# --- ana_17: Closing weekend (Feb 21-22) sprint to finish ---
print("\n=== ana_17 ===")
final2 = df[df['date'].isin(['2026-02-21','2026-02-22'])]
print(f"Final 2 days: {len(final2)} events, {final2['is_medal_event'].sum()} medal")
print(final2.groupby('date')['is_medal_event'].sum())
print("\nClosing-day medals by discipline:")
print(final2[final2['is_medal_event']==True].groupby('discipline_name').size().sort_values(ascending=False).to_string())

# --- ana_18: estimated_start flag rate ---
print("\n=== ana_18 ===")
est = df['estimated_start'].sum()
print(f"Sessions with estimated_start=TRUE: {est} ({est/len(df)*100:.1f}%)")
print(df.groupby('discipline_name')['estimated_start'].sum().sort_values(ascending=False).head(10))

# --- ana_19: longest single session ---
print("\n=== ana_19 ===")
df['start_dt'] = pd.to_datetime(df['start_datetime_utc'])
df['end_dt'] = pd.to_datetime(df['end_datetime_utc'])
df['dur_min'] = (df['end_dt']-df['start_dt']).dt.total_seconds()/60
longest = df.nlargest(5,'dur_min')[['date','discipline_name','event_description','venue_name','dur_min']]
print(longest.to_string(index=False))

# --- ana_20: gender split in event_description ---
print("\n=== ana_20 ===")
def gender(s):
    s = str(s).lower()
    if "men's" in s or "men " in s:
        if "women's" in s or "women " in s: return "mixed"
        return "men"
    if "women's" in s or "women " in s: return "women"
    if "mixed" in s: return "mixed"
    return "other"
df['gender'] = df['event_description'].apply(gender)
print(df.groupby('gender').agg(
    total=('event_code','count'),
    medal=('is_medal_event','sum'),
).to_string())
