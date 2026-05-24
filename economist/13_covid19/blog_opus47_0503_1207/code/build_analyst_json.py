"""Stage 2 - Analyst: assemble analyst.json from the analysis scripts above."""
import pandas as pd
import numpy as np
import json

DATA = "/Users/forrest/Desktop/data2blog/data_preprint/economist/13_covid19"
PROJECT = "/Users/forrest/Desktop/data2blog/project/economist/13_covid19/blog_opus47_0503_1207"

jh = pd.read_csv(f"{DATA}/03-04-2020_JH_cases.csv")
jh['country'] = jh['Country/Region'].replace({'US': 'United States', 'UK': 'United Kingdom', 'Mainland China': 'China'})
country_total = jh.groupby('country')['Confirmed'].sum().sort_values(ascending=False)

pred = pd.read_csv(f"{DATA}/PredictedCases.csv")
cov = pd.read_csv(f"{DATA}/covid_cases_and_covariates_march_4_selected.csv")
cov['mean_tour'] = (cov['outbound_tour_groups_Q3_2019_improved'] + cov['inbound_tour_groups_Q3_2019_1_improved']) / 2
merged = pred.merge(cov[['country', 'mean_tour', 'continent']], on='country', how='left')

# Build chart tables ----------------------------------------------------------
top15_cases = country_total.head(15)
top15_table = {
    "description": "Top 15 countries / regions by JHU-reported confirmed COVID-19 cases on 4 March 2020",
    "columns": ["country", "cases", "share_pct"],
    "rows": [[c, int(v), round(v / country_total.sum() * 100, 2)] for c, v in top15_cases.items()],
}

# Scatter rows (all 124)
scatter_rows = []
for _, r in merged.iterrows():
    scatter_rows.append([
        r['country'],
        round(float(r['mean_tour']), 1),
        int(r['cases']),
        bool(r['oecd']),
        round(float(r['NoPopModPredictedCases']), 2),
        round(float(r['NoPopModResidualLogCases']), 4),
        r['continent']
    ])
scatter_table = {
    "description": "All 124 countries: mean Chinese tour-group flows (Q3 2019), reported cases (4 Mar 2020), OECD flag, model-predicted cases, residual in log-units",
    "columns": ["country", "mean_tour", "cases", "oecd", "predicted_cases", "residual_log", "continent"],
    "rows": scatter_rows,
}

# Regression-line table (50 points along log scale)
xs = np.logspace(0, np.log10(merged['mean_tour'].max()), 50)
reg_rows = [[round(float(x), 2), round(float(np.exp(-8.4363 + 1.1313 * np.log(max(x, 1)))), 4)] for x in xs]
reg_table = {
    "description": "OECD-only OLS fit: y = exp(-8.4363 + 1.1313 * log(x)). 50 evenly log-spaced sample points for plotting the regression line.",
    "columns": ["mean_tour", "predicted_cases"],
    "rows": reg_rows,
}

# Top-15 tourism countries
tour_top15 = cov.sort_values('mean_tour', ascending=False).head(15)
tour_table = {
    "description": "Top 15 destinations/origins of Chinese tour-group flows in Q3 2019 (mean of inbound and outbound)",
    "columns": ["country", "mean_tour", "oecd"],
    "rows": [[r['country'], int(r['mean_tour']), bool(r['oecd'])] for _, r in tour_top15.iterrows()],
}

# Bottom 15 (most under-detected)
bot15 = pred.sort_values('NoPopModResidualLogCases').head(15).copy()
under_table = {
    "description": "15 countries reporting the fewest cases relative to tourism-flow prediction. residual_log < 0 = below the OECD-fit line. multiplier = predicted/max(reported,1).",
    "columns": ["country", "oecd", "reported_cases", "predicted_cases", "residual_log", "multiplier"],
    "rows": [
        [r['country'], bool(r['oecd']), int(r['cases']), round(float(r['NoPopModPredictedCases']), 1),
         round(float(r['NoPopModResidualLogCases']), 3),
         round(float(r['NoPopModPredictedCases'] / max(r['cases'], 1)), 1)]
        for _, r in bot15.iterrows()
    ],
}

# Top 15 (most over-detected)
top15 = pred.sort_values('NoPopModResidualLogCases', ascending=False).head(15).copy()
over_table = {
    "description": "15 countries reporting the most cases relative to tourism-flow prediction. residual_log > 0 = above the OECD-fit line.",
    "columns": ["country", "oecd", "reported_cases", "predicted_cases", "residual_log"],
    "rows": [
        [r['country'], bool(r['oecd']), int(r['cases']), round(float(r['NoPopModPredictedCases']), 1),
         round(float(r['NoPopModResidualLogCases']), 3)]
        for _, r in top15.iterrows()
    ],
}

# Hidden-multiplier focus table — 12 most populous / largest predicted under-detected
under_focus = merged[merged['NoPopModPredictedCases'] >= 50].sort_values('NoPopModResidualLogCases').head(12).copy()
focus_table = {
    "description": "Top 12 countries with predicted >=50 cases that report far fewer than the model expects. multiplier = predicted/max(reported,1).",
    "columns": ["country", "reported_cases", "predicted_cases", "multiplier"],
    "rows": [
        [r['country'], int(r['cases']), int(round(r['NoPopModPredictedCases'])),
         round(float(r['NoPopModPredictedCases'] / max(r['cases'], 1)), 1)]
        for _, r in under_focus.iterrows()
    ],
}

# Build full analyst.json
analyst = {
    "meta": {"role": "analyst", "version": "2.0"},
    "dataset": {
        "files": [
            "03-04-2020_JH_cases.csv",
            "chinese_tourism.csv",
            "covid_cases_and_covariates_march_4_selected.csv",
            "PredictedCases.csv",
        ],
        "rows": 124,
        "columns": 37,
        "what_one_row_represents": "One country: its OECD status, mean Chinese tour-group flow (Q3 2019), confirmed COVID-19 cases as of 4 March 2020 (JHU CSSE), model prediction and residual.",
        "time_range": "Tourism: Q3 2019. Cases: 4 March 2020 snapshot.",
        "geographic_scope": "124 countries, all continents",
    },
    "items": {
        "ana_01": {
            "label": "Global case landscape, 4 March 2020",
            "content": "On 4 March 2020 the Johns Hopkins dashboard counted 95,124 confirmed COVID-19 cases worldwide. Mainland China alone held 80,271 of them — 84.4% of the global total. Hubei province by itself accounted for 67,332 cases (70.8% of global). Outside China only three countries had more than two thousand cases: South Korea (5,621), Italy (3,089) and Iran (2,922). The next group — Japan, France, Germany, Spain, the United States — sat between 150 and 350 cases each. Eighty-six countries had reported any cases at all; the remaining 55 in this dataset had reported zero.",
            "type": "ranking",
            "strength": "strong",
            "calculation": {
                "file": "code/case_landscape.py",
                "lines": [11, 30],
                "output": "Total reported confirmed cases: 95,124\nNumber of countries/regions reporting cases: 86\nChina (Mainland) share: 84.4%\nHubei province alone: 67,332 (70.8% of global)\nTop 5 outside China: South Korea 5,621; Italy 3,089; Iran 2,922; Others 706; Japan 331",
            },
            "data_table": top15_table,
            "based_on": ["det_03"],
        },
        "ana_02": {
            "label": "OECD-only regression: log-tourism explains 59% of log-cases",
            "content": "Fitting a simple linear regression on the 34 OECD countries gives log(cases+1) = -8.44 + 1.13 * log(mean tour-group flow). The slope is 1.13 (SE 0.17, t = 6.83, p < 1e-7) and the model explains R-squared = 0.59 of the variance in log-cases. The slightly super-linear slope means cases grow a little faster than tourism — doubling tourism predicts roughly a 2.2x increase in cases. The fit is strong enough to score every country against it: a country sitting on the line reports the cases its tourism flow would predict; a country far below is reporting fewer than expected; a country far above is reporting more.",
            "type": "correlation",
            "strength": "strong",
            "calculation": {
                "file": "code/regression_model.py",
                "lines": [12, 28],
                "output": "OECD countries in fit: 34\nIntercept: -8.4363  Slope (LogTourists coef): 1.1313\nR-squared: 0.5933  F p-value: 9.977e-08  n: 34",
            },
            "data_table": reg_table,
            "based_on": ["det_05", "det_06"],
        },
        "ana_03": {
            "label": "Tourism flows: where Chinese tour groups go",
            "content": "Chinese outbound and inbound tour-group flows in Q3 2019 totalled about 8.94 million person-trips across these 124 countries. The flow is heavily concentrated: the top ten destinations account for 74.1% of the total. Thailand sits at the top with 1.55 million (almost twice Japan's 1.25 million); Taiwan, Vietnam, Singapore, Malaysia and Russia each saw 400,000 to 950,000 group-trips. OECD countries account for only 35% of total flow because the top non-OECD destinations — Thailand, Vietnam, Indonesia, Russia — outweigh most OECD members. This concentration matters: it means a small number of non-OECD countries had the largest exposure but also some of the lowest reported case counts.",
            "type": "distribution",
            "strength": "strong",
            "calculation": {
                "file": "code/regression_model.py",
                "lines": [33, 47],
                "output": "Top 5 by mean Q3 2019 tour-group flow: Thailand 1,548,725; Japan 1,247,334; Taiwan 944,784; Vietnam 682,555; Singapore 468,114\nTotal flow: 8,942,938\nOECD share: 35.0%  Top 10 share: 74.1%",
            },
            "data_table": tour_table,
            "based_on": ["det_02"],
        },
        "ana_04": {
            "label": "Most under-detected countries vs the OECD-fit prediction",
            "content": "Five countries sit more than 3.9 log-units below the OECD-fit line — the equivalent of reporting roughly 50 to 170 times fewer cases than the model expects. Russia, with 434,000 mean tour-group flows, reported just 3 cases vs a predicted 517 (172x). Indonesia reported 2 cases vs 330 predicted (165x). Myanmar, Philippines, Vietnam and Thailand follow, each reporting 50x or fewer than expected. Most of the largest residuals are non-OECD, but New Zealand and Turkey appear among the top under-detectors too — a hint that even within the OECD, surveillance was patchy in early March.",
            "type": "ranking",
            "strength": "strong",
            "calculation": {
                "file": "code/residuals.py",
                "lines": [13, 23],
                "output": "Russia: reported 3, predicted 517, multiplier 172.5x\nIndonesia: reported 2, predicted 330, multiplier 165.0x\nMyanmar: reported 0, predicted 110\nPhilippines: reported 3, predicted 208 (69.2x)\nVietnam: reported 16, predicted 863 (53.9x)\nThailand: reported 43, predicted 2181 (50.7x)",
            },
            "data_table": under_table,
            "based_on": ["det_06", "det_07"],
        },
        "ana_05": {
            "label": "Most over-detected countries vs prediction",
            "content": "The other end of the residual list is dominated by countries that were already in the news in early March: Iran (2,922 reported vs ~12 predicted, +5.46 log-units), Italy (3,089 vs 156 predicted, +2.99), South Korea (5,621 vs 392 predicted, +2.66). Iran's residual is by far the largest in the dataset — a 230x over-shoot of the tourism-implied baseline, consistent with the country having seeded outbreaks that ran far ahead of imports. Norway, Iceland, Spain, Austria and Belgium also sit comfortably above their predicted values: small-tourism countries that had nonetheless caught the wave from Italy.",
            "type": "ranking",
            "strength": "strong",
            "calculation": {
                "file": "code/residuals.py",
                "lines": [25, 35],
                "output": "Iran: 2,922 reported, 12.5 predicted, residual_log +5.46\nItaly: 3,089 reported, 155.6 predicted, residual_log +2.99\nSouth Korea: 5,621 reported, 392.0 predicted, residual_log +2.66\nNorway: 56 reported, 7.1 predicted, residual_log +2.09\nIceland: 26 reported, 5.7 predicted, residual_log +1.56\nSpain: 222 reported, 48.2 predicted, residual_log +1.53",
            },
            "data_table": over_table,
            "based_on": ["det_04", "det_07"],
        },
        "ana_06": {
            "label": "OECD vs non-OECD: a systematic surveillance gap",
            "content": "The OECD-only fit is mean-zero by construction, but the 90 non-OECD countries it was applied to are systematically below the line. Their mean residual is -0.85 log-units; their median is -0.73. Translated out of log space, non-OECD countries report on average about 43% of the cases the OECD-fit line would predict. 64% of non-OECD countries sit below the line, vs 56% of OECD members — a small gap in count, a large gap in size (the non-OECD residual SD is 1.69 vs 1.37 for OECD). The asymmetry is exactly what The Economist's argument predicts: cases per tourist look comparable in well-resourced systems and systematically smaller in less-resourced ones.",
            "type": "group-diff",
            "strength": "moderate",
            "calculation": {
                "file": "code/residuals.py",
                "lines": [37, 56],
                "output": "OECD (n=34): mean residual_log 0.000  median -0.005  SD 1.368\nNon-OECD (n=90): mean residual_log -0.847  median -0.730  SD 1.694\nGap: -0.847 log-units = non-OECD reports 43% of OECD-predicted level\n64% of non-OECD below line vs 56% of OECD",
            },
            "data_table": {
                "description": "Group comparison of residuals (OECD-fit OLS) between OECD and non-OECD countries.",
                "columns": ["group", "n", "mean_residual_log", "median_residual_log", "sd_residual_log", "pct_below_line"],
                "rows": [
                    ["OECD", 34, 0.000, -0.005, 1.368, 56],
                    ["Non-OECD", 90, -0.847, -0.730, 1.694, 64],
                ],
            },
            "based_on": ["det_06", "det_04"],
        },
        "ana_07": {
            "label": "Full scatter: tourism flow vs reported cases",
            "content": "Plotting all 124 countries in log-log space (mean Chinese tour-group flow on x, reported cases on y, with the OECD-only OLS line overlaid) gives the entire picture in one frame. The OECD points cluster around the line; non-OECD points scatter widely with most below it. Iran, Italy and South Korea sit far above. Russia, Indonesia, Thailand, Vietnam, the Philippines and Myanmar sit conspicuously below. The fit is the spine of the entire piece: the line is a 'what should be there' baseline, and every country's distance from it tells a story about either their outbreak or their surveillance.",
            "type": "correlation",
            "strength": "strong",
            "calculation": {
                "file": "code/scatter_data.py",
                "lines": [16, 26],
                "output": "Top countries by tour flow with cases:\nThailand tour=1,548,725 cases=43; Japan tour=1,247,334 cases=331\nTaiwan tour=944,784 cases=42; Vietnam tour=682,555 cases=16\nItaly tour=150,124 cases=3,089 (above line); Iran tour=12 cases=2,922 (far above line)",
            },
            "data_table": scatter_table,
            "based_on": ["det_05", "det_06"],
        },
        "ana_08": {
            "label": "Hidden-cases multiplier for the largest under-detectors",
            "content": "Among countries whose model-predicted caseload is at least 50, twelve report dramatically less than expected. Russia (172x), Indonesia (165x), Myanmar (110x), Philippines (69x), Vietnam (54x), Thailand (51x), Taiwan (30x), New Zealand (27x), Malaysia (11x), Japan (5x), Singapore (5x) and Australia (3x). Read literally, these are the multipliers The Economist's model implies between true exposure and reported cases. Some of these countries — Singapore, Taiwan, Australia — may simply have effective testing-and-tracing programmes that prevented imported cases from blowing up. Others — Russia, Indonesia, Myanmar — fit a different, darker pattern: low testing, low reporting, large unseen outbreaks.",
            "type": "anomaly",
            "strength": "strong",
            "calculation": {
                "file": "code/scatter_data.py",
                "lines": [29, 36],
                "output": "Top 12 under-detectors with multiplier:\nRussia 172.5x; Indonesia 165.0x; Myanmar 109.9x; Philippines 69.2x; Vietnam 53.9x; Thailand 50.7x; Taiwan 29.7x; New Zealand 26.6x; Malaysia 11.1x; Japan 5.2x; Singapore 5.1x; Australia 3.1x",
            },
            "data_table": focus_table,
            "based_on": ["det_04", "det_07"],
        },
    },
    "caveats": [
        {
            "id": "ana_caveat_01",
            "content": "Tour-group flows are a proxy: not all travellers are tour-group members, and the data are from Q3 2019, six months before the analysis. The proxy is most accurate for countries with stable tourism patterns and least accurate for those whose post-summer travel mix shifted.",
        },
        {
            "id": "ana_caveat_02",
            "content": "The OECD-only fit projects an 'expected' caseload onto non-OECD countries that may have very different surveillance, healthcare and reporting systems. A residual is not proof of under-reporting — it could also reflect successful containment, demographic differences, climatic differences, or population-density differences not captured here.",
        },
        {
            "id": "ana_caveat_03",
            "content": "All confirmed-case figures are reported numbers, themselves subject to lag and reporting practice on 4 March 2020. 'Reported cases' should always be read as 'cases known to have been recorded by that date', not 'cases that existed'.",
        },
    ],
}

with open(f"{PROJECT}/analyst.json", "w") as f:
    json.dump(analyst, f, indent=2)

print(f"Wrote analyst.json with {len(analyst['items'])} items.")
print(f"data_table sizes:")
for k, item in analyst['items'].items():
    n = len(item['data_table']['rows'])
    print(f"  {k}: {n} rows ({item['label']})")
