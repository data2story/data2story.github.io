"""Stage 2 - Analyst: residuals — who is over- and under-detected vs the OECD-implied prediction."""
import pandas as pd
import numpy as np

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/13_covid19"
pred = pd.read_csv(f"{DATA}/PredictedCases.csv")

# Predicted cases = exp(NoPopModPredictedLogCases)
# Reported cases = pred['cases']
# Residual log = LogCases - NoPopModPredictedLogCases  (positive = over-reporting / over-detection)
pred = pred.sort_values('NoPopModResidualLogCases')

# --- ana_04: Bottom 15 (most under-detected vs prediction) ---
print("=== ana_04 ===")
print("Most UNDER-detected — countries reporting far fewer cases than tourism flows would predict:")
bot = pred.head(15).copy()
bot['multiple_below'] = bot['NoPopModPredictedCases'] / np.maximum(bot['cases'], 1)
print(f"{'Country':25s}  {'OECD':5s}  {'Reported':>9s}  {'Predicted':>10s}  {'Resid(log)':>10s}  {'Implied×':>9s}")
for _, r in bot.iterrows():
    flag = "OECD" if r['oecd'] else "    "
    print(f"  {r['country']:23s}  {flag:5s}  {int(r['cases']):>9,}  {r['NoPopModPredictedCases']:>10.1f}  {r['NoPopModResidualLogCases']:>10.2f}  {r['multiple_below']:>9.1f}")

# --- ana_05: Top 15 (most over-detected vs prediction) ---
print("\n=== ana_05 ===")
print("Most OVER-detected — countries reporting more cases than tourism alone would predict:")
top = pred.tail(15).iloc[::-1]
print(f"{'Country':25s}  {'OECD':5s}  {'Reported':>9s}  {'Predicted':>10s}  {'Resid(log)':>10s}")
for _, r in top.iterrows():
    flag = "OECD" if r['oecd'] else "    "
    print(f"  {r['country']:23s}  {flag:5s}  {int(r['cases']):>9,}  {r['NoPopModPredictedCases']:>10.1f}  {r['NoPopModResidualLogCases']:>10.2f}")

# --- ana_06: OECD vs non-OECD residual distribution ---
print("\n=== ana_06 ===")
oecd_resid = pred[pred['oecd'] == True]['NoPopModResidualLogCases']
non_resid = pred[pred['oecd'] == False]['NoPopModResidualLogCases']
print(f"OECD countries (n={len(oecd_resid)}):")
print(f"  Mean residual (log): {oecd_resid.mean():+.3f}")
print(f"  Median residual:     {oecd_resid.median():+.3f}")
print(f"  SD:                  {oecd_resid.std():.3f}")
print(f"Non-OECD countries (n={len(non_resid)}):")
print(f"  Mean residual (log): {non_resid.mean():+.3f}")
print(f"  Median residual:     {non_resid.median():+.3f}")
print(f"  SD:                  {non_resid.std():.3f}")
print(f"\nDifference (non-OECD mean - OECD mean): {non_resid.mean() - oecd_resid.mean():+.3f} log-units")
print(f"Translated: non-OECD countries report on average exp({non_resid.mean() - oecd_resid.mean():.2f}) = {np.exp(non_resid.mean() - oecd_resid.mean()):.2f}x the OECD level relative to prediction.")

# Count by sign
print(f"\nNon-OECD countries below the OECD line: {(non_resid < 0).sum()} of {len(non_resid)} ({(non_resid<0).mean()*100:.0f}%)")
print(f"OECD countries below their own line: {(oecd_resid < 0).sum()} of {len(oecd_resid)} ({(oecd_resid<0).mean()*100:.0f}%)")
