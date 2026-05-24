"""Calendar heatmap data + time-of-day analysis."""
import pandas as pd

DATA_PATH = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/06_winter-olympics-2026/schedule.csv"
df = pd.read_csv(DATA_PATH)
df['start_dt_local'] = pd.to_datetime(df['start_datetime_local'])
df['hour'] = df['start_dt_local'].dt.hour

# --- ana_06: events per day (calendar heatmap source) ---
print("=== ana_06 ===")
daily = df.groupby('date').agg(
    total=('event_code','count'),
    medal=('is_medal_event','sum'),
    training=('is_training','sum'),
).reset_index()
daily['competition'] = daily['total'] - daily['training']
daily['day_of_week'] = pd.to_datetime(daily['date']).dt.day_name()
print(daily.to_string(index=False))
print(f"\nPeak medal day: {daily.loc[daily['medal'].idxmax(),'date']} ({daily['medal'].max()} medals)")
print(f"Peak total day: {daily.loc[daily['total'].idxmax(),'date']} ({daily['total'].max()} events)")

# --- ana_07: medal events by day of week ---
print("\n=== ana_07 ===")
dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dow = df.groupby('day_of_week').agg(
    total=('event_code','count'),
    medal=('is_medal_event','sum'),
).reindex(dow_order).reset_index()
print(dow.to_string(index=False))

# --- ana_08: start hour distribution (local Italian time) ---
print("\n=== ana_08 ===")
hr = df.groupby('hour').agg(
    total=('event_code','count'),
    medal=('is_medal_event','sum'),
).reset_index()
hr['non_medal'] = hr['total'] - hr['medal']
print(hr.to_string(index=False))
print(f"\nMedal events peak hour: {hr.loc[hr['medal'].idxmax(),'hour']}h with {hr['medal'].max()} medals")

# --- ana_09: prime-time alignment to NBC US prime ---
print("\n=== ana_09 ===")
# NBC primetime "afternoon": 14:00-17:00 ET = 20:00-23:00 CET local
# NBC primetime evening: 20:00-23:00 ET = next-day 02:00-05:00 CET (live)
# Best slot for *live* US prime audience = 14:00-17:00 ET = 20:00-23:00 local Italian
medal_df = df[df['is_medal_event']==True].copy()
prime_window = medal_df[(medal_df['hour']>=18) & (medal_df['hour']<=21)]
afternoon = medal_df[(medal_df['hour']>=10) & (medal_df['hour']<13)]
morning = medal_df[(medal_df['hour']<10)]
print(f"Medal events 18:00-21:59 local (= afternoon US ET): {len(prime_window)} ({len(prime_window)/len(medal_df)*100:.1f}%)")
print(f"Medal events 10:00-12:59 local (= dawn US ET): {len(afternoon)} ({len(afternoon)/len(medal_df)*100:.1f}%)")
print(f"Medal events <10:00 local: {len(morning)} ({len(morning)/len(medal_df)*100:.1f}%)")

# --- ana_10: hour x is_medal heatmap source ---
print("\n=== ana_10 ===")
heat = df.groupby(['date','hour']).size().reset_index(name='count')
heat_med = df[df['is_medal_event']==True].groupby(['date','hour']).size().reset_index(name='count')
print(f"Calendar-hour cells (date×hour): {len(heat)}")
print("Top 10 cells by total events:")
print(heat.nlargest(10, 'count').to_string(index=False))
