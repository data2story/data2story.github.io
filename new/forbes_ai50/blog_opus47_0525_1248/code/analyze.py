#!/usr/bin/env python3
"""Forbes AI 50 analysis. Reads 'forbes ai50.xlsx' and prints findings per ana_xx.
Run from DATA_DIR (or anywhere; DATA path is resolved relative to this file by default).
"""
import sys, os, re
from collections import Counter, defaultdict
import openpyxl

# Resolve data path: arg 1, else default location
DEFAULT = "/Users/forrest/Desktop/data2story-skill/data/forbes_ai50/forbes ai50.xlsx"
PATH = sys.argv[1] if len(sys.argv) > 1 else DEFAULT

wb = openpyxl.load_workbook(PATH)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
header = rows[0]
data = [r for r in rows[1:] if r and r[0] is not None]

# ---------- helpers ----------
def parse_funding(s):
    """'$830 M' -> 830 ; '$60 B' -> 60000 ; '$182.6 B' -> 182600 ; '$0 M' -> 0. Unit = millions."""
    if s is None:
        return None
    t = str(s).replace("$", "").strip()
    m = re.match(r"([\d.]+)\s*([MB])", t, re.I)
    if not m:
        return None
    val = float(m.group(1)); unit = m.group(2).upper()
    return val * 1000.0 if unit == "B" else val

records = []
for name, what, funding, year, hq in data:
    records.append({
        "name": name,
        "what": (what or "").strip(),
        "funding_raw": funding,
        "funding_m": parse_funding(funding),
        "year": int(year) if year is not None else None,
        "hq": (hq or "").strip(),
    })

N = len(records)

# ---------- ana_01: dataset shape + funding normalization ----------
print("=== ana_01 ===")
print(f"rows={N} cols={len(header)} columns={list(header)}")
yrs = [r["year"] for r in records if r["year"]]
print(f"year range: {min(yrs)} -> {max(yrs)} (span {max(yrs)-min(yrs)} years)")
funds = [r["funding_m"] for r in records if r["funding_m"] is not None]
print(f"funding parsed for {len(funds)}/{N}; unit=millions USD")
print("sample normalization: $60 B -> 60000 ; $182.6 B -> 182600 ; $830 M -> 830 ; $0 M -> 0")
zeros = [r["name"] for r in records if r["funding_m"] == 0]
print(f"zero-funding rows (bootstrapped/undisclosed): {zeros}")
# line 60

# ---------- ana_02: funding leaderboard + power-law skew ----------
print("\n=== ana_02 ===")
ranked = sorted(records, key=lambda r: (r["funding_m"] if r["funding_m"] is not None else -1), reverse=True)
total = sum(funds)
print(f"total cohort funding = {total:,.1f} M  (= ${total/1000:,.2f} B)")
import statistics as st
print(f"mean = {st.mean(funds):,.1f} M ; median = {st.median(funds):,.1f} M")
top2 = ranked[:2]
top2_sum = sum(r["funding_m"] for r in top2)
print(f"top 2 = {[r['name'] for r in top2]} = {top2_sum:,.1f} M = {100*top2_sum/total:.1f}% of total")
top5_sum = sum(r["funding_m"] for r in ranked[:5])
print(f"top 5 share = {100*top5_sum/total:.1f}%")
print("Full leaderboard (name, $M):")
for r in ranked:
    print(f"  {r['name']:<24} {r['funding_m']:>9,.0f}")
# line 80

# ---------- ana_03: median vs mean gap / the long tail ----------
print("\n=== ana_03 ===")
below_median = [r for r in funds if r < st.median(funds)]
print(f"median funding = {st.median(funds):,.0f} M ; mean = {st.mean(funds):,.0f} M ; mean/median = {st.mean(funds)/st.median(funds):.1f}x")
# how many companies below $1B
under_1b = [r for r in records if r["funding_m"] is not None and r["funding_m"] < 1000]
print(f"companies under $1B: {len(under_1b)}/{N} = {100*len(under_1b)/N:.0f}%")
over_1b = [r for r in records if r["funding_m"] is not None and r["funding_m"] >= 1000]
print(f"companies at/over $1B: {len(over_1b)}")
print(f"OpenAI+Anthropic = {sum(r['funding_m'] for r in records if r['name'] in ('OpenAI','Anthropic')):,.0f} M = {100*sum(r['funding_m'] for r in records if r['name'] in ('OpenAI','Anthropic'))/total:.1f}% of total")
# line 95

# ---------- ana_04: geography ----------
print("\n=== ana_04 ===")
def geo_bucket(hq):
    h = hq.lower()
    if "united states" in h or "united states" in h or h.endswith("united states"):
        country = "United States"
    else:
        # last token after comma is the country
        country = hq.split(",")[-1].strip()
    return country
countries = Counter(geo_bucket(r["hq"]) for r in records)
print("By country:")
for c, n in countries.most_common():
    print(f"  {c:<20} {n}")
us = [r for r in records if "United States" in r["hq"]]
intl = [r for r in records if "United States" not in r["hq"]]
print(f"US = {len(us)} ; International = {len(intl)}")
# California vs rest of US
def city_state(hq):
    parts = [p.strip() for p in hq.split(",")]
    return parts
sf = [r for r in records if r["hq"].split(",")[0].strip() == "San Francisco"]
ca = [r for r in records if ", California," in r["hq"] or r["hq"].endswith("California, United States") or "California" in r["hq"]]
print(f"San Francisco (city) = {len(sf)} ; California (state) = {len(ca)} ; rest of US = {len(us)-len(ca)} ; intl = {len(intl)}")
print("California cities:", Counter(r['hq'].split(',')[0].strip() for r in ca))
# line 118

# ---------- ana_05: geo 4-bucket for chart ----------
print("\n=== ana_05 ===")
def bucket4(r):
    hq = r["hq"]
    if "United States" not in hq:
        return "International"
    city = hq.split(",")[0].strip()
    if "California" in hq:
        if city == "San Francisco":
            return "San Francisco"
        return "Rest of Bay Area / CA"
    return "Rest of US"
b4 = Counter(bucket4(r) for r in records)
order = ["San Francisco", "Rest of Bay Area / CA", "Rest of US", "International"]
for k in order:
    print(f"  {k:<24} {b4[k]}  ({100*b4[k]/N:.0f}%)")
# intl detail
print("International cities:")
for r in records:
    if "United States" not in r["hq"]:
        print(f"   {r['name']:<18} {r['hq']}")
# line 138

# ---------- ana_06: founding year distribution + surge ----------
print("\n=== ana_06 ===")
yc = Counter(r["year"] for r in records if r["year"])
for y in sorted(yc):
    print(f"  {y}: {yc[y]}")
post2020 = [r for r in records if r["year"] and r["year"] >= 2020]
post2022 = [r for r in records if r["year"] and r["year"] >= 2022]
print(f"founded 2020 or later: {len(post2020)}/{N} = {100*len(post2020)/N:.0f}%")
print(f"founded 2022 or later: {len(post2022)}/{N} = {100*len(post2022)/N:.0f}%")
print(f"oldest: {min((r['year'],r['name']) for r in records if r['year'])}")
print(f"newest: {max((r['year'],r['name']) for r in records if r['year'])}")
peak_year = yc.most_common(1)[0]
print(f"peak founding year: {peak_year[0]} with {peak_year[1]} companies")
# line 152

# ---------- ana_07: category taxonomy of 'What It Does' ----------
print("\n=== ana_07 ===")
CAT = {
    "Foundation models": ["Anthropic","OpenAI","Cohere","Mistral AI","Reflection","Safe Superintelligence","Thinking Machines Lab"],
    "Coding & app builders": ["Cognition","Cursor","Replit","Lovable","Gamma"],
    "Generative media": ["Black Forest Labs","ElevenLabs","HeyGen","Krea","Midjourney","Runway","Suno","Synthesia"],
    "Agents (CS / GTM / knowledge)": ["Clay","Decagon","Genspark.ai","Glean","Sierra","EliseAI"],
    "Healthcare": ["Abridge","Chai Discovery","OpenEvidence"],
    "Legal & finance": ["Harvey","Legora","Rogo"],
    "Robotics & autonomy": ["Applied Intuition","Physical Intelligence","Skild AI","World Labs"],
    "AI infrastructure & chips": ["Baseten","Crusoe","Fal","Fireworks AI","SambaNova","Together AI","Databricks"],
    "Search": ["Perplexity"],
    "Data labeling / research data": ["Mercor","Surge AI","Listen Labs"],
    "Productivity": ["Notion"],
    "Security": ["Cyera"],
    "Education / voice tutor": ["Speak"],
}
# verify every company assigned exactly once
assigned = {}
for cat, names in CAT.items():
    for nm in names:
        assigned[nm] = cat
missing = [r["name"] for r in records if r["name"] not in assigned]
print("unassigned:", missing)
catcount = Counter(assigned[r["name"]] for r in records if r["name"] in assigned)
for c, n in catcount.most_common():
    print(f"  {c:<32} {n}")
print(f"total categorized: {sum(catcount.values())}/{N}")
# funding by category
catfund = defaultdict(float)
for r in records:
    if r["name"] in assigned and r["funding_m"] is not None:
        catfund[assigned[r["name"]]] += r["funding_m"]
print("funding by category ($M):")
for c, f in sorted(catfund.items(), key=lambda x:-x[1]):
    print(f"  {c:<32} {f:>10,.0f}")
# line 188

# ---------- ana_08: application layer vs foundation models funding ----------
print("\n=== ana_08 ===")
fm = catfund["Foundation models"]
app = total - fm
print(f"Foundation-model funding = {fm:,.0f} M = {100*fm/total:.1f}% of total")
print(f"Everything else (application+infra) = {app:,.0f} M = {100*app/total:.1f}%")
fm_co = catcount["Foundation models"]
print(f"Foundation-model companies = {fm_co} of {N} ({100*fm_co/N:.0f}% of companies) hold {100*fm/total:.1f}% of capital")
# line 196

# ---------- ana_09: most common 'what it does' phrasings / verticalization ----------
print("\n=== ana_09 ===")
# count companies that are clearly 'agents' or 'agent' mentions, 'generation', etc.
def has(r, *kw):
    w = r["what"].lower()
    return any(k in w for k in kw)
agentic = [r["name"] for r in records if has(r,"agent")]
generation = [r["name"] for r in records if has(r,"generation","generator","generative")]
coding = [r["name"] for r in records if has(r,"coding","app and website","app development","app deployment")]
print(f"mention 'agent(s)': {len(agentic)} -> {agentic}")
print(f"mention generation/generative: {len(generation)} -> {generation}")
print(f"coding/app building/deploy: {len(coding)} -> {coding}")
# line 207

# ---------- ana_10: funding vs founding year (do older companies have more?) ----------
print("\n=== ana_10 ===")
pairs = [(r["year"], r["funding_m"], r["name"]) for r in records if r["year"] and r["funding_m"] is not None]
# correlation
import math
xs = [p[0] for p in pairs]; ys = [p[1] for p in pairs]
mx, my = st.mean(xs), st.mean(ys)
cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))/len(xs)
sx = st.pstdev(xs); sy = st.pstdev(ys)
corr = cov/(sx*sy) if sx and sy else 0
print(f"Pearson corr(year, funding) = {corr:.3f} (n={len(pairs)})")
# median funding by founding-era bucket
def era(y):
    if y <= 2018: return "2013-2018"
    if y <= 2021: return "2019-2021"
    return "2022-2025"
eras = defaultdict(list)
for y,f,nm in pairs:
    eras[era(y)].append(f)
for e in ["2013-2018","2019-2021","2022-2025"]:
    v = eras[e]
    print(f"  {e}: n={len(v)} median=${st.median(v):,.0f}M mean=${st.mean(v):,.0f}M")
# line 226

# ---------- ana_11: logo coverage (verified real vs wordmark) ----------
print("\n=== ana_11 ===")
verified = ["Anthropic","Applied Intuition","Cohere","Cursor","Databricks","ElevenLabs","Glean","HeyGen","Lovable","Mistral AI","Notion","OpenAI","OpenEvidence","Perplexity","Physical Intelligence","Replit","Runway","Suno"]
dropped = ["Clay","Cognition","Crusoe","Fal","Gamma","Harvey","Midjourney","Reflection","Sierra","Speak","Synthesia","World Labs"]
print(f"verified real logos = {len(verified)}; dropped mismatches = {len(dropped)}")
print(f"wordmark fallback (dropped + not-found) = {N - len(verified)} of {N}")
print("verified:", verified)
print("dropped:", dropped)
# line 235
