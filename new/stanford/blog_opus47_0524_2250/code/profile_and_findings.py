"""Stanford founders analysis. Run from DATA_DIR.
Usage: cd DATA_DIR && python3 .../code/profile_and_findings.py
"""
import pandas as pd
import numpy as np
import re

df = pd.read_csv('stanford_founders.csv')
ranked = pd.read_csv('founders_ranked.csv')
industry = pd.read_csv('industry_breakdown.csv')
tech = pd.read_csv('tech_companies.csv')

# --- ana_00: Dataset profile ---
print("=== ana_00 ===")
print("rows:", len(df))
print("unique companies (company_id):", df['company_id'].nunique())
print("unique founders (founder_id):", df['founder_id'].nunique())
yr = pd.to_numeric(df['founded_year'], errors='coerce')
print("year min/max:", int(yr.min()), int(yr.max()))
print("is_tech True rows:", int((df['is_tech'] == True).sum()))
print("industries (industry_breakdown rows):", len(industry))
print("missing founded_year:", int(yr.isna().sum()))
print("missing headquarters:", int(df['headquarters'].isna().sum()))
print("rows with no industry (unspecified):", int(df['industry'].isna().sum()))

# --- ana_01: Foundings by decade (the boom curve) ---
print("=== ana_01 ===")
uniq = df.drop_duplicates('company_id').copy()
uy = pd.to_numeric(uniq['founded_year'], errors='coerce')
dec = (uy // 10 * 10).dropna().astype(int)
dec_counts = dec.value_counts().sort_index()
for d, c in dec_counts.items():
    print(f"{d}s: {c}")
print("peak decade:", dec_counts.idxmax(), dec_counts.max())

# --- ana_02: Most prolific founders (raw, all orgs) ---
print("=== ana_02 ===")
print(ranked.head(12).to_string(index=False))

# --- ana_03: Geographic concentration of headquarters ---
print("=== ana_03 ===")
hq = uniq['headquarters'].value_counts()
print(hq.head(12).to_string())
bay = ['San Francisco', 'Mountain View', 'Palo Alto', 'Sunnyvale', 'Menlo Park',
       'San Jose', 'Santa Clara', 'Cupertino', 'Redwood City', 'Los Altos',
       'Foster City', 'Fremont', 'San Mateo', 'Milpitas', 'Belmont']
hq_known = uniq.dropna(subset=['headquarters'])
bay_n = hq_known['headquarters'].isin(bay).sum()
print("HQ known:", len(hq_known), "| Bay Area core cities:", bay_n,
      f"({100*bay_n/len(hq_known):.1f}% of known-HQ companies)")

# --- ana_04: Industry breakdown excluding unspecified ---
print("=== ana_04 ===")
ind2 = industry[industry['industry'] != '(unspecified)'].head(12)
print(ind2.to_string(index=False))
unspec = industry[industry['industry'] == '(unspecified)']['company_count'].iloc[0]
print("unspecified count:", int(unspec), f"({100*unspec/industry['company_count'].sum():.1f}% of all industry tags)")

# --- ana_05: The tech-flag undercount ---
print("=== ana_05 ===")
n_no_industry = int(df['industry'].isna().sum())
n_tech = int((df['is_tech'] == True).sum())
print("total links:", len(df))
print("links with NO industry recorded:", n_no_industry, f"({100*n_no_industry/len(df):.1f}%)")
print("links flagged is_tech=True:", n_tech, f"({100*n_tech/len(df):.1f}%)")
print("links with an industry but not tech-flagged:", len(df) - n_no_industry - n_tech)

# --- ana_06: Founding-era tech share over time (tech flag) ---
print("=== ana_06 ===")
df2 = df.copy()
df2['yr'] = pd.to_numeric(df2['founded_year'], errors='coerce')
df2['dec'] = (df2['yr'] // 10 * 10)
g = df2.dropna(subset=['dec']).groupby('dec').agg(
    total=('company', 'size'),
    tech=('is_tech', lambda s: (s == True).sum())
)
g['tech_pct'] = (100 * g['tech'] / g['total']).round(1)
g.index = g.index.astype(int)
print(g.to_string())

# --- ana_07: The canonical company timeline (named landmarks) ---
print("=== ana_07 ===")
landmarks = ['Hewlett-Packard', 'Sun Microsystems', 'Cisco', 'Silicon Graphics',
             'Logitech', 'Intuit', 'Yahoo!', 'Google', 'PayPal', 'LinkedIn',
             'Tesla', 'Palantir Technologies', 'Instagram', 'Snapchat',
             'Nvidia', 'NVIDIA', 'WhatsApp', 'YouTube']
sub = df[df['company'].isin(landmarks)][['company', 'founded_year', 'founder']].drop_duplicates('company')
sub = sub.sort_values('founded_year')
print(sub.to_string(index=False))

# --- ana_08: Co-founder density (companies with multiple Stanford founders) ---
print("=== ana_08 ===")
co = df.groupby(['company_id', 'company'])['founder'].nunique().reset_index(name='n_stanford_founders')
co = co.sort_values('n_stanford_founders', ascending=False)
print("companies with >1 Stanford founder:", int((co['n_stanford_founders'] > 1).sum()))
print(co.head(10).to_string(index=False))

# --- ana_09: Tech vs non-tech among industry-specified companies ---
print("=== ana_09 ===")
spec = df[df['industry'].notna()].drop_duplicates('company_id')
spec_tech = (spec['is_tech'] == True).sum()
print("companies with a specified industry:", len(spec))
print("of those, tech-flagged:", int(spec_tech), f"({100*spec_tech/len(spec):.1f}%)")
print("non-tech specified:", len(spec) - int(spec_tech))
