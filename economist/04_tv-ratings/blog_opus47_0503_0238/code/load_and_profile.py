"""Stage 2 / Step 1 — Dataset profile + global rating drift."""
import csv
from collections import Counter, defaultdict
from statistics import mean, median, stdev

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/04_tv-ratings/IMDb_Economist_tv_ratings.csv'

with open(DATA) as f:
    rows = list(csv.DictReader(f))

# Cast types
for r in rows:
    r['av_rating'] = float(r['av_rating'])
    r['share'] = float(r['share'])
    r['seasonNumber'] = int(r['seasonNumber'])
    r['year'] = int(r['date'][:4])
    r['genres_list'] = [g.strip() for g in r['genres'].split(',') if g.strip()]

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"Rows (seasons): {len(rows)}")
print(f"Unique titles: {len(set(r['title'] for r in rows))}")
print(f"Unique titleIds: {len(set(r['titleId'] for r in rows))}")
years = sorted(set(r['year'] for r in rows))
print(f"Year range: {years[0]} to {years[-1]}")
print(f"Mean av_rating: {mean(r['av_rating'] for r in rows):.3f}")
print(f"Median av_rating: {median(r['av_rating'] for r in rows):.3f}")
print(f"Std dev av_rating: {stdev(r['av_rating'] for r in rows):.3f}")
print(f"Min av_rating: {min(r['av_rating'] for r in rows):.3f}")
print(f"Max av_rating: {max(r['av_rating'] for r in rows):.3f}")

# --- ana_02: Median rating per premiere year ---
print("\n=== ana_02 ===")
by_year = defaultdict(list)
for r in rows:
    by_year[r['year']].append(r['av_rating'])

year_stats = []
for y in sorted(by_year):
    vals = by_year[y]
    year_stats.append((y, len(vals), median(vals), mean(vals)))

print("year, n_seasons, median, mean")
for y, n, med, m in year_stats:
    print(f"{y}, {n}, {med:.3f}, {m:.3f}")

# Compare 1990s to 2010s
nineties = [r['av_rating'] for r in rows if 1990 <= r['year'] <= 1999]
tens = [r['av_rating'] for r in rows if 2010 <= r['year'] <= 2018]
print(f"\n1990s median: {median(nineties):.3f}, mean: {mean(nineties):.3f}, n={len(nineties)}")
print(f"2010s median: {median(tens):.3f}, mean: {mean(tens):.3f}, n={len(tens)}")
print(f"Median lift 1990s→2010s: {median(tens) - median(nineties):+.3f}")

# --- ana_03: Number of seasons per premiere year (Peak TV) ---
print("\n=== ana_03 ===")
print("year, n_seasons")
for y, n, _, _ in year_stats:
    print(f"{y}, {n}")
print(f"\nSeasons in 1990: {by_year[1990] and len(by_year[1990])}")
print(f"Seasons in 2017 (last full year): {len(by_year[2017])}")
print(f"Growth multiple: {len(by_year[2017]) / max(1,len(by_year[1990])):.1f}x")

# --- ana_04: Floor vs. ceiling — 10th vs 90th percentile by year ---
print("\n=== ana_04 ===")

def pct(vals, p):
    s = sorted(vals)
    if not s:
        return None
    i = (len(s) - 1) * p
    lo, hi = int(i), min(int(i) + 1, len(s) - 1)
    frac = i - lo
    return s[lo] * (1 - frac) + s[hi] * frac

print("year, n, p10, p50, p90")
floor_ceiling = []
for y in sorted(by_year):
    vals = by_year[y]
    if len(vals) < 5:  # skip thin years for percentile reliability
        continue
    p10, p50, p90 = pct(vals, 0.10), pct(vals, 0.50), pct(vals, 0.90)
    floor_ceiling.append((y, len(vals), p10, p50, p90))
    print(f"{y}, {len(vals)}, {p10:.3f}, {p50:.3f}, {p90:.3f}")

# Compare endpoints
fc_1995 = [r for r in floor_ceiling if r[0] == 1995]
fc_2017 = [r for r in floor_ceiling if r[0] == 2017]
if fc_1995 and fc_2017:
    a, b = fc_1995[0], fc_2017[0]
    print(f"\nFloor (p10) 1995 vs 2017: {a[2]:.2f} → {b[2]:.2f} (Δ {b[2]-a[2]:+.2f})")
    print(f"Median (p50) 1995 vs 2017: {a[3]:.2f} → {b[3]:.2f} (Δ {b[3]-a[3]:+.2f})")
    print(f"Ceiling (p90) 1995 vs 2017: {a[4]:.2f} → {b[4]:.2f} (Δ {b[4]-a[4]:+.2f})")
