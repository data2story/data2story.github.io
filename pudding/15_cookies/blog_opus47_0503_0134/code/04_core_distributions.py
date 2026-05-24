"""Distributions of the core ingredients across recipes — for histogram charts."""
import pandas as pd
import os
import json

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/15_cookies"
df = pd.read_csv(os.path.join(DATA_DIR, "choc_chip_cookie_ingredients.csv"), encoding='latin-1')
total_recipes = df['Recipe_Index'].nunique()
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# Pivot: one row per recipe, columns = ingredients
pivot = df.pivot_table(index='Recipe_Index', columns='Ingredient',
                       values='Quantity', aggfunc='sum').fillna(0)

# Combine related chocolate chip variants into a single series
chip_cols = [c for c in pivot.columns if 'chocolate chip' in c]
pivot['chocolate_chips_total'] = pivot[chip_cols].sum(axis=1)

# Combine related sugar variants into one
sugar_cols = ['sugar', 'light brown sugar', 'dark brown sugar']
sugar_cols = [c for c in sugar_cols if c in pivot.columns]
pivot['sugars_total'] = pivot[sugar_cols].sum(axis=1)
# Treat 'sugar' as 'white sugar' for clarity (per the dataset README, this is the convention)
pivot['white sugar'] = pivot['sugar']

# --- ana_08: Distribution of flour quantity ---
print("=== ana_08 ===")
flour = pivot['all purpose flour']
flour_used = flour[flour > 0]
print(f"All purpose flour: {(flour > 0).sum()}/{total_recipes} recipes use it ({(flour > 0).mean()*100:.1f}%)")
print(f"Mean: {flour_used.mean():.3f} cups, Median: {flour_used.median()}, Std: {flour_used.std():.3f}")
print(f"Min: {flour_used.min()}, Max: {flour_used.max()}")
print(f"5th-95th percentile: {flour_used.quantile(0.05):.2f} - {flour_used.quantile(0.95):.2f}")

# --- ana_09: Distribution of butter quantity ---
print("\n=== ana_09 ===")
butter = pivot['butter']
butter_used = butter[butter > 0]
print(f"Butter: {(butter > 0).sum()}/{total_recipes} recipes use it ({(butter > 0).mean()*100:.1f}%)")
print(f"Mean: {butter_used.mean():.3f} cups, Median: {butter_used.median()}, Std: {butter_used.std():.3f}")
print(f"Min: {butter_used.min()}, Max: {butter_used.max()}")
print(f"5th-95th percentile: {butter_used.quantile(0.05):.2f} - {butter_used.quantile(0.95):.2f}")

# --- ana_10: Brown sugar vs white sugar ---
print("\n=== ana_10 ===")
ws = pivot['white sugar'][pivot['white sugar'] > 0]
lbs = pivot['light brown sugar'][pivot['light brown sugar'] > 0]
print(f"White sugar: used in {len(ws)}/{total_recipes} ({len(ws)/total_recipes*100:.1f}%), mean = {ws.mean():.3f} cups")
print(f"Light brown sugar: used in {len(lbs)}/{total_recipes} ({len(lbs)/total_recipes*100:.1f}%), mean = {lbs.mean():.3f} cups")

# Of recipes that have BOTH, ratio brown:white
both = pivot[(pivot['white sugar'] > 0) & (pivot['light brown sugar'] > 0)]
ratio = both['light brown sugar'] / both['white sugar']
print(f"\nRecipes using both: {len(both)}")
print(f"Brown:White ratio (mean): {ratio.mean():.3f}, median: {ratio.median():.3f}")
print(f"Recipes with MORE brown than white: {(ratio > 1).sum()} ({(ratio > 1).mean()*100:.1f}%)")
print(f"Recipes with MORE white than brown: {(ratio < 1).sum()} ({(ratio < 1).mean()*100:.1f}%)")

# --- ana_11: Chocolate chip distribution ---
print("\n=== ana_11 ===")
chips = pivot['chocolate_chips_total']
chips_used = chips[chips > 0]
print(f"Any chocolate chip: {(chips > 0).sum()}/{total_recipes} recipes ({(chips > 0).mean()*100:.1f}%)")
print(f"Mean total chips: {chips_used.mean():.3f} cups, Median: {chips_used.median()}, Std: {chips_used.std():.3f}")

# By type
for c in chip_cols:
    n = (pivot[c] > 0).sum()
    if n > 0:
        m = pivot[c][pivot[c] > 0].mean()
        print(f"  {c}: {n} recipes ({n/total_recipes*100:.1f}%), mean = {m:.3f} cups")

# --- ana_12: Eggs ---
print("\n=== ana_12 ===")
eggs = pivot['egg'] if 'egg' in pivot.columns else None
if eggs is not None:
    eggs_used = eggs[eggs > 0]
    print(f"Eggs: {(eggs > 0).sum()}/{total_recipes} recipes ({(eggs > 0).mean()*100:.1f}%)")
    print(f"Mean: {eggs_used.mean():.3f}, Median: {eggs_used.median()}")

# Save the core distribution histograms as JSON-friendly data
print("\n=== ana_08_table ===")
flour_buckets = pd.cut(flour_used, bins=[0, 1, 2, 3, 4, 5, 10],
                       labels=['0-1', '1-2', '2-3', '3-4', '4-5', '5+'])
print(flour_buckets.value_counts().sort_index().to_string())

print("\n=== ana_09_table ===")
butter_buckets = pd.cut(butter_used, bins=[0, 0.5, 1, 1.5, 2, 5],
                        labels=['0-0.5', '0.5-1', '1-1.5', '1.5-2', '2+'])
print(butter_buckets.value_counts().sort_index().to_string())

print("\n=== ana_11_table ===")
chip_buckets = pd.cut(chips_used, bins=[0, 0.5, 1, 1.5, 2, 3, 10],
                      labels=['0-0.5', '0.5-1', '1-1.5', '1.5-2', '2-3', '3+'])
print(chip_buckets.value_counts().sort_index().to_string())
