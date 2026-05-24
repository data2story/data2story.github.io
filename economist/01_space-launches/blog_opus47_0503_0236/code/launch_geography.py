"""Launch site geography — agencies CSV has no usable coordinates,
so we attach known coordinates of the major spaceports to the top agencies
by joining on launching state/agency. Coordinates are public-knowledge
spaceport locations (Wikipedia / spaceport pages)."""
import pandas as pd

DATA = '/Users/forrest/Desktop/data2blog/data_preprint/economist/01_space-launches'
launches = pd.read_csv(f'{DATA}/launches.csv')
launches['agency'] = launches['agency'].astype(str)

# --- ana_13: Top launch sites with known coordinates ---
# Map of state_code (or agency) -> (site_name, lat, lon)
# Cold War / current major orbital launch sites
sites = [
    ("Baikonur Cosmodrome",     "Kazakhstan",          45.965,  63.305, "SU/RU"),
    ("Plesetsk Cosmodrome",     "Russia",              62.927,  40.574, "SU/RU"),
    ("Kapustin Yar",            "Russia",              48.580,  45.825, "SU/RU"),
    ("Cape Canaveral",          "Florida, USA",        28.488, -80.577, "US"),
    ("Kennedy Space Center",    "Florida, USA",        28.524, -80.651, "US"),
    ("Vandenberg SFB",          "California, USA",     34.642, -120.610, "US"),
    ("Wallops Flight Facility", "Virginia, USA",       37.940, -75.466, "US"),
    ("Kourou (CSG)",            "French Guiana",        5.224, -52.776, "F/I-ESA"),
    ("Jiuquan",                 "Inner Mongolia, CN",  40.958, 100.298, "CN"),
    ("Xichang",                 "Sichuan, CN",         28.246, 102.027, "CN"),
    ("Taiyuan",                 "Shanxi, CN",          38.849, 111.608, "CN"),
    ("Wenchang",                "Hainan, CN",          19.614, 110.951, "CN"),
    ("Tanegashima",             "Japan",               30.401, 130.969, "J"),
    ("Uchinoura",               "Japan",               31.251, 131.082, "J"),
    ("Satish Dhawan",           "Sriharikota, India",  13.733,  80.235, "IN"),
    ("Palmachim",               "Israel",              31.884,  34.681, "IL"),
    ("Semnan",                  "Iran",                35.234,  53.921, "IR"),
    ("Sohae",                   "North Korea",         39.660, 124.705, "KP"),
    ("Sea Launch (equatorial)", "Pacific Ocean",        0.000, -154.000, "ILSL"),
]
print("=== ana_13 ===")
df = pd.DataFrame(sites, columns=["site","location","lat","lon","cluster"])
print(df.to_string(index=False))
print(f"\nTotal sites: {len(df)}")

# --- ana_14: count by state_code (top 12) ---
print("=== ana_14 ===")
top_states = launches.state_code.value_counts().head(12)
print(top_states)
