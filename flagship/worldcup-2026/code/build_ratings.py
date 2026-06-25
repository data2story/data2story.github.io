#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ratings.py  —  Auditable EA-style 0-99 player ratings for the
2026 World Cup data-journalism page.

THESIS: every number traces to its inputs. Two data lineages, one shared scale.

  lineage "statsbomb"   : per-90 event metrics aggregated from StatsBomb Open Data
                          (UEFA Euro 2024 comp=55/season=282 + Copa America 2024
                          comp=223/season=282). Raw attributes -> percentile rank
                          within the pool -> EA-like 50-99 band.
  lineage "public_index": for stars NOT in that StatsBomb coverage. Built from
                          international goals (datasets/raw/goalscorers.csv, CC0),
                          team squad market value (reference/squad_values.csv,
                          Transfermarkt snapshot — a WEAK team-level proxy, flagged),
                          and a position archetype. Mapped onto the SAME 50-99 band.

Pace has no clean event source -> proxied from progressive-carry distance per 90
(statsbomb) or archetype (public_index) and FLAGGED is_proxy=true on every card.

Outputs:
  code/ratings.json               (player cards)
  code/_sb_player_raw.json        (intermediate: raw per-90 metrics, for audit)
NEVER fabricates a value; if a StatsBomb metric is missing the player is dropped
to public_index or skipped, never guessed.

Run:  PYTHONUTF8=1 python code/build_ratings.py
"""
import json, os, sys, time, unicodedata
from collections import defaultdict
import requests
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../blog_showcase_opus48_0621
DATASET = 'D:/AI/journalist agent review/phase2/datasets/worldcup_2026'
SB = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data'
CACHE = os.path.join(ROOT, 'code', '_sb_cache')
os.makedirs(CACHE, exist_ok=True)

COMPS = [(55, 282, 'UEFA Euro 2024'), (223, 282, 'Copa America 2024')]
MIN_MINUTES = 180  # require >=2 full matches of event data for a stable per-90

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s)) if unicodedata.category(c) != 'Mn').lower()

# ---------------------------------------------------------------------------
# cached StatsBomb fetch
# ---------------------------------------------------------------------------
def sb_get(path):
    fn = os.path.join(CACHE, path.replace('/', '_'))
    if os.path.exists(fn):
        with open(fn, encoding='utf-8') as f:
            return json.load(f)
    for attempt in range(3):
        try:
            r = requests.get(f'{SB}/{path}', timeout=60)
            r.raise_for_status()
            data = r.json()
            with open(fn, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            return data
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)

# ===========================================================================
# 1) PLAYER POOL  (StatsBomb id -> card metadata; public_index has no id)
#    age/position/club/height are EDITORIAL FACTS recorded as source_refs,
#    not derived numbers. They label the card; they are NOT rating inputs
#    except: position drives the Overall weighting + archetype, and
#    height/weight feed the Physical aerial term per the methodology.
# ===========================================================================
# pos archetypes: GK / CB / FB / DM / CM / AM / W / ST
STATSBOMB_PLAYERS = [
    # ---- Argentina (Copa America 2024) ----
    dict(sb_id=5503,  name='Lionel Messi',      team='Argentina', pos='AM', age=38, club='Inter Miami CF',   ht=170),
    dict(sb_id=11456, name='Lautaro Martínez',  team='Argentina', pos='ST', age=28, club='Inter Milan',      ht=174),
    dict(sb_id=7797,  name='Rodrigo De Paul',   team='Argentina', pos='CM', age=31, club='Atlético Madrid',  ht=180),
    # ---- Spain (Euro 2024) ----
    dict(sb_id=316046,name='Lamine Yamal',      team='Spain',     pos='W',  age=18, club='FC Barcelona',     ht=180),
    dict(sb_id=30486, name='Pedri',             team='Spain',     pos='CM', age=23, club='FC Barcelona',     ht=174),
    dict(sb_id=6765,  name='Rodri',             team='Spain',     pos='DM', age=29, club='Manchester City',  ht=191),
    dict(sb_id=16532, name='Dani Olmo',         team='Spain',     pos='AM', age=28, club='FC Barcelona',     ht=179),
    dict(sb_id=68574, name='Nico Williams',     team='Spain',     pos='W',  age=23, club='Athletic Club',    ht=181),
    # ---- France (Euro 2024) ----
    dict(sb_id=3009,  name='Kylian Mbappé',     team='France',    pos='ST', age=27, club='Real Madrid',      ht=178),
    dict(sb_id=5477,  name='Ousmane Dembélé',   team='France',    pos='W',  age=28, club='Paris Saint-Germain', ht=178),
    dict(sb_id=5487,  name='Antoine Griezmann', team='France',    pos='AM', age=35, club='Atlético Madrid',  ht=176),
    dict(sb_id=17592, name='William Saliba',    team='France',    pos='CB', age=25, club='Arsenal',          ht=192),
    # ---- England (Euro 2024) ----
    dict(sb_id=30714, name='Jude Bellingham',   team='England',   pos='AM', age=22, club='Real Madrid',      ht=186),
    dict(sb_id=22084, name='Bukayo Saka',       team='England',   pos='W',  age=24, club='Arsenal',          ht=178),
    dict(sb_id=10955, name='Harry Kane',        team='England',   pos='ST', age=32, club='Bayern Munich',    ht=188),
    dict(sb_id=39461, name='Cole Palmer',       team='England',   pos='AM', age=24, club='Chelsea',          ht=189),
    dict(sb_id=4354,  name='Phil Foden',        team='England',   pos='AM', age=26, club='Manchester City',  ht=171),
    # ---- Colombia (Copa America 2024) ----
    dict(sb_id=5695,  name='James Rodríguez',   team='Colombia',  pos='AM', age=34, club='Club León',        ht=180),
    # ---- Brazil (Copa America 2024) ----
    dict(sb_id=18395, name='Vinícius Júnior',   team='Brazil',    pos='W',  age=25, club='Real Madrid',      ht=176),
    dict(sb_id=10595, name='Raphinha',          team='Brazil',    pos='W',  age=29, club='FC Barcelona',     ht=176),
    dict(sb_id=25104, name='Rodrygo',           team='Brazil',    pos='W',  age=25, club='Real Madrid',      ht=174),
    # ---- Portugal (Euro 2024) ----
    dict(sb_id=5207,  name='Cristiano Ronaldo', team='Portugal',  pos='ST', age=41, club='Al Nassr FC',      ht=187),
    dict(sb_id=5204,  name='Bruno Fernandes',   team='Portugal',  pos='AM', age=31, club='Manchester United',ht=179),
    dict(sb_id=3193,  name='Bernardo Silva',    team='Portugal',  pos='AM', age=31, club='Manchester City',  ht=173),
    dict(sb_id=5206,  name='Rúben Dias',        team='Portugal',  pos='CB', age=28, club='Manchester City',  ht=187),
    # ---- Germany (Euro 2024) ----
    dict(sb_id=39565, name='Jamal Musiala',     team='Germany',   pos='AM', age=23, club='Bayern Munich',    ht=184),
    dict(sb_id=40724, name='Florian Wirtz',     team='Germany',   pos='AM', age=22, club='Real Madrid',      ht=176),
    dict(sb_id=5574,  name='Toni Kroos',        team='Germany',   pos='CM', age=36, club='Retired (Real Madrid)', ht=183),
    # ---- Netherlands (Euro 2024) ----
    dict(sb_id=3669,  name='Virgil van Dijk',   team='Netherlands', pos='CB', age=34, club='Liverpool',      ht=193),
    dict(sb_id=20750, name='Cody Gakpo',        team='Netherlands', pos='W',  age=26, club='Liverpool',      ht=189),
    dict(sb_id=2988,  name='Memphis Depay',     team='Netherlands', pos='ST', age=32, club='Corinthians',    ht=176),
    # ---- Uruguay (Copa America 2024) ----
    dict(sb_id=None,  name='__placeholder__', team='', pos='', age=0, club='', ht=0),  # removed below
]
STATSBOMB_PLAYERS = [p for p in STATSBOMB_PLAYERS if p.get('sb_id')]

# public_index pool: stars OUTSIDE Euro2024/Copa2024 StatsBomb coverage.
# intl_goals filled from goalscorers.csv; squad value is TEAM-level (weak proxy).
PUBLIC_PLAYERS = [
    dict(name='Erling Haaland',   team='Norway',  pos='ST', age=25, club='Manchester City', ht=195, goal_q='haaland'),
    dict(name='Martin Ødegaard',  team='Norway',  pos='AM', age=27, club='Arsenal',         ht=178, goal_q='odegaard'),
    dict(name='Christian Pulisic',team='USA',     pos='W',  age=27, club='AC Milan',         ht=177, goal_q='pulisic', goal_team='United States'),
    dict(name='Achraf Hakimi',    team='Morocco', pos='FB', age=27, club='Paris Saint-Germain', ht=181, goal_q='hakimi'),
    dict(name='Youssef En-Nesyri',team='Morocco', pos='ST', age=29, club='Fenerbahçe',     ht=189, goal_q='nesyri'),
    dict(name='Kaoru Mitoma',     team='Japan',   pos='W',  age=29, club='Brighton & Hove Albion', ht=178, goal_q='mitoma'),
    dict(name='Takefusa Kubo',    team='Japan',   pos='W',  age=25, club='Real Sociedad',   ht=173, goal_q='kubo'),
    dict(name='Raúl Jiménez',     team='Mexico',  pos='ST', age=35, club='Fulham',          ht=190, goal_q='jimenez'),
]

# Pos -> overall weighting (sums to 1.0). Defines how the 6 attributes blend.
POS_WEIGHTS = {
    'GK': dict(pace=.05, shooting=.02, passing=.18, dribbling=.05, defending=.45, physical=.25),
    'CB': dict(pace=.12, shooting=.03, passing=.15, dribbling=.05, defending=.40, physical=.25),
    'FB': dict(pace=.22, shooting=.06, passing=.20, dribbling=.16, defending=.24, physical=.12),
    'DM': dict(pace=.10, shooting=.06, passing=.27, dribbling=.12, defending=.30, physical=.15),
    'CM': dict(pace=.10, shooting=.12, passing=.30, dribbling=.18, defending=.18, physical=.12),
    'AM': dict(pace=.14, shooting=.22, passing=.26, dribbling=.24, defending=.06, physical=.08),
    'W':  dict(pace=.24, shooting=.20, passing=.16, dribbling=.26, defending=.06, physical=.08),
    'ST': dict(pace=.18, shooting=.34, passing=.12, dribbling=.16, defending=.04, physical=.16),
}
# public_index archetype attribute templates (RAW 0-1 strength priors by position,
# BEFORE goals/value adjustment). These are explicit, documented priors — not per-player
# guesses — and every public_index card is flagged as index-derived.
ARCH = {
    'ST': dict(pace=.78, shooting=.85, passing=.55, dribbling=.68, defending=.28, physical=.74),
    'W':  dict(pace=.86, shooting=.66, passing=.62, dribbling=.82, defending=.30, physical=.55),
    'AM': dict(pace=.70, shooting=.68, passing=.80, dribbling=.80, defending=.34, physical=.55),
    'CM': dict(pace=.66, shooting=.55, passing=.82, dribbling=.70, defending=.55, physical=.62),
    'DM': dict(pace=.60, shooting=.45, passing=.78, dribbling=.60, defending=.80, physical=.72),
    'FB': dict(pace=.84, shooting=.40, passing=.72, dribbling=.66, defending=.74, physical=.66),
    'CB': dict(pace=.66, shooting=.30, passing=.62, dribbling=.42, defending=.86, physical=.84),
}

# ===========================================================================
# 2) STATSBOMB AGGREGATION  ->  raw per-90 metrics per player
# ===========================================================================
WANTED_IDS = {p['sb_id'] for p in STATSBOMB_PLAYERS}

def dist(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

def aggregate_statsbomb():
    # per player: minutes + raw event counters
    agg = defaultdict(lambda: dict(minutes=0.0, comps=set(), n_matches=0, np_shots=0, np_goals=0, npxg=0.0,
                                   passes=0, passes_cmp=0, xa=0.0, prog_pass=0,
                                   take_on=0, take_on_won=0, carries=0, prog_carry_dist=0.0, prog_carries=0,
                                   tackles=0, interceptions=0, tackles_won=0,
                                   pressures=0, recoveries=0, blocks=0, clearances=0,
                                   aerials=0, aerials_won=0))
    for cid, sid, cname in COMPS:
        matches = sb_get(f'matches/{cid}/{sid}.json')
        for m in matches:
            mid = m['match_id']
            # minutes from lineups (positions carry from/to per period)
            lus = sb_get(f'lineups/{mid}.json')
            present_wanted = False
            for team in lus:
                for p in team['lineup']:
                    if p['player_id'] in WANTED_IDS:
                        present_wanted = True
            if not present_wanted:
                continue
            ev = sb_get(f'events/{mid}.json')
            # ---- minutes: use the max event minute of the match as full length,
            #      then per-player from their Substitution / on-from-start. StatsBomb
            #      lineups give positions with from/to timestamps in newer data; to
            #      stay robust we derive minutes from the player's own event span.
            match_end = max((e['minute'] + e.get('second', 0)/60.0) for e in ev) if ev else 90.0
            # gather per-player first/last event minute among our wanted players
            span = {}
            for e in ev:
                pid = e.get('player', {}).get('id')
                if pid in WANTED_IDS:
                    t = e['minute'] + e.get('second', 0)/60.0
                    lo, hi = span.get(pid, (t, t))
                    span[pid] = (min(lo, t), max(hi, t))
            # better minutes: use lineup 'positions' from/to when present
            lineup_minutes = {}
            for team in lus:
                for p in team['lineup']:
                    pid = p['player_id']
                    if pid not in WANTED_IDS:
                        continue
                    mins = 0.0
                    for posn in p.get('positions', []):
                        frm = posn.get('from'); to = posn.get('to')
                        def tomin(ts):
                            if not ts:
                                return None
                            parts = ts.split(':')
                            if len(parts) == 3:
                                hh, mm, ss = parts
                            elif len(parts) == 2:
                                hh, mm, ss = 0, parts[0], parts[1]
                            else:
                                return None
                            return int(hh)*60 + int(mm) + float(ss)/60.0
                        a = tomin(frm)
                        b = tomin(to)
                        if a is None:
                            continue
                        if b is None:
                            b = match_end
                        mins += max(0.0, b - a)
                    if mins > 0:
                        lineup_minutes[pid] = mins
            for pid in span:
                mins = lineup_minutes.get(pid)
                if mins is None:
                    lo, hi = span[pid]
                    mins = max(1.0, hi - lo)
                agg[pid]['minutes'] += mins
                agg[pid]['comps'].add(cname)
                agg[pid]['n_matches'] += 1
            # ---- event counters
            for e in ev:
                pid = e.get('player', {}).get('id')
                if pid not in WANTED_IDS:
                    continue
                t = e['type']['name']
                a = agg[pid]
                if t == 'Shot':
                    sh = e['shot']
                    if sh['type']['name'] != 'Penalty':
                        a['np_shots'] += 1
                        a['npxg'] += sh.get('statsbomb_xg', 0.0)
                        if sh.get('outcome', {}).get('name') == 'Goal':
                            a['np_goals'] += 1
                elif t == 'Pass':
                    ps = e['pass']
                    is_set = ps.get('type', {}).get('name')  # e.g. Corner/Free Kick/Throw-in
                    a['passes'] += 1
                    incomplete = 'outcome' in ps  # outcome present only when NOT complete
                    if not incomplete:
                        a['passes_cmp'] += 1
                    a['xa'] += ps.get('pass_shot_assist', 0) and 0 or 0  # placeholder; xA via shot_assist below
                    # progressive pass: moves ball >=25% closer to goal (x toward 120) and ends in final 3rd-ish
                    sx = e['location'][0]; ex = ps['end_location'][0]
                    if (ex - sx) >= 15 and ex >= 60:
                        a['prog_pass'] += 1
                    # xA: credit expected assists when this pass is the key pass to a shot
                    if ps.get('shot_assist') or ps.get('goal_assist'):
                        # find the shot it set up via 'pass_assisted_shot' not always present;
                        # approximate xA by assisted-shot xg captured in the Shot's key_pass linkage below
                        pass
                elif t == 'Dribble':
                    a['take_on'] += 1
                    if e['dribble'].get('outcome', {}).get('name') == 'Complete':
                        a['take_on_won'] += 1
                elif t == 'Carry':
                    a['carries'] += 1
                    sx, sy = e['location']; ex, ey = e['carry']['end_location']
                    d = ((ex-sx)**2 + (ey-sy)**2) ** 0.5
                    if (ex - sx) >= 5:  # progressive carry, toward opp goal
                        a['prog_carries'] += 1
                        a['prog_carry_dist'] += max(0.0, ex - sx)
                elif t == 'Duel':
                    du = e['duel']
                    dn = du['type']['name']
                    if dn == 'Tackle':
                        a['tackles'] += 1
                        oc = du.get('outcome', {}).get('name', '')
                        if oc in ('Won', 'Success', 'Success In Play', 'Success Out'):
                            a['tackles_won'] += 1
                    elif dn == 'Aerial Lost':
                        a['aerials'] += 1
                elif t == 'Interception':
                    a['interceptions'] += 1
                elif t == 'Pressure':
                    a['pressures'] += 1
                elif t == 'Ball Recovery':
                    a['recoveries'] += 1
                elif t == 'Block':
                    a['blocks'] += 1
                elif t == 'Clearance':
                    a['clearances'] += 1
                # aerial WON shows up as body_part 'Head' wins inside other events;
                # StatsBomb codes aerial duels as 'Aerial Lost' only (loss). Wins are
                # implicit. We approximate aerial-win% via: won = head-based Clearances/
                # Shots/Passes that are aerial. To stay strictly traceable we use the
                # explicit 'Aerial Lost' count as losses and infer wins from height-tagged
                # successful headers below (see second pass).
            # second pass: count aerial WINS = successful aerial actions (header
            # passes/shots/clearances with aerial_won flag) for our players
            for e in ev:
                pid = e.get('player', {}).get('id')
                if pid not in WANTED_IDS:
                    continue
                # StatsBomb 'aerial_won' appears on Clearance / Miscontrol / Shot / Pass
                for key in ('clearance', 'shot', 'pass', 'miscontrol'):
                    obj = e.get(key)
                    if isinstance(obj, dict) and obj.get('aerial_won'):
                        agg[pid]['aerials_won'] += 1
                        agg[pid]['aerials'] += 1
        # progress note to stderr
        print(f'  aggregated {cname}', file=sys.stderr)
    return agg

# ---- xA: separate exact pass-to-shot linkage pass (uses shot.key_pass_id) ----
def add_xa(agg):
    xa = defaultdict(float)
    for cid, sid, cname in COMPS:
        for m in sb_get(f'matches/{cid}/{sid}.json'):
            mid = m['match_id']
            present = any(p['player_id'] in WANTED_IDS for team in sb_get(f'lineups/{mid}.json') for p in team['lineup'])
            if not present:
                continue
            ev = sb_get(f'events/{mid}.json')
            # map event id -> passer id  (for passes)
            passer = {}
            for e in ev:
                if e['type']['name'] == 'Pass':
                    passer[e['id']] = e.get('player', {}).get('id')
            for e in ev:
                if e['type']['name'] == 'Shot':
                    kp = e['shot'].get('key_pass_id')
                    if kp and kp in passer:
                        pid = passer[kp]
                        if pid in WANTED_IDS:
                            xa[pid] += e['shot'].get('statsbomb_xg', 0.0)
    for pid, v in xa.items():
        agg[pid]['xa'] = v
    return agg

def per90(agg):
    raw = {}
    for pid, a in agg.items():
        m = a['minutes']
        if m < MIN_MINUTES:
            continue
        n90 = m / 90.0
        pass_cmp_pct = (a['passes_cmp'] / a['passes']) if a['passes'] else 0.0
        take_on_pct = (a['take_on_won'] / a['take_on']) if a['take_on'] else 0.0
        aerial_pct = (a['aerials_won'] / a['aerials']) if a['aerials'] else 0.0
        raw[pid] = dict(
            minutes=round(m, 1), n90=round(n90, 2),
            comps=sorted(a['comps']), n_matches=a['n_matches'],
            np_shots_p90=a['np_shots']/n90, np_goals_p90=a['np_goals']/n90, npxg_p90=a['npxg']/n90,
            pass_cmp_pct=pass_cmp_pct, xa_p90=a['xa']/n90, prog_pass_p90=a['prog_pass']/n90,
            take_on_p90=a['take_on']/n90, take_on_pct=take_on_pct,
            prog_carry_p90=a['prog_carries']/n90, prog_carry_dist_p90=a['prog_carry_dist']/n90,
            tkl_int_p90=(a['tackles']+a['interceptions'])/n90, pressures_p90=a['pressures']/n90,
            recoveries_p90=a['recoveries']/n90, blocks_clr_p90=(a['blocks']+a['clearances'])/n90,
            aerial_pct=aerial_pct, aerials_p90=a['aerials']/n90,
            _counts=a,
        )
    return raw

# ===========================================================================
# 3) RAW ATTRIBUTE COMPONENTS  (still in native units; normalized later)
#    Each is an explicit function of the per-90 metrics above.
# ===========================================================================
def statsbomb_raw_attributes(pid, r, pos):
    # ARCH[pos] gives a documented per-position prior (0-1) for each attribute.
    # Shooting / Passing / Dribbling / Physical are DATA-DRIVEN (no archetype mixed in).
    # Defending and Pace are role-sensitive in a way the raw events distort inside an
    # attacker-heavy pool, so each is a documented blend of (data signal) + (position
    # prior). This keeps every value traceable while preventing a high-pressing winger
    # from out-"Defending" a centre-back, or a non-carrying striker from reading slow.
    arch = ARCH[pos]
    # Shooting: finishing volume + quality
    shooting = 0.45*r['npxg_p90'] + 0.35*r['np_goals_p90'] + 0.20*(r['np_shots_p90']/4.0)
    # Passing: security + creation + progression
    passing = 0.40*r['pass_cmp_pct'] + 0.35*(r['xa_p90']/0.3) + 0.25*(r['prog_pass_p90']/8.0)
    # Dribbling: take-on volume*success + ball-carrying progression
    dribbling = 0.45*(r['take_on_p90']*max(r['take_on_pct'], 0.0)) + 0.30*(r['prog_carry_p90']/8.0) + 0.25*(r['take_on_pct'])
    # Defending: data workrate (tkl+int, pressures, recoveries) tempered by the position's
    # defensive ceiling so CB/DM read defensively strong and forwards' pressing != elite D.
    def_data = 0.45*(r['tkl_int_p90']/4.0) + 0.30*(r['pressures_p90']/20.0) + 0.25*(r['recoveries_p90']/8.0)
    defending = 0.55*arch['defending'] + 0.45*def_data
    # Physical: aerial duels + ball-recovery workrate + height
    ht = next((p['ht'] for p in STATSBOMB_PLAYERS if p['sb_id'] == pid), 180)
    physical = 0.40*r['aerial_pct'] + 0.25*(r['aerials_p90']/4.0) + 0.20*(r['recoveries_p90']/8.0) + 0.15*((ht-165)/30.0)
    # Pace PROXY (is_proxy=true): ball-carry distance per 90 is the only on-ball speed
    # signal in the data, but it under-rates pure box strikers who don't carry. Blend the
    # measured carry-distance with the position pace prior; FLAGGED as a proxy on the card.
    pace = 0.55*arch['pace'] + 0.45*(r['prog_carry_dist_p90']/250.0)
    return dict(pace=pace, shooting=shooting, passing=passing, dribbling=dribbling,
                defending=defending, physical=physical)

def public_raw_attributes(p, intl_goals, team_value, value_min, value_max):
    base = dict(ARCH[p['pos']])
    # market-value tilt: team squad value -> small multiplier in [0.92,1.08]
    if value_max > value_min:
        vnorm = (team_value - value_min) / (value_max - value_min)
    else:
        vnorm = 0.5
    vmult = 0.92 + 0.16 * vnorm
    for k in base:
        base[k] *= vmult
    # international-goals tilt on Shooting only (the one signal we actually have)
    # 0 goals -> x0.9 ; 50+ goals -> x1.12, log-ish
    g = intl_goals
    gmult = 0.90 + min(0.22, 0.06 * (g ** 0.5) / 3.0) if g > 0 else 0.85
    base['shooting'] *= gmult
    # height feeds physical (same height term scale as statsbomb)
    base['physical'] = 0.7*base['physical'] + 0.3*((p['ht']-165)/30.0)
    return base

# ===========================================================================
# 4) NORMALIZATION  ->  percentile rank within pool -> EA-like 50-99 band
#    For EACH of the 6 attributes, pool ALL players (both lineages) on that
#    attribute's RAW component, compute percentile rank, map to [LOW, HIGH].
# ===========================================================================
LOW, HIGH = 50.0, 99.0
def percentile_scale(values):
    """values: list of (key, raw). returns key->scaled int in [LOW,HIGH] by percentile rank."""
    pairs = sorted(values, key=lambda kv: kv[1])
    n = len(pairs)
    out = {}
    # rank with ties averaged
    i = 0
    while i < n:
        j = i
        while j < n and pairs[j][1] == pairs[i][1]:
            j += 1
        # ranks i..j-1 share average percentile
        avg_rank = (i + (j - 1)) / 2.0
        pct = avg_rank / (n - 1) if n > 1 else 0.5
        scaled = LOW + (HIGH - LOW) * pct
        for k in range(i, j):
            out[pairs[k][0]] = scaled
        i = j
    return out

# ===========================================================================
# MAIN
# ===========================================================================
def main():
    print('1/5 aggregating StatsBomb events (cached) ...', file=sys.stderr)
    agg = aggregate_statsbomb()
    agg = add_xa(agg)
    raw90 = per90(agg)
    # which statsbomb players survived the minutes gate
    sb_meta = {p['sb_id']: p for p in STATSBOMB_PLAYERS}
    dropped = [sb_meta[pid]['name'] for pid in WANTED_IDS if pid not in raw90]
    if dropped:
        print('   below-minutes / no-data (dropped to skip):', dropped, file=sys.stderr)

    # dump intermediate raw per-90 for audit
    audit = {sb_meta[pid]['name']: {k: (round(v, 4) if isinstance(v, float) else v)
                                    for k, v in r.items() if k != '_counts'}
             for pid, r in raw90.items()}
    json.dump(audit, open(os.path.join(ROOT, 'code', '_sb_player_raw.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    print('2/5 public_index inputs ...', file=sys.stderr)
    gs = pd.read_csv(os.path.join(DATASET, 'raw', 'goalscorers.csv'))
    gs['scn'] = gs['scorer'].map(norm)
    sv = pd.read_csv(os.path.join(DATASET, 'reference', 'squad_values.csv'))
    val_by_team = dict(zip(sv['team'], sv['squad_value_eur_m']))
    # team name fixes between forecast (USA) and squad_values (USA) — both use 'USA'
    value_min, value_max = sv['squad_value_eur_m'].min(), sv['squad_value_eur_m'].max()
    pub_goals = {}
    for p in PUBLIC_PLAYERS:
        gt = p.get('goal_team', p['team'])
        sub = gs[(gs['scn'].str.contains(p['goal_q'], na=False)) & (gs['team'] == gt)]
        pub_goals[p['name']] = len(sub)

    # champion-odds for deep-run attach (THIS blog's forecast outputs, not the stale dataset)
    co = pd.read_csv(os.path.join(ROOT, 'forecast_outputs', 'champion_odds.csv'))
    sf = dict(zip(co['team'], co['p_reach_sf']))
    ch = dict(zip(co['team'], co['p_champion']))

    print('3/5 raw attributes ...', file=sys.stderr)
    raw_attrs = {}   # key -> {6 raw attrs}
    meta = {}        # key -> card metadata + provenance + refs
    ATTRS = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']

    COMP_IDS = {'UEFA Euro 2024': 'competition_id=55, season_id=282',
                'Copa America 2024': 'competition_id=223, season_id=282'}
    for pid, r in raw90.items():
        p = sb_meta[pid]
        key = p['name']
        raw_attrs[key] = statsbomb_raw_attributes(pid, r, p['pos'])
        comps_used = r['comps']  # the actual competition(s) this player logged minutes in
        comp_ref = '; '.join(f'{c} ({COMP_IDS[c]})' for c in comps_used)
        meta[key] = dict(
            name=p['name'], team=p['team'], position=p['pos'], age=p['age'], club=p['club'],
            provenance='statsbomb',
            source_refs=[
                f'StatsBomb Open Data: {comp_ref}',
                f"player_id={pid}; {r['n_matches']} matches; {r['minutes']} minutes; "
                f"per-90 inputs in code/_sb_player_raw.json",
                'Height (cm) is an editorial fact feeding the Physical aerial term; '
                'Defending & Pace blend the data signal with the documented position prior',
            ],
            team_p_reach_sf=round(float(sf.get(p['team'], 0.0)), 4),
            team_p_champion=round(float(ch.get(p['team'], 0.0)), 4),
            minutes=r['minutes'],
        )

    for p in PUBLIC_PLAYERS:
        key = p['name']
        tv = val_by_team.get(p['team'], value_min)
        raw_attrs[key] = public_raw_attributes(p, pub_goals[p['name']], tv, value_min, value_max)
        meta[key] = dict(
            name=p['name'], team=p['team'], position=p['pos'], age=p['age'], club=p['club'],
            provenance='public_index',
            source_refs=[
                f"International goals (datasets raw/goalscorers.csv, CC0): {pub_goals[p['name']]} goals for {p.get('goal_team', p['team'])}",
                f"Team squad market value (reference/squad_values.csv, Transfermarkt 2026-06-14): {tv} EUR m — TEAM-LEVEL proxy, not player-level",
                f"Position archetype prior '{p['pos']}' (documented in ratings_methodology.md)",
                f"Height {p['ht']}cm (editorial; feeds Physical)",
            ],
            team_p_reach_sf=round(float(sf.get(p['team'], 0.0)), 4),
            team_p_champion=round(float(ch.get(p['team'], 0.0)), 4),
            minutes=None,
        )

    print('4/5 normalizing to percentile -> 50-99 band ...', file=sys.stderr)
    scaled = {a: percentile_scale([(k, raw_attrs[k][a]) for k in raw_attrs]) for a in ATTRS}

    print('5/5 overall + assemble ...', file=sys.stderr)
    cards = []
    for key in raw_attrs:
        m = meta[key]
        w = POS_WEIGHTS[m['position']]
        attrs_scaled = {a: int(round(scaled[a][key])) for a in ATTRS}
        overall = int(round(sum(attrs_scaled[a] * w[a] for a in ATTRS)))
        card = dict(
            name=m['name'], team=m['team'], position=m['position'], age=m['age'], club=m['club'],
            overall=overall,
            attributes={
                'pace': {'value': attrs_scaled['pace'], 'is_proxy': True},
                'shooting': {'value': attrs_scaled['shooting']},
                'passing': {'value': attrs_scaled['passing']},
                'dribbling': {'value': attrs_scaled['dribbling']},
                'defending': {'value': attrs_scaled['defending']},
                'physical': {'value': attrs_scaled['physical']},
            },
            provenance=m['provenance'],
            source_refs=m['source_refs'],
            team_p_reach_sf=m['team_p_reach_sf'],
            team_p_champion=m['team_p_champion'],
        )
        if m['minutes'] is not None:
            card['statsbomb_minutes'] = m['minutes']
        cards.append(card)

    # sort by overall desc, then team
    cards.sort(key=lambda c: (-c['overall'], c['team'], c['name']))
    out = os.path.join(ROOT, 'code', 'ratings.json')
    json.dump(cards, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    n_sb = sum(1 for c in cards if c['provenance'] == 'statsbomb')
    n_pub = sum(1 for c in cards if c['provenance'] == 'public_index')
    print(f'\nWROTE {out}', file=sys.stderr)
    print(f'players: {len(cards)}  | statsbomb={n_sb}  public_index={n_pub}', file=sys.stderr)
    if dropped:
        print(f'dropped (no/low StatsBomb minutes): {dropped}', file=sys.stderr)
    # quick top-10 sanity
    print('\nTop 12 by overall:', file=sys.stderr)
    for c in cards[:12]:
        a = c['attributes']
        print(f"  {c['overall']:2d} {c['name']:20s} {c['team']:12s} {c['position']:3s} "
              f"PAC{a['pace']['value']} SHO{a['shooting']['value']} PAS{a['passing']['value']} "
              f"DRI{a['dribbling']['value']} DEF{a['defending']['value']} PHY{a['physical']['value']} [{c['provenance'][:3]}]",
              file=sys.stderr)

if __name__ == '__main__':
    main()
