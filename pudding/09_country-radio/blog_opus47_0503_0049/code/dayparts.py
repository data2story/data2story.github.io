"""
dayparts.py — Daypart distribution of women's vs men's plays and back-to-backs.

Dayparts (from The Pudding's coding):
  OVN  midnight - 6 a.m.    (overnight)
  AMD  6 a.m.  - 10 a.m.    (morning drive)
  MID  10 a.m. - 3 p.m.     (midday)
  PMD  3 p.m.  - 7 p.m.     (afternoon drive)
  EVE  7 p.m.  - midnight   (evening)
"""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/09_country-radio"
summary = pd.read_csv(os.path.join(DATA_DIR, "output", "summary.csv"))

dayparts = ["OVN", "AMD", "MID", "PMD", "EVE"]
dayparts_label = {
    "OVN": "Overnight (12am-6am)",
    "AMD": "Morning drive (6am-10am)",
    "MID": "Midday (10am-3pm)",
    "PMD": "Afternoon drive (3pm-7pm)",
    "EVE": "Evening (7pm-12am)",
}

# --- ana_05: Where women's plays land in the day ---
print("=== ana_05 ===")
total_women = summary["onlyWomenSongs_COUNT"].sum()
women_by_part = {}
for dp in dayparts:
    col = f"{dp}womenSongs_COUNT"
    women_by_part[dp] = summary[col].sum()
print(f"Total women plays: {total_women:,}")
women_total_check = sum(women_by_part.values())
print(f"Total via daypart cols: {women_total_check:,}")
print()
print("Women's plays by daypart (share of women's plays):")
for dp in dayparts:
    n = women_by_part[dp]
    print(f"  {dp} {dayparts_label[dp]:30s}  {n:>5,}  {n/total_women*100:5.2f}%")

# --- ana_06: Where women's back-to-backs land ---
print("\n=== ana_06 ===")
total_b2b = summary["b2bWomenSongs_COUNT"].sum()
b2b_by_part = {}
for dp in dayparts:
    col = f"b2b{dp}womenSongs_COUNT"
    b2b_by_part[dp] = summary[col].sum()
print(f"Total women b2b plays: {total_b2b}")
print()
print("Women's BACK-TO-BACK plays by daypart (share of women's b2b):")
for dp in dayparts:
    n = b2b_by_part[dp]
    print(f"  {dp} {dayparts_label[dp]:30s}  {n:>5}  {n/total_b2b*100:5.2f}%")

# Concentration in graveyard (OVN + EVE)
gy = b2b_by_part["OVN"] + b2b_by_part["EVE"]
print(f"\nGraveyard concentration (OVN + EVE) of women's b2b: {gy} of {total_b2b}  ({gy/total_b2b*100:.1f}%)")
# line ~50

# --- ana_07: Men's daypart distribution for comparison ---
print("\n=== ana_07 ===")
total_men = summary["onlyMenSongs_COUNT"].sum()
men_by_part = {}
for dp in dayparts:
    col = f"{dp}menSongs_COUNT"
    men_by_part[dp] = summary[col].sum()
print("Men's plays by daypart (share of men's plays):")
for dp in dayparts:
    n = men_by_part[dp]
    print(f"  {dp} {dayparts_label[dp]:30s}  {n:>6,}  {n/total_men*100:5.2f}%")

# Drive-time share comparison
women_drive = women_by_part["AMD"] + women_by_part["PMD"]
men_drive = men_by_part["AMD"] + men_by_part["PMD"]
print(f"\nWomen's share in drive-time slots (AMD+PMD): {women_drive/(women_drive+men_drive)*100:.2f}%")
print(f"Women's share in graveyard slots (OVN+EVE):  {(women_by_part['OVN']+women_by_part['EVE'])/((women_by_part['OVN']+women_by_part['EVE'])+(men_by_part['OVN']+men_by_part['EVE']))*100:.2f}%")
# line ~70

# --- ana_08: Within-daypart women share ---
print("\n=== ana_08 ===")
print("Women's share of total plays WITHIN each daypart:")
for dp in dayparts:
    w = women_by_part[dp]
    m = men_by_part[dp]
    # Approximate: women plays / (women + men) — ignores mixed-gender for clean comparison
    share = w / (w + m) * 100
    print(f"  {dp} {dayparts_label[dp]:30s}  women={w:>5}  men={m:>6}  women_share={share:5.2f}%")
