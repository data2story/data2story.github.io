"""Stage 2 Analyst — coded uniform color combos.

Builds the most common shirt+jacket+bottom-color combos to surface the
'unofficial uniform' of pop boy band videos.
"""
import csv
import os
from collections import Counter

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/12_boybands"

with open(os.path.join(DATA_DIR, "boys.csv"), encoding="utf-8") as f:
    boys = list(csv.DictReader(f))

# --- ana_27: shirt color + bottom color (top combos) ---
print("=== ana_27 ===")
combo = Counter((r["shirt_color"], r["bottom_color"]) for r in boys)
print(f"Total members: {len(boys)}, distinct shirt-bottom combos: {len(combo)}")
print("Top 10 shirt+bottom combos:")
for (s, b), n in combo.most_common(10):
    print(f"  {s!r:18s} + {b!r:14s}  {n:3d}  ({n/len(boys)*100:.1f}%)")

# --- ana_28: monochrome members ---
print("\n=== ana_28 ===")
mono_black = sum(1 for r in boys if r["shirt_color"] == "black" and r["bottom_color"] == "black")
mono_white = sum(1 for r in boys if r["shirt_color"] == "white" and r["bottom_color"] == "black")  # white tee navy/black
white_navy = sum(1 for r in boys if r["shirt_color"] == "white" and r["bottom_color"] == "navy blue")
black_navy = sum(1 for r in boys if r["shirt_color"] == "black" and r["bottom_color"] == "navy blue")
white_black = sum(1 for r in boys if r["shirt_color"] == "white" and r["bottom_color"] == "black")
print(f"  all black (shirt+bottom): {mono_black} ({mono_black/len(boys)*100:.1f}%)")
print(f"  white shirt + navy bottom: {white_navy} ({white_navy/len(boys)*100:.1f}%)")
print(f"  white shirt + black bottom: {white_black} ({white_black/len(boys)*100:.1f}%)")
print(f"  black shirt + navy bottom: {black_navy} ({black_navy/len(boys)*100:.1f}%)")
two_color_uniform = mono_black + white_navy + white_black + black_navy
print(f"  black/white/navy uniform total: {two_color_uniform}/{len(boys)} ({two_color_uniform/len(boys)*100:.1f}%)")
