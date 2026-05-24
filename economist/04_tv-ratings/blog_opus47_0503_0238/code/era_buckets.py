"""Stage 2 / Step 4 — Era buckets aligned with the prestige-TV thesis."""
import csv
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

# --- ana_14: Three eras — Pre-Sopranos, Cable Prestige, Streaming ---
print("=== ana_14 ===")
eras = [
    ("Pre-Sopranos (1990–1998)", 1990, 1998),
    ("Cable prestige (1999–2012)", 1999, 2012),
    ("Streaming era (2013–2018)", 2013, 2018),
]
era_data = []
for label, lo, hi in eras:
    vals = [r['av_rating'] for r in rows if lo <= r['year'] <= hi]
    n = len(vals)
    era_data.append((label, lo, hi, n, median(vals), mean(vals),
                    sorted(vals)[int(0.10*(len(vals)-1))],
                    sorted(vals)[int(0.90*(len(vals)-1))]))
    print(f"{label}: n={n}, median={median(vals):.3f}, mean={mean(vals):.3f}")

# Print as a structured table
print("\nera, n_seasons, median, mean, p10, p90")
for label, lo, hi, n, med, m, p10, p90 in era_data:
    print(f"{label}, {n}, {med:.3f}, {m:.3f}, {p10:.3f}, {p90:.3f}")

# --- ana_15: Top 10 seasons of all time, with era flag ---
print("\n=== ana_15 ===")
top = sorted(rows, key=lambda r: -r['av_rating'])[:10]
for i, r in enumerate(top, 1):
    yr = r['year']
    if yr <= 1998:
        era = "Pre-Sopranos"
    elif yr <= 2012:
        era = "Cable prestige"
    else:
        era = "Streaming"
    print(f"{i}. {r['title']} S{r['seasonNumber']} ({yr}) — {r['av_rating']:.3f} [{era}]")

# --- ana_16: Share of "very high" (≥ 9.0) and "very low" (≤ 6.0) seasons by year ---
print("\n=== ana_16 ===")
by_year = defaultdict(list)
for r in rows:
    by_year[r['year']].append(r)
print("year, n, pct_above_9, pct_below_6")
extremes = []
for y in sorted(by_year):
    seasons = by_year[y]
    n = len(seasons)
    above = sum(1 for s in seasons if s['av_rating'] >= 9.0)
    below = sum(1 for s in seasons if s['av_rating'] <= 6.0)
    pa = 100*above/n
    pb = 100*below/n
    extremes.append((y, n, above, below, pa, pb))
    print(f"{y}, {n}, {pa:.1f}%, {pb:.1f}%")

# --- ana_17: Game of Thrones season-by-season trajectory ---
print("\n=== ana_17 ===")
got = sorted([r for r in rows if r['title'] == 'Game of Thrones'],
             key=lambda r: r['seasonNumber'])
for r in got:
    print(f"  S{r['seasonNumber']} ({r['date']}): {r['av_rating']:.3f}  share={r['share']}")

# --- ana_18: Breaking Bad trajectory ---
print("\n=== ana_18 ===")
bb = sorted([r for r in rows if r['title'] == 'Breaking Bad'],
            key=lambda r: r['seasonNumber'])
for r in bb:
    print(f"  S{r['seasonNumber']} ({r['date']}): {r['av_rating']:.3f}  share={r['share']}")

# --- ana_19: The Wire trajectory ---
print("\n=== ana_19 ===")
wire = sorted([r for r in rows if r['title'] == 'The Wire'],
              key=lambda r: r['seasonNumber'])
for r in wire:
    print(f"  S{r['seasonNumber']} ({r['date']}): {r['av_rating']:.3f}  share={r['share']}")

# --- ana_20: The Sopranos trajectory ---
print("\n=== ana_20 ===")
sopranos = sorted([r for r in rows if r['title'] == 'The Sopranos'],
                  key=lambda r: r['seasonNumber'])
for r in sopranos:
    print(f"  S{r['seasonNumber']} ({r['date']}): {r['av_rating']:.3f}  share={r['share']}")
