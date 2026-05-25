#!/usr/bin/env python3
"""Humanity's Last Exam (cais/hle) — full reproducible analysis over hle_questions.csv.
Run from the data directory: python3 analyze.py  (expects hle_questions.csv in cwd or ../data/hle)
Each finding prints '=== ana_xx ===' and matches an item in analyst.json.
"""
import pandas as pd
import os

# locate CSV
CANDIDATES = ["hle_questions.csv",
              os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "hle", "hle_questions.csv"),
              "/Users/forrest/Desktop/data2story-skill/data/hle/hle_questions.csv"]
CSV = next(p for p in CANDIDATES if os.path.exists(p))
df = pd.read_csv(CSV)
N = len(df)

# normalise author field: empty/blank -> NaN
df["author_name"] = df["author_name"].astype(str).str.strip()
df.loc[df["author_name"].isin(["", "nan", "None"]), "author_name"] = pd.NA

# ---------------------------------------------------------------------------
# --- ana_01: Dataset shape & integrity ---
print("=== ana_01 ===")
print(f"rows={N} cols={df.shape[1]} columns={list(df.columns)}")
miss = df.isna().sum()
print("missing per column:")
for c in df.columns:
    print(f"  {c}: {int(miss[c])}")
named = df["author_name"].notna().sum()
print(f"named authors present: {named} ({named/N*100:.1f}%)  anonymous/blank: {N-named} ({(N-named)/N*100:.1f}%)")

# --- ana_02: Category distribution vs official benchmark ---
print("=== ana_02 ===")
OFFICIAL = {"Math":41,"Biology/Medicine":11,"Computer Science/AI":10,"Physics":9,
            "Humanities/Social Science":9,"Other":9,"Chemistry":7,"Engineering":4}
vc = df["category"].value_counts()
for cat, cnt in vc.items():
    pct = cnt/N*100
    off = OFFICIAL.get(cat)
    print(f"  {cat}: {cnt} ({pct:.1f}%)   official~{off}%")

# --- ana_03: Math dominance ---
print("=== ana_03 ===")
math_n = int(vc["Math"])
print(f"Math: {math_n}/{N} = {math_n/N*100:.1f}%")
others_sum = N - math_n
print(f"All 7 non-Math categories combined: {others_sum} ({others_sum/N*100:.1f}%)")
second = vc.index[1]
print(f"Math is {math_n/int(vc[second]):.1f}x the next-largest category ({second}: {int(vc[second])})")

# --- ana_04: answer_type split overall ---
print("=== ana_04 ===")
at = df["answer_type"].value_counts()
for k,v in at.items():
    print(f"  {k}: {v} ({v/N*100:.1f}%)")

# --- ana_05: has_image split overall ---
print("=== ana_05 ===")
im = df["has_image"].value_counts()
for k,v in im.items():
    print(f"  {k}: {v} ({v/N*100:.1f}%)")

# --- ana_06: image rate by category ---
print("=== ana_06 ===")
g = df.groupby("category")["has_image"].apply(lambda s: (s=="yes").mean()*100).sort_values(ascending=False)
cnts = df.groupby("category").apply(lambda d: (d["has_image"]=="yes").sum())
for cat in g.index:
    print(f"  {cat}: {cnts[cat]} images / {int(vc[cat])} = {g[cat]:.1f}%")
overall_img = (df["has_image"]=="yes").mean()*100
print(f"  OVERALL image rate: {overall_img:.1f}%")

# --- ana_07: answer_type by category (multipleChoice share) ---
print("=== ana_07 ===")
mc = df.groupby("category")["answer_type"].apply(lambda s: (s=="multipleChoice").mean()*100).sort_values(ascending=False)
mc_cnt = df.groupby("category").apply(lambda d: (d["answer_type"]=="multipleChoice").sum())
for cat in mc.index:
    print(f"  {cat}: {int(mc_cnt[cat])} MC / {int(vc[cat])} = {mc[cat]:.1f}% multipleChoice")
print(f"  OVERALL multipleChoice: {(df['answer_type']=='multipleChoice').mean()*100:.1f}%")

# --- ana_08: subject long tail ---
print("=== ana_08 ===")
sub = df["raw_subject"].value_counts()
print(f"distinct raw_subjects: {df['raw_subject'].nunique()}")
print("top 15 subjects:")
for s,c in sub.head(15).items():
    print(f"  {s}: {c} ({c/N*100:.1f}%)")
singletons = (sub==1).sum()
print(f"subjects represented by exactly 1 question: {singletons}")
top1_share = sub.iloc[0]/N*100
print(f"#1 subject '{sub.index[0]}' alone = {top1_share:.1f}% of all questions")
# share covered by long tail (subjects with <=5 q)
tail = sub[sub<=5]
print(f"subjects with <=5 questions: {len(tail)} subjects covering {tail.sum()} questions ({tail.sum()/N*100:.1f}%)")

# --- ana_09: author breadth & concentration ---
print("=== ana_09 ===")
auth = df["author_name"].value_counts()
print(f"distinct named authors: {df['author_name'].nunique()}")
print(f"questions with a named author: {df['author_name'].notna().sum()}")
print("top 10 contributors:")
for a,c in auth.head(10).items():
    print(f"  {a}: {c}")
one_q = (auth==1).sum()
print(f"contributors with exactly 1 question: {one_q} ({one_q/df['author_name'].nunique()*100:.1f}% of named authors)")
named_total = df["author_name"].notna().sum()
top10_share = auth.head(10).sum()/named_total*100
print(f"top 10 authors account for {auth.head(10).sum()} of {named_total} attributed questions ({top10_share:.1f}%)")

# --- ana_10: 'Other' category composition ---
print("=== ana_10 ===")
oth = df[df["category"]=="Other"]["raw_subject"].value_counts()
print(f"'Other' category n={len(df[df['category']=='Other'])}, distinct subjects={oth.nunique() if hasattr(oth,'nunique') else len(oth)}")
for s,c in oth.head(12).items():
    print(f"  {s}: {c}")

# --- ana_11: answer length / form for exactMatch ---
print("=== ana_11 ===")
em = df[df["answer_type"]=="exactMatch"].copy()
em["alen"] = em["answer"].astype(str).str.len()
print(f"exactMatch n={len(em)}")
print(f"answer string length: median={em['alen'].median():.0f}, mean={em['alen'].mean():.1f}, max={em['alen'].max()}")
short = (em["alen"]<=3).sum()
print(f"exactMatch answers <=3 chars (e.g. single number/letter): {short} ({short/len(em)*100:.1f}%)")
# fraction of exactMatch answers that are purely numeric-ish
import re
numeric = em["answer"].astype(str).str.match(r'^[\s\-\+\$]*[\d\.,]+\s*%?$').sum()
print(f"exactMatch answers that are a bare number: {numeric} ({numeric/len(em)*100:.1f}%)")

# --- ana_12: question text length by category (how long the prompts are) ---
print("=== ana_12 ===")
df["qlen"] = df["question"].astype(str).str.len()
ql = df.groupby("category")["qlen"].median().sort_values(ascending=False)
for cat in ql.index:
    print(f"  {cat}: median {ql[cat]:.0f} chars")
print(f"  OVERALL median question length: {df['qlen'].median():.0f} chars")
