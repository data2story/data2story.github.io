"""Agency-level analysis — types, top agencies, the SpaceX rise."""
import pandas as pd

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/01_space-launches'
launches = pd.read_csv(f'{DATA}/launches.csv')

# --- ana_04: agency_type breakdown total + over time ---
print("=== ana_04 ===")
total = launches.agency_type.value_counts()
print(f"TOTAL by agency_type:")
print(total)
print(f"% breakdown: state={total['state']/total.sum()*100:.1f}%, private={total['private']/total.sum()*100:.1f}%, startup={total['startup']/total.sum()*100:.1f}%")

# yearly by agency_type
yearly_type = launches.groupby(['launch_year', 'agency_type']).size().unstack(fill_value=0).reset_index()
print(f"\nYEARLY by agency_type:")
print(yearly_type.to_string(index=False))

# --- ana_05: Startups appear after 2008 ---
print("=== ana_05 ===")
first_startup = launches[launches.agency_type=='startup'].launch_year.min()
print(f"First startup launch year: {first_startup}")
startup_yearly = launches[launches.agency_type=='startup'].groupby('launch_year').size()
print(startup_yearly)
print(f"startups 2014-2018 total: {launches[(launches.agency_type=='startup') & (launches.launch_year>=2014)].shape[0]}")

# --- ana_06: Top 15 agencies all-time ---
print("=== ana_06 ===")
top = launches.agency.value_counts().head(15)
print(top)

# --- ana_07: Top agencies in 2018 ---
print("=== ana_07 ===")
top_2018 = launches[launches.launch_year==2018].agency.value_counts().head(15)
print(top_2018)

# --- ana_08: SpaceX's rise (yearly count) ---
print("=== ana_08 ===")
spacex = launches[launches.agency=='SPX'].groupby('launch_year').size()
print(spacex)
print(f"SPX first year: {spacex.index.min()}, 2018: {spacex.iloc[-1] if 2018 in spacex.index else 'NA'}")
print(f"SPX total: {spacex.sum()}")

# --- ana_09: SPX cumulative ---
print("=== ana_09 ===")
print(spacex.cumsum())
