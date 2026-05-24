"""City-level extremes: top cities by 8 / 16 / 20 week drive, by collapse,
and by fragility under nearest-clinic closure."""
import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/13_clinics/cities.csv"
df = pd.read_csv(DATA)

# --- ana_11: longest 8-week drives (open) ---
print("=== ana_11 ===")
worst_8 = df.nlargest(15, 'gestation_8_duration')[['city','state','population','gestation_8_duration','gestation_16_duration','gestation_20_duration']]
print("Longest 8-week round-trip drives (cities):")
print(worst_8.to_string(index=False))

# --- ana_12: longest 16-week drives (open) ---
print("\n=== ana_12 ===")
worst_16 = df.nlargest(15, 'gestation_16_duration')[['city','state','population','gestation_8_duration','gestation_16_duration','gestation_20_duration']]
print("Longest 16-week round-trip drives:")
print(worst_16.to_string(index=False))

# --- ana_13: longest 20-week drives (open) ---
print("\n=== ana_13 ===")
worst_20 = df.nlargest(15, 'gestation_20_duration')[['city','state','population','gestation_8_duration','gestation_16_duration','gestation_20_duration']]
print("Longest 20-week round-trip drives:")
print(worst_20.to_string(index=False))

# --- ana_14: biggest 8 -> 16 week jump within a city ---
print("\n=== ana_14 ===")
df['jump_8_16'] = df['gestation_16_duration'] - df['gestation_8_duration']
df['jump_8_20'] = df['gestation_20_duration'] - df['gestation_8_duration']
big_jump_16 = df.nlargest(15, 'jump_8_16')[['city','state','population','gestation_8_duration','gestation_16_duration','jump_8_16']]
print("Biggest 8 -> 16 week jumps (drive grows the most as gestation rises):")
print(big_jump_16.to_string(index=False))

# --- ana_15: biggest 8 -> 20 week jump ---
print("\n=== ana_15 ===")
big_jump_20 = df.nlargest(15, 'jump_8_20')[['city','state','population','gestation_8_duration','gestation_20_duration','jump_8_20']]
print("Biggest 8 -> 20 week jumps:")
print(big_jump_20.to_string(index=False))

# --- ana_16: closure fragility — biggest gap when nearest clinic closes (8wk) ---
print("\n=== ana_16 ===")
df['fragility_8'] = df['gestation_8_duration_closed'] - df['gestation_8_duration']
df['fragility_20'] = df['gestation_20_duration_closed'] - df['gestation_20_duration']
print("Cities with biggest 8-week fragility (drive when nearest clinic closes):")
top_frag_8 = df.nlargest(15, 'fragility_8')[['city','state','population','gestation_8_duration','gestation_8_duration_closed','fragility_8']]
print(top_frag_8.to_string(index=False))

# --- ana_17: closure fragility 20 weeks ---
print("\n=== ana_17 ===")
print("Cities with biggest 20-week fragility:")
top_frag_20 = df.nlargest(15, 'fragility_20')[['city','state','population','gestation_20_duration','gestation_20_duration_closed','fragility_20']]
print(top_frag_20.to_string(index=False))

# --- ana_18: zero-time cities (clinic in/near city) — share by gestation ---
print("\n=== ana_18 ===")
print("share of cities with 0h round-trip (clinic in or adjacent to city):")
for c, label in [('gestation_8_duration','8 wk'),('gestation_12_duration','12 wk'),
                  ('gestation_16_duration','16 wk'),('gestation_20_duration','20 wk')]:
    n = (df[c]==0).sum()
    pct = n/len(df)*100
    pop_pct = df.loc[df[c]==0,'population'].sum()/df['population'].sum()*100
    print(f"  {label}: {n} cities ({pct:.1f}%) | pop coverage {pop_pct:.1f}%")
