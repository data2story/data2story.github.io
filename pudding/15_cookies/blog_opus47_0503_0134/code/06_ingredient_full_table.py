"""Generate the full table of all 68 ingredients with mean quantity, prevalence, unit."""
import pandas as pd
import os
import json

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/15_cookies"
df = pd.read_csv(os.path.join(DATA_DIR, "choc_chip_cookie_ingredients.csv"), encoding='latin-1')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
total_recipes = df['Recipe_Index'].nunique()

# --- ana_17: Full ingredient table ---
print("=== ana_17 ===")
sums = df.groupby('Ingredient')['Quantity'].sum()
mean_q_pop = (sums / total_recipes)
freq = df.groupby('Ingredient')['Recipe_Index'].nunique()
unit = df.groupby('Ingredient')['Unit'].first()
mean_q_when_used = df.groupby('Ingredient')['Quantity'].mean()

# Build full table
tbl = pd.DataFrame({
    'mean_population': mean_q_pop.round(4),
    'mean_when_used': mean_q_when_used.round(3),
    'unit': unit,
    'recipes': freq,
    'pct': (freq / total_recipes * 100).round(1)
}).sort_values('pct', ascending=False)
print(f"Total ingredients: {len(tbl)}")
print(tbl.to_string())

# Save full table as JSON for the analyst.json data_table
out = []
for ing, row in tbl.iterrows():
    out.append([ing, float(row['mean_population']), float(row['mean_when_used']),
                row['unit'] if pd.notna(row['unit']) else '',
                int(row['recipes']), float(row['pct'])])

# print as JSON-ish
import json as _json
print("\n=== ana_17_json ===")
print(_json.dumps(out, indent=None)[:1500] + "...")

# Save to a data file in code/ for later lookup
with open(os.path.join(os.path.dirname(__file__), '..', 'code', 'all_ingredients.json'), 'w') as f:
    _json.dump(out, f)
