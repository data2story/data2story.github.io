"""Per-discipline aggregations: total sessions, medal events, training share, NOC count proxy."""
import pandas as pd
import json

DATA_PATH = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/06_winter-olympics-2026/schedule.csv"
df = pd.read_csv(DATA_PATH)

# Detective context: NOC counts per sport (from external research)
NOC_COUNTS = {
    "Alpine Skiing": 80,
    "Biathlon": 40,
    "Bobsleigh": 25,
    "Cross-Country Skiing": 65,
    "Curling": 14,
    "Figure Skating": 40,
    "Freestyle Skiing": 35,
    "Ice Hockey": 12,
    "Luge": 22,
    "Nordic Combined": 14,
    "Short Track Speed Skating": 22,
    "Skeleton": 20,
    "Ski Jumping": 22,
    "Ski Mountaineering": 13,
    "Snowboard": 30,
    "Speed Skating": 25,
}

# --- ana_01: sessions per discipline ---
print("=== ana_01 ===")
sess = df.groupby("discipline_name").size().sort_values(ascending=False)
print(sess.to_string())
print(f"Total: {sess.sum()}")

# --- ana_02: medal events per discipline ---
print("\n=== ana_02 ===")
medals = df[df['is_medal_event']==True].groupby("discipline_name").size().sort_values(ascending=False)
print(medals.to_string())
print(f"Total medal events: {medals.sum()}")

# --- ana_03: training vs competition split ---
print("\n=== ana_03 ===")
trn = df.groupby(['discipline_name','is_training']).size().unstack(fill_value=0)
trn.columns = ['competition','training']
trn['training_pct'] = (trn['training']/(trn['training']+trn['competition'])*100).round(1)
trn = trn.sort_values('training_pct', ascending=False)
print(trn.to_string())
overall_train = (df['is_training'].sum() / len(df) * 100)
overall_medal = (df['is_medal_event'].sum() / len(df) * 100)
print(f"\nOverall training share: {overall_train:.1f}%")
print(f"Overall medal-event share: {overall_medal:.1f}%")

# --- ana_04: medal density (medals per NOC competing) — "easiest" gold ---
print("\n=== ana_04 ===")
density = pd.DataFrame({
    'discipline_name': list(NOC_COUNTS.keys()),
    'noc_count': list(NOC_COUNTS.values()),
})
medals_df = medals.reset_index()
medals_df.columns = ['discipline_name','medal_events']
density = density.merge(medals_df, on='discipline_name', how='left').fillna(0)
density['medals_per_noc'] = (density['medal_events']/density['noc_count']).round(3)
density = density.sort_values('medals_per_noc', ascending=False)
print(density.to_string(index=False))

# --- ana_05: average session duration (minutes) by discipline, competition only ---
print("\n=== ana_05 ===")
df['start_dt'] = pd.to_datetime(df['start_datetime_utc'])
df['end_dt'] = pd.to_datetime(df['end_datetime_utc'])
df['dur_min'] = (df['end_dt']-df['start_dt']).dt.total_seconds()/60
comp = df[df['is_training']==False].groupby('discipline_name')['dur_min'].agg(['mean','median','count']).round(1)
comp = comp.sort_values('mean', ascending=False)
print(comp.to_string())
overall_dur = df['dur_min'].mean()
print(f"\nOverall mean duration: {overall_dur:.1f} min")
