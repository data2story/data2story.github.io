#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_historical.py  --  Section-3 "historical base rate" anchor for the
World Cup 2026 verifiable blog.

The page argues: the model gives Argentina a 30.8% chance of winning. A reader's
instinct is "favourites always flop." The data anchor is that, historically, the
pre-tournament FAVOURITE wins only ~23% of World Cups -- so 30.8% is ABOVE the
long-run favourite hit-rate (a slightly-stronger-than-usual favourite, not a lock).

This script regenerates ONLY the facts we can compute deterministically from the
source table (historical_wc_summary.csv, 22 men's World Cups 1930-2022). It writes
historical_favourites.json.

PROVENANCE -- two clearly separated kinds of fact live in the output:
  * "computed"  : derived here from the CSV. Reproducible -> backs a runnable cell.
  * "cited"     : the ~23% favourite-win base rate. This is NOT in our table; it is
                  an EXTERNAL fact quoted from FIFA's review of the 22 men's
                  tournaments. It is hard-coded below with its source + wording and
                  passed through verbatim -- the script does not "compute" it.

Run (Windows):  py code/build_historical.py
Determinism:    no network, no randomness, fixed input file -> identical output.
"""

import csv
import collections
import json
import os

# --- paths -------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
# Source table is READ-ONLY and lives in the shared dataset, not in the clone.
SRC = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "..",
    "datasets", "worldcup_2026", "historical_wc_summary.csv"))
OUT = os.path.join(HERE, "historical_favourites.json")

# West Germany (1954/1974/1990) and Germany (2014) are the SAME nation. The raw
# table lists them as separate labels; we report both the raw label count and the
# merged-nation count so the provenance is explicit (merging is an editorial call,
# not something the bare table asserts).
NATION_ALIASES = {"West Germany": "Germany"}


def load_rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute(rows):
    n = len(rows)
    champ_labels = [r["champion"] for r in rows]
    label_counts = collections.Counter(champ_labels)

    # merged-nation view (West Germany -> Germany)
    nation_counts = collections.Counter(
        NATION_ALIASES.get(c, c) for c in champ_labels)

    # title concentration: share of the 22 titles held by the top-N nations
    top3 = nation_counts.most_common(3)
    top3_titles = sum(v for _, v in top3)

    # repeat champions (won >= 2), nation-merged
    repeat = {k: v for k, v in nation_counts.items() if v >= 2}
    repeat_titles = sum(repeat.values())

    # host advantage: champion nation == host nation. Co-hosted 2002 (South
    # Korea/Japan) was won by Brazil, so it does not count -- the simple string
    # match handles it correctly (no host string equals "Brazil").
    host_wins = [r for r in rows if r["host"] == r["champion"]]

    # goals-per-tournament trend (raw goals normalised by number of teams, since
    # the field grew 13 -> 32). Reported as a small series for an optional chart.
    goals_series = [
        {
            "year": int(r["year"]),
            "goals_total": int(r["goals_total"]),
            "num_teams": int(r["num_teams"]),
            "goals_per_team": round(int(r["goals_total"]) / int(r["num_teams"]), 3),
        }
        for r in rows
    ]
    first_year, last_year = int(rows[0]["year"]), int(rows[-1]["year"])

    return {
        "num_tournaments": n,
        "span": {"first": first_year, "last": last_year},
        "distinct_champion_labels": len(label_counts),
        "distinct_champion_nations": len(nation_counts),
        "champions_by_nation": [
            {"nation": k, "titles": v} for k, v in nation_counts.most_common()
        ],
        "top3_nations": [{"nation": k, "titles": v} for k, v in top3],
        "top3_share": {
            "titles": top3_titles,
            "of": n,
            "pct": round(100 * top3_titles / n, 1),
        },
        "repeat_champions": {
            "count": len(repeat),
            "titles_held": repeat_titles,
            "share_pct": round(100 * repeat_titles / n, 1),
            "nations": [{"nation": k, "titles": v}
                        for k, v in sorted(repeat.items(),
                                           key=lambda kv: (-kv[1], kv[0]))],
        },
        "host_wins": {
            "count": len(host_wins),
            "of": n,
            "pct": round(100 * len(host_wins) / n, 1),
            "instances": [{"year": int(r["year"]), "nation": r["host"]}
                          for r in host_wins],
        },
        "goals_per_tournament": goals_series,
    }


# --- CITED external fact (NOT computed from the table) ------------------------
# Kept verbatim so it can be cited honestly. The ~23% favourite-win rate is the
# anchor that makes 30.8% read as "above the historical favourite hit-rate".
CITED_FAVOURITE_BASE_RATE = {
    "kind": "cited",
    "claim": "Pre-tournament favourites have won only about 23% of men's "
             "World Cups; the listed favourites have lifted the trophy only "
             "five times in 22 editions.",
    "value_pct": 23,
    "favourite_wins_count": 5,
    "of_tournaments": 22,
    "shortest_price_favourite_wins_since_1966": {
        "count": 3,
        "instances": ["West Germany 1974", "Brazil 1994", "Spain 2010"],
        "note": "Of the editions since 1966 (when pre-tournament odds were first "
                "recorded), the SHORTEST-PRICE favourite went on to win only "
                "three times.",
    },
    "verbatim": ("Favourites tend to win about 23% of the time, based on FIFA's "
                 "review of the previous 22 men's tournaments. The listed World "
                 "Cup favourites have won the trophy only five times over the years."),
    "primary_source": {
        "publisher": "FIFA",
        "title": "What happened to the FIFA World Cup favourites?",
        "url": ("https://www.fifa.com/en/tournaments/mens/worldcup/"
                "canadamexicousa2026/articles/"
                "what-happened-to-the-fifa-world-cup-favourites"),
    },
    "secondary_source": {
        "publisher": "European Gaming Industry News (europeangaming.eu)",
        "title": "50+ World Cup betting statistics: Trends & records (2026)",
        "url": "https://europeangaming.eu/portal/world-cup-betting-statistics/",
        "note": "Independent aggregation that restates the same FIFA ~23% figure "
                "and adds the 'shortest-price favourite won only 3 times since "
                "1966' detail.",
    },
    "accessed": "2026-06-24",
    "provenance": "EXTERNAL / CITED -- not derivable from historical_wc_summary.csv. "
                  "Belongs in verify_map as a 'fact' entry (click-to-source), NOT "
                  "as a runnable cell.",
}


def main():
    rows = load_rows(SRC)
    computed = compute(rows)

    # The model's headline figure, restated here only so the comparison the page
    # makes is self-documenting. It comes from the simulation (client_model.js /
    # forecast), not from this table -- flagged as such.
    model_argentina = {
        "kind": "external_model_output",
        "value_pct": 30.8,
        "team": "Argentina",
        "as_of": "2026-06-23",
        "provenance": "Produced by the tournament Monte-Carlo (100,000 sims); "
                      "NOT computed here. Restated only to frame the 30.8% vs ~23% "
                      "comparison.",
    }

    out = {
        "_about": "Historical base-rate anchor for the WC2026 blog: is the "
                  "model's 30.8% for Argentina 'a lot'? Compares it to the "
                  "long-run rate at which the pre-tournament favourite actually "
                  "wins (~23%).",
        "_provenance_legend": {
            "computed": "Derived deterministically from "
                        "historical_wc_summary.csv by build_historical.py. "
                        "Reproducible -> back with a runnable verify cell.",
            "cited": "External fact quoted from a named source. Back with a "
                     "'fact' (click-to-source) verify entry, never a cell.",
            "external_model_output": "From the simulation, restated for framing.",
        },
        "source_table": {
            "path": "phase2/datasets/worldcup_2026/historical_wc_summary.csv",
            "rows": computed["num_tournaments"],
            "coverage": "Men's FIFA World Cups %d-%d"
                        % (computed["span"]["first"], computed["span"]["last"]),
        },
        "computed_from_table": computed,
        "cited_favourite_base_rate": CITED_FAVOURITE_BASE_RATE,
        "model_headline": model_argentina,
        "framing": {
            "argentina_model_pct": 30.8,
            "favourite_base_rate_pct": 23,
            "delta_pp": round(30.8 - 23, 1),
            "reading": "Argentina's 30.8% sits ABOVE the ~23% long-run "
                       "favourite hit-rate -- a slightly-stronger-than-usual "
                       "favourite, not a lock.",
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # console summary
    c = computed
    print("Wrote", OUT)
    print("Tournaments        :", c["num_tournaments"],
          "(%d-%d)" % (c["span"]["first"], c["span"]["last"]))
    print("Distinct labels    :", c["distinct_champion_labels"],
          "| merged nations:", c["distinct_champion_nations"])
    print("Top-3 nations share: %d/%d = %.1f%%"
          % (c["top3_share"]["titles"], c["top3_share"]["of"],
             c["top3_share"]["pct"]),
          [(t["nation"], t["titles"]) for t in c["top3_nations"]])
    print("Repeat champions   : %d nations hold %d/%d titles (%.1f%%)"
          % (c["repeat_champions"]["count"], c["repeat_champions"]["titles_held"],
             c["num_tournaments"], c["repeat_champions"]["share_pct"]))
    print("Host-nation wins   : %d/%d = %.1f%%"
          % (c["host_wins"]["count"], c["host_wins"]["of"], c["host_wins"]["pct"]))
    print("CITED favourite    : ~%d%% (FIFA, %d of %d), shortest-price only %d since 1966"
          % (CITED_FAVOURITE_BASE_RATE["value_pct"],
             CITED_FAVOURITE_BASE_RATE["favourite_wins_count"],
             CITED_FAVOURITE_BASE_RATE["of_tournaments"],
             CITED_FAVOURITE_BASE_RATE["shortest_price_favourite_wins_since_1966"]["count"]))


if __name__ == "__main__":
    main()
