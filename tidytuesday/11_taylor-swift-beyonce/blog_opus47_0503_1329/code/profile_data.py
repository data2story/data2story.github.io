"""Profile all four CSVs: shape, columns, sample values, missing rates."""
import pandas as pd
from pathlib import Path

DATA = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/11_taylor-swift-beyonce")

bey = pd.read_csv(DATA / "beyonce_lyrics.csv")
ts = pd.read_csv(DATA / "taylor_swift_lyrics.csv")
sales = pd.read_csv(DATA / "sales.csv")
charts = pd.read_csv(DATA / "charts.csv")

# strip column whitespace from Taylor's table
ts.columns = [c.strip() for c in ts.columns]
ts["Artist"] = ts["Artist"].str.strip()
ts["Album"] = ts["Album"].str.strip()
ts["Title"] = ts["Title"].str.strip()

# --- ana_01: Dataset shape summary ---
print("=== ana_01 ===")
for name, df in [("beyonce_lyrics", bey), ("taylor_swift_lyrics", ts), ("sales", sales), ("charts", charts)]:
    print(f"{name}: rows={len(df)}, cols={len(df.columns)}, columns={list(df.columns)}")
print()
print(f"Beyonce unique songs: {bey['song_id'].nunique()}")
print(f"Beyonce avg lines per song: {bey.groupby('song_id').size().mean():.1f}")
print(f"Taylor songs: {len(ts)}")
print(f"Taylor unique albums: {ts['Album'].nunique()}")
print(f"Beyonce shows in beyonce_lyrics? {(bey['artist_name']=='Beyoncé').sum()} of {len(bey)} rows")
print(f"Distinct artists in beyonce_lyrics: {bey['artist_name'].value_counts().head(10).to_dict()}")
