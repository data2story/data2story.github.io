"""State-level analysis: which states have the longest drives, single-clinic
fragility, and the largest 8 -> 16 week gestation collapse."""
import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/13_clinics/cities.csv"
df = pd.read_csv(DATA)

# --- ana_08: state population-weighted mean drive at each gestation ---
print("=== ana_08 ===")
def pop_weighted_mean(group, col):
    return (group[col]*group['population']).sum()/group['population'].sum()

state_avg = df.groupby('state').apply(lambda g: pd.Series({
    'pop_total': g['population'].sum(),
    'cities': len(g),
    'wk8_drive':  pop_weighted_mean(g, 'gestation_8_duration'),
    'wk12_drive': pop_weighted_mean(g, 'gestation_12_duration'),
    'wk16_drive': pop_weighted_mean(g, 'gestation_16_duration'),
    'wk20_drive': pop_weighted_mean(g, 'gestation_20_duration'),
})).round(2)

print("Top 12 states by 20-week round-trip drive (population-weighted mean):")
top20 = state_avg.sort_values('wk20_drive', ascending=False).head(12)
print(top20.to_string())

# --- ana_09: state 8 -> 20 week collapse magnitude ---
print("\n=== ana_09 ===")
state_avg['collapse_8_to_20'] = state_avg['wk20_drive'] - state_avg['wk8_drive']
state_avg['collapse_8_to_16'] = state_avg['wk16_drive'] - state_avg['wk8_drive']
print("Top 12 states by 8 -> 20 week drive INCREASE (population-weighted):")
print(state_avg.sort_values('collapse_8_to_20', ascending=False).head(12).to_string())

# --- ana_10: closed-scenario state fragility (the second-clinic gap) ---
print("\n=== ana_10 ===")
state_closed = df.groupby('state').apply(lambda g: pd.Series({
    'pop_total': g['population'].sum(),
    'wk8_open':   pop_weighted_mean(g, 'gestation_8_duration'),
    'wk8_closed': pop_weighted_mean(g, 'gestation_8_duration_closed'),
    'wk20_open':  pop_weighted_mean(g, 'gestation_20_duration'),
    'wk20_closed':pop_weighted_mean(g, 'gestation_20_duration_closed'),
})).round(2)
state_closed['fragility_8'] = state_closed['wk8_closed'] - state_closed['wk8_open']
state_closed['fragility_20'] = state_closed['wk20_closed'] - state_closed['wk20_open']
print("Top 12 states by 8-week fragility (gap when nearest clinic closes):")
print(state_closed.sort_values('fragility_8', ascending=False).head(12).to_string())
print()
print("Top 12 states by 20-week fragility:")
print(state_closed.sort_values('fragility_20', ascending=False).head(12).to_string())
