"""Assemble the canonical team table: merge group/confed (teams) + FIFA rank/points
(ratings) + squad value (values) into one teams.csv. Move the now-redundant source
CSVs into reference/ for provenance. Idempotent-ish (re-running after merge is a no-op
on already-moved files)."""
import sys, shutil
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import pandas as pd
from pathlib import Path

D = Path(r"D:\AI\journalist agent review\phase2\datasets\worldcup_2026")
ref = D / "reference"
ref.mkdir(exist_ok=True)

teams = pd.read_csv(D / "teams.csv", encoding="utf-8")
# already-merged guard
if "fifa_rank" in teams.columns and "squad_value_eur_m" in teams.columns:
    print("teams.csv already enriched; skipping merge.")
else:
    ratings = pd.read_csv(D / "team_ratings_prior.csv", encoding="utf-8")[["team", "fifa_rank", "fifa_points"]]
    values = pd.read_csv(D / "squad_values.csv", encoding="utf-8")[["team", "squad_value_eur_m"]]
    m = teams.merge(ratings, on="team", how="left").merge(values, on="team", how="left")
    assert len(m) == 48, f"expected 48 teams, got {len(m)}"
    assert m["fifa_rank"].notna().all(), f"missing fifa_rank: {m[m.fifa_rank.isna()].team.tolist()}"
    assert m["squad_value_eur_m"].notna().all(), f"missing value: {m[m.squad_value_eur_m.isna()].team.tolist()}"
    m["fifa_rank"] = m["fifa_rank"].astype(int)
    m.to_csv(D / "teams.csv", index=False, encoding="utf-8")
    print("merged teams.csv columns:", list(m.columns))
    print(m.sort_values("fifa_rank").head(8).to_string(index=False))

# relocate redundant source files (their data now lives in teams.csv; kept for provenance/source_name)
for f in ["team_ratings_prior.csv", "squad_values.csv"]:
    src = D / f
    if src.exists():
        shutil.move(str(src), str(ref / f))
        print("moved ->", ref / f)
    else:
        print("already moved:", f)
