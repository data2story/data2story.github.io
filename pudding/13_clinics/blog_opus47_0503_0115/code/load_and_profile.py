"""Load the dataset and produce dataset profile + field inventory.

The 'duration' columns are in HOURS (round-trip, rounded down, binned into
1-hour increments) per the Pudding methodology, despite the README labelling
the field 'minutes'. This is confirmed by the article text and the actual
value range (max ~9-11) which matches '~9 hours round-trip'.
"""
import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/13_clinics/cities.csv"
df = pd.read_csv(DATA)

# --- ana_01: dataset profile ---
print("=== ana_01 ===")
print(f"rows={len(df)}, cols={len(df.columns)}")
print(f"states={df['state'].nunique()}")
print(f"total_pop_covered={df['population'].sum():,}")
print(f"min_city_pop={df['population'].min():,}")
print(f"max_city_pop={df['population'].max():,}")
print(f"missing_values_total={df.isnull().sum().sum()}")

# --- ana_02: gestation 8 distribution ---
print("\n=== ana_02 ===")
g8 = df['gestation_8_duration']
print("hours of round-trip drive at 8 weeks:")
print(g8.value_counts().sort_index())
print(f"cities with 0h drive: {(g8==0).sum()} ({(g8==0).mean()*100:.1f}%)")
print(f"cities with 4h+ drive: {(g8>=4).sum()} ({(g8>=4).mean()*100:.1f}%)")

# --- ana_03: gestation collapse: drive at each gestation ---
print("\n=== ana_03 ===")
for col in ['gestation_8_duration','gestation_12_duration','gestation_16_duration','gestation_20_duration']:
    s = df[col]
    pop = df['population']
    pop_weighted_mean = (s * pop).sum() / pop.sum()
    pop_with_zero = pop[s==0].sum() / pop.sum() * 100
    pop_with_4plus = pop[s>=4].sum() / pop.sum() * 100
    print(f"{col}: cities_mean={s.mean():.2f}h, pop_weighted_mean={pop_weighted_mean:.2f}h, pct_pop_zero={pop_with_zero:.1f}%, pct_pop_4plus={pop_with_4plus:.1f}%")
