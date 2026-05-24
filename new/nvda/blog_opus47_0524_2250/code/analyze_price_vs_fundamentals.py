#!/usr/bin/env python3
"""Join split-adjusted price to fundamentals on period_end, plus price history. Run from DATA_DIR."""
import pandas as pd
import sys, os

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else "/Users/forrest/Desktop/data2blog-skill/data/nvda"
ann = pd.read_csv(os.path.join(DATA_DIR, "financials_annual.csv")).sort_values("period_end").reset_index(drop=True)
daily = pd.read_csv(os.path.join(DATA_DIR, "stock_prices_daily.csv"))
yr = pd.read_csv(os.path.join(DATA_DIR, "stock_price_by_year.csv"))

daily["Date"] = pd.to_datetime(daily["Date"]) if "Date" in daily.columns else pd.to_datetime(daily.iloc[:,0])
# detect close column
close_col = [c for c in daily.columns if c.lower() in ("close","adj close","adj_close")]
close_col = close_col[0] if close_col else daily.columns[-1]
date_col = [c for c in daily.columns if c.lower()=="date"]
date_col = date_col[0] if date_col else daily.columns[0]
daily[date_col] = pd.to_datetime(daily[date_col])
daily = daily.sort_values(date_col).reset_index(drop=True)

def b(x): return round(x/1e9,2)

# --- ana_08: Split-adjusted price joined to each fiscal period_end ---
print("=== ana_08 ===")
ann["period_end_dt"] = pd.to_datetime(ann["period_end"])
ann["fy_end_year"] = ann["period_end_dt"].dt.year
rows = []
for _, r in ann.iterrows():
    pe = r["period_end_dt"]
    # nearest trading day on or before period_end
    sub = daily[daily[date_col] <= pe]
    if len(sub):
        px = sub.iloc[-1][close_col]
    else:
        px = daily.iloc[0][close_col]
    rows.append((r["fy_end_year"], round(float(px),2), b(r["revenue"]), b(r["net_income"])))
pf = pd.DataFrame(rows, columns=["fy_end_year","price_at_period_end","revenue_b","net_income_b"])
print(pf.to_string(index=False))
print(f"Price at FY-end 2011: ${pf.iloc[0]['price_at_period_end']} -> FY-end 2026: ${pf.iloc[-1]['price_at_period_end']}")
print(f"Split-adjusted price multiple: {round(pf.iloc[-1]['price_at_period_end']/pf.iloc[0]['price_at_period_end'],0)}x")

# --- ana_09: Net income vs price correlation (do fundamentals explain price?) ---
print("=== ana_09 ===")
corr = pf["net_income_b"].corr(pf["price_at_period_end"])
corr_rev = pf["revenue_b"].corr(pf["price_at_period_end"])
print(f"Pearson correlation net_income vs price_at_period_end: {round(corr,3)}")
print(f"Pearson correlation revenue vs price_at_period_end: {round(corr_rev,3)}")
# log-log to see if multiple expanded
import numpy as np
print(f"Price grew {round(pf.iloc[-1]['price_at_period_end']/pf.iloc[0]['price_at_period_end'],0)}x vs net income {round(ann.iloc[-1]['net_income']/ann.iloc[0]['net_income'],0)}x over the same window.")

# --- ana_10: Annual stock return — best and worst years ---
print("=== ana_10 ===")
yr_recent = yr[yr["year"]>=2011][["year","close","yoy_return_pct"]].copy()
print(yr_recent.to_string(index=False))
best = yr_recent.sort_values("yoy_return_pct",ascending=False).head(3)
worst = yr_recent.sort_values("yoy_return_pct").head(3)
print("Best return years:"); print(best.to_string(index=False))
print("Worst return years:"); print(worst.to_string(index=False))

# --- ana_11: Revenue vs price both indexed to FY2011=100 (the gap and convergence) ---
print("=== ana_11 ===")
base_rev = ann.iloc[0]["revenue"]
base_px = pf.iloc[0]["price_at_period_end"]
idx_rows = []
for i, r in ann.iterrows():
    idx_rows.append((pf.iloc[i]["fy_end_year"],
                     round(r["revenue"]/base_rev*100,0),
                     round(pf.iloc[i]["price_at_period_end"]/base_px*100,0)))
idx = pd.DataFrame(idx_rows, columns=["fy_end_year","revenue_index","price_index"])
print(idx.to_string(index=False))
print("Both indexed to FY-end 2011 = 100. Price index far outruns revenue index = multiple expansion.")
