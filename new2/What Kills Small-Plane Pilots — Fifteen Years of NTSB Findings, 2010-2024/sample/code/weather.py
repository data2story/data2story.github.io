"""
Stage-2 / Analyst — weather.py
VFR-into-IMC, VMC vs IMC, light_cond, and the day-vs-night fatality split.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(r"D:\AI\journalist agent review\phase2\datasets\ntsb_small_aircraft\ga_accidents_2010_2024.csv")
df = pd.read_csv(DATA, dtype=object, low_memory=False)
df["inj_tot_f"] = pd.to_numeric(df["inj_tot_f"], errors="coerce").fillna(0)
df["fatal"] = df["ev_highest_injury"].eq("FATL")

# Roll up to one row per event for state-level comparisons.
ev = df.drop_duplicates("ev_id").copy()
ev_id_fatal = df.groupby("ev_id")["fatal"].any()
ev["any_fatal"] = ev["ev_id"].map(ev_id_fatal)

# --- ana_17: VMC vs IMC accident share + fatality share ---
print("=== ana_17 ===")
wx = ev.groupby(ev["wx_cond_basic"].fillna("UNK")).agg(
    events=("ev_id", "count"),
    fatal_events=("any_fatal", "sum"),
).reset_index().rename(columns={"wx_cond_basic": "wx"})
wx["share_of_events_pct"] = (wx.events / wx.events.sum() * 100).round(1)
wx["fatal_share_pct"] = (wx.fatal_events / wx.events * 100).round(1)
print(wx.to_string(index=False))

vmc_fatal = wx[wx.wx == "VMC"].fatal_share_pct.iat[0]
imc_fatal = wx[wx.wx == "IMC"].fatal_share_pct.iat[0]
print(f"VMC fatal_share: {vmc_fatal}%")
print(f"IMC fatal_share: {imc_fatal}%")
print(f"IMC vs VMC ratio: {imc_fatal / vmc_fatal:.1f}x")

# --- ana_18: VFR-into-IMC — IMC weather with non-IFR flight plan ---
print("=== ana_18 ===")
# Define the canonical pattern from det_05: wx = IMC, flight plan != IFR (NONE / VFR / CVFR / MVFR / NaN / UNK)
def is_vfr_into_imc(row) -> bool:
    if pd.isna(row.wx_cond_basic) or row.wx_cond_basic != "IMC":
        return False
    fp = row.flt_plan_filed
    if pd.isna(fp):
        return True  # absence of plan in IMC counts
    return fp in {"NONE", "VFR", "CVFR", "MVFR", "UNK"}


ev["vfr_into_imc"] = ev.apply(is_vfr_into_imc, axis=1)
v = ev.groupby("vfr_into_imc").agg(events=("ev_id", "count"), fatal_events=("any_fatal", "sum")).reset_index()
v["fatal_share_pct"] = (v.fatal_events / v.events * 100).round(1)
print(v.to_string(index=False))

# Sub-table for a 2x2 chart: weather × flight-plan-class
ev["fp_class"] = ev.flt_plan_filed.where(
    ev.flt_plan_filed.isin(["IFR", "VFR", "CVFR", "NONE", "MVFR", "VFIF"]),
    "OTHER",
).fillna("MISSING")
ev["wx_class"] = ev.wx_cond_basic.where(ev.wx_cond_basic.isin(["VMC", "IMC"]), "UNK").fillna("UNK")
matrix = ev.groupby(["wx_class", "fp_class"]).agg(
    events=("ev_id", "count"),
    fatal_events=("any_fatal", "sum"),
).reset_index()
matrix["fatal_share_pct"] = (matrix.fatal_events / matrix.events * 100).round(1)
print(matrix.to_string(index=False))

# --- ana_19: Light conditions — day vs night fatality ---
print("=== ana_19 ===")
light_map = {"DAYL": "Day", "NITE": "Night", "DUSK": "Dusk", "DAWN": "Dawn", "NDRK": "Night-dark", "NBRT": "Night-bright"}
ev["light"] = ev.light_cond.map(light_map).fillna("Unknown")
lt = ev.groupby("light").agg(events=("ev_id", "count"), fatal_events=("any_fatal", "sum")).reset_index()
lt["fatal_share_pct"] = (lt.fatal_events / lt.events * 100).round(1)
lt["share_of_events_pct"] = (lt.events / lt.events.sum() * 100).round(1)
print(lt.sort_values("events", ascending=False).to_string(index=False))

# A coarser day/night/twilight bucket for charting:
def coarse_light(x):
    if x in {"DAYL"}: return "Day"
    if x in {"NITE", "NDRK", "NBRT"}: return "Night"
    if x in {"DUSK", "DAWN"}: return "Twilight"
    return "Unknown"


ev["light_coarse"] = ev.light_cond.apply(coarse_light)
lc = ev.groupby("light_coarse").agg(events=("ev_id", "count"), fatal_events=("any_fatal", "sum")).reset_index()
lc["fatal_share_pct"] = (lc.fatal_events / lc.events * 100).round(1)
print(lc.to_string(index=False))
