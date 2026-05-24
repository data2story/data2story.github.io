"""Stage 2 / Step 5 — Emit chart-ready data_tables (printed, then transcribed into analyst.json)."""
import csv
import json
from collections import defaultdict
from statistics import median, mean

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/04_tv-ratings/IMDb_Economist_tv_ratings.csv'

with open(DATA) as f:
    rows = list(csv.DictReader(f))
for r in rows:
    r['av_rating'] = float(r['av_rating'])
    r['share'] = float(r['share'])
    r['seasonNumber'] = int(r['seasonNumber'])
    r['year'] = int(r['date'][:4])
    r['genres_list'] = [g.strip() for g in r['genres'].split(',') if g.strip()]


def pct(vals, p):
    s = sorted(vals)
    if not s:
        return None
    i = (len(s) - 1) * p
    lo, hi = int(i), min(int(i) + 1, len(s) - 1)
    frac = i - lo
    return s[lo] * (1 - frac) + s[hi] * frac


# Table A: per-year n, p10, p50, p90 (for floor/ceiling chart)
print("=== TABLE: year_floor_ceiling ===")
by_year = defaultdict(list)
for r in rows:
    by_year[r['year']].append(r['av_rating'])
table = []
for y in sorted(by_year):
    vals = by_year[y]
    if len(vals) < 5:
        # still report
        p10, p50, p90 = pct(vals, 0.10), pct(vals, 0.50), pct(vals, 0.90)
    else:
        p10, p50, p90 = pct(vals, 0.10), pct(vals, 0.50), pct(vals, 0.90)
    table.append([y, len(vals), round(p10, 3), round(p50, 3), round(p90, 3)])
print(json.dumps(table, indent=None))

# Table B: scatter — every season as (year, av_rating, share, title) — full
print("\n=== TABLE: scatter_all (sample of 10 rows shown) ===")
scatter = [[r['date'][:7], round(r['av_rating'], 3), round(r['share'], 2), r['title'], r['seasonNumber']] for r in rows]
print(f"len={len(scatter)}, sample:")
for s in scatter[:10]:
    print(s)

# Save full scatter to a JSON file the analyst.json data_table will reference
with open('/Users/forrest/Desktop/data2blog/project/economist/04_tv-ratings/blog_opus47_0503_0238/code/scatter_all.json', 'w') as f:
    json.dump(scatter, f)
print(f"\nWrote scatter_all.json with {len(scatter)} rows")

# Table C: era buckets summary
print("\n=== TABLE: era_buckets ===")
eras = [
    ("Pre-Sopranos (1990–1998)", 1990, 1998),
    ("Cable prestige (1999–2012)", 1999, 2012),
    ("Streaming era (2013–2018)", 2013, 2018),
]
for label, lo, hi in eras:
    vals = [r['av_rating'] for r in rows if lo <= r['year'] <= hi]
    n = len(vals)
    print([label, n, round(median(vals),3), round(mean(vals),3),
           round(pct(vals,0.10),3), round(pct(vals,0.90),3)])

# Table D: genre 1990s vs 2010s drift (for divergent bar)
print("\n=== TABLE: genre_drift ===")
genres_seen = defaultdict(int)
for r in rows:
    for g in r['genres_list']:
        genres_seen[g] += 1
big_genres = [g for g, c in genres_seen.items() if c >= 60]
for g in big_genres:
    nineties = [r['av_rating'] for r in rows
                if g in r['genres_list'] and 1990 <= r['year'] <= 1999]
    tens = [r['av_rating'] for r in rows
            if g in r['genres_list'] and 2010 <= r['year'] <= 2018]
    if len(nineties) >= 5 and len(tens) >= 5:
        a, b = median(nineties), median(tens)
        print([g, len(nineties), len(tens), round(a,3), round(b,3), round(b-a,3)])

# Table E: GoT, Breaking Bad, Sopranos, Wire trajectories
print("\n=== TABLE: marquee_shows ===")
for title in ['Game of Thrones', 'Breaking Bad', 'The Sopranos', 'The Wire',
              'Mad Men', 'BoJack Horseman', 'Lost', 'Dexter']:
    show_rows = sorted([r for r in rows if r['title'] == title], key=lambda r: r['seasonNumber'])
    if not show_rows:
        print(f"  (not in dataset: {title})")
        continue
    for r in show_rows:
        print([title, r['seasonNumber'], r['date'], round(r['av_rating'],3), round(r['share'],2)])

# Table F: share quartile vs rating
print("\n=== TABLE: share_quartiles ===")
shares = sorted(r['share'] for r in rows)
n = len(shares)
q1 = shares[n//4]
q2 = shares[n//2]
q3 = shares[3*n//4]
buckets = {'Q1: lowest 25% votes': [], 'Q2': [], 'Q3': [], 'Q4: highest 25% votes': []}
for r in rows:
    s = r['share']
    if s <= q1:
        buckets['Q1: lowest 25% votes'].append(r['av_rating'])
    elif s <= q2:
        buckets['Q2'].append(r['av_rating'])
    elif s <= q3:
        buckets['Q3'].append(r['av_rating'])
    else:
        buckets['Q4: highest 25% votes'].append(r['av_rating'])
for b, vals in buckets.items():
    print([b, len(vals), round(median(vals),3), round(mean(vals),3)])

# Table G: per-year season count
print("\n=== TABLE: yearly_volume ===")
for y in sorted(by_year):
    print([y, len(by_year[y])])
