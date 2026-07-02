"""
profile_data.py — Dataset profiling for the space-launches story.
Run from DATA_DIR (or anywhere; uses an explicit DATA_DIR path resolved relative to repo).
Profiles launches.csv (5726 data rows) + agencies.csv (74 data rows).
This is a profiling/inventory script — findings live in analyze.py.
"""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:/AI/journalist agent review/phase2/datasets/journals/Economist/data/2018-10-20_space-launches",
)

launches = pd.read_csv(os.path.join(DATA_DIR, "launches.csv"))
agencies = pd.read_csv(os.path.join(DATA_DIR, "agencies.csv"))

print("=== SHAPE ===")
print("launches:", launches.shape)
print("agencies:", agencies.shape)

print("\n=== launches dtypes ===")
print(launches.dtypes)

print("\n=== launches missing per column ===")
print(launches.isna().sum())

print("\n=== launch_year range (raw) ===")
print("min:", launches["launch_year"].min(), "max:", launches["launch_year"].max())
print(launches["launch_year"].describe())

print("\n=== state_code value counts (ALL) ===")
print(launches["state_code"].value_counts(dropna=False).to_string())

print("\n=== agency_type value counts ===")
print(launches["agency_type"].value_counts(dropna=False).to_string())

print("\n=== category value counts ===")
print(launches["category"].value_counts(dropna=False).to_string())

print("\n=== agency (launching agency) cardinality ===")
print("n unique agency:", launches["agency"].nunique())
print(launches["agency"].value_counts().head(20).to_string())

print("\n=== type (vehicle) cardinality ===")
print("n unique type:", launches["type"].nunique())
print(launches["type"].value_counts().head(25).to_string())

print("\n=== launch_date typo check (non-parseable / weird years) ===")
ld = pd.to_datetime(launches["launch_date"], errors="coerce")
print("rows where launch_date fails to parse:", ld.isna().sum())
# find raw launch_date strings whose 4-char year-prefix != launch_year (element-wise)
date_str = launches["launch_date"].astype(str)
yr_str = launches["launch_year"].astype(str)
mismatch = [not d.startswith(y) for d, y in zip(date_str, yr_str)]
bad = launches[pd.Series(mismatch, index=launches.index)]
print("rows where launch_date prefix != launch_year (incl. NaN dates):")
print(bad[["tag", "launch_date", "launch_year", "type", "agency", "state_code"]].head(20).to_string())

print("\n=== 2018 rows (partial year check) ===")
y2018 = launches[launches["launch_year"] == 2018]
print("2018 row count:", len(y2018))
m2018 = pd.to_datetime(y2018["launch_date"], errors="coerce").dt.month.value_counts().sort_index()
print("2018 by month (parsed, typo excluded):")
print(m2018.to_string())

print("\n=== agencies.csv columns ===")
print(list(agencies.columns))
print("\n=== agencies agency_type ===")
print(agencies["agency_type"].value_counts(dropna=False).to_string())
print("\n=== agencies with usable lat/long ===")
ag = agencies.copy()
ag["latitude"] = pd.to_numeric(ag["latitude"], errors="coerce")
ag["longitude"] = pd.to_numeric(ag["longitude"], errors="coerce")
geo = ag.dropna(subset=["latitude", "longitude"])
print("agencies rows with numeric lat/long:", len(geo))
print(geo[["agency", "short_name", "state_code", "latitude", "longitude", "agency_type", "count"]].to_string())

print("\n=== agencies.csv 'count' vs fresh launches.csv count (by agency) — top mismatches ===")
fresh = launches["agency"].value_counts().rename("fresh")
ac = agencies.set_index("agency")["count"]
cmp = pd.concat([ac, fresh], axis=1)
cmp["diff"] = cmp["count"] - cmp["fresh"]
print(cmp[cmp["diff"].fillna(0) != 0].sort_values("diff", key=abs, ascending=False).head(20).to_string())
