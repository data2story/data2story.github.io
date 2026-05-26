"""Theme arc — dominance by decade, Star Wars + Bionicle lifecycles, supertheme rollup.

Findings produced:
  ana_07: Top themes by all-time set count (rollup to root theme)
  ana_08: Theme dominance by decade — top 5 super-themes per decade
  ana_09: Star Wars share of new sets per year
  ana_10: Bionicle lifecycle — sets per year
"""
from __future__ import annotations
import os
import sys
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA = os.environ.get("DATA", r"D:\AI\journalist agent review\phase2\datasets\2016-06-01_lego-database")
sets = pd.read_csv(os.path.join(DATA, "sets.csv"))
themes = pd.read_csv(os.path.join(DATA, "themes.csv"))


def root_of(tid, theme_map):
    seen = set()
    cur = tid
    while pd.notna(cur) and int(cur) in theme_map:
        if int(cur) in seen:
            return int(cur)  # cycle guard
        seen.add(int(cur))
        parent = theme_map[int(cur)]["parent_id"]
        if pd.isna(parent):
            return int(cur)
        cur = parent
    return tid


# itertuples reserves `.name` for the row label, so rename the theme name column first.
themes_local = themes.rename(columns={"name": "theme_label"})
theme_map = {int(r.id): {"name": r.theme_label, "parent_id": r.parent_id}
             for r in themes_local.itertuples(index=False)}
sets["root_theme_id"] = sets["theme_id"].apply(lambda x: root_of(x, theme_map))
sets["root_theme_name"] = sets["root_theme_id"].map({i: t["name"] for i, t in theme_map.items()})
sets["theme_name"] = sets["theme_id"].map({i: t["name"] for i, t in theme_map.items()})
sets = sets[sets["year"] <= 2024]

# --- ana_07: All-time set count per super-theme (top 25) ---
print("=== ana_07 ===")
sup = sets.groupby("root_theme_name").size().rename("n_sets").sort_values(ascending=False)
print(sup.head(25).to_string())
print(f"\nTotal unique root themes: {sets['root_theme_id'].nunique()}")
print(f"Total unique sub-themes: {sets['theme_id'].nunique()}")

# --- ana_08: Decade dominance — top super-themes per decade ---
print("=== ana_08 ===")
sets["decade"] = (sets["year"] // 10) * 10
by_decade = sets.groupby(["decade", "root_theme_name"]).size().rename("n").reset_index()
for d in sorted(by_decade["decade"].unique()):
    top = by_decade[by_decade["decade"] == d].nlargest(5, "n")
    print(f"\n{int(d)}s:")
    print(top.to_string(index=False))

# --- ana_09: Star Wars share by year ---
print("=== ana_09 ===")
sw = sets[sets["root_theme_name"].str.contains("Star Wars", na=False)]
yearly_all = sets.groupby("year").size().rename("n_all")
yearly_sw = sw.groupby("year").size().rename("n_sw")
yearly = pd.concat([yearly_all, yearly_sw], axis=1).fillna(0)
yearly["sw_share"] = yearly["n_sw"] / yearly["n_all"] * 100
print(yearly[yearly.index >= 1995].to_string())

# --- ana_10: Bionicle lifecycle ---
print("=== ana_10 ===")
bn_names = ["Bionicle"]
bn = sets[sets["root_theme_name"].isin(bn_names)]
print(bn.groupby("year").size().to_string())
print(f"\nTotal Bionicle sets: {len(bn)}")
print(f"Years active: {sorted(bn['year'].unique().tolist())}")

# --- Save a tidy yearly-share frame for the data_table downstream ---
print("=== theme_yearly_top12 ===")
top12 = sup.head(12).index.tolist()
print("top 12 super-themes:", top12)
yearly_by_theme = sets[sets["root_theme_name"].isin(top12)].groupby(
    ["year", "root_theme_name"]).size().rename("n").reset_index()
print(yearly_by_theme.tail(40).to_string(index=False))
