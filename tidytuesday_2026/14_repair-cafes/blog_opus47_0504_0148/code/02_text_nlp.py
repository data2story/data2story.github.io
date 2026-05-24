"""NLP analysis of free-text fields: defect_found, failure_reasons, repair_info_source."""
import pandas as pd
import numpy as np
import re
from pathlib import Path
from collections import Counter

DATA_DIR = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday_2026/14_repair-cafes")
repairs = pd.read_csv(DATA_DIR / "repairs.csv", low_memory=False)
text = pd.read_csv(DATA_DIR / "repairs_text.csv", low_memory=False)

repairs['repaired'] = repairs['repaired'].replace({'ja': 'yes'})
df = repairs.merge(text, on='repair_id', how='left')
df['repair_date'] = pd.to_datetime(df['repair_date'], errors='coerce')
df['year'] = df['repair_date'].dt.year

# --- ana_09: failure_reasons checkbox-list distribution ---
print("=== ana_09 ===")
failed = df[df['repaired'].isin(['no', 'half'])].copy()
fr = failed['failure_reasons'].dropna().astype(str)
# Parse: list separated by ';'
all_reasons = []
for s in fr:
    parts = [p.strip() for p in re.split(r'[;|]', s) if p.strip() and p.strip().upper() != 'NA']
    all_reasons.extend(parts)
reason_counts = Counter(all_reasons)
total_failed = len(failed)
print(f"Total failed/half rows: {total_failed}")
print(f"Top 15 failure reason tags:")
for r, c in sorted(reason_counts.items(), key=lambda x: -x[1])[:15]:
    print(f"  {c:>6} ({100*c/total_failed:5.1f}%) {r}")

# --- ana_10: defect_found common phrases (English-language proxy) ---
print("\n=== ana_10 ===")
def_found = df['defect_found'].dropna().astype(str).str.lower().str.strip()
def_found = def_found[~def_found.isin(['na','n/a','-'])]
# Top exact phrases
top_defects = def_found.value_counts().head(30)
print("Top 30 raw defect phrases:")
print(top_defects.to_string())

# --- ana_11: defect themes via keyword grouping ---
print("\n=== ana_11 ===")
themes = {
    'no power / does not turn on': r'does\s*not\s*(turn\s*on|switch\s*on|start|work|power)|won.t\s*(turn\s*on|start|work|switch)|geen\s*stroom|niet\s*aan|n.allume\s*pas|kein\s*strom|werkt\s*niet|defect|out\s*of\s*order|gaat\s*niet\s*aan',
    'broken / cracked / damaged': r'broken|cracked|damaged|kapot|cassé|gebroken|broke',
    'leaking / dripping': r'\bleak|drip|lek|fuit',
    'noise / loud / strange sound': r'\bnoise|noisy|loud|geluid|maakt\s*lawaai|bruit',
    'loose / wobbly / wiggle': r'loose|wobbl|wiggle|los\b',
    'battery / charging': r'battery|batter|charge|charging|laad|accu|batterie',
    'overheats / smoking / burning': r'overheat|smoke|burn|burning|smell|brandt|brûle',
    'dirty / clogged / blocked': r'\bdirty|clog|block|verstopt|encrass',
    'won\'t spin / won\'t turn / motor': r'motor|won.t\s*spin|won.t\s*turn|draait\s*niet|tourne\s*pas',
    'screen / display issue': r'screen|display|scherm|écran|crack',
    'cable / cord / plug': r'\bcord|cable|plug|wire|kabel|snoer|stekker|cordon',
    'sewing/zipper/seam (textile)': r'zipper|seam|hem|zoom|naad|rits|fermeture|tear|rip\b',
    'sharpening (knives)': r'sharpen|sharpening|slijp',
    'clock / time / hands': r'clock|hand[s]?\s+(stuck|stop)|wijzers',
}
total_defect_rows = (~def_found.isna()).sum()
theme_counts = {}
for name, pat in themes.items():
    n = def_found.str.contains(pat, regex=True, na=False).sum()
    theme_counts[name] = n
    print(f"  {n:>7} ({100*n/total_defect_rows:5.2f}%) {name}")
print(f"Total non-NA defect_found rows: {total_defect_rows}")

# --- ana_12: GenAI vs YouTube vs traditional sources ---
print("\n=== ana_12 ===")
src = df.dropna(subset=['repair_info_source']).copy()
src['repair_info_source_l'] = src['repair_info_source'].astype(str).str.lower()
url = df.dropna(subset=['repair_info_url']).copy()
url['repair_info_url_l'] = url['repair_info_url'].astype(str).str.lower()

# Tag types
def tag_source(s):
    if 'youtube' in s or 'youtu.be' in s:
        return 'youtube'
    if any(k in s for k in ['chatgpt','chat gpt','openai','gpt-','gemini','bard','claude','copilot','perplexity','grok','generative ai','gen ai','genai','ai ','ai,','artificial intelligence']):
        return 'genai'
    if 'manual' in s or 'handleiding' in s or 'instruction' in s or 'guide' in s or 'service manual' in s:
        return 'manual'
    if 'ifixit' in s:
        return 'ifixit'
    if 'forum' in s or 'reddit' in s:
        return 'forum'
    if 'website' in s or 'site' in s or 'http' in s or 'www' in s or '.com' in s or '.nl' in s:
        return 'other_web'
    if 'experience' in s or 'own knowledge' in s or 'eigen' in s or 'expert' in s:
        return 'experience'
    if 'colleague' in s or 'collega' in s or 'friend' in s:
        return 'colleague'
    return 'other'

# Combine source + url evidence
df['_src'] = df['repair_info_source'].astype(str).str.lower().fillna('')
df['_url'] = df['repair_info_url'].astype(str).str.lower().fillna('')
df['_combo'] = df['_src'] + ' || ' + df['_url']

ai_pat = r'(chatgpt|chat\s*gpt|openai|\bgpt[- ]?[345o]|gemini|bard\b|claude|copilot|perplexity|\bgrok\b|generative\s*ai|\bgen[- ]?ai\b|artificial\s*intelligence)'
yt_pat = r'(youtube|youtu\.be)'

df['_is_ai'] = df['_combo'].str.contains(ai_pat, regex=True, na=False)
df['_is_yt'] = df['_combo'].str.contains(yt_pat, regex=True, na=False)
# A row 'used some info' if used_repair_info=='yes' or any source/url filled
df['_used_info'] = (df['used_repair_info'].astype(str).str.lower() == 'yes') | (df['repair_info_source'].notna()) | (df['repair_info_url'].notna())

print(f"Total rows: {len(df)}")
print(f"Rows with AI mention: {df['_is_ai'].sum()}")
print(f"Rows with YouTube mention: {df['_is_yt'].sum()}")

# By year
yr = df.groupby('year').agg(
    n=('repair_id','count'),
    used=('_used_info','sum'),
    yt=('_is_yt','sum'),
    ai=('_is_ai','sum')
).reset_index()
yr['yt_pct'] = 100*yr['yt']/yr['n']
yr['ai_pct'] = 100*yr['ai']/yr['n']
print(yr.to_string(index=False))

# --- ana_13: Notable AI examples (real rows) ---
print("\n=== ana_13 ===")
ai_rows = df[df['_is_ai']].copy()
print(f"Earliest AI mention: {ai_rows['repair_date'].min()}")
print(f"Latest AI mention: {ai_rows['repair_date'].max()}")
print("Sample AI source values:")
for v in ai_rows['repair_info_source'].dropna().unique()[:25]:
    print(f"  - {v}")

# --- ana_14: Failure reasons by category (where do parts run out most?) ---
print("\n=== ana_14 ===")
parts_pat = r'(spare\s*part|part\s*not\s*available|part.*expensive|reserveonderdeel|reserveonderdelen|onderdeel\s*niet|pieces?\s*détachées?|onderdelen)'
df['_no_part'] = df['failure_reasons'].astype(str).str.lower().str.contains(parts_pat, regex=True, na=False)
no_part_by_cat = df.groupby('category').agg(
    failed=('repaired', lambda x: (x.isin(['no','half'])).sum()),
    no_part=('_no_part','sum'),
    n=('repair_id','count')
).reset_index()
no_part_by_cat['no_part_pct_of_failed'] = 100*no_part_by_cat['no_part']/no_part_by_cat['failed'].replace(0, np.nan)
no_part_by_cat['no_part_pct_of_n'] = 100*no_part_by_cat['no_part']/no_part_by_cat['n']
print(no_part_by_cat.sort_values('no_part_pct_of_n', ascending=False).round(2).to_string(index=False))

# --- ana_15: Repairability (1-10) → success rate correlation ---
print("\n=== ana_15 ===")
have = df.dropna(subset=['repairability']).copy()
have['success'] = (have['repaired'] == 'yes').astype(int)
by_score = have.groupby('repairability').agg(success_rate=('success','mean'), n=('success','size')).reset_index()
by_score['success_rate'] *= 100
print(by_score.round(2).to_string(index=False))

# --- ana_16: Brand-level success for top-volume brands ---
print("\n=== ana_16 ===")
# Restrict to one common product type for fairness: Vacuum cleaners
for product in ['Vacuum cleaner', 'Coffee maker']:
    sub = df[df['kind_of_product'] == product]
    g = sub.groupby('brand').agg(n=('repair_id','count'), yes=('repaired', lambda x: (x=='yes').sum())).reset_index()
    g = g[g['n'] >= 100]
    g['success_pct'] = 100*g['yes']/g['n']
    g = g.sort_values('success_pct', ascending=False)
    print(f"\n--- {product} (brands with n>=100) ---")
    print(g[['brand','n','success_pct']].round(2).to_string(index=False))

# --- ana_17: Country-level success rate ---
print("\n=== ana_17 ===")
g = df.groupby('country').agg(n=('repair_id','count'),
                                yes=('repaired', lambda x:(x=='yes').sum()),
                                half=('repaired', lambda x:(x=='half').sum())).reset_index()
g = g[g['n'] >= 100]
g['success_pct'] = 100*g['yes']/g['n']
g['success_or_partial_pct'] = 100*(g['yes']+g['half'])/g['n']
g = g.sort_values('success_pct', ascending=False)
print(g.round(2).to_string(index=False))
