"""
Data2Story Analyst -- Cape Verde remittance dependence (WB WDI BX.TRF.PWKR.DT.GD.ZS).

ana_06  CPV arc 1980-2024: 28.2% of GDP -> 12.3%
ana_07  Global rank on remittance dependence, 2024 (aggregates excluded)
ana_08  Rank history 1980-2024: best-ever global rank

Aggregate rows (World, Sub-Saharan Africa, ...) are excluded from every ranking
via the WB metadata file: true countries have a non-empty Region field.

Run:  py remittances_analysis.py     (PYTHONUTF8=1; deterministic, local files only)
"""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR", r"D:\AI\journalist agent review\phase2\data\cape-verde-diaspora"
)
P = lambda *a: os.path.join(DATA_DIR, *a)

r = pd.read_csv(P("02_remittances", "remittances_pct_gdp_tidy.csv"))
meta = pd.read_csv(P("02_remittances",
                     "Metadata_Country_API_BX.TRF.PWKR.DT.GD.ZS_DS2_en_csv_v2_6343.csv"),
                   encoding="utf-8-sig")
countries = set(meta[meta.Region.notna()]["Country Code"])  # aggregates out
rc = r[r["Country Code"].isin(countries)].copy()
cpv = rc[rc["Country Code"] == "CPV"].sort_values("year")

# --- ana_06: CPV remittance arc 1980-2024 ---
print("=== ana_06 ===")
first, last = cpv.iloc[0], cpv.iloc[-1]
peak = cpv.loc[cpv.remittances_pct_gdp.idxmax()]
low = cpv.loc[cpv.remittances_pct_gdp.idxmin()]
print(f"first: {int(first.year)} = {first.remittances_pct_gdp:.1f}% of GDP")
print(f"peak : {int(peak.year)} = {peak.remittances_pct_gdp:.1f}%")
print(f"low  : {int(low.year)} = {low.remittances_pct_gdp:.1f}%")
print(f"last : {int(last.year)} = {last.remittances_pct_gdp:.1f}%")
cpv["decade"] = (cpv.year // 10) * 10
dec = cpv.groupby("decade").remittances_pct_gdp.mean().round(1)
print("decade means (% of GDP):")
print(dec.to_string())
print("full series (year, pct):")
print(", ".join(f"{int(y)}:{v:.1f}" for y, v in zip(cpv.year, cpv.remittances_pct_gdp)))

# --- ana_07: Global rank 2024 (countries only) ---
print("=== ana_07 ===")
y24 = rc[rc.year == 2024].dropna(subset=["remittances_pct_gdp"]).copy()
y24 = y24.sort_values("remittances_pct_gdp", ascending=False).reset_index(drop=True)
y24["rank"] = y24.index + 1
print(f"countries reporting in 2024: {len(y24)}")
cv24 = y24[y24["Country Code"] == "CPV"].iloc[0]
print(f"Cabo Verde 2024: {cv24.remittances_pct_gdp:.1f}% of GDP -> "
      f"rank #{int(cv24['rank'])} of {len(y24)} (top {int(cv24['rank']) / len(y24) * 100:.0f}%)")
print(y24.head(20)[["rank", "Country Name", "remittances_pct_gdp"]]
      .assign(remittances_pct_gdp=lambda x: x.remittances_pct_gdp.round(1)).to_string(index=False))
ssa = set(meta[meta.Region == "Sub-Saharan Africa"]["Country Code"])
y24_ssa = y24[y24["Country Code"].isin(ssa)].reset_index(drop=True)
y24_ssa["ssa_rank"] = y24_ssa.index + 1
print("Sub-Saharan Africa top 8, 2024:")
print(y24_ssa.head(8)[["ssa_rank", "Country Name", "remittances_pct_gdp"]]
      .assign(remittances_pct_gdp=lambda x: x.remittances_pct_gdp.round(1)).to_string(index=False))

# --- ana_08: Rank history 1980-2024 (best-ever global rank) ---
print("=== ana_08 ===")
hist = []
for y in range(1980, 2025):
    yy = rc[(rc.year == y)].dropna(subset=["remittances_pct_gdp"])
    yy = yy.sort_values("remittances_pct_gdp", ascending=False).reset_index(drop=True)
    row = yy[yy["Country Code"] == "CPV"]
    if row.empty:
        continue
    rank = int(row.index[0]) + 1
    hist.append((y, rank, len(yy), round(row.iloc[0].remittances_pct_gdp, 1)))
h = pd.DataFrame(hist, columns=["year", "cpv_rank", "n_countries", "cpv_pct"])
print(h.to_string(index=False))
best = h.loc[h.cpv_rank.idxmin()]
top10_years = h[h.cpv_rank <= 10]
print(f"best-ever rank: #{int(best.cpv_rank)} of {int(best.n_countries)} in {int(best.year)} "
      f"({best.cpv_pct}% of GDP)")
print(f"years ranked in the global top 10: {len(top10_years)} "
      f"({', '.join(str(int(y)) for y in top10_years.year)})")
