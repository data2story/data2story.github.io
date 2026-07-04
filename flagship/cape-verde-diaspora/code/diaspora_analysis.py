"""
Data2Story Analyst -- Cape Verde diaspora geography (UN DESA IMS 2024 slice).

ana_01  Top destinations 2024 (UN born-in-Cabo-Verde migrant stock)
ana_02  Growth 1990 -> 2024 by destination (Luxembourg surge)
ana_03  Sao Tome and Principe: the one shrinking destination (famine-era echo)
ana_04  UN emigrant floor vs resident population, 1990-2024 waves
ana_05  Global rank: emigrant floor as % of resident population (all origins)

LAYER RULE (det_07/det_17): every number here is the UN "born in Cabo Verde,
living abroad" MIGRANT-STOCK layer -- a FLOOR. The Netherlands, United States,
Spain and Senegal are structurally ABSENT from the 2024 bilateral matrix.
Never mix these values with heritage/ancestry estimates.

Run:  py diaspora_analysis.py     (PYTHONUTF8=1; deterministic, local files only)
"""
import os
import openpyxl
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR", r"D:\AI\journalist agent review\phase2\data\cape-verde-diaspora"
)
P = lambda *a: os.path.join(DATA_DIR, *a)

d = pd.read_csv(P("01_diaspora", "cape_verde_emigrants_by_destination.csv"))
d["destination"] = d["destination"].str.replace("*", "", regex=False).str.strip()
world = d[d.is_world_total].set_index("year").migrants
dest = d[~d.is_world_total]
piv = dest.pivot_table(index="destination", columns="year", values="migrants")

pop = pd.read_csv(P("04_population", "population_total_tidy.csv"))
cpv_pop = pop[pop["Country Code"] == "CPV"].set_index("year").population

# --- ana_01: Top destinations 2024 (UN migrant-stock floor) ---
print("=== ana_01 ===")
t24 = piv[2024].sort_values(ascending=False)
w24 = int(world[2024])
print(f"World total (floor) 2024: {w24:,}")
named = int(t24.sum())
print(f"Sum of 24 named destinations: {named:,} ({named / w24 * 100:.1f}% of world total)")
print(f"'Other' (not broken out): {w24 - named:,}")
for dst, v in t24.items():
    print(f"  {dst}: {int(v):,} ({v / w24 * 100:.1f}%)")
top2 = t24.iloc[:2].sum()
print(f"Portugal+France = {int(top2):,} = {top2 / w24 * 100:.1f}% of the world total")
print("full wave matrix (destinations sorted by 2024, plus World):")
full = piv.reindex(t24.index).astype(int)
full.loc["World"] = world.astype(int)
print(full.to_string())

# --- ana_02: Growth 1990 -> 2024 by destination ---
print("=== ana_02 ===")
g = piv[[1990, 2024]].copy()
g.columns = ["y1990", "y2024"]
g["multiple"] = (g.y2024 / g.y1990).where(g.y1990 > 0).round(2)
g = g.sort_values("y2024", ascending=False)
print(f"World total: {int(world[1990]):,} -> {int(world[2024]):,} "
      f"= x{world[2024] / world[1990]:.2f} in 34 years")
print(g.to_string())
lux = piv.loc["Luxembourg"]
lux_pop_2024 = int(pop[(pop["Country Code"] == "LUX") & (pop.year == 2024)].population.iloc[0])
print(f"Luxembourg wave series: {[int(v) for v in lux]}")
print(f"Luxembourg 2024: {int(lux[2024]):,} CV-born = "
      f"{lux[2024] / lux_pop_2024 * 100:.2f}% of Luxembourg's population ({lux_pop_2024:,})")

# --- ana_03: Sao Tome and Principe, the one shrinking destination ---
print("=== ana_03 ===")
st = piv.loc["Sao Tome and Principe"]
print("Sao Tome and Principe wave series (year: migrants):")
for y, v in st.items():
    print(f"  {y}: {int(v):,}")
print(f"Change 1990->2024: {int(st[2024]) - int(st[1990]):,} ({(st[2024] / st[1990] - 1) * 100:.1f}%)")
shrunk = piv[piv[2024] < piv[1990]].index.tolist()
print(f"Destinations with 2024 < 1990 (of {len(piv)}): {shrunk}")

# --- ana_04: UN emigrant floor vs resident population, 1990-2024 ---
print("=== ana_04 ===")
print("wave | UN born-in-CV abroad (floor) | CPV resident pop | ratio")
rows04 = []
for y in [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]:
    ratio = world[y] / cpv_pop[y] * 100
    rows04.append((y, int(world[y]), int(cpv_pop[y]), round(ratio, 1)))
    print(f"  {y} | {int(world[y]):>7,} | {int(cpv_pop[y]):>7,} | {ratio:.1f}%")

# --- ana_05: Global rank of emigrant floor as % of resident population ---
print("=== ana_05 ===")
# Per-origin world totals from the raw UN DESA matrix (dest_code 900 = World).
wb = openpyxl.load_workbook(P("01_diaspora", "undesa_ims_2024_destination_origin.xlsx"),
                            read_only=True)
ws = wb["Table 1"]
origin_tot = {}
for row in ws.iter_rows(min_row=12, max_col=15, values_only=True):
    (_i, dst, _cov, _dt, dcode, origin, ocode, *vals) = row
    if dcode is None or origin is None or ocode is None:
        continue
    if int(dcode) == 900 and int(ocode) < 900:  # World row, individual origin
        v = vals[7]  # 2024 wave
        if v not in (None, "", ".."):
            origin_tot[origin.replace("*", "").strip()] = int(v)
print(f"origins with a 2024 world-total row: {len(origin_tot)}")

meta = pd.read_csv(P("04_population",
                     "Metadata_Country_API_SP.POP.TOTL_DS2_EN_csv_v2_3107.csv"),
                   encoding="utf-8-sig")
countries = meta[meta.Region.notna()]  # drop WB aggregates (World, regions, ...)
pop24 = pop[pop.year == 2024].merge(countries[["Country Code"]], on="Country Code")
pop_by_name = pop24.set_index("Country Name").population

UN_TO_WB = {  # UN DESA location name -> WB WDI Country Name (only mismatches)
    "United States of America": "United States", "Republic of Korea": "Korea, Rep.",
    "Dem. People's Republic of Korea": "Korea, Dem. People's Rep.",
    "Iran (Islamic Republic of)": "Iran, Islamic Rep.",
    "Venezuela (Bolivarian Republic of)": "Venezuela, RB",
    "Bolivia (Plurinational State of)": "Bolivia", "Egypt": "Egypt, Arab Rep.",
    "Yemen": "Yemen, Rep.", "Gambia": "Gambia, The", "Bahamas": "Bahamas, The",
    "Democratic Republic of the Congo": "Congo, Dem. Rep.", "Congo": "Congo, Rep.",
    "Micronesia (Fed. States of)": "Micronesia, Fed. Sts.",
    "Saint Lucia": "St. Lucia", "Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
    "Saint Kitts and Nevis": "St. Kitts and Nevis", "Saint Martin (French part)": "St. Martin (French part)",
    "Sint Maarten (Dutch part)": "Sint Maarten (Dutch part)",
    "Kyrgyzstan": "Kyrgyz Republic", "Slovakia": "Slovak Republic",
    "Lao People's Democratic Republic": "Lao PDR",
    "China, Hong Kong SAR": "Hong Kong SAR, China", "China, Macao SAR": "Macao SAR, China",
    "State of Palestine": "West Bank and Gaza", "Cote d'Ivoire": "Cote d'Ivoire",
    "Turkiye": "Turkiye", "Viet Nam": "Viet Nam",
    "United Republic of Tanzania": "Tanzania", "Republic of Moldova": "Moldova",
    "Brunei Darussalam": "Brunei Darussalam", "Curacao": "Curacao",
    "Syrian Arab Republic": "Syrian Arab Republic",
}
def to_wb(name):
    # normalize accents the two sources spell differently
    n = (name.replace("ô", "o").replace("ç", "c").replace("ü", "u")
             .replace("é", "e").replace("è", "e"))
    return UN_TO_WB.get(name, UN_TO_WB.get(n, name))

rows05, unmatched = [], []
for origin, emig in origin_tot.items():
    wb_name = to_wb(origin)
    if wb_name in pop_by_name.index:
        p24 = pop_by_name[wb_name]
        rows05.append((wb_name, emig, int(p24), round(emig / p24 * 100, 1)))
    else:
        unmatched.append((origin, emig))
rk = pd.DataFrame(rows05, columns=["origin", "emigrants_2024", "population_2024",
                                   "ratio_pct"]).sort_values("ratio_pct", ascending=False)
rk["rank"] = range(1, len(rk) + 1)
print(f"matched origins: {len(rk)}; unmatched (no WB population row, excluded): {len(unmatched)}")
print("largest excluded origins:", sorted(unmatched, key=lambda x: -x[1])[:8])
print(rk.head(25).to_string(index=False))
cv_row = rk[rk.origin == "Cabo Verde"].iloc[0]
print(f"Cabo Verde: rank #{int(cv_row['rank'])} of {len(rk)} "
      f"(emigrant floor {cv_row.emigrants_2024:,} = {cv_row.ratio_pct}% of residents)")
africa = countries[countries.Region == "Sub-Saharan Africa"]["Country Code"]
af_names = set(pop24[pop24["Country Code"].isin(africa)]["Country Name"])
rk_af = rk[rk.origin.isin(af_names)].reset_index(drop=True)
print("Sub-Saharan Africa top 5 by ratio:")
print(rk_af.head(5).to_string(index=False))
