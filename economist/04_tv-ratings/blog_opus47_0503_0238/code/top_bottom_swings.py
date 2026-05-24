"""Stage 2 / Step 2 — Top, bottom, and biggest within-show swings."""
import csv
from collections import defaultdict

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/04_tv-ratings/IMDb_Economist_tv_ratings.csv'

with open(DATA) as f:
    rows = list(csv.DictReader(f))

for r in rows:
    r['av_rating'] = float(r['av_rating'])
    r['share'] = float(r['share'])
    r['seasonNumber'] = int(r['seasonNumber'])
    r['year'] = int(r['date'][:4])

# --- ana_05: Top 15 highest-rated seasons ---
print("=== ana_05 ===")
top = sorted(rows, key=lambda r: -r['av_rating'])[:15]
for i, r in enumerate(top, 1):
    print(f"{i}. {r['title']} S{r['seasonNumber']} ({r['date'][:4]}): {r['av_rating']:.3f}  share={r['share']}")

# --- ana_06: Bottom 15 lowest-rated seasons ---
print("\n=== ana_06 ===")
bot = sorted(rows, key=lambda r: r['av_rating'])[:15]
for i, r in enumerate(bot, 1):
    print(f"{i}. {r['title']} S{r['seasonNumber']} ({r['date'][:4]}): {r['av_rating']:.3f}  share={r['share']}")

# --- ana_07: Biggest within-show drops (any season vs. earlier season) ---
print("\n=== ana_07 ===")
by_show = defaultdict(list)
for r in rows:
    by_show[r['title']].append(r)

drops = []
rises = []
for title, seasons in by_show.items():
    if len(seasons) < 2:
        continue
    seasons = sorted(seasons, key=lambda r: r['seasonNumber'])
    peak_so_far = seasons[0]['av_rating']
    peak_idx = 0
    for i, s in enumerate(seasons[1:], 1):
        delta = s['av_rating'] - peak_so_far
        if delta < 0:
            drops.append({
                'title': title,
                'from_season': peak_idx + 1,
                'to_season': s['seasonNumber'],
                'from_rating': peak_so_far,
                'to_rating': s['av_rating'],
                'delta': delta,
                'date_to': s['date']
            })
        if s['av_rating'] > peak_so_far:
            peak_so_far = s['av_rating']
            peak_idx = i
    # And track best lift first->last
    if len(seasons) >= 2:
        delta = seasons[-1]['av_rating'] - seasons[0]['av_rating']
        rises.append({
            'title': title,
            'first_season': seasons[0]['seasonNumber'],
            'last_season': seasons[-1]['seasonNumber'],
            'first_rating': seasons[0]['av_rating'],
            'last_rating': seasons[-1]['av_rating'],
            'delta': delta,
        })

# Top 12 biggest drops from prior peak
drops_sorted = sorted(drops, key=lambda d: d['delta'])[:12]
print("Biggest drops from a previous peak (within-show):")
for d in drops_sorted:
    print(f"  {d['title']} S{d['from_season']}→S{d['to_season']}: "
          f"{d['from_rating']:.2f} → {d['to_rating']:.2f}  (Δ {d['delta']:+.2f}, {d['date_to'][:4]})")

# --- ana_08: Biggest sustained rises (first season → best later season) ---
print("\n=== ana_08 ===")
rises_sorted = sorted(rises, key=lambda d: -d['delta'])[:12]
print("Biggest first→last lift (last season - first season):")
for r in rises_sorted:
    print(f"  {r['title']} S{r['first_season']}→S{r['last_season']}: "
          f"{r['first_rating']:.2f} → {r['last_rating']:.2f}  (Δ {r['delta']:+.2f})")

# --- ana_09: Shows with the most seasons in dataset ---
print("\n=== ana_09 ===")
show_counts = sorted(by_show.items(), key=lambda x: -len(x[1]))[:15]
for title, seasons in show_counts:
    avg = sum(s['av_rating'] for s in seasons) / len(seasons)
    yr_first = min(s['date'][:4] for s in seasons)
    yr_last = max(s['date'][:4] for s in seasons)
    print(f"  {title}: {len(seasons)} seasons ({yr_first}–{yr_last}), avg {avg:.2f}")
