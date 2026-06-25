"""
build_goals.py - regenerate goals_2026.json: the "goals so far" data for the
2026 World Cup blog (golden-boot race + goal patterns), as of 2026-06-23.

TWO data sources, each labelled in the output so a later stage can build a
verify_map entry + runnable cell:

  (A) CURRENT 2026 World Cup goals -> openfootball CC0 `2026/worldcup.json`
      (https://github.com/openfootball/worldcup.json, raw on GitHub).
      The snapshot used for this build is cached locally as
      `_of_2026_raw.json` for offline determinism; pass --refresh to re-pull.
      We compute: top scorers (golden-boot race), and - because the 2026
      tournament has enough goals so far (139 events / 46 played matches) -
      the 2026 goals-by-minute distribution + penalty/open-play/own-goal split
      AND a per-team goals-scored tally.

  (B) LONG-RUN HISTORICAL base rate -> the shared local `goalscorers.csv`
      (47,676 historical international goals: date, home_team, away_team, team,
      scorer, minute, own_goal, penalty). Used ONLY as base-rate *context*
      next to the 2026 numbers, never mixed into the 2026 golden-boot race.

Everything is deterministic: same inputs -> byte-identical goals_2026.json
(scorers sorted by goals desc then name; buckets in fixed order).

openfootball goal schema (per match):
  team1, team2, score.ft=[h,a], group, round, date, ground,
  goals1=[{name,minute,penalty?,owngoal?}], goals2=[...].
  - minute may be stoppage-time like "90+5" -> parsed to its base bucket via
    the displayed minute (the "+N" is added on, so "90+5" counts in the 90+
    bucket; "45+2" counts in the 31-45 bucket — i.e. bucket by the base clock).
  - own-goals are listed under the *scoring* team's array but credited to the
    conceding player; they are EXCLUDED from scorer tallies and counted in
    their own-goal category for the pen/open-play/own-goal split.

Run:
  py build_goals.py            # use cached _of_2026_raw.json (offline, default)
  py build_goals.py --refresh  # re-pull the openfootball snapshot first
"""
import sys, json, argparse
from pathlib import Path
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows GBK console
except Exception:
    pass

HERE = Path(__file__).resolve().parent


def _find_dataset_csv():
    """Locate the shared READ-ONLY goalscorers.csv. From this clone the path is
    .../phase2/datasets/...; walk up until we find a phase2/datasets/ match so the
    script also works if relocated."""
    rel = Path("datasets") / "worldcup_2026" / "raw" / "goalscorers.csv"
    for p in [HERE, *HERE.parents]:
        cand = p / "phase2" / rel
        if cand.exists():
            return cand
        cand = p / rel                      # in case we're already inside phase2/
        if cand.exists():
            return cand
    # last-resort: the known absolute layout
    return HERE.parents[3] / rel


DATASET_CSV = _find_dataset_csv()

OF_URL = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
OF_CACHE = HERE / "_of_2026_raw.json"

SNAPSHOT_DATE = "2026-06-23"

# fixed 15-minute buckets (final bucket folds 90+ stoppage time into "90+")
BUCKETS = ["1-15", "16-30", "31-45", "46-60", "61-75", "76-90", "90+"]


def base_minute(raw):
    """Return the displayed clock minute as an int. Handles openfootball string
    minutes ('90+5' -> 90, '45+2' -> 45) AND the historical csv's float minutes
    ('44.0' -> 44). Blank/NaN -> None."""
    s = str(raw).strip()
    if not s or s.lower() in ("nan", "none"):
        return None
    head = s.split("+", 1)[0].strip()
    try:
        return int(round(float(head)))      # '44.0' and '44' both work
    except (ValueError, TypeError):
        return None


def bucket_for(raw):
    """Map a raw minute string to one of BUCKETS. Stoppage time ('90+5') -> '90+'."""
    s = str(raw).strip()
    if "+" in s and s.split("+", 1)[0].strip() == "90":
        return "90+"               # second-half stoppage time
    m = base_minute(s)
    if m is None:
        return None
    if m > 90:
        return "90+"
    if m <= 15:
        return "1-15"
    if m <= 30:
        return "16-30"
    if m <= 45:
        return "31-45"             # incl. first-half stoppage '45+N'
    if m <= 60:
        return "46-60"
    if m <= 75:
        return "61-75"
    return "76-90"                  # 76..90


def load_openfootball(refresh):
    if refresh or not OF_CACHE.exists():
        import requests
        r = requests.get(OF_URL, timeout=30)
        r.raise_for_status()
        OF_CACHE.write_text(r.text, encoding="utf-8")
    return json.loads(OF_CACHE.read_text(encoding="utf-8"))


def goal_events_2026(doc):
    """Flatten openfootball matches into goal events. Returns (events, n_played)."""
    events = []
    n_played = 0
    for m in doc["matches"]:
        if not m.get("score"):
            continue               # not played yet
        n_played += 1
        for side, team, opp in (("goals1", m["team1"], m["team2"]),
                                ("goals2", m["team2"], m["team1"])):
            for g in (m.get(side) or []):
                events.append({
                    "scorer": g.get("name", ""),
                    "team": team,           # the team that got the goal credited on the board
                    "opponent": opp,
                    "minute_raw": str(g.get("minute", "")),
                    "bucket": bucket_for(g.get("minute", "")),
                    "penalty": bool(g.get("penalty")),
                    "owngoal": bool(g.get("owngoal")),
                    "date": m.get("date"),
                    "group": m.get("group"),
                })
    return events, n_played


def top_scorers(events, limit=15):
    """Golden-boot race. Own-goals excluded (credited to the conceding player)."""
    tally = defaultdict(lambda: {"goals": 0, "penalties": 0, "open_play": 0})
    for e in events:
        if e["owngoal"]:
            continue
        key = (e["scorer"], e["team"])
        t = tally[key]
        t["goals"] += 1
        if e["penalty"]:
            t["penalties"] += 1
        else:
            t["open_play"] += 1
    rows = [{"player": k[0], "team": k[1], **v} for k, v in tally.items()]
    rows.sort(key=lambda r: (-r["goals"], r["player"]))   # deterministic
    return rows[:limit]


def minute_distribution(events):
    counts = Counter(e["bucket"] for e in events if e["bucket"])
    total = sum(counts.values())
    return [{
        "bucket": b,
        "goals": counts.get(b, 0),
        "pct": round(100.0 * counts.get(b, 0) / total, 1) if total else 0.0,
    } for b in BUCKETS], total


def type_split(events):
    own = sum(1 for e in events if e["owngoal"])
    pen = sum(1 for e in events if e["penalty"] and not e["owngoal"])
    opn = sum(1 for e in events if not e["penalty"] and not e["owngoal"])
    total = own + pen + opn
    def pct(x):
        return round(100.0 * x / total, 1) if total else 0.0
    return {
        "open_play": {"goals": opn, "pct": pct(opn)},
        "penalty": {"goals": pen, "pct": pct(pen)},
        "own_goal": {"goals": own, "pct": pct(own)},
        "total": total,
    }


def team_tally(events, limit=20):
    """Per-team goals scored (own-goals NOT credited to the team that benefited)."""
    c = Counter()
    for e in events:
        if e["owngoal"]:
            continue
        c[e["team"]] += 1
    rows = [{"team": t, "goals": n} for t, n in c.items()]
    rows.sort(key=lambda r: (-r["goals"], r["team"]))
    return rows[:limit]


# ---- historical base rate from the shared goalscorers.csv (context only) ----

def historical_base_rate():
    import pandas as pd
    df = pd.read_csv(DATASET_CSV, encoding="utf-8")
    # normalise booleans (csv stores TRUE/FALSE strings)
    def asbool(s):
        return s.astype(str).str.strip().str.upper().eq("TRUE")
    own = asbool(df["own_goal"])
    pen = asbool(df["penalty"])

    # minute distribution
    bk = df["minute"].map(bucket_for)
    bcounts = bk.value_counts()
    btotal = int(bcounts.sum())
    minute = [{
        "bucket": b,
        "goals": int(bcounts.get(b, 0)),
        "pct": round(100.0 * int(bcounts.get(b, 0)) / btotal, 1) if btotal else 0.0,
    } for b in BUCKETS]

    n_own = int(own.sum())
    n_pen = int((pen & ~own).sum())
    n_open = int((~pen & ~own).sum())
    total = n_own + n_pen + n_open
    def pct(x):
        return round(100.0 * x / total, 1) if total else 0.0
    split = {
        "open_play": {"goals": n_open, "pct": pct(n_open)},
        "penalty": {"goals": n_pen, "pct": pct(n_pen)},
        "own_goal": {"goals": n_own, "pct": pct(n_own)},
        "total": total,
    }
    return {
        "source_file": "phase2/datasets/worldcup_2026/raw/goalscorers.csv",
        "n_goal_events": int(len(df)),
        "date_range": [str(df["date"].min()), str(df["date"].max())],
        "minute_distribution": minute,
        "type_split": split,
        "_note": ("Long-run base rate over all recorded international goals; "
                  "shown as context next to the 2026 numbers, NOT mixed in."),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true",
                    help="re-pull the openfootball 2026 snapshot before building")
    args = ap.parse_args()

    doc = load_openfootball(args.refresh)
    events, n_played = goal_events_2026(doc)

    scorers = top_scorers(events)
    minute, minute_total = minute_distribution(events)
    split = type_split(events)
    teams = team_tally(events)

    out = {
        "as_of": SNAPSHOT_DATE,
        "_about": ("'Goals so far' at the 2026 World Cup: golden-boot race + goal "
                   "patterns. 2026 numbers from openfootball (CC0); historical "
                   "base rate from the shared goalscorers.csv. Regenerate with "
                   "`py build_goals.py` (offline cache) or `--refresh`."),
        "current_2026": {
            "source": "openfootball worldcup.json 2026 (CC0)",
            "source_url": OF_URL,
            "source_cache": "code/_of_2026_raw.json",
            "matches_played": n_played,
            "total_matches": len(doc["matches"]),
            "goal_events": len(events),
            "golden_boot": {
                "_note": ("Own-goals excluded (credited to the conceding player). "
                          "Ties broken alphabetically. pens+open_play = goals."),
                "leaders": scorers,
            },
            "goals_by_minute": {
                "_note": ("15-minute buckets; first-half stoppage ('45+N') folds "
                          "into 31-45, second-half stoppage ('90+N') into 90+. "
                          "Includes penalties + own-goals (every goal event)."),
                "total": minute_total,
                "buckets": minute,
            },
            "type_split": split,
            "team_goals": {
                "_note": "Goals scored per team; own-goals not credited to the beneficiary.",
                "teams": teams,
            },
        },
        "historical_base_rate": historical_base_rate(),
    }

    (HERE / "goals_2026.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- console summary (deterministic) ----
    print(f"wrote goals_2026.json  (as_of {SNAPSHOT_DATE})")
    print(f"  2026: {n_played} played / {len(doc['matches'])} matches, {len(events)} goal events")
    print("  golden boot (top 5):")
    for r in scorers[:5]:
        print(f"    {r['goals']}  {r['player']:<22} {r['team']:<14} "
              f"(open {r['open_play']}, pen {r['penalties']})")
    late = next(b for b in minute if b["bucket"] == "76-90")
    stop = next(b for b in minute if b["bucket"] == "90+")
    print(f"  2026 minute split total={minute_total}; "
          f"76-90={late['pct']}%  90+={stop['pct']}%  "
          f"(76th-min-on = {round(late['pct']+stop['pct'],1)}%)")
    s = split
    print(f"  2026 type split: open {s['open_play']['pct']}%  "
          f"pen {s['penalty']['pct']}%  own {s['own_goal']['pct']}%  (n={s['total']})")
    h = out["historical_base_rate"]["type_split"]
    print(f"  hist base rate (n={h['total']}): open {h['open_play']['pct']}%  "
          f"pen {h['penalty']['pct']}%  own {h['own_goal']['pct']}%")


if __name__ == "__main__":
    main()
