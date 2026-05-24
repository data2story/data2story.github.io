"""Profile the launches and agencies datasets."""
import pandas as pd

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/01_space-launches'

launches = pd.read_csv(f'{DATA}/launches.csv')
agencies = pd.read_csv(f'{DATA}/agencies.csv')

# --- ana_00: Profile ---
print("=== ana_00 ===")
print(f"launches rows={len(launches)}, cols={len(launches.columns)}")
print(f"years: {launches.launch_year.min()}-{launches.launch_year.max()}")
print(f"agencies rows={len(agencies)}")
print(f"unique agencies in launches: {launches.agency.nunique()}")
print(f"unique state_codes: {launches.state_code.nunique()}")
print(f"missing agency_type: {launches.agency_type.isna().sum()}")
