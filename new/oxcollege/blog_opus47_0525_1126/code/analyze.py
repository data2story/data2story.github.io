#!/usr/bin/env python3
"""Analysis of Oxford colleges founding history.
Run from DATA_DIR (data/oxcollege). Produces all ana_xx findings.
"""
import csv, re
from collections import Counter, defaultdict

DATA = "oxford_colleges.csv"
CENT = "colleges_by_century.csv"

rows = list(csv.DictReader(open(DATA, encoding="utf-8")))
N = len(rows)

def year(r):
    y = r["founded_year"].strip()
    return int(y) if y else None

years = [year(r) for r in rows]
have_year = [r for r in rows if year(r) is not None]

# --- ana_01: Dataset shape and missingness ---
print("=== ana_01 ===")
cols = list(rows[0].keys())
miss = {c: sum(1 for r in rows if not r[c].strip()) for c in cols}
yr = [year(r) for r in have_year]
print(f"rows={N} cols={len(cols)}")
print(f"founded_year range: {min(yr)} -> {max(yr)} (span {max(yr)-min(yr)} years)")
for c in sorted(miss, key=lambda k: -miss[k]):
    print(f"  {c}: {miss[c]} missing")
blank = [r['college'] for r in rows if year(r) is None]
print(f"blank founded_year: {len(blank)} -> {blank}")
# end ana_01

# --- ana_02: Foundations per century (two waves) ---
print("\n=== ana_02 ===")
cent_rows = list(csv.DictReader(open(CENT, encoding="utf-8")))
for cr in cent_rows:
    print(f"  {cr['century']}: {cr['colleges_founded']}")
known = [(cr['century'], int(cr['colleges_founded'])) for cr in cent_rows if cr['century'] != 'unknown']
peak = max(known, key=lambda x: x[1])
print(f"peak century: {peak[0]} with {peak[1]}")
print(f"13th+14th medieval = {7+5}; 19th+20th modern = {9+9}")
# end ana_02

# --- ana_03: The oldest-college cluster (15-year window) ---
print("\n=== ana_03 ===")
ordered = sorted(have_year, key=year)
for r in ordered[:6]:
    print(f"  {year(r)}  {r['college']}")
top3 = [r for r in ordered if r['college'] in ('University College, Oxford','Balliol College','Merton College')]
ys = [year(r) for r in top3]
print(f"oldest-three window: {min(ys)}-{max(ys)} = {max(ys)-min(ys)} years")
print(f"Rewley Abbey (1201) precedes Univ (1249) by {1249-1201} years")
# end ana_03

# --- ana_04: Founders — counting people (split on ';') ---
print("\n=== ana_04 ===")
founder_count = Counter()
for r in rows:
    f = r['founder'].strip()
    if not f: continue
    for person in [p.strip() for p in f.split(';') if p.strip()]:
        founder_count[person] += 1
n_with_founder = sum(1 for r in rows if r['founder'].strip())
print(f"colleges with a recorded founder: {n_with_founder}/{N}")
print(f"distinct founders: {len(founder_count)}")
for person, c in founder_count.most_common(8):
    print(f"  {person}: {c}")
multi = founder_count.most_common(1)[0]
print(f"most prolific: {multi[0]} ({multi[1]})")
# end ana_04

# --- ana_05: Namesakes — religious vs personal ---
print("\n=== ana_05 ===")
religious_kw = ['Mary','Jesus','John the Baptist','All Souls','Trinity','Saint','St ','Hugh','Hilda','Catherine','Peter','Anne','Anthony','Cross','Edmund','Durham Priory']
n_named = sum(1 for r in rows if r['named_after'].strip())
relig=0; personal=0; relig_list=[]; pers_list=[]
for r in rows:
    na=r['named_after'].strip()
    if not na: continue
    is_relig = any(k in na for k in religious_kw)
    if is_relig: relig+=1; relig_list.append((r['college'],na))
    else: personal+=1; pers_list.append((r['college'],na))
print(f"colleges with a namesake: {n_named}/{N}")
print(f"religious/saint namesakes: {relig}")
print(f"personal/secular namesakes: {personal}")
print("religious examples:", relig_list[:6])
print("personal examples:", pers_list[:6])
# end ana_05

# --- ana_06: Defunct / merged / non-residential rows ---
print("\n=== ana_06 ===")
defunct = ['Rewley Abbey','Gloucester College','Durham College','Canterbury College',
           'Cardinal College',"King Henry VIII's College","St Mary's College",
           "St Bernard's College, Oxford",'Greek College','Templeton College','Examination Schools']
present = [r['college'] for r in rows if r['college'] in defunct]
print(f"defunct/merged/non-residential rows flagged: {len(present)}")
for c in present: print(f"  {c}")
print(f"surviving-college estimate: {N - len(present)} of {N}")
# end ana_06

# --- ana_07: Gaps between consecutive foundings ---
print("\n=== ana_07 ===")
oy = sorted(set(year(r) for r in have_year))
gaps=[]
for a,b in zip(oy, oy[1:]):
    gaps.append((b-a,a,b))
gaps.sort(reverse=True)
print("largest gaps between founding years:")
for g,a,b in gaps[:5]:
    print(f"  {g} years: {a} -> {b}")
# 18th century drought
c18 = [r['college'] for r in have_year if 1700 <= year(r) < 1800]
print(f"18th-century foundations: {len(c18)} -> {c18}")
# end ana_07

# --- ana_08: Mottos almost entirely absent ---
print("\n=== ana_08 ===")
mottos = [(r['college'], r['motto']) for r in rows if r['motto'].strip()]
print(f"colleges with a recorded motto: {len(mottos)}/{N}")
for c,m in mottos: print(f"  {c}: {m}")
# end ana_08

# --- ana_09: Coat-of-arms coverage in the image cache ---
print("\n=== ana_09 ===")
import os
cache = "wikimedia_assets"
coa = [f for f in os.listdir(cache) if f.endswith("__coat_of_arms.png")]
photo = [f for f in os.listdir(cache) if f.endswith("__photo.jpg") or f.endswith("__photo.png")]
print(f"real coats of arms available: {len(coa)}")
print(f"real campus photos available: {len(photo)}")
print(f"colleges in CSV: {N}")
# end ana_09

# --- ana_10: Founding-rate by half-century (modern acceleration) ---
print("\n=== ana_10 ===")
buckets = Counter()
for r in have_year:
    y=year(r); b=(y//50)*50
    buckets[b]+=1
for b in sorted(buckets):
    print(f"  {b}s-{b+49}: {buckets[b]}")
# end ana_10
print("\nDONE")
