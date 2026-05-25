#!/usr/bin/env python3
"""Stanford -> Silicon Valley founder pipeline analysis.
Run from DATA_DIR (data/stanford). Produces all ana_xx outputs."""
import csv, re
from collections import Counter, defaultdict

ROWS = []
with open('stanford_founders.csv') as f:
    for r in csv.DictReader(f):
        ROWS.append(r)

# --- ana_01: Dataset profile ---
print("=== ana_01 ===")
print(f"total rows (founder->company links): {len(ROWS)}")
print(f"distinct founders: {len(set(r['founder_id'] for r in ROWS))}")
print(f"distinct companies (by company_id): {len(set(r['company_id'] for r in ROWS))}")
years = [int(r['founded_year']) for r in ROWS if r['founded_year'].strip().isdigit()]
print(f"rows with founded_year: {len(years)}; range {min(years)}-{max(years)}")
print(f"rows with headquarters: {sum(1 for r in ROWS if r['headquarters'].strip())}")
print(f"rows with industry: {sum(1 for r in ROWS if r['industry'].strip())}")
print(f"rows flagged is_tech True: {sum(1 for r in ROWS if r['is_tech']=='True')}")

# --- ana_02: Most prolific founders (by raw P112 count) ---
print("\n=== ana_02 ===")
fcount = Counter()
fcompanies = defaultdict(list)
for r in ROWS:
    fcount[r['founder']] += 1
    fcompanies[r['founder']].append(r['company'])
top = fcount.most_common(15)
for name, n in top:
    print(f"{name}: {n}")

# --- ana_03: Unique companies after de-dup on company_id ---
print("\n=== ana_03 ===")
uniq_companies = set(r['company_id'] for r in ROWS)
print(f"raw links: {len(ROWS)}")
print(f"unique companies/orgs (de-duped on company_id): {len(uniq_companies)}")
print(f"duplicate rows from co-founders: {len(ROWS) - len(uniq_companies)}")
# companies with most co-founders in data
co_per_company = Counter(r['company'] for r in ROWS)
multi = [(c,n) for c,n in co_per_company.items() if n>=3]
multi.sort(key=lambda x:-x[1])
print("companies appearing >=3x (multiple Stanford co-founders / dup entities):")
for c,n in multi[:10]:
    print(f"  {c}: {n}")

# --- ana_04: Founding-year timeline by decade/era ---
print("\n=== ana_04 ===")
era_bounds = [(0,1949,'Pre-1950'),(1950,1969,'1950s-60s'),(1970,1989,'1970s-80s'),
              (1990,1999,'1990s'),(2000,2009,'2000s'),(2010,2025,'2010s-20s')]
# de-dup year on company_id (use first row per company)
seen=set(); comp_year={}
for r in ROWS:
    if r['company_id'] not in seen and r['founded_year'].strip().isdigit():
        comp_year[r['company_id']]=int(r['founded_year']); seen.add(r['company_id'])
era_counts=Counter()
for y in comp_year.values():
    for lo,hi,lbl in era_bounds:
        if lo<=y<=hi: era_counts[lbl]+=1; break
for lo,hi,lbl in era_bounds:
    print(f"{lbl}: {era_counts[lbl]}")
print(f"companies with year: {len(comp_year)}")

# --- ana_05: Decade histogram (finer) ---
print("\n=== ana_05 ===")
dec=Counter()
for y in comp_year.values():
    dec[(y//10)*10]+=1
for d in sorted(dec):
    print(f"{d}s: {dec[d]}")

# --- ana_06: Industry breakdown ---
print("\n=== ana_06 ===")
with open('industry_breakdown.csv') as f:
    ind=[(r['industry'],int(r['company_count'])) for r in csv.DictReader(f)]
total_ind=sum(n for _,n in ind)
unspec=[n for i,n in ind if i=='(unspecified)'][0]
print(f"total industry rows: {total_ind}; (unspecified): {unspec} ({100*unspec/total_ind:.1f}%)")
print("top specified industries:")
for i,n in ind:
    if i!='(unspecified)':
        print(f"  {i}: {n}")
    if i!='(unspecified)' and ind.index((i,n))>12: break

# --- ana_07: Tech vs non-tech (and the undercount) ---
print("\n=== ana_07 ===")
tech_rows=sum(1 for r in ROWS if r['is_tech']=='True')
nontech_rows=len(ROWS)-tech_rows
no_industry=sum(1 for r in ROWS if not r['industry'].strip())
print(f"is_tech True: {tech_rows} ({100*tech_rows/len(ROWS):.1f}%)")
print(f"is_tech False: {nontech_rows} ({100*nontech_rows/len(ROWS):.1f}%)")
print(f"  of which no industry on Wikidata: {no_industry} ({100*no_industry/len(ROWS):.1f}%)")
print(f"  is_tech False WITH an industry recorded: {nontech_rows-no_industry}")

# --- ana_08: HQ geography ---
print("\n=== ana_08 ===")
# de-dup on company_id, use HQ
seen=set(); comp_hq={}
for r in ROWS:
    if r['company_id'] not in seen:
        comp_hq[r['company_id']]=r['headquarters'].strip(); seen.add(r['company_id'])
hq=Counter(h for h in comp_hq.values() if h)
print(f"unique companies with HQ recorded: {sum(hq.values())} of {len(comp_hq)}")
# group bay area
bay={'Palo Alto','Mountain View','Menlo Park','Stanford','Cupertino','Sunnyvale','Santa Clara',
     'San Jose','Redwood City','Los Altos','Foster City','San Mateo','Fremont'}
sf=Counter();
groups=Counter()
for h,n in hq.items():
    if h=='San Francisco': groups['San Francisco']+=n
    elif h in bay: groups['Rest of Bay Area']+=n
    else: groups['Elsewhere']+=n
print("top HQ cities:")
for h,n in hq.most_common(12):
    print(f"  {h}: {n}")
print("grouped:")
for g,n in groups.most_common():
    print(f"  {g}: {n}")

# --- ana_09: Founder type breakdown (the 'founded by is broad' caveat, Musk example) ---
print("\n=== ana_09 ===")
# classify Musk's 15
musk = sorted(set(fcompanies['Elon Musk']))
print(f"Elon Musk's {len(musk)} foundings (raw P112):")
for c in musk: print(f"  {c}")
# rough classify
noncompany_kw=['PAC','Party','School','Institute','Foundation','Fund','Forum','Prize','Review','Fellowship',
               'Bureau','Commission','Committee','Googleplex','Institution']
def is_noncompany(name):
    return any(k.lower() in name.lower() for k in noncompany_kw)
# across all unique companies
seen=set(); allnames=[]
for r in ROWS:
    if r['company_id'] not in seen:
        allnames.append(r['company']); seen.add(r['company_id'])
nc=sum(1 for n in allnames if is_noncompany(n))
print(f"\nof {len(allnames)} unique entities, ~{nc} look like non-companies (PAC/foundation/school/fund/prize/institute)")
print(f"~{len(allnames)-nc} look like actual companies")

# --- ana_10: The famous lineage timeline (named landmark companies) ---
print("\n=== ana_10 ===")
landmarks=['Hewlett-Packard','Litton Industries','Sun Microsystems','Cisco','Silicon Graphics',
           'Logitech','Intuit','Yahoo','Nvidia','Google','LinkedIn','PayPal','YouTube','Tesla',
           'Palantir Technologies','SpaceX','Instagram','Snapchat','Neuralink','OpenAI','Coursera',
           'Robinhood','DoorDash']
comp_year_name={}
seen=set()
for r in ROWS:
    if r['company_id'] not in seen and r['founded_year'].strip().isdigit():
        comp_year_name[r['company']]=int(r['founded_year']); seen.add(r['company_id'])
hits=[]
for lm in landmarks:
    for cn,y in comp_year_name.items():
        if lm.lower() in cn.lower():
            hits.append((y,cn)); break
hits.sort()
for y,cn in hits:
    print(f"{y}  {cn}")
