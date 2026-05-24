#!/usr/bin/env python3
"""Analysis of AI model iteration speed (aispeed dataset).
Run from DATA_DIR: python3 cadence_analysis.py
All findings tagged with ana_xx markers.
"""
import pandas as pd
import os

DATA = os.environ.get("AISPEED_DATA", "/Users/forrest/Desktop/data2blog-skill/data/aispeed")

cad = pd.read_csv(os.path.join(DATA, "frontier_cadence_by_year.csv"))
gaps = pd.read_csv(os.path.join(DATA, "frontier_release_gaps.csv"))
mpy = pd.read_csv(os.path.join(DATA, "models_per_year.csv"))
raw = pd.read_csv(os.path.join(DATA, "notable_ai_models_epoch.csv"))

# === dataset profile ===
print("=== profile ===")
print("raw rows:", len(raw), "cols:", len(raw.columns))
print("cadence rows:", len(cad))
print("gaps rows:", len(gaps))
print("mpy rows:", len(mpy))
_pd = pd.to_datetime(raw["Publication date"], errors="coerce")
print("raw date range:", _pd.min(), "->", _pd.max())

# --- ana_01: Headline cadence collapse (median days between frontier releases by year) ---
print("\n=== ana_01 ===")
clean = cad[cad["year"] >= 2018].copy()
for _, r in clean.iterrows():
    print(f"{int(r['year'])}: median {r['median_days_between_releases']} days, n={int(r['frontier_releases'])}")
m2018 = cad.loc[cad.year == 2018, "median_days_between_releases"].iloc[0]
m2025 = cad.loc[cad.year == 2025, "median_days_between_releases"].iloc[0]
print(f"2018 median: {m2018}, 2025 median: {m2025}, speedup: {m2018/m2025:.1f}x")

# --- ana_02: The 2022 cliff (ChatGPT-year inflection) ---
print("\n=== ana_02 ===")
m2021 = cad.loc[cad.year == 2021, "median_days_between_releases"].iloc[0]
m2022 = cad.loc[cad.year == 2022, "median_days_between_releases"].iloc[0]
m2023 = cad.loc[cad.year == 2023, "median_days_between_releases"].iloc[0]
print(f"2021 median gap: {m2021} days")
print(f"2022 median gap: {m2022} days (factor vs 2021: {m2021/m2022:.1f}x faster)")
print(f"2023 median gap: {m2023} days")
print(f"2021->2023 compression: {m2021/m2023:.1f}x")

# --- ana_03: Releases per year exploded (frontier language releases counted in cadence) ---
print("\n=== ana_03 ===")
for _, r in cad[cad.year >= 2018].iterrows():
    print(f"{int(r['year'])}: {int(r['frontier_releases'])} frontier releases")
r2018 = cad.loc[cad.year == 2018, "frontier_releases"].iloc[0]
r2025 = cad.loc[cad.year == 2025, "frontier_releases"].iloc[0]
print(f"2018: {int(r2018)} -> 2025: {int(r2025)} = {r2025/r2018:.1f}x more releases")

# --- ana_04: Mean vs median divergence (mean falls even faster; distribution skew) ---
print("\n=== ana_04 ===")
for _, r in cad[cad.year >= 2019].iterrows():
    med = r["median_days_between_releases"]; mn = r["mean_days_between_releases"]
    print(f"{int(r['year'])}: median {med}, mean {mn:.1f}, mean-median gap {mn-med:.1f}")

# --- ana_05: Annual notable-model volume growth (macro backdrop) ---
print("\n=== ana_05 ===")
recent = mpy[(mpy.year >= 2015) & (mpy.year <= 2026)]
for _, r in recent.iterrows():
    print(f"{int(r['year'])}: {int(r['notable_models'])} notable models")
v2015 = mpy.loc[mpy.year == 2015, "notable_models"].iloc[0]
v2025 = mpy.loc[mpy.year == 2025, "notable_models"].iloc[0]
print(f"2015: {int(v2015)} -> 2025: {int(v2025)} = {v2025/v2015:.1f}x")
print("NOTE: 2026 value is partial-year (through mid-May)")

# --- ana_06: Per-lab cadence — every named lab sped up (latest-year vs earliest-year median gap) ---
print("\n=== ana_06 ===")
gaps2 = gaps.dropna(subset=["days_since_prev_from_org"]).copy()
gaps2["year"] = pd.to_datetime(gaps2["publication_date"]).dt.year
labs = ["OpenAI", "Anthropic", "Google", "Meta AI", "xAI", "DeepSeek", "Mistral AI", "Alibaba", "Google DeepMind", "DeepMind"]
lab_rows = []
for lab in labs:
    sub = gaps2[gaps2.organization == lab]
    if len(sub) == 0:
        continue
    overall_median = sub["days_since_prev_from_org"].median()
    # recent (2025+) vs earlier
    recent = sub[sub.year >= 2025]["days_since_prev_from_org"]
    n = len(sub)
    rec_med = recent.median() if len(recent) else None
    print(f"{lab}: n_gaps={n}, overall_median={overall_median:.0f}d, 2025+_median={'%.0f'%rec_med if rec_med is not None else 'NA'}d")
    lab_rows.append((lab, n, overall_median, rec_med))

# --- ana_07: Anthropic specifically (detective benchmark cross-check) ---
print("\n=== ana_07 ===")
ant = gaps2[gaps2.organization == "Anthropic"].sort_values("publication_date")
print(ant[["model", "publication_date", "days_since_prev_from_org"]].to_string(index=False))
ant_2023 = ant[ant.year == 2023]["days_since_prev_from_org"]
ant_2025 = ant[ant.year >= 2025]["days_since_prev_from_org"]
print(f"Anthropic 2023 median gap: {ant_2023.median():.0f}d (n={len(ant_2023)})")
print(f"Anthropic 2025+ median gap: {ant_2025.median():.0f}d (n={len(ant_2025)})")

# --- ana_08: OpenAI cadence (the pace-setter, most releases) ---
print("\n=== ana_08 ===")
oa = gaps2[gaps2.organization == "OpenAI"]
oa_early = oa[oa.year <= 2022]["days_since_prev_from_org"]
oa_late = oa[oa.year >= 2024]["days_since_prev_from_org"]
print(f"OpenAI total gaps: {len(oa)}")
print(f"OpenAI <=2022 median gap: {oa_early.median():.0f}d (n={len(oa_early)})")
print(f"OpenAI >=2024 median gap: {oa_late.median():.0f}d (n={len(oa_late)})")

# --- ana_09: Zero-day collisions — same-day releases (the race tightens to simultaneity) ---
print("\n=== ana_09 ===")
zero = gaps2[gaps2.days_since_prev_from_org == 0]
print(f"Releases with 0 days since the lab's previous release: {len(zero)}")
print(zero.groupby("organization").size().to_string())
zero_by_year = zero.groupby("year").size()
print("By year:")
print(zero_by_year.to_string())
