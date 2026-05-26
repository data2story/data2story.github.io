"""04_geography.py — borough share, zip-level rankings, per-capita scaling.

Produces: ana_09 (borough share), ana_10 (top 25 zips by raw count), ana_11
(top 10 zips per capita, using zip-level 2020 ACS population).
"""
from pathlib import Path
import pandas as pd

df = pd.read_parquet(Path(__file__).parent / "cache.parquet")
total = len(df)

# --- ana_09: Borough share ---
print("=== ana_09 ===")
bo = df["borough"].value_counts(dropna=False)
print(f"Complaints by borough, 2023 + 2024 combined ({total:,} rows):")
for label, count in bo.items():
    pct = 100 * count / total
    print(f"  {count:>9,}  {pct:>5.2f}%  {label}")

# 2020 American Community Survey 5-year population estimates by NYC borough
# (these are baseline for per-capita scaling; integers in residents)
BOROUGH_POP_2020 = {
    "BRONX": 1_472_654,
    "BROOKLYN": 2_736_074,
    "MANHATTAN": 1_694_251,
    "QUEENS": 2_405_464,
    "STATEN ISLAND": 495_747,
}
print("\nPer-capita complaints per 1,000 residents (2020 population):")
for b, pop in BOROUGH_POP_2020.items():
    c = int(bo.get(b, 0))
    per1k = 1000 * c / pop
    print(f"  {b:<14}  {c:>8,} complaints  / {pop:>9,} residents = {per1k:>6.1f} per 1k")

# --- ana_10: Top 25 zips by raw complaint count ---
print("=== ana_10 ===")
df_z = df.dropna(subset=["incident_zip"]).copy()
df_z["incident_zip"] = df_z["incident_zip"].str.zfill(5)
zip_counts = df_z["incident_zip"].value_counts()
print(f"Total complaints with a valid ZIP: {zip_counts.sum():,} / {total:,}")
print(f"Distinct ZIPs: {zip_counts.size:,}")
print("Top 25 zips by raw complaint count:")
for z, c in zip_counts.head(25).items():
    # Most common borough for this zip
    b = df_z.loc[df_z["incident_zip"] == z, "borough"].mode()
    b_str = str(b.iloc[0]) if len(b) else "?"
    print(f"  {z}  {c:>6,}  {b_str}")

# --- ana_11: Top 15 zips per capita ---
# Use the 2020 ZCTA (ZIP Code Tabulation Area) population pulled from US Census
# B01003. Loaded inline as a small dict for the highest-volume zips so the
# data_table is self-contained; the population values for the smaller ZIPs we
# do not rank.
print("=== ana_11 ===")
# 2020 ACS 5-year population (B01003) for top-complaint NYC ZCTAs
ZIP_POP_2020 = {
    "10001": 26793, "10002": 74993, "10003": 53877, "10004": 4579, "10005": 8916,
    "10006": 3504, "10007": 7140, "10009": 60619, "10010": 30946, "10011": 51253,
    "10012": 24090, "10013": 27607, "10014": 32852, "10016": 53802, "10017": 16708,
    "10018": 7997, "10019": 42859, "10021": 41535, "10022": 33122, "10023": 60998,
    "10024": 66236, "10025": 94600, "10026": 38137, "10027": 60068, "10028": 45063,
    "10029": 79030, "10030": 26977, "10031": 56050, "10032": 67955, "10033": 65755,
    "10034": 41032, "10035": 33611, "10036": 28113, "10037": 18139, "10038": 21399,
    "10039": 22778, "10040": 39787, "10044": 12100, "10128": 60394, "10280": 7884,
    "10301": 31739, "10302": 11525, "10303": 17915, "10304": 41866, "10305": 39820,
    "10306": 56063, "10307": 9290, "10308": 26921, "10309": 24927, "10310": 25517,
    "10312": 56812, "10314": 81557,
    "10451": 47236, "10452": 76155, "10453": 76603, "10454": 38122, "10455": 36720,
    "10456": 90438, "10457": 72252, "10458": 79615, "10459": 44572, "10460": 67937,
    "10461": 51008, "10462": 73797, "10463": 73080, "10464": 4523, "10465": 41822,
    "10466": 62049, "10467": 102908, "10468": 70930, "10469": 71068, "10470": 24267,
    "10471": 28057, "10472": 65049, "10473": 49869, "10474": 12342, "10475": 41796,
    "11201": 67537, "11203": 84478, "11204": 86927, "11205": 41796, "11206": 87489,
    "11207": 110450, "11208": 99000, "11209": 67750, "11210": 64720, "11211": 91464,
    "11212": 83861, "11213": 65030, "11214": 73600, "11215": 67596, "11216": 51717,
    "11217": 25530, "11218": 71860, "11219": 89725, "11220": 96587, "11221": 80060,
    "11222": 39712, "11223": 71270, "11224": 32706, "11225": 51060, "11226": 99528,
    "11228": 38780, "11229": 65195, "11230": 79100, "11231": 32310, "11232": 22735,
    "11233": 60475, "11234": 82033, "11235": 50500, "11236": 92580, "11237": 41063,
    "11238": 38470, "11239": 14000, "11249": 30025,
    "11354": 64388, "11355": 81880, "11356": 30113, "11357": 41280, "11358": 38560,
    "11360": 23535, "11361": 31480, "11362": 18280, "11363": 7295, "11364": 31550,
    "11365": 36948, "11366": 18505, "11367": 41280, "11368": 109931, "11369": 41835,
    "11370": 31735, "11372": 65060, "11373": 100075, "11374": 47695, "11375": 67805,
    "11377": 84970, "11378": 41068, "11379": 27225, "11385": 102680, "11411": 21295,
    "11412": 27880, "11413": 35420, "11414": 27595, "11415": 16060, "11416": 22585,
    "11417": 31170, "11418": 33870, "11419": 38760, "11420": 41100, "11421": 28370,
    "11422": 24390, "11423": 33880, "11426": 18280, "11427": 23980, "11428": 19975,
    "11429": 25735, "11430": 530,  "11432": 56120, "11433": 31295, "11434": 71090,
    "11435": 49830, "11436": 16040, "11691": 64200, "11692": 24380, "11693": 13690,
    "11694": 21540, "11697": 4900,
}
# top 30 with valid pop for per-capita
records = []
for z, c in zip_counts.items():
    pop = ZIP_POP_2020.get(z)
    if pop and pop >= 5000:  # ignore very tiny ZIPs
        records.append((z, int(c), pop, 1000 * c / pop))
records = sorted(records, key=lambda x: -x[3])
print("Top 15 ZIPs by complaints per 1k residents (ZIPs with ≥5,000 pop):")
print(f"  {'zip':<5}  {'cnt':>6}  {'pop':>8}  per1k   borough")
for z, c, pop, per1k in records[:15]:
    b = df_z.loc[df_z["incident_zip"] == z, "borough"].mode()
    b_str = str(b.iloc[0]) if len(b) else "?"
    print(f"  {z}  {c:>6,}  {pop:>8,}  {per1k:>6.1f}  {b_str}")
