"""Demographic 'optimism' analysis: who reads probability words higher?"""
import pandas as pd
import numpy as np

DATA = '/Users/forrest/Desktop/data2story-skill/data/likely'
aj = pd.read_csv(f'{DATA}/absolute_judgements.csv')
rm = pd.read_csv(f'{DATA}/respondent_metadata.csv')

# Build a per-respondent "optimism" score: their average term-centered value
# (positive = reads phrases as higher prob than average; negative = lower)
term_mean = aj.groupby('term')['probability'].transform('mean')
aj = aj.assign(centered=aj['probability'] - term_mean)
resp_opt = aj.groupby('response_id')['centered'].mean().rename('optimism')
df = rm.merge(resp_opt, on='response_id')

def grp_report(col, minn=30):
    g = df.groupby(col)['optimism'].agg(['mean','count'])
    g = g[g['count'] >= minn].sort_values('mean', ascending=False)
    return g

# --- ana_12: Optimism by country (top countries) ---
print("=== ana_12 ===")
gc = grp_report('country_of_residence', minn=40)
print("Optimism (term-centered mean, pp above/below global avg) by country (n>=40):")
print(gc.round(2).to_string())
# US vs UK ratio on raw values (det_04 benchmark: ~1.03x)
us = aj.merge(rm[['response_id','country_of_residence']],on='response_id')
us_m = us[us.country_of_residence=='United States']['probability'].mean()
uk_m = us[us.country_of_residence=='United Kingdom']['probability'].mean()
print(f"US mean raw value {us_m:.2f}, UK mean raw value {uk_m:.2f}, ratio US/UK = {us_m/uk_m:.3f}")

# --- ana_13: Optimism by age band ---
print("=== ana_13 ===")
order_age = ['Under 18','18-24','25-34','35-44','45-54','55-64','65-74','75+']
ga = df.groupby('age_band')['optimism'].agg(['mean','count']).reindex(order_age).dropna()
print(ga.round(2).to_string())

# --- ana_14: Optimism by English background ---
print("=== ana_14 ===")
ge = grp_report('english_background', minn=30)
print(ge.round(2).to_string())

# --- ana_15: Optimism by education ---
print("=== ana_15 ===")
edu_order = ['Less than high school','High school','Some college','Bachelor','Postgraduate']
gd = df.groupby('education_level')['optimism'].agg(['mean','count']).reindex(edu_order).dropna()
print(gd.round(2).to_string())

print("=== summary spread ===")
print(f"Country optimism spread (max-min, n>=40): {gc['mean'].max()-gc['mean'].min():.2f} pp")
print(f"English-background spread: {ge['mean'].max()-ge['mean'].min():.2f} pp")
