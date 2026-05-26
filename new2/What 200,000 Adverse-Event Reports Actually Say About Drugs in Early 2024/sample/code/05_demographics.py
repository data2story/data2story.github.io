"""05_demographics.py — sex, age, country distribution."""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:\AI\journalist agent review\phase2\datasets\openfda_faers_2024",
)
sample = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_sample.csv"))
N = len(sample)

# --- ana_22: Sex distribution ---
print("=== ana_22 ===")
sex_map = {0: "Unknown", 1: "Male", 2: "Female"}
sex_vc = sample["patient_sex"].value_counts(dropna=False)
for code, n in sex_vc.items():
    lab = sex_map.get(code, "MISSING")
    print(f"{lab}\t{n:,}\t{n/N*100:.2f}%")

# --- ana_23: Age distribution (only rows with age in years) ---
print("=== ana_23 ===")
# unit 801 = Year per OpenFDA spec
yrs = sample[(sample["patient_onset_age_unit"] == 801) & sample["patient_onset_age"].notna()].copy()
print(f"rows with valid age in years: {len(yrs):,} ({len(yrs)/N*100:.1f}%)")
print(f"median: {yrs['patient_onset_age'].median():.1f}  mean: {yrs['patient_onset_age'].mean():.1f}")
# bins
bins = [0,18,30,40,50,60,70,80,90,200]
labels=["<18","18-29","30-39","40-49","50-59","60-69","70-79","80-89","90+"]
yrs["band"] = pd.cut(yrs["patient_onset_age"], bins=bins, labels=labels, right=False, include_lowest=True)
band_vc = yrs["band"].value_counts().reindex(labels)
for b, n in band_vc.items():
    print(f"{b}\t{n:,}\t{n/len(yrs)*100:.2f}%")

# --- ana_24: Age × sex ---
print("=== ana_24 ===")
yrs["sex_str"] = yrs["patient_sex"].map(sex_map).fillna("Unknown")
xt = pd.crosstab(yrs["band"], yrs["sex_str"])
# also unconditional
print(xt.to_string())

# --- ana_25: Country of occurrence (top 25) ---
print("=== ana_25 ===")
occ_vc = sample["occurcountry"].value_counts(dropna=False).head(25)
total_known = sample["occurcountry"].notna().sum()
for c, n in occ_vc.items():
    print(f"{c}\t{n:,}\t{n/N*100:.2f}%")
print(f"reports with known occurcountry: {total_known:,} ({total_known/N*100:.1f}%)")

# --- ana_26: Country of reporter (top 25) ---
print("=== ana_26 ===")
src_vc = sample["primarysourcecountry"].value_counts(dropna=False).head(25)
for c, n in src_vc.items():
    print(f"{c}\t{n:,}\t{n/N*100:.2f}%")

# --- ana_27: Reporter vs occurrence agreement ---
print("=== ana_27 ===")
both = sample.dropna(subset=["occurcountry", "primarysourcecountry"])
match = (both["occurcountry"] == both["primarysourcecountry"]).sum()
print(f"rows with both fields: {len(both):,}")
print(f"matching: {match:,} ({match/len(both)*100:.2f}%)")

# US-specific
us_rows = (sample["primarysourcecountry"] == "US").sum()
print(f"reports filed FROM US: {us_rows:,} ({us_rows/N*100:.2f}%)")
us_occ = (sample["occurcountry"] == "US").sum()
print(f"reports OCCURRING IN US: {us_occ:,} ({us_occ/N*100:.2f}%)")

# --- ana_28: Reporter type breakdown ---
print("=== ana_28 ===")
report_type_map = {1: "Spontaneous", 2: "Study", 3: "Other", 4: "Not available"}
rt_vc = sample["reporttype"].value_counts(dropna=False)
for code, n in rt_vc.items():
    lab = report_type_map.get(code, "MISSING")
    print(f"{lab}\t{n:,}\t{n/N*100:.2f}%")
