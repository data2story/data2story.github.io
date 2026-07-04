"""
Data2Story Analyst -- the 2026 World Cup squad as a diaspora map (squad_2026.csv).

ana_09  15 of 26 born abroad: the birth-country breakdown
ana_10  Caps & goals by birth group; every WC2026 goal traced to a birthplace
ana_11  All 26 play their club football outside Cape Verde

Goal attributions for WC2026 matches (scorers are not in international_results.csv)
come from detective.json det_01/det_02 sourced facts; birth countries from the CSV.

Run:  py squad_analysis.py     (PYTHONUTF8=1; deterministic, local files only)
"""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR", r"D:\AI\journalist agent review\phase2\data\cape-verde-diaspora"
)
s = pd.read_csv(os.path.join(DATA_DIR, "03_football", "squad_2026.csv"))

# --- ana_09: 15 of 26 born abroad -- birth-country breakdown ---
print("=== ana_09 ===")
n = len(s)
abroad = s[s.born_abroad]
print(f"born abroad: {len(abroad)}/{n} = {len(abroad) / n * 100:.1f}%")
bc = s.birth_country.value_counts()
for c, v in bc.items():
    print(f"  {c}: {v}")
pos_split = s.groupby("pos").born_abroad.agg(["sum", "count"])
print("by position (born_abroad / total):")
for p_, row in pos_split.iterrows():
    print(f"  {p_}: {int(row['sum'])}/{int(row['count'])}")
s["age_20260703"] = ((pd.Timestamp("2026-07-03") - pd.to_datetime(s.dob)).dt.days / 365.25)
old = s.loc[s.age_20260703.idxmax()]
yng = s.loc[s.age_20260703.idxmin()]
print(f"oldest : {old['name']} {old.age_20260703:.1f}y (b. {old.dob}, {old.birth_country})")
print(f"youngest: {yng['name']} {yng.age_20260703:.1f}y (b. {yng.dob}, {yng.birth_country})")

# --- ana_10: caps & goals by birth group; WC2026 goals traced ---
print("=== ana_10 ===")
grp = s.groupby("born_abroad")[["caps", "goals"]].sum()
tot_caps, tot_goals = s.caps.sum(), s.goals.sum()
ab_caps, ab_goals = grp.loc[True, "caps"], grp.loc[True, "goals"]
print(f"total caps: {tot_caps}, from born-abroad players: {ab_caps} "
      f"({ab_caps / tot_caps * 100:.1f}%)")
print(f"total pre-tournament goals: {tot_goals}, from born-abroad players: {ab_goals} "
      f"({ab_goals / tot_goals * 100:.1f}%)")
top_scorer = s.loc[s.goals.idxmax()]
print(f"top pre-tournament scorer: {top_scorer['name']} ({int(top_scorer.goals)} goals, "
      f"{int(top_scorer.caps)} caps, born {top_scorer.birth_country})")
by_country = s.groupby("birth_country")[["caps", "goals"]].sum().join(
    s.birth_country.value_counts().rename("players")).sort_values("players", ascending=False)
print(by_country.to_string())
# WC2026 goals: scorers per det_01 (vs Argentina) and det_02 (vs Uruguay)
wc_scorers = ["Kevin Pina", "Hélio Varela", "Deroy Duarte", "Sidny Lopes Cabral"]
print("WC2026 goalscorers traced to birth country (det_01/det_02 + squad csv):")
for nm in wc_scorers:
    row = s[s.name == nm].iloc[0]
    print(f"  {nm}: born {row.birth_country} (caps {int(row.caps)}, "
          f"pre-tournament goals {int(row.goals)})")
n_abroad_goals = sum(s[s.name == nm].iloc[0].born_abroad for nm in wc_scorers)
print(f"WC2026 goals by born-abroad players: {n_abroad_goals}/4; "
      f"both Argentina-match scorers born in the Netherlands (Rotterdam, det_04)")
print("cross-check det_04: Deroy Duarte pre-tournament goals = "
      f"{int(s[s.name == 'Deroy Duarte'].iloc[0].goals)} "
      "(his 59' vs Argentina was indeed his first international goal)")

# --- ana_11: all 26 play club football outside Cape Verde ---
print("=== ana_11 ===")
cc = s.club_country.value_counts()
print(f"club countries: {s.club_country.nunique()}; players at clubs in Cape Verde: "
      f"{int((s.club_country == 'CPV').sum())}")
for c, v in cc.items():
    print(f"  {c}: {v}")
