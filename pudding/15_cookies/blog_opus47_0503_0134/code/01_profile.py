"""Profile and overall stats of the cookie ingredients dataset."""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/15_cookies"
df = pd.read_csv(os.path.join(DATA_DIR, "choc_chip_cookie_ingredients.csv"), encoding='latin-1')

# --- ana_01: Dataset shape ---
print("=== ana_01 ===")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Column names: {list(df.columns)}")
print(f"Unique recipes: {df['Recipe_Index'].nunique()}")
print(f"Unique ingredients: {df['Ingredient'].nunique()}")
print(f"Source breakdown:")
src = df['Recipe_Index'].str.extract(r'^([A-Za-z]+)_')[0].value_counts()
print(src)

# --- ana_02: Ingredients per recipe distribution ---
print("\n=== ana_02 ===")
counts = df.groupby('Recipe_Index').size()
print(f"Mean ingredients per recipe: {counts.mean():.2f}")
print(f"Median: {counts.median()}")
print(f"Min: {counts.min()}")
print(f"Max: {counts.max()}")
print(f"Std: {counts.std():.2f}")
print(f"\nDistribution buckets:")
buckets = pd.cut(counts, bins=[0, 6, 8, 10, 12, 15, 30], labels=['1-6', '7-8', '9-10', '11-12', '13-15', '16+'])
print(buckets.value_counts().sort_index())
print(f"\nTop 5 most-ingredient recipes:")
print(counts.sort_values(ascending=False).head())
