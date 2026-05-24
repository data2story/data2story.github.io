"""Lyric-level analysis: line counts, word counts, repetition, top words."""
import pandas as pd
import re
from pathlib import Path
from collections import Counter

DATA = Path("/Users/forrest/Desktop/data2blog/data_preprint/tidytuesday/11_taylor-swift-beyonce")

bey = pd.read_csv(DATA / "beyonce_lyrics.csv")
ts = pd.read_csv(DATA / "taylor_swift_lyrics.csv")
ts.columns = [c.strip() for c in ts.columns]
for c in ["Artist", "Album", "Title"]:
    ts[c] = ts[c].str.strip()

STOP = {
    "the","a","an","and","or","but","if","then","of","to","for","in","on","at","by","with","as",
    "is","are","was","were","be","been","being","do","does","did","done","have","has","had",
    "i","you","he","she","it","we","they","me","him","her","us","them","my","your","his","its",
    "our","their","this","that","these","those","what","when","where","why","how","who","whom",
    "all","some","no","not","just","so","up","down","out","off","over","under","again","further",
    "now","ll","ve","re","s","t","d","m","ya","oh","ooh","yeah","na","la","mm","ay","gon","ain",
    "got","get","go","let","know","like","cause","cuz","til","gonna","wanna","yeh","hey","ah"
}

WORD = re.compile(r"[a-zA-Z']+")

def tokens(text):
    if not isinstance(text, str): return []
    text = text.lower().replace("’","'").replace("‘","'")
    return [w for w in WORD.findall(text) if w not in STOP and len(w) > 1]

# --- ana_02: Per-album line and word counts (Taylor) ---
print("=== ana_02 ===")
ts_per_album = []
for album in ts["Album"].unique():
    sub = ts[ts["Album"] == album]
    lines = 0
    words = 0
    for lyr in sub["Lyrics"].fillna(""):
        l = [x for x in lyr.splitlines() if x.strip()]
        lines += len(l)
        words += sum(len(re.findall(r"[A-Za-z']+", x)) for x in l)
    ts_per_album.append({
        "artist": "Taylor Swift",
        "album": album,
        "songs": len(sub),
        "lines": lines,
        "words": words,
        "lines_per_song": round(lines / max(len(sub), 1), 1),
    })
ts_album_df = pd.DataFrame(ts_per_album)
print(ts_album_df.to_string(index=False))
print(f"Taylor total lines: {ts_album_df['lines'].sum()}, total words: {ts_album_df['words'].sum()}")

# --- ana_03: Beyonce per-song stats (no album in dataset) ---
print()
print("=== ana_03 ===")
bey_per_song = bey.groupby("song_name").agg(lines=("song_line","count")).reset_index()
print(f"Beyonce: {len(bey_per_song)} songs, total lines = {bey_per_song['lines'].sum()}")
print(f"Beyonce mean lines/song: {bey_per_song['lines'].mean():.1f}")
print(f"Beyonce median lines/song: {bey_per_song['lines'].median()}")
print("Top 10 longest Beyonce songs (by line count):")
print(bey_per_song.nlargest(10, "lines").to_string(index=False))

# --- ana_04: Most repeated lines (signature hooks) ---
print()
print("=== ana_04 ===")
line_counts = bey.groupby(["song_name","line"]).size().reset_index(name="repeats")
top_repeats_b = line_counts.nlargest(15, "repeats")
print("Beyonce — top 15 most-repeated lines within a single song:")
print(top_repeats_b.to_string(index=False))

# Taylor: split each Lyrics blob into lines, count within song
ts_repeat_rows = []
for _, row in ts.iterrows():
    if not isinstance(row["Lyrics"], str): continue
    lines = [l.strip() for l in row["Lyrics"].splitlines() if l.strip()]
    cnt = Counter(lines)
    for line, n in cnt.most_common(3):
        if n >= 4:
            ts_repeat_rows.append({"album": row["Album"], "title": row["Title"], "line": line, "repeats": n})
ts_repeat_df = pd.DataFrame(ts_repeat_rows).sort_values("repeats", ascending=False).head(15)
print()
print("Taylor — top 15 most-repeated lines within a single song:")
print(ts_repeat_df.to_string(index=False))

# --- ana_05: Top non-stopword words for each artist ---
print()
print("=== ana_05 ===")
bey_tokens = []
for line in bey["line"].fillna(""):
    bey_tokens.extend(tokens(line))
bey_top = Counter(bey_tokens).most_common(30)
print("Beyonce top 30 words:")
for w,c in bey_top:
    print(f"  {w}: {c}")

ts_tokens = []
for lyr in ts["Lyrics"].fillna(""):
    ts_tokens.extend(tokens(lyr))
ts_top = Counter(ts_tokens).most_common(30)
print("Taylor top 30 words:")
for w,c in ts_top:
    print(f"  {w}: {c}")

# --- ana_06: Love-words ratio comparison ---
print()
print("=== ana_06 ===")
LOVE_WORDS = {"love","loved","loving","loves","heart","hearts","baby","babe","kiss","kissed","kisses"}
b_total = len(bey_tokens)
t_total = len(ts_tokens)
b_love = sum(1 for w in bey_tokens if w in LOVE_WORDS)
t_love = sum(1 for w in ts_tokens if w in LOVE_WORDS)
print(f"Beyonce love-words: {b_love}/{b_total} = {b_love/b_total*100:.2f}%")
print(f"Taylor love-words: {t_love}/{t_total} = {t_love/t_total*100:.2f}%")
print(f"Ratio Taylor/Beyonce: {(t_love/t_total)/(b_love/b_total):.2f}x")
