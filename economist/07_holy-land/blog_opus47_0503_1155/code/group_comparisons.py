"""Compare Israel vs West Bank settler growth rates, and Arab populations
across the four constituencies.
"""

import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/economist/07_holy-land"

jews = pd.read_csv(f"{DATA_DIR}/population.jews.csv")
arabs = pd.read_csv(f"{DATA_DIR}/population.arabs.csv")
arabs = arabs.loc[:, ~arabs.columns.str.contains("^Unnamed")]

# --- ana_10: Settlers grow much faster than Israel proper ---
print("=== ana_10 ===")
first = jews.iloc[0]
last = jews.iloc[-1]
print(f"Israel proper Jews 1998: {int(first['Israel']):,} -> 2021: {int(last['Israel']):,} (x{last['Israel']/first['Israel']:.2f})")
print(f"West Bank settlers 1998: {int(first['West.Bank']):,} -> 2021: {int(last['West.Bank']):,} (x{last['West.Bank']/first['West.Bank']:.2f})")
print(f"East Jerusalem Jews 1998: {int(first['East.Jerusalem']):,} -> 2021: {int(last['East.Jerusalem']):,} (x{last['East.Jerusalem']/first['East.Jerusalem']:.2f})")
mult_settler = (last['West.Bank']/first['West.Bank']) / (last['Israel']/first['Israel'])
print(f"\nWest Bank settler growth was {mult_settler:.2f}x as fast as Israel proper")

# --- ana_11: Share of Jewish population that lives over the Green Line ---
print("\n=== ana_11 ===")
# Total Jews = Israel + West Bank + East Jerusalem
beyond = jews["West.Bank"] + jews["East.Jerusalem"]
total = jews["Israel"] + jews["West.Bank"] + jews["East.Jerusalem"]
share = 100 * beyond / total
table = pd.DataFrame({
    "year": jews["year"],
    "beyond_line": beyond.astype(int),
    "total_jews": total.astype(int),
    "pct_beyond": share.round(2),
})
print(table.to_string(index=False))
first_pct = share.iloc[0]
last_pct = share.iloc[-1]
print(f"\nShare of all Jews living beyond the Green Line:")
print(f"  1998: {first_pct:.2f}%")
print(f"  2021: {last_pct:.2f}% (+{last_pct-first_pct:.2f} pp)")

# --- ana_12: Arab populations by region 1998 vs 2021 ---
print("\n=== ana_12 ===")
first_a = arabs.iloc[0]
last_a = arabs.iloc[-1]
regions = ["Israel", "West.Bank", "East.Jerusalem", "Gaza"]
print(f"{'region':<15} {'1998':>12} {'2021':>12} {'multiple':>10}")
for r in regions:
    print(f"{r:<15} {int(first_a[r]):>12,} {int(last_a[r]):>12,} x{last_a[r]/first_a[r]:>7.2f}")

# Arab mix in 2021
total_arab_2021 = sum(last_a[r] for r in regions)
print(f"\n2021 Arab share by region:")
for r in regions:
    pct = 100 * last_a[r] / total_arab_2021
    print(f"  {r:<15} {int(last_a[r]):>12,} ({pct:5.1f}%)")

# --- ana_13: Gaza disengagement scale comparison ---
print("\n=== ana_13 ===")
# 8,000 settlers were removed from Gaza in 2005
gaza_baseline = 8000
last_jews = jews.iloc[-1]
wb_2021 = last_jews["West.Bank"]
ej_2021 = last_jews["East.Jerusalem"]
all_settlers = wb_2021 + ej_2021
print(f"Gaza disengagement (2005): 8,000 settlers")
print(f"West Bank settlers (2021): {int(wb_2021):,} = {wb_2021/gaza_baseline:.1f}x Gaza scale")
print(f"East Jerusalem settlers (2021): {int(ej_2021):,} = {ej_2021/gaza_baseline:.1f}x Gaza scale")
print(f"Total beyond Green Line (2021): {int(all_settlers):,} = {all_settlers/gaza_baseline:.1f}x Gaza scale")
