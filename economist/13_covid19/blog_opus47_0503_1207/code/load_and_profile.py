"""Stage 2 - Analyst: dataset profiling for the COVID-19 tourism-flows analysis."""
import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/13_covid19"

jh = pd.read_csv(f"{DATA}/03-04-2020_JH_cases.csv")
tour = pd.read_csv(f"{DATA}/chinese_tourism.csv")
pred = pd.read_csv(f"{DATA}/PredictedCases.csv")
cov = pd.read_csv(f"{DATA}/covid_cases_and_covariates_march_4_selected.csv")

# --- ana_profile: Dataset profile ---
print("=== ana_profile ===")
print("Files:")
print(f"  03-04-2020_JH_cases.csv  rows={len(jh)}  cols={jh.shape[1]}  -- one row per region/state")
print(f"  chinese_tourism.csv      rows={len(tour)}  cols={tour.shape[1]}  -- one row per country")
print(f"  PredictedCases.csv       rows={len(pred)}  cols={pred.shape[1]}  -- one row per country (model output)")
print(f"  covid_cases_and_covariates_march_4_selected.csv rows={len(cov)}  cols={cov.shape[1]} -- one row per country (full covariates)")
print(f"\nJHU date range: 2020-03-04 (single snapshot)")
print(f"Continents in tourism data: {sorted(tour['continent'].unique().tolist())}")
print(f"OECD countries: {(cov['oecd']==True).sum()}")
print(f"Non-OECD countries: {(cov['oecd']==False).sum()}")
print(f"Total countries: {len(cov)}")
print(f"\nCountries with zero confirmed cases on 4 Mar 2020: {(cov['cases']==0).sum()}")
print(f"Countries with >0 cases: {(cov['cases']>0).sum()}")
print(f"\nMissing values in PredictedCases:")
print(pred.isna().sum().to_string())
