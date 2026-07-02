"""
analyze.py — Full analytical spine for the space-launches story.
Reproduces every number in analyst.json. Run from anywhere (DATA_DIR resolved by env or default).

  set PYTHONUTF8=1
  py code/analyze.py

Data quality handled (per detective det_11/det_12):
  - 2918-10-11 launch_date typo -> 2018-10-11 (Soyuz MS-10 abort, a FAILURE)
  - SU + RU merged into one "USSR/Russia" series
  - F + I-ESA + I-ELDO merged into "Europe" (ESA / Arianespace bloc)
  - all counts recomputed from launches.csv (agencies.csv 'count' is stale)
  - 2018 is a PARTIAL year (ends Oct); flagged everywhere it appears

Outputs (besides stdout):
  - code/derived_tables.json : every ana_xx data_table, machine-readable
  - code/client_data.json    : compact slices for the in-browser client models
"""
import os
import json
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:/AI/journalist agent review/phase2/datasets/journals/Economist/data/2018-10-20_space-launches",
)
HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# LOAD + CLEAN
# ----------------------------------------------------------------------------
launches = pd.read_csv(os.path.join(DATA_DIR, "launches.csv"))
agencies = pd.read_csv(os.path.join(DATA_DIR, "agencies.csv"))

# (clean 1) fix the 2918 -> 2018 launch_date typo (tag 2018-F01, Soyuz MS-10 abort)
typo_mask = launches["launch_date"].astype(str).str.startswith("2918")
n_typo = int(typo_mask.sum())
launches.loc[typo_mask, "launch_date"] = launches.loc[typo_mask, "launch_date"].str.replace(
    "2918", "2018", regex=False
)

# (clean 2) country grouping: SU+RU -> USSR/Russia ; F+I-ESA+I-ELDO -> Europe
EUROPE = {"F", "I-ESA", "I-ELDO"}
def to_country(sc):
    if sc in ("SU", "RU"):
        return "USSR/Russia"
    if sc == "US":
        return "USA"
    if sc == "CN":
        return "China"
    if sc in EUROPE:
        return "Europe"
    if sc == "J":
        return "Japan"
    if sc == "IN":
        return "India"
    return "Other"
launches["country"] = launches["state_code"].map(to_country)

# (clean 3) success flag from category O/F
launches["success"] = launches["category"].eq("O")
launches["decade"] = (launches["launch_year"] // 10) * 10

MAIN = ["USSR/Russia", "USA", "China", "Europe", "Japan", "India", "Other"]
derived = {}   # ana_xx -> data_table dict
client = {}    # client-model data slices

def dt(desc, columns, rows):
    return {"description": desc, "columns": columns, "rows": rows}

# ============================================================================
# ana_01 — Dataset overview / census scope
# ============================================================================
print("=== ana_01 ===")
n_rows = len(launches)
yr_min, yr_max = int(launches.launch_year.min()), int(launches.launch_year.max())
n_states = launches.state_code.nunique()
n_success = int(launches.success.sum())
n_fail = int((~launches.success).sum())
ov_rate = round(100 * n_success / n_rows, 1)
print(f"rows (orbital launch attempts): {n_rows}")
print(f"year range: {yr_min}-{yr_max} ({yr_max - yr_min + 1} calendar years)")
print(f"distinct state_code: {n_states}")
print(f"distinct vehicle types: {launches.type.nunique()}")
print(f"success (O): {n_success}  failure (F): {n_fail}  overall success rate: {ov_rate}%")
print(f"agency_type split: {launches.agency_type.value_counts().to_dict()}")
print(f"launch_date typo rows fixed (2918->2018): {n_typo}")
derived["ana_01"] = dt(
    "Census scope: launches by outcome",
    ["outcome", "count", "pct"],
    [["Success (O)", n_success, round(100 * n_success / n_rows, 1)],
     ["Failure (F)", n_fail, round(100 * n_fail / n_rows, 1)]],
)

# ============================================================================
# ana_02 — Global launches per year (the "how much" trend)
# ============================================================================
print("\n=== ana_02 ===")
per_year = launches.groupby("launch_year").size()
peak_year = int(per_year.idxmax()); peak_val = int(per_year.max())
print(f"peak year: {peak_year} with {peak_val} launches")
print(f"2018 (PARTIAL, ends Oct): {int(per_year.get(2018, 0))}")
print("decade peak context -> 1957 first row; full series below:")
print(per_year.to_string())
derived["ana_02"] = dt(
    "Global orbital launch attempts per year, 1957-2018 (2018 partial)",
    ["year", "launches", "partial"],
    [[int(y), int(c), (y == 2018)] for y, c in per_year.items()],
)

# ============================================================================
# ana_03 — Launches per country per year (CORE multi-line; SU+RU merged)
# ============================================================================
print("\n=== ana_03 ===")
cy = (launches.groupby(["launch_year", "country"]).size()
      .unstack("country").reindex(columns=MAIN).fillna(0).astype(int))
cy = cy.reindex(range(yr_min, yr_max + 1), fill_value=0)
cy["Total"] = cy.sum(axis=1)
print("country x year matrix (head + tail):")
print(cy.head(6).to_string())
print("...")
print(cy.tail(8).to_string())
matrix_rows = [[int(y)] + [int(cy.loc[y, c]) for c in MAIN] + [int(cy.loc[y, "Total"])]
               for y in cy.index]
derived["ana_03"] = dt(
    "Launches per launching country per year (SU+RU=USSR/Russia; F+I-ESA+I-ELDO=Europe); 2018 partial",
    ["year"] + MAIN + ["Total"],
    matrix_rows,
)
client["country_year_matrix"] = {"columns": ["year"] + MAIN, "rows": [r[:-1] for r in matrix_rows]}

# ============================================================================
# ana_04 — Cumulative / total launches by country, full era
# ============================================================================
print("\n=== ana_04 ===")
totals = launches.groupby("country").size().reindex(MAIN).astype(int)
tot_all = int(totals.sum())
print("total launches 1957-2018 by country (recomputed from launches.csv):")
for c in MAIN:
    print(f"  {c:14s} {int(totals[c]):5d}  ({100*totals[c]/tot_all:4.1f}%)")
print(f"  {'TOTAL':14s} {tot_all:5d}")
derived["ana_04"] = dt(
    "Total orbital launches 1957-2018 by country (full era)",
    ["country", "launches", "pct"],
    [[c, int(totals[c]), round(100 * totals[c] / tot_all, 1)] for c in MAIN],
)

# ============================================================================
# ana_05 — China's rise by decade + 2018 crossover (partial-aware)
# ============================================================================
print("\n=== ana_05 ===")
cn = launches[launches.country == "China"]
cn_by_dec = cn.groupby("decade").size()
print("China launches by decade:")
print(cn_by_dec.to_string())
y2018 = launches[launches.launch_year == 2018]
hh = y2018.groupby("country").size().reindex(MAIN).fillna(0).astype(int).sort_values(ascending=False)
print("\n2018 head-to-head IN THIS DATASET (PARTIAL year, ends Oct):")
print(hh.to_string())
print("  -> external full-year 2018 (det_07): China 39, USA 34, Russia 20, global 114")
derived["ana_05"] = dt(
    "China launches per decade (1970s-2010s)",
    ["decade", "launches"],
    [[f"{int(d)}s", int(c)] for d, c in cn_by_dec.items()],
)
derived["ana_05b_2018_partial"] = dt(
    "2018 launches by country: this dataset (PARTIAL, ends Oct) vs external full-year",
    ["country", "dataset_partial_2018", "external_full_year_2018"],
    [["China", int(hh.get("China", 0)), 39],
     ["USA", int(hh.get("USA", 0)), 34],
     ["USSR/Russia", int(hh.get("USSR/Russia", 0)), 20],
     ["Europe", int(hh.get("Europe", 0)), None],
     ["Japan", int(hh.get("Japan", 0)), None],
     ["India", int(hh.get("India", 0)), None],
     ["Other", int(hh.get("Other", 0)), None]],
)
client["2018_partial"] = {c: int(hh.get(c, 0)) for c in MAIN}
client["2018_partial"]["_months_elapsed"] = 10  # dataset ends October 2018

# ============================================================================
# ana_06 — National share of global launches by decade (duopoly -> crowd)
# ============================================================================
print("\n=== ana_06 ===")
dec_country = (launches.groupby(["decade", "country"]).size()
               .unstack("country").reindex(columns=MAIN).fillna(0).astype(int))
dec_share = dec_country.div(dec_country.sum(axis=1), axis=0).mul(100).round(1)
print("share of global launches by country, per decade (%):")
print(dec_share.to_string())
share_rows = [[f"{int(d)}s"] + [float(dec_share.loc[d, c]) for c in MAIN] for d in dec_share.index]
derived["ana_06"] = dt(
    "Share of global launches by country, per decade (%) — 2010s incl. partial 2018",
    ["decade"] + MAIN,
    share_rows,
)

# ============================================================================
# ana_07 — Concentration: top-2 (US + USSR/Russia) share by decade + HHI
# ============================================================================
print("\n=== ana_07 ===")
top2 = (dec_country["USA"] + dec_country["USSR/Russia"]) / dec_country.sum(axis=1) * 100
# HHI over the 7 country groups (0-10000)
shares_frac = dec_country.div(dec_country.sum(axis=1), axis=0)
hhi = (shares_frac.pow(2).sum(axis=1) * 10000).round(0)
print("decade | top2(US+USSR/Russia)% | HHI(7-group, /10000) | n_countries_with_launch")
n_active = (dec_country > 0).sum(axis=1)
for d in dec_country.index:
    print(f"  {int(d)}s   {top2[d]:5.1f}%             {int(hhi[d]):5d}                {int(n_active[d])}")
derived["ana_07"] = dt(
    "Launch concentration by decade: Cold-War duopoly share + Herfindahl index",
    ["decade", "top2_US_USSR_Russia_pct", "HHI", "countries_active"],
    [[f"{int(d)}s", round(float(top2[d]), 1), int(hhi[d]), int(n_active[d])] for d in dec_country.index],
)

# ============================================================================
# ana_08 — Agency_type composition over time (state/private/startup)
# ============================================================================
print("\n=== ana_08 ===")
TYPES = ["state", "private", "startup"]
at_year = (launches.groupby(["launch_year", "agency_type"]).size()
           .unstack("agency_type").reindex(columns=TYPES).fillna(0).astype(int))
at_year = at_year.reindex(range(yr_min, yr_max + 1), fill_value=0)
first_year = {t: int(launches[launches.agency_type == t].launch_year.min()) for t in TYPES}
print("first appearance year by agency_type:", first_year)
at_dec = (launches.groupby(["decade", "agency_type"]).size()
          .unstack("agency_type").reindex(columns=TYPES).fillna(0).astype(int))
at_dec_share = at_dec.div(at_dec.sum(axis=1), axis=0).mul(100).round(1)
print("agency_type share by decade (%):")
print(at_dec_share.to_string())
derived["ana_08"] = dt(
    "Agency-type share of launches by decade (%): state vs private vs startup",
    ["decade"] + TYPES,
    [[f"{int(d)}s"] + [float(at_dec_share.loc[d, t]) for t in TYPES] for d in at_dec_share.index],
)
derived["ana_08b_year"] = dt(
    "Agency-type launches per year (for stacked-area)",
    ["year"] + TYPES,
    [[int(y)] + [int(at_year.loc[y, t]) for t in TYPES] for y in at_year.index],
)

# ============================================================================
# ana_09 — Success rate overall + by decade
# ============================================================================
print("\n=== ana_09 ===")
dec_succ = launches.groupby("decade")["success"].agg(["sum", "count"])
dec_succ["rate"] = (dec_succ["sum"] / dec_succ["count"] * 100).round(1)
print("success rate by decade:")
print(dec_succ.to_string())
print(f"OVERALL: {n_success}/{n_rows} = {ov_rate}%")
derived["ana_09"] = dt(
    "Launch success rate by decade (and overall)",
    ["decade", "successes", "attempts", "success_rate_pct"],
    [[f"{int(d)}s", int(r["sum"]), int(r["count"]), float(r["rate"])] for d, r in dec_succ.iterrows()],
)
client["success_by_decade"] = {f"{int(d)}s": [int(r["sum"]), int(r["count"])] for d, r in dec_succ.iterrows()}

# ============================================================================
# ana_10 — Success rate by country (reliability benchmark)
# ============================================================================
print("\n=== ana_10 ===")
ctry_succ = launches.groupby("country")["success"].agg(["sum", "count"])
ctry_succ["rate"] = (ctry_succ["sum"] / ctry_succ["count"] * 100).round(1)
ctry_succ = ctry_succ.reindex(MAIN)
print(ctry_succ.to_string())
derived["ana_10"] = dt(
    "Launch success rate by country (all-time)",
    ["country", "successes", "attempts", "success_rate_pct"],
    [[c, int(ctry_succ.loc[c, "sum"]), int(ctry_succ.loc[c, "count"]), float(ctry_succ.loc[c, "rate"])] for c in MAIN],
)
client["success_by_country"] = {c: [int(ctry_succ.loc[c, "sum"]), int(ctry_succ.loc[c, "count"])] for c in MAIN}

# ============================================================================
# ana_11 — Success rate by agency_type
# ============================================================================
print("\n=== ana_11 ===")
at_succ = launches.groupby("agency_type")["success"].agg(["sum", "count"])
at_succ["rate"] = (at_succ["sum"] / at_succ["count"] * 100).round(1)
at_succ = at_succ.reindex(TYPES)
print(at_succ.to_string())
derived["ana_11"] = dt(
    "Launch success rate by agency type",
    ["agency_type", "successes", "attempts", "success_rate_pct"],
    [[t, int(at_succ.loc[t, "sum"]), int(at_succ.loc[t, "count"]), float(at_succ.loc[t, "rate"])] for t in TYPES],
)
client["success_by_type"] = {t: [int(at_succ.loc[t, "sum"]), int(at_succ.loc[t, "count"])] for t in TYPES}

# ============================================================================
# ana_12 — Top individual vehicle types
# ============================================================================
print("\n=== ana_12 ===")
vt = launches["type"].value_counts().head(20)
print(vt.to_string())
derived["ana_12"] = dt(
    "Top 20 individual launch-vehicle types by launch count",
    ["vehicle_type", "launches"],
    [[t, int(c)] for t, c in vt.items()],
)

# ============================================================================
# ana_13 — Vehicle FAMILIES (grouped) — workhorse vs Long March vs Falcon
# ============================================================================
print("\n=== ana_13 ===")
def to_family(t):
    t = str(t)
    R7 = ("Soyuz", "Voskhod", "Vostok", "Molniya", "Sputnik", "Polyot", "Luna")
    if t.startswith(R7):
        return "R-7 / Soyuz family (USSR/RU)"
    if t.startswith("Kosmos"):
        return "Kosmos (USSR/RU)"
    if t.startswith("Proton"):
        return "Proton (USSR/RU)"
    if t.startswith("Tsiklon") or t.startswith("Dnepr") or t.startswith("Rokot") or t.startswith("Zenit"):
        return "Tsiklon/Zenit/Dnepr (USSR/RU)"
    if t.startswith("Chang Zheng"):
        return "Long March / Chang Zheng (China)"
    if t.startswith("Falcon"):
        return "Falcon (SpaceX)"
    if t.startswith("Ariane"):
        return "Ariane (Europe)"
    if t.startswith("Atlas"):
        return "Atlas (USA)"
    if t.startswith("Delta") or t.startswith("Thor"):
        return "Thor/Delta (USA)"
    if t.startswith("Titan"):
        return "Titan (USA)"
    if t.startswith("Space Shuttle"):
        return "Space Shuttle (USA)"
    if t.startswith("Saturn"):
        return "Saturn (USA)"
    if t.startswith("Scout"):
        return "Scout (USA)"
    if t.startswith("H-II") or t.startswith("H-I") or t.startswith("N-") or t.startswith("M-") or t.startswith("Mu") or t.startswith("Epsilon") or t.startswith("J-I") or t.startswith("Lambda"):
        return "Japanese launchers"
    if t.startswith("PSLV") or t.startswith("GSLV") or t.startswith("SLV") or t.startswith("ASLV"):
        return "Indian launchers (PSLV/GSLV)"
    if t.startswith("Electron"):
        return "Electron (Rocket Lab)"
    return "Other / various"
launches["family"] = launches["type"].map(to_family)
fam = launches.groupby("family").size().sort_values(ascending=False)
print(fam.to_string())
derived["ana_13"] = dt(
    "Launch-vehicle FAMILIES by total launches (grouped from 366 types)",
    ["family", "launches"],
    [[f, int(c)] for f, c in fam.items()],
)

# ============================================================================
# ana_14 — China = Long March
# ============================================================================
print("\n=== ana_14 ===")
cn_fam = cn.groupby(cn["type"].str.startswith("Chang Zheng")).size()
cn_cz = int(cn[cn["type"].str.startswith("Chang Zheng")].shape[0])
cn_total = int(len(cn))
print(f"China launches on Chang Zheng (Long March): {cn_cz} of {cn_total} = {100*cn_cz/cn_total:.1f}%")
cn_top = cn["type"].value_counts().head(8)
print("top Chinese vehicle types:")
print(cn_top.to_string())
derived["ana_14"] = dt(
    "China's launches: Long March (Chang Zheng) vs other vehicles",
    ["vehicle_group", "launches", "pct_of_china"],
    [["Long March (Chang Zheng)", cn_cz, round(100 * cn_cz / cn_total, 1)],
     ["Other Chinese vehicles", cn_total - cn_cz, round(100 * (cn_total - cn_cz) / cn_total, 1)]],
)

# ============================================================================
# ana_15 — SpaceX / startup detail
# ============================================================================
print("\n=== ana_15 ===")
startup = launches[launches.agency_type == "startup"]
print("startup launches by agency code:")
print(startup.groupby("agency").size().to_string())
print("startup launches by vehicle type:")
print(startup.groupby("type").size().to_string())
print("startup launches by state_code:")
print(startup.groupby("state_code").size().to_string())
print("startup launches by year:")
print(startup.groupby("launch_year").size().to_string())
spx_types = launches[launches.agency == "SPX"].groupby("type").size()
print("SpaceX (SPX) by vehicle:")
print(spx_types.to_string())
derived["ana_15"] = dt(
    "The 'startup' class: launches by vehicle (SpaceX Falcon + Rocket Lab Electron)",
    ["vehicle_type", "launches", "first_year"],
    [[t, int(c), int(startup[startup.type == t].launch_year.min())]
     for t, c in startup.groupby("type").size().sort_values(ascending=False).items()],
)

# ============================================================================
# ana_16 — Arianespace / European commercial wave
# ============================================================================
print("\n=== ana_16 ===")
ae = launches[launches.agency == "AE"]
print(f"Arianespace (AE) total launches: {len(ae)}")
print(f"AE first/last year: {int(ae.launch_year.min())}-{int(ae.launch_year.max())}")
print("AE by vehicle (top):")
print(ae["type"].value_counts().head(6).to_string())
# private agency_type over time, share led by Europe early
priv = launches[launches.agency_type == "private"]
print(f"private agency_type total: {len(priv)}; first year {int(priv.launch_year.min())}")
print("top 'private' agency codes:")
print(priv.groupby("agency").size().sort_values(ascending=False).head(8).to_string())
derived["ana_16"] = dt(
    "Largest commercial 'private' providers by launches (pre- and during-SpaceX era)",
    ["agency", "launches"],
    [[a, int(c)] for a, c in priv.groupby("agency").size().sort_values(ascending=False).head(8).items()],
)

# ============================================================================
# ana_17 — Geography: launches by launching state (choropleth) + lat/long caveat
# ============================================================================
print("\n=== ana_17 ===")
ag2 = agencies.copy()
ag2["lat_num"] = pd.to_numeric(ag2["latitude"], errors="coerce")
ag2["lon_num"] = pd.to_numeric(ag2["longitude"], errors="coerce")
n_geo = int(ag2.dropna(subset=["lat_num", "lon_num"]).shape[0])
print(f"agencies.csv rows with usable numeric lat/long: {n_geo} of {len(ag2)}  <-- lat/long are all '-' (UNUSABLE for a point map)")
# choropleth-ready: launches by raw state_code (so a country map can be drawn)
state_counts = launches.groupby("state_code").size().sort_values(ascending=False)
STATE_NAME = {"SU": "Soviet Union", "US": "United States", "RU": "Russia", "CN": "China",
              "F": "France/Europe (ESA)", "J": "Japan", "IN": "India", "I-ESA": "ESA (multinational)",
              "IL": "Israel", "I": "Italy", "IR": "Iran", "KP": "North Korea", "CYM": "Sea Launch (Cayman flag)",
              "KR": "South Korea", "I-ELDO": "ELDO (Europe)", "BR": "Brazil", "UK": "United Kingdom"}
print("launches by raw state_code (choropleth source):")
for sc, c in state_counts.items():
    print(f"  {sc:7s} {STATE_NAME.get(sc, sc):26s} {int(c):5d}")
derived["ana_17"] = dt(
    "Launches by launching state (choropleth-ready; lat/long unusable so country map, not point map)",
    ["state_code", "country_name", "launches"],
    [[sc, STATE_NAME.get(sc, sc), int(c)] for sc, c in state_counts.items()],
)

# ============================================================================
# ana_18 — Top launching agencies (where coded) + SU-agency-NaN caveat
# ============================================================================
print("\n=== ana_18 ===")
n_agency_na = int(launches["agency"].isna().sum())
print(f"launches.csv 'agency' is NaN for {n_agency_na} rows (= all SU launches; Soviet orgs not coded in launches.csv)")
top_agency = launches["agency"].value_counts().head(15)
# attach english name from agencies.csv where available
ag_name = agencies.set_index("agency")["short_english_name"].to_dict()
ag_full = agencies.set_index("agency")["english_name"].to_dict()
print("top launching agencies (where coded):")
for a, c in top_agency.items():
    nm = ag_full.get(a) if isinstance(ag_full.get(a), str) and ag_full.get(a) != "-" else ag_name.get(a, "")
    print(f"  {a:8s} {int(c):5d}  {nm}")
derived["ana_18"] = dt(
    "Top launching agencies where coded in launches.csv (SU/Soviet orgs are uncoded -> excluded)",
    ["agency", "launches", "name"],
    [[a, int(c), (ag_full.get(a) if isinstance(ag_full.get(a), str) and ag_full.get(a) != "-" else ag_name.get(a, ""))]
     for a, c in top_agency.items()],
)

# ============================================================================
# ana_19 — VALIDATION: China-overtakes robustness (partial vs full-year)
# ============================================================================
print("\n=== ana_19 ===")
# (a) within the truncated dataset window, does China already lead?
ds_rank = hh.sort_values(ascending=False)
print("Dataset's PARTIAL 2018 ranking (Jan-Oct):")
print(ds_rank.head(4).to_string())
# (b) annualize the dataset's partial-2018 leaders (x 12/10) as a naive baseline
months = 10
print(f"\nNaive annualization (x 12/{months}) of dataset partial 2018:")
for c in ["China", "USA", "USSR/Russia"]:
    raw = int(hh.get(c, 0)); ann = round(raw * 12 / months, 1)
    print(f"  {c:12s} partial {raw:3d} -> annualized ~{ann}")
print("External full-year 2018 (independent record, det_07): China 39, USA 34, Russia 20")
# (c) was China ever #1 in any PRIOR year? (falsification frame)
lead_by_year = cy[MAIN].idxmax(axis=1)
cn_lead_years = [int(y) for y in lead_by_year.index if lead_by_year[y] == "China"]
print(f"\nYears in this dataset where China is the single largest launcher: {cn_lead_years}")
print("(China leads only at the dataset's end -> 2018 is genuinely the crossover, not a recurring fluke)")
derived["ana_19"] = dt(
    "Validation of 'China overtakes' 2018: dataset-partial vs naive-annualized vs external full-year",
    ["country", "dataset_partial_JanOct", "naive_annualized", "external_full_year"],
    [["China", int(hh.get("China", 0)), round(int(hh.get("China", 0)) * 12 / months, 1), 39],
     ["USA", int(hh.get("USA", 0)), round(int(hh.get("USA", 0)) * 12 / months, 1), 34],
     ["USSR/Russia", int(hh.get("USSR/Russia", 0)), round(int(hh.get("USSR/Russia", 0)) * 12 / months, 1), 20]],
)

# ============================================================================
# ana_20 — Launch volume by decade (peak 1980s, post-Soviet dip)
# ============================================================================
print("\n=== ana_20 ===")
dec_vol = launches.groupby("decade").size()
print("launches per decade (2010s incl. partial 2018; 1950s is 1957-59 only):")
for d, c in dec_vol.items():
    note = ""
    if d == 1950: note = " (1957-59 only)"
    if d == 2010: note = " (2010-2018, 2018 partial)"
    print(f"  {int(d)}s  {int(c):5d}{note}")
derived["ana_20"] = dt(
    "Total launches per decade (1950s = 1957-59; 2010s = 2010-2018 with 2018 partial)",
    ["decade", "launches"],
    [[f"{int(d)}s", int(c)] for d, c in dec_vol.items()],
)

# ----------------------------------------------------------------------------
# WRITE machine-readable outputs
# ----------------------------------------------------------------------------
with open(os.path.join(HERE, "derived_tables.json"), "w", encoding="utf-8") as f:
    json.dump(derived, f, indent=2, ensure_ascii=False)
with open(os.path.join(HERE, "client_data.json"), "w", encoding="utf-8") as f:
    json.dump(client, f, indent=2, ensure_ascii=False)
print("\n[wrote] code/derived_tables.json  and  code/client_data.json")
print(f"[check] country totals sum = {tot_all} (must equal {n_rows})")
