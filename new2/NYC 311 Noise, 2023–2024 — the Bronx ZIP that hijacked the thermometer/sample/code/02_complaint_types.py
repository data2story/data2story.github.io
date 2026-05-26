"""02_complaint_types.py — complaint_type breakdown, top descriptors, agency split.

Produces: ana_04 (complaint_type ranking), ana_05 (top descriptors), ana_06 (agency split).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")

# --- ana_04: Complaint-type distribution ---
print("=== ana_04 ===")
ct = df["complaint_type"].value_counts()
total = len(df)
print(f"All complaint_type values, 2023 + 2024 combined ({total:,} rows):")
for label, count in ct.items():
    pct = 100 * count / total
    print(f"  {count:>9,}  {pct:>5.2f}%  {label}")

# --- ana_05: Top descriptors overall, and within each complaint_type ---
print("=== ana_05 ===")
desc_overall = df["descriptor"].value_counts()
print("Top 25 descriptors overall:")
for label, count in desc_overall.head(25).items():
    pct = 100 * count / total
    print(f"  {count:>8,}  {pct:>5.2f}%  {label}")

print("\nTop 3 descriptors within each major complaint_type:")
for ctype, _ in ct.head(7).items():
    sub = df.loc[df["complaint_type"] == ctype, "descriptor"]
    top3 = sub.value_counts().head(3)
    print(f"  {ctype}  (n={len(sub):,})")
    for d, c in top3.items():
        share = 100 * c / max(len(sub), 1)
        print(f"     {c:>7,}  {share:>5.1f}%  {d}")

# --- ana_06: Responding agency split ---
print("=== ana_06 ===")
ag = df["agency"].value_counts()
print("Complaints by responding agency (2023 + 2024 combined):")
for label, count in ag.items():
    pct = 100 * count / total
    print(f"  {count:>9,}  {pct:>5.2f}%  {label}")

# Agency × complaint_type cross-tab — which agency owns which buckets
print("\nAgency × complaint_type (counts):")
crosstab = pd.crosstab(df["complaint_type"], df["agency"])
crosstab = crosstab.loc[ct.index]  # order by overall volume
crosstab["TOTAL"] = crosstab.sum(axis=1)
print(crosstab.to_string())
