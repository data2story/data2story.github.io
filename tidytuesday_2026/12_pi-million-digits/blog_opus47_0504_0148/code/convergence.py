"""Running cumulative frequency of each digit — when does it 'settle' near 10%?"""
import pandas as pd
import numpy as np
import json

CSV = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/12_pi-million-digits/pi_digits.csv"
df = pd.read_csv(CSV)
digits = df['digit'].to_numpy()
N = len(digits)

# --- ana_13: Cumulative frequency vs n at log-spaced sample points ---
print("=== ana_13 ===")
# Use log-spaced n: 10, 30, 100, 300, 1k, 3k, 10k, 30k, 100k, 300k, 1M
sample_ns = [10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000, 1000000]
header = "n," + ",".join(f"d{d}" for d in range(10))
print(header)
table_rows = []
for n in sample_ns:
    counts = np.bincount(digits[:n], minlength=10)
    pcts = [100.0 * c / n for c in counts]
    print(f"{n}," + ",".join(f"{p:.3f}" for p in pcts))
    table_rows.append([n] + [round(p, 4) for p in pcts])

# --- ana_14: When does each digit first stay within +/- 0.1pp of 10%? ---
print("=== ana_14 ===")
# For each digit, walk through n=1..N, track running pct, find smallest n* such that for all m>=n* the running pct stays within 9.9% to 10.1%.
# We compute backward: for each m, is the running pct in [9.9, 10.1]? Then n* is the last m where it left the band, +1.
# But that's expensive if we did it naively. Instead, build cumulative counts in O(N) once.
cum = np.zeros((10, N), dtype=np.float64)
for d in range(10):
    cum[d, :] = np.cumsum(digits == d)
ns = np.arange(1, N + 1)
results = []
for d in range(10):
    pct = 100.0 * cum[d, :] / ns
    in_band = np.abs(pct - 10.0) <= 0.1
    # last index where pct is OUTSIDE band
    if in_band.all():
        settle_n = 1
    else:
        last_outside = np.where(~in_band)[0].max()
        # require not just last outside, but also that we have enough digits afterwards
        if last_outside == N - 1:
            settle_n = None  # never settled
        else:
            settle_n = int(last_outside + 2)  # 1-indexed: position right after last violation
    results.append((d, settle_n))
    print(f"digit {d}: settles within +/-0.1pp of 10% at n = {settle_n}")

# --- ana_15: Cumulative frequency curve data for chart (every digit at log-spaced points) ---
print("=== ana_15 ===")
# Long-format table: (n, digit, pct)
chart_ns = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
chart_rows = []
for n in chart_ns:
    counts = np.bincount(digits[:n], minlength=10)
    for d in range(10):
        pct = 100.0 * counts[d] / n
        chart_rows.append([n, d, round(pct, 4)])
print(f"chart_rows count: {len(chart_rows)}")

# Dump for designer/programmer
with open("/Users/forrest/Desktop/data2blog/project/tidytuesday_2026/12_pi-million-digits/blog_opus47_0504_0148/code/_convergence_dump.json", "w") as f:
    json.dump({"sample_ns": sample_ns, "log_table": table_rows, "settled": [(int(d), s) for d, s in results], "chart_rows": chart_rows}, f, indent=2)
print("dumped _convergence_dump.json")
