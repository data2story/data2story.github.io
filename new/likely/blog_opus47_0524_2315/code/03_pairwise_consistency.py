"""Pairwise comparisons: closest contests, and consistency with absolute rankings."""
import pandas as pd
import numpy as np
from itertools import combinations

DATA = '/Users/forrest/Desktop/data2story-skill/data/likely'
aj = pd.read_csv(f'{DATA}/absolute_judgements.csv')
pc = pd.read_csv(f'{DATA}/pairwise_comparisons.csv')

# Absolute mean per term (for cross-check)
abs_mean = aj.groupby('term')['probability'].mean()

# --- ana_08: Closest head-to-head contests (most disagreement on which is higher) ---
print("=== ana_08 ===")
# normalize pair so (a,b) and (b,a) are the same
def pair_key(r):
    return tuple(sorted([r['term1'], r['term2']]))
pc['pair'] = pc.apply(pair_key, axis=1)
rows = []
for pair, grp in pc.groupby('pair'):
    a, b = pair
    n = len(grp)
    a_wins = (grp['selected'] == a).sum()
    b_wins = (grp['selected'] == b).sum()
    # share that picked the alphabetically-first term
    a_share = a_wins / n * 100
    winner_share = max(a_wins, b_wins) / n * 100
    rows.append([a, b, n, a_wins, b_wins, round(a_share,1), round(winner_share,1)])
contests = pd.DataFrame(rows, columns=['term_a','term_b','n','a_wins','b_wins','a_share','winner_share'])
closest = contests.sort_values('winner_share').head(12)
print("Closest contests (winner_share near 50% = most disagreement):")
print(closest.to_string(index=False))

# --- ana_09: 'Could Happen' vs 'Might Happen' near 50/50 (det_04) ---
print("=== ana_09 ===")
for combo in [('Could Happen','Might Happen'), ('Likely','Probable'), ('May Happen','Might Happen'),
              ('May Happen','Could Happen')]:
    key = tuple(sorted(combo))
    sub = contests[(contests.term_a==key[0]) & (contests.term_b==key[1])]
    if len(sub):
        r = sub.iloc[0]
        print(f"{r.term_a} vs {r.term_b}: n={r.n}, {r.term_a} chosen {r.a_share:.1f}% | abs means: {abs_mean[r.term_a]:.1f} vs {abs_mean[r.term_b]:.1f}")

# --- ana_10: Internal consistency — repeated pair agreement rate ---
print("=== ana_10 ===")
# Each respondent saw 10 pairs incl 1 repeated. Find respondents who saw the same unordered pair twice.
dup = pc.groupby(['response_id','pair'])
flip_rates = []
inconsistent = 0
total_repeats = 0
for (rid, pair), grp in dup:
    if len(grp) >= 2:
        total_repeats += 1
        if grp['selected'].nunique() > 1:
            inconsistent += 1
print(f"Respondents with a repeated pair: {total_repeats}")
print(f"Of those, gave a DIFFERENT answer the 2nd time (flipped): {inconsistent} ({inconsistent/total_repeats*100:.1f}%)")
print(f"Consistent (same answer both times): {(total_repeats-inconsistent)/total_repeats*100:.1f}%")

# --- ana_11: Pairwise rank vs absolute rank — do they agree? ---
print("=== ana_11 ===")
# Build a win-rate ranking: for each term, total times chosen / total times it appeared
appear = {}
wins = {}
for _, r in pc.iterrows():
    for t in [r['term1'], r['term2']]:
        appear[t] = appear.get(t,0)+1
    wins[r['selected']] = wins.get(r['selected'],0)+1
winrate = pd.Series({t: wins.get(t,0)/appear[t] for t in appear}).sort_values(ascending=False)
abs_rank = abs_mean.rank(ascending=False)
pw_rank = winrate.rank(ascending=False)
cmp = pd.DataFrame({'abs_mean': abs_mean, 'abs_rank': abs_rank, 'winrate': winrate*100, 'pw_rank': pw_rank})
cmp = cmp.sort_values('abs_rank')
cmp['rank_gap'] = cmp['abs_rank'] - cmp['pw_rank']
print(cmp.round(1).to_string())
sp = cmp[['abs_rank','pw_rank']].corr(method='spearman').iloc[0,1]
print(f"Spearman rank correlation (absolute vs pairwise): {sp:.3f}")
