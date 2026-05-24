#!/usr/bin/env python3
"""NVDA financials analysis. Run from DATA_DIR or pass path. All findings print '=== ana_xx ==='."""
import pandas as pd
import sys, os

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else "/Users/forrest/Desktop/data2blog-skill/data/nvda"
ann = pd.read_csv(os.path.join(DATA_DIR, "financials_annual.csv"))
ann = ann.sort_values("period_end").reset_index(drop=True)
ann["fy_label"] = "FY" + ann["fy"].astype(str)
# fix the fiscal labeling artifact: there is an fy=2013 row with period_end 2014-01-26 and none labeled 2014.
# We use period_end calendar year of the END date for a clean "fiscal year ending" label.
ann["fy_end_year"] = pd.to_datetime(ann["period_end"]).dt.year  # the calendar year FY ends in

# Helper for billions
def b(x):
    return round(x / 1e9, 2)

# --- ana_01: Revenue trajectory FY2011-FY2026 ---
print("=== ana_01 ===")
ann["revenue_b"] = ann["revenue"].apply(b)
ann["rev_yoy_pct"] = (ann["revenue"].pct_change() * 100).round(1)
print(ann[["fy_end_year", "period_end", "revenue_b", "rev_yoy_pct"]].to_string(index=False))
print(f"FY2011 revenue: ${b(ann.iloc[0]['revenue'])}B -> FY2026 revenue: ${b(ann.iloc[-1]['revenue'])}B")
print(f"Total multiple FY2011->FY2026: {round(ann.iloc[-1]['revenue']/ann.iloc[0]['revenue'],1)}x")

# --- ana_02: The FY2024 inflection — biggest YoY jump ---
print("=== ana_02 ===")
infl = ann[["fy_end_year", "revenue_b", "rev_yoy_pct"]].copy()
top = infl.sort_values("rev_yoy_pct", ascending=False).head(5)
print("Top 5 YoY revenue growth years:")
print(top.to_string(index=False))
# FY ending 2024 (fy label 2024) and the 2-year ramp
r2023 = ann[ann["fy_end_year"]==2023]["revenue"].iloc[0]
r2024 = ann[ann["fy_end_year"]==2024]["revenue"].iloc[0]
r2026 = ann[ann["fy_end_year"]==2026]["revenue"].iloc[0]
print(f"FY ending 2023: ${b(r2023)}B (flat) -> FY ending 2024: ${b(r2024)}B = +{round((r2024/r2023-1)*100,1)}%")
print(f"FY ending 2024: ${b(r2024)}B -> FY ending 2026: ${b(r2026)}B = {round(r2026/r2024,1)}x in two years")

# --- ana_03: Gross margin trend and the FY2023 dip ---
print("=== ana_03 ===")
gm = ann[["fy_end_year", "gross_margin_pct", "net_margin_pct"]].copy()
print(gm.to_string(index=False))
print(f"Net margin FY2022(end): {ann[ann['fy_end_year']==2022]['net_margin_pct'].iloc[0]}%")
print(f"Net margin FY2023(end) DIP: {ann[ann['fy_end_year']==2023]['net_margin_pct'].iloc[0]}%")
print(f"Net margin FY2024(end) RECOVERY: {ann[ann['fy_end_year']==2024]['net_margin_pct'].iloc[0]}%")
print(f"Net margin FY2025(end) PEAK: {ann[ann['fy_end_year']==2025]['net_margin_pct'].iloc[0]}%")
print(f"Gross margin FY2024-FY2026 all above 70%: {gm[gm['fy_end_year']>=2024]['gross_margin_pct'].tolist()}")

# --- ana_04: Net income (split-immune) growth ---
print("=== ana_04 ===")
ann["net_income_b"] = ann["net_income"].apply(b)
ni = ann[["fy_end_year", "net_income_b"]].copy()
print(ni.to_string(index=False))
ni2024 = ann[ann["fy_end_year"]==2024]["net_income"].iloc[0]
ni2025 = ann[ann["fy_end_year"]==2025]["net_income"].iloc[0]
ni2026 = ann[ann["fy_end_year"]==2026]["net_income"].iloc[0]
print(f"Net income FY-end 2024: ${b(ni2024)}B -> 2025: ${b(ni2025)}B -> 2026: ${b(ni2026)}B")
print(f"Net income 2024->2025 growth: +{round((ni2025/ni2024-1)*100,1)}%")
print(f"Net income FY2011 ${b(ann.iloc[0]['net_income'])}B -> FY2026 ${b(ni2026)}B = {round(ni2026/ann.iloc[0]['net_income'],0)}x")

# --- ana_05: The EPS split trap ---
print("=== ana_05 ===")
eps = ann[ann["fy_end_year"].isin([2024,2025,2026])][["fy_end_year","eps_diluted","net_income"]].copy()
eps["net_income_b"] = eps["net_income"].apply(b)
print(eps[["fy_end_year","eps_diluted","net_income_b"]].to_string(index=False))
print("EPS 'falls' 11.93 -> 2.94 across the 10:1 split while net income MORE THAN DOUBLES.")
print("11.93 / 10 = 1.193 (post-split-equivalent); reported 2.94 is HIGHER because earnings grew.")

# --- ana_06: R&D spend scaling ---
print("=== ana_06 ===")
ann["rnd_b"] = ann["rnd_expense"].apply(b)
ann["rnd_pct_rev"] = (ann["rnd_expense"]/ann["revenue"]*100).round(1)
rnd = ann[["fy_end_year","rnd_b","rnd_pct_rev"]].copy()
print(rnd.to_string(index=False))
print(f"R&D FY2011: ${b(ann.iloc[0]['rnd_expense'])}B ({ann.iloc[0]['rnd_pct_rev'] if 'rnd_pct_rev' in ann else ''}) -> FY2026: ${b(ann.iloc[-1]['rnd_expense'])}B")
print(f"R&D as % of revenue: peaked at {ann['rnd_pct_rev'].max()}%, FY2026 down to {ann.iloc[-1]['rnd_pct_rev']}% even as absolute R&D hit record ${b(ann.iloc[-1]['rnd_expense'])}B")

# --- ana_07: Balance sheet expansion (assets & equity) ---
print("=== ana_07 ===")
ann["assets_b"] = ann["total_assets"].apply(b)
ann["equity_b"] = ann["stockholders_equity"].apply(b)
bs = ann[["fy_end_year","assets_b","equity_b"]].copy()
print(bs.to_string(index=False))
print(f"Total assets FY2011 ${b(ann.iloc[0]['total_assets'])}B -> FY2026 ${b(ann.iloc[-1]['total_assets'])}B")
print(f"Stockholders equity FY2011 ${b(ann.iloc[0]['stockholders_equity'])}B -> FY2026 ${b(ann.iloc[-1]['stockholders_equity'])}B")
