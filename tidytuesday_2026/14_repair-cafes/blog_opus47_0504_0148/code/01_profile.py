"""Profile and basic distributions for the Repair Cafes dataset."""
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/14_repair-cafes")
repairs = pd.read_csv(DATA_DIR / "repairs.csv", low_memory=False)
repairs_text = pd.read_csv(DATA_DIR / "repairs_text.csv", low_memory=False)

# Normalize 'ja' (Dutch yes) to 'yes'
repairs['repaired'] = repairs['repaired'].replace({'ja': 'yes'})

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"Rows in repairs.csv: {len(repairs)}")
print(f"Rows in repairs_text.csv: {len(repairs_text)}")
print(f"Date range: {repairs['repair_date'].min()} to {repairs['repair_date'].max()}")
print(f"Countries: {repairs['country'].nunique()}")
print(f"Cafes (branches): {repairs['repair_cafe_number'].nunique()}")
print(f"Unique kind_of_product: {repairs['kind_of_product'].nunique()}")
print(f"Unique brand: {repairs['brand'].nunique()}")
print(f"Unique category: {repairs['category'].nunique()}")

# --- ana_02: Repair outcome distribution (the headline 65% claim revisited) ---
print("\n=== ana_02 ===")
total = len(repairs)
out = repairs['repaired'].value_counts(dropna=False)
print(out)
yes = out.get('yes', 0)
half = out.get('half', 0)
no = out.get('no', 0)
print(f"yes pct: {100*yes/total:.2f}")
print(f"half pct: {100*half/total:.2f}")
print(f"no pct: {100*no/total:.2f}")
print(f"yes+half pct: {100*(yes+half)/total:.2f}")

# --- ana_03: Top 15 most-repaired product kinds ---
print("\n=== ana_03 ===")
top_products = repairs['kind_of_product'].value_counts().head(15)
print(top_products)

# --- ana_04: Repair success rate by top product ---
print("\n=== ana_04 ===")
top20 = repairs['kind_of_product'].value_counts().head(20).index.tolist()
sub = repairs[repairs['kind_of_product'].isin(top20)].copy()
ct = pd.crosstab(sub['kind_of_product'], sub['repaired'], normalize='index') * 100
ct = ct.reindex(top20)
ct['n'] = repairs['kind_of_product'].value_counts().reindex(top20).values
print(ct.round(1).to_string())

# --- ana_05: Country distribution ---
print("\n=== ana_05 ===")
country_counts = repairs['country'].value_counts()
print(country_counts.head(15))
print(f"NL share: {100*country_counts.get('NL',0)/total:.2f}%")
print(f"Top 5 share: {100*country_counts.head(5).sum()/total:.2f}%")

# --- ana_06: Time trend - yearly volume ---
print("\n=== ana_06 ===")
repairs['repair_date'] = pd.to_datetime(repairs['repair_date'], errors='coerce')
repairs['year'] = repairs['repair_date'].dt.year
yearly = repairs.groupby('year').size()
print(yearly.to_string())

# --- ana_07: Repairability distribution (1-10 score) ---
print("\n=== ana_07 ===")
rep_score = repairs['repairability'].dropna()
print(f"n: {len(rep_score)}")
print(f"mean: {rep_score.mean():.2f}")
print(f"median: {rep_score.median()}")
hist = rep_score.value_counts().sort_index()
print(hist.to_string())

# --- ana_08: Categories ---
print("\n=== ana_08 ===")
cat_outcome = pd.crosstab(repairs['category'], repairs['repaired'], normalize='index') * 100
cat_n = repairs['category'].value_counts()
cat_outcome = cat_outcome.reindex(cat_n.index)
cat_outcome['n'] = cat_n.values
print(cat_outcome.round(1).to_string())
