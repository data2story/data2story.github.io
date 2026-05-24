"""Analyse Jewish settler growth in the West Bank and East Jerusalem,
including the distance-from-Green-Line breakdown.
"""

import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/economist/07_holy-land"

jews = pd.read_csv(f"{DATA_DIR}/population.jews.csv")
ej_wb = pd.read_csv(f"{DATA_DIR}/population.ej.wb.csv")
ej_wb = ej_wb.rename(columns={"East.Jersualem": "East.Jerusalem"})

# --- ana_05: West Bank Jewish settler growth 1998 -> 2021 ---
print("=== ana_05 ===")
wb_first = jews.iloc[0]
wb_last = jews.iloc[-1]
print(f"West Bank Jewish population 1998: {int(wb_first['West.Bank']):,}")
print(f"West Bank Jewish population 2021: {int(wb_last['West.Bank']):,}")
mult = wb_last["West.Bank"] / wb_first["West.Bank"]
absolute = wb_last["West.Bank"] - wb_first["West.Bank"]
print(f"Growth: {absolute:,.0f} settlers added; {mult:.2f}x multiple")
# Annual time series for chart
wb_table = jews[["year", "West.Bank", "East.Jerusalem"]].copy()
wb_table["West.Bank"] = wb_table["West.Bank"].astype(int)
wb_table["East.Jerusalem"] = wb_table["East.Jerusalem"].astype(int)
print(wb_table.to_string(index=False))

# --- ana_06: East Jerusalem Jewish growth 1998 -> 2021 ---
print("\n=== ana_06 ===")
ej_first = jews.iloc[0]["East.Jerusalem"]
ej_last = jews.iloc[-1]["East.Jerusalem"]
print(f"East Jerusalem Jewish population 1998: {int(ej_first):,}")
print(f"East Jerusalem Jewish population 2021: {int(ej_last):,}")
print(f"Growth: {(ej_last-ej_first):,.0f} ({(ej_last/ej_first-1)*100:.1f}%)")

# --- ana_07: Settlers by distance from Green Line ---
print("\n=== ana_07 ===")
print(ej_wb.to_string(index=False))
# Compute the share each bucket holds in 2021
last = ej_wb.iloc[-1]
buckets = ["East.Jerusalem", "0-2.5km", "2.5-5km", "5-15km", ">15km"]
total_2021 = sum(last[b] for b in buckets)
print(f"\n2021 totals across all buckets: {int(total_2021):,}")
print("2021 share by bucket:")
for b in buckets:
    pct = 100 * last[b] / total_2021
    print(f"  {b:15} {int(last[b]):>9,} ({pct:5.1f}%)")

# Compute share within West Bank only (excluding East Jerusalem)
print("\nWithin West Bank (excluding East Jerusalem):")
wb_only = sum(last[b] for b in buckets if b != "East.Jerusalem")
for b in ["0-2.5km", "2.5-5km", "5-15km", ">15km"]:
    pct = 100 * last[b] / wb_only
    print(f"  {b:15} {int(last[b]):>9,} ({pct:5.1f}%)")
print(f"  TOTAL WB ONLY:  {int(wb_only):>9,}")
near = last["0-2.5km"] + last["2.5-5km"]
near_pct = 100 * near / wb_only
print(f"  Within 5 km:    {int(near):>9,} ({near_pct:.1f}%) — 'consensus' bloc territory")
deep = last[">15km"]
deep_pct = 100 * deep / wb_only
print(f"  Deeper than 15 km: {int(deep):>9,} ({deep_pct:.1f}%) — would require evacuation")

# --- ana_08: Growth rates by distance bucket ---
print("\n=== ana_08 ===")
first = ej_wb.iloc[0]
print(f"Growth multiples 1998 -> 2021 by bucket:")
for b in buckets:
    mult = last[b] / first[b]
    abs_growth = last[b] - first[b]
    print(f"  {b:15}  1998={int(first[b]):>7,}  2021={int(last[b]):>7,}  x{mult:.2f}  (+{int(abs_growth):,})")

# --- ana_09: How much of West Bank growth happened deep beyond 15 km? ---
print("\n=== ana_09 ===")
gain_close = (last["0-2.5km"] - first["0-2.5km"]) + (last["2.5-5km"] - first["2.5-5km"])
gain_mid = last["5-15km"] - first["5-15km"]
gain_deep = last[">15km"] - first[">15km"]
gain_total = gain_close + gain_mid + gain_deep
print(f"Total West Bank settler gain (excl. East Jerusalem) 1998-2021: {int(gain_total):,}")
print(f"  within 5 km of Green Line:  +{int(gain_close):>7,}  ({100*gain_close/gain_total:.1f}% of growth)")
print(f"  5-15 km from Green Line:    +{int(gain_mid):>7,}  ({100*gain_mid/gain_total:.1f}% of growth)")
print(f"  deeper than 15 km:          +{int(gain_deep):>7,}  ({100*gain_deep/gain_total:.1f}% of growth)")
