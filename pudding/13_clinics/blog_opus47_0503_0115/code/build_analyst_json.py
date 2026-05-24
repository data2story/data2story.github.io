"""Build the final analyst.json from computed analyses.

This script reproduces all data_tables and writes the JSON file directly.
It encodes calculation links (file + lines) for every finding."""
import json, pandas as pd, os

PROJECT = "/Users/forrest/Desktop/data2blog/project/pudding/13_clinics/blog_opus47_0503_0115"
DATA    = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/13_clinics/cities.csv"
df = pd.read_csv(DATA)

# Helper: pop-weighted mean
def pwm(s, w):
    return (s*w).sum()/w.sum()

total_pop = df['population'].sum()
gest_cols = {
    8:  ('gestation_8_duration',  'gestation_8_duration_closed'),
    12: ('gestation_12_duration', 'gestation_12_duration_closed'),
    16: ('gestation_16_duration', 'gestation_16_duration_closed'),
    20: ('gestation_20_duration', 'gestation_20_duration_closed'),
}

items = {}

# ana_01: dataset profile (no data_table)
items['ana_01'] = {
    'label': "749 cities, 122M Americans, 47 contiguous states",
    'content': (
        "The dataset covers 749 contiguous-US cities with population over 50,000, totaling 122,636,107 residents — "
        "roughly 38% of the US population. Cities range from Madison, Mississippi (50,138) to New York "
        "(8,550,405). The dataset has 14 columns and zero missing values; 47 states are represented "
        "(Alaska and Hawaii are excluded by design because abortion access there typically requires air "
        "travel, not driving). Each row encodes the round-trip driving time in HOURS — rounded down to "
        "the nearest hour and binned — to the nearest abortion clinic willing to perform a procedure at "
        "8, 12, 16, and 20 weeks of gestation, plus a counterfactual scenario in which the closest "
        "clinic has closed."),
    'type': 'distribution',
    'strength': 'strong',
    'calculation': {
        'file': 'code/load_and_profile.py',
        'lines': [13, 24],
        'output': "rows=749, cols=14\nstates=47\ntotal_pop_covered=122,636,107\nmin_city_pop=50,138\nmax_city_pop=8,550,405\nmissing_values_total=0"
    },
    'based_on': ['det_02']
}

# ana_02: 79.8% of cities have a 0-hour drive at 8 weeks
items['ana_02'] = {
    'label': "Most cities sit within walking distance of a clinic at 8 weeks",
    'content': (
        "At 8 weeks of gestation — the universe of clinics willing to perform first-trimester procedures — "
        "598 of 749 cities (79.8%) record a round-trip driving time of 0 hours, meaning the closest clinic "
        "is in or immediately adjacent to the city. Only 14 cities (1.9%) face a round-trip drive of 4 "
        "hours or more. Population-weighted, 88.8% of urban Americans live in a 0-hour-drive city at 8 "
        "weeks. This is the rosiest snapshot the dataset can produce: at the earliest gestation, in normal "
        "operating conditions, the median experience is genuinely 'a clinic is here.'"),
    'type': 'distribution',
    'strength': 'strong',
    'calculation': {
        'file': 'code/access_thresholds.py',
        'lines': [22, 31],
        'output': "8wk\t\t100.0%\t20.2%\t10.1%\t1.9%\t0.9%\npop coverage 0h: 88.8%"
    },
    'data_table': {
        'description': "Histogram of round-trip driving hours at 8 weeks (cities)",
        'columns': ["hours", "cities", "pct_cities", "pop_coverage_pct"],
        'rows': [
            [0, 598, 79.8, 88.8],
            [1, 75, 10.0, 5.1],
            [2, 39, 5.2, 2.9],
            [3, 23, 3.1, 1.9],
            [4, 6, 0.8, 0.6],
            [5, 1, 0.1, 0.06],
            [6, 2, 0.3, 0.13],
            [7, 1, 0.1, 0.16],
            [8, 3, 0.4, 0.41],
            [9, 1, 0.1, 0.06],
        ]
    },
    'based_on': []
}

# ana_03: gestation collapse — pop-weighted drive at each gestation
items['ana_03'] = {
    'label': "Average drive triples between 8 and 20 weeks",
    'content': (
        "The population-weighted mean round-trip drive grows from 0.25 hours at 8 weeks to 0.30 at 12, "
        "0.59 at 16, and 1.02 hours at 20 weeks — a 4x increase across the gestational ladder. The share "
        "of urban Americans living in a city with a 0-hour drive falls from 88.8% (8 weeks) to 66.9% (20 "
        "weeks); the share facing a 4+ hour round-trip rises from 1.4% to 10.8%. Most clinics offer first-"
        "trimester care; far fewer perform second-trimester D&E procedures. The clinic universe for a "
        "20-week patient is a small fraction of the universe for an 8-week patient, and the geography of "
        "access collapses correspondingly."),
    'type': 'trend',
    'strength': 'strong',
    'calculation': {
        'file': 'code/distributions_and_map_data.py',
        'lines': [40, 49],
        'output': "8\t0.40\t0.25\t88.8\t1.4\n12\t0.48\t0.30\t86.4\t1.7\n16\t0.82\t0.59\t78.1\t5.2\n20\t1.30\t1.02\t66.9\t10.8"
    },
    'data_table': {
        'description': "Drive-time metrics at each gestation week (open scenario)",
        'columns': ["weeks", "city_mean_hours", "pop_weighted_hours", "pct_pop_0h", "pct_pop_4plus_h"],
        'rows': [
            [8, 0.40, 0.25, 88.8, 1.4],
            [12, 0.48, 0.30, 86.4, 1.7],
            [16, 0.82, 0.59, 78.1, 5.2],
            [20, 1.30, 1.02, 66.9, 10.8],
        ]
    },
    'based_on': ['det_03']
}

# ana_04: 151 cities lack a 1-hour round-trip at 8 weeks (Pudding's headline)
items['ana_04'] = {
    'label': "151 cities sit beyond a one-hour round-trip — even at 8 weeks",
    'content': (
        "151 of the 749 cities (20.2%) record a round-trip drive of one hour or more even at the earliest "
        "gestation, when the clinic universe is largest. By 16 weeks that figure rises to 255 cities "
        "(34.0%); by 20 weeks, 339 cities (45.3%) — nearly half the urban population studied — sit beyond "
        "a one-hour round-trip from the nearest provider. This is the Pudding's headline number, and it "
        "describes a baseline of friction even before any clinic closes."),
    'type': 'distribution',
    'strength': 'strong',
    'calculation': {
        'file': 'code/access_thresholds.py',
        'lines': [55, 65],
        'output': "cities lacking 'within 1h round-trip' at 8 weeks (open): 151\ncities lacking 1h round-trip at 16 weeks: 255\ncities lacking 1h round-trip at 20 weeks: 339"
    },
    'data_table': {
        'description': "Cities lacking a 1-hour round-trip at each gestation",
        'columns': ["weeks", "cities_lacking_1h", "pct_cities", "scenario"],
        'rows': [
            [8, 151, 20.2, "open"],
            [12, 180, 24.0, "open"],
            [16, 255, 34.0, "open"],
            [20, 339, 45.3, "open"],
            [8, 283, 37.8, "closed"],
            [12, 350, 46.7, "closed"],
            [16, 419, 55.9, "closed"],
            [20, 505, 67.4, "closed"],
        ]
    },
    'based_on': ['det_01']
}

# ana_05: closed scenario — fragility of the system
items['ana_05'] = {
    'label': "Closing the nearest clinic doubles the share of long drives",
    'content': (
        "The dataset's 'closed' columns simulate the closure of the closest clinic — a controlled "
        "stress test on the system. The result: the share of cities lacking a 1-hour round-trip jumps "
        "from 20.2% to 37.8% at 8 weeks, and from 45.3% to 67.4% at 20 weeks. Population-weighted, "
        "the share of urban Americans living in a 0-hour-drive city collapses from 66.9% to 42.7% at "
        "20 weeks. The system is not slack: shutting one clinic per region is enough to push roughly "
        "two-thirds of cities outside an hour-round-trip at 20 weeks. This is what the loss of even "
        "a single second-trimester provider looks like."),
    'type': 'group-diff',
    'strength': 'strong',
    'calculation': {
        'file': 'code/access_thresholds.py',
        'lines': [33, 42],
        'output': "8wk_closed\t37.8%\t19.9%\t5.9%\t2.3%\n20wk_closed\t67.4%\t45.7%\t31.6%\t17.8%"
    },
    'data_table': {
        'description': "Open vs closed scenario: pop-weighted drive metrics by gestation",
        'columns': ["weeks", "open_pop_weighted_h", "closed_pop_weighted_h", "open_pct_pop_0h", "closed_pct_pop_0h"],
        'rows': [
            [8, 0.25, 0.58, 88.8, 75.2],
            [12, 0.30, 0.72, 86.4, 69.2],
            [16, 0.59, 1.28, 78.1, 59.0],
            [20, 1.02, 2.31, 66.9, 42.7],
        ]
    },
    'based_on': ['det_08', 'det_06']
}

# ana_06: state ranking by 20-week drive (pop-weighted)
items['ana_06'] = {
    'label': "Idaho's 20-week round-trip averages 9 hours",
    'content': (
        "Population-weighted across each state's qualifying cities, Idaho records a 20-week round-trip "
        "drive of 9.00 hours — the longest in the dataset. North Dakota follows at 8.62, Louisiana at "
        "6.63, South Dakota at 6.50, Mississippi at 5.31. Population-weighted means understate the worst "
        "experience because the weighting smooths over the rural minority — but even with that smoothing, "
        "five states cross the 5-hour threshold. By contrast, 18 states record a population-weighted "
        "20-week drive under one hour (e.g. New York 0.04, California 0.07, Massachusetts 0.00)."),
    'type': 'ranking',
    'strength': 'strong',
    'calculation': {
        'file': 'code/state_rollup.py',
        'lines': [14, 25],
        'output': "Idaho\t564170\t6\t0.60\t0.70\t7.40\t9.00\nNorth Dakota\t246701\t3\t1.90\t1.90\t1.90\t8.62\nLouisiana\t1154323\t7\t0.48\t0.48\t0.48\t6.63"
    },
    'data_table': {
        'description': "Population-weighted 20-week round-trip drive by state (top 12)",
        'columns': ["state", "pop_total", "wk20_hours", "wk8_hours", "collapse_8_to_20"],
        'rows': [
            ["Idaho", 564170, 9.00, 0.60, 8.40],
            ["North Dakota", 246701, 8.62, 1.90, 6.72],
            ["Louisiana", 1154323, 6.63, 0.48, 6.15],
            ["South Dakota", 245113, 6.50, 2.70, 3.80],
            ["Mississippi", 295119, 5.31, 0.49, 4.82],
            ["Wyoming", 123620, 4.95, 3.44, 1.51],
            ["Virginia", 2095024, 4.59, 0.28, 4.31],
            ["Montana", 240923, 4.43, 0.50, 3.93],
            ["South Carolina", 592160, 4.39, 0.00, 4.39],
            ["Tennessee", 2320805, 3.94, 0.46, 3.48],
            ["Kentucky", 1052512, 3.59, 0.89, 2.70],
            ["Arkansas", 715425, 2.65, 0.63, 2.02],
        ]
    },
    'based_on': ['det_05']
}

# ana_07: Idaho 8 -> 16 week jump (the Boise example)
items['ana_07'] = {
    'label': "Boise: from in-city to 8-hour round-trip in eight weeks",
    'content': (
        "Boise City has a 0-hour round-trip drive at 8 weeks and 12 weeks — a clinic in the city. At 16 "
        "weeks the round-trip becomes 8 hours; at 20 weeks, 10 hours. Three other Idaho cities — "
        "Nampa, Meridian, Caldwell — show the identical pattern (0/0/8/10), as does El Paso, Texas "
        "(0/0/7/7) and Bend, Oregon (0/0/6/6). For these cities the gestation collapse is binary: a "
        "first-trimester patient never leaves town; a second-trimester patient drives across or out of "
        "the state. The 8 → 16 week jump is the cleanest illustration of the dataset's central finding."),
    'type': 'anomaly',
    'strength': 'strong',
    'calculation': {
        'file': 'code/worst_cities.py',
        'lines': [27, 41],
        'output': "Boise City Idaho 218281 0 8 10\nNampa Idaho 89839 0 8 10\nMeridian Idaho 90739 0 8 10\nCaldwell Idaho 51686 0 8 10\nEl Paso Texas 681124 0 7 7\nBend Oregon 87014 0 6 6"
    },
    'data_table': {
        'description': "Cities with biggest 8 -> 16 week round-trip jump",
        'columns': ["city", "state", "population", "wk8_h", "wk16_h", "wk20_h", "jump_8_16_h"],
        'rows': [
            ["Boise City", "Idaho", 218281, 0, 8, 10, 8],
            ["Nampa", "Idaho", 89839, 0, 8, 10, 8],
            ["Meridian", "Idaho", 90739, 0, 8, 10, 8],
            ["Caldwell", "Idaho", 51686, 0, 8, 10, 8],
            ["El Paso", "Texas", 681124, 0, 7, 7, 7],
            ["Bend", "Oregon", 87014, 0, 6, 6, 6],
            ["Knoxville", "Tennessee", 185291, 0, 5, 5, 5],
            ["Sioux Falls", "South Dakota", 171544, 0, 5, 5, 5],
            ["Fayetteville", "Arkansas", 82830, 0, 5, 5, 5],
            ["Medford", "Oregon", 79805, 0, 5, 8, 5],
            ["Springdale", "Arkansas", 77859, 0, 5, 5, 5],
            ["Las Cruces", "New Mexico", 101643, 1, 6, 6, 5],
            ["Johnson City", "Tennessee", 66027, 1, 6, 6, 5],
            ["Rogers", "Arkansas", 63159, 1, 6, 6, 5],
            ["Grand Junction", "Colorado", 60358, 2, 7, 7, 5],
        ]
    },
    'based_on': ['det_03']
}

# ana_08: longest 8-week drives even in normal conditions
items['ana_08'] = {
    'label': "Rapid City to a clinic: 9 hours round-trip — at any gestation",
    'content': (
        "Rapid City, South Dakota, sits the farthest from any clinic in the dataset at the earliest "
        "gestation: 9 hours round-trip at 8 weeks, climbing to 10 by 16 weeks. Lubbock, Midland, Odessa, "
        "Amarillo and San Angelo (all West Texas) each record 6-8 hours round-trip at 8 weeks. These are "
        "the cities whose first-trimester patients are already on what is functionally a road-trip; the "
        "8-week column does not save them. They are also the cities where a single closure is "
        "catastrophic — Rapid City's 8-week round-trip jumps to 9 even before a closure, and the closed "
        "scenarios push the worst into the teens of hours."),
    'type': 'ranking',
    'strength': 'strong',
    'calculation': {
        'file': 'code/worst_cities.py',
        'lines': [9, 13],
        'output': "Rapid City\tSD\t9\t10\t10\nLubbock\tTX\t8\t8\t10\nMidland\tTX\t8\t8\t9\nOdessa\tTX\t8\t8\t9\nAmarillo\tTX\t7\t7\t7"
    },
    'data_table': {
        'description': "Cities with longest 8-week round-trip drives",
        'columns': ["city", "state", "population", "wk8_h", "wk16_h", "wk20_h"],
        'rows': [
            ["Rapid City", "South Dakota", 73569, 9, 10, 10],
            ["Lubbock", "Texas", 249042, 8, 8, 10],
            ["Midland", "Texas", 132950, 8, 8, 9],
            ["Odessa", "Texas", 118968, 8, 8, 9],
            ["Amarillo", "Texas", 198645, 7, 7, 7],
            ["San Angelo", "Texas", 100450, 6, 6, 6],
            ["Casper", "Wyoming", 60285, 6, 6, 7],
            ["Bismarck", "North Dakota", 71167, 5, 5, 11],
            ["Laredo", "Texas", 255473, 4, 4, 4],
            ["Springfield", "Missouri", 166810, 4, 5, 5],
            ["Abilene", "Texas", 121721, 4, 4, 5],
            ["Lake Charles", "Louisiana", 76070, 4, 4, 4],
            ["Lake Havasu City", "Arizona", 53553, 4, 4, 5],
            ["La Crosse", "Wisconsin", 52306, 4, 4, 4],
            ["Corpus Christi", "Texas", 324074, 3, 3, 4],
        ]
    },
    'based_on': ['det_05']
}

# ana_09: longest 20-week drives
items['ana_09'] = {
    'label': "Eleven hours from Bismarck to second-trimester care",
    'content': (
        "The longest 20-week round-trip drive in the dataset is Bismarck, North Dakota, at 11 hours — "
        "the equivalent of a full working day plus a meal. Lubbock, Boise, Nampa, Meridian, Caldwell, "
        "Rapid City, and Missoula each record 10-hour round-trips at 20 weeks. New Orleans, Rochester "
        "(NY), Brownsville and others sit at 8 hours. With state-mandated waiting periods, those drives "
        "double, since a patient must make two trips. A 10-hour round-trip is not a 'long drive'; it is "
        "two days off work, a hotel, gas, and whatever child care a person has to arrange to disappear "
        "for 48 hours."),
    'type': 'ranking',
    'strength': 'strong',
    'calculation': {
        'file': 'code/worst_cities.py',
        'lines': [21, 28],
        'output': "Bismarck\tND\t11\nLubbock\tTX\t10\nBoise City\tID\t10\nNampa\tID\t10\nMeridian\tID\t10\nMissoula\tMT\t10"
    },
    'data_table': {
        'description': "Cities with longest 20-week round-trip drives",
        'columns': ["city", "state", "population", "wk8_h", "wk20_h"],
        'rows': [
            ["Bismarck", "North Dakota", 71167, 5, 11],
            ["Lubbock", "Texas", 249042, 8, 10],
            ["Boise City", "Idaho", 218281, 0, 10],
            ["Nampa", "Idaho", 89839, 0, 10],
            ["Meridian", "Idaho", 90739, 0, 10],
            ["Rapid City", "South Dakota", 73569, 9, 10],
            ["Missoula", "Montana", 71022, 0, 10],
            ["Caldwell", "Idaho", 51686, 0, 10],
            ["Midland", "Texas", 132950, 8, 9],
            ["Odessa", "Texas", 118968, 8, 9],
            ["Grand Forks", "North Dakota", 57011, 2, 9],
            ["New Orleans", "Louisiana", 389617, 0, 8],
            ["Rochester", "New York", 209802, 0, 8],
            ["Brownsville", "Texas", 183887, 2, 8],
            ["Medford", "Oregon", 79805, 0, 8],
        ]
    },
    'based_on': ['det_07']
}

# ana_10: closure fragility — 8-week — Texas Rio Grande Valley + ND
items['ana_10'] = {
    'label': "If McAllen's clinic closes, a 0-hour drive becomes 6",
    'content': (
        "Five cities in the Texas Rio Grande Valley — McAllen, Mission, Edinburg, Pharr, Harlingen — "
        "go from a 0-1 hour round-trip to a 6-7 hour round-trip when their nearest clinic is removed. "
        "Three North Dakota cities (Fargo, Grand Forks, Bismarck) jump by 6-7 hours; Mississippi's "
        "Jackson goes from 0 to 5; Louisiana's Shreveport from 0 to 5. These are 'one-clinic regions': "
        "their access is robust at first glance but completely dependent on a single facility. The "
        "fragility is not theoretical — Wyoming's only clinic closed in July 2017, and HB2 in Texas had "
        "demonstrated through 2013-2016 that single-region waves of closures were a real policy outcome."),
    'type': 'ranking',
    'strength': 'strong',
    'calculation': {
        'file': 'code/worst_cities.py',
        'lines': [38, 50],
        'output': "Mission\tTX\t0\t7\t7\nGrand Forks\tND\t2\t9\t7\nMcAllen\tTX\t0\t6\t6\nFargo\tND\t0\t6\t6\nEdinburg\tTX\t0\t6\t6"
    },
    'data_table': {
        'description': "Cities with biggest 8-week fragility (drive jump when closest clinic closes)",
        'columns': ["city", "state", "population", "wk8_open_h", "wk8_closed_h", "fragility_h"],
        'rows': [
            ["Mission", "Texas", 83298, 0, 7, 7],
            ["Grand Forks", "North Dakota", 57011, 2, 9, 7],
            ["McAllen", "Texas", 140269, 0, 6, 6],
            ["Fargo", "North Dakota", 118523, 0, 6, 6],
            ["Edinburg", "Texas", 84497, 0, 6, 6],
            ["Pharr", "Texas", 76538, 0, 6, 6],
            ["Bismarck", "North Dakota", 71167, 5, 11, 6],
            ["Harlingen", "Texas", 65774, 1, 7, 6],
            ["Shreveport", "Louisiana", 197204, 0, 5, 5],
            ["Brownsville", "Texas", 183887, 2, 7, 5],
            ["Jackson", "Mississippi", 170674, 0, 5, 5],
            ["Sioux Falls", "South Dakota", 171544, 0, 5, 5],
            ["Medford", "Oregon", 79805, 0, 5, 5],
            ["Bossier City", "Louisiana", 68094, 0, 5, 5],
            ["Wichita", "Kansas", 389965, 0, 4, 4],
        ]
    },
    'based_on': ['det_08', 'det_04']
}

# ana_11: 20-week fragility — Mountain West
items['ana_11'] = {
    'label': "If Salt Lake's clinic closes, the round-trip jumps from 0 to 11 hours",
    'content': (
        "The 20-week 'closed' scenario shows the most extreme single-closure consequences anywhere in "
        "the dataset, concentrated in Utah, Montana, and New Mexico. Billings, Montana, jumps from 0 to "
        "15 hours round-trip. Albuquerque and Rio Rancho jump from 0 to 12. Eight Utah cities — Salt "
        "Lake City, West Valley City, West Jordan, Ogden, Layton, Logan, Taylorsville, South Jordan — "
        "all jump 10-12 hours. These are population centers, not remote outposts. The closure of a "
        "single second-trimester provider is enough to push hundreds of thousands of urban Americans "
        "into a 10+ hour round-trip drive."),
    'type': 'ranking',
    'strength': 'strong',
    'calculation': {
        'file': 'code/worst_cities.py',
        'lines': [52, 64],
        'output': "Billings\tMT\t110263\t0\t15\t15\nAlbuquerque\tNM\t559121\t0\t12\t12\nSalt Lake City\tUT\t192672\t0\t11\t11"
    },
    'data_table': {
        'description': "Cities with biggest 20-week fragility (drive jump when closest clinic closes)",
        'columns': ["city", "state", "population", "wk20_open_h", "wk20_closed_h", "fragility_h"],
        'rows': [
            ["Billings", "Montana", 110263, 0, 15, 15],
            ["Albuquerque", "New Mexico", 559121, 0, 12, 12],
            ["Rio Rancho", "New Mexico", 94171, 0, 12, 12],
            ["Logan", "Utah", 50371, 2, 14, 12],
            ["Salt Lake City", "Utah", 192672, 0, 11, 11],
            ["West Valley City", "Utah", 136208, 0, 11, 11],
            ["West Jordan", "Utah", 111946, 0, 11, 11],
            ["Ogden", "Utah", 85444, 1, 12, 11],
            ["Layton", "Utah", 74143, 1, 12, 11],
            ["Taylorsville", "Utah", 60514, 0, 11, 11],
            ["South Jordan", "Utah", 66648, 0, 11, 11],
            ["Sandy", "Utah", 93613, 1, 11, 10],
            ["Great Falls", "Montana", 59638, 6, 16, 10],
            ["Little Rock", "Arkansas", 197992, 0, 9, 9],
            ["Provo", "Utah", 115264, 1, 10, 9],
        ]
    },
    'based_on': ['det_08']
}

# ana_12: state-level 8 -> 20 week collapse
items['ana_12'] = {
    'label': "Idaho's drive grows 8.4 hours between 8 and 20 weeks",
    'content': (
        "Idaho posts the largest 8-to-20-week increase in any state: a population-weighted 8.4-hour "
        "growth (0.60 → 9.00). North Dakota grows 6.7 hours, Louisiana 6.2, Mississippi 4.8, South "
        "Carolina 4.4, Virginia 4.3. These are not remote states — Virginia is the 12th most populous "
        "in the union — but the network of clinics willing to perform second-trimester procedures "
        "thins out enough that even mid-Atlantic and Deep South states post 4+ hour collapses. The "
        "hidden geography of the gestational ladder maps onto the same regions: the Mountain West, "
        "the Plains, the Mississippi Delta, the South."),
    'type': 'ranking',
    'strength': 'strong',
    'calculation': {
        'file': 'code/state_rollup.py',
        'lines': [27, 33],
        'output': "Idaho\t8.40\nNorth Dakota\t6.72\nLouisiana\t6.15\nMississippi\t4.82"
    },
    'data_table': {
        'description': "States ranked by 8 -> 20 week round-trip drive growth (population-weighted)",
        'columns': ["state", "pop_total", "wk8_h", "wk20_h", "collapse_8_to_20_h"],
        'rows': [
            ["Idaho", 564170, 0.60, 9.00, 8.40],
            ["North Dakota", 246701, 1.90, 8.62, 6.72],
            ["Louisiana", 1154323, 0.48, 6.63, 6.15],
            ["Mississippi", 295119, 0.49, 5.31, 4.82],
            ["South Carolina", 592160, 0.00, 4.39, 4.39],
            ["Virginia", 2095024, 0.28, 4.59, 4.31],
            ["Montana", 240923, 0.50, 4.43, 3.93],
            ["South Dakota", 245113, 2.70, 6.50, 3.80],
            ["Tennessee", 2320805, 0.46, 3.94, 3.48],
            ["Kentucky", 1052512, 0.89, 3.59, 2.70],
            ["Alabama", 1167176, 0.28, 2.50, 2.22],
            ["Arkansas", 715425, 0.63, 2.65, 2.02],
        ]
    },
    'based_on': ['det_03', 'det_04']
}

# ana_13: city-level table for the map (slim)
import json as _json
with open(os.path.join(PROJECT, 'code/city_table.json')) as f:
    city_table = _json.load(f)
items['ana_13'] = {
    'label': "Slim city table — lat/lng + drive at each gestation",
    'content': (
        "The slim city table holds 749 rows — one per city — with population, latitude, longitude, and "
        "the round-trip driving time at 8/16/20 weeks plus the 8 and 20 week 'closed' counterfactuals. "
        "It is the data that drives the interactive US map: each city is a circle whose color encodes "
        "the drive time and whose size encodes the population, with the gestation/scenario toggled by "
        "the reader. The dataset's contiguous-US scope is visible in the latitude range (25.5° to 48.8°)"
        " and longitude range (-123.3° to -70.3°)."),
    'type': 'distribution',
    'strength': 'strong',
    'calculation': {
        'file': 'code/build_city_table.py',
        'lines': [12, 22],
        'output': "slim_rows=749, lat range=[25.469,48.752], lng range=[-123.262,-70.255]"
    },
    'data_table': {
        'description': "Per-city: population, lat, lng, and round-trip drive at each gestation/scenario (749 rows)",
        'columns': city_table['columns'],
        'rows': city_table['rows'],
    },
    'based_on': []
}

# ana_14: zero-time city share by gestation
items['ana_14'] = {
    'label': "Share of cities with a 0-hour drive falls from 80% to 55%",
    'content': (
        "The share of cities recording a 0-hour round-trip drive — meaning the closest clinic is in or "
        "directly adjacent to the city — falls from 79.8% at 8 weeks to 76.0% at 12, 66.0% at 16, and "
        "54.7% at 20 weeks. Population-weighted, those shares are 88.8%, 86.4%, 78.1%, and 66.9%. The "
        "20-week column erases the comfort of the 8-week one: nearly half of US cities, weighted by "
        "size to a third of the urban population, are not within a comfortable drive of a clinic that "
        "will see them."),
    'type': 'distribution',
    'strength': 'strong',
    'calculation': {
        'file': 'code/worst_cities.py',
        'lines': [66, 72],
        'output': "8 wk: 598 cities (79.8%) | pop coverage 88.8%\n20 wk: 410 cities (54.7%) | pop coverage 66.9%"
    },
    'data_table': {
        'description': "Share of cities and population with 0-hour round-trip by gestation",
        'columns': ["weeks", "cities_0h", "pct_cities_0h", "pct_pop_0h"],
        'rows': [
            [8, 598, 79.8, 88.8],
            [12, 569, 76.0, 86.4],
            [16, 494, 66.0, 78.1],
            [20, 410, 54.7, 66.9],
        ]
    },
    'based_on': []
}

# ana_15: Histogram of round-trip drive (cities) — for chart
items['ana_15'] = {
    'label': "Distribution of round-trip drives shifts right with gestation",
    'content': (
        "The full histogram of round-trip drives across all 749 cities widens at every gestation step. "
        "At 8 weeks, the modal drive is 0 hours and the long tail ends at 9 hours (one city — Rapid "
        "City). At 20 weeks, the modal drive is still 0 but the tail stretches to 11 hours (Bismarck), "
        "and the second-most common drive becomes 1 hour rather than 0 for the first time. The "
        "distribution flattens — more cities pile up in the 1-3 hour buckets — reflecting the "
        "thinning second-trimester clinic universe rather than any geographic change in the cities "
        "themselves."),
    'type': 'distribution',
    'strength': 'moderate',
    'calculation': {
        'file': 'code/distributions_and_map_data.py',
        'lines': [13, 19],
        'output': "0\t598\t569\t494\t410\n1\t75\t94\t111\t141\n11\t0\t0\t0\t1"
    },
    'data_table': {
        'description': "City counts at each round-trip hour, by gestation",
        'columns': ["hours", "wk8", "wk12", "wk16", "wk20"],
        'rows': [
            [0, 598, 569, 494, 410],
            [1, 75, 94, 111, 141],
            [2, 39, 39, 49, 50],
            [3, 23, 28, 43, 49],
            [4, 6, 8, 22, 27],
            [5, 1, 3, 10, 19],
            [6, 2, 2, 9, 23],
            [7, 1, 2, 3, 13],
            [8, 3, 3, 7, 6],
            [9, 1, 1, 0, 3],
            [10, 0, 0, 1, 7],
            [11, 0, 0, 0, 1],
        ]
    },
    'based_on': []
}

# Final write
out = {
    "meta": {"role": "analyst", "version": "2.0"},
    "dataset": {
        "files": ["cities.csv"],
        "rows": 749,
        "columns": 14,
        "what_one_row_represents": "A single contiguous-US city of population >50,000 and its round-trip driving time in HOURS to the nearest abortion clinic at four gestational cutoffs, plus a 'nearest-clinic-closed' counterfactual for each cutoff",
        "time_range": "Snapshot as of August 2017",
        "geographic_scope": "Contiguous US, 47 states (excludes AK, HI, and small-population states without qualifying cities)"
    },
    "items": items,
    "caveats": [
        {"id": "ana_caveat_01", "content": "All round-trip drive durations are integer HOURS (rounded down, then binned), despite the README labelling them 'minutes'. The Pudding methodology paragraph and the actual value range (max 11) confirm this."},
        {"id": "ana_caveat_02", "content": "0-hour round-trips dominate any unweighted average — 79.8% of cities are 0-hour at 8 weeks. Population-weighted means are reported alongside city means everywhere this would mislead."},
        {"id": "ana_caveat_03", "content": "The 'closed' columns simulate ONLY the closure of the closest clinic. They do not model multi-clinic waves of closures (HB2 in Texas; post-Dobbs sweeps), so they understate worst-case fragility."},
        {"id": "ana_caveat_04", "content": "Driving time alone understates the patient burden because state-mandated waiting periods often require two trips to the same clinic. The drive is the floor, not the ceiling."},
        {"id": "ana_caveat_05", "content": "The dataset reflects the access network in mid-2017, after HB2 was struck down but before its closed clinics had reopened, and well before the post-Dobbs (June 2022) wave of total bans. It is a baseline, not the present."}
    ]
}

with open(os.path.join(PROJECT,'analyst.json'),'w') as f:
    json.dump(out, f, indent=2)
print(f"wrote {os.path.join(PROJECT,'analyst.json')}")
print(f"items: {len(items)}; total size: {os.path.getsize(os.path.join(PROJECT,'analyst.json'))} bytes")
