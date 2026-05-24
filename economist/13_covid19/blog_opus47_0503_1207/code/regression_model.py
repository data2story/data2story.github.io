"""Stage 2 - Analyst: replicate the OECD-only OLS log-tourism -> log-cases regression."""
import pandas as pd
import numpy as np
import statsmodels.api as sm

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/13_covid19"
pred = pd.read_csv(f"{DATA}/PredictedCases.csv")
cov = pd.read_csv(f"{DATA}/covid_cases_and_covariates_march_4_selected.csv")

# --- ana_02: Replicate OECD-only OLS regression ---
print("=== ana_02 ===")
oecd = pred[pred['oecd'] == True].copy()
non_oecd = pred[pred['oecd'] == False].copy()
print(f"OECD countries in fit: {len(oecd)}")
print(f"Non-OECD countries (held out / scored only): {len(non_oecd)}")

X = sm.add_constant(oecd['LogTourists'])
y = oecd['LogCases']
model = sm.OLS(y, X).fit()
print(model.summary().as_text())

intercept, slope = model.params['const'], model.params['LogTourists']
r2 = model.rsquared
n = int(model.nobs)
p = model.f_pvalue
print(f"\nIntercept: {intercept:.4f}")
print(f"Slope (LogTourists coef): {slope:.4f}")
print(f"R-squared: {r2:.4f}")
print(f"F p-value: {p:.3e}")
print(f"n: {n}")

# --- ana_03: Tourism distribution across countries ---
print("\n=== ana_03 ===")
mean_tour = (cov['outbound_tour_groups_Q3_2019_improved'] +
             cov['inbound_tour_groups_Q3_2019_1_improved']) / 2
cov['mean_tour'] = mean_tour
top_tour = cov.sort_values('mean_tour', ascending=False).head(15)
print("Top 15 countries by mean Chinese tour-group flows (Q3 2019):")
for _, row in top_tour.iterrows():
    flag = "OECD" if row['oecd'] else "    "
    print(f"  {flag}  {row['country']:25s}  {int(row['mean_tour']):>10,}")
print(f"\nTotal mean flow across all 124 countries: {int(mean_tour.sum()):,}")
print(f"OECD share of total flow: {(cov[cov.oecd==True]['mean_tour'].sum() / mean_tour.sum() * 100):.1f}%")
print(f"Top 10 share of total flow: {(top_tour.head(10)['mean_tour'].sum() / mean_tour.sum() * 100):.1f}%")
