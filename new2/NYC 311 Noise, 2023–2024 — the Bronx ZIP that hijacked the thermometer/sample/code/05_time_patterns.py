"""05_time_patterns.py — month, day-of-week, hour-of-day, and the late-June fireworks spike.

Produces: ana_12 (monthly seasonality), ana_13 (day-of-week), ana_14 (hour-of-day),
ana_15 (late-June fireworks pulse).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")
df["created_date"] = pd.to_datetime(df["created_date"])
df["year"] = df["created_date"].dt.year
df["month"] = df["created_date"].dt.month
df["dow"] = df["created_date"].dt.day_name()
df["hour"] = df["created_date"].dt.hour

# --- ana_12: Monthly seasonality ---
print("=== ana_12 ===")
mo = df.groupby(["year", "month"]).size().unstack(level="year").fillna(0).astype(int)
mo.index.name = "month"
print("Complaints per month, 2023 vs 2024 (rows are calendar months):")
print(mo.to_string())

# --- ana_13: Day-of-week pattern ---
print("=== ana_13 ===")
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_counts = df["dow"].value_counts().reindex(order)
total = dow_counts.sum()
print("Complaints by day of the week (2023 + 2024):")
for d, c in dow_counts.items():
    print(f"  {d:<10}  {c:>8,}  {100*c/total:>5.2f}%")

# --- ana_14: Hour-of-day pattern, overall and Fri/Sat-night vs weekday ---
print("=== ana_14 ===")
hr_all = df.groupby("hour").size()
print("Hour-of-day complaint counts (24h, all days):")
for h, c in hr_all.items():
    print(f"  {int(h):>2}:00  {c:>7,}")

print("\nHour-of-day, weekend nights (Fri+Sat) vs weekday nights (Mon-Thu+Sun):")
weekend = df.loc[df["dow"].isin(["Friday", "Saturday"]), "hour"].value_counts().sort_index()
weekday = df.loc[df["dow"].isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Sunday"]), "hour"].value_counts().sort_index()
# Normalise to complaints-per-day
weekend_per_day = weekend / (df.loc[df["dow"].isin(["Friday", "Saturday"]), "created_date"].dt.normalize().nunique())
weekday_per_day = weekday / (df.loc[df["dow"].isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Sunday"]), "created_date"].dt.normalize().nunique())
print(f"  hour   wkday/d   wknd/d   wknd÷wkday")
for h in range(24):
    wd = weekday_per_day.get(h, 0)
    we = weekend_per_day.get(h, 0)
    ratio = we / wd if wd else 0
    print(f"  {h:>2}:00  {wd:>7.0f}   {we:>7.0f}   {ratio:>5.2f}")

# --- ana_15: Late-June fireworks pulse — daily complaints around July 4 ---
print("=== ana_15 ===")
# Look at June 20 → July 8 each year
window_2023 = df[(df["created_date"] >= "2023-06-20") & (df["created_date"] < "2023-07-09")]
window_2024 = df[(df["created_date"] >= "2024-06-20") & (df["created_date"] < "2024-07-09")]
print("Daily complaint count, late-June into July 8, each year:")
print(f"  {'date':<12}  {'2023':>8}  {'date':<12}  {'2024':>8}")
d23 = window_2023.groupby(window_2023["created_date"].dt.normalize()).size()
d24 = window_2024.groupby(window_2024["created_date"].dt.normalize()).size()
days = list(d23.index) if len(d23) else []
for d in days:
    matching_2024 = pd.Timestamp(year=2024, month=d.month, day=d.day)
    c23 = d23.get(d, 0)
    c24 = d24.get(matching_2024, 0)
    print(f"  {d.date()}  {c23:>8,}  {matching_2024.date()}  {c24:>8,}")

# fireworks descriptor share
print("\nFireworks-related descriptors, all years, all months:")
firework_mask = df["descriptor"].astype(str).str.contains("Firework", case=False, na=False)
print(f"  fireworks-tagged complaints: {firework_mask.sum():,}")
fw = df.loc[firework_mask]
fw_month = fw.groupby([fw["created_date"].dt.year, fw["created_date"].dt.month]).size()
print("\nFireworks complaints by year-month (only months with ≥10):")
for (y, m), c in fw_month.items():
    if c >= 10:
        print(f"  {int(y)}-{int(m):02d}: {c:>5,}")
