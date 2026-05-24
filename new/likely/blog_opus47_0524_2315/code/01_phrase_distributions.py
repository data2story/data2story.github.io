"""Per-phrase distribution analysis: central tendency and spread (disagreement)."""
import pandas as pd
import numpy as np

DATA = '/Users/forrest/Desktop/data2story-skill/data/likely'
aj = pd.read_csv(f'{DATA}/absolute_judgements.csv')

# --- ana_01: Per-phrase central tendency, ranked by mean ---
print("=== ana_01 ===")
g = aj.groupby('term')['probability']
stats = pd.DataFrame({
    'mean': g.mean(), 'median': g.median(), 'std': g.std(),
    'q25': g.quantile(0.25), 'q75': g.quantile(0.75), 'n': g.count()
})
stats['iqr'] = stats['q75'] - stats['q25']
stats = stats.sort_values('mean', ascending=False)
pd.set_option('display.width', 200)
print(stats.round(1).to_string())

# --- ana_02: Disagreement ranking — which phrases split people most (by std dev) ---
print("=== ana_02 ===")
disagree = stats.sort_values('std', ascending=False)
print(disagree[['mean', 'median', 'std', 'iqr']].round(1).to_string())

# --- ana_03: Realistic Possibility vs UK official 40-50% benchmark (det_03) ---
print("=== ana_03 ===")
rp = aj[aj.term == 'Realistic Possibility']['probability']
in_band = ((rp >= 40) & (rp <= 50)).mean() * 100
print(f"Realistic Possibility: mean={rp.mean():.1f} median={rp.median():.0f} std={rp.std():.1f}")
print(f"UK official definition 40-50%. Share of responses inside 40-50%: {in_band:.1f}%")
print(f"Share below 40%: {(rp<40).mean()*100:.1f}%  Share above 50%: {(rp>50).mean()*100:.1f}%")
print(f"Min {rp.min()} Max {rp.max()}  range spans full 0-100")
# spread histogram for chart
bins = list(range(0, 101, 10))
hist = pd.cut(rp, bins=bins, include_lowest=True).value_counts().sort_index()
print("histogram (10-pt bins):")
for iv, c in hist.items():
    print(f"  {int(iv.left)}-{int(iv.right)}: {c}")

# --- ana_04: How wide each phrase spans — full-range phrases ---
print("=== ana_04 ===")
span = aj.groupby('term')['probability'].agg(['min','max','std'])
span['range'] = span['max'] - span['min']
# fraction of mass in extreme tails for the "spanning" phrases
for t in ['May Happen','Might Happen','Could Happen','Realistic Possibility']:
    s = aj[aj.term==t]['probability']
    print(f"{t}: <=10%: {(s<=10).mean()*100:.0f}%  >=90%: {(s>=90).mean()*100:.0f}%  std {s.std():.1f}")
