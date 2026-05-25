#!/usr/bin/env python3
"""
MTUS Harmonized Aggregated File (HAF) analysis.
Reads ONLY MTUS_haf.dta, using column subsets (never all 160 cols at once).
All population means are PROPWT-weighted. Good-quality diaries only (propwt>0).
Activity totals are in minutes per day; each diary day sums to 1440 min.
"""
import pandas as pd
import numpy as np

DTA = "/Users/forrest/Desktop/data2story-skill/data/mtus/MTUS_haf.dta"

ISO2NAME = {
    'US':'United States','KR':'South Korea','IT':'Italy','NL':'Netherlands','UK':'United Kingdom',
    'ES':'Spain','CA':'Canada','FR':'France','HU':'Hungary','ZA':'South Africa','FI':'Finland',
    'BE':'Belgium','AT':'Austria','DE':'Germany','NO':'Norway','BG':'Bulgaria','DK':'Denmark',
    'AR':'Argentina','SI':'Slovenia','IL':'Israel','PL':'Poland','AM':'Armenia','RS':'Serbia',
    'CZ':'Czech Republic','PE':'Peru'
}

def wmean(values, weights):
    values = np.asarray(values, float); weights = np.asarray(weights, float)
    m = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if m.sum() == 0: return np.nan
    return np.average(values[m], weights=weights[m])

# Activity columns (25-category harmonized totals, minutes/day)
ACT = ['sleep','eatdrink','selfcare','paidwork','educatn','foodprep','cleanetc','maintain',
       'shopserv','garden','petcare','eldcare','pkidcare','ikidcare','religion','volorgwk',
       'commute','travel','sportex','tvradio','read','compint','goout','leisure']

print("Loading column subset (demographics + activities)...")
cols = ['isocountry','survey','year','sex','age','emp','propwt'] + ACT
df = pd.read_stata(DTA, columns=cols, convert_categoricals=False)
print("rows loaded:", len(df))

# Restrict to good-quality diaries (propwt>0) and valid sex
df = df[(df['propwt'] > 0) & df['sex'].isin([1,2])].copy()
# Activity totals: -9 indicates not separately measured; treat as NaN, but for the
# coarse 25-category file these are 0-1440 with no -9. Clip negatives to NaN to be safe.
for c in ACT:
    df.loc[df[c] < 0, c] = np.nan
print("good-quality rows:", len(df))

# Derived composite measures (minutes/day)
df['housework'] = df[['foodprep','cleanetc','maintain','shopserv','garden','petcare']].sum(axis=1)
df['childcare'] = df[['pkidcare','ikidcare']].sum(axis=1)
df['unpaid']    = df['housework'] + df['childcare'] + df['eldcare']
df['screen']    = df['tvradio'] + df['compint']
df['totalwork'] = df['paidwork'] + df['unpaid']
df['cname'] = df['isocountry'].map(ISO2NAME)

def hm(mins):
    mins = float(mins); h = int(mins//60); m = int(round(mins-h*60))
    if m==60: h+=1; m=0
    return f"{h}h{m:02d}m"

# =====================================================================
# --- ana_01: The gender gap in unpaid vs paid work (headline) ---
print("=== ana_01 ===")
gp = {}
for s,lab in [(1,'Men'),(2,'Women')]:
    sub = df[df['sex']==s]
    gp[lab] = {
        'paid': wmean(sub['paidwork'], sub['propwt']),
        'unpaid': wmean(sub['unpaid'], sub['propwt']),
        'housework': wmean(sub['housework'], sub['propwt']),
        'childcare': wmean(sub['childcare'], sub['propwt']),
        'total': wmean(sub['totalwork'], sub['propwt']),
    }
for lab in ['Men','Women']:
    g=gp[lab]
    print(f"{lab}: paid={g['paid']:.1f} ({hm(g['paid'])}) unpaid={g['unpaid']:.1f} ({hm(g['unpaid'])}) "
          f"housework={g['housework']:.1f} childcare={g['childcare']:.1f} total={g['total']:.1f} ({hm(g['total'])})")
print(f"Unpaid gap (W-M): {gp['Women']['unpaid']-gp['Men']['unpaid']:.1f} min; ratio W/M = {gp['Women']['unpaid']/gp['Men']['unpaid']:.2f}")
print(f"Paid gap (M-W):   {gp['Men']['paid']-gp['Women']['paid']:.1f} min")
print(f"Total work gap (W-M): {gp['Women']['total']-gp['Men']['total']:.1f} min")

# =====================================================================
# --- ana_02: The average day, all people, weighted (24h budget) ---
print("=== ana_02 ===")
day = {}
report_cats = [('sleep','Sleep'),('paidwork','Paid work'),('housework','Housework'),
               ('childcare','Childcare'),('eatdrink','Eating & drinking'),('selfcare','Personal care'),
               ('educatn','Education'),('commute','Commute'),('travel','Other travel'),
               ('screen','TV, radio & computer'),('read','Reading'),('sportex','Sport & exercise'),
               ('goout','Going out'),('leisure','Other leisure')]
for col,lab in report_cats:
    day[lab] = wmean(df[col], df['propwt'])
tot = sum(day.values())
for lab in [l for _,l in report_cats]:
    print(f"{lab:24s} {day[lab]:6.1f} min  ({hm(day[lab])})")
print(f"Sum of reported categories: {tot:.1f} min of 1440")

# =====================================================================
# --- ana_03: Who sleeps most / least (country ranking) ---
print("=== ana_03 ===")
rows=[]
for iso,sub in df.groupby('isocountry'):
    rows.append((ISO2NAME.get(iso,iso), iso, wmean(sub['sleep'],sub['propwt']), len(sub)))
sleep_rank = sorted(rows, key=lambda r:-r[2])
for name,iso,v,n in sleep_rank:
    print(f"{name:16s} {v:6.1f} ({hm(v)})  n={n}")

# =====================================================================
# --- ana_04: Who works most (paid work, country ranking) ---
print("=== ana_04 ===")
rows=[]
for iso,sub in df.groupby('isocountry'):
    rows.append((ISO2NAME.get(iso,iso), iso, wmean(sub['paidwork'],sub['propwt']), len(sub)))
work_rank = sorted(rows, key=lambda r:-r[2])
for name,iso,v,n in work_rank:
    print(f"{name:16s} {v:6.1f} ({hm(v)})  n={n}")

# =====================================================================
# --- ana_05: The housework gender gap by country ---
print("=== ana_05 ===")
rows=[]
for iso,sub in df.groupby('isocountry'):
    m=sub[sub['sex']==1]; w=sub[sub['sex']==2]
    wm=wmean(w['unpaid'],w['propwt']); mm=wmean(m['unpaid'],m['propwt'])
    rows.append((ISO2NAME.get(iso,iso), iso, wm, mm, wm-mm, len(sub)))
gap_rank = sorted(rows, key=lambda r:-r[4])
for name,iso,wmv,mmv,gap,n in gap_rank:
    print(f"{name:16s} W={wmv:6.1f} M={mmv:6.1f} gap={gap:6.1f} ({hm(gap)})  n={n}")

# =====================================================================
# --- ana_06: Rise of computer/ICT time vs TV/radio over decades ---
print("=== ana_06 ===")
df['decade'] = (df['year']//10*10).astype('Int64')
rows=[]
for dec,sub in df.groupby('decade'):
    if pd.isna(dec) or len(sub)<500: continue
    rows.append((int(dec), wmean(sub['tvradio'],sub['propwt']), wmean(sub['compint'],sub['propwt']),
                 wmean(sub['screen'],sub['propwt']), len(sub)))
rows=sorted(rows)
for dec,tv,comp,scr,n in rows:
    print(f"{dec}s  TV/radio={tv:6.1f}  computer={comp:6.1f}  total screen={scr:6.1f}  n={n}")

# =====================================================================
# --- ana_07: The average day, then vs now (1960s/70s vs 2010s/20s) ---
print("=== ana_07 ===")
early = df[df['year']<1980]; late = df[df['year']>=2010]
chg_cats=[('sleep','Sleep'),('paidwork','Paid work'),('housework','Housework'),
          ('tvradio','TV & radio'),('compint','Computer & internet'),('eatdrink','Eating'),
          ('commute','Commute'),('sportex','Sport & exercise'),('childcare','Childcare')]
print(f"early n={len(early)} (yr<1980); late n={len(late)} (yr>=2010)")
for col,lab in chg_cats:
    e=wmean(early[col],early['propwt']); l=wmean(late[col],late['propwt'])
    print(f"{lab:22s} {e:6.1f} -> {l:6.1f}  ({l-e:+.1f})")

# =====================================================================
# --- ana_08: Gender convergence in unpaid work across decades ---
print("=== ana_08 ===")
rows=[]
for dec,sub in df.groupby('decade'):
    if pd.isna(dec) or len(sub)<500: continue
    m=sub[sub['sex']==1]; w=sub[sub['sex']==2]
    wm=wmean(w['unpaid'],w['propwt']); mm=wmean(m['unpaid'],m['propwt'])
    rows.append((int(dec), wm, mm, wm-mm, len(sub)))
rows=sorted(rows)
for dec,wmv,mmv,gap,n in rows:
    print(f"{dec}s  W={wmv:6.1f}  M={mmv:6.1f}  gap={gap:6.1f}  n={n}")

# =====================================================================
# --- ana_09: Total work near-invariance (paid+unpaid by sex by decade) ---
print("=== ana_09 ===")
rows=[]
for dec,sub in df.groupby('decade'):
    if pd.isna(dec) or len(sub)<500: continue
    m=sub[sub['sex']==1]; w=sub[sub['sex']==2]
    rows.append((int(dec), wmean(w['totalwork'],w['propwt']), wmean(m['totalwork'],m['propwt']),
                 wmean(sub['totalwork'],sub['propwt']), len(sub)))
rows=sorted(rows)
for dec,wt,mt,allt,n in rows:
    print(f"{dec}s  W_total={wt:6.1f}  M_total={mt:6.1f}  all={allt:6.1f}  n={n}")
