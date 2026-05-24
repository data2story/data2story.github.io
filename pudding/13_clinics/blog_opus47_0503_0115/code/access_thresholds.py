"""Compute share of cities + share of US urban population at each round-trip
threshold, for each gestation, in the open and closed scenarios.

These are the headline distributions the Pudding piece relied on.
"""
import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/13_clinics/cities.csv"
df = pd.read_csv(DATA)

GEST_COLS = {
    8:  ('gestation_8_duration',  'gestation_8_duration_closed'),
    12: ('gestation_12_duration', 'gestation_12_duration_closed'),
    16: ('gestation_16_duration', 'gestation_16_duration_closed'),
    20: ('gestation_20_duration', 'gestation_20_duration_closed'),
}

THRESHOLDS = [0, 1, 2, 4, 6]

# --- ana_04: pct of cities at each threshold by gestation (open) ---
print("=== ana_04 ===")
print("pct of CITIES at each round-trip threshold (open scenario):")
print("week\t\t" + "\t".join(f">={t}h" for t in THRESHOLDS))
for wk, (open_c, _) in GEST_COLS.items():
    s = df[open_c]
    pcts = [(s>=t).mean()*100 for t in THRESHOLDS]
    print(f"{wk}wk\t\t" + "\t".join(f"{p:.1f}%" for p in pcts))

# --- ana_05: pct of POPULATION at each threshold by gestation (open) ---
print("\n=== ana_05 ===")
print("pct of POPULATION at each round-trip threshold (open scenario):")
total_pop = df['population'].sum()
print("week\t\t" + "\t".join(f">={t}h" for t in THRESHOLDS))
for wk, (open_c, _) in GEST_COLS.items():
    s = df[open_c]
    pcts = [df.loc[s>=t,'population'].sum()/total_pop*100 for t in THRESHOLDS]
    print(f"{wk}wk\t\t" + "\t".join(f"{p:.1f}%" for p in pcts))

# --- ana_06: closed scenario at week 8 — fragility ---
print("\n=== ana_06 ===")
print("CLOSED scenario at 8 weeks — what happens if the closest clinic shuts:")
print("week\t\t" + "\t".join(f">={t}h" for t in THRESHOLDS))
for wk, (open_c, closed_c) in GEST_COLS.items():
    s = df[closed_c]
    pcts = [(s>=t).mean()*100 for t in THRESHOLDS]
    print(f"{wk}wk_closed\t" + "\t".join(f"{p:.1f}%" for p in pcts))

# --- ana_07: 1h round-trip threshold (the Pudding's headline 151 cities) ---
print("\n=== ana_07 ===")
g8 = df['gestation_8_duration']
g8c = df['gestation_8_duration_closed']
n_lack = (g8>=1).sum()
print(f"cities lacking 'within 1h round-trip' at 8 weeks (open): {n_lack}")
print(f"cities lacking 'within 1h round-trip' at 8 weeks (closed scenario): {(g8c>=1).sum()}")
n_lack16 = (df['gestation_16_duration']>=1).sum()
n_lack20 = (df['gestation_20_duration']>=1).sum()
print(f"cities lacking 1h round-trip at 16 weeks: {n_lack16}")
print(f"cities lacking 1h round-trip at 20 weeks: {n_lack20}")
