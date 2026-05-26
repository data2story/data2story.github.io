"""
Stage-2 / Analyst — narratives.py
Lightweight text-mining of the narr_cause column (the NTSB's own probable-cause prose).
We use regex keyword counts to recover the categorical signals that are missing
from the structured `phase_flt_spec` column (which is empty in this slice).
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

DATA = Path(r"D:\AI\journalist agent review\phase2\datasets\ntsb_small_aircraft\ga_accidents_2010_2024.csv")
df = pd.read_csv(DATA, dtype=object, low_memory=False)
df["inj_tot_f"] = pd.to_numeric(df["inj_tot_f"], errors="coerce").fillna(0)
df["fatal"] = df["ev_highest_injury"].eq("FATL")

# Use lowercase narr_cause text once.
df["cause_lc"] = df["narr_cause"].fillna("").str.lower()
df["has_cause"] = df["cause_lc"].str.len() > 0

# --- ana_20: How often each cause-language pattern appears, and its fatality share ---
print("=== ana_20 ===")

patterns = {
    "loss_of_control": r"loss of (?:airplane |aircraft )?control",
    "stall_aerodynamic": r"\bstall\b",
    "spin": r"\bspin(s|ned|ning)?\b",
    "fuel_exhaustion": r"fuel exhaustion|exhausted (?:the )?fuel|out of fuel",
    "fuel_starvation": r"fuel starvation|starved of fuel",
    "fuel_management": r"fuel (?:mis)?management|inadequate fuel",
    "engine_failure": r"engine failure|loss of engine power|partial loss of engine|engine malfunction",
    "vfr_into_imc": r"vfr (?:flight )?into (?:imc|instrument)|continued vfr flight into|continued visual flight into imc",
    "spatial_disorientation": r"spatial disorientation",
    "controlled_flight_into_terrain": r"controlled flight into terrain|cfit",
    "wire_strike": r"wire strike|struck (?:a |the )?wire|powerline",
    "bird_strike": r"bird strike|struck a bird",
    "icing": r"\bicing\b|airframe ice|carb(?:uretor)? ice",
    "go_around": r"go.?around",
    "runway_excursion": r"runway excursion|departed the runway|overran the runway|veered off the runway",
    "hard_landing": r"hard landing",
    "porpoise": r"porpois(e|ing)",
    "stall_spin": r"stall(\b.{0,20}\bspin)|stall/spin",
    "improper_decision": r"improper (?:decision|judgment)|inadequate decision",
    "pilot_inexperience": r"inexperience(?:d)?|insufficient (?:total )?experience",
    "alcohol_drugs": r"alcohol|impairment|drug",
    "midair_collision": r"mid.?air collision|midair collision",
    "structural_failure": r"structural failure|in.?flight breakup|in.?flight break.?up",
    # Phases recovered from text — recovers what phase_flt_spec lost:
    "phase_takeoff": r"\b(takeoff|take.?off|initial climb)\b",
    "phase_landing": r"\b(landing|touchdown|flare)\b",
    "phase_approach": r"\bapproach\b",
    "phase_cruise": r"\bcruise\b",
    "phase_maneuvering": r"\bmaneuver(?:ing|ed)?\b",
    "phase_taxi": r"\btaxi(?:ing|ed)?\b",
}

# Roll one row per event (use first non-null cause text per event).
ev = df.groupby("ev_id").agg(
    cause=("cause_lc", "first"),
    fatal=("fatal", "any"),
    deaths=("inj_tot_f", "max"),
).reset_index()
total_events = ev.shape[0]
events_with_cause = ev[ev["cause"].str.len() > 0]
total_with_cause = events_with_cause.shape[0]
print(f"events_total: {total_events}")
print(f"events_with_cause_text: {total_with_cause}")
print(f"cause_text_coverage_pct: {total_with_cause / total_events * 100:.1f}")

rows = []
for name, pat in patterns.items():
    rx = re.compile(pat)
    hit = events_with_cause["cause"].str.contains(rx, regex=True)
    n = int(hit.sum())
    fatal_n = int(events_with_cause.loc[hit, "fatal"].sum())
    deaths = int(events_with_cause.loc[hit, "deaths"].sum())
    pct = (n / total_with_cause * 100) if total_with_cause else 0.0
    fpct = (fatal_n / n * 100) if n else 0.0
    rows.append({
        "pattern": name,
        "events": n,
        "events_pct": round(pct, 1),
        "fatal_events": fatal_n,
        "fatal_share_pct": round(fpct, 1),
        "deaths_sum": deaths,
    })

cause_tbl = pd.DataFrame(rows).sort_values("events", ascending=False)
print(cause_tbl.to_string(index=False))

# --- ana_21: VFR-into-IMC by text vs by columns (cross-check det_05) ---
print("=== ana_21 ===")
text_hits = events_with_cause["cause"].str.contains(r"vfr (?:flight )?into (?:imc|instrument)|continued vfr flight into|continued visual flight into imc", regex=True)
text_n = int(text_hits.sum())
text_fatal = int(events_with_cause.loc[text_hits, "fatal"].sum())
print(f"text_vfr_into_imc_events: {text_n}")
print(f"text_vfr_into_imc_fatal_share_pct: {text_fatal / text_n * 100:.1f}")
print(f"deaths_in_those: {int(events_with_cause.loc[text_hits, 'deaths'].sum())}")

# --- ana_22: Phase-of-flight recovered from text — share of accidents by mention ---
print("=== ana_22 ===")
phase_pats = {k: patterns[k] for k in patterns if k.startswith("phase_")}
prows = []
for name, pat in phase_pats.items():
    rx = re.compile(pat)
    hit = events_with_cause["cause"].str.contains(rx, regex=True)
    n = int(hit.sum())
    fatal_n = int(events_with_cause.loc[hit, "fatal"].sum())
    prows.append({
        "phase_text_mention": name.replace("phase_", ""),
        "events": n,
        "events_pct_of_cause_text": round(n / total_with_cause * 100, 1),
        "fatal_events": fatal_n,
        "fatal_share_pct": round(fatal_n / n * 100, 1) if n else 0,
    })
ptbl = pd.DataFrame(prows).sort_values("events", ascending=False)
print(ptbl.to_string(index=False))

# --- ana_23: Top deadliest single events (worst events by deaths) ---
print("=== ana_23 ===")
worst = ev.sort_values("deaths", ascending=False).head(10)
print(worst[["ev_id", "deaths"]].to_string(index=False))

# Pull the cause text for the top-3 deadliest events as quote material.
print("\n--- Top-3 worst-event probable-cause quotes ---")
for _, r in worst.head(3).iterrows():
    cause_full = df.loc[df.ev_id == r.ev_id, "narr_cause"].dropna().iat[0]
    print(f"\n[{r.ev_id}, deaths={int(r.deaths)}]")
    print(cause_full[:600] + ("..." if len(cause_full) > 600 else ""))
