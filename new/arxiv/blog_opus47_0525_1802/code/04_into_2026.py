"""Extend the submission story into 2026 using the full-history monthly file.
The per-category/per-archive files stop at 2025-10, but get_monthly_submissions.csv
runs to 2026-05, so total monthly output (not category breakdown) is available for 2026.
Run from anywhere. Finding prefixed `=== ana_xx ===`."""
import pandas as pd

DATA = "/Users/forrest/Desktop/data2story-skill/data/arxiv"
hist = pd.read_csv(f"{DATA}/get_monthly_submissions.csv")

# --- ana_24: Into 2026 — the climb continues, first 30k month ---
print("=== ana_24 ===")
# Monthly total submissions, 2023-01 onward (full-history file; not category-capped)
win = hist[hist["month"] >= "2023-01"].copy()
print("window:", win["month"].iloc[0], "->", win["month"].iloc[-1], "| n =", len(win))

# All-time monthly record
mx = hist.loc[hist["submissions"].idxmax()]
print("all-time monthly record:", mx["month"], int(mx["submissions"]))

# 2026 so far (May 2026 is a month in progress as of 2026-05-25)
y26 = hist[hist["month"].str.startswith("2026")]
print("2026 months:")
print(y26[["month", "submissions"]].to_string(index=False))

# Year-over-year, like-for-like Jan-May window
m5 = ["-01", "-02", "-03", "-04", "-05"]
s26 = hist[hist["month"].isin([f"2026{m}" for m in m5])]["submissions"].sum()
s25 = hist[hist["month"].isin([f"2025{m}" for m in m5])]["submissions"].sum()
print(f"Jan-May total: 2025={s25}  2026={s26}  YoY={100*(s26-s25)/s25:.1f}%")
