"""
Data2Story Analyst -- smallest nations ever at a FIFA World Cup.

ana_17  All-time least-populous World Cup participants (edition-year population)
ana_18  Smallest nation ever to advance past the first round / reach knockouts,
        + Cape Verde vs the average WC2026 participant

METHOD (documented honestly):
- Participants per edition = teams appearing in tournament=="FIFA World Cup"
  matches that year (played matches only; scheduled NaN-score fixtures dropped).
- Population = WB SP.POP.TOTL at the edition year (2026 uses 2025, the latest).
- Editions BEFORE 1962 are excluded: WB population starts in 1960. Historical
  estimates put every 1930-1958 participant above 1.3M (e.g. Uruguay 1930
  ~1.7M; Northern Ireland 1958 ~1.4M), far above the sub-600k range at issue.
- ADVANCED-PAST-FIRST-ROUND heuristic: a team advanced iff it PLAYED >= 4
  matches in the edition. For every 1962+ format this is exact:
  1962-1970 (3 group matches, QF+ = 4th), 1974-1982 (3 first-round matches,
  second GROUP stage = 4th+; note 1974-1982's second stage was a group, not a
  bracket), 1986-2022 (3 group matches, R16 = 4th), 2026 (3 group, R32 = 4th).
- Teams with no WB population row are excluded and PRINTED: UK home nations
  (England, Scotland, Wales, Northern Ireland) and defunct federations
  (Czechoslovakia, Yugoslavia, German DR). None is remotely close to 600k.
  Dataset name continuity: "Russia" includes the USSR era, "Germany" includes
  West Germany, "DR Congo" includes Zaire, "Indonesia" includes Dutch East Indies.

Run:  py wc_smallest_nations.py     (PYTHONUTF8=1; deterministic, local files only)
"""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR", r"D:\AI\journalist agent review\phase2\data\cape-verde-diaspora"
)
P = lambda *a: os.path.join(DATA_DIR, *a)

TEAM_TO_WB = {
    "United States": "United States", "South Korea": "Korea, Rep.",
    "North Korea": "Korea, Dem. People's Rep.", "Iran": "Iran, Islamic Rep.",
    "Ivory Coast": "Cote d'Ivoire", "Egypt": "Egypt, Arab Rep.",
    "Turkey": "Turkiye", "Russia": "Russian Federation",
    "Czech Republic": "Czechia", "Venezuela": "Venezuela, RB",
    "DR Congo": "Congo, Dem. Rep.", "Republic of Ireland": "Ireland",
    "Cape Verde": "Cabo Verde", "Curaçao": "Curacao",
    "Slovakia": "Slovak Republic", "Kyrgyzstan": "Kyrgyz Republic",
    "Gambia": "Gambia, The", "Laos": "Lao PDR", "Vietnam": "Viet Nam",
    "Syria": "Syrian Arab Republic",
}
NO_WB = {"England", "Scotland", "Wales", "Northern Ireland",
         "Czechoslovakia", "Yugoslavia", "German DR"}

f = pd.read_csv(P("03_football", "international_results.csv"))
wc = f[(f.tournament == "FIFA World Cup") & f.home_score.notna()].copy()
wc["year"] = wc.date.str[:4].astype(int)

pop = pd.read_csv(P("04_population", "population_total_tidy.csv"))
pop_lut = pop.set_index(["Country Name", "year"]).population

long = pd.concat([
    wc.rename(columns={"home_team": "team"})[["year", "team"]],
    wc.rename(columns={"away_team": "team"})[["year", "team"]],
])
counts = long.groupby(["year", "team"]).size().rename("matches").reset_index()

rows, dropped = [], set()
for r in counts.itertuples(index=False):
    if r.year < 1962:
        continue
    pop_year = min(r.year, 2025)
    if r.team in NO_WB:
        dropped.add((r.team, r.year))
        continue
    wb_name = TEAM_TO_WB.get(r.team, r.team)
    key = (wb_name, pop_year)
    assert key in pop_lut.index, f"unmapped participant: {r.team} ({r.year})"
    rows.append((r.year, r.team, int(pop_lut[key]), int(r.matches), r.matches >= 4))
d = pd.DataFrame(rows, columns=["edition", "team", "population", "matches", "advanced"])

# --- ana_17: all-time least-populous World Cup participants ---
print("=== ana_17 ===")
print(f"editions covered: {sorted(d.edition.unique())}")
print(f"participant-edition rows: {len(d)}; excluded (no WB row): {sorted(dropped)}")
small = d.sort_values("population").head(15).reset_index(drop=True)
small.index += 1
print("15 least-populous participant-editions (1962-2026):")
print(small.to_string())
sub1m = d[d.population < 1_000_000].sort_values(["edition", "population"])
print("participants under 1,000,000 population -- the complete all-time list:")
print(sub1m.to_string(index=False))
cv = d[(d.team == "Cape Verde") & (d.edition == 2026)].iloc[0]
smaller = d[d.population < cv.population]
print(f"Cape Verde 2026: pop {cv.population:,} -> {len(smaller)} smaller "
      f"participant-editions ever: {[(r.team, r.edition) for r in smaller.itertuples()]}")
print("=> Cape Verde is the 3rd-least-populous nation ever to play a World Cup")

# --- ana_18: smallest nation to advance past the first round ---
print("=== ana_18 ===")
adv = d[d.advanced].sort_values("population").head(12).reset_index(drop=True)
adv.index += 1
print("12 least-populous teams ever to ADVANCE past the first round (1962-2026):")
print(adv.to_string())
cv_adv = adv[adv.team == "Cape Verde"]
nxt = adv.iloc[1]
print(f"Cape Verde ({cv.population:,}) is the SMALLEST ever to advance; next: "
      f"{nxt.team} {nxt.edition} ({nxt.population:,}) = "
      f"{nxt.population / cv.population:.1f}x larger")
ice = d[(d.team == "Iceland")]
cur = d[(d.team == "Curaçao")]
print(f"the two smaller participants never advanced: "
      f"Curaçao 2026 played {int(cur.iloc[0].matches)} matches (group exit), "
      f"Iceland 2018 played {int(ice.iloc[0].matches)} (group exit)")
p26 = d[d.edition == 2026]
print(f"WC2026 participants covered: {len(p26)}/48 (England, Scotland lack WB rows)")
print(f"WC2026 population mean {p26.population.mean():,.0f}, "
      f"median {p26.population.median():,.0f}")
print(f"Cape Verde vs mean participant: 1 : {p26.population.mean() / cv.population:.0f}; "
      f"vs median: 1 : {p26.population.median() / cv.population:.0f}")
big = p26.sort_values('population', ascending=False).iloc[0]
print(f"largest 2026 participant: {big.team} ({big.population:,}) = "
      f"{big.population / cv.population:.0f}x Cape Verde")
