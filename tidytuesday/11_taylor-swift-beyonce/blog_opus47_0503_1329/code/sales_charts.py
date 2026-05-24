"""Album sales and chart-position analysis."""
import pandas as pd
import re
from pathlib import Path

DATA = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/11_taylor-swift-beyonce")
sales = pd.read_csv(DATA / "sales.csv")
charts = pd.read_csv(DATA / "charts.csv")
sales["sales"] = pd.to_numeric(sales["sales"], errors="coerce")
charts["chart_position"] = pd.to_numeric(charts["chart_position"], errors="coerce")

# parse release year from "October 24, 2006" etc
def parse_year(x):
    if not isinstance(x, str): return None
    m = re.search(r"\b(19|20)\d{2}\b", x)
    return int(m.group(0)) if m else None
sales["year"] = sales["released"].map(parse_year)
charts["year"] = charts["released"].map(parse_year)

# --- ana_07: WW album sales ranking ---
print("=== ana_07 ===")
ww = sales[sales["country"] == "WW"].sort_values("sales", ascending=False)
print("Worldwide album sales (millions):")
ww_disp = ww[["artist","title","year","sales"]].copy()
ww_disp["sales_M"] = (ww_disp["sales"]/1e6).round(2)
print(ww_disp[["artist","title","year","sales_M"]].to_string(index=False))
print(f"Taylor WW total: {ww[ww.artist=='Taylor Swift']['sales'].sum()/1e6:.2f}M")
print(f"Beyoncé WW total: {ww[ww.artist=='Beyoncé']['sales'].sum()/1e6:.2f}M")

# --- ana_08: US album sales ranking ---
print()
print("=== ana_08 ===")
us = sales[sales["country"] == "US"].sort_values("sales", ascending=False)
us_disp = us[["artist","title","year","sales"]].copy()
us_disp["sales_M"] = (us_disp["sales"]/1e6).round(2)
print("US album sales (millions):")
print(us_disp[["artist","title","year","sales_M"]].to_string(index=False))
print(f"Taylor US total: {us[us.artist=='Taylor Swift']['sales'].sum()/1e6:.2f}M")
print(f"Beyoncé US total: {us[us.artist=='Beyoncé']['sales'].sum()/1e6:.2f}M")

# --- ana_09: Sales by country tile ---
print()
print("=== ana_09 ===")
country_sums = sales.groupby(["artist","country"])["sales"].sum().reset_index()
print("Total sales (millions) by artist x country:")
country_sums["sales_M"] = (country_sums["sales"]/1e6).round(2)
print(country_sums.sort_values(["country","artist"]).to_string(index=False))

# --- ana_10: Hit-rate (peaked at #1) per artist by country ---
print()
print("=== ana_10 ===")
no1 = charts.dropna(subset=["chart_position"]).copy()
no1["is_no1"] = no1["chart_position"] == 1
hit = no1.groupby(["artist","chart"]).agg(num_albums=("title","nunique"), n1s=("is_no1","sum")).reset_index()
hit["pct_no1"] = (hit["n1s"]/hit["num_albums"]*100).round(1)
print(hit.sort_values(["chart","artist"]).to_string(index=False))

# overall #1 percentage
print()
overall = no1.groupby("artist").agg(total=("chart_position","count"), n1s=("is_no1","sum")).reset_index()
overall["pct"] = (overall["n1s"]/overall["total"]*100).round(1)
print("Overall #1 rate (across countries):")
print(overall.to_string(index=False))

# --- ana_11: Per-album world chart performance (median peak) ---
print()
print("=== ana_11 ===")
albums = charts.dropna(subset=["chart_position"]).copy()
album_perf = albums.groupby(["artist","title","year"]).agg(
    median_peak=("chart_position","median"),
    n_charts=("chart","nunique"),
    n1s=("chart_position", lambda s: (s==1).sum())
).reset_index().sort_values(["artist","year"])
print(album_perf.to_string(index=False))

# --- ana_12: Total worldwide units (different country labels per artist) ---
print()
print("=== ana_12 ===")
# Beyonce uses "World", Taylor uses "WW"
ww_labels = {"Taylor Swift": "WW", "Beyoncé": "World"}
total_t = sales[(sales.country=="WW") & (sales.artist=="Taylor Swift")]["sales"].sum()
total_b = sales[(sales.country=="World") & (sales.artist=="Beyoncé")]["sales"].sum()
print(f"WW total units (Beyoncé, label='World'): {total_b/1e6:.2f}M (4 albums reported)")
print(f"WW total units (Taylor, label='WW'): {total_t/1e6:.2f}M (6 albums reported)")
print(f"Taylor / Beyoncé worldwide units ratio: {total_t/total_b:.2f}x")
# Per-album average:
b_albums = sales[(sales.country=="World") & (sales.artist=="Beyoncé")]
t_albums = sales[(sales.country=="WW") & (sales.artist=="Taylor Swift")]
print(f"Beyoncé worldwide-reported albums: {sorted(b_albums['title'].tolist())}")
print(f"Taylor worldwide-reported albums: {sorted(t_albums['title'].tolist())}")
print(f"Beyoncé avg WW units/album: {b_albums['sales'].mean()/1e6:.2f}M")
print(f"Taylor avg WW units/album: {t_albums['sales'].mean()/1e6:.2f}M")
# show full beyonce world breakdown
print()
print("Beyoncé worldwide breakdown:")
print(b_albums[["title","year","sales"]].assign(sales_M=lambda d:(d.sales/1e6).round(2)).to_string(index=False))
