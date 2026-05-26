"""Generate a sonification WAV: each month from 2020-01 to 2026-05 becomes one short note.
Pitch is mapped logarithmically from the month's verification count.

Output: assets/timeline_sonification.wav (~12 sec).

Mapping:
- 77 months of data (2020-01 to 2026-05)
- Each note: ~155ms (sine wave + soft envelope to avoid clicks)
- Pitch scale: log10(count) → MIDI note in C major pentatonic between C3 (~131 Hz) and C6 (~1047 Hz)
- The peak (3,151) is the highest tone; the minimum (155) is one of the lowest
"""

import math
import struct
import wave
from pathlib import Path

OUT = Path(r"D:\AI\journalist agent review\phase2\project\speedrun_top100\blog_opus47_0525_2242\assets\timeline_sonification.wav")

# (year, month, count) for 2020-01 .. 2026-05 — copied verbatim from ana_25 / ana_30
SERIES = [
    (2020,1,155),(2020,2,158),(2020,3,243),(2020,4,275),(2020,5,317),(2020,6,342),
    (2020,7,505),(2020,8,401),(2020,9,378),(2020,10,401),(2020,11,489),(2020,12,536),
    (2021,1,585),(2021,2,661),(2021,3,731),(2021,4,655),(2021,5,826),(2021,6,830),
    (2021,7,666),(2021,8,547),(2021,9,544),(2021,10,538),(2021,11,543),(2021,12,512),
    (2022,1,886),(2022,2,414),(2022,3,425),(2022,4,502),(2022,5,1604),(2022,6,769),
    (2022,7,848),(2022,8,484),(2022,9,412),(2022,10,447),(2022,11,343),(2022,12,415),
    (2023,1,541),(2023,2,477),(2023,3,551),(2023,4,472),(2023,5,400),(2023,6,651),
    (2023,7,772),(2023,8,769),(2023,9,418),(2023,10,326),(2023,11,345),(2023,12,520),
    (2024,1,581),(2024,2,491),(2024,3,457),(2024,4,523),(2024,5,595),(2024,6,692),
    (2024,7,1055),(2024,8,777),(2024,9,539),(2024,10,501),(2024,11,487),(2024,12,600),
    (2025,1,645),(2025,2,979),(2025,3,1003),(2025,4,734),(2025,5,651),(2025,6,780),
    (2025,7,1020),(2025,8,1088),(2025,9,912),(2025,10,1526),(2025,11,1537),(2025,12,1336),
    (2026,1,1811),(2026,2,1997),(2026,3,3151),(2026,4,2234),(2026,5,1917),
]

# C major pentatonic across 3 octaves: C3 .. C6
# scale degrees in semitones from C: 0, 2, 4, 7, 9
PENTATONIC_OFFSETS = [0, 2, 4, 7, 9]
def midi_to_hz(m): return 440.0 * 2 ** ((m - 69) / 12)
SCALE_HZ = []
for octave in (3, 4, 5):  # C3=48, C4=60, C5=72
    base_midi = 12 * (octave + 1)
    for off in PENTATONIC_OFFSETS:
        SCALE_HZ.append(midi_to_hz(base_midi + off))
SCALE_HZ.append(midi_to_hz(72))  # C6 to cap
SCALE_HZ = sorted(SCALE_HZ)
print(f"scale of {len(SCALE_HZ)} pitches from {SCALE_HZ[0]:.0f}Hz to {SCALE_HZ[-1]:.0f}Hz")

# Logarithmic pitch mapping
counts = [c for _, _, c in SERIES]
log_min = math.log10(min(counts))
log_max = math.log10(max(counts))
def pitch_for(c):
    x = (math.log10(c) - log_min) / (log_max - log_min)  # 0..1
    idx = round(x * (len(SCALE_HZ) - 1))
    return SCALE_HZ[idx]

# Audio params
SR = 44100
NOTE_DUR = 0.16  # seconds per note
ATTACK = 0.01
RELEASE = 0.05

def note_samples(freq, dur, vel=0.6):
    n = int(SR * dur)
    out = []
    for i in range(n):
        t = i / SR
        # envelope
        if t < ATTACK:
            env = t / ATTACK
        elif t > dur - RELEASE:
            env = max(0, (dur - t) / RELEASE)
        else:
            env = 1.0
        # gentle additive harmonics to sound less like a sine
        s = math.sin(2*math.pi*freq*t) + 0.3 * math.sin(2*math.pi*freq*2*t) + 0.1 * math.sin(2*math.pi*freq*3*t)
        s /= 1.4
        out.append(int(vel * env * s * 32767))
    return out

samples = []
for y, m, c in SERIES:
    freq = pitch_for(c)
    samples.extend(note_samples(freq, NOTE_DUR))

# Add a tail of silence
samples.extend([0] * int(SR * 0.2))

print(f"total samples: {len(samples)}, duration: {len(samples)/SR:.2f}s, notes: {len(SERIES)}")

with wave.open(str(OUT), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b"".join(struct.pack("<h", s) for s in samples))

print(f"wrote {OUT}")
print(f"   size: {OUT.stat().st_size} bytes")
