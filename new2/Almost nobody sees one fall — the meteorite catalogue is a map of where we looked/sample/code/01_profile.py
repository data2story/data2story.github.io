"""01_profile.py — Dataset profile and field inventory for the Meteorite Landings dataset.
Run from any cwd; uses absolute path to the CSV.
"""
import pandas as pd
import numpy as np

CSV = r"D:/AI/journalist agent review/phase2/datasets/2020-07-29_meteorite-landings/meteorite_landings.csv"
df = pd.read_csv(CSV)

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"rows={len(df):,}  cols={df.shape[1]}")
print(f"columns={list(df.columns)}")
print(f"fell={int((df['fall']=='Fell').sum()):,}  found={int((df['fall']=='Found').sum()):,}")
print(f"valid_nametype={int((df['nametype']=='Valid').sum()):,}  relict={int((df['nametype']=='Relict').sum()):,}")
print(f"distinct_recclass={df['recclass'].nunique()}")
print(f"distinct_names={df['name'].nunique()}")
print(f"year_min={df['year'].min()}  year_max={df['year'].max()}  null_years={int(df['year'].isna().sum())}")
print(f"mass_g_min={df['mass (g)'].min()}  mass_g_max={df['mass (g)'].max():.0f}  null_mass={int(df['mass (g)'].isna().sum())}")
print(f"missing_coords={int(df['reclat'].isna().sum()):,}  ({df['reclat'].isna().mean()*100:.1f}%)")

# --- ana_02: Missing-value rates per column ---
print("\n=== ana_02 ===")
miss = df.isna().sum().to_frame('missing')
miss['rate_pct'] = (miss['missing'] / len(df) * 100).round(3)
print(miss.to_string())

# --- ana_03: Year column quality — out-of-range / suspect values ---
print("\n=== ana_03 ===")
yr = df['year']
future = df[yr > 2025]
zero  = df[yr == 0]
pre1000 = df[(yr > 0) & (yr < 1000)]
print(f"rows_with_year_gt_2025={len(future)}")
print(future[['name','year','fall']].to_string(index=False))
print(f"rows_with_year_eq_0={len(zero)}")
print(f"rows_with_year_in_(0,1000)={len(pre1000)}")
print(pre1000.sort_values('year')[['name','year','fall']].head(10).to_string(index=False))
# Clean version used by downstream scripts: 1 <= year <= 2025
clean_year = yr.between(1, 2025)
print(f"rows_after_year_clean={int(clean_year.sum()):,}  dropped={int((~clean_year & yr.notna()).sum())}")

# Cache cleaned data for downstream scripts
df_clean = df[clean_year | yr.isna()].copy()
df_clean.to_pickle(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225/code/_clean.pkl")
print("wrote _clean.pkl")
