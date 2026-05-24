"""Histogram of round-trip drive at each gestation, plus a city-level
slim table for the map (lat/lng + drive at each gestation)."""
import pandas as pd, json

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/13_clinics/cities.csv"
df = pd.read_csv(DATA)

# --- ana_19: histogram of round-trip drive (cities) for each gestation ---
print("=== ana_19 ===")
print("Round-trip drive histogram (cities) per gestation:")
hist_cols = ['gestation_8_duration','gestation_12_duration','gestation_16_duration','gestation_20_duration']
hist = pd.DataFrame({c: df[c].value_counts().sort_index() for c in hist_cols}).fillna(0).astype(int)
print(hist.to_string())

# --- ana_20: histogram (population-weighted) ---
print("\n=== ana_20 ===")
print("Round-trip drive histogram (population-weighted) per gestation:")
def pop_hist(col):
    g = df.groupby(col)['population'].sum()
    return g
ph = pd.DataFrame({c: pop_hist(c) for c in hist_cols}).fillna(0).astype(int)
print(ph.to_string())

# --- ana_21: city-level slim table (for map) ---
print("\n=== ana_21 ===")
# slim columns useful for the map
slim = df[['city','state','population','latitude','longitude',
           'gestation_8_duration','gestation_12_duration','gestation_16_duration','gestation_20_duration',
           'gestation_8_duration_closed','gestation_20_duration_closed']].copy()
print(f"slim_rows={len(slim)}, lat range=[{slim.latitude.min()},{slim.latitude.max()}], "
      f"lng range=[{slim.longitude.min()},{slim.longitude.max()}]")
print("first 5 rows:")
print(slim.head().to_string())

# --- ana_22: gestation collapse curve (mean & population-weighted, per gestation) ---
print("\n=== ana_22 ===")
print("gestation\tcity_mean\tpop_weighted\tpct_pop_zero\tpct_pop_4plus")
total_pop = df['population'].sum()
for wk, c in [(8,'gestation_8_duration'),(12,'gestation_12_duration'),
              (16,'gestation_16_duration'),(20,'gestation_20_duration')]:
    s = df[c]
    pwm = (s*df['population']).sum()/total_pop
    pct_zero = df.loc[s==0,'population'].sum()/total_pop*100
    pct_4 = df.loc[s>=4,'population'].sum()/total_pop*100
    print(f"{wk}\t\t{s.mean():.2f}\t\t{pwm:.2f}\t\t{pct_zero:.1f}\t\t{pct_4:.1f}")

# --- ana_23: same metrics for closed scenario ---
print("\n=== ana_23 ===")
print("CLOSED scenario gestation collapse:")
print("gestation\tcity_mean\tpop_weighted\tpct_pop_zero\tpct_pop_4plus")
for wk, c in [(8,'gestation_8_duration_closed'),(12,'gestation_12_duration_closed'),
              (16,'gestation_16_duration_closed'),(20,'gestation_20_duration_closed')]:
    s = df[c]
    pwm = (s*df['population']).sum()/total_pop
    pct_zero = df.loc[s==0,'population'].sum()/total_pop*100
    pct_4 = df.loc[s>=4,'population'].sum()/total_pop*100
    print(f"{wk}\t\t{s.mean():.2f}\t\t{pwm:.2f}\t\t{pct_zero:.1f}\t\t{pct_4:.1f}")
