"""
Stage-2 / Analyst — geography.py
State-level accident counts, the Alaska outlier, and an injuries-by-region split.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(r"D:\AI\journalist agent review\phase2\datasets\ntsb_small_aircraft\ga_accidents_2010_2024.csv")
df = pd.read_csv(DATA, dtype=object, low_memory=False)
df["inj_tot_f"] = pd.to_numeric(df["inj_tot_f"], errors="coerce").fillna(0)
df["fatal"] = df["ev_highest_injury"].eq("FATL")

# --- ana_14: Events and fatalities by state, top 15 ---
print("=== ana_14 ===")
ev = df.drop_duplicates("ev_id")
fatal_by_ev = df.groupby("ev_id")["inj_tot_f"].max().reset_index()
ev = ev.merge(fatal_by_ev, on="ev_id", suffixes=("", "_x"))
state = ev.groupby("ev_state").agg(
    events=("ev_id", "count"),
    fatal_events=("inj_tot_f", lambda x: (x > 0).sum()),
    deaths=("inj_tot_f", "sum"),
).reset_index().sort_values("events", ascending=False)
total_ev = ev.shape[0]
state["events_share_pct"] = (state.events / total_ev * 100).round(1)
state["fatal_share_pct"] = (state.fatal_events / state.events * 100).round(1)
print(state.head(15).to_string(index=False))
print(f"total_states: {state.shape[0]}")

# --- ana_15: Alaska focused split ---
print("=== ana_15 ===")
ak = state[state.ev_state == "AK"].iloc[0]
print(f"AK events: {ak.events}  ({ak.events_share_pct}% of all)")
print(f"AK deaths: {int(ak.deaths)}")
print(f"AK fatal_share_pct: {ak.fatal_share_pct}")
# compare AK fatal share with rest-of-US fatal share
rest = ev[ev.ev_state != "AK"]
rest_events = rest.shape[0]
rest_fatal_events = (rest.inj_tot_f > 0).sum()
rest_share = rest_fatal_events / rest_events * 100
print(f"Rest_of_US fatal_share_pct: {rest_share:.1f}")
print(f"AK_vs_rest_fatal_share_ratio: {ak.fatal_share_pct / rest_share:.2f}x")

# Lower-48 state events per capita would need population denominator;
# instead we report raw state events for the map.
state.to_csv(Path(__file__).parent / "_state_table.csv", index=False)

# --- ana_16: Top deadliest cities by total deaths ---
print("=== ana_16 ===")
city = ev.groupby(["ev_city", "ev_state"]).agg(
    events=("ev_id", "count"),
    deaths=("inj_tot_f", "sum"),
).reset_index()
city = city.sort_values("deaths", ascending=False)
print(city.head(15).to_string(index=False))
