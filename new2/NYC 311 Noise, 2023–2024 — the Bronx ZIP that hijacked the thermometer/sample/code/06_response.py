"""06_response.py — response time + resolution_description patterns.

Produces: ana_16 (response time by agency / complaint_type),
ana_17 (resolution_description distribution and 'no evidence' share),
ana_18 (NYPD residential — share that closed with 'no evidence').
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")
df["created_date"] = pd.to_datetime(df["created_date"])
df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")
df["response_hours"] = (df["closed_date"] - df["created_date"]).dt.total_seconds() / 3600
closed = df.dropna(subset=["response_hours"]).copy()

# --- ana_16: Response time by agency × top complaint type ---
print("=== ana_16 ===")
# trim crazy negative or absurdly long values (1y) before computing summary stats
clean = closed[(closed["response_hours"] >= 0) & (closed["response_hours"] <= 24 * 365)]
print(f"closed complaints with valid response_hours: {len(clean):,} / {len(df):,}")

# Median + 90th-percentile response time by agency
print("\nResponse-time summary by responding agency (closed cases only):")
agg = (
    clean.groupby("agency", observed=True)["response_hours"]
    .agg(["count", "median", lambda s: s.quantile(0.9)])
    .rename(columns={"<lambda_0>": "p90_h"})
)
agg = agg.sort_values("count", ascending=False)
for ag_label, row in agg.iterrows():
    print(f"  {ag_label:<6}  n={int(row['count']):>9,}  median={row['median']:>8.2f} h  p90={row['p90_h']:>9.2f} h")

print("\nMedian response (h) by complaint_type × agency:")
ct_top = clean["complaint_type"].value_counts().head(8).index
ag_top = clean["agency"].value_counts().head(4).index
sub = clean[clean["complaint_type"].isin(ct_top) & clean["agency"].isin(ag_top)]
pivot = sub.pivot_table(values="response_hours", index="complaint_type", columns="agency", aggfunc="median", observed=True)
pivot = pivot.loc[ct_top]
print(pivot.round(2).to_string())

# --- ana_17: Resolution-description top categories overall ---
print("=== ana_17 ===")
# bucket the long, varied resolution_description text into a few common patterns
rd = df["resolution_description"].fillna("(no resolution text)").astype(str)
total = len(df)
def bucket(s):
    s_low = s.lower()
    if s == "(no resolution text)":
        return "no resolution text"
    if "no evidence of the violation" in s_low:
        return "NYPD: no evidence of violation"
    if "action was not necessary" in s_low or "took action to fix" in s_low or "responded to the complaint and" in s_low:
        return "NYPD: responded, took action / not necessary"
    if "no one was at the location" in s_low or "unable to gain entry" in s_low:
        return "NYPD: nobody home / no entry"
    if "issued a summons" in s_low or "issued a violation" in s_low:
        return "issued a summons or violation"
    if "the issue was already resolved" in s_low or "the condition no longer exists" in s_low:
        return "condition no longer exists"
    if "duplicate of" in s_low:
        return "duplicate complaint"
    if "you may need to provide additional information" in s_low or "we will notify you" in s_low:
        return "DEP: inspector to be assigned"
    if "issued an order" in s_low:
        return "DEP: issued order"
    if "no violation was observed" in s_low or "inspected and no violation" in s_low:
        return "DEP: inspected, no violation observed"
    if "department of environmental protection inspected the complaint" in s_low:
        return "DEP: inspected the complaint"
    return "other (long-tail)"
df["res_bucket"] = rd.apply(bucket)
b_counts = df["res_bucket"].value_counts()
print(f"Resolution bucket distribution ({total:,} rows):")
for label, count in b_counts.items():
    print(f"  {count:>9,}  {100*count/total:>5.2f}%  {label}")

# --- ana_18: NYPD residential — share that closed with 'no evidence' ---
print("=== ana_18 ===")
nypd_res = df[(df["agency"] == "NYPD") & (df["complaint_type"] == "Noise - Residential")]
n = len(nypd_res)
print(f"NYPD residential noise complaints: {n:,}")
b = nypd_res["res_bucket"].value_counts()
for label, count in b.items():
    print(f"  {count:>9,}  {100*count/n:>5.2f}%  {label}")
