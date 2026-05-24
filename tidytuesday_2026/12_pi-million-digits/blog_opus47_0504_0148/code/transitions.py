"""10x10 transition matrix P[i,j] = Pr(next = j | current = i), plus chi-squared on length-2 strings."""
import pandas as pd
import numpy as np
from scipy import stats
import json

CSV = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/12_pi-million-digits/pi_digits.csv"

df = pd.read_csv(CSV)
digits = df['digit'].to_numpy()
N = len(digits)

# Transition counts
T = np.zeros((10, 10), dtype=np.int64)
np.add.at(T, (digits[:-1], digits[1:]), 1)
n_pairs = N - 1
print(f"N digits = {N}, transitions = {n_pairs}")

# Conditional probabilities P[i,j] = T[i,j] / row_sum
row_sums = T.sum(axis=1, keepdims=True)
Pcond = T / row_sums

# --- ana_04: Self-transition rates (the diagonal) ---
print("=== ana_04 ===")
diag_rows = []
for i in range(10):
    rs = int(row_sums[i, 0])
    self_p = float(Pcond[i, i])
    se = np.sqrt(0.1 * 0.9 / rs)
    pct = 100.0 * self_p
    dev_pp = pct - 10.0
    ci_lo = 100*(self_p - 1.96*se)
    ci_hi = 100*(self_p + 1.96*se)
    diag_rows.append((i, int(T[i, i]), round(pct, 4), round(dev_pp, 4), round(ci_lo, 4), round(ci_hi, 4)))
    print(f"digit {i}: P({i}->{i}) = {pct:.4f}% (dev {dev_pp:+.4f}pp, 95%CI [{ci_lo:.4f},{ci_hi:.4f}])")

# --- ana_05: Full 10x10 transition matrix as percentages ---
print("=== ana_05 ===")
print("conditional P[i,j] in percent, rows = current digit, cols = next digit")
heat_rows = []
for i in range(10):
    row = [round(100.0 * Pcond[i, j], 4) for j in range(10)]
    heat_rows.append([i] + row)
    print(f"row {i}: " + " ".join(f"{v:6.4f}" for v in row))

# --- ana_06: Length-2 string chi-squared (100 cells, df=99) ---
print("=== ana_06 ===")
expected = n_pairs / 100.0
chi2 = ((T - expected) ** 2 / expected).sum()
p = 1 - stats.chi2.cdf(chi2, df=99)
print(f"expected per cell = {expected}")
print(f"chi2 = {chi2:.4f}")
print(f"df = 99")
print(f"p-value = {p:.4f}")
print(f"critical chi2 at alpha=0.05, df=99: {stats.chi2.ppf(0.95, 99):.4f}")

# --- ana_07: Most & least frequent transitions ---
print("=== ana_07 ===")
flat = []
for i in range(10):
    for j in range(10):
        flat.append((i, j, int(T[i, j])))
flat.sort(key=lambda x: x[2])
print("5 least frequent transitions (count):")
for i, j, c in flat[:5]:
    print(f"  {i}->{j}: {c} ({100*c/n_pairs:.4f}%)")
print("5 most frequent transitions (count):")
for i, j, c in flat[-5:]:
    print(f"  {i}->{j}: {c} ({100*c/n_pairs:.4f}%)")

# Save matrix to disk for designer/programmer
out = {
    "T": T.tolist(),
    "Pcond_pct": [[float(round(100*Pcond[i, j], 4)) for j in range(10)] for i in range(10)],
    "row_sums": [int(row_sums[i, 0]) for i in range(10)],
}
with open("/Users/forrest/Desktop/data2blog/project/tidytuesday_2026/12_pi-million-digits/blog_opus47_0504_0148/code/_transitions_dump.json", "w") as f:
    json.dump(out, f, indent=2)
print("dumped _transitions_dump.json")
