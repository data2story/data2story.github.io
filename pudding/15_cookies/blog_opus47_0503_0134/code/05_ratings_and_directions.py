"""Ratings analysis and directions corpus stats."""
import pandas as pd
import os
import re
from collections import Counter

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/15_cookies"
df = pd.read_csv(os.path.join(DATA_DIR, "choc_chip_cookie_ingredients.csv"), encoding='latin-1')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# --- ana_13: Rating distribution (where present) ---
print("=== ana_13 ===")
ratings = df.groupby('Recipe_Index')['Rating'].first().dropna()
print(f"Recipes with rating: {len(ratings)}/{df['Recipe_Index'].nunique()} ({len(ratings)/df['Recipe_Index'].nunique()*100:.1f}%)")
print(f"Rating mean: {ratings.mean():.3f}")
print(f"Rating median: {ratings.median():.3f}")
print(f"Rating std: {ratings.std():.3f}")
print(f"Min: {ratings.min():.3f}, Max: {ratings.max():.3f}")
buckets = pd.cut(ratings, bins=[0, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.01],
                 labels=['<0.6', '0.6-0.7', '0.7-0.8', '0.8-0.85', '0.85-0.9', '0.9-0.95', '0.95+'])
print("Rating buckets:")
print(buckets.value_counts().sort_index().to_string())

# --- ana_14: Directions corpus stats ---
print("\n=== ana_14 ===")
with open(os.path.join(DATA_DIR, "All_directions.txt"), encoding='latin-1') as f:
    text = f.read()
lines = [ln.strip() for ln in text.split('\n') if ln.strip()]
print(f"Total non-empty lines: {len(lines)}")
total_words = sum(len(ln.split()) for ln in lines)
print(f"Total words: {total_words}")
print(f"Mean words per instruction line: {total_words/len(lines):.2f}")

# --- ana_15: Most common bigrams in directions (cooking verbs/phrases) ---
print("\n=== ana_15 ===")
def tokenize(s):
    return re.findall(r"[a-z]+", s.lower())
toks = tokenize(text)
print(f"Total tokens (alphabetic): {len(toks)}")
print(f"Unique tokens: {len(set(toks))}")
bigrams = Counter(zip(toks, toks[1:]))
common_bigrams = bigrams.most_common(25)
print("Top 25 bigrams in cookie directions:")
for (a, b), c in common_bigrams:
    print(f"  {a} {b}: {c}")

# --- ana_16: Oven temperature prevalence ---
print("\n=== ana_16 ===")
temps = re.findall(r"(\d+)\s*degrees", text)
temps = [int(t) for t in temps if 200 <= int(t) <= 500]
temp_counts = Counter(temps)
print("Most common oven temperatures (Fahrenheit):")
for t, c in temp_counts.most_common(10):
    print(f"  {t}F: {c} mentions")
