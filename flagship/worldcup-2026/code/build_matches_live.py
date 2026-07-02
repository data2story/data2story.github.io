"""
build_matches_live.py — rebuild matches.csv to the LIVE Round-of-32 state from openfootball.

Fetches the canonical openfootball 2026 World Cup feed and rewrites ../matches.csv as a
drop-in replacement of the existing file, advancing it from the mid-group-stage snapshot to
the live state (all 72 group games played; Round of 32 10/16 played, 6 scheduled).

Schema (drop-in + one added column):
    match_id,date,stage,group,home,away,home_goals,away_goals,status,winner
The original 9 columns are byte-for-byte compatible with the old file (same match_id
numbering, stage/group labels, home/away orientation, integer scores, 'played'/'scheduled'
status, and the R16..Final placeholder-name rows). The NEW `winner` column is empty for
every group row and every unplayed row, and holds the advancing team for each played
knockout game.

How each block is built:
  * Group rows (match_id 1..72): matched to openfootball by unordered team pair, so the
    blog's own match_id numbering + home/away orientation are preserved; only real scores
    are filled in. (Verified: 0 orientation flips / 0 date mismatches vs the old file.)
  * R32 rows (73..88): real team names taken from openfootball's Round-of-32 array (index
    i -> match_id 73+i). 10 played -> real score + winner; 6 scheduled -> blank.
    - Winner is read from openfootball's own result (penalties > extra-time > full-time),
      NOT inferred from Elo. For the penalty/ET upsets (Paraguay, Morocco, Belgium) this is
      the team openfootball advances into the Round of 16.
  * R16..Final rows (89..104): copied verbatim from the existing matches.csv (placeholder
    names like "Winner Match 74"); they stay scheduled.

Cross-checks before writing (all must pass, else the script aborts):
  * 72 group games, all played.
  * R32 matchups (73..88) derived independently from bracket_rules.json (r32_slots +
    best_thirds_allocation) applied to the real final standings == openfootball R32, 16/16.
  * Every played-KO winner appears among the openfootball Round-of-16 feeders.

Run:  python build_matches_live.py      (writes ../matches.csv)
Source: https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json
"""
import sys, json, urllib.request
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent          # .../blog root (worldcup_2026)
SRC_URL = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
MATCHES = DATA / "matches.csv"
BRACKET = DATA / "bracket_rules.json"


def fetch_openfootball():
    """Return the parsed openfootball feed (list of match dicts)."""
    req = urllib.request.Request(SRC_URL, headers={"User-Agent": "wc2026-forecast/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)["matches"]


def ko_result(m):
    """(winner, loser) for a decided knockout game, else None.
    Priority: penalty shootout > extra-time > full-time (openfootball score keys p/aet/et/ft)."""
    sc = m.get("score")
    if not sc:
        return None
    t1, t2 = m["team1"], m["team2"]
    for key in ("p", "aet", "et", "ft"):
        v = sc.get(key)
        if v is not None:
            h, a = v
            if h > a:
                return (t1, t2)
            if a > h:
                return (t2, t1)
            # exact tie at this level -> fall through to a finer decider
    return None


def build():
    ms = fetch_openfootball()
    br = json.loads(BRACKET.read_text(encoding="utf-8"))
    old = pd.read_csv(MATCHES, encoding="utf-8")

    group_matches = [m for m in ms if m.get("group")]
    of_r32 = [m for m in ms if m.get("round") == "Round of 32"]
    of_r16 = [m for m in ms if m.get("round") == "Round of 16"]
    assert len(group_matches) == 72, f"expected 72 group games, got {len(group_matches)}"
    assert all(m.get("score", {}) and m["score"].get("ft") for m in group_matches), \
        "some group game has no full-time score"
    assert len(of_r32) == 16, f"expected 16 R32 games, got {len(of_r32)}"

    # ---- group scores indexed by unordered team pair (preserve blog orientation) ----
    pair_score = {}
    for m in group_matches:
        pair_score[frozenset([m["team1"], m["team2"]])] = m["score"]["ft"]

    # ---- final standings + independent R32 derivation cross-check (16/16) ----
    from collections import defaultdict
    tab = defaultdict(lambda: {"pts": 0, "gd": 0, "gf": 0, "grp": None})
    for m in group_matches:
        g = m["group"].replace("Group ", "")
        t1, t2 = m["team1"], m["team2"]
        h, a = m["score"]["ft"]
        tab[t1]["grp"] = g; tab[t2]["grp"] = g
        tab[t1]["pts"] += 3 if h > a else (1 if h == a else 0)
        tab[t2]["pts"] += 3 if a > h else (1 if a == h else 0)
        tab[t1]["gf"] += h; tab[t2]["gf"] += a
        tab[t1]["gd"] += h - a; tab[t2]["gd"] += a - h
    groups = sorted({v["grp"] for v in tab.values()})
    standings = {}
    for g in groups:
        ts = [t for t, v in tab.items() if v["grp"] == g]
        ts.sort(key=lambda t: (tab[t]["pts"], tab[t]["gd"], tab[t]["gf"]), reverse=True)
        standings[g] = ts
    thirds = [standings[g][2] for g in groups]
    thirds.sort(key=lambda t: (tab[t]["pts"], tab[t]["gd"], tab[t]["gf"]), reverse=True)
    qual8 = sorted(tab[t]["grp"] for t in thirds[:8])
    key = "".join(qual8)
    assign = br["best_thirds_allocation"]["table"][key]["assign"]   # {matchid_str: '3X'}
    r32_slots = br["r32_slots"]

    def resolve(code, mid):
        if code[0] == "1":
            return standings[code[1]][0]
        if code[0] == "2":
            return standings[code[1]][1]
        if code[0] == "3":
            return standings[assign[str(mid)][-1]][2]
        raise ValueError(code)

    derived = {}
    ok = 0
    for i, mid in enumerate(range(73, 89)):
        s = r32_slots[str(mid)]
        dh, da = resolve(s["home"], mid), resolve(s["away"], mid)
        derived[mid] = (dh, da)
        oh, oa = of_r32[i]["team1"], of_r32[i]["team2"]
        if (dh, da) == (oh, oa):
            ok += 1
    assert ok == 16, (f"R32 derivation mismatch: only {ok}/16 match openfootball "
                      f"(best-thirds key={key})")

    # ---- KO winners + R16 cross-check ----
    r16_teams = {t for m in of_r16 for t in (m["team1"], m["team2"])
                 if not str(t).startswith("W")}
    ko_win = {}   # match_id -> (winner, loser) for played R32 games
    for i, m in enumerate(of_r32):
        res = ko_result(m)
        if res is not None:
            ko_win[73 + i] = res
            assert res[0] in r16_teams, \
                f"winner {res[0]} of match {73+i} not found among R16 feeders"

    # ---- assemble rows ----
    rows = []
    for _, r in old.iterrows():
        mid = int(r["match_id"])
        stage = r["stage"]
        if stage == "group":
            ft = pair_score.get(frozenset([r["home"], r["away"]]))
            assert ft is not None, f"no openfootball score for group pair {r['home']} v {r['away']}"
            hg, ag = int(ft[0]), int(ft[1])
            rows.append([mid, r["date"], stage, r["group"], r["home"], r["away"],
                         hg, ag, "played", ""])
        elif 73 <= mid <= 88:
            idx = mid - 73
            m = of_r32[idx]
            home, away = m["team1"], m["team2"]
            if mid in ko_win:
                # played: winner-priority score (p>et>ft) drives display; use ft for the
                # home_goals/away_goals columns (the 90'/regulation scoreline), winner column
                # carries the actual advancer.
                ft = m["score"]["ft"]
                winner = ko_win[mid][0]
                rows.append([mid, m["date"], "R32", "", home, away,
                             int(ft[0]), int(ft[1]), "played", winner])
            else:
                rows.append([mid, m["date"], "R32", "", home, away, "", "", "scheduled", ""])
        else:
            # R16..Final: copy the existing placeholder row verbatim, winner empty
            rows.append([mid, r["date"], stage, r["group"] if pd.notna(r["group"]) else "",
                         r["home"], r["away"], "", "", "scheduled", ""])

    cols = ["match_id", "date", "stage", "group", "home", "away",
            "home_goals", "away_goals", "status", "winner"]
    out = pd.DataFrame(rows, columns=cols)
    # keep empty group cell for knockout rows blank (not 'nan')
    out["group"] = out["group"].fillna("")
    out.to_csv(MATCHES, index=False, encoding="utf-8")

    # ---- report ----
    ngp = int((out["stage"] == "group").sum())
    nr32_played = int(((out["stage"] == "R32") & (out["status"] == "played")).sum())
    nr32_sched = int(((out["stage"] == "R32") & (out["status"] == "scheduled")).sum())
    print(f"wrote {MATCHES}")
    print(f"  group rows: {ngp} (all played)")
    print(f"  R32: {nr32_played} played + {nr32_sched} scheduled")
    print(f"  best-thirds key = {key} (option_no {br['best_thirds_allocation']['table'][key]['option_no']})")
    print(f"  R32 derivation vs openfootball: {ok}/16 EXACT")
    print("  played-KO winners:")
    for mid in sorted(ko_win):
        w, l = ko_win[mid]
        m = of_r32[mid - 73]
        sc = m["score"]
        pk = "pens" if "p" in sc else ("ET" if ("et" in sc or "aet" in sc) else "90'")
        print(f"    {mid} {m['team1']} v {m['team2']}: winner={w} ({pk})")


if __name__ == "__main__":
    build()
