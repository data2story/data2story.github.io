"""Pre-model consistency + leakage check. Read-only diagnostics.

Points at the blog root (where the model actually reads its data). The old separate
team_ratings_prior.csv / squad_values.csv inputs were consolidated into teams.csv, so
those cross-table checks are dropped; team strength/value now live as columns on teams.csv.
The load-bearing check here is the martj42 leakage frontier (no history row on/after the
forecast cutoff feeds the Elo).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import pandas as pd
from pathlib import Path

D = Path(__file__).resolve().parent.parent          # blog root (worldcup_2026)
teams = pd.read_csv(D / "teams.csv", encoding="utf-8")
matches = pd.read_csv(D / "matches.csv", encoding="utf-8")

canon = set(teams["team"])
print("=== canonical teams:", len(canon))

print("\n=== teams.csv columns (strength/value carried here now) ===")
print(list(teams.columns))

print("\n=== group-match name consistency (should be empty) ===")
grp = matches[matches["stage"] == "group"]
mteams = set(grp["home"]) | set(grp["away"])
print("group-match teams - canon:", sorted(mteams - canon))
print("canon - group-match teams:", sorted(canon - mteams))

# knockout rows that carry real team names (not 'Winner Match ..' placeholders)
ko = matches[matches["stage"] != "group"]
ko_named = set()
for t in set(ko["home"]) | set(ko["away"]):
    if isinstance(t, str) and not t.startswith(("Winner ", "Loser ", "Runner", "3rd ", "W", "L")):
        ko_named.add(t)
print("named-KO teams not in canon:", sorted(ko_named - canon))

print("\n=== played / scheduled ===")
print("played:", int((matches["status"] == "played").sum()),
      "scheduled:", int((matches["status"] == "scheduled").sum()))
print("group played:", int(((matches["stage"] == "group") & (matches["status"] == "played")).sum()),
      "of", int((matches["stage"] == "group").sum()))
r32 = matches[matches["stage"] == "R32"]
print("R32 played:", int((r32["status"] == "played").sum()), "of", len(r32))
if "winner" in matches.columns:
    kw = matches[(matches["stage"] != "group") & matches["winner"].notna()
                 & (matches["winner"].astype(str) != "")]
    bad = [(int(r.match_id), r.winner) for r in kw.itertuples()
           if r.winner not in (r.home, r.away)]
    print("KO winner column set on", len(kw), "rows; winner-not-in-row:", bad)
pl = matches[matches["status"] == "played"]
print("played date range:", pl["date"].min(), "->", pl["date"].max())

print("\n=== martj42 history + leakage frontier ===")
hist = pd.read_csv(D / "intl_results_history.csv", encoding="utf-8")
print("hist rows:", len(hist), "cols:", list(hist.columns))
print("hist date range:", hist["date"].min(), "->", hist["date"].max())
hteams = set(hist["home_team"]) | set(hist["away_team"])
# apply the same two aliases elo.py uses before flagging as missing
alias = {"USA": "United States", "Bosnia & Herzegovina": "Bosnia and Herzegovina"}
missing = sorted(t for t in canon if alias.get(t, t) not in hteams)
print("canonical teams NOT found in martj42 after alias (need name map):", missing)

CUTOFF = "2026-06-24"    # must equal elo.TODAY_CUTOFF; Elo trains strictly before this date
wc = hist[hist["tournament"].astype(str).str.contains("World Cup", case=False, na=False)]
wc26 = wc[wc["date"] >= "2026-01-01"]
# The model (elo.load_history) trains only on SCORED rows with date < cutoff: it drops
# rows with a null score, then applies the < cutoff filter. Future/unplayed fixtures that
# the frozen martj42 snapshot lists on/after the cutoff have null scores -> excluded twice.
scored = hist.dropna(subset=["home_score", "away_score"])
leak_scored = int((scored["date"] >= CUTOFF).sum())   # scored rows that WOULD feed Elo & leak
file_after = int((hist["date"] >= CUTOFF).sum())       # rows in the file on/after cutoff (may be unscored)
print(f"leakage cutoff (elo.TODAY_CUTOFF): {CUTOFF}")
print(f"file rows dated >= {CUTOFF}: {file_after} (of which WC: {int((wc26['date'] >= CUTOFF).sum())}) "
      f"-> these are UNSCORED future fixtures, dropped by the model")
print(f"SCORED rows dated >= {CUTOFF} that would actually feed Elo: {leak_scored}")
print("LEAKAGE-SAFE (model):", leak_scored == 0,
      "(0 => Elo trains only on scored matches before the cutoff)")
