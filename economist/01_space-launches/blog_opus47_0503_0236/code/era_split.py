"""Cold War vs post-Cold War splits, by bloc."""
import pandas as pd

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/01_space-launches'
launches = pd.read_csv(f'{DATA}/launches.csv')

def bloc(s):
    if s in ('SU', 'RU'):
        return 'USSR/Russia'
    if s == 'US':
        return 'United States'
    if s == 'CN':
        return 'China'
    return 'Other'

launches['bloc'] = launches.state_code.map(bloc)

# --- ana_15: Cold War (1957-1991) bloc share ---
print("=== ana_15 ===")
cw = launches[launches.launch_year <= 1991].bloc.value_counts()
total_cw = cw.sum()
print(f"Cold War launches total: {total_cw}")
for b, c in cw.items():
    print(f"{b}: {c} ({c/total_cw*100:.1f}%)")

# --- ana_16: Post-Cold War (1992-2018) bloc share ---
print("=== ana_16 ===")
pc = launches[launches.launch_year >= 1992].bloc.value_counts()
total_pc = pc.sum()
print(f"Post-Cold War launches total: {total_pc}")
for b, c in pc.items():
    print(f"{b}: {c} ({c/total_pc*100:.1f}%)")

# --- ana_17: state_code rank, full ---
print("=== ana_17 ===")
state_names = {
    'SU': 'Soviet Union', 'RU': 'Russia', 'US': 'United States', 'CN': 'China',
    'F': 'France', 'J': 'Japan', 'IN': 'India', 'I-ESA': 'ESA',
    'IL': 'Israel', 'I': 'Italy', 'IR': 'Iran', 'KP': 'North Korea',
    'CYM': 'Cayman/Sea Launch', 'I-ELDO': 'ELDO (Europe)', 'KR': 'South Korea',
    'BR': 'Brazil', 'UK': 'United Kingdom'
}
sc = launches.state_code.value_counts()
total = sc.sum()
for s, c in sc.items():
    print(f"{s} | {state_names.get(s, s)} | {c} | {c/total*100:.2f}%")

# --- ana_18: 2018 cadence by bloc — China surpasses everyone ---
print("=== ana_18 ===")
b2018 = launches[launches.launch_year == 2018].bloc.value_counts()
print(f"2018 (partial through Oct): total {b2018.sum()}")
for b, c in b2018.items():
    print(f"{b}: {c}")

# --- ana_19: Post-2010 startup acceleration ---
print("=== ana_19 ===")
startup_yearly = launches[launches.agency_type == 'startup'].groupby('launch_year').size()
print("Startup launches per year:")
for y, c in startup_yearly.items():
    print(f"{y}: {c}")
print(f"\nFirst startup year: {startup_yearly.index.min()}")
print(f"Total startup launches 2017-2018: {startup_yearly[startup_yearly.index >= 2017].sum()}")
print(f"Total startup launches all years: {startup_yearly.sum()}")
