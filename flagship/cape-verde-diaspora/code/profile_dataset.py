"""
Data2Story Analyst -- Cape Verde diaspora nation: dataset profile.

Profiles every file the analysis uses: rows, columns, missing values,
cardinality, time ranges. Feeds the `dataset` block of analyst.json.

Run:  py profile_dataset.py     (PYTHONUTF8=1; deterministic, local files only)
DATA_DIR resolves from the env var, defaulting to the canonical dataset path.
"""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR", r"D:\AI\journalist agent review\phase2\data\cape-verde-diaspora"
)
P = lambda *a: os.path.join(DATA_DIR, *a)

print("=== profile ===")

# 01 diaspora slice (UN DESA IMS 2024, origin = Cabo Verde)
d = pd.read_csv(P("01_diaspora", "cape_verde_emigrants_by_destination.csv"))
print(f"[diaspora slice] rows={len(d)} cols={d.shape[1]} "
      f"destinations={d[~d.is_world_total].destination.nunique()} "
      f"waves={sorted(d.year.unique())} missing_migrants={d.migrants.isna().sum()}")

# 02 remittances (WB WDI BX.TRF.PWKR.DT.GD.ZS, tidy long)
r = pd.read_csv(P("02_remittances", "remittances_pct_gdp_tidy.csv"))
cpv_r = r[r["Country Code"] == "CPV"]
print(f"[remittances] rows={len(r)} entities={r['Country Code'].nunique()} "
      f"years={r.year.min()}-{r.year.max()} CPV_years={len(cpv_r)} "
      f"CPV_range={cpv_r.year.min()}-{cpv_r.year.max()}")

# 03 football results (martj42, CC0)
f = pd.read_csv(P("03_football", "international_results.csv"))
played = f.dropna(subset=["home_score", "away_score"])
sched = f[f.home_score.isna()]
cv = played[(played.home_team == "Cape Verde") | (played.away_team == "Cape Verde")]
print(f"[results] rows={len(f)} played={len(played)} scheduled_unplayed={len(sched)} "
      f"dates={f.date.min()}..{f.date.max()} teams={pd.concat([f.home_team, f.away_team]).nunique()} "
      f"tournaments={f.tournament.nunique()}")
print(f"[results] Cape Verde played matches={len(cv)} first={cv.date.min()} last={cv.date.max()}")
print("[results] scheduled (NaN-score) rows are FUTURE fixtures and are DROPPED everywhere:")
print(sched[["date", "home_team", "away_team", "tournament"]].to_string(index=False))

# 03 squad
s = pd.read_csv(P("03_football", "squad_2026.csv"))
print(f"[squad] rows={len(s)} cols={s.shape[1]} born_abroad={int(s.born_abroad.sum())} "
      f"birth_countries={s.birth_country.nunique()} missing={int(s.isna().sum().sum())}")

# 04 population (WB WDI SP.POP.TOTL, tidy long)
p = pd.read_csv(P("04_population", "population_total_tidy.csv"))
cpv_p = p[p["Country Code"] == "CPV"]
print(f"[population] rows={len(p)} entities={p['Country Code'].nunique()} "
      f"years={p.year.min()}-{p.year.max()} CPV_2025={int(cpv_p[cpv_p.year == 2025].population.iloc[0]):,}")

# WB metadata (aggregate filter: Region is empty for aggregates like 'World')
m = pd.read_csv(P("04_population",
                  "Metadata_Country_API_SP.POP.TOTL_DS2_EN_csv_v2_3107.csv"),
                encoding="utf-8-sig")
n_countries = m.Region.notna().sum()
print(f"[metadata] entities={len(m)} true_countries(Region non-empty)={n_countries} "
      f"aggregates={m.Region.isna().sum()}")
