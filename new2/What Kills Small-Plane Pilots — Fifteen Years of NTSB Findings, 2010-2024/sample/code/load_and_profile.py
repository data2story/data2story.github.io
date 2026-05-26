"""
Stage-2 / Analyst — load_and_profile.py
Loads the NTSB GA Part-91 slice, prints a one-screen profile,
then computes core distributions used by every downstream script.

Run from any cwd; paths are absolute so output is reproducible.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

DATA = Path(r"D:\AI\journalist agent review\phase2\datasets\ntsb_small_aircraft\ga_accidents_2010_2024.csv")

# Load — dtype=object so we don't lose codes like '091' or partial dates.
df = pd.read_csv(DATA, dtype=object, low_memory=False)

# Cast a handful of cols we'll use numerically.
for col in ["ev_year", "ev_month", "inj_tot_f", "inj_tot_s", "inj_tot_m", "inj_tot_t", "num_eng", "acft_year"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"rows: {len(df)}")
print(f"columns: {df.shape[1]}")
print(f"year_range: {int(df.ev_year.min())}..{int(df.ev_year.max())}")
print(f"distinct_events (ev_id): {df.ev_id.nunique()}")
multi_acft = len(df) - df.ev_id.nunique()
print(f"multi_aircraft_event_rows: {multi_acft}")
nn = df.notna().mean().sort_values(ascending=False)
print("col_nonnull_rate_top10:")
print(nn.head(10).to_string())
print("col_nonnull_rate_bottom10:")
print(nn.tail(10).to_string())

# Severity / damage normalization — used downstream.
df["fatal"] = df["ev_highest_injury"].eq("FATL")
df["destroyed"] = df["damage"].eq("DEST")
df["is_homebuilt"] = df["homebuilt"].eq("Y")

# --- ana_02: Annual event and fatal-event counts ---
print("=== ana_02 ===")
# An "event" should be deduped on ev_id (so a 2-airplane midair counts once);
# fatal-event = the event has at least one row with FATL.
ev = df.drop_duplicates("ev_id")
ev_fatal = (
    df.groupby("ev_id")["fatal"].any().reset_index(name="any_fatal").merge(ev[["ev_id", "ev_year"]], on="ev_id")
)
yearly = ev_fatal.groupby("ev_year").agg(events=("ev_id", "count"), fatal_events=("any_fatal", "sum")).reset_index()
yearly["fatal_share_pct"] = (yearly.fatal_events / yearly.events * 100).round(1)
print(yearly.to_string(index=False))

# --- ana_03: Month-of-year seasonality ---
print("=== ana_03 ===")
ev_month = df.drop_duplicates("ev_id").assign(any_fatal=lambda d: d["ev_id"].map(df.groupby("ev_id")["fatal"].any()))
month = ev_month.groupby("ev_month").agg(events=("ev_id", "count"), fatal_events=("any_fatal", "sum")).reset_index()
month["fatal_share_pct"] = (month.fatal_events / month.events * 100).round(1)
print(month.to_string(index=False))

# --- ana_04: Highest-injury distribution (across aircraft-rows) ---
print("=== ana_04 ===")
inj = df["ev_highest_injury"].fillna("UNKNOWN").value_counts(dropna=False)
inj_pct = (inj / inj.sum() * 100).round(2)
print(pd.concat([inj.rename("count"), inj_pct.rename("pct")], axis=1).to_string())

# --- ana_05: Aircraft-damage distribution ---
print("=== ana_05 ===")
dmg = df["damage"].fillna("UNKNOWN").value_counts(dropna=False)
dmg_pct = (dmg / dmg.sum() * 100).round(2)
print(pd.concat([dmg.rename("count"), dmg_pct.rename("pct")], axis=1).to_string())

# --- ana_06: Phase of flight ---
print("=== ana_06 ===")
# Many phase codes; tally raw values then map the common ones.
phase = df["phase_flt_spec"].fillna("UNKNOWN").value_counts()
phase_pct = (phase / phase.sum() * 100).round(2)
top_phase = pd.concat([phase.rename("count"), phase_pct.rename("pct")], axis=1).head(20)
print(top_phase.to_string())
print(f"distinct_phase_codes: {df['phase_flt_spec'].nunique(dropna=True)}")

# --- ana_07: Aircraft category (AIR / HELI / GYRO / GLDR / BALL / etc.) ---
print("=== ana_07 ===")
cat = df["acft_category"].fillna("UNKNOWN").value_counts()
cat_pct = (cat / cat.sum() * 100).round(2)
print(pd.concat([cat.rename("count"), cat_pct.rename("pct")], axis=1).to_string())

# Save normalized helpers to a parquet file so later scripts don't re-parse.
OUT = Path(r"D:\AI\journalist agent review\phase2\project\ntsb_small_aircraft\blog_opus47_0525_2243\code\_normalized.parquet")
keep = [c for c in df.columns if c not in {"narr_accp", "narr_accf", "narr_cause"}]
keep.extend(["fatal", "destroyed", "is_homebuilt"])
df_keep = df[list(dict.fromkeys(keep))]
try:
    df_keep.to_parquet(OUT, index=False)
    print(f"wrote: {OUT}")
except Exception as exc:  # pyarrow may not be installed; fall through to CSV
    OUT_CSV = OUT.with_suffix(".csv")
    df_keep.to_csv(OUT_CSV, index=False)
    print(f"wrote: {OUT_CSV} (parquet failed: {exc})")
