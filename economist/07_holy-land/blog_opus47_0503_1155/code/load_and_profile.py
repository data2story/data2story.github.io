"""Load all three CSVs, profile them, compute totals and crossover.

Run from DATA_DIR = data_preprint/economist/07_holy-land/.
"""

import pandas as pd

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/economist/07_holy-land"

jews = pd.read_csv(f"{DATA_DIR}/population.jews.csv")
arabs = pd.read_csv(f"{DATA_DIR}/population.arabs.csv")
# arabs has trailing empty columns; strip them
arabs = arabs.loc[:, ~arabs.columns.str.contains("^Unnamed")]
ej_wb = pd.read_csv(f"{DATA_DIR}/population.ej.wb.csv")
# ej_wb header has the typo "East.Jersualem" -> rename
ej_wb = ej_wb.rename(columns={"East.Jersualem": "East.Jerusalem"})

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print("FILES:")
print(f"  population.jews.csv: {jews.shape} rows={len(jews)} cols={list(jews.columns)}")
print(f"  population.arabs.csv: {arabs.shape} rows={len(arabs)} cols={list(arabs.columns)}")
print(f"  population.ej.wb.csv: {ej_wb.shape} rows={len(ej_wb)} cols={list(ej_wb.columns)}")
print(f"YEAR RANGE: {int(jews.year.min())}-{int(jews.year.max())}")
print(f"NULLS jews: {jews.isna().sum().sum()}")
print(f"NULLS arabs: {arabs.isna().sum().sum()}")
print(f"NULLS ej_wb: {ej_wb.isna().sum().sum()}")

# --- ana_02: Total Jewish vs Arab populations between river and sea (1998 vs 2021) ---
print("\n=== ana_02 ===")
jews_total = jews["Israel"] + jews["West.Bank"] + jews["East.Jerusalem"]
arabs_total = arabs["Israel"] + arabs["West.Bank"] + arabs["East.Jerusalem"] + arabs["Gaza"]
totals = pd.DataFrame({
    "year": jews["year"],
    "jews_total": jews_total,
    "arabs_total": arabs_total,
})
totals["jewish_share_pct"] = 100 * totals["jews_total"] / (totals["jews_total"] + totals["arabs_total"])
totals["arab_share_pct"] = 100 - totals["jewish_share_pct"]
totals["gap"] = totals["jews_total"] - totals["arabs_total"]
print(totals.to_string(index=False))

# --- ana_03: Crossover year (when Arabs first equal/exceed Jews) ---
print("\n=== ana_03 ===")
crossed = totals[totals["arabs_total"] >= totals["jews_total"]]
if len(crossed) == 0:
    print("Arab total never reaches Jewish total in this 1998-2021 window.")
else:
    first_year = int(crossed["year"].iloc[0])
    print(f"First year Arabs >= Jews: {first_year}")
    row = crossed.iloc[0]
    print(f"  Jews:  {int(row.jews_total):,}")
    print(f"  Arabs: {int(row.arabs_total):,}")
    print(f"  Gap:   {int(row.gap):,}")
# Also report 1998 vs 2021 in detail
first = totals.iloc[0]
last = totals.iloc[-1]
print(f"1998: Jews {int(first.jews_total):,} ({first.jewish_share_pct:.1f}%) vs Arabs {int(first.arabs_total):,} ({first.arab_share_pct:.1f}%)")
print(f"2021: Jews {int(last.jews_total):,} ({last.jewish_share_pct:.1f}%) vs Arabs {int(last.arabs_total):,} ({last.arab_share_pct:.1f}%)")
print(f"Jewish-share change 1998->2021: {first.jewish_share_pct - last.jewish_share_pct:+.1f} pp (decline)")

# --- ana_04: Combined totals data table for chart ---
print("\n=== ana_04 ===")
# Long-form table for line chart: year, group, count
rows = []
for _, r in totals.iterrows():
    rows.append({"year": int(r.year), "group": "Jews", "count": int(r.jews_total)})
    rows.append({"year": int(r.year), "group": "Arabs", "count": int(r.arabs_total)})
print(pd.DataFrame(rows).head(6).to_string(index=False))
print("...")
print(pd.DataFrame(rows).tail(6).to_string(index=False))

# Save summary table for downstream stages
totals.to_csv("/tmp/holy_land_totals.csv", index=False)
print("\nWrote /tmp/holy_land_totals.csv")
