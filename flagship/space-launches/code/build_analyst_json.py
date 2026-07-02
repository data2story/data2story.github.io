"""
build_analyst_json.py — assembles PROJECT_DIR/analyst.json from:
  - code/derived_tables.json  (data_tables, produced verbatim by analyze.py)
  - the curated prose / based_on / calculation refs below

This is the ASSEMBLER, not analysis: it copies each ana_xx data_table straight
from analyze.py's machine output so the numbers in analyst.json are guaranteed
to match the code (reproducibility mandate). Run AFTER analyze.py.

  set PYTHONUTF8=1
  py code/build_analyst_json.py
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(HERE)
with open(os.path.join(HERE, "derived_tables.json"), encoding="utf-8") as f:
    D = json.load(f)

F = "code/analyze.py"

# finding_id -> (label, type, strength, based_on, lines, output_snippet, data_table_key,
#                content, notable_instance, client_model_ref)
items = {}

def add(fid, label, typ, strength, based_on, lines, output, table_key, content,
        notable=None, client_model=None):
    it = {
        "label": label,
        "content": content,
        "type": typ,
        "strength": strength,
        "calculation": {"file": F, "lines": lines, "output": output},
        "data_table": D[table_key],
        "based_on": based_on,
    }
    if notable:
        it["notable_instance"] = notable
    if client_model:
        it["client_model"] = client_model
    items[fid] = it

add("ana_01", "Census scope: 5,726 launches, 1957-2018, 94% success",
    "distribution", "strong", ["det_01", "det_02", "det_03"], [74, 93],
    "rows (orbital launch attempts): 5726\nyear range: 1957-2018 (62 calendar years)\n"
    "distinct state_code: 17\ndistinct vehicle types: 366\n"
    "success (O): 5384  failure (F): 342  overall success rate: 94.0%\n"
    "agency_type split: {'state': 4776, 'private': 880, 'startup': 70}\n"
    "launch_date typo rows fixed (2918->2018): 1",
    "ana_01",
    "The dataset is a complete census, not a sample: 5,726 orbital launch attempts from the "
    "first ever (Sputnik, 1957) through October 2018, drawn from Jonathan McDowell's JSR catalog. "
    "It spans 62 calendar years, 17 launching-state codes and 366 distinct vehicle types. Overall "
    "5,384 attempts succeeded and 342 failed — a 94.0% all-era success rate. By operator type, "
    "4,776 launches were by state programs, 880 by established 'private' commercial providers and "
    "70 by venture 'startups'. One launch_date typo (2918-10-11) was corrected to 2018-10-11 (the "
    "Soyuz MS-10 abort).")

add("ana_02", "Global launches per year (the 'how much' is roughly flat)",
    "trend", "strong", ["det_05", "det_11"], [98, 109],
    "peak year: 1967 with 139 launches\n2018 (PARTIAL, ends Oct): 80\n"
    "1965 124 / 1967 139 / 1976 131 / 1985 125 / 2009 77 / 2017 90 / 2018 80(partial)",
    "ana_02",
    "Launch volume rose steeply through the early 1960s, then held a Cold-War cruising altitude of "
    "roughly 100-140 launches a year from the mid-1960s to 1990 (single-year peak: 139 in 1967). "
    "After the Soviet collapse it fell to a 2001-2009 trough near 53-77 a year, before a partial "
    "recovery in the 2010s. 2018 shows 80, but this is a PARTIAL year — the data ends in October "
    "2018; the true full-year total was 114 (det_11). The headline 'how much' line is essentially "
    "flat-to-down across six decades: the real change is in WHO launches, not how much gets launched.",
    notable={"name": "1967", "value": "139 launches — the single busiest year on record",
             "why": "the Cold-War cadence peak, against which the 2010s recovery (80-90/yr) still looks modest"})

add("ana_03", "CORE: launches per country per year, 1957-2018 (SU+RU merged)",
    "trend", "strong", ["det_06", "det_12", "det_15"], [114, 130],
    "2014  USSR/Russia 30  USA 24  China 16  Europe 11 ...\n"
    "2016  USSR/Russia 17  USA 22  China 22 ...\n"
    "2017  USSR/Russia 18  USA 30  China 18 ...\n"
    "2018  USSR/Russia 10  USA 27  China 28  Europe 6  Japan 5  India 4  (PARTIAL)",
    "ana_03",
    "This is the spine chart: launches per launching country per year, 1957-2018, with SU+RU merged "
    "into one USSR/Russia series and F+I-ESA+I-ELDO merged into Europe. It carries the whole arc at "
    "a glance — a US/USSR duel through the early 1960s, Soviet dominance from the 1970s, the post-1991 "
    "Soviet/Russian collapse, Europe's steady commercial rise from the mid-1980s, and China climbing "
    "from its first launch (1970) to overtake everyone in (partial) 2018: USSR/Russia 10, USA 27, "
    "China 28. 2018 is partial (Jan-Oct), so its bars are undercounts of the full year.",
    client_model="launchSnapshot")

add("ana_04", "Cumulative ledger: the Cold-War duopoly is still 85% of all launches",
    "ranking", "strong", ["det_04"], [135, 146],
    "USSR/Russia 3178 (55.5%)\nUSA 1716 (30.0%)\nEurope 307 (5.4%)\nChina 302 (5.3%)\n"
    "Japan 115 (2.0%)\nIndia 65 (1.1%)\nOther 43 (0.8%)\nTOTAL 5726",
    "ana_04",
    "Over the full era the Cold-War duopoly still dominates the cumulative ledger: USSR/Russia 3,178 "
    "launches (55.5% of every orbital launch ever) and the USA 1,716 (30.0%) together account for "
    "85.5% of all launches in history. Europe (307, 5.4%) narrowly leads China (302, 5.3%) on the "
    "all-time count — but China's launches are overwhelmingly recent. Japan (115, 2.0%), India "
    "(65, 1.1%) and all others combined (43, 0.8%) form the tail. The cumulative picture is the OLD "
    "world; the per-year picture (ana_03) is the new one.",
    notable={"name": "USSR/Russia", "value": "3,178 launches (55.5% of all-time)",
             "why": "more than half of everything ever launched came from one program lineage — the scale the new contenders are measured against"},
    client_model="cumulativeThrough")

add("ana_05", "China's rise by decade and the 2018 crossover (partial-aware)",
    "trend", "strong", ["det_06", "det_07", "det_11"], [151, 178],
    "China by decade: 1970s 13 / 1980s 15 / 1990s 39 / 2000s 64 / 2010s 171\n"
    "2018 dataset (PARTIAL): China 28, USA 27, USSR/Russia 10\n"
    "external full-year 2018 (det_07): China 39, USA 34, Russia 20, global 114",
    "ana_05",
    "China is the clearest new contender. Its launches climb decade on decade: 13 in the 1970s, 15 "
    "in the 1980s, 39 in the 1990s, 64 in the 2000s and 171 in the 2010s. The crossover lands in "
    "2018: within this partial (Jan-Oct) dataset China already leads with 28 launches to the USA's "
    "27 and Russia's 10. External full-year records (det_07) make it decisive — China 39, USA 34, "
    "Russia 20, of a global 114. Caveat: the dataset's 2018 is truncated, so the 28-27 margin is a "
    "partial-year figure; the full-year margin (39-34) is wider. See ana_19 for the validation.",
    notable={"name": "2018", "value": "China 28 > USA 27 (partial); 39 > 34 (full year)",
             "instance_ref": "", "why": "the first year in the entire 62-year record that China is the world's top launcher"},
    client_model="annualize")

add("ana_06", "National share of launches by decade (no bloc holds a majority by 2010s)",
    "trend", "moderate", ["det_15"], [183, 194],
    "decade  USSR/Russia  USA  China  Europe\n1950 21.2 78.8 0 0\n1980 80.0 13.4 1.3 2.8\n"
    "2000 36.8 33.7 9.8 12.6\n2010 28.3 26.2 23.2 10.9",
    "ana_06",
    "Reframed as shares of the global total, the pluralization is stark. The USSR/Russia share runs "
    "21%->44%->74%->80%->48%->37%->28% across the 1950s-2010s; the US share falls from 79% (1950s) to "
    "a low of 13% (1980s, the Soviet peak) and recovers to 26% (2010s); China rises from ~0 to 23% by "
    "the 2010s; Europe peaks near 13% (2000s). For the first time since the 1950s, no single bloc "
    "holds a majority of launches in the 2010s.")

add("ana_07", "Concentration: the superpower duopoly's share fell from ~99% to 54%",
    "trend", "strong", ["det_15"], [199, 212],
    "decade | top2(US+USSR/Russia)% | HHI(/10000) | countries_active\n"
    "1950s 100.0 6664 2\n1960s 98.9 4940 5\n1980s 93.5 6596 7\n1990s 81.2 3551 7\n"
    "2000s 70.5 2762 7\n2010s 54.5 2193 7",
    "ana_07",
    "The single cleanest measure of 'a duel became a crowd': the two Cold-War superpowers' combined "
    "share of global launches falls from 100% (1950s) and ~99% (1960s) to 93.5% (1980s), 81.2% "
    "(1990s), 70.5% (2000s) and just 54.5% in the 2010s. A 7-group Herfindahl index drops in step "
    "from ~6,600 toward ~2,200. The number of countries launching in a decade rose from 2 to 7. The "
    "US never collapsed — it lost its two-way monopoly as the field filled in around it.",
    notable={"name": "2010s", "value": "US+USSR/Russia = 54.5% (down from ~99%)",
             "why": "the headline structural fact — the superpowers went from owning the field to sharing it"},
    client_model="launchSnapshot")

add("ana_08", "Two commercialization waves: Arianespace (1984) then startups (2006)",
    "trend", "moderate", ["det_08", "det_10"], [217, 238],
    "first appearance: state 1957, private 1984, startup 2006\n"
    "agency_type share by decade (%):\n1990 state 69.1 private 30.9 startup 0\n"
    "2000 state 52.3 private 46.9 startup 0.8\n2010 state 54.9 private 36.3 startup 8.8",
    "ana_08",
    "A new KIND of actor appears late. 'Startup' launches (almost all SpaceX, plus Rocket Lab) first "
    "appear in 2006 and reach 8.8% of all launches in the 2010s. The older 'private' commercial "
    "category (led by Arianespace from 1984) peaked earlier — 30.9% of launches in the 1990s and "
    "46.9% in the 2000s — then fell to 36.3% in the 2010s as STATE launches rebounded (China). So "
    "commercialization is not one monotonic trend: an Arianespace-style commercial wave (1984-2000s) "
    "was followed by a venture-startup wave (2006-), even as a parallel new state surge (China) ran "
    "alongside. 'Private' and 'startup' are genuinely different vintages of actor.")

add("ana_09", "Reliability matured to a 95-97% plateau",
    "trend", "moderate", ["det_13"], [243, 254],
    "decade success rate: 1950s 46.2 / 1960s 87.0 / 1970s 94.9 / 1980s 97.1 / "
    "1990s 95.5 / 2000s 96.8 / 2010s 96.3\nOVERALL: 5384/5726 = 94.0%",
    "ana_09",
    "Launch reliability matured fast then plateaued high: the success rate rose from 46.2% in the "
    "experimental 1950s to 87.0% (1960s), 94.9% (1970s) and a 97.1% peak in the 1980s, holding at "
    "95-97% ever since (96.3% in the 2010s). The all-era rate is 94.0%, dragged down only by the "
    "high-failure pioneering years. Modern orbital launch is a high-reliability activity (det_13).",
    client_model="successRate")

add("ana_10", "Every major power launches at 89-96%; new contenders match incumbents",
    "group-diff", "strong", ["det_13"], [259, 269],
    "Europe 95.8 / China 95.7 / USSR/Russia 95.2 / USA 92.4 / Japan 92.2 / India 89.2 / Other 65.1\n"
    "(China 289/302; USA 1585/1716)",
    "ana_10",
    "Every major launching power clusters in a tight, high-reliability band: Europe 95.8%, China "
    "95.7%, USSR/Russia 95.2%, USA 92.4%, Japan 92.2%, India 89.2%. Only the small 'Other' bucket "
    "(early Israeli, Iranian, Brazilian and North-Korean and other experimental programs) sits low at "
    "65.1%, on just 43 attempts. The crucial point against any 'cutting corners' read: the new "
    "contenders are NOT trading reliability for entry — China's 95.7% matches the incumbents exactly.",
    notable={"name": "China", "value": "95.7% success (289 of 302) — ties the most reliable incumbents",
             "why": "directly rebuts the idea that China's launch surge is lower-quality volume"},
    client_model="successRate")

add("ana_11", "By operator type, commercial 'private' is the most reliable (97.4%)",
    "group-diff", "moderate", ["det_13", "det_08"], [274, 284],
    "private 97.4 (857/880) / state 93.4 (4462/4776) / startup 92.9 (65/70)",
    "ana_11",
    "By operator type the established commercial 'private' providers are actually the MOST reliable at "
    "97.4% (Arianespace-led), state programs 93.4% (they carry every early experimental failure), and "
    "startups 92.9% — competitive despite SpaceX's three early Falcon 1 failures and one Rocket Lab "
    "loss weighing on a small 70-launch base. Reliability does not split cleanly by 'old vs new'.",
    client_model="successRate")

add("ana_12", "Top vehicles are Soviet workhorses; Falcon 9 and Long March rank low all-time",
    "ranking", "moderate", ["det_04"], [289, 296],
    "Soyuz-U 632 / Kosmos 11K65M 445 / Voskhod 11A57 299 / Molniya 8K78M 272 / "
    "Soyuz-U-PVB 154 / Space Shuttle 135 / Ariane 5ECA 67 / Falcon 9 62 / Chang Zheng 2C 44",
    "ana_12",
    "The most-flown individual vehicles are overwhelmingly Soviet workhorses: Soyuz-U (632), Kosmos "
    "11K65M (445), Voskhod 11A57 (299), Molniya 8K78M (272), Soyuz-U-PVB (154), then the US Space "
    "Shuttle (135). The first non-Soviet/non-US high-volume vehicle is Europe's Ariane 5ECA (67); "
    "SpaceX's Falcon 9 (62) and China's Chang Zheng 2C (44) sit far down the all-time list. The new "
    "contenders' vehicles are recent, not yet voluminous — their weight is in the last decade only.")

add("ana_13", "Vehicle families: Soviet fleet (>3,200) still dwarfs Long March (287) and Falcon (68)",
    "ranking", "moderate", ["det_04", "det_06"], [301, 345],
    "R-7/Soyuz 1832 / Thor/Delta 621 / Kosmos 621 / Proton 411 / Atlas 403 / "
    "Tsiklon/Zenit/Dnepr 342 / Long March 287 / Ariane 244 / Titan 215 / Shuttle 135 / "
    "Japanese 108 / Scout 99 / Falcon 68 / Indian 65 / Electron 2",
    "ana_13",
    "Grouped into families, the Soviet/Russian fleet dominates: the R-7/Soyuz family (1,832 launches "
    "in this data), Kosmos (621), Proton (411) and Tsiklon/Zenit/Dnepr (342) together exceed 3,200. "
    "US families follow — Thor/Delta (621), Atlas (403), Titan (215), Space Shuttle (135). China's "
    "Long March family totals 287, Europe's Ariane 244, and SpaceX's Falcon just 68 — small in "
    "cumulative terms but concentrated almost entirely in the final decade of the data. (Family "
    "grouping is defined by the to_family() mapping in analyze.py and is approximate at the margins.)")

add("ana_14", "China's program IS the Long March: 287 of 302 launches (95%)",
    "distribution", "strong", ["det_06"], [350, 363],
    "China on Chang Zheng (Long March): 287 of 302 = 95.0%\n"
    "CZ-2C 44 / CZ-3B 41 / CZ-2D 40 / CZ-4B 30 / CZ-3A 27 / CZ-4C 25",
    "ana_14",
    "China's program is almost entirely one rocket family: 287 of its 302 launches (95.0%) are Long "
    "March (Chang Zheng) vehicles — CZ-2C (44), CZ-3B (41), CZ-2D (40), CZ-4B (30), CZ-3A (27) and so "
    "on. Unlike the diversified US fleet (Thor/Delta, Atlas, Titan, Shuttle, Falcon), China's rise "
    "IS the Long March's rise — a single sovereign family scaling up.",
    notable={"name": "Long March (Chang Zheng)", "value": "287 of 302 Chinese launches (95.0%)",
             "why": "the concentration shows China's ascent is one state rocket program, not a diversified market"})

add("ana_15", "The startup class: SpaceX 68 + Rocket Lab 2, ramping to ~18/yr by 2018",
    "ranking", "strong", ["det_08", "det_09"], [368, 386],
    "startup vehicles: Falcon 9 62 / Falcon 1 5 / Falcon Heavy 1 / Electron 2 (all state_code US)\n"
    "startup by year: 2006 1 ... 2017 19, 2018 18(partial)\nSPX total 68; RLABU 2",
    "ana_15",
    "The 'startup' class totals 70 launches: SpaceX 68 (Falcon 9 62, Falcon 1 5, Falcon Heavy 1) and "
    "Rocket Lab 2 (Electron); all carry state_code US. SpaceX's first launch in the data is 2006 "
    "(Falcon 1); the cadence ramps to 19 launches in 2017 and 18 in partial 2018 — by the dataset's "
    "end SpaceX alone rivals mid-size national programs. Rocket Lab's Electron appears right at the "
    "edge (first orbital flights 2017-2018), marking a second, small-satellite startup axis that runs "
    "orthogonal to the country story.",
    notable={"name": "Falcon 9", "value": "62 of SpaceX's 68 launches; 19 startup launches in 2017",
             "why": "the vehicle that turned 'startup' from a label into a rival to national programs"})

add("ana_16", "Before SpaceX, commercial meant Europe: Arianespace 260 launches",
    "ranking", "moderate", ["det_10"], [391, 406],
    "Arianespace (AE) 260 launches, 1984-2018\ntop 'private' agencies: AE 260, ILSK 97, ULAL 71, "
    "MDSSC 62, OSC 60, ULAB 60, BLS 56, LMA 43",
    "ana_16",
    "Before SpaceX, commercial launch meant Europe. Arianespace (agency AE) flew 260 launches from "
    "1984 to 2018 — the largest single commercial provider in the data, led by Ariane 5ECA (65) and "
    "the Ariane 4 series. The broader 'private' category is led by AE (260), then the Proton marketer "
    "ILS/Khrunichev (ILSK 97), ULA-Atlas (ULAL 71), McDonnell Douglas (MDSSC 62), Orbital (OSC 60), "
    "ULA-Delta (ULAB 60) and Boeing (BLS 56) — mostly established aerospace primes, a different "
    "species from the venture startups of ana_15.")

add("ana_17", "Geography: lat/long are UNUSABLE; only a country choropleth is possible",
    "distribution", "moderate", ["det_14", "det_15"], [411, 430],
    "agencies.csv rows with usable numeric lat/long: 0 of 74  <-- all '-'\n"
    "by state_code: SU 2444, US 1716, RU 734, CN 302, F 291, J 115, IN 65, IL 10, I 9, IR 8, KP 5",
    "ana_17",
    "DATA CAVEAT turned finding: although agencies.csv has latitude/longitude columns, every value is "
    "'-' — 0 of 74 rows carry usable coordinates — so a launch-SITE point map cannot be built from "
    "this data (contrary to the Detective's assumption). A country-level choropleth still works from "
    "launch counts by state_code: Soviet Union 2,444, United States 1,716, Russia 734, China 302, "
    "France/Europe 291, Japan 115, India 65, then a long tail (Israel 10, Italy 9, Iran 8, North "
    "Korea 5, Sea Launch/Cayman 4, South Korea 3, ELDO 3, Brazil 2, UK 2). For a continuous fill, "
    "SU and RU should be merged onto one country (Russia).")

add("ana_18", "Top agencies (caveat: Soviet orgs are uncoded in launches.csv)",
    "ranking", "weak", ["det_12"], [435, 451],
    "'agency' is NaN for 2444 rows (= all SU launches)\n"
    "top coded: US 1202, RU 619, CN 302, AE 260, ILSK 97, J 78, ULAL 71, SPX 68, IN 65, MDSSC 62",
    "ana_18",
    "DATA CAVEAT turned finding: in launches.csv the 'agency' column is blank for all 2,444 Soviet "
    "(SU) launches — Soviet orgs (RVSN, UNKS) are coded only in agencies.csv — so an agency-level "
    "ranking from launches.csv structurally understates the USSR. Among coded agencies the leaders "
    "are the generic US (1,202), RU (619) and CN (302) state codes, then Arianespace (260), "
    "ILS/Khrunichev (97), Japan (78), ULA-Atlas (71), SpaceX (68), India (65) and McDonnell Douglas "
    "(62). For Soviet-era providers use vehicle families (ana_13) instead of this ranking.")

add("ana_19", "VALIDATION: 'China overtakes 2018' holds at partial, annualized AND full-year",
    "ranking", "strong", ["det_07", "det_11"], [456, 479],
    "dataset PARTIAL 2018: China 28 > USA 27 > Russia 10\n"
    "naive annualize x12/10: China ~33.6 > USA ~32.4\n"
    "external full-year: China 39 > USA 34 > Russia 20\n"
    "years China is #1 launcher in whole dataset: [2018]",
    "ana_19",
    "Validation of the 'China overtakes' headline, stated at the right level. WHAT IS VALIDATED: the "
    "per-year COUNT crossover. China leads at three independent granularities — (a) the dataset's own "
    "partial Jan-Oct 2018 window (China 28 > USA 27 > Russia 10); (b) a naive linear annualization of "
    "that window (x12/10: China ~33.6, USA ~32.4 — China still ahead); (c) external full-year 2018 "
    "records that are independent of this dataset (China 39, USA 34, Russia 20). Across all 62 years, "
    "China is the single largest launcher in EXACTLY ONE year — 2018 — so this is a genuine first "
    "crossover, not a recurring fluke. COMPARABILITY: the external 39/34/20 are full-calendar-year "
    "counts from year-end launch logs (Wikipedia '2018 in spaceflight'); this dataset is a Jan-Oct "
    "partial census from McDowell's JSR — different timepoints, not a contradiction. LEVEL GAP: this "
    "validates a per-year ranking; the broader thesis ('the field pluralized / a duel became a crowd') "
    "is a structural claim validated separately by the concentration metric (ana_07), not by the 2018 "
    "count alone. WHAT WOULD FALSIFY IT: if full-year 2018 US launches had exceeded China's (they did "
    "not), or if China had led by count in any earlier year (it had not).",
    client_model="annualize")

add("ana_20", "Launch volume by decade: 1970s peak (1,226), post-Soviet trough (650)",
    "trend", "moderate", ["det_05", "det_11"], [484, 496],
    "1950s 52 / 1960s 982 / 1970s 1226 / 1980s 1191 / 1990s 889 / 2000s 650 / 2010s 736(partial 2018)",
    "ana_20",
    "By decade the volume arc is clear: 52 (1957-59), 982 (1960s), a peak of 1,226 (1970s) and 1,191 "
    "(1980s), then the post-Soviet decline to 889 (1990s) and a 650 trough (2000s), recovering to 736 "
    "in the 2010s (2010-2018, with 2018 partial). The peak DECADE is actually the 1970s, narrowly "
    "above the 1980s; the 1980s figure of 1,191 matches the external benchmark the Detective cited "
    "(det_05), as do the 1990s (889) and 2000s (650).")

# ---------------------------------------------------------------------------
analyst = {
    "meta": {
        "role": "analyst",
        "version": "2.0",
        "dataset": "Economist / 2018-10-20_space-launches",
        "one_line": "Quantitative spine for 'the space race is dominated by new contenders': "
                    "5,726 orbital launches (1957-2018) recomputed from launches.csv, showing WHO "
                    "launches pluralizing (superpower duopoly share 99%->54%) more than HOW MUCH.",
        "reproducibility": "Every number is regenerated by code/analyze.py from launches.csv; "
                           "data_tables are copied verbatim from code/derived_tables.json by "
                           "code/build_analyst_json.py. Client models in code/client_model.js "
                           "(data slice code/client_data.json) recompute headlines in-browser.",
    },
    "dataset": {
        "files": ["launches.csv", "agencies.csv"],
        "rows": 5726,
        "columns": 11,
        "what_one_row_represents": "One orbital launch attempt (success or failure)",
        "time_range": "1957-2018 (2018 PARTIAL — ends October; 80 rows vs 114 full-year)",
        "geographic_scope": "Global; 17 launching-state codes (agencies.csv lat/long are all '-' so "
                            "no point-map coordinates are available — see ana_17)",
    },
    "items": items,
    "client_models": [
        {"name": "launchSnapshot", "file": "code/client_model.js", "serves": ["ana_03", "ana_06", "ana_07"],
         "inputs": {"year": "int 1957-2018"},
         "output": "{counts{country}, total, shares{country}, leader, duopolyShare} for that year",
         "data_slice": "code/client_data.json -> country_year_matrix",
         "note": "Powers the hero year-scrubber launch-race + the 'duel -> crowd' reveal: "
                 "duopolyShare (US+USSR/Russia) falls from 99.2% (1965) to 46.3% (2018)."},
        {"name": "cumulativeThrough", "file": "code/client_model.js", "serves": ["ana_04"],
         "inputs": {"year": "int"},
         "output": "{cum{country}, ranked[[country,total]]} summed 1957..year",
         "data_slice": "country_year_matrix",
         "note": "Cumulative 'who is ahead' bar race; ends USSR/Russia 3178 > USA 1716 > Europe 307."},
        {"name": "successRate", "file": "code/client_model.js", "serves": ["ana_09", "ana_10", "ana_11"],
         "inputs": {"scope": "country|type|decade", "key": "e.g. China / startup / 1980s"},
         "output": "{successes, attempts, rate}",
         "data_slice": "successByCountry / successByType / successByDecade",
         "note": "Powers a success-rate calculator and the verify-layer recompute."},
        {"name": "annualize", "file": "code/client_model.js", "serves": ["ana_05", "ana_19"],
         "inputs": {"partialCount": "int", "monthsElapsed": "int (default 10 = Jan-Oct 2018)"},
         "output": "projected full-year = partialCount*12/monthsElapsed",
         "note": "Lets the reader recompute the partial-2018 caveat honestly (naive pro-rate, NOT a "
                 "forecast): China 28 -> ~33.6 vs external actual 39."},
    ],
    "caveats": [
        {"id": "ana_caveat_01",
         "content": "2018 is a PARTIAL year: the data ends October 2018 with 80 launches vs the 114 "
                    "full-year total. Never compare partial-2018 head-to-head with prior full years "
                    "without annualizing or labelling it partial. The China-overtakes story holds "
                    "anyway (and more strongly at full year) — see ana_19."},
        {"id": "ana_caveat_02",
         "content": "agencies.csv latitude/longitude are ALL '-' (0 of 74 numeric). A launch-SITE "
                    "point map is NOT buildable from this data; only a country-level choropleth from "
                    "state_code counts (ana_17). This contradicts the Detective's lat/long-map "
                    "assumption — flagged for the Designer."},
        {"id": "ana_caveat_03",
         "content": "launches.csv 'agency' is blank (NaN) for all 2,444 Soviet (SU) launches — Soviet "
                    "orgs are coded only in agencies.csv — so agency-level rankings (ana_18) "
                    "understate the USSR. Use vehicle families (ana_13) for Soviet-era providers."},
        {"id": "ana_caveat_04",
         "content": "agencies.csv's precomputed 'count' is stale vs fresh launches.csv row counts "
                    "(SpaceX 65 vs 68, Arianespace 258 vs 260, ULA-Delta 58 vs 60, etc.). ALL counts "
                    "in analyst.json are recomputed from launches.csv; agencies.csv is used only for "
                    "names/metadata."},
        {"id": "ana_caveat_05",
         "content": "Merges applied: SU+RU -> one 'USSR/Russia' series (the same program lineage "
                    "across the 1991 break); F+I-ESA+I-ELDO -> 'Europe' (the ESA/Arianespace bloc). "
                    "Italy (state_code I, the San Marco program) is kept in 'Other', not Europe, as a "
                    "separate national effort."},
        {"id": "ana_caveat_06",
         "content": "Data typo fixed: one launch_date '2918-10-11' -> '2018-10-11' (tag 2018-F01, the "
                    "Soyuz MS-10 abort, a FAILURE). 13 other rows (old failures) have blank "
                    "launch_date but valid launch_year; all year-based analysis uses launch_year and "
                    "is unaffected by the blank dates."},
        {"id": "ana_caveat_07",
         "content": "The 'startup' agency_type is small (70 launches) and US-only here, so its 92.9% "
                    "success rate (ana_11) rests on a thin base; treat startup-vs-incumbent reliability "
                    "comparisons as indicative, not definitive."},
    ],
}

out = os.path.join(PROJECT_DIR, "analyst.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(analyst, f, indent=2, ensure_ascii=False)
print(f"[wrote] {out}")
print(f"[items] {len(items)} ana_xx findings")
print(f"[client_models] {len(analyst['client_models'])}")
print(f"[caveats] {len(analyst['caveats'])}")
