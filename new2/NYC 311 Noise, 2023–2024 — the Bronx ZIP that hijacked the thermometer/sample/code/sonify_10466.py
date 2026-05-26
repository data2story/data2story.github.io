"""sonify_10466.py — sonify ZIP 10466's daily complaint volume over 2024.

Maps each of the 366 days of 2024 to a percussive tone (50 ms FM bell)
whose amplitude scales linearly with that day's complaint count. The
result is a ~3-second loop that *audibly* shows the eight massive
mobile-app bursts described in ana_25 — most days are nearly silent,
the burst days slam.

Output: PROJECT_DIR/assets/sonify_10466.wav (16-bit mono, 44.1 kHz)
"""
from pathlib import Path
import numpy as np
import wave
import pandas as pd

CODE_DIR = Path(__file__).parent
PROJECT_DIR = CODE_DIR.parent
OUT_WAV = PROJECT_DIR / "assets" / "sonify_10466.wav"

SR = 22050  # half-rate, perfectly fine for percussion + smaller WAV
DAY_SECONDS = 0.045
N_PER_DAY = int(SR * DAY_SECONDS)
F_BASE = 220.0  # A3
F_TOP = 1760.0  # A6
NORM_CEIL = 5000.0  # 4,952 was the historical max — clip there

# 1. Load + filter 10466's 2024 daily counts
df = pd.read_parquet(CODE_DIR / "cache.parquet")
df["created_date"] = pd.to_datetime(df["created_date"])
z = df[(df["incident_zip"] == "10466") & (df["created_date"].dt.year == 2024)]
daily = z.groupby(z["created_date"].dt.normalize()).size()
all_2024 = pd.date_range("2024-01-01", "2024-12-31", freq="D")
daily = daily.reindex(all_2024, fill_value=0).astype(int)
print(f"sonifying {len(daily)} days; max day = {daily.max()}, median = {int(daily.median())}")

# 2. Synthesise each day as a short FM bell, amplitude scaled by complaints
t = np.arange(N_PER_DAY) / SR
envelope = np.exp(-t * 30.0)  # quick decay

wav = np.zeros(N_PER_DAY * len(daily), dtype=np.float32)
for i, c in enumerate(daily.values):
    if c == 0:
        continue  # silence
    # map count → pitch (log scale)
    rel = min(c / NORM_CEIL, 1.0)
    pitch = F_BASE * (F_TOP / F_BASE) ** rel
    # amplitude: square-root scale so a big burst dominates without clipping
    amp = 0.92 * np.sqrt(rel)
    # FM bell: carrier + modulator
    mod = 3.0 * pitch * np.sin(2 * np.pi * pitch * t)
    sig = amp * envelope * np.sin(2 * np.pi * pitch * t + mod * 0.005)
    wav[i * N_PER_DAY : (i + 1) * N_PER_DAY] = sig

# 3. Write 16-bit WAV
wav_int16 = np.clip(wav, -1.0, 1.0)
wav_int16 = (wav_int16 * 32767).astype(np.int16)

with wave.open(str(OUT_WAV), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes(wav_int16.tobytes())
print(f"wrote {OUT_WAV} ({OUT_WAV.stat().st_size/1e3:.1f} KB, {len(wav)/SR:.2f} seconds)")
