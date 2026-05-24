"""Per-digit frequencies, chi-squared vs uniform, 95% CI per digit."""
import pandas as pd
import numpy as np
from scipy import stats

CSV = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/12_pi-million-digits/pi_digits.csv"

df = pd.read_csv(CSV)

# Use ALL million-and-one digits (the leading 3 plus 1,000,000 decimals).
digits = df['digit'].to_numpy()
N = len(digits)
counts = np.bincount(digits, minlength=10)
expected = N / 10.0

# --- ana_01: Per-digit counts and percentages ---
print("=== ana_01 ===")
print(f"N = {N}")
print(f"expected per digit = {expected}")
rows = []
for d in range(10):
    c = int(counts[d])
    pct = 100.0 * c / N
    se = np.sqrt(0.1 * 0.9 / N)
    ci_lo = (c / N - 1.96 * se) * 100
    ci_hi = (c / N + 1.96 * se) * 100
    dev_pp = pct - 10.0
    rows.append((d, c, round(pct, 4), round(ci_lo, 4), round(ci_hi, 4), round(dev_pp, 4)))
    print(f"digit {d}: count={c:>7d}, pct={pct:.4f}%, dev={dev_pp:+.4f}pp, 95%CI=[{ci_lo:.4f},{ci_hi:.4f}]")

# --- ana_02: Chi-squared goodness-of-fit vs uniform ---
print("=== ana_02 ===")
chi2, p = stats.chisquare(counts, [expected]*10)
print(f"chi2 = {chi2:.4f}")
print(f"df = 9")
print(f"p-value = {p:.4f}")
print(f"Critical chi2 at alpha=0.05, df=9: {stats.chi2.ppf(0.95, 9):.4f}")
# strong = clearly unusual; weak = consistent with uniform

# --- ana_03: Most/least common digit, max deviation ---
print("=== ana_03 ===")
order = np.argsort(counts)
print(f"least frequent digit: {order[0]} with {counts[order[0]]}")
print(f"most  frequent digit: {order[-1]} with {counts[order[-1]]}")
print(f"max|count - expected| = {max(abs(counts - expected))}")
print(f"max deviation in pp: {100*max(abs(counts/N - 0.1)):.4f}")
