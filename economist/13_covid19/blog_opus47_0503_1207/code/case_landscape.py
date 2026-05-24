"""Stage 2 - Analyst: 4 March 2020 global confirmed-case snapshot."""
import pandas as pd

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/13_covid19"

jh = pd.read_csv(f"{DATA}/03-04-2020_JH_cases.csv")
jh['country'] = jh['Country/Region'].replace({'US': 'United States', 'UK': 'United Kingdom', 'Mainland China': 'China'})
country_total = jh.groupby('country')['Confirmed'].sum().sort_values(ascending=False)

# --- ana_01: Global case landscape on 4 March 2020 ---
print("=== ana_01 ===")
print(f"Total reported confirmed cases: {country_total.sum():,}")
print(f"Number of countries/regions reporting cases: {(country_total > 0).sum()}")
print(f"\nTop 15 by confirmed cases:")
for country, cases in country_total.head(15).items():
    pct = cases / country_total.sum() * 100
    print(f"  {country:25s} {int(cases):>7,}  ({pct:5.2f}%)")

china_total = country_total.get('China', 0)
print(f"\nChina (Mainland) share of global total: {china_total/country_total.sum()*100:.1f}%")

hubei = jh[jh['Province/State'] == 'Hubei']['Confirmed'].sum()
print(f"Hubei province alone: {int(hubei):,}  ({hubei/country_total.sum()*100:.1f}% of global)")

# Top 5 outside China
outside = country_total[country_total.index != 'China'].head(5)
print(f"\nTop 5 outside China:")
for c, v in outside.items():
    print(f"  {c:25s} {int(v):>7,}")
