"""06_time.py — within-2024 time patterns (Jan 1 – Feb 23 sample window)."""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:\AI\journalist agent review\phase2\datasets\openfda_faers_2024",
)
sample = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_sample.csv"))
sample["dt"] = pd.to_datetime(sample["receivedate"].astype(str), format="%Y%m%d", errors="coerce")

# --- ana_29: Daily report volume across the 54-day window ---
print("=== ana_29 ===")
daily = sample.groupby(sample["dt"].dt.date).size().reset_index(name="n_reports")
daily.columns = ["date", "n_reports"]
print(daily.to_string(index=False))

# --- ana_30: Weekday vs weekend ---
print("=== ana_30 ===")
sample["dow"] = sample["dt"].dt.day_name()
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow = sample["dow"].value_counts().reindex(dow_order)
print(dow.to_string())
print(f"weekday total: {dow[:5].sum():,}")
print(f"weekend total: {dow[5:].sum():,}")
print(f"weekday avg/day: {dow[:5].sum()/dow[:5].count():.0f} (across 5 weekdays in pattern)")

# --- ana_31: serious% over time ---
print("=== ana_31 ===")
sample["week"] = sample["dt"].dt.to_period("W").astype(str)
weekly = sample.groupby("week").agg(
    n=("serious", "count"),
    serious=("serious", lambda x: (x == 1).sum()),
    death=("seriousnessdeath", lambda x: (x == 1).sum()),
    hosp=("seriousnesshospitalization", lambda x: (x == 1).sum()),
).reset_index()
weekly["pct_serious"] = weekly["serious"] / weekly["n"] * 100
weekly["pct_death"] = weekly["death"] / weekly["n"] * 100
weekly["pct_hosp"] = weekly["hosp"] / weekly["n"] * 100
print(weekly.to_string(index=False))
