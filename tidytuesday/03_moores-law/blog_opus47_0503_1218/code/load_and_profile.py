"""Load CPU/GPU/RAM CSVs from the TidyTuesday Moore's Law dataset.

Profiling: row counts, year ranges, missing values, unique designers/manufacturers,
and a few sanity checks on the raw fields.
"""
import pandas as pd
import numpy as np
import sys
import os

DATA_DIR = '/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/03_moores-law'

cpu = pd.read_csv(os.path.join(DATA_DIR, 'cpu.csv'))
gpu = pd.read_csv(os.path.join(DATA_DIR, 'gpu.csv'))
ram = pd.read_csv(os.path.join(DATA_DIR, 'ram.csv'))

# --- ana_00: dataset profile ---
print("=== ana_00 ===")
for name, df in [('cpu', cpu), ('gpu', gpu), ('ram', ram)]:
    n = len(df)
    miss_tc = df['transistor_count'].isna().sum()
    yr_min = int(df['date_of_introduction'].min())
    yr_max = int(df['date_of_introduction'].max())
    miss_proc = df['process'].isna().sum() if 'process' in df.columns else 'NA'
    print(f"{name}: rows={n}  yr={yr_min}-{yr_max}  missing_tc={miss_tc}  missing_process={miss_proc}")

# Designers / manufacturers
print("\n--- designers (cpu) ---")
print(cpu['designer'].value_counts().head(10))
print("\n--- designers_s (gpu) ---")
print(gpu['designer_s'].value_counts().head(10))
print("\n--- manufacturers_s (ram) ---")
print(ram['manufacturer_s'].value_counts().head(10))
