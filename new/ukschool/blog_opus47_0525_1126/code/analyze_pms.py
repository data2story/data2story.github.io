#!/usr/bin/env python3
"""Analysis of UK Prime Ministers: Oxford vs Cambridge.
Run from DATA_DIR (data/ukschool). All findings tagged ana_xx.
"""
import csv
from collections import Counter, defaultdict

PM = "uk_prime_ministers.csv"
COUNTS = "pm_count_by_university.csv"
COMP = "oxbridge_comparison.csv"


def load_pms():
    with open(PM, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify(row):
    ox = row["oxford"] == "True"
    cam = row["cambridge"] == "True"
    if ox and cam:
        return "Both"
    if ox:
        return "Oxford"
    if cam:
        return "Cambridge"
    # not oxbridge: distinguish other-uni vs none
    return row["classification"]  # "Other" or "Unknown"


def year(row):
    ts = row["term_start"]
    if not ts:
        return None
    return int(ts[:4])


pms = load_pms()

# --- ana_01: The headline split — Oxford vs Cambridge across PMs, Nobels, alumni ---
print("=== ana_01 ===")
comp = {}
with open(COMP, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        comp[r["university"]] = r
for uni in ("Oxford", "Cambridge"):
    r = comp[uni]
    print(f"{uni}: PMs={r['uk_prime_ministers']} Nobel={r['nobel_laureates']} alumni={r['total_alumni_on_wikidata']}")
ox_pm, cam_pm = int(comp["Oxford"]["uk_prime_ministers"]), int(comp["Cambridge"]["uk_prime_ministers"])
ox_nb, cam_nb = int(comp["Oxford"]["nobel_laureates"]), int(comp["Cambridge"]["nobel_laureates"])
print(f"PM ratio Oxford:Cambridge = {ox_pm/cam_pm:.2f}:1")
print(f"Nobel ratio Cambridge:Oxford = {cam_nb/ox_nb:.2f}:1")

# --- ana_02: Full PM university breakdown of all 59 holders ---
print("=== ana_02 ===")
cats = Counter()
for r in pms:
    c = classify(r)
    # normalize labels
    cats[c] += 1
# Build presentation categories matching the count CSV semantics
ox_total = sum(1 for r in pms if r["oxford"] == "True")
cam_total = sum(1 for r in pms if r["cambridge"] == "True")
both = sum(1 for r in pms if r["oxford"] == "True" and r["cambridge"] == "True")
ox_only = ox_total - both
cam_only = cam_total - both
other = sum(1 for r in pms if classify(r) == "Other")
unknown = sum(1 for r in pms if classify(r) == "Unknown")
total = len(pms)
print(f"Total PMs: {total}")
print(f"Oxford (total incl both): {ox_total}  | Oxford only: {ox_only}")
print(f"Cambridge (total incl both): {cam_total} | Cambridge only: {cam_only}")
print(f"Both: {both}")
print(f"Other university: {other}")
print(f"No university recorded: {unknown}")
print(f"Oxbridge share of all PMs: {(ox_total+cam_only)/total*100:.1f}%")

# --- ana_03: Chronological regime change — PMs by university over time (by decade of first term) ---
print("=== ana_03 ===")
# Use earliest term_start per PM (rows are first-term entries already)
era_rows = []
for r in pms:
    y = year(r)
    if y is None:
        continue
    cls = classify(r)
    grp = cls if cls in ("Oxford", "Cambridge", "Both") else ("Other" if cls == "Other" else "None")
    era_rows.append((y, grp, r["name"]))
era_rows.sort()
# Cambridge last PM, Oxford streak since 1937
cam_years = sorted(y for y, g, n in era_rows if g in ("Cambridge", "Both"))
ox_years = sorted(y for y, g, n in era_rows if g in ("Oxford", "Both"))
print(f"Last Cambridge-linked PM first term: {max(cam_years)}")
print(f"First Oxford PM first term: {min(ox_years)}  Last: {max(ox_years)}")
# Of English-university PMs since 1937, how many Oxford vs Cambridge vs other?
post37 = [(y, g, n) for y, g, n in era_rows if y >= 1937]
post37_eng = [(y, g, n) for y, g, n in post37 if g in ("Oxford", "Cambridge", "Both")]
print(f"Since 1937, PMs whose university is Oxford-linked: {sum(1 for y,g,n in post37_eng if g in ('Oxford','Both'))}")
print(f"Since 1937, PMs whose university is Cambridge-linked: {sum(1 for y,g,n in post37_eng if g=='Cambridge')}")
# decade buckets for chart
dec = defaultdict(lambda: Counter())
for y, g, n in era_rows:
    d = (y // 20) * 20  # 20-year buckets to keep chart readable
    dec[d][g] += 1
print("20yr-bucket, Oxford, Cambridge, Both, Other, None:")
for d in sorted(dec):
    c = dec[d]
    print(f"{d}s: Ox={c['Oxford']} Cam={c['Cambridge']} Both={c['Both']} Other={c['Other']} None={c['None']}")

# --- ana_04: Which Oxford/Cambridge colleges feed PMs (Christ Church dominance) ---
print("=== ana_04 ===")
OX_COLLEGES = {"Christ Church","Balliol College","Trinity College","Brasenose College","St John's College",
               "Merton College","Lincoln College","University College, Oxford","University College","Jesus College",
               "Hertford College","Somerville College","St Hugh's College","St Edmund Hall","Pembroke College"}
# Count college mentions only for Oxford/Cambridge PMs, mapping known Oxford colleges.
oxford_college_counts = Counter()
for r in pms:
    if r["oxford"] != "True":
        continue
    insts = [i.strip() for i in r["institutions"].split(";") if i.strip()]
    for i in insts:
        if i in OX_COLLEGES:
            oxford_college_counts[i] += 1
            break  # first matching Oxford college
# Christ Church specifically
cc = sum(1 for r in pms if "Christ Church" in r["institutions"])
print(f"PMs whose record includes 'Christ Church': {cc}")
print("Oxford college (first match) counts among Oxford PMs:")
for col, n in oxford_college_counts.most_common():
    print(f"  {col}: {n}")

# --- ana_05: Eton & secondary-school funnel ---
print("=== ana_05 ===")
eton = sum(1 for r in pms if "Eton College" in r["institutions"])
eton_cc = sum(1 for r in pms if "Eton College" in r["institutions"] and "Christ Church" in r["institutions"])
print(f"PMs educated at Eton College (in dataset): {eton}")
print(f"PMs educated at BOTH Eton and Christ Church (in dataset): {eton_cc}")

# --- ana_06: The non-graduates and 'Other university' PMs, named ---
print("=== ana_06 ===")
none_pms = [r["name"] for r in pms if classify(r) == "Unknown"]
other_pms = [r["name"] for r in pms if classify(r) == "Other"]
print(f"No university recorded ({len(none_pms)}): {none_pms}")
print(f"Other university ({len(other_pms)}): {other_pms}")

# --- ana_07: Notability-normalised rate — PMs per 1,000 recorded alumni ---
print("=== ana_07 ===")
ox_alum = int(comp["Oxford"]["total_alumni_on_wikidata"])
cam_alum = int(comp["Cambridge"]["total_alumni_on_wikidata"])
ox_pm_rate = ox_pm / ox_alum * 1000
cam_pm_rate = cam_pm / cam_alum * 1000
ox_nb_rate = ox_nb / ox_alum * 1000
cam_nb_rate = cam_nb / cam_alum * 1000
print(f"Oxford total recorded alumni: {ox_alum}; Cambridge: {cam_alum}")
print(f"Oxford PMs per 1,000 recorded alumni: {ox_pm_rate:.3f}")
print(f"Cambridge PMs per 1,000 recorded alumni: {cam_pm_rate:.3f}")
print(f"Oxford Nobels per 1,000 recorded alumni: {ox_nb_rate:.3f}")
print(f"Cambridge Nobels per 1,000 recorded alumni: {cam_nb_rate:.3f}")
print(f"Oxford PM-rate advantage over Cambridge: {ox_pm_rate/cam_pm_rate:.2f}x")
print(f"Cambridge Nobel-rate advantage over Oxford: {cam_nb_rate/ox_nb_rate:.2f}x")

# --- ana_08: Portrait coverage — how many PMs have a real Wikimedia portrait ---
print("=== ana_08 ===")
import json, os
mani_path = "wikimedia_assets/wikimedia_manifest.json"
have = 0
if os.path.exists(mani_path):
    mani = json.load(open(mani_path))
    photo_qids = {e["qid"] for e in mani if e.get("kind") == "photo" and e.get("status") == "ok"}
    for r in pms:
        if r["wikidata_id"] in photo_qids:
            have += 1
print(f"PMs with a real Wikimedia portrait in the cache: {have} of {len(pms)}")
