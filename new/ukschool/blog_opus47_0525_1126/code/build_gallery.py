#!/usr/bin/env python3
"""Build the per-PM gallery table (name, term_start, university group, college, portrait file)
by joining uk_prime_ministers.csv to the Wikimedia manifest on QID.
Run from DATA_DIR. Produces ana_09 (gallery) and ana_10 (university crest/campus asset map).
"""
import csv, json, os

pms = list(csv.DictReader(open("uk_prime_ministers.csv", newline="", encoding="utf-8")))
mani = json.load(open("wikimedia_assets/wikimedia_manifest.json"))
by_qid_photo = {e["qid"]: e for e in mani if e.get("kind") == "photo"}

OX_COLLEGES = ["Christ Church","Balliol College","Trinity College","Brasenose College","St John's College",
               "Merton College","Lincoln College","University College, Oxford","Jesus College",
               "Hertford College","Somerville College","St Hugh's College","St Edmund Hall","Pembroke College"]
CAM_COLLEGES = ["Trinity College","King's College","St John's College","Pembroke College","Peterhouse",
                "Clare College"]

def group(r):
    ox = r["oxford"] == "True"; cam = r["cambridge"] == "True"
    if ox and cam: return "Both"
    if ox: return "Oxford"
    if cam: return "Cambridge"
    return "Other" if r["classification"] == "Other" else "None"

def first_college(r, group_name):
    insts = [i.strip() for i in r["institutions"].split(";") if i.strip()]
    pool = OX_COLLEGES if group_name in ("Oxford","Both") else (CAM_COLLEGES if group_name=="Cambridge" else [])
    for c in insts:
        if c in pool:
            return c
    return ""

# --- ana_09: Per-PM gallery table ---
print("=== ana_09 ===")
rows = []
for r in pms:
    g = group(r)
    col = first_college(r, g)
    ent = by_qid_photo.get(r["wikidata_id"])
    fname = os.path.basename(ent["local_path"]) if ent else ""
    artist = (ent.get("artist") or "") if ent else ""
    lic = (ent.get("license") or "") if ent else ""
    ystr = r["term_start"][:4] if r["term_start"] else ""
    rows.append([r["name"], ystr, g, col, fname, artist, lic])
# sort by term start year (empty last)
rows.sort(key=lambda x: (x[1] == "", x[1]))
print(f"Gallery rows: {len(rows)}")
for row in rows[:5]:
    print(row)
print("...")
for row in rows[-3:]:
    print(row)
# group tallies for filter chips
from collections import Counter
gc = Counter(row[2] for row in rows)
print("Group tallies:", dict(gc))

# --- ana_10: University head-to-head asset map (crest, logo, campus) ---
print("=== ana_10 ===")
asset_map = {}
for e in mani:
    if e["qid"] in ("Q34433", "Q35794"):
        asset_map.setdefault(e["qid"], {})[e["kind"]] = {
            "file": os.path.basename(e["local_path"]),
            "license": e.get("license"),
            "artist": e.get("artist") or "",
            "credit": e.get("credit") or "",
            "source_url": e.get("descriptionurl") or e.get("source_url"),
        }
print(json.dumps(asset_map, indent=1))

# dump gallery to a json the designer/programmer pathway can reference if needed
json.dump(rows, open("/tmp/_gallery_rows.json","w"))
