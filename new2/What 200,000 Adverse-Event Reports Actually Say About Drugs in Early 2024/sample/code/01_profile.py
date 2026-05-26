"""
01_profile.py — Basic dataset profile.
Run from anywhere with DATA_DIR set; defaults to the project dataset.
"""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:\AI\journalist agent review\phase2\datasets\openfda_faers_2024",
)

sample = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_sample.csv"))
drugs = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_drugs.csv"))
reactions = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_reactions.csv"))

# --- ana_01: row & column shape across the three files ---
print("=== ana_01 ===")
for name, df in [("sample", sample), ("drugs", drugs), ("reactions", reactions)]:
    print(f"{name}: rows={len(df):,} cols={len(df.columns)} cols={list(df.columns)}")

# --- ana_02: time range of received reports ---
print("=== ana_02 ===")
sample["receivedate_str"] = sample["receivedate"].astype(str)
sample["received_dt"] = pd.to_datetime(sample["receivedate_str"], format="%Y%m%d", errors="coerce")
print("min:", sample["received_dt"].min(), "max:", sample["received_dt"].max())
print("unique dates:", sample["received_dt"].nunique())
print("rows w/ valid date:", sample["received_dt"].notna().sum())

# --- ana_03: null & missingness per column in sample ---
print("=== ana_03 ===")
nulls = sample.isna().sum().sort_values(ascending=False)
total = len(sample)
for col, n in nulls.items():
    if n > 0:
        print(f"{col}: missing={n:,} ({n/total*100:.1f}%)")
print(f"total rows: {total:,}")

# --- ana_04: encoding check — seriousness sub-flag values actually present ---
print("=== ana_04 ===")
for col in ("serious", "seriousnessdeath", "seriousnesshospitalization", "patient_sex", "reporttype"):
    vc = sample[col].value_counts(dropna=False).head(10)
    print(f"\n{col}:")
    print(vc)

# --- ana_05: per-report drug / reaction counts ---
print("=== ana_05 ===")
print("n_drugs distribution:")
print(sample["n_drugs"].describe())
print("n_drugs value counts (top 12):")
print(sample["n_drugs"].value_counts().head(12).sort_index())
print()
print("n_reactions distribution:")
print(sample["n_reactions"].describe())
print("n_reactions value counts (top 12):")
print(sample["n_reactions"].value_counts().head(12).sort_index())
