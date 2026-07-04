"""
Data2Story Analyst -- Elo engine + Cape Verde's football trajectory.

ana_12  Cape Verde's Elo trajectory 1979-2026 (year-end rating + world rank)
ana_13  Win rate by decade
ana_14  The WC2026 arc match by match (pre-match ratings + Elo win expectancy)
ana_15  Biggest upsets in international football by Elo gap; Cape Verde's own
ana_16  Rating rank vs population rank: the smallest country in the Elo top 60

ELO SPEC (World Football Elo Ratings convention, eloratings.net):
  R_new = R_old + K * G * (W - We),  We = 1 / (10 ** (-dr/400) + 1)
  dr = R_team(+100 if home & not neutral) - R_opp(+100 if home & not neutral)
  K by tournament: FIFA World Cup finals 60; continental finals (Euro, Copa
  America, AFCON, Asian Cup, Gold Cup/CONCACAF Champ, Oceania Nations Cup,
  Confederations Cup) 50; qualifiers + Nations Leagues 40; other tournaments 30;
  friendlies 20.
  G (goal-difference multiplier): 1 if margin<=1; 1.5 if margin==2;
  (11+margin)/8 if margin>=3.
  All teams start at 1500 on first appearance. Scores are FT-incl-extra-time,
  shootouts recorded as draws (dataset convention) -> W=0.5.
  Scheduled fixtures with NaN scores are dropped. Deterministic, single pass.

Run:  py elo_ratings.py     (PYTHONUTF8=1; deterministic, local files only)
"""
import os
import pandas as pd

DATA_DIR = os.environ.get(
    "DATA_DIR", r"D:\AI\journalist agent review\phase2\data\cape-verde-diaspora"
)
P = lambda *a: os.path.join(DATA_DIR, *a)

CONTINENTAL_FINALS = {
    "African Cup of Nations", "Copa América", "UEFA Euro", "AFC Asian Cup",
    "Gold Cup", "CONCACAF Championship", "Oceania Nations Cup", "Confederations Cup",
}
NATIONS_LEAGUES = {"UEFA Nations League", "CONCACAF Nations League"}

def k_factor(t):
    if t == "FIFA World Cup":
        return 60
    if "qualification" in t or t in NATIONS_LEAGUES:
        return 40
    if t in CONTINENTAL_FINALS:
        return 50
    if t == "Friendly":
        return 20
    return 30

def goal_mult(margin):
    if margin <= 1:
        return 1.0
    if margin == 2:
        return 1.5
    return (11 + margin) / 8

def load_played():
    f = pd.read_csv(P("03_football", "international_results.csv"))
    f = f.dropna(subset=["home_score", "away_score"]).copy()
    f = f.sort_values(["date"], kind="mergesort").reset_index(drop=True)
    return f

def run_elo(df):
    """Single chronological pass. Returns df + pre/post rating & prior-match-count
    columns, plus final {team: rating}, {team: matches}, {team: last_date}."""
    R, N, LAST = {}, {}, {}
    cols = {c: [] for c in ["pre_home", "pre_away", "post_home", "post_away",
                            "n_home", "n_away"]}
    for row in df.itertuples(index=False):
        h, a = row.home_team, row.away_team
        rh, ra = R.get(h, 1500.0), R.get(a, 1500.0)
        cols["pre_home"].append(rh); cols["pre_away"].append(ra)
        cols["n_home"].append(N.get(h, 0)); cols["n_away"].append(N.get(a, 0))
        adv = 0 if row.neutral else 100
        dr = (rh + adv) - ra
        we_h = 1 / (10 ** (-dr / 400) + 1)
        margin = abs(row.home_score - row.away_score)
        w_h = 1.0 if row.home_score > row.away_score else (0.0 if row.home_score < row.away_score else 0.5)
        delta = k_factor(row.tournament) * goal_mult(margin) * (w_h - we_h)
        R[h], R[a] = rh + delta, ra - delta
        N[h] = N.get(h, 0) + 1; N[a] = N.get(a, 0) + 1
        LAST[h] = row.date; LAST[a] = row.date
        cols["post_home"].append(R[h]); cols["post_away"].append(R[a])
    out = df.copy()
    for c, v in cols.items():
        out[c] = v
    return out, R, N, LAST

def fifa_family(df):
    """Teams that ever played World Cup or WC qualification -- a data-driven
    proxy for FIFA members, excluding hobby/non-FIFA teams (Jersey, Basque
    Country, ...) that otherwise pollute rank pools."""
    wc = df[df.tournament.isin(["FIFA World Cup", "FIFA World Cup qualification"])]
    return set(wc.home_team) | set(wc.away_team)

if __name__ == "__main__":
    df = load_played()
    elo, R, N, LAST = run_elo(df)
    FIFA = fifa_family(df)
    CV = "Cape Verde"
    is_cv_h, is_cv_a = elo.home_team == CV, elo.away_team == CV
    cv = elo[is_cv_h | is_cv_a].copy()
    cv["cv_pre"] = elo.pre_home.where(is_cv_h, elo.pre_away)
    cv["cv_post"] = elo.post_home.where(is_cv_h, elo.post_away)
    cv["opp"] = elo.away_team.where(is_cv_h, elo.home_team)
    cv["opp_pre"] = elo.pre_away.where(is_cv_h, elo.pre_home)
    cv["cv_score"] = elo.home_score.where(is_cv_h, elo.away_score)
    cv["opp_score"] = elo.away_score.where(is_cv_h, elo.home_score)
    cv["res"] = ["W" if s > o else ("D" if s == o else "L")
                 for s, o in zip(cv.cv_score, cv.opp_score)]

    # --- ana_12: Cape Verde's Elo trajectory 1979-2026 ---
    print("=== ana_12 ===")
    first = cv.iloc[0]
    print(f"first recorded match: {first.date} {first.home_team} {int(first.home_score)}-"
          f"{int(first.away_score)} {first.away_team} ({first.tournament})")
    modern = cv[cv.date >= "1979"]
    print(f"matches: {len(cv)} total ({len(modern)} from the 1979 debut on; "
          f"1 colonial-era friendly in 1959)")
    peak = cv.loc[cv.cv_post.idxmax()]
    print(f"PEAK rating: {peak.cv_post:.0f} on {peak.date} "
          f"(after {peak.home_team} {int(peak.home_score)}-{int(peak.away_score)} "
          f"{peak.away_team}, {peak.tournament})")
    print(f"rating after final data match ({cv.iloc[-1].date}): {cv.iloc[-1].cv_post:.0f}")
    # year-end rating + rank among established, active teams
    yr_rows = []
    R2, N2, LAST2 = {}, {}, {}
    year_marks = sorted(set(int(d[:4]) for d in cv.date if int(d[:4]) >= 1979))
    dfi = list(df.itertuples(index=False))
    idx = 0
    for y in year_marks:
        end = f"{y}-12-31"
        while idx < len(dfi) and dfi[idx].date <= end:
            row = dfi[idx]
            h, a = row.home_team, row.away_team
            rh, ra = R2.get(h, 1500.0), R2.get(a, 1500.0)
            adv = 0 if row.neutral else 100
            we_h = 1 / (10 ** (-((rh + adv) - ra) / 400) + 1)
            margin = abs(row.home_score - row.away_score)
            w_h = 1.0 if row.home_score > row.away_score else (0.0 if row.home_score < row.away_score else 0.5)
            delta = k_factor(row.tournament) * goal_mult(margin) * (w_h - we_h)
            R2[h], R2[a] = rh + delta, ra - delta
            N2[h] = N2.get(h, 0) + 1; N2[a] = N2.get(a, 0) + 1
            LAST2[h] = row.date; LAST2[a] = row.date
            idx += 1
        if CV not in R2:
            continue
        pool = {t: r for t, r in R2.items()
                if N2[t] >= 10 and LAST2[t] >= f"{y - 3}-01-01" and t in FIFA}
        rank = 1 + sum(r > R2[CV] for r in pool.values())
        yr_rows.append((y, round(R2[CV]), rank, len(pool)))
    print("year-end rating + world rank (established teams: >=10 matches, active <=4y):")
    print("year rating rank pool")
    for y, r_, rk_, np_ in yr_rows:
        print(f"{y} {r_} {rk_} {np_}")

    # --- ana_13: win rate by decade ---
    print("=== ana_13 ===")
    cv["decade"] = (cv.date.str[:4].astype(int) // 10) * 10
    dec = cv.groupby("decade").res.value_counts().unstack(fill_value=0)
    for c in ["W", "D", "L"]:
        if c not in dec:
            dec[c] = 0
    dec["P"] = dec[["W", "D", "L"]].sum(axis=1)
    dec["win_pct"] = (dec.W / dec.P * 100).round(1)
    dec["unbeaten_pct"] = ((dec.W + dec.D) / dec.P * 100).round(1)
    print(dec[["P", "W", "D", "L", "win_pct", "unbeaten_pct"]].to_string())

    # --- ana_14: the WC2026 arc match by match ---
    print("=== ana_14 ===")
    wc = cv[(cv.tournament == "FIFA World Cup")]
    for r_ in wc.itertuples(index=False):
        we = 1 / (10 ** (-(r_.cv_pre - r_.opp_pre) / 400) + 1)  # all neutral venues
        print(f"{r_.date} vs {r_.opp}: {int(r_.cv_score)}-{int(r_.opp_score)} {r_.res} | "
              f"CV pre-Elo {r_.cv_pre:.0f} vs {r_.opp_pre:.0f} | "
              f"Elo expectancy {we * 100:.1f}% | post {r_.cv_post:.0f} "
              f"({r_.cv_post - r_.cv_pre:+.0f})")
    g = wc[wc.date <= "2026-06-27"]
    print(f"group stage: {sum(g.res == 'W')}W-{sum(g.res == 'D')}D-{sum(g.res == 'L')}L, "
          f"goals {int(g.cv_score.sum())}-{int(g.opp_score.sum())}")
    print(f"Elo change across the tournament: "
          f"{wc.iloc[0].cv_pre:.0f} -> {wc.iloc[-1].cv_post:.0f} "
          f"({wc.iloc[-1].cv_post - wc.iloc[0].cv_pre:+.0f})")

    # --- ana_15: biggest upsets by Elo gap (both teams >=30 prior matches) ---
    print("=== ana_15 ===")
    e = elo[(elo.n_home >= 30) & (elo.n_away >= 30)].copy()
    hw = e.home_score > e.away_score
    aw = e.away_score > e.home_score
    e = e[hw | aw].copy()
    home_won = e.home_score > e.away_score
    adv = (~e.neutral) * 100
    e["winner"] = e.home_team.where(home_won, e.away_team)
    e["loser"] = e.away_team.where(home_won, e.home_team)
    e["w_pre"] = e.pre_home.where(home_won, e.pre_away)
    e["l_pre"] = e.pre_away.where(home_won, e.pre_home)
    e["gap"] = ((e.pre_away + 0) - (e.pre_home + adv)).where(home_won,
               (e.pre_home + adv) - (e.pre_away + 0))  # adjusted loser - winner
    e["w_score"] = e.home_score.where(home_won, e.away_score).astype(int)
    e["l_score"] = e.away_score.where(home_won, e.home_score).astype(int)
    ups = e.sort_values("gap", ascending=False).head(12)
    print("top 12 upsets all-time (adjusted Elo gap = loser(+home adv) - winner):")
    for r_ in ups.itertuples(index=False):
        print(f"  {r_.date} {r_.winner} beat {r_.loser} "
              f"{r_.w_score}-{r_.l_score} ({r_.tournament}) "
              f"gap {r_.gap:.0f} [{r_.w_pre:.0f} vs {r_.l_pre:.0f}]")
    cv_ups = e[(e.winner == CV) & (e.gap > 0)].sort_values("gap", ascending=False).head(5)
    print("Cape Verde's biggest Elo upsets:")
    for r_ in cv_ups.itertuples(index=False):
        print(f"  {r_.date} beat {r_.loser} {r_.w_score}-{r_.l_score} "
              f"({r_.tournament}) gap {r_.gap:.0f}")
    pt_gap = float(cv_ups.iloc[0].gap)
    print(f"rank of the 2015 Portugal win (gap {pt_gap:.0f}) among all "
          f"{len(e):,} decided matches: #{int((e.gap > pt_gap).sum()) + 1}")
    wc_ups = e[e.tournament == "FIFA World Cup"].sort_values("gap", ascending=False).head(5)
    print("biggest FIFA World Cup FINALS upsets by Elo gap:")
    for r_ in wc_ups.itertuples(index=False):
        print(f"  {r_.date} {r_.winner} beat {r_.loser} {r_.w_score}-{r_.l_score} "
              f"gap {r_.gap:.0f}")
    last_wc = cv[cv.date == "2026-07-03"].iloc[0]
    arg_gap = last_wc.opp_pre - last_wc.cv_pre  # neutral venue, no adv
    n_bigger = int((e.gap > arg_gap).sum())
    n_bigger_wc = int((e[e.tournament == "FIFA World Cup"].gap > arg_gap).sum())
    print(f"hypothetical: beating Argentina (pre-match gap {arg_gap:.0f}) would have ranked "
          f"~#{n_bigger + 1} among {len(e):,} decided matches between established teams, "
          f"and #{n_bigger_wc + 1} among World Cup FINALS upsets")

    # --- ana_16: rating rank vs population rank ---
    print("=== ana_16 ===")
    pool = {t: r for t, r in R.items()
            if N[t] >= 30 and LAST[t] >= "2024-01-01" and t in FIFA}
    board = sorted(pool.items(), key=lambda kv: -kv[1])
    cv_rank = [t for t, _ in board].index(CV) + 1
    print(f"current Elo (post {max(d for d in df.date)} data, FIFA-family teams): "
          f"Cape Verde {R[CV]:.0f} = rank #{cv_rank} of {len(board)} active teams "
          f"(top {cv_rank / len(board) * 100:.0f}%)")
    pop = pd.read_csv(P("04_population", "population_total_tidy.csv"))
    meta = pd.read_csv(P("04_population",
                         "Metadata_Country_API_SP.POP.TOTL_DS2_EN_csv_v2_3107.csv"),
                       encoding="utf-8-sig")
    countries = set(meta[meta.Region.notna()]["Country Code"])
    p25 = pop[(pop.year == 2025) & (pop["Country Code"].isin(countries))]
    by_name = p25.set_index("Country Name").population
    TEAM_TO_WB = {
        "United States": "United States", "South Korea": "Korea, Rep.",
        "North Korea": "Korea, Dem. People's Rep.", "Iran": "Iran, Islamic Rep.",
        "Ivory Coast": "Cote d'Ivoire", "Egypt": "Egypt, Arab Rep.",
        "Turkey": "Turkiye", "Russia": "Russian Federation",
        "Czech Republic": "Czechia", "Venezuela": "Venezuela, RB",
        "DR Congo": "Congo, Dem. Rep.", "Republic of Ireland": "Ireland",
        "Cape Verde": "Cabo Verde", "Curaçao": "Curacao",
        "Slovakia": "Slovak Republic", "Syria": "Syrian Arab Republic",
        "Kyrgyzstan": "Kyrgyz Republic", "Gambia": "Gambia, The",
        "Congo": "Congo, Rep.", "Laos": "Lao PDR", "Vietnam": "Viet Nam",
    }
    print(f"Elo top {cv_rank} with 2025 population (n/a = no WB row, e.g. UK nations):")
    rows16 = []
    for i, (t, r_) in enumerate(board[:cv_rank], 1):
        wbn = TEAM_TO_WB.get(t, t)
        p_ = int(by_name[wbn]) if wbn in by_name.index else None
        rows16.append((i, t, round(r_), p_))
        print(f"  #{i} {t} {r_:.0f} pop={p_ if p_ is not None else 'n/a'}")
    above = [x for x in rows16 if x[3] is not None and x[0] < cv_rank]
    min_above = min(above, key=lambda x: x[3])
    print(f"smallest-population team ranked ABOVE Cape Verde: {min_above[1]} "
          f"(#{min_above[0]}, pop {min_above[3]:,}) -> Cape Verde is the "
          f"least-populous team in the world's Elo top {cv_rank}")
    cv_pop = int(by_name["Cabo Verde"])
    smaller_ranked = [(i, t, r_, p_) for i, (t, r_) in enumerate(board, 1)
                      if (lambda w: w in by_name.index and by_name[w] < cv_pop)
                      (TEAM_TO_WB.get(t, t))]
    nxt = smaller_ranked[0] if smaller_ranked else None
    if nxt:
        print(f"first team with a SMALLER population on the board: {nxt[1]} "
              f"at rank #{nxt[0]} (Elo {nxt[2]:.0f})")
    pop_sorted = p25.sort_values("population").reset_index(drop=True)
    cv_pop_rank = int(pop_sorted[pop_sorted["Country Code"] == "CPV"].index[0]) + 1
    print(f"population rank: Cabo Verde #{cv_pop_rank} smallest of {len(pop_sorted)} "
          f"WB countries (bottom {cv_pop_rank / len(pop_sorted) * 100:.0f}%)")
