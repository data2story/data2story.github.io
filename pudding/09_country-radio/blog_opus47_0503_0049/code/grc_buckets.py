"""
grc_buckets.py — Gold / Recurrent / Current programming-bucket analysis.

Country radio classifies every song into:
  G = Gold      — established hit, often years/decades old
  R = Recurrent — rotated off "current" recently, still played
  C = Current   — actively being promoted to chart
"""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"
summary = pd.read_csv(os.path.join(DATA_DIR, "output", "summary.csv"))

# --- ana_09: Gold/Recurrent/Current totals for women vs men ---
print("=== ana_09 ===")
buckets = [("G", "Gold"), ("R", "Recurrent"), ("C", "Current")]

women_total = 0
men_total = 0
women_b2b_total = 0
men_b2b_total = 0

print("Women's plays and b2bs by programming bucket:")
women_breakdown = {}
for code, label in buckets:
    plays = int(summary[f"{code}womenSongs_COUNT"].sum())
    b2b = int(summary[f"b2b{code}womenSongs_COUNT"].sum())
    women_breakdown[code] = {"plays": plays, "b2b": b2b}
    women_total += plays
    women_b2b_total += b2b
    print(f"  {code} {label:9s}  plays={plays:>5,}  b2b={b2b:>4}")

print(f"  TOTAL          plays={women_total:,}  b2b={women_b2b_total}")

print("\nMen's plays and b2bs by programming bucket:")
men_breakdown = {}
for code, label in buckets:
    plays = int(summary[f"{code}menSongs_COUNT"].sum())
    b2b = int(summary[f"b2b{code}menSongs_COUNT"].sum())
    men_breakdown[code] = {"plays": plays, "b2b": b2b}
    men_total += plays
    men_b2b_total += b2b
    print(f"  {code} {label:9s}  plays={plays:>6,}  b2b={b2b:>5}")
print(f"  TOTAL          plays={men_total:,}  b2b={men_b2b_total}")

# --- ana_10: Share of women's plays / b2bs that are Gold ---
print("\n=== ana_10 ===")
print("Composition of women's plays by bucket:")
for code, label in buckets:
    p = women_breakdown[code]["plays"]
    print(f"  {code} {label:9s}  {p:>5,}  {p/women_total*100:5.2f}% of women's plays")
print("\nComposition of women's BACK-TO-BACKs by bucket:")
for code, label in buckets:
    b = women_breakdown[code]["b2b"]
    print(f"  {code} {label:9s}  {b:>5}  {b/women_b2b_total*100:5.2f}% of women's b2b plays")

print("\nComposition of MEN's plays by bucket (for comparison):")
for code, label in buckets:
    p = men_breakdown[code]["plays"]
    print(f"  {code} {label:9s}  {p:>6,}  {p/men_total*100:5.2f}% of men's plays")
print("\nComposition of MEN's BACK-TO-BACKs by bucket:")
for code, label in buckets:
    b = men_breakdown[code]["b2b"]
    print(f"  {code} {label:9s}  {b:>5}  {b/men_b2b_total*100:5.2f}% of men's b2b plays")

# Headline contrast
women_gold_share_b2b = women_breakdown["G"]["b2b"] / women_b2b_total * 100
men_gold_share_b2b = men_breakdown["G"]["b2b"] / men_b2b_total * 100
women_current_share_b2b = women_breakdown["C"]["b2b"] / women_b2b_total * 100
men_current_share_b2b = men_breakdown["C"]["b2b"] / men_b2b_total * 100
print(f"\nGold share of women's b2b: {women_gold_share_b2b:.1f}%  vs men's b2b Gold share: {men_gold_share_b2b:.1f}%")
print(f"Current share of women's b2b: {women_current_share_b2b:.1f}%  vs men's b2b Current share: {men_current_share_b2b:.1f}%")
