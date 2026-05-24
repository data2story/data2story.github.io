"""Stage 2 Analyst — appearance distributions across all 234 members.

Computes hair color, frosted-tip rate, hair length/style, eyes,
skin tone, facial hair, accessories, top/bottom style, jacket/shirt/bottom color,
height stats, instruments, etc. Feeds analyst.json items ana_06 .. ana_15.
"""
import csv
import os
from collections import Counter

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/12_boybands"

with open(os.path.join(DATA_DIR, "boys.csv"), encoding="utf-8") as f:
    boys = list(csv.DictReader(f))

N = len(boys)


def show(label, counter, top=None):
    items = counter.most_common(top)
    for k, v in items:
        print(f"  {k!r:35s}  {v:3d}  ({v/N*100:.1f}%)")


# --- ana_06: hair color across all members ---
print("=== ana_06 ===")
hc = Counter(r["hair_color"] for r in boys)
show("hair_color", hc)
black_n = hc["black"]
brown_n = hc["brown"]
blonde_n = hc["blonde"]
print(f"\n black + brown share: {(black_n + brown_n)/N*100:.1f}%")
print(f" blonde-only share: {blonde_n/N*100:.1f}%")
unusual = sum(v for k, v in hc.items() if k in ("red", "green", "blue", "silver", "strawberry blonde"))
print(f" exotic colors total: {unusual} ({unusual/N*100:.1f}%)")

# --- ana_07: frosted tips ---
print("\n=== ana_07 ===")
hf = Counter(r["hair_frosted"] for r in boys)
show("hair_frosted", hf)
yes = hf["yes"]
exotic = hf.get("red", 0) + hf.get("green", 0)
print(f"\n yes-frosted: {yes}/{N} = {yes/N*100:.1f}%")
print(f" red/green tips: {exotic}/{N} = {exotic/N*100:.1f}%")

# --- ana_08: hair length + style ---
print("\n=== ana_08 ===")
hl = Counter(r["hair_length"] for r in boys)
print("hair_length:")
show("hair_length", hl)
hs = Counter(r["hair_style"] for r in boys)
print("\nhair_style top 10:")
show("hair_style", hs, 10)
short_pct = hl["short"] / N * 100
print(f"\n short-hair share: {short_pct:.1f}%")

# --- ana_09: eyes ---
print("\n=== ana_09 ===")
ec = Counter(r["eyes"].lower() for r in boys)
show("eyes", ec)

# --- ana_10: skin tone distribution ---
print("\n=== ana_10 ===")
sk = Counter(r["skin"] for r in boys)
order = ["light", "medium-light", "medium", "medium-dark", "dark"]
for k in order:
    v = sk.get(k, 0)
    print(f"  {k:14s}  {v:3d}  ({v/N*100:.1f}%)")
light = sk["light"] + sk["medium-light"]
dark = sk["medium-dark"] + sk["dark"]
print(f"\n light-or-medium-light: {light/N*100:.1f}%")
print(f" medium-dark-or-dark:   {dark/N*100:.1f}%")

# --- ana_11: facial hair ---
print("\n=== ana_11 ===")
fh = Counter((r["facial_hair"] or "(none)") for r in boys)
show("facial_hair", fh, 10)
none = fh["(none)"]
print(f"\n clean-shaven: {none}/{N} = {none/N*100:.1f}%")

# --- ana_12: accessories ---
print("\n=== ana_12 ===")
acc = Counter((r["accessories"] or "(none)") for r in boys)
show("accessories", acc, 12)
none = acc["(none)"]
# count individual accessory tokens
from itertools import chain
tokens = Counter(t.strip() for r in boys if r["accessories"] for t in r["accessories"].split(","))
print("\n token totals:")
for k, v in tokens.most_common(10):
    print(f"  {k!r:25s}  {v:3d}")
print(f"\n (none) accessory share: {none/N*100:.1f}%")
ear = tokens.get("earrings", 0)
neck = tokens.get("necklace", 0)
print(f" earrings token: {ear} ({ear/N*100:.1f}%)")
print(f" necklace token: {neck} ({neck/N*100:.1f}%)")

# --- ana_13: top + bottom style ---
print("\n=== ana_13 ===")
ts = Counter(r["top_style"] for r in boys)
print("top_style top 10:")
show("top_style", ts, 10)
bs = Counter(r["bottom_style"] for r in boys)
print("\nbottom_style:")
show("bottom_style", bs)
suits = sum(v for k, v in ts.items() if "suit jacket" in k or "tuxedo" in k.lower())
print(f"\n suit-jacket-style tops: {suits} ({suits/N*100:.1f}%)")
dress_pants = bs.get("dress pants", 0)
print(f" dress pants share: {dress_pants/N*100:.1f}%")
jeans = bs.get("jeans", 0) + bs.get("acid wash jeans", 0)
print(f" jeans (incl. acid wash): {jeans/N*100:.1f}%")

# --- ana_14: instruments ---
print("\n=== ana_14 ===")
ic = Counter((r["instrument"] or "(none)") for r in boys)
show("instrument", ic)
no_instrument = ic["(none)"]
print(f"\n no instrument visible: {no_instrument}/{N} = {no_instrument/N*100:.1f}%")
plays_anything = N - no_instrument
print(f" plays an instrument:  {plays_anything}/{N} = {plays_anything/N*100:.1f}%")

# --- ana_15: shirt + jacket + bottom color ---
print("\n=== ana_15 ===")
sc = Counter(r["shirt_color"] for r in boys)
print("shirt_color top 8:")
show("shirt_color", sc, 8)
jc = Counter((r["jacket_color"] or "(no jacket)") for r in boys)
print("\njacket_color top 8:")
show("jacket_color", jc, 8)
bc = Counter(r["bottom_color"] for r in boys)
print("\nbottom_color top 8:")
show("bottom_color", bc, 8)

# --- ana_16: height stats ---
print("\n=== ana_16 ===")
heights = [int(r["height"]) for r in boys if r["height"]]
print(f"  members with height: {len(heights)}/{N}")
if heights:
    h_mean = sum(heights) / len(heights)
    h_med = sorted(heights)[len(heights) // 2]
    print(f"  mean: {h_mean:.2f} in ({h_mean*2.54:.1f} cm)")
    print(f"  median: {h_med} in ({h_med*2.54:.1f} cm)")
    print(f"  min: {min(heights)} in / max: {max(heights)} in")
# US adult male median height ~ 69 in (175 cm) per CDC NHANES
print("\n  US adult male median height (CDC): 69.1 in / 175.4 cm")
