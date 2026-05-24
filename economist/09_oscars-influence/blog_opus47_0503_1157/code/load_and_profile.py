"""Load movie-counts.csv, profile schema, basic stats, and dataset shape."""
import pandas as pd
import numpy as np

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/09_oscars-influence/movie-counts.csv'

df = pd.read_csv(DATA, encoding='latin-1')

# --- ana_01: Dataset shape and time span ---
print("=== ana_01 ===")
print(f"rows: {len(df):,}")
print(f"columns: {len(df.columns)} -> {list(df.columns)}")
print(f"release_year range: {df.release_year.min()} - {df.release_year.max()}")
print(f"oscars_year range: {df.oscars_year.min()} - {df.oscars_year.max()}")
print(f"unique movies: {df.movie_name.nunique():,}")
print(f"sum of count column (total IMDb connections): {df['count'].sum():,}")
# line 16

# --- ana_02: Field types and missingness ---
print("\n=== ana_02 ===")
print(df.dtypes)
print("\nmissing per column:")
print(df.isna().sum())
# line 22

# --- ana_03: Best Picture status breakdown ---
print("\n=== ana_03 ===")
result_counts = df['result'].fillna('not_nominated').value_counts(dropna=False)
print(result_counts)
print(f"\nBest Picture winners (W): {(df['result'] == 'W').sum()}")
print(f"Nominees only (N): {(df['result'] == 'N').sum()}")
n_unique_winners = df.loc[df['result'] == 'W', 'movie_name'].nunique()
print(f"Unique BP winning films in dataset: {n_unique_winners}")
# line 31
