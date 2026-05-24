"""Load Milano-Cortina 2026 schedule and profile dataset.
Run: python3 load_and_profile.py
"""
import pandas as pd

DATA_PATH = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/06_winter-olympics-2026/schedule.csv"

df = pd.read_csv(DATA_PATH)

# --- ana_00: dataset shape ---
print("=== ana_00 ===")
print(f"rows={len(df)} cols={len(df.columns)}")
print(df.dtypes)
print("\nMissing per col:")
print(df.isna().sum())
print("\nUnique cardinalities:")
for c in df.columns:
    print(f"  {c}: {df[c].nunique()} unique")
print("\nDate range:", df['date'].min(), "→", df['date'].max())
print("\nis_medal_event values:", df['is_medal_event'].value_counts(dropna=False).to_dict())
print("is_training values:", df['is_training'].value_counts(dropna=False).to_dict())
