"""Profile the four CSVs in DATA_DIR and produce dataset-level statistics."""
import pandas as pd
import os

DATA_DIR = "/Users/forrest/Desktop/data2blog/data_preprint/pudding/06_register/data"

songs = pd.read_csv(os.path.join(DATA_DIR, "songs.csv"))
y2019 = pd.read_csv(os.path.join(DATA_DIR, "2019.csv"))
avg = pd.read_csv(os.path.join(DATA_DIR, "avg.csv"))
avg_top = pd.read_csv(os.path.join(DATA_DIR, "avg_top.csv"))

# --- ana_profile: Dataset profile ---
print("=== ana_profile ===")
print("songs.csv:", songs.shape, "cols:", list(songs.columns))
print("2019.csv:", y2019.shape, "cols:", list(y2019.columns))
print("avg.csv:", avg.shape, "cols:", list(avg.columns))
print("avg_top.csv:", avg_top.shape, "cols:", list(avg_top.columns))
print("songs.csv year range:", songs['year'].min(), "to", songs['year'].max())
print("songs.csv n unique songs:", songs['song_title'].nunique())
print("songs.csv n distinct (title,year):", songs[['song_title','year']].drop_duplicates().shape[0])
print("2019.csv gender counts:")
print(y2019['gender'].value_counts())
print("2019.csv genre counts:")
print(y2019['genre'].value_counts())
print("2019.csv spoken counts:")
print(y2019['spoken'].value_counts(dropna=False))
print("songs.csv missing per col:")
print(songs.isna().sum())
print("2019.csv missing per col:")
print(y2019.isna().sum())
print("songs.csv register stats:")
print(songs['register'].describe())
print("songs.csv peak_rank min/max:", songs['peak_rank'].min(), songs['peak_rank'].max())
print("songs.csv points stats:")
print(songs['points'].describe())
