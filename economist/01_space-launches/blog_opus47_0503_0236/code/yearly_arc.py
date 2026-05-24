"""Yearly launch arcs — global, Cold War, and modern."""
import pandas as pd

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/01_space-launches'
launches = pd.read_csv(f'{DATA}/launches.csv')

# --- ana_01: Yearly global launches 1957-2018 ---
print("=== ana_01 ===")
yearly = launches.groupby('launch_year').size().reset_index(name='count')
print(yearly.to_string(index=False))
peak = yearly.loc[yearly['count'].idxmax()]
trough = yearly[yearly.launch_year >= 1965].loc[yearly[yearly.launch_year >= 1965]['count'].idxmin()]
print(f"\nPEAK: {int(peak.launch_year)} with {int(peak['count'])} launches")
print(f"POST-1965 TROUGH: {int(trough.launch_year)} with {int(trough['count'])} launches")
print(f"2018 (partial): {int(yearly[yearly.launch_year==2018]['count'].iloc[0])}")
print(f"1957: {int(yearly[yearly.launch_year==1957]['count'].iloc[0])}")
# line 18

# --- ana_02: Yearly cadence by superpower bloc (USSR+RU vs US vs China vs Other) ---
print("=== ana_02 ===")
def bloc(s):
    if s in ('SU', 'RU'):
        return 'USSR/Russia'
    if s == 'US':
        return 'United States'
    if s == 'CN':
        return 'China'
    return 'Other'
launches['bloc'] = launches.state_code.map(bloc)
by_bloc = launches.groupby(['launch_year', 'bloc']).size().unstack(fill_value=0).reset_index()
print(by_bloc.to_string(index=False))

# --- ana_03: Soviet peak vs current state ---
print("=== ana_03 ===")
sov_peak = launches[launches.state_code=='SU'].groupby('launch_year').size()
print(f"Soviet peak year: {sov_peak.idxmax()} with {sov_peak.max()} launches")
print(f"Soviet final year: 1991 with {launches[(launches.state_code=='SU') & (launches.launch_year==1991)].shape[0]}")
ru_2018 = launches[(launches.state_code=='RU') & (launches.launch_year==2018)].shape[0]
print(f"Russia 2018: {ru_2018}")
us_peak = launches[launches.state_code=='US'].groupby('launch_year').size()
print(f"US peak: {us_peak.idxmax()} with {us_peak.max()} launches")
us_2018 = launches[(launches.state_code=='US') & (launches.launch_year==2018)].shape[0]
print(f"US 2018: {us_2018}")
cn_2018 = launches[(launches.state_code=='CN') & (launches.launch_year==2018)].shape[0]
print(f"China 2018: {cn_2018}")
cn_1990 = launches[(launches.state_code=='CN') & (launches.launch_year==1990)].shape[0]
print(f"China 1990: {cn_1990}")
