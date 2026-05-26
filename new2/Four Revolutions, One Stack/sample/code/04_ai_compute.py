"""AI training compute analysis from core__ai-notable-models.csv (1950-2026, 1018 models).

Produces ana_11..ana_14.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(r"D:/AI/journalist agent review/phase2/datasets/energy_revolutions/data")

ai = pd.read_csv(DATA_DIR / "core__ai-notable-models.csv")
ai["Publication date"] = pd.to_datetime(ai["Publication date"], errors="coerce")
ai["pub_year"] = ai["Publication date"].dt.year
# Coerce numeric cols
for c in ["Training compute (FLOP)", "Training power draw (W)", "Training compute cost (2023 USD)", "Parameters"]:
    ai[c] = pd.to_numeric(ai[c], errors="coerce")


# --- ana_11: Training compute over time — full series + by-year median (log) ---
print("=== ana_11 ===")
have = ai.dropna(subset=["pub_year", "Training compute (FLOP)"])
print(f"Models with both pub_year and Training compute: {len(have)} of {len(ai)}")
print(f"Year range: {int(have.pub_year.min())}-{int(have.pub_year.max())}")
by_year = have.groupby(have.pub_year.astype(int))["Training compute (FLOP)"].agg(["count", "median", "max"]).reset_index()
by_year.columns = ["Year", "n_models", "median_FLOP", "max_FLOP"]
print(by_year.head(5).to_string(index=False))
print("...")
print(by_year.tail(10).to_string(index=False))


# --- ana_12: Doubling time of frontier training compute, pre-2010 vs post-2010 ---
print("\n=== ana_12 ===")
def doubling_time_from_log_slope(df_):
    # Fit log10(max_FLOP) ~ a + b*Year
    x = df_.Year.astype(float).values
    y = np.log10(df_.max_FLOP.values)
    b, a = np.polyfit(x, y, 1)
    # Doubling time = log10(2) / b years
    dt = np.log10(2) / b if b > 0 else float("inf")
    return b, dt
pre = by_year[(by_year.Year >= 1950) & (by_year.Year < 2010) & by_year.max_FLOP.notna()]
post = by_year[(by_year.Year >= 2010) & by_year.max_FLOP.notna()]
b_pre, dt_pre = doubling_time_from_log_slope(pre)
b_post, dt_post = doubling_time_from_log_slope(post)
print(f"Pre-2010 ({len(pre)} years): log10 slope = {b_pre:.4f}/yr  =>  doubling time = {dt_pre*12:.1f} months")
print(f"Post-2010 ({len(post)} years): log10 slope = {b_post:.4f}/yr  =>  doubling time = {dt_post*12:.1f} months")
print(f"Acceleration factor: {dt_pre/dt_post:.2f}x faster after 2010")

# Frontier model compute by year (max)
print("\n(reference) Max training compute by year, post-2010:")
print(post[["Year", "max_FLOP", "n_models"]].to_string(index=False))


# --- ana_13: Top 15 highest-compute models with names + dates ---
print("\n=== ana_13 ===")
top = ai.dropna(subset=["Training compute (FLOP)"]).nlargest(15, "Training compute (FLOP)")
for _, r in top[["Model", "Organization", "Publication date", "Training compute (FLOP)", "Training power draw (W)"]].iterrows():
    pd_s = r["Publication date"].strftime("%Y-%m-%d") if pd.notna(r["Publication date"]) else "n/a"
    pw = f"{r['Training power draw (W)']:.2e} W" if pd.notna(r["Training power draw (W)"]) else "n/a"
    print(f"  {r.Model[:35]:35s}  {str(r.Organization)[:25]:25s}  {pd_s}  FLOP={r['Training compute (FLOP)']:.2e}  Pwr={pw}")


# --- ana_14: Training power draw of frontier AI models over time ---
print("\n=== ana_14 ===")
pw = ai.dropna(subset=["pub_year", "Training power draw (W)"])
print(f"Models with pub_year + power draw: {len(pw)}")
pw_by_year = pw.groupby(pw.pub_year.astype(int))["Training power draw (W)"].agg(["count", "median", "max"]).reset_index()
pw_by_year.columns = ["Year", "n_models", "median_W", "max_W"]
print(pw_by_year.tail(15).to_string(index=False))
# Compute median power draw for frontier (top-decile by compute) per year, post-2015
print("\nMax training power by year, post-2015:")
for y in range(2015, 2027):
    r = pw_by_year[pw_by_year.Year == y]
    if not r.empty:
        print(f"  {y}: {r.max_W.iloc[0]:.2e} W  (n={int(r.n_models.iloc[0])})")
