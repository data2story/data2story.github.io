"""Round-number bias and presentation-order (anchoring) effects."""
import pandas as pd
import numpy as np

DATA = '/Users/forrest/Desktop/data2story-skill/data/likely'
aj = pd.read_csv(f'{DATA}/absolute_judgements.csv')

# --- ana_05: Round-number bias (multiples of 10, ending in 5) ---
print("=== ana_05 ===")
p = aj['probability']
mult10 = (p % 10 == 0).mean() * 100
end5 = (p % 10 == 5).mean() * 100
print(f"Multiples of 10: {mult10:.1f}%")
print(f"Ending in 5 (not 10): {end5:.1f}%")
print(f"Multiple of 5 (incl 10): {(p%5==0).mean()*100:.1f}%")
print(f"Other (not multiple of 5): {(p%5!=0).mean()*100:.1f}%")
# last-digit distribution for chart
ld = (p % 10).value_counts().sort_index()
print("last-digit counts:")
for d, c in ld.items():
    print(f"  {d}: {c} ({c/len(p)*100:.1f}%)")

# --- ana_06: Share of respondents who rounded EVERY estimate to a multiple of 10 ---
print("=== ana_06 ===")
def all_mult10(s): return (s % 10 == 0).all()
per_resp = aj.groupby('response_id')['probability'].apply(all_mult10)
print(f"Respondents who gave only multiples of 10: {per_resp.mean()*100:.1f}% ({per_resp.sum()} of {len(per_resp)})")
per5 = aj.groupby('response_id')['probability'].apply(lambda s:(s%5==0).all())
print(f"Respondents who gave only multiples of 5: {per5.mean()*100:.1f}% ({per5.sum()} of {len(per5)})")

# --- ana_07: Order / anchoring effect — does position in the sequence shift the value? ---
print("=== ana_07 ===")
# Within each term, does the value depend on the order it was shown?
# Compute per-order mean (across all terms) after centering each term to remove term effect
aj2 = aj.copy()
term_mean = aj2.groupby('term')['probability'].transform('mean')
aj2['centered'] = aj2['probability'] - term_mean
order_eff = aj2.groupby('order')['centered'].agg(['mean','count'])
print("Order effect (term-centered mean value by presentation position):")
print(order_eff.round(2).to_string())
early = aj2[aj2.order <= 3]['centered'].mean()
late = aj2[aj2.order >= 17]['centered'].mean()
print(f"First 3 positions centered mean: {early:.2f}")
print(f"Last 3 positions centered mean: {late:.2f}")
print(f"Difference (early - late): {early-late:.2f} percentage points")
corr = aj2[['order','centered']].corr().iloc[0,1]
print(f"Correlation order vs term-centered value: {corr:.4f}")
