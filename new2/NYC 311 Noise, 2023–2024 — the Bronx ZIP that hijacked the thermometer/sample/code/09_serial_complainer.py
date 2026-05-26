"""09_serial_complainer.py — ZIP 10466 deep dive.

Wakefield/Williamsbridge in the Bronx (ZIP 10466) accounts for 76,380
complaints, the most of any zip in NYC. Its 2024 volume is 7.7x its 2023
volume, almost all came from the mobile app, and its single noisiest day
(2024-09-15) had 4,952 complaints — one every 17 seconds for 24 hours
straight. This is almost certainly an organized mass-complaint event or a
small group spamming the app.

Produces: ana_24 (10466 totals + YoY), ana_25 (10466 single-day extremes
+ channel of those complaints).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")
df["created_date"] = pd.to_datetime(df["created_date"])

z = df[df["incident_zip"] == "10466"].copy()
z["year"] = z["created_date"].dt.year
z["day"] = z["created_date"].dt.normalize()

# --- ana_24: 10466 totals, YoY, top descriptors ---
print("=== ana_24 ===")
print(f"ZIP 10466 (Wakefield / Williamsbridge, Bronx) — 2-year total: {len(z):,}")
yc = z["year"].value_counts().sort_index()
print(f"  2023: {int(yc.get(2023,0)):,}")
print(f"  2024: {int(yc.get(2024,0)):,}")
ratio = yc.get(2024,0) / max(yc.get(2023,1), 1)
print(f"  ratio: {ratio:.2f}x")
desc_top = z["descriptor"].value_counts().head(5)
total_z = len(z)
print(f"Top descriptors for 10466:")
for d, c in desc_top.items():
    print(f"  {c:>6,}  {100*c/total_z:>5.2f}%  {d}")

# Compare 10466 share against city for 2024 specifically
city_2024 = len(df[df["created_date"].dt.year == 2024])
z_2024 = int(yc.get(2024, 0))
print(f"\nIn 2024, 10466 alone is {z_2024:,} of {city_2024:,} citywide complaints = {100*z_2024/city_2024:.2f}% — one zip with ~62k residents made up this share of all NYC noise complaints.")

# --- ana_25: 10466 noisiest single days + channel ---
print("=== ana_25 ===")
daily_z = z.groupby("day").size()
top10 = daily_z.nlargest(10)
print(f"10466 single-day top 10:")
for d, c in top10.items():
    sub = z[z["day"] == d]
    by_ch = sub["open_data_channel_type"].value_counts()
    mobile = int(by_ch.get("MOBILE", 0))
    online = int(by_ch.get("ONLINE", 0))
    phone = int(by_ch.get("PHONE", 0))
    print(f"  {d.date()}  total={c:>5,}   mobile={mobile:>5,}  online={online:>4,}  phone={phone:>4,}")

# Rate metric: on the Sep 15 spike day, complaints per second
peak_day = top10.idxmax()
peak_count = int(top10.iloc[0])
seconds = 86400
rate = peak_count / seconds
print(f"\nOn {peak_day.date()}, 10466 logged {peak_count:,} complaints in 24h — one every {seconds/peak_count:.1f} seconds.")

# Median complaints per day in 10466 vs every other day
median_z = daily_z.median()
print(f"\n10466 median complaints per day:    {median_z:.0f}")
print(f"10466 mean   complaints per day:    {daily_z.mean():.0f}")
print(f"10466 days above 1000 complaints:   {(daily_z > 1000).sum()}")
print(f"10466 days above 2000 complaints:   {(daily_z > 2000).sum()}")
print(f"10466 days above 3000 complaints:   {(daily_z > 3000).sum()}")
