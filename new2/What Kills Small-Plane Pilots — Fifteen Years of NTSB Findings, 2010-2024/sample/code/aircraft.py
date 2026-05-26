"""
Stage-2 / Analyst — aircraft.py
Aircraft-side analyses: make/model normalization, homebuilt premium,
engine count, age, category-conditional fatality rates.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

DATA = Path(r"D:\AI\journalist agent review\phase2\datasets\ntsb_small_aircraft\ga_accidents_2010_2024.csv")
df = pd.read_csv(DATA, dtype=object, low_memory=False)
for c in ["inj_tot_f", "inj_tot_t", "num_eng", "acft_year", "ev_year"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["fatal"] = df["ev_highest_injury"].eq("FATL")

# --- Helper: collapse free-text manufacturer to a canonical brand bucket ---
BRAND_MAP = {
    "cessna": "Cessna",
    "piper": "Piper",
    "beech": "Beech",
    "raytheon aircraft": "Beech",
    "hawker beechcraft": "Beech",
    "textron aviation": "Cessna",
    "cirrus": "Cirrus",
    "mooney": "Mooney",
    "robinson": "Robinson",
    "bell": "Bell",
    "bellanca": "Bellanca",
    "aeronca": "Aeronca",
    "maule": "Maule",
    "schweizer": "Schweizer",
    "boeing": "Boeing",  # mostly Boeing/Stearman biplanes in GA
    "stearman": "Boeing",
    "luscombe": "Luscombe",
    "stinson": "Stinson",
    "champion": "Champion",
    "diamond": "Diamond",
    "american champion": "Champion",
    "van's": "Van's",
    "vans aircraft": "Van's",
    "vans": "Van's",
    "extra": "Extra",
    "grumman": "Grumman",
    "american aviation": "Grumman",
    "icon": "Icon",
    "kitfox": "Kitfox",
    "lancair": "Lancair",
    "glasair": "Glasair",
    "rans": "Rans",
    "zenith": "Zenith",
    "quad city": "Quad City",
    "rotorway": "Rotorway",
    "enstrom": "Enstrom",
    "schweizer": "Schweizer",
    "mcdonnell douglas": "McDonnell Douglas",
    "hughes": "Hughes",
    "sikorsky": "Sikorsky",
    "eurocopter": "Eurocopter",
    "airbus helicopters": "Eurocopter",
    "globe": "Globe",
    "ercoupe": "Ercoupe",
    "north american": "North American",
    "navion": "Navion",
}


def brand_of(make: str) -> str:
    if not isinstance(make, str):
        return "UNKNOWN"
    m = make.strip().lower()
    for key, label in BRAND_MAP.items():
        if key in m:
            return label
    # Fall back: title-case the raw token, keep top-of-list canonical.
    return make.strip().upper().split()[0].title() if make.strip() else "UNKNOWN"


df["brand"] = df["acft_make"].apply(brand_of)


# --- ana_08: Top manufacturer brands by accident count ---
print("=== ana_08 ===")
b = df.groupby("brand").agg(events=("ev_id", "nunique"), fatal_events=("fatal", "sum")).reset_index()
b["fatal_share_pct"] = (b.fatal_events / b.events * 100).round(1)
b = b.sort_values("events", ascending=False)
total_ev = df.ev_id.nunique()
b["share_of_all_pct"] = (b.events / total_ev * 100).round(1)
print(b.head(20).to_string(index=False))
print(f"top3_share_pct: {b.head(3).share_of_all_pct.sum():.1f}")

# --- ana_09: Top specific Cessna and Piper models ---
print("=== ana_09 ===")
df["acft_model_norm"] = df["acft_model"].fillna("").str.upper().str.strip()
m_cessna = df[df.brand == "Cessna"].groupby("acft_model_norm").size().sort_values(ascending=False).head(15)
print("--- Cessna ---")
print(m_cessna.to_string())
m_piper = df[df.brand == "Piper"].groupby("acft_model_norm").size().sort_values(ascending=False).head(15)
print("--- Piper ---")
print(m_piper.to_string())

# --- ana_10: Homebuilt vs factory-certificated — accident count and fatal share ---
print("=== ana_10 ===")
hb = df.groupby(df.homebuilt.fillna("?")).agg(
    aircraft_rows=("ev_id", "size"),
    events=("ev_id", "nunique"),
    fatal_events=("fatal", "sum"),
).reset_index().rename(columns={"homebuilt": "homebuilt_flag"})
hb["fatal_share_pct"] = (hb.fatal_events / hb.events * 100).round(1)
print(hb.to_string(index=False))
# Detective det_04 claims roughly 4x higher fatal rate for E/A-B versus certificated.
# We can't compute per-100k-hour rate without exposure denominator, but we can compare fatal-share within accidents.
hb_y = hb[hb.homebuilt_flag == "Y"].fatal_share_pct.iat[0]
hb_n = hb[hb.homebuilt_flag == "N"].fatal_share_pct.iat[0]
print(f"homebuilt_fatal_share_pct: {hb_y}")
print(f"factory_fatal_share_pct: {hb_n}")
print(f"ratio_homebuilt_over_factory: {hb_y / hb_n:.2f}x")

# --- ana_11: Engine count distribution and fatal share ---
print("=== ana_11 ===")
eng = df.groupby(df.num_eng.fillna(-1).astype(int)).agg(
    events=("ev_id", "nunique"), fatal_events=("fatal", "sum")
).reset_index().rename(columns={"num_eng": "engines"})
eng["fatal_share_pct"] = (eng.fatal_events / eng.events * 100).round(1)
print(eng.to_string(index=False))

# --- ana_12: Aircraft age (event year minus acft_year) ---
print("=== ana_12 ===")
df["age_yrs"] = df.ev_year - df.acft_year
age = df["age_yrs"].dropna()
print(f"median_age_yrs: {age.median():.0f}")
print(f"mean_age_yrs: {age.mean():.1f}")
print(f"pct_over_30: {(age > 30).mean() * 100:.1f}")
print(f"pct_over_40: {(age > 40).mean() * 100:.1f}")
print(f"pct_over_50: {(age > 50).mean() * 100:.1f}")
# bucketed distribution for chart
buckets = pd.cut(age, bins=[-1, 5, 10, 20, 30, 40, 50, 200], labels=["0-5", "6-10", "11-20", "21-30", "31-40", "41-50", "50+"])
print(buckets.value_counts().sort_index().to_string())

# --- ana_13: Type-of-flying breakdown (personal vs instructional vs other) ---
print("=== ana_13 ===")
type_map = {
    "PERS": "Personal",
    "INST": "Instructional",
    "BUS": "Business",
    "BUS ": "Business",
    "EXEC": "Business",
    "FERY": "Ferry",
    "POSI": "Positioning",
    "OWRK": "Other-work",
    "GLDT": "Glider-tow",
    "AOBV": "Aerial-obs",
    "SKYD": "Skydiving",
    "BANT": "Banner-tow",
    "AAPL": "Aerial-app",
    "PUBF": "Public",
    "PUBS": "Public",
    "PUBL": "Public",
    "PUBU": "Public",
    "ASHO": "Air-show",
    "FIRF": "Firefighting",
    "FLTS": "Flight-test",
    "EXLD": "External-load",
    "ADRP": "Airdrop",
    "UNK": "Unknown",
    "UNK ": "Unknown",
}
df["flight_type"] = df["type_fly"].map(type_map).fillna("Other")
ft = df.groupby("flight_type").agg(events=("ev_id", "nunique"), fatal_events=("fatal", "sum")).reset_index()
ft["fatal_share_pct"] = (ft.fatal_events / ft.events * 100).round(1)
ft = ft.sort_values("events", ascending=False)
print(ft.to_string(index=False))
