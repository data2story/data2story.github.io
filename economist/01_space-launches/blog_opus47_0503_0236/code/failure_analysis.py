"""Failure rate analysis — by decade, by agency_type."""
import pandas as pd

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/01_space-launches'
launches = pd.read_csv(f'{DATA}/launches.csv')
launches['decade'] = (launches.launch_year // 10) * 10
launches['failed'] = (launches.category == 'F').astype(int)

# --- ana_10: Failure rate by decade ---
print("=== ana_10 ===")
fr = launches.groupby('decade').agg(total=('category','size'), failures=('failed','sum'))
fr['fail_pct'] = fr.failures / fr.total * 100
print(fr.to_string())

# --- ana_11: Failure rate by agency_type ---
print("=== ana_11 ===")
ft = launches.groupby('agency_type').agg(total=('category','size'), failures=('failed','sum'))
ft['fail_pct'] = ft.failures / ft.total * 100
print(ft.to_string())

# --- ana_12: Total launches and successful launches ---
print("=== ana_12 ===")
print(f"Total launches: {len(launches)}")
print(f"Successful: {(launches.category=='O').sum()}")
print(f"Failed: {(launches.category=='F').sum()}")
print(f"Overall fail %: {(launches.category=='F').mean()*100:.2f}")
