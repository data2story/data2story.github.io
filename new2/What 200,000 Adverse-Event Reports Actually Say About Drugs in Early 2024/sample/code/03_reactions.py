"""03_reactions.py — reaction-side analysis: ranking, concentration, outcomes."""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR",
    r"D:\AI\journalist agent review\phase2\datasets\openfda_faers_2024",
)
reactions = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_reactions.csv"))
sample = pd.read_csv(os.path.join(DATA_DIR, "faers_2024_sample.csv"))

# --- ana_12: Top 30 MedDRA Preferred Terms ---
print("=== ana_12 ===")
top_pt = reactions["reactionmeddrapt"].value_counts().head(30)
total_react_rows = len(reactions)
for pt, n in top_pt.items():
    print(f"{pt}\t{n:,}\t{n/total_react_rows*100:.2f}%")
print(f"total reaction rows: {total_react_rows:,}")
print(f"unique PT terms: {reactions['reactionmeddrapt'].nunique():,}")

# --- ana_13: Concentration — top-N share of all reaction rows ---
print("=== ana_13 ===")
vc = reactions["reactionmeddrapt"].value_counts()
for N in [10, 25, 50, 100, 250, 500, 1000]:
    if len(vc) >= N:
        share = vc.head(N).sum() / total_react_rows * 100
        print(f"top {N} PTs cover {share:.2f}% of all reaction rows")

# --- ana_14: Reaction outcome distribution ---
print("=== ana_14 ===")
outcome_map = {1: "Recovered/resolved", 2: "Recovering/resolving",
               3: "Not recovered/not resolved", 4: "Recovered with sequelae",
               5: "Fatal", 6: "Unknown"}
out_vc = reactions["reactionoutcome"].value_counts(dropna=False)
for code, n in out_vc.items():
    label = outcome_map.get(code, "MISSING/other")
    print(f"{code}: {label}\t{n:,}\t{n/total_react_rows*100:.2f}%")

# --- ana_15: How often is "Drug ineffective" the entire complaint ---
print("=== ana_15 ===")
de = reactions[reactions["reactionmeddrapt"] == "Drug ineffective"]
de_reports = de["safetyreportid"].nunique()
total_reports = sample["safetyreportid"].nunique()
print(f"reports containing 'Drug ineffective': {de_reports:,} of {total_reports:,} ({de_reports/total_reports*100:.2f}%)")
# reports where Drug ineffective is the ONLY reaction
solo = (reactions.groupby("safetyreportid")
        .agg(only_drug_ineffective=("reactionmeddrapt",
                lambda x: (set(x) == {"Drug ineffective"}))))
solo_n = int(solo["only_drug_ineffective"].sum())
print(f"reports where 'Drug ineffective' is the ONLY reaction: {solo_n:,} ({solo_n/total_reports*100:.2f}%)")

# --- ana_16: Fatal-outcome reactions — which PTs are most often tagged Fatal (code 5) ---
print("=== ana_16 ===")
fatal = reactions[reactions["reactionoutcome"] == 5]
top_fatal = fatal["reactionmeddrapt"].value_counts().head(30)
total_fatal_rows = len(fatal)
print(f"total fatal-outcome reaction rows: {total_fatal_rows:,}")
for pt, n in top_fatal.items():
    print(f"{pt}\t{n:,}\t{n/total_fatal_rows*100:.2f}%")

# --- ana_17: Reactions per outcome category, normalized ---
print("=== ana_17 ===")
# For each top-30 PT: % of its rows that resolved vs fatal vs unknown
top_pts = top_pt.index[:20]
pt_outcome = (reactions[reactions["reactionmeddrapt"].isin(top_pts)]
              .groupby("reactionmeddrapt")["reactionoutcome"]
              .value_counts(normalize=False)
              .unstack(fill_value=0))
pt_total = pt_outcome.sum(axis=1)
pt_outcome_pct = pt_outcome.div(pt_total, axis=0) * 100
pt_outcome_pct["TOTAL"] = pt_total
print(pt_outcome_pct.round(1).sort_values("TOTAL", ascending=False).to_string())
