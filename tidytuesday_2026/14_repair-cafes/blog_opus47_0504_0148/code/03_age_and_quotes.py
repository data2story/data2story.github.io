"""Item-age analysis and select notable verbatim quotes from the free-text fields."""
import pandas as pd
import numpy as np
import re
from pathlib import Path
from collections import Counter

DATA_DIR = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/14_repair-cafes")
repairs = pd.read_csv(DATA_DIR / "repairs.csv", low_memory=False)
text = pd.read_csv(DATA_DIR / "repairs_text.csv", low_memory=False)
repairs['repaired'] = repairs['repaired'].replace({'ja': 'yes'})
df = repairs.merge(text, on='repair_id', how='left')
df['repair_date'] = pd.to_datetime(df['repair_date'], errors='coerce')

# --- ana_18: Item age at time of repair attempt ---
print("=== ana_18 ===")
df['age'] = df['repair_date'].dt.year - df['estimated_year_of_production']
df_age = df[(df['age'] >= 0) & (df['age'] <= 80)].copy()
print(f"Median age: {df_age['age'].median()}")
print(f"Mean age: {df_age['age'].mean():.2f}")
# Bucket
bins = [-1, 1, 3, 5, 10, 15, 20, 30, 50, 81]
labels = ['0-1','2-3','4-5','6-10','11-15','16-20','21-30','31-50','50+']
df_age['age_bucket'] = pd.cut(df_age['age'], bins=bins, labels=labels)
by_bucket = df_age.groupby('age_bucket', observed=True).agg(
    n=('age','size'),
    success=('repaired', lambda x: (x=='yes').sum())
).reset_index()
by_bucket['success_pct'] = 100*by_bucket['success']/by_bucket['n']
print(by_bucket.to_string(index=False))

# --- ana_19: Most-repaired vintage items (>=20 years old) ---
print("\n=== ana_19 ===")
old = df_age[df_age['age'] >= 20]
print(f"Number of items aged 20+ years brought in: {len(old)}")
print(f"Their success rate: {100*(old['repaired']=='yes').sum()/len(old):.2f}%")
top_old = old.groupby('kind_of_product').size().sort_values(ascending=False).head(15)
print("Top 15 vintage product types:")
print(top_old.to_string())

# --- ana_20: Trousers / pants — the textile success champion ---
print("\n=== ana_20 ===")
tr = df[df['kind_of_product'] == 'Trousers / pants']
print(f"Trousers n: {len(tr)}")
print(f"Trousers success: {100*(tr['repaired']=='yes').sum()/len(tr):.2f}%")
# Most common defects
top_defects = tr['defect_found'].dropna().astype(str).str.lower().str.strip().value_counts().head(15)
print("Top 15 trouser defects:")
print(top_defects.to_string())

# --- ana_21: Vacuum cleaner — the most-fought battle ---
print("\n=== ana_21 ===")
vc = df[df['kind_of_product'] == 'Vacuum cleaner']
print(f"Vacuum cleaner n: {len(vc)}")
print(f"Success: {100*(vc['repaired']=='yes').sum()/len(vc):.2f}%")
# Failure reasons specific to vacuum cleaners
vc_failed = vc[vc['repaired'].isin(['no','half'])]
all_reasons = []
for s in vc_failed['failure_reasons'].dropna().astype(str):
    parts = [p.strip() for p in re.split(r'[;|]', s) if p.strip() and p.strip().upper() != 'NA']
    all_reasons.extend(parts)
rc = Counter(all_reasons)
print("Top failure reasons for vacuum cleaners:")
for r, c in sorted(rc.items(), key=lambda x: -x[1])[:10]:
    print(f"  {c:>5} ({100*c/len(vc_failed):5.2f}%) {r}")

# --- ana_22: Cumulative repairs and CO2 saved (det_03 anchor) ---
print("\n=== ana_22 ===")
df_yes = df[df['repaired'] == 'yes']
total_yes = len(df_yes)
total_co2_kg = total_yes * 24
print(f"Total successful repairs: {total_yes}")
print(f"Estimated CO2 saved (24 kg/repair): {total_co2_kg} kg = {total_co2_kg/1000:.1f} tonnes")
# By year
yearly_yes = df_yes.copy()
yearly_yes['year'] = yearly_yes['repair_date'].dt.year
yr = yearly_yes.groupby('year').size().reset_index(name='yes')
yr['cumulative'] = yr['yes'].cumsum()
yr['co2_tonnes_cum'] = yr['cumulative'] * 24 / 1000
print(yr.to_string(index=False))

# --- ana_23: Verbatim quotes — failure_reason_open with humor / pathos ---
print("\n=== ana_23 ===")
quotes_pool = df.dropna(subset=['failure_reason_open']).copy()
quotes_pool['fr_open'] = quotes_pool['failure_reason_open'].astype(str)
# Filter: english-ish, length 30-160, not all caps, mentions something specific
def good_q(s):
    if len(s) < 25 or len(s) > 200: return False
    if s.upper() == s: return False
    if s.lower() in ['na','n/a']: return False
    return True
quotes_pool['ok'] = quotes_pool['fr_open'].apply(good_q)
sample = quotes_pool[quotes_pool['ok']].sample(40, random_state=7)
print("Random failure_reason_open quotes (n=40):")
for _, row in sample.iterrows():
    print(f"  [{row['kind_of_product']}] {row['fr_open'][:180]}")

# --- ana_24: Most common 'suggestions' phrases (advice from repairers) ---
print("\n=== ana_24 ===")
sug = df['suggestions'].dropna().astype(str).str.strip()
sug = sug[~sug.str.lower().isin(['na','n/a','-'])]
print(f"Total non-empty suggestions: {len(sug)}")
top_sug = sug.value_counts().head(20)
print("Top 20 suggestion phrases:")
print(top_sug.to_string())
