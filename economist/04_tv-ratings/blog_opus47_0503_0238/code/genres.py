"""Stage 2 / Step 3 — Genre comparisons + share-vs-rating relationship."""
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
    r['genres_list'] = [g.strip() for g in r['genres'].split(',') if g.strip()]

# --- ana_10: Median rating per genre tag (each season counts once per tag) ---
print("=== ana_10 ===")
genre_ratings = defaultdict(list)
for r in rows:
    for g in r['genres_list']:
        genre_ratings[g].append(r['av_rating'])

# Filter to genres with at least 30 seasons
genre_stats = []
for g, vals in genre_ratings.items():
    if len(vals) >= 30:
        genre_stats.append((g, len(vals), median(vals), mean(vals)))

genre_stats.sort(key=lambda x: -x[2])
print(f"{'genre':<14} {'n':>5} {'median':>8} {'mean':>8}")
for g, n, med, m in genre_stats:
    print(f"{g:<14} {n:>5} {med:>8.3f} {m:>8.3f}")

# --- ana_11: Genre rating drift across decades (top genres) ---
print("\n=== ana_11 ===")
big_genres = [g for g, _, _, _ in genre_stats][:10]
print(f"{'genre':<14} {'1990s_med':>10} {'2010s_med':>10} {'Δ':>8}")
genre_drift = []
for g in big_genres:
    nineties = [r['av_rating'] for r in rows
                if g in r['genres_list'] and 1990 <= r['year'] <= 1999]
    tens = [r['av_rating'] for r in rows
            if g in r['genres_list'] and 2010 <= r['year'] <= 2018]
    if len(nineties) < 5 or len(tens) < 5:
        continue
    a, b = median(nineties), median(tens)
    genre_drift.append((g, a, b, b - a))
    print(f"{g:<14} {a:>10.3f} {b:>10.3f} {b-a:>+8.3f}")

# --- ana_12: Share vs. rating — do popular shows rate higher? ---
print("\n=== ana_12 ===")
# Bucket by share quartiles
shares = sorted(r['share'] for r in rows)
n = len(shares)
q1 = shares[n//4]
q2 = shares[n//2]
q3 = shares[3*n//4]
print(f"share quartiles: q1={q1:.3f}, q2={q2:.3f}, q3={q3:.3f}, max={shares[-1]:.2f}")

buckets = defaultdict(list)
for r in rows:
    s = r['share']
    if s <= q1:
        b = 'Q1 (lowest 25% votes)'
    elif s <= q2:
        b = 'Q2'
    elif s <= q3:
        b = 'Q3'
    else:
        b = 'Q4 (highest 25% votes)'
    buckets[b].append(r['av_rating'])

print(f"{'bucket':<25} {'n':>5} {'median':>8} {'mean':>8}")
order = ['Q1 (lowest 25% votes)', 'Q2', 'Q3', 'Q4 (highest 25% votes)']
share_buckets_data = []
for b in order:
    vals = buckets[b]
    share_buckets_data.append((b, len(vals), median(vals), mean(vals)))
    print(f"{b:<25} {len(vals):>5} {median(vals):>8.3f} {mean(vals):>8.3f}")

# Pearson r on log-share vs rating
import math
xs = [math.log10(r['share'] + 0.01) for r in rows]
ys = [r['av_rating'] for r in rows]
mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
denx = math.sqrt(sum((x-mx)**2 for x in xs))
deny = math.sqrt(sum((y-my)**2 for y in ys))
r = num / (denx*deny)
print(f"\nPearson r (log share, rating): {r:.3f}")

# --- ana_13: Most-voted seasons (by share) ---
print("\n=== ana_13 ===")
top_share = sorted(rows, key=lambda r: -r['share'])[:15]
for i, r in enumerate(top_share, 1):
    print(f"{i}. {r['title']} S{r['seasonNumber']} ({r['date'][:4]}): "
          f"rating={r['av_rating']:.2f}, share={r['share']:.2f}")
