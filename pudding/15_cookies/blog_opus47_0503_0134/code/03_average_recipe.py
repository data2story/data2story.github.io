"""Compute the mathematical average recipe — quantity per ingredient."""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/15_cookies"
df = pd.read_csv(os.path.join(DATA_DIR, "choc_chip_cookie_ingredients.csv"), encoding='latin-1')
total_recipes = df['Recipe_Index'].nunique()

# Average across ALL 211 recipes (assuming missing = 0)
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# --- ana_06: The "average cookie" recipe — top 10 ingredients by mean quantity ---
print("=== ana_06 ===")
sums = df.groupby('Ingredient')['Quantity'].sum()
mean_q = (sums / total_recipes).round(3)
freq = df.groupby('Ingredient')['Recipe_Index'].nunique()
unit = df.groupby('Ingredient')['Unit'].first()
avg_table = pd.DataFrame({
    'mean_quantity': mean_q,
    'unit': unit,
    'recipes_with': freq,
    'pct_with': (freq / total_recipes * 100).round(1)
}).sort_values('mean_quantity', ascending=False)

# Filter to top 12 by mean quantity (the "core")
print("THE AVERAGE CHOCOLATE CHIP COOKIE — top 12 by mean quantity (per 48 cookies):")
print(avg_table.head(12).to_string())

# --- ana_07: How many distinct ingredients does the "average" cookie contain? ---
print("\n=== ana_07 ===")
print(f"Total distinct ingredients across all 211 recipes: {len(avg_table)}")
print(f"Number of ingredients with mean > 0.5 of unit: {(avg_table['mean_quantity'] > 0.5).sum()}")
print(f"Number of ingredients with mean > 0.01: {(avg_table['mean_quantity'] > 0.01).sum()}")
print(f"Number of trace ingredients (mean < 0.01): {(avg_table['mean_quantity'] < 0.01).sum()}")
