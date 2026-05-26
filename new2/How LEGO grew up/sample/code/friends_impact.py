"""LEGO Friends and the pastel/pink palette shift.

Findings produced:
  ana_11: Friends-vs-rest pink/pastel color quantity per year
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
colors = pd.read_csv(os.path.join(DATA, "colors.csv"))
inv = pd.read_csv(os.path.join(DATA, "inventories.csv"))
ip = pd.read_csv(os.path.join(DATA, "inventory_parts.csv"))


def root_of(tid, theme_map):
    seen = set()
    cur = tid
    while pd.notna(cur) and int(cur) in theme_map:
        if int(cur) in seen:
            return int(cur)
        seen.add(int(cur))
        parent = theme_map[int(cur)]["parent_id"]
        if pd.isna(parent):
            return int(cur)
        cur = parent
    return tid


themes_local = themes.rename(columns={"name": "theme_label"})
theme_map = {int(r.id): {"name": r.theme_label, "parent_id": r.parent_id}
             for r in themes_local.itertuples(index=False)}
sets["root_theme_id"] = sets["theme_id"].apply(lambda x: root_of(x, theme_map))
sets["root_theme_name"] = sets["root_theme_id"].map({i: t["name"] for i, t in theme_map.items()})

# Get latest inventory per set with year + theme
latest_inv = inv.sort_values("version").groupby("set_num").tail(1)[["id", "set_num"]]
latest_inv = latest_inv.rename(columns={"id": "inventory_id"})
latest_inv = latest_inv.merge(sets[["set_num", "year", "root_theme_name"]], on="set_num", how="left")

ipy = ip.merge(latest_inv, on="inventory_id", how="inner")
ipy = ipy[(ipy["color_id"] != -1) & (ipy["year"] <= 2024)]

# Identify pink / pastel / lavender colors
pink_kw = ["Pink", "Lavender", "Magenta", "Violet"]
pink_ids = colors[colors["name"].str.contains("|".join(pink_kw), case=False, na=False)]["id"].tolist()
print(f"Pink/lavender/magenta/violet color IDs: {len(pink_ids)}")
print(colors[colors["id"].isin(pink_ids)][["id", "name", "rgb"]].to_string(index=False))

# --- ana_11: Pink palette in Friends vs other themes per year ---
print("=== ana_11 ===")
ipy["is_pink"] = ipy["color_id"].isin(pink_ids)
ipy["is_friends"] = ipy["root_theme_name"] == "Friends"
agg = ipy[ipy["is_pink"]].groupby(["year", "is_friends"])["quantity"].sum().unstack().fillna(0).astype(int)
agg.columns = ["other_themes_pink_qty", "friends_pink_qty"]
agg = agg[agg.index.notna()]
agg = agg[(agg.index >= 2000)]
print(agg.to_string())
print()

# Pink quantity ALL themes (vs total quantity per year) — share of pink overall
total_y = ipy.groupby("year")["quantity"].sum()
pink_y = ipy[ipy["is_pink"]].groupby("year")["quantity"].sum()
share = (pink_y / total_y * 100).rename("pink_share_pct")
print("Overall pink share of all parts placed, per year (2005-2024):")
print(share[(share.index >= 2005)].to_string())

# Friends specifically: how many sets, how many parts, in what years
print("\nFriends set count by year:")
fr = sets[sets["root_theme_name"] == "Friends"]
print(fr.groupby("year").size().to_string())
print(f"\nFriends total sets: {len(fr)}")
print(f"Friends years: {sorted(fr['year'].dropna().unique().tolist())}")
