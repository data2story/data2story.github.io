#!/usr/bin/env python3
"""
Data2Story Analyst — FIFA 2026 World Cup schedule x venue climate.
Loads the schedule CSVs and joins venue_weather.csv on `stadium`.
Run from anywhere; uses paths relative to this file's repo root.
"""
import csv, os, math
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DATA = os.path.join(ROOT, "data", "fifa26_schedule")

def load_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

sched = load_csv(os.path.join(DATA, "FIFA2026_schedule.csv"))
fix   = load_csv(os.path.join(DATA, "FIFA2026_schedule_Fixtures.csv"))
wx    = load_csv(os.path.join(DATA, "venue_weather.csv"))

# weather lookup by stadium
W = {r["stadium"]: r for r in wx}
def fnum(r, k): return float(r[k])

# ---------- ana_01: dataset profile ----------
print("=== ana_01 ===")
print(f"schedule rows={len(sched)} fixtures rows={len(fix)} weather rows={len(wx)}")
print(f"unique stadiums in schedule={len(set(r['stadium'] for r in sched))}")
print(f"unique stadiums in weather={len(set(r['stadium'] for r in wx))}")
dates = sorted(set(r["date_dt"] for r in sched))
print(f"date range {dates[0]} -> {dates[-1]} across {len(dates)} match days")
# join completeness
missing = set(r["stadium"] for r in sched) - set(W)
print(f"stadiums in schedule with NO weather match: {missing or 'none'}")

# ---------- ana_02: matches per venue ----------
print("=== ana_02 ===")
cnt = Counter(r["stadium"] for r in sched)
rows_v = []
for st, c in cnt.most_common():
    w = W[st]
    rows_v.append([st, w["city"], w["country"], c])
    print(f"{c:>2}  {st:<32} {w['city']}")
print(f"total matches = {sum(cnt.values())}")

# ---------- ana_03: matches per host nation ----------
print("=== ana_03 ===")
nat = Counter()
for r in sched:
    nat[W[r["stadium"]]["country"]] += 1
for k, v in nat.most_common():
    print(f"{k}: {v} matches across {len(set(W[s]['stadium'] for s in cnt if W[s]['country']==k))} venues")
nat_rows = [[k, v] for k, v in nat.most_common()]

# ---------- ana_04: feels-like (apparent high) ranking ----------
print("=== ana_04 ===")
heat = sorted(wx, key=lambda r: fnum(r, "avg_apparent_high_c"), reverse=True)
heat_rows = []
for r in heat:
    heat_rows.append([r["city"], r["venue"], round(fnum(r,"avg_apparent_high_c"),1),
                      round(fnum(r,"avg_high_c"),1), int(fnum(r,"avg_humidity_pct")), cnt[r["stadium"]]])
    print(f"{fnum(r,'avg_apparent_high_c'):>5.1f}C feels  ({fnum(r,'avg_high_c'):>4.1f}C air)  hum {fnum(r,'avg_humidity_pct'):>4.1f}%  {r['city']} / {r['venue']}")
spread = fnum(heat[0],"avg_apparent_high_c") - fnum(heat[-1],"avg_apparent_high_c")
print(f"feels-like spread: {fnum(heat[0],'avg_apparent_high_c')}C ({heat[0]['city']}) to {fnum(heat[-1],'avg_apparent_high_c')}C ({heat[-1]['city']}) = {round(spread,1)}C")

# ---------- ana_05: hot match-hours (matches x feels-like) ----------
print("=== ana_05 ===")
hm = []
for r in wx:
    score = cnt[r["stadium"]] * fnum(r,"avg_apparent_high_c")
    hm.append([r["city"], cnt[r["stadium"]], round(fnum(r,"avg_apparent_high_c"),1), round(score,1)])
hm.sort(key=lambda x: x[3], reverse=True)
for city, m, fl, sc in hm:
    print(f"{sc:>7.1f}  {city:<22} {m} matches x {fl}C")
# share of "hot football": matches at feels-like >= 34C
hot_venues = [r for r in wx if fnum(r,"avg_apparent_high_c") >= 34]
hot_matches = sum(cnt[r["stadium"]] for r in hot_venues)
print(f"matches at venues with feels-like >= 34C: {hot_matches} of 104 = {round(100*hot_matches/104,1)}%")
fifapro6 = {"Atlanta Stadium","Dallas Stadium","Houston Stadium","Kansas City Stadium","Miami Stadium","Estadio Monterrey"}
fifapro_matches = sum(cnt[s] for s in fifapro6)
print(f"matches at FIFPRO 'extremely high risk' 6 venues: {fifapro_matches} of 104 = {round(100*fifapro_matches/104,1)}%")

# ---------- ana_06: rain exposure ----------
print("=== ana_06 ===")
rain = sorted(wx, key=lambda r: fnum(r,"rainy_day_share"), reverse=True)
rain_rows = []
for r in rain:
    rain_rows.append([r["city"], round(fnum(r,"rainy_day_share")*100), round(fnum(r,"avg_precip_mm_per_day"),1), cnt[r["stadium"]]])
    print(f"{fnum(r,'rainy_day_share')*100:>5.0f}% wet days  {fnum(r,'avg_precip_mm_per_day'):>4.1f}mm/day  {r['city']}")

# ---------- ana_07: altitude ----------
print("=== ana_07 ===")
alt = sorted(wx, key=lambda r: fnum(r,"elevation_m"), reverse=True)
alt_rows = []
for r in alt:
    alt_rows.append([r["city"], int(fnum(r,"elevation_m")), cnt[r["stadium"]]])
    print(f"{int(fnum(r,'elevation_m')):>5}m  {r['city']}  ({r['venue']})")

# ---------- ana_08: temp vs humidity scatter (brutal vs mild) ----------
print("=== ana_08 ===")
scatter = []
def bucket(r):
    fl = fnum(r,"avg_apparent_high_c"); hum = fnum(r,"avg_humidity_pct")
    if fl >= 34 and hum >= 70: return "brutal (hot+humid)"
    if fl >= 34: return "dry-hot"
    if fl <= 27: return "mild"
    return "warm"
for r in wx:
    b = bucket(r)
    scatter.append([r["city"], round(fnum(r,"avg_apparent_high_c"),1), round(fnum(r,"avg_humidity_pct"),1), cnt[r["stadium"]], b])
    print(f"{r['city']:<22} feels {fnum(r,'avg_apparent_high_c'):>5.1f}C hum {fnum(r,'avg_humidity_pct'):>4.1f}%  -> {b}")
bcount = Counter(s[4] for s in scatter)
print("buckets:", dict(bcount))

# ---------- ana_09: map data (lat/lon + all climate per venue) ----------
print("=== ana_09 ===")
map_rows = []
photo_slug = {  # city -> asset filename slug
}
def slug(city):
    return city.lower().replace(" ","_").replace("/","_").replace(".","").replace("'","")
# Map by stadium to photo file (Kansas City has none)
city_to_photo = {
 "Mexico City":"mexico_city__photo.jpg","Guadalajara":"guadalajara__photo.jpg","Monterrey":"monterrey__photo.jpg",
 "Toronto":"toronto__photo.png","Vancouver":"vancouver__photo.jpg","Atlanta":"atlanta__photo.jpg",
 "Foxborough":"boston__photo.jpg","Arlington":"dallas__photo.jpg","Houston":"houston__photo.jpg",
 "Kansas City":"","Inglewood":"los_angeles__photo.jpg","Miami Gardens":"miami__photo.jpg",
 "East Rutherford":"new_york_new_jersey__photo.jpg","Philadelphia":"philadelphia__photo.jpg",
 "Santa Clara":"san_francisco_bay_area__photo.jpg","Seattle":"seattle__photo.jpg"}
for r in wx:
    map_rows.append([
        r["stadium"], r["venue"], r["city"], r["country"],
        round(fnum(r,"lat"),4), round(fnum(r,"lon"),4), int(fnum(r,"elevation_m")),
        round(fnum(r,"avg_apparent_high_c"),1), round(fnum(r,"avg_high_c"),1),
        int(fnum(r,"avg_humidity_pct")), round(fnum(r,"rainy_day_share")*100), cnt[r["stadium"]],
        city_to_photo.get(r["city"],"")
    ])
    print(f"{r['city']:<18} ({r['lat']},{r['lon']}) feels {r['avg_apparent_high_c']} photo={city_to_photo.get(r['city'],'NONE')}")

# ---------- ana_10: schedule timeline by date ----------
print("=== ana_10 ===")
bydate = Counter(r["date_dt"] for r in sched)
tl_rows = [[d, bydate[d]] for d in sorted(bydate)]
print(f"first day {sorted(bydate)[0]} ({bydate[sorted(bydate)[0]]} matches), last {sorted(bydate)[-1]} ({bydate[sorted(bydate)[-1]]})")
busiest = max(bydate.items(), key=lambda x: x[1])
print(f"busiest day: {busiest[0]} with {busiest[1]} matches")
print(f"group-stage window has up to {busiest[1]} matches/day across venues")

# ---------- ana_11: correlation humidity vs feels-like gap ----------
print("=== ana_11 ===")
gap_rows = []
for r in wx:
    gap = fnum(r,"avg_apparent_high_c") - fnum(r,"avg_high_c")
    gap_rows.append([r["city"], round(fnum(r,"avg_humidity_pct"),1), round(gap,1)])
gap_rows.sort(key=lambda x: x[2], reverse=True)
for city, hum, g in gap_rows:
    print(f"{g:>+5.1f}C feels-gap  hum {hum:>4.1f}%  {city}")
# simple pearson
import statistics as st
hs = [fnum(r,"avg_humidity_pct") for r in wx]
gs = [fnum(r,"avg_apparent_high_c")-fnum(r,"avg_high_c") for r in wx]
mh, mg = st.mean(hs), st.mean(gs)
cov = sum((h-mh)*(g-mg) for h,g in zip(hs,gs))/len(hs)
corr = cov/(st.pstdev(hs)*st.pstdev(gs))
print(f"pearson(humidity, feels-gap) = {round(corr,3)}")

# ---------- ana_12: extremes / stat callouts ----------
print("=== ana_12 ===")
hottest = max(wx, key=lambda r: fnum(r,"avg_apparent_high_c"))
coolest = min(wx, key=lambda r: fnum(r,"avg_apparent_high_c"))
wettest = max(wx, key=lambda r: fnum(r,"rainy_day_share"))
driest  = min(wx, key=lambda r: fnum(r,"rainy_day_share"))
highest = max(wx, key=lambda r: fnum(r,"elevation_m"))
maxhi   = max(wx, key=lambda r: fnum(r,"max_high_c"))
print(f"hottest feels-like: {hottest['city']} {hottest['avg_apparent_high_c']}C")
print(f"coolest feels-like: {coolest['city']} {coolest['avg_apparent_high_c']}C")
print(f"wettest: {wettest['city']} {round(fnum(wettest,'rainy_day_share')*100)}% of days")
print(f"driest: {driest['city']} {round(fnum(driest,'rainy_day_share')*100)}% of days")
print(f"highest altitude: {highest['city']} {int(fnum(highest,'elevation_m'))}m")
print(f"hottest single day on record in window: {maxhi['city']} {maxhi['max_high_c']}C")

# ---------- emit JSON-ready tables to stdout marker for reference ----------
print("=== TABLES_OK ===")
