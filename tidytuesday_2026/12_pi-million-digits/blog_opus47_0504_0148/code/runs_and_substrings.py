"""Longest run of each digit; first occurrence of famous substrings; '0123456789' search."""
import pandas as pd
import numpy as np

CSV = "/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/12_pi-million-digits/pi_digits.csv"
df = pd.read_csv(CSV)
digits_arr = df['digit'].to_numpy()
N = len(digits_arr)
# Convert to string for substring searches.
# Position 1 corresponds to the '3' (integer part). Decimals are positions 2..N.
# But the standard convention "decimal place 762" counts from the first digit AFTER the decimal point.
# So decimal place k = digit_position k+1 in this dataset.
pi_str = "".join(str(d) for d in digits_arr)
print(f"len(pi_str) = {len(pi_str)} (positions 1..{N})")
print(f"first 30 digits: {pi_str[:30]}")
# Decimal-only substring (drop the leading '3'); index 0 in pi_decimal corresponds to decimal place 1.
pi_decimal = pi_str[1:]
print(f"first 30 decimals: {pi_decimal[:30]}")

# --- ana_08: Longest run of each digit and where it starts (in decimals) ---
print("=== ana_08 ===")
import re
run_rows = []
for d in range(10):
    pat = re.compile(f"({d})\\1+")
    best_len = 0
    best_pos = -1
    for m in pat.finditer(pi_decimal):
        L = m.end() - m.start()
        if L > best_len:
            best_len = L
            best_pos = m.start() + 1  # 1-indexed decimal place
    # Single occurrences (run length 1) won't be matched by the regex above; min run length is 2.
    # Check: does that digit appear at all? Of course it does, but we want runs >=2.
    # If best_len is 0, fall back to length 1 by finding first occurrence.
    if best_len == 0:
        idx = pi_decimal.find(str(d))
        best_len = 1
        best_pos = idx + 1
    run_rows.append((d, best_len, best_pos))
    print(f"digit {d}: longest run = {best_len}, starts at decimal place {best_pos}")

# --- ana_09: Feynman point — first run of 4, 5, 6 of any single digit ---
print("=== ana_09 ===")
# Find first run of length k for k=4,5,6,7
for k in [3, 4, 5, 6, 7]:
    pat = re.compile(r"(\d)\1{" + str(k-1) + r",}")
    m = pat.search(pi_decimal)
    if m:
        print(f"first run of length >= {k}: '{m.group(0)}' starts at decimal place {m.start()+1} (digit {m.group(1)})")
    else:
        print(f"first run of length >= {k}: none found in {len(pi_decimal)} decimals")

# --- ana_10: First occurrence of famous substrings ---
print("=== ana_10 ===")
# Substrings: 0123456789, 9876543210, the digits of e (271828182845), birthdates examples, the answer 42, leet 1337, beast 666
# We're searching in decimals (so we don't accidentally include the leading 3).
queries = [
    ("0123456789", "ten digits ascending"),
    ("9876543210", "ten digits descending"),
    ("314159", "first 6 digits of pi (self-reference)"),
    ("271828", "first 6 digits of e"),
    ("999999", "Feynman point"),
    ("000000", "six zeros"),
    ("888888", "six eights"),
    ("1234", "1234"),
    ("0000", "0000"),
    ("42", "the answer 42"),
    ("666", "beast 666"),
    ("123456", "six ascending"),
    ("123456789", "nine ascending"),
]
for q, desc in queries:
    idx = pi_decimal.find(q)
    pos = idx + 1 if idx >= 0 else None
    print(f"  '{q}' ({desc}): {'first occurrence at decimal place ' + str(pos) if pos else 'NOT FOUND in first 1,000,000 decimals'}")

# --- ana_11: Birthday hit-rate — what fraction of 6-digit MMDDYY (or any 6-digit string) appears? ---
print("=== ana_11 ===")
# Distinct 6-digit strings present somewhere in the first million decimals
# We can compute this with a sliding window.
present = set()
for i in range(len(pi_decimal) - 5):
    present.add(pi_decimal[i:i+6])
total_possible = 10**6
hit_rate = len(present) / total_possible
print(f"distinct 6-digit strings present: {len(present):,} / {total_possible:,} = {100*hit_rate:.2f}%")
# also length 5 and length 7
for L in [4, 5, 6, 7]:
    s = set()
    for i in range(len(pi_decimal) - L + 1):
        s.add(pi_decimal[i:i+L])
    print(f"  length-{L} coverage: {len(s):,} / {10**L:,} = {100*len(s)/10**L:.2f}%")

# --- ana_12: Where does the digit-pair "00" through "99" first appear? ---
print("=== ana_12 ===")
pair_first = []
for d1 in range(10):
    for d2 in range(10):
        s = f"{d1}{d2}"
        idx = pi_decimal.find(s)
        pair_first.append((s, idx + 1))
pair_first.sort(key=lambda x: x[1])
print("first 5 pairs to appear (earliest):")
for s, p in pair_first[:5]:
    print(f"  '{s}' at decimal {p}")
print("last 5 pairs to appear (latest first appearance):")
for s, p in pair_first[-5:]:
    print(f"  '{s}' at decimal {p}")
