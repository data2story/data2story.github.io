"""Load pi digits and produce dataset profile."""
import pandas as pd
import numpy as np

CSV = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/12_pi-million-digits/pi_digits.csv"

df = pd.read_csv(CSV)
print(f"shape: {df.shape}")
print(f"columns: {list(df.columns)}")
print(f"dtypes:\n{df.dtypes}")
print(f"head:\n{df.head()}")
print(f"tail:\n{df.tail()}")
print(f"null counts:\n{df.isnull().sum()}")
print(f"digit dtype: {df['digit'].dtype}")
print(f"unique digits: {sorted(df['digit'].unique().tolist())}")
print(f"min position: {df['digit_position'].min()}, max position: {df['digit_position'].max()}")

# --- ana_00: Dataset profile ---
print("=== ana_00 ===")
print(f"rows: {len(df)}")
print(f"first 10 digits: {df['digit'].iloc[:10].tolist()}")
print(f"first row's digit (the leading 3): {df['digit'].iloc[0]}")
# So digit_position 1 = '3' (the integer part). Positions 2..1000001 = the million decimals.
