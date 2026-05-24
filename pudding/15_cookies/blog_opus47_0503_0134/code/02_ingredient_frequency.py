"""Frequency and rarity analysis of ingredients across the 211 recipes."""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/15_cookies"
df = pd.read_csv(os.path.join(DATA_DIR, "choc_chip_cookie_ingredients.csv"), encoding='latin-1')
total_recipes = df['Recipe_Index'].nunique()

# --- ana_03: Ingredient appearance frequency ---
print("=== ana_03 ===")
ing_recipe_count = df.groupby('Ingredient')['Recipe_Index'].nunique().sort_values(ascending=False)
ing_pct = (ing_recipe_count / total_recipes * 100).round(1)
freq_df = pd.DataFrame({'recipes': ing_recipe_count, 'pct': ing_pct})
print(f"Total unique ingredients: {len(ing_recipe_count)}")
print(f"\nTop 20 most common (universal staples):")
print(freq_df.head(20).to_string())

# --- ana_04: Long tail — ingredients that appear in only a few recipes ---
print("\n=== ana_04 ===")
rare = freq_df[freq_df['recipes'] <= 3].sort_values('recipes')
print(f"Ingredients appearing in 1-3 recipes only: {len(rare)}")
print(f"\nThe 'curiosities' (the long tail of trace ingredients):")
print(rare.head(40).to_string())

# --- ana_05: Bucketed frequency distribution ---
print("\n=== ana_05 ===")
buckets = pd.cut(freq_df['pct'],
                 bins=[0, 5, 25, 50, 75, 100],
                 labels=['<5% (rare)', '5-25%', '25-50%', '50-75%', '75-100% (universal)'])
print("How many ingredients in each frequency bucket:")
print(buckets.value_counts().sort_index())
