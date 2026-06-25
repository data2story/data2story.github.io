#!/usr/bin/env python3
"""
build_odds_snapshot.py  -  Freeze a dated "model vs market" odds snapshot.

This script IS the provenance trail for the betting-odds module. It takes a
hand-recorded snapshot of one sportsbook's outright-winner prices (DraftKings,
read off ESPN on 2026-06-21) and joins it to the model's championship
probabilities (forecast_outputs/champion_odds.csv), computing every derived
number transparently so a reader can re-run it.

Honesty notes baked into the output:
  * Market odds are a DATED SNAPSHOT, not live, and are NOT a model input.
  * Raw implied % = 1/decimal. Across the FULL 48-team board these sum to more
    than 100% (the bookmaker's overround / "vig"). The 10 listed contenders
    only sum to ~99% because the other 38 longshots carry the rest of the
    margin -- so we DO NOT normalise within the top 10 (that would wrongly
    imply they hold ~100% of the probability).
  * De-vigged % is an APPROXIMATION under an explicitly stated ~112% book
    (typical for a 48-team outright market); it is labelled as such.
"""
import csv, json
from pathlib import Path

BASE = Path("D:/AI/journalist agent review/phase2/project/worldcup_2026/blog_verify_opus48_0623_polish")
DS   = Path("D:/AI/journalist agent review/phase2/datasets/worldcup_2026")

# --- Snapshot: DraftKings outright winner, via ESPN, 2026-06-21 (American odds) ---
# Order here is the market's ranking (1 = shortest price = favourite).
DRAFTKINGS_AMERICAN = [
    ("France",      380),
    ("Spain",       550),
    ("England",     550),
    ("Argentina",   800),
    ("Portugal",   1000),
    ("Brazil",     1200),
    ("Germany",    1300),
    ("Netherlands",1300),
    ("Norway",     3500),
    ("Morocco",    3500),
]
ASSUMED_BOOK_OVERROUND = 1.12  # ~112% total book for a 48-team outright (stated assumption)

def american_to_decimal(a: int) -> float:
    return round(a / 100 + 1, 4) if a > 0 else round(100 / (-a) + 1, 4)

# --- Model championship probabilities (exact, from the forecast) ---
model_pct = {}
with open(BASE / "forecast_outputs" / "champion_odds.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        model_pct[row["team"]] = round(float(row["p_champion"]) * 100, 2)

# model rank over ALL 48 teams
model_rank = {t: i + 1 for i, (t, _) in enumerate(
    sorted(model_pct.items(), key=lambda kv: -kv[1]))}

market_decimal = {t: american_to_decimal(a) for t, a in DRAFTKINGS_AMERICAN}
market_rank    = {t: i + 1 for i, (t, _) in enumerate(DRAFTKINGS_AMERICAN)}
market_american = dict(DRAFTKINGS_AMERICAN)

# --- Build the comparison rows: union of model top-10 + market top-10 ---
model_top10 = [t for t, _ in sorted(model_pct.items(), key=lambda kv: -kv[1])[:10]]
union = list(dict.fromkeys([t for t, _ in DRAFTKINGS_AMERICAN] + model_top10))

rows = []
for t in union:
    dec = market_decimal.get(t)
    raw = round(100.0 / dec, 2) if dec else None
    devig = round(raw / ASSUMED_BOOK_OVERROUND, 2) if raw is not None else None
    rows.append({
        "team": t,
        "model_pct": model_pct.get(t),
        "model_rank": model_rank.get(t),
        "market_american": (("+" if market_american[t] > 0 else "") + str(market_american[t])) if t in market_american else None,
        "market_decimal": dec,
        "market_implied_raw_pct": raw,
        "market_implied_devig_pct": devig,
        "market_rank": market_rank.get(t),  # None => outside the book's top 10
    })

# sort by the model's view (the story is model-centric)
rows.sort(key=lambda r: (-(r["model_pct"] or 0)))

snapshot = {
    "meta": {
        "title": "Model vs market - 2026 World Cup outright winner",
        "as_of": "2026-06-21",
        "book": "DraftKings",
        "via": "ESPN",
        "odds_data_license": "Odds via The Odds API (display permitted); book prices cross-checked on ESPN",
        "format": "american",
        "assumed_book_overround": ASSUMED_BOOK_OVERROUND,
        "is_live": False,
        "is_model_input": False,
        "leakage_note": "These market prices are display-only context; they are NOT fed into the forecast model.",
        "overround_note": ("Raw implied probabilities are 1/decimal. Across the full 48-team board they "
                           "sum to ~112% - the bookmaker's margin - so they slightly overstate true "
                           "chances. The de-vigged column divides by that assumed ~112% book; the "
                           "model-vs-market gap is real and, if anything, understated after the margin."),
        "headline": None,  # filled below
        "responsible_gambling": {
            "framing": "Informational only - not betting advice. This compares a statistical model with bookmaker odds for analysis.",
            "age": "18+ (UK) / 21+ (most US states)",
            "help_uk": "UK National Gambling Helpline 0808 8020 133 (gamcare.org.uk)",
            "help_us": "US 1-800-GAMBLER",
            "note": "GambleAware closed 2026-03-31; use GamCare / the National Gambling Helpline."
        }
    },
    "rows": rows,
}

# derive headline facts
mkt_fav = min(market_rank, key=market_rank.get)
arg_mkt_rank = market_rank.get("Argentina")
model_fav = min(model_rank, key=model_rank.get)
snapshot["meta"]["headline"] = (
    f"The model's favourite ({model_fav} {model_pct[model_fav]}%) is the market's "
    f"#{arg_mkt_rank}; the market's favourite is {mkt_fav}."
)

out = BASE / "code" / "odds_snapshot.json"
out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")

# console summary
print("wrote", out)
print("model favourite :", model_fav, model_pct[model_fav], "%")
print("market favourite:", mkt_fav, market_american[mkt_fav], "->", market_decimal[mkt_fav])
print("Argentina market rank:", arg_mkt_rank)
print("\nteam          model%  mkt(am)  raw%   devig%  mkt_rank")
for r in rows:
    print(f"{r['team']:<13} {str(r['model_pct']):>5}  {str(r['market_american'] or '-'):>6}  "
          f"{str(r['market_implied_raw_pct'] or '-'):>5}  {str(r['market_implied_devig_pct'] or '-'):>5}   "
          f"{r['market_rank'] or '-'}")
