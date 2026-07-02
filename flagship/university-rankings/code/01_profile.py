"""
01_profile.py — dataset profile + field inventory + methodology-weight lookup.
Run from DATA_DIR:  PYTHONUTF8=1 py "<PROJECT_DIR>/code/01_profile.py"
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c  # noqa: E402

DATA = c.DATA_DIR

# --- ana_01: Dataset profile — files, rows, coverage years, one-row meaning ---
print("=== ana_01 ===")
files = {
    "THE (the/timesData.csv)": ("the/timesData.csv", "world_rank", "year"),
    "ARWU (arwu/shanghaiData.csv)": ("arwu/shanghaiData.csv", "world_rank", "year"),
    "QS 2023 (qs/QS_2023_Dataset.csv)": ("qs/QS_2023_Dataset.csv", "rank display", None),
    "CWUR (cwur/cwurData.csv)": ("cwur/cwurData.csv", "world_rank", "year"),
    "OpenAlex (openalex/openalex_institutions_research_output.csv)":
        ("openalex/openalex_institutions_research_output.csv", None, None),
    "join crosswalk (_join/school_and_country_table.csv)":
        ("_join/school_and_country_table.csv", None, None),
}
for label, (path, _rank, yearcol) in files.items():
    df = pd.read_csv(os.path.join(DATA, path))
    yrs = ""
    if yearcol and yearcol in df.columns:
        u = sorted(df[yearcol].unique())
        yrs = f" | years {u[0]}-{u[-1]}"
    print(f"{label}: rows={len(df)}, cols={df.shape[1]}{yrs}")
lei = pd.read_excel(os.path.join(DATA, "leiden", "leiden_open_2024_universities.xlsx"))
print(f"Leiden registry (leiden/..xlsx): rows={len(lei)}, cols={lei.shape[1]} (name/ROR/country only)")
print("One row = one university's placement in one system"
      " (THE/ARWU/CWUR carry a `year`; QS is the single 2023 edition; OpenAlex is one row per institution).")
print("Cleanest cross-SYSTEM year = 2015 (THE 2015 rows=%d, ARWU 2015 rows=%d, CWUR 2015 rows=%d)."
      % ((pd.read_csv(os.path.join(DATA, 'the/timesData.csv')).year == 2015).sum(),
         (pd.read_csv(os.path.join(DATA, 'arwu/shanghaiData.csv')).year == 2015).sum(),
         (pd.read_csv(os.path.join(DATA, 'cwur/cwurData.csv')).year == 2015).sum()))

# --- ana_01b: per-column missing/quirk audit for the join-relevant columns ---
print("=== ana_01b ===")
the = pd.read_csv(os.path.join(DATA, "the/timesData.csv"))
the15 = the[the.year == 2015]
print("THE 2015 world_rank banded (non-integer) rows:",
      the15["world_rank"].astype(str).str.contains("-").sum(),
      "e.g.", [x for x in the15["world_rank"].unique() if "-" in str(x)][:4])
qs = pd.read_csv(os.path.join(DATA, "qs/QS_2023_Dataset.csv"))
print("QS 'score scaled' non-numeric rows:",
      pd.to_numeric(qs["score scaled"], errors="coerce").isna().sum(),
      "| QS rank display tie rows ('='):", qs["rank display"].astype(str).str.contains("=").sum())
oa = pd.read_csv(os.path.join(DATA, "openalex/openalex_institutions_research_output.csv"))
print("OpenAlex two_yr_mean_citedness anomalies (>15 vs peer median %.2f):" % oa.two_yr_mean_citedness.median(),
      oa[oa.two_yr_mean_citedness > 15][["institution", "two_yr_mean_citedness"]].to_dict("records"))
cwur = pd.read_csv(os.path.join(DATA, "cwur/cwurData.csv"))
print("CWUR indicator cols are RANKS (1=best), opposite direction to 0-100 scores. "
      "2015 broad_impact nulls:", cwur[cwur.year == 2015]["broad_impact"].isna().sum(),
      "| 2012-2013 broad_impact nulls:", cwur[cwur.year.isin([2012, 2013])]["broad_impact"].isna().sum())

# --- ana_02: methodology weighting lookup (perception -> measured-output axis) ---
# Source: detective det_02..det_07 (published methodologies). Not computed from CSV;
# it is the mechanical REASON the tables disagree, encoded as a chart-ready table.
print("=== ana_02 ===")
weights = [
    # system, reputation_survey_share_pct, citations/impact, research_output/prizes, teaching/faculty, international, industry
    ("QS 2023 (legacy)", 50, 20, 0, 20, 10, 0),
    ("THE (2011-2023)",  33, 30, 0, 30, 7.5, 2.5),
    ("ARWU",              0,  20, 70, 0, 0, 0),
    ("CWUR (current)",    0,  10, 75, 0, 0, 0),
    ("OpenAlex",          0, 100, 0, 0, 0, 0),
]
print("system | reputation% | citations/impact% | research-output/prizes% | teaching/faculty% | intl% | industry%")
for row in weights:
    print(row)
print("Reputation-survey share ranks the systems on a perception<->output axis: "
      "QS 50% > THE 33% > ARWU 0% = CWUR 0%; OpenAlex 0% (pure output).")
