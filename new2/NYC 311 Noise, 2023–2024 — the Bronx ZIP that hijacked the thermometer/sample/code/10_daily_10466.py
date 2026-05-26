"""10_daily_10466.py — full 366-day daily complaint series for ZIP 10466 in 2024.

The sonification + scrubber visual in edt_06 needs the daily series, not
just the top-10 single days that ana_25 contains. This script emits the
full year as the data_table backing ana_26.

Produces: ana_26 (10466 full 366-day daily series for 2024).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")
df["created_date"] = pd.to_datetime(df["created_date"])

z = df[(df["incident_zip"] == "10466") & (df["created_date"].dt.year == 2024)]
daily = z.groupby(z["created_date"].dt.normalize()).size()
all_2024 = pd.date_range("2024-01-01", "2024-12-31", freq="D")
daily = daily.reindex(all_2024, fill_value=0).astype(int)

# --- ana_26: ZIP 10466 daily complaints, full year 2024 ---
print("=== ana_26 ===")
print(f"days covered: {len(daily)}")
print(f"min:    {daily.min()}  on {daily.idxmin().date()}")
print(f"max:    {daily.max()}  on {daily.idxmax().date()}")
print(f"median: {int(daily.median())}")
print(f"mean:   {daily.mean():.1f}")
print(f"days ≥ 1000:  {(daily >= 1000).sum()}")
print(f"days ≥ 3000:  {(daily >= 3000).sum()}")
print(f"sum (2024 total for 10466): {int(daily.sum()):,}")

# also write a JSON the analyst.json data_table can be cross-checked against
import json
out = Path(__file__).parent / "_10466_daily_2024.json"
out.write_text(json.dumps({
    "columns": ["date", "complaints"],
    "rows": [[d.strftime("%Y-%m-%d"), int(c)] for d, c in daily.items()],
}))
print(f"wrote {out.name}: {out.stat().st_size:,} bytes")
