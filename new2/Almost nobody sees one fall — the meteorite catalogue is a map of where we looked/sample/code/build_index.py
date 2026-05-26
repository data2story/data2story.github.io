"""build_index.py — Programmer stage. Generates index.html from editor/analyst/designer JSON.
NOTE: This script is the Programmer's implementation; it does not have access to the raw CSV.
All numeric content comes from analyst.json data_tables; map markers come from the analyst's
pre-curated _map_data.json (which is itself derived from the raw data by the Analyst).
"""
import json
import pathlib

PROJ = pathlib.Path(r"D:/AI/journalist agent review/phase2/project/2020-07-29_meteorite-landings/blog_opus47_0525_2225")
analyst = json.loads((PROJ / "analyst.json").read_text(encoding="utf-8"))["items"]
editor = json.loads((PROJ / "editor.json").read_text(encoding="utf-8"))
designer = json.loads((PROJ / "designer.json").read_text(encoding="utf-8"))["items"]
map_data = json.loads((PROJ / "code/_map_data.json").read_text(encoding="utf-8"))

def table(ana_id):
    """Return data_table for an ana_xx as list of dicts."""
    t = analyst[ana_id]["data_table"]
    cols = t["columns"]
    return [dict(zip(cols, row)) for row in t["rows"]]

# === Vega-Lite specs ===

# des_05: stacked bar Fell vs Found by decade
decade_rows_raw = table("ana_06")  # columns: decade, Fell, Found, Total
decade_rows = []
for r in decade_rows_raw:
    decade_rows.append({"decade": r["decade"], "fall": "Found", "count": r["Found"]})
    decade_rows.append({"decade": r["decade"], "fall": "Fell", "count": r["Fell"]})

des_05_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Fell vs Found per decade",
    "width": "container",
    "height": 360,
    "background": "transparent",
    "data": {"values": decade_rows},
    "layer": [
        {
            "mark": {"type": "bar", "tooltip": True},
            "encoding": {
                "x": {"field": "decade", "type": "ordinal", "axis": {"title": "Decade", "labelAngle": -40, "values": [1700, 1750, 1800, 1850, 1900, 1950, 1970, 1980, 1990, 2000, 2010], "labelFontSize": 11}},
                "y": {"field": "count", "type": "quantitative", "axis": {"title": "Meteorites entered into the catalogue"}},
                "color": {
                    "field": "fall", "type": "nominal",
                    "scale": {"domain": ["Found", "Fell"], "range": ["#7a9bbf", "#b94a2c"]},
                    "legend": {"title": "Fall type", "orient": "top-left"}
                },
                "order": {"field": "fall", "type": "nominal", "sort": ["Found", "Fell"]}
            }
        },
        {
            "data": {"values": [{"decade": 1970, "label": "ANSMET begins\n(Japanese teams\nsince 1969)"}]},
            "mark": {"type": "text", "color": "#222", "fontSize": 11, "align": "left", "baseline": "bottom", "dx": 6, "dy": -10},
            "encoding": {
                "x": {"field": "decade", "type": "ordinal"},
                "y": {"datum": 17500, "type": "quantitative"},
                "text": {"field": "label"}
            }
        }
    ],
    "config": {"view": {"stroke": None}, "axis": {"grid": False, "domainColor": "#bbb"}}
}

# des_08: horizontal log-bucket mass histogram
mass_rows = table("ana_08")  # columns: bucket, count
des_08_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Mass distribution in log buckets",
    "width": "container",
    "height": 320,
    "background": "transparent",
    "data": {"values": mass_rows},
    "layer": [
        {
            "mark": {"type": "bar", "tooltip": True, "color": "#3d6fa3"},
            "encoding": {
                "y": {"field": "bucket", "type": "ordinal", "sort": ["<1g", "1-10g", "10-100g", "100g-1kg", "1-10kg", "10-100kg", "100kg-1t", "1-10t", "10-100t"], "axis": {"title": None, "labelFontSize": 12}},
                "x": {"field": "count", "type": "quantitative", "axis": {"title": "Meteorite count"}}
            }
        },
        {
            "mark": {"type": "text", "color": "#222", "fontSize": 11, "align": "left", "dx": 6},
            "encoding": {
                "y": {"field": "bucket", "type": "ordinal"},
                "x": {"field": "count", "type": "quantitative"},
                "text": {"field": "count", "type": "quantitative", "format": ","}
            }
        }
    ],
    "config": {"view": {"stroke": None}, "axis": {"grid": False, "domainColor": "#bbb"}}
}

# des_09: top 20 leaderboard, horizontal bars, log mass
top20_rows = table("ana_09")  # columns: rank, name, mass_kg, family, recclass, fall, year, lat, lon
des_09_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Top 20 heaviest meteorites",
    "width": "container",
    "height": 460,
    "background": "transparent",
    "data": {"values": top20_rows},
    "layer": [
        {
            "mark": {"type": "bar", "tooltip": True},
            "encoding": {
                "y": {"field": "name", "type": "nominal", "sort": "-x", "axis": {"title": None, "labelFontSize": 12}},
                "x": {"field": "mass_kg", "type": "quantitative", "scale": {"type": "log", "domain": [1000, 100000]}, "axis": {"title": "Recovered mass (kg, log scale)", "format": ",d"}},
                "x2": {"datum": 1000},
                "color": {
                    "field": "family", "type": "nominal",
                    "scale": {
                        "domain": ["Iron meteorite", "Stony-iron", "Ordinary chondrite"],
                        "range": ["#5f4b32", "#9b7e3f", "#7a9bbf"]
                    },
                    "legend": {"title": "Family", "orient": "top-right"}
                }
            }
        },
        {
            "mark": {"type": "text", "color": "#222", "fontSize": 11, "align": "left", "dx": 6},
            "encoding": {
                "y": {"field": "name", "type": "nominal", "sort": "-x"},
                "x": {"field": "mass_kg", "type": "quantitative"},
                "text": {"field": "mass_kg", "type": "quantitative", "format": ",d"}
            }
        }
    ],
    "config": {"view": {"stroke": None}, "axis": {"grid": False, "domainColor": "#bbb"}}
}

# des_12: twin chart hconcat — family by count + family by median mass
fam_count_rows = table("ana_10")  # columns: family, count, pct
fam_mass_rows = table("ana_11")   # columns: family, n, median_g, mean_g
common_color = {
    "domain": ["Ordinary chondrite", "Carbonaceous chondrite", "HED achondrite", "Iron meteorite", "Primitive/other achondrite", "Enstatite chondrite", "Stony-iron", "Lunar achondrite", "Rumuruti (R) chondrite", "Martian achondrite", "Other / Ungrouped", "Other chondrite", "Unknown"],
    "range": ["#7a9bbf", "#4f8a7d", "#a6736f", "#5f4b32", "#b09b6a", "#9b9be8", "#9b7e3f", "#bfb098", "#84a85a", "#c95d4d", "#888", "#aaa", "#ccc"]
}
# Lock both panels to the SAME y-axis order — sorted by row count, descending.
# This is what makes the "rank flip" visual: Iron meteorite stays at row 4 in both
# panels, but its bar is tiny on the left (by count) and the longest on the right (by mass).
FAMILY_ORDER = [r["family"] for r in sorted(fam_count_rows, key=lambda r: -r["pct"])]

# Merge into a single denormalised dataset with one row per family (13 rows, one per
# FAMILY_ORDER entry). Missing values are null. This is critical — when the two panels
# use SEPARATE datasets with different row counts, Vega-Lite shifts bars to fill gaps
# in the sort array and the labels stop matching the bars.
mass_by_family = {r["family"]: r for r in fam_mass_rows}
count_by_family = {r["family"]: r for r in fam_count_rows}
merged_fam_rows = []
for fam in FAMILY_ORDER:
    m = mass_by_family.get(fam, {})
    c = count_by_family.get(fam, {})
    merged_fam_rows.append({
        "family": fam,
        "pct": c.get("pct"),
        "count": c.get("count"),
        "median_g": m.get("median_g"),
        "n_with_mass": m.get("n"),
        "mean_g": m.get("mean_g"),
    })

des_12_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Family by count vs by median mass — shared y order to show the rank flip",
    "background": "transparent",
    "data": {"values": merged_fam_rows},
    "hconcat": [
        {
            "title": "By row count (% of catalogue)",
            "width": 280, "height": 360,
            "layer": [
                {
                    "mark": {"type": "bar", "tooltip": False, "opacity": 0.001},
                    "encoding": {
                        "y": {"field": "family", "type": "nominal", "sort": FAMILY_ORDER, "axis": {"title": None, "labelFontSize": 11, "labelLimit": 200}},
                        "x": {"datum": 0, "type": "quantitative", "scale": {"domain": [0, 90]}},
                        "x2": {"datum": 90}
                    }
                },
                {
                    "mark": {"type": "bar", "tooltip": True},
                    "encoding": {
                        "y": {"field": "family", "type": "nominal", "sort": FAMILY_ORDER, "axis": {"title": None, "labelFontSize": 11, "labelLimit": 200}},
                        "x": {"field": "pct", "type": "quantitative", "scale": {"domain": [0, 90]}, "axis": {"title": "% of catalogue", "format": ".0f"}},
                        "color": {"field": "family", "type": "nominal", "scale": common_color, "legend": None},
                        "tooltip": [
                            {"field": "family", "type": "nominal", "title": "Family"},
                            {"field": "count", "type": "quantitative", "title": "Count", "format": ","},
                            {"field": "pct", "type": "quantitative", "title": "% of catalogue", "format": ".2f"},
                            {"field": "median_g", "type": "quantitative", "title": "Median mass (g)", "format": ",.1f"}
                        ]
                    }
                }
            ]
        },
        {
            "title": "By median mass (grams, log)",
            "width": 280, "height": 360,
            "layer": [
                {
                    "mark": {"type": "bar", "tooltip": False, "opacity": 0.001},
                    "encoding": {
                        "y": {"field": "family", "type": "nominal", "sort": FAMILY_ORDER, "axis": {"title": None, "labels": False, "ticks": False, "domain": True}},
                        "x": {"datum": 5, "type": "quantitative", "scale": {"type": "log", "domain": [5, 20000]}},
                        "x2": {"datum": 20000}
                    }
                },
                {
                    "transform": [{"filter": "datum.median_g != null"}],
                    "mark": {"type": "bar", "tooltip": True},
                    "encoding": {
                        "y": {"field": "family", "type": "nominal", "sort": FAMILY_ORDER, "axis": {"title": None, "labels": False, "ticks": False, "domain": True}},
                        "x": {"field": "median_g", "type": "quantitative", "scale": {"type": "log", "domain": [5, 20000]}, "axis": {"title": "Median mass (g, log)", "format": ",d"}},
                        "x2": {"datum": 5},
                        "color": {"field": "family", "type": "nominal", "scale": common_color, "legend": None},
                        "tooltip": [
                            {"field": "family", "type": "nominal", "title": "Family"},
                            {"field": "median_g", "type": "quantitative", "title": "Median mass (g)", "format": ",.1f"},
                            {"field": "mean_g", "type": "quantitative", "title": "Mean mass (g)", "format": ",.0f"},
                            {"field": "n_with_mass", "type": "quantitative", "title": "Rows with mass", "format": ","}
                        ]
                    }
                }
            ]
        }
    ],
    "resolve": {"scale": {"y": "shared", "color": "shared"}},
    "config": {"view": {"stroke": None}, "axis": {"grid": False, "domainColor": "#bbb"}}
}

# des_13: stacked-area Antarctica vs RestOfWorld by decade
ant_rows = table("ana_19")  # columns: decade, RestOfWorld, Antarctica, Total, Antarctica_share_pct
ant_long = []
for r in ant_rows:
    ant_long.append({"decade": r["decade"], "region": "Antarctica", "count": r["Antarctica"]})
    ant_long.append({"decade": r["decade"], "region": "Rest of world", "count": r["RestOfWorld"]})

des_13_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Antarctic share by decade",
    "width": "container",
    "height": 340,
    "background": "transparent",
    "data": {"values": ant_long},
    "layer": [
        {
            "mark": {"type": "area", "tooltip": True, "opacity": 0.88, "interpolate": "monotone"},
            "encoding": {
                "x": {"field": "decade", "type": "ordinal", "axis": {"title": "Decade", "labelAngle": -40, "labelFontSize": 11}},
                "y": {"field": "count", "type": "quantitative", "axis": {"title": "Geocoded meteorites entered"}, "stack": "zero"},
                "color": {
                    "field": "region", "type": "nominal",
                    "scale": {"domain": ["Antarctica", "Rest of world"], "range": ["#a8c9e8", "#c97a55"]},
                    "legend": {"title": "Region", "orient": "top-left"}
                },
                "order": {"field": "region", "type": "nominal", "sort": ["Antarctica", "Rest of world"]}
            }
        },
        {
            "data": {"values": [
                {"decade": 1980, "y": 4500, "label": "1980s: 93% Antarctic"},
                {"decade": 2000, "y": 14000, "label": "2000s: hot deserts catch up"}
            ]},
            "mark": {"type": "text", "color": "#222", "fontSize": 11, "fontWeight": 600, "align": "center"},
            "encoding": {
                "x": {"field": "decade", "type": "ordinal"},
                "y": {"field": "y", "type": "quantitative"},
                "text": {"field": "label"}
            }
        }
    ],
    "config": {"view": {"stroke": None}, "axis": {"grid": False, "domainColor": "#bbb"}}
}

# === HTML body content ===

# Compact map data for inline use
fells = map_data["fells"]
founds = map_data["founds"]

# 20-note sonification timing: 8 sec / 20 = 0.4s per note
SONIFY_NOTE_S = 0.4

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Almost nobody sees one fall — the meteorite catalogue is a map of where we looked</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="https://cdn.jsdelivr.net/npm/vega@5.30.0"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@5.21.0"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@6.26.0"></script>
<style>
:root {{
  --bg: #f7f4ee;
  --fg: #1f1f1f;
  --muted: #5a5a5a;
  --rule: #d8d3c8;
  --accent: #b94a2c;
  --iron: #5f4b32;
  --serif: 'Iowan Old Style', Georgia, 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: var(--bg); color: var(--fg); font-family: var(--serif); font-size: 18px; line-height: 1.6; -webkit-font-smoothing: antialiased; }}
.story {{ max-width: 720px; margin: 0 auto; padding: 4rem 1.5rem 6rem; }}
.story p {{ margin: 0 0 1.1rem; }}

/* Teaser */
.teaser {{ position: relative; width: 100vw; height: 90vh; min-height: 540px; overflow: hidden; background: #111; }}
.teaser video, .teaser img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.teaser-overlay {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: flex-end; padding: 6rem 2rem 3rem; background: linear-gradient(to bottom, transparent 40%, rgba(0,0,0,0.78) 100%); color: #f7f4ee; }}
.teaser-overlay h1 {{ font-family: var(--serif); font-size: clamp(2.4rem, 6vw, 5rem); line-height: 1.05; margin: 0 0 0.5rem; max-width: 18ch; font-weight: 600; }}
.teaser-overlay p {{ font-family: var(--sans); font-size: 1.1rem; max-width: 40ch; color: #d6d2c7; margin: 0 0 0.2rem; letter-spacing: 0.01em; }}
.teaser-credit {{ position: absolute; right: 1.2rem; bottom: 0.6rem; color: rgba(255,255,255,0.55); font-family: var(--sans); font-size: 0.72rem; letter-spacing: 0.02em; }}

/* Sections */
section {{ margin-top: 3.4rem; padding-top: 0.5rem; }}
section h2 {{ font-family: var(--serif); font-weight: 600; font-size: 1.9rem; line-height: 1.18; margin: 0 0 1.6rem; border-top: 1px solid var(--rule); padding-top: 1.6rem; }}

/* Stat callout */
.stat-callout {{ margin: 2rem 0 2.4rem; padding: 1.4rem 1.2rem; background: #fff; border-left: 6px solid var(--accent); display: block; text-align: left; box-shadow: 0 1px 0 rgba(0,0,0,0.04); }}
.stat-callout .stat-eyebrow {{ font-family: var(--sans); font-size: 0.7rem; letter-spacing: 0.18em; color: var(--muted); margin-bottom: 0.4rem; text-transform: uppercase; }}
.stat-callout .stat-number {{ font-family: var(--serif); font-size: clamp(3.6rem, 9vw, 5.6rem); font-weight: 700; line-height: 1; color: var(--accent); display: block; margin: 0.1rem 0; letter-spacing: -0.02em; }}
.stat-callout .stat-caption {{ font-family: var(--serif); font-size: 1.02rem; color: var(--muted); margin-top: 0.4rem; max-width: 36ch; }}

/* Quiz */
.quiz {{ margin: 2.4rem 0; padding: 1.6rem 1.4rem; background: #fff; border: 1px solid var(--rule); }}
.quiz .quiz-prompt {{ font-family: var(--sans); font-size: 0.95rem; color: var(--muted); margin: 0 0 1rem; }}
.quiz .quiz-options {{ display: flex; flex-wrap: wrap; gap: 0.6rem; margin: 0 0 1rem; }}
.quiz button {{ font-family: var(--sans); font-size: 0.95rem; padding: 0.6rem 1.2rem; background: #f0ece3; border: 1px solid var(--rule); cursor: pointer; transition: all 0.18s ease; }}
.quiz button:hover {{ background: #e8e2d3; }}
.quiz button.selected {{ background: var(--fg); color: #fff; border-color: var(--fg); }}
.quiz button:disabled {{ cursor: default; }}
.quiz-reveal {{ display: none; margin-top: 1.2rem; padding-top: 1rem; border-top: 1px dashed var(--rule); font-family: var(--sans); font-size: 0.92rem; color: var(--muted); }}
.quiz-bars {{ display: grid; grid-template-columns: 7em 1fr; gap: 0.4rem 0.8rem; align-items: center; margin: 0.6rem 0; }}
.quiz-bars .bar {{ height: 18px; display: block; background: var(--rule); position: relative; }}
.quiz-bars .bar.you {{ background: #cbb89b; }}
.quiz-bars .bar.real {{ background: var(--accent); }}
.quiz-bars .bar-label {{ font-size: 0.85rem; color: var(--fg); }}
.quiz-bars .bar-value {{ font-size: 0.78rem; color: var(--muted); margin-left: 0.4rem; }}

/* Figures */
figure {{ margin: 2.4rem auto; display: block; }}
figure img {{ width: 100%; height: auto; max-width: 100%; display: block; }}
figcaption {{ font-family: var(--sans); font-size: 0.82rem; color: var(--muted); margin-top: 0.6rem; line-height: 1.45; }}

/* Charts */
.chart-container {{ margin: 2.4rem auto; padding: 1.2rem 0; width: 100%; max-width: 720px; }}
.chart-container canvas, .chart-container svg {{ max-width: 100%; }}

/* Map — body has no max-width so 100% naturally fills the viewport */
.map-section {{ margin: 3rem 0; position: relative; width: 100%; }}
.map-wrap {{ width: 100%; position: relative; }}
.map-frame {{ height: 560px; width: 100%; background: #1a1a1a; }}
.map-controls {{ position: absolute; top: 14px; left: 14px; z-index: 800; background: rgba(20, 16, 12, 0.86); color: #f7f4ee; padding: 0.8rem 1rem; font-family: var(--sans); font-size: 0.84rem; line-height: 1.45; max-width: 260px; border: 1px solid rgba(247, 244, 238, 0.08); }}
.map-controls .legend-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; vertical-align: middle; margin-right: 6px; border: 1px solid rgba(247, 244, 238, 0.35); }}
.map-controls label {{ display: block; margin-top: 0.55rem; cursor: pointer; }}
.map-controls input {{ margin-right: 6px; }}
.map-caption {{ font-family: var(--sans); font-size: 0.82rem; color: var(--muted); margin-top: 0.6rem; max-width: 720px; margin-left: auto; margin-right: auto; padding: 0 1.5rem; line-height: 1.45; }}

/* Audio container */
.audio-container {{ margin: 2rem 0; padding: 1.2rem 1.2rem; background: #fff; border: 1px solid var(--rule); display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }}
.audio-container .audio-label {{ font-family: var(--sans); font-size: 0.85rem; color: var(--muted); flex: 1 1 auto; min-width: 180px; }}
.audio-container .audio-label strong {{ display: block; color: var(--fg); font-size: 0.95rem; font-weight: 600; margin-bottom: 2px; }}
.audio-container .audio-now {{ font-family: var(--sans); font-size: 0.85rem; color: var(--accent); font-weight: 600; margin-top: 0.4rem; min-height: 1.2em; }}
.audio-container audio {{ flex: 1 1 280px; min-width: 240px; }}

/* Vega bars highlight class (sonification) */
.sonify-bar-highlight {{ stroke: #b94a2c !important; stroke-width: 2.5px !important; }}

/* References */
.references {{ margin-top: 5rem; padding-top: 2rem; border-top: 1px solid var(--rule); font-family: var(--sans); font-size: 0.85rem; color: var(--muted); }}
.references h3 {{ font-family: var(--serif); font-weight: 600; font-size: 1.1rem; color: var(--fg); margin: 0 0 0.8rem; }}
.references ul {{ margin: 0; padding-left: 1.2rem; }}
.references li {{ margin-bottom: 0.4rem; line-height: 1.5; }}
.references a {{ color: var(--accent); }}

a {{ color: var(--accent); }}

@media (max-width: 600px) {{
  .story {{ padding: 2.5rem 1.2rem 4rem; }}
  .teaser {{ height: 80vh; min-height: 480px; }}
  .map-frame {{ height: 420px; }}
}}
</style>
</head>
<body>

<!-- ============================================================ -->
<!-- Teaser — full-viewport. Video plays; falls back to static image. -->
<!-- ============================================================ -->
<div class="teaser" data-des-group="teaser">
  <video autoplay loop muted playsinline data-des="des_02" poster="assets/ref_hoba.jpg">
    <source src="assets/teaser_hoba_motion.mp4" type="video/mp4">
  </video>
  <img src="assets/ref_hoba.jpg" data-des="des_01" alt="The Hoba meteorite, a 60-tonne iron block in Namibia" style="display:none">
  <div class="teaser-overlay">
    <h1>Almost nobody sees one fall</h1>
    <p>How the meteorite catalogue is really made</p>
  </div>
  <div class="teaser-credit">Hoba meteorite, Namibia — photo CC BY 2.0 Eugen Zibiso / Wikimedia Commons</div>
</div>

<article class="story">

<!-- ============================================================ -->
<!-- edt_01 — Hook: Almost nobody sees one fall -->
<!-- ============================================================ -->
<section data-edt="edt_01" data-det="det_02,det_03">

  <h2>Almost nobody sees one fall</h2>

  <div class="stat-callout" data-des="des_03" data-ana="ana_04,ana_01">
    <div class="stat-eyebrow">Observed falls</div>
    <div class="stat-number">2.42%</div>
    <div class="stat-caption">of the 45,716 named meteorites in the catalogue were ever observed falling. 1,107 of them. The other 44,609 were found later.</div>
  </div>

  <p data-ana="ana_04" data-det="det_02">The Meteoritical Society catalogues 45,716 named meteorites. Only 1,107 of them — 2.42% — were ever observed during the fall itself. The rest are Finds: rocks recognised on the ground at some unknown later date, sometimes thousands of years after they landed.</p>

  <p data-ana="ana_18" data-det="det_03">The witnessing rate is roughly six observed falls per year worldwide, and it has been roughly six per year for as long as anyone has been counting. The Earth gets hit by an estimated 1,800 land-falls every year. So the chance that any given fall enters the catalogue as a witnessed event is well under one percent.</p>

  <p>Everything else this blog covers is a consequence of that gap.</p>

  <div class="quiz" id="des_04_quiz" data-des="des_04" data-ana="ana_04">
    <div class="quiz-prompt">Quick guess — of the 45,716 named meteorites in this catalogue, roughly what fraction were ever observed falling?</div>
    <div class="quiz-options" id="quiz-options">
      <button data-pct="20">1 in 5 (20%)</button>
      <button data-pct="10">1 in 10 (10%)</button>
      <button data-pct="5">1 in 20 (5%)</button>
      <button data-pct="2">1 in 50 (2%)</button>
    </div>
    <div class="quiz-reveal" id="quiz-reveal">
      <div class="quiz-bars" id="quiz-bars"></div>
      <div id="quiz-comment"></div>
    </div>
  </div>

</section>

<!-- ============================================================ -->
<!-- edt_02 — The Find explosion of 1969 -->
<!-- ============================================================ -->
<section data-edt="edt_02" data-det="det_04">

  <h2>The Find explosion of 1969</h2>

  <p data-ana="ana_07">The cleanest way to see the catalogue's shape is to split it at 1970. Before 1970, the dataset records 1,431 Finds. After 1970, it records 42,886 — a thirty-fold jump that is the single biggest pattern in the data.</p>

  <p data-ana="ana_06">Decade-by-decade counts make the timing impossible to miss. Through the 1960s, Finds tick along at a few hundred per decade. In the 1970s the number jumps to 4,909. In the 1990s it crosses ten thousand. In the 2000s alone, more meteorites enter the catalogue (17,698) than in the entire previous century combined.</p>

  <p data-det="det_04">Nothing changed in the sky in 1969. What changed is that the first systematic Antarctic search began. Japanese and then American teams started driving snowmobiles across blue-ice fields where katabatic winds had spent millennia scouring meteorites back to the surface. ANSMET alone has now recovered more than 23,000 specimens — more than half of every meteorite humans have ever named.</p>

  <div class="chart-container" id="des_05" data-des="des_05" data-ana="ana_06"></div>

  <figure data-des="des_06">
    <img src="assets/ref_antarctic_recovery.jpg" alt="A researcher recovering a meteorite from Antarctic ice" data-des="des_06">
    <figcaption>A researcher in the field with a newly-found meteorite, Antarctica. The operational shift behind the 1970s spike. <i>(Public domain, NASA / H. Raab via Wikimedia Commons.)</i></figcaption>
  </figure>

</section>

<!-- ============================================================ -->
<!-- edt_03 — A map of where humans looked -->
<!-- ============================================================ -->
<section data-edt="edt_03" data-det="det_04">

  <h2>A map of where humans looked</h2>

  <p data-ana="ana_14">Among the 38,400 catalogue rows with coordinates, 22,099 — 59.2% — are below latitude -60. All 22,099 are Finds. The Antarctic ice contributes more than half of every geocoded meteorite humans have ever recovered, and zero observed falls.</p>

  <p data-ana="ana_15">Strip Antarctica away and the remaining geography is itself almost all desert. The Arabian peninsula and Oman supply 3,154 rocks; the Sahara and Sahel 2,414; the US southwest 1,063; the Australian outback 540; the Atacama 415. The single hottest five-degree cell outside Antarctica is the corner of West Africa where longitude zero crosses the Sahara, with more than six thousand entries.</p>

  <p>The pattern is not that meteorites prefer cold or dry land. It is that on cold or dry land they stand out, and on cold or dry land humans now go looking.</p>

</section>

<div class="map-section">
  <div class="map-wrap">
    <div class="map-frame" id="des_07" data-des="des_07" data-ana="ana_14,ana_15"></div>
    <div class="map-controls">
      <div><span class="legend-dot" style="background:#b94a2c"></span>Observed fall (1,096 shown)</div>
      <div><span class="legend-dot" style="background:#7a9bbf"></span>Later find (1,669 shown — 2,000-row random sample)</div>
      <label><input type="checkbox" id="toggle-founds" checked> Show Finds layer</label>
      <label><input type="checkbox" id="toggle-fells" checked> Show Fells layer</label>
    </div>
  </div>
  <div class="map-caption">Each red dot is a meteorite someone watched fall; each blue dot is a meteorite found later. 16% of catalogue rows have no coordinates and are silently dropped from this map; Founds are shown as a 2,000-row random sample (full set is ~37,300). Antarctic ice and the three hot-desert belts dominate the blue layer — the catalogue is largely a record of where field teams went looking. <i>(Basemap: CartoDB Dark Matter. Data: Meteoritical Bulletin via NASA Open Data Portal.)</i></div>
</div>

<article class="story" style="margin-top: 0; padding-top: 1rem;">

<!-- ============================================================ -->
<!-- edt_04 — Ten orders of magnitude, log-normal -->
<!-- ============================================================ -->
<section data-edt="edt_04" data-det="det_07">

  <h2>Ten orders of magnitude, log-normal</h2>

  <p data-ana="ana_08">Meteorite masses span more than ten orders of magnitude — from sub-gram chips to the sixty-tonne Hoba. The median rock weighs 32.7 grams (about a tomato). The arithmetic mean is 13.3 kilograms (a cinder block), four hundred times larger than the median. That ratio is the canonical signature of a heavy-tailed distribution: a small number of giants and an army of pebbles.</p>

  <p data-ana="ana_05">The asymmetry shows up sharply across the Fell-vs-Found split. Median Fell mass is 2,800 grams; median Found mass is 30.5 grams. A typical witnessed meteorite is ninety-two times heavier than a typical recovered one. That makes physical sense: the only meteorites loud and bright enough to be seen mid-fall are the big ones. Antarctic and desert searches, by contrast, pick up gram-scale chips an eyewitness would never even notice.</p>

  <div class="chart-container" id="des_08" data-des="des_08" data-ana="ana_08"></div>

</section>

<!-- ============================================================ -->
<!-- edt_05 — The top 20 are a wall of iron -->
<!-- ============================================================ -->
<section data-edt="edt_05" data-det="det_05,det_07,det_08,det_09">

  <h2>The top 20 are a wall of iron</h2>

  <p data-ana="ana_09,ana_22">Sort the catalogue by mass and the top twenty rows are a wall of iron. Hoba (60 tonnes, Namibia), Cape York (58 tonnes, Greenland), Campo del Cielo (50 tonnes, Argentina), Canyon Diablo (30 tonnes, Arizona, the body that punched out Meteor Crater), Armanty (28 tonnes, Xinjiang). Every one is an iron meteorite. The first stony rock to appear — the Jilin H5 chondrite that fell on China in 1976 — does not show up until rank nineteen.</p>

  <p data-ana="ana_20" data-det="det_07">Widen the window to the top hundred and the bias holds: seventy-two of the heaviest hundred meteorites in the catalogue are irons, ten are stony-irons, only fifteen are ordinary chondrites. Yet irons are barely 2.3% of the catalogue by count. The heaviest meteorites on Earth are not a sample of what falls; they are a sample of what survives. Iron blocks shrug off atmospheric ablation and weather slowly enough that a 60-tonne lump can sit in a Namibian field for eighty thousand years and still be there to plough into.</p>

  <p data-det="det_08,det_05">Some of these rocks were the centre of their own stories long before the Meteoritical Society named them. The Inughuit of Greenland cold-forged iron tools from the Cape York fragments for centuries before Robert Peary sledged the largest three off the ice in the 1890s and sold the biggest one to the American Museum of Natural History for forty thousand dollars. Hoba was discovered in 1920 by a Namibian farmer ploughing a field; it was declared a national monument before anyone tried to move it.</p>

  <div class="chart-container" id="des_09" data-des="des_09" data-ana="ana_09"></div>

  <div class="audio-container" data-des="des_10" data-ana="ana_09">
    <div class="audio-label">
      <strong>Hear the top 20.</strong>
      Each meteorite gets one marimba note; pitch scales with log mass. The 60-tonne Hoba is the lowest note, the 3.8-tonne Vaca Muerta the highest.
      <div class="audio-now" id="sonify-now">Press play.</div>
    </div>
    <audio controls preload="metadata" src="assets/sonification_top20_mass.wav" id="sonify-audio" data-des="des_10" data-ana="ana_09"></audio>
  </div>

  <figure data-des="des_11">
    <img src="assets/ref_ahnighito.jpg" alt="The Ahnighito fragment of Cape York at the American Museum of Natural History" data-des="des_11">
    <figcaption>Ahnighito (Cape York fragment, 34 tonnes) — row 2 of the leaderboard. Its display stand at the American Museum of Natural History reaches down to the bedrock. <i>(Photo CC BY 2.0 Mike Cassano via Wikimedia Commons.)</i></figcaption>
  </figure>

</section>

<!-- ============================================================ -->
<!-- edt_06 — Counts say chondrite, mass says iron -->
<!-- ============================================================ -->
<section data-edt="edt_06" data-det="det_11">

  <h2>Counts say chondrite, mass says iron</h2>

  <p data-ana="ana_10" data-det="det_11">By row count, the catalogue is dominated by one composition family. Ordinary chondrites — H, L, and LL groups with petrologic types 3 through 6 — make up 86.96% of all entries (39,756 of 45,716). Carbonaceous chondrites are a distant second at 3.50%, followed by the HED achondrites at 2.59% and iron meteorites at 2.34%. The dataset's own breakdown matches the literature's "87% ordinary chondrite" benchmark almost to the decimal.</p>

  <p data-ana="ana_11">Now flip the lens to mass per row. Iron meteorites carry a median mass of 10,000 grams — ten kilograms. Ordinary chondrites' median is 28.5 grams. The typical iron is three hundred and fifty times heavier than the typical chondrite. So irons are 1 in 43 rows by count, but they dominate the heavy tail. The same flip explains why an analysis based on the top of the chart and an analysis based on row counts produce two completely different pictures of "what a meteorite is."</p>

  <p data-ana="ana_12">Witness rates by family expose a quieter selection effect. Iron meteorites and HED achondrites are observed falling at 4.6% and 5.1% respectively — roughly double the catalogue's overall 2.4% rate. Ordinary chondrites sit at the mean (2.1%). Lunar achondrites are 0.0%: none of the 165 lunar meteorites in the catalogue has ever been seen falling. Every one of them was recovered from Antarctic ice or hot-desert pavement, identified later in a lab.</p>

  <div class="chart-container" id="des_12" data-des="des_12" data-ana="ana_10,ana_11"></div>

</section>

<!-- ============================================================ -->
<!-- edt_07 — Close: catalogue is a record of where we looked -->
<!-- ============================================================ -->
<section data-edt="edt_07" data-det="det_04">

  <h2>The catalogue is a record of where we looked</h2>

  <p data-ana="ana_19">Decade-by-decade, the Antarctic share of the catalogue has its own history. In the 1970s and 1980s, blue-ice teams supplied 89-94% of every dated geocoded rock. In the 1990s, hot-desert programs in the Sahara and Arabia caught up; by the 2000s, Antarctica's share had dropped to 39% even as the absolute count kept rising. The frozen 2010s tail of the dataset shows the deserts now leading.</p>

  <p data-ana="ana_07">Lay all three numbers next to each other — 2.4% witnessed, 59% Antarctic, 97% post-1969 — and the meteorite catalogue stops looking like an inventory of what hits Earth and starts looking like an inventory of where and when humans looked for what hit Earth a long time ago. Witnessed falls are the only rows that approximate a random sample of what is really up there, and there are barely a thousand of them spread across twelve hundred years.</p>

  <p>Whatever the next forty thousand entries look like, the controlling variable will be the same: which search programs run, where, and for how long.</p>

  <div class="chart-container" id="des_13" data-des="des_13" data-ana="ana_19"></div>

  <figure data-des="des_14">
    <img src="assets/ref_meteor_crater.jpg" alt="Aerial view of Meteor Crater (Barringer Crater), Arizona" data-des="des_14">
    <figcaption>Meteor Crater — the only entry in this catalogue you can still see from orbit. Made by Canyon Diablo, row 4 by mass. <i>(USGS aerial photograph, public domain.)</i></figcaption>
  </figure>

</section>

<!-- References -->
<section class="references">
  <h3>References & data</h3>
  <ul>
    <li><b>Data source.</b> Meteoritical Bulletin Database, maintained by the Meteoritical Society's Nomenclature Committee — <a href="https://www.lpi.usra.edu/meteor/">lpi.usra.edu/meteor</a>. The snapshot used here is the NASA Open Data Portal mirror, surfaced via <a href="https://www.data-is-plural.com/archive/2020-07-29-edition/">Data Is Plural (2020-07-29)</a>. Public-domain release.</li>
    <li><b>Antarctic recovery context.</b> ANSMET — <a href="https://caslabs.case.edu/ansmet/faqs/">Case Western Reserve University FAQs</a>; <a href="https://en.wikipedia.org/wiki/ANSMET">ANSMET on Wikipedia</a>.</li>
    <li><b>Fall-rate benchmark.</b> <a href="https://en.wikipedia.org/wiki/Meteorite_fall_statistics">Meteorite fall statistics — Wikipedia</a>: ~1,800 land-falls/year, ~7.9 observed-fall reports/year (2007-2018), &gt;10/year since 2020.</li>
    <li><b>Composition reference.</b> <a href="https://en.wikipedia.org/wiki/Ordinary_chondrite">Ordinary chondrite — Wikipedia</a>; <a href="https://en.wikipedia.org/wiki/Glossary_of_meteoritics">Glossary of meteoritics</a>.</li>
    <li><b>Named-meteorite background.</b> Hoba: <a href="https://en.wikipedia.org/wiki/Hoba_meteorite">Wikipedia</a>; Cape York: <a href="https://en.wikipedia.org/wiki/Cape_York_meteorite">Wikipedia</a>; Campo del Cielo: <a href="https://en.wikipedia.org/wiki/Campo_del_Cielo">Wikipedia</a>; Canyon Diablo / Meteor Crater: <a href="https://en.wikipedia.org/wiki/Canyon_Diablo_(meteorite)">Wikipedia</a>; Armanty / Aletai: <a href="https://en.wikipedia.org/wiki/Aletai_meteorite">Wikipedia</a>.</li>
    <li><b>Reference photos.</b> Hoba (CC BY 2.0, Eugen Zibiso); Ahnighito (CC BY 2.0, Mike Cassano); Canyon Diablo fragment, El Chaco fragment, ALH81005 lunar meteorite — Wikimedia Commons; Antarctic recovery photo & Meteor Crater aerial — public domain (NASA / USGS).</li>
    <li><b>Built with.</b> Vega-Lite 5, Leaflet 1.9, Web Audio API, vanilla JS. Charts and stats traced via <code>data-edt</code> / <code>data-ana</code> / <code>data-des</code> / <code>data-det</code> attributes.</li>
  </ul>
</section>

</article>

<script>
// ============================================================
// Data inlined from analyst.json data_tables and from the
// analyst's pre-curated map sample.
// ============================================================
const DES05_SPEC = {json.dumps(des_05_spec, ensure_ascii=False)};
const DES08_SPEC = {json.dumps(des_08_spec, ensure_ascii=False)};
const DES09_SPEC = {json.dumps(des_09_spec, ensure_ascii=False)};
const DES12_SPEC = {json.dumps(des_12_spec, ensure_ascii=False)};
const DES13_SPEC = {json.dumps(des_13_spec, ensure_ascii=False)};
const TOP20 = {json.dumps(top20_rows, ensure_ascii=False)};
const MAP_FELLS = {json.dumps(fells, ensure_ascii=False)};
const MAP_FOUNDS = {json.dumps(founds, ensure_ascii=False)};

// ------- Render Vega-Lite charts -------
function renderAll() {{
  vegaEmbed('#des_05', DES05_SPEC, {{actions: false}}).catch(console.error);
  vegaEmbed('#des_08', DES08_SPEC, {{actions: false}}).catch(console.error);
  vegaEmbed('#des_09', DES09_SPEC, {{actions: false}}).then(r => {{
    window._vegaTop20 = r;
  }}).catch(console.error);
  vegaEmbed('#des_12', DES12_SPEC, {{actions: false}}).catch(console.error);
  vegaEmbed('#des_13', DES13_SPEC, {{actions: false}}).catch(console.error);
}}

// ------- Leaflet map -------
function initMap() {{
  const map = L.map('des_07', {{
    center: [10, 0],
    zoom: 2,
    minZoom: 2,
    maxZoom: 6,
    worldCopyJump: false,
    preferCanvas: true,
    zoomControl: true,
    attributionControl: true
  }});
  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}.png', {{
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  }}).addTo(map);

  const foundsLayer = L.layerGroup();
  MAP_FOUNDS.forEach(([lat, lon, name, mass, year]) => {{
    L.circleMarker([lat, lon], {{
      radius: 2.5,
      color: '#7a9bbf',
      weight: 0,
      fillColor: '#7a9bbf',
      fillOpacity: 0.75
    }}).bindPopup(`<b>${{name}}</b><br>Find · ${{year || 'no year'}} · ${{mass ? mass.toLocaleString() + ' kg' : 'no mass'}}`).addTo(foundsLayer);
  }});

  const fellsLayer = L.layerGroup();
  MAP_FELLS.forEach(([lat, lon, name, mass, year]) => {{
    L.circleMarker([lat, lon], {{
      radius: 4,
      color: 'rgba(247,244,238,0.6)',
      weight: 0.8,
      fillColor: '#b94a2c',
      fillOpacity: 0.92
    }}).bindPopup(`<b>${{name}}</b><br>Observed Fell · ${{year || 'no year'}} · ${{mass ? mass.toLocaleString() + ' kg' : 'no mass'}}`).addTo(fellsLayer);
  }});

  foundsLayer.addTo(map);
  fellsLayer.addTo(map);

  document.getElementById('toggle-founds').addEventListener('change', e => {{
    if (e.target.checked) foundsLayer.addTo(map); else map.removeLayer(foundsLayer);
  }});
  document.getElementById('toggle-fells').addEventListener('change', e => {{
    if (e.target.checked) fellsLayer.addTo(map); else map.removeLayer(fellsLayer);
  }});
}}

// ------- Quiz logic -------
function initQuiz() {{
  const opts = document.getElementById('quiz-options');
  const reveal = document.getElementById('quiz-reveal');
  const bars = document.getElementById('quiz-bars');
  const comment = document.getElementById('quiz-comment');
  const REAL_PCT = 2.42;
  opts.addEventListener('click', e => {{
    const btn = e.target.closest('button');
    if (!btn) return;
    Array.from(opts.querySelectorAll('button')).forEach(b => {{ b.disabled = true; b.classList.remove('selected'); }});
    btn.classList.add('selected');
    const guess = parseFloat(btn.dataset.pct);
    const maxPct = Math.max(guess, REAL_PCT) * 1.15;
    bars.innerHTML = `
      <div class="bar-label">Your guess</div>
      <div><span class="bar you" style="width: ${{(guess/maxPct*100).toFixed(1)}}%"></span><span class="bar-value">${{guess}}%</span></div>
      <div class="bar-label">Actual</div>
      <div><span class="bar real" style="width: ${{(REAL_PCT/maxPct*100).toFixed(1)}}%"></span><span class="bar-value">${{REAL_PCT}}% — 1,107 of 45,716</span></div>
    `;
    let txt;
    if (guess === 2) txt = 'Spot on. Most readers overshoot by 2-10x.';
    else if (guess === 5) txt = 'Closer than most. The catalogue is even sparser than 1 in 20.';
    else if (guess === 10) txt = 'Off by ~4x. There is no observed fall about half the days of the year — fewer than 7 worldwide per year.';
    else txt = 'A common guess, and a long way off. There are roughly six observed falls per year — across the entire planet.';
    comment.textContent = txt;
    reveal.style.display = 'block';
  }});
}}

// ------- Sonification: chart-synced highlight -------
function initSonify() {{
  const audio = document.getElementById('sonify-audio');
  const now = document.getElementById('sonify-now');
  const noteSecs = {SONIFY_NOTE_S};
  const names = TOP20.map(r => r.name);
  let lastIdx = -1;
  function highlightBar(idx) {{
    const svg = document.querySelector('#des_09 svg');
    if (!svg) return;
    svg.querySelectorAll('.sonify-bar-highlight').forEach(el => el.classList.remove('sonify-bar-highlight'));
    const bars = svg.querySelectorAll('g.mark-rect path, g.mark-rect rect');
    // Vega-Lite renders bars in data order; sort "-x" reorders the y axis but data index is unchanged.
    // We highlight by the rank position from the top instead — bars are top-to-bottom in y order.
    if (bars[idx]) bars[idx].classList.add('sonify-bar-highlight');
  }}
  audio.addEventListener('timeupdate', () => {{
    const t = audio.currentTime;
    const idx = Math.min(TOP20.length - 1, Math.floor(t / noteSecs));
    if (idx !== lastIdx) {{
      lastIdx = idx;
      highlightBar(idx);
      const rec = TOP20[idx];
      if (rec) now.textContent = `▶ ${{rec.name}} — ${{(rec.mass_kg).toLocaleString()}} kg (${{rec.family}})`;
    }}
  }});
  audio.addEventListener('ended', () => {{
    now.textContent = 'Done — all 20.';
    const svg = document.querySelector('#des_09 svg');
    if (svg) svg.querySelectorAll('.sonify-bar-highlight').forEach(el => el.classList.remove('sonify-bar-highlight'));
  }});
  audio.addEventListener('play', () => {{
    now.textContent = '▶ Starting…';
  }});
  audio.addEventListener('pause', () => {{
    if (!audio.ended) now.textContent = 'Paused.';
  }});
}}

// ------- Boot -------
document.addEventListener('DOMContentLoaded', () => {{
  renderAll();
  initMap();
  initQuiz();
  initSonify();
}});
</script>

</body>
</html>
"""

(PROJ / "index.html").write_text(HTML, encoding="utf-8")
print(f"wrote index.html ({len(HTML)} chars)")
