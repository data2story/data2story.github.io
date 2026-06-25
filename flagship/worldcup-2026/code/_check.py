"""Pre-model consistency + leakage check. Read-only diagnostics."""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import pandas as pd
from pathlib import Path

D = Path(r"D:\AI\journalist agent review\phase2\datasets\worldcup_2026")
teams = pd.read_csv(D / "teams.csv", encoding="utf-8")
ratings = pd.read_csv(D / "team_ratings_prior.csv", encoding="utf-8")
values = pd.read_csv(D / "squad_values.csv", encoding="utf-8")
matches = pd.read_csv(D / "matches.csv", encoding="utf-8")

canon = set(teams["team"])
print("=== canonical teams:", len(canon))

print("\n=== cross-table name consistency (should all be empty) ===")
print("ratings - canon:", sorted(set(ratings["team"]) - canon))
print("canon - ratings:", sorted(canon - set(ratings["team"])))
print("values  - canon:", sorted(set(values["team"]) - canon))
print("canon - values :", sorted(canon - set(values["team"])))

grp = matches[matches["stage"] == "group"]
mteams = set(grp["home"]) | set(grp["away"])
print("group-match teams - canon:", sorted(mteams - canon))
print("canon - group-match teams:", sorted(canon - mteams))

print("\n=== played / scheduled ===")
print("played:", int((matches["status"] == "played").sum()),
      "scheduled:", int((matches["status"] == "scheduled").sum()))
print("group played:", int(((matches["stage"] == "group") & (matches["status"] == "played")).sum()),
      "of", int((matches["stage"] == "group").sum()))
pl = matches[matches["status"] == "played"]
print("played date range:", pl["date"].min(), "->", pl["date"].max())

print("\n=== martj42 history + leakage frontier ===")
hist = pd.read_csv(D / "intl_results_history.csv", encoding="utf-8")
print("hist rows:", len(hist), "cols:", list(hist.columns))
print("hist date range:", hist["date"].min(), "->", hist["date"].max())
hteams = set(hist["home_team"]) | set(hist["away_team"])
missing = sorted(canon - hteams)
print("canonical teams NOT found verbatim in martj42 (need name map):", missing)

wc = hist[hist["tournament"].astype(str).str.contains("World Cup", case=False, na=False)]
wc26 = wc[wc["date"] >= "2026-01-01"]
print("2026 WC-ish rows in martj42:", len(wc26),
      "date range:", (wc26["date"].min() if len(wc26) else None), "->",
      (wc26["date"].max() if len(wc26) else None))
print("2026 WC tournaments:", sorted(wc26["tournament"].astype(str).unique()))
print("rows dated >= 2026-06-19 (would leak):",
      int((hist["date"] >= "2026-06-19").sum()),
      "| of which WC:", int((wc26["date"] >= "2026-06-19").sum()))
print("\n2026 WC rows per date:")
print(wc26.groupby("date").size().to_string())
