"""Quantitative findings about laughter, topic structure, and callbacks in Ali Wong's Baby Cobra."""

from collections import Counter
from load_and_profile import load_captions, load_topics


def fmt_mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


captions = load_captions()
topics = load_topics()
TOTAL_DURATION = 3535 - 28  # first caption start to last caption stop

# --- ana_01: Total laughter time and share of the hour ---
print("=== ana_01 ===")
total_laugh = sum(c["laugh"] for c in captions)
print(f"Total laughter seconds: {total_laugh}")
print(f"Total set duration (first caption to last): {TOTAL_DURATION} s")
print(f"Laughter share of stage time: {total_laugh / TOTAL_DURATION * 100:.1f}%")
laughs = [c["laugh"] for c in captions if c["laugh"] > 0]
print(f"Laugh-bearing captions: {len(laughs)} of {len(captions)} ({len(laughs)/len(captions)*100:.1f}%)")
print(f"Mean laugh duration when present: {sum(laughs)/len(laughs):.2f} s")
print(f"Median laugh duration when present: {sorted(laughs)[len(laughs)//2]:.2f} s")

# --- ana_02: The single biggest laugh — the laughter climax ---
print("\n=== ana_02 ===")
sorted_caps = sorted(captions, key=lambda c: c["laugh"], reverse=True)
top = sorted_caps[0]
print(f"Largest laugh: {top['laugh']} s")
print(f"Caption: {top['caption']!r}")
print(f"Time: {top['timeStart']} s ({fmt_mmss(top['timeStart'])})")
print(f"Topic group: {top['group']}")
print(f"Position in hour: {top['timeStart']/TOTAL_DURATION*100:.1f}% through")
print("\nTop 10 laugh moments:")
for c in sorted_caps[:10]:
    print(f"  {c['laugh']:.1f}s @ {fmt_mmss(c['timeStart'])} [{c['group']}] {c['caption'][:70]}")

# --- ana_03: Laugh-duration distribution (histogram) ---
print("\n=== ana_03 ===")
buckets = [(0, 0), (0.5, 0.5), (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5),
           (3, 3.5), (4, 4.5), (5, 5.5), (6, 6.5), (7, 7.5), (8, 9.5), (10, 99)]
labels = ["0", "0.5", "1.0", "1.5", "2.0", "2.5", "3-3.5", "4-4.5", "5-5.5", "6-6.5", "7-7.5", "8-9.5", "10+"]
hist = []
for (lo, hi), lbl in zip(buckets, labels):
    n = sum(1 for c in captions if lo <= c["laugh"] <= hi)
    hist.append((lbl, n))
    print(f"  {lbl:8s}  {n:4d}")
print(f"\nMax: {max(c['laugh'] for c in captions)}")
print(f"Captions with laugh >= 5s: {sum(1 for c in captions if c['laugh'] >= 5)}")
print(f"Captions with laugh >= 6s: {sum(1 for c in captions if c['laugh'] >= 6)}")
print(f"Captions with laugh >= 7s: {sum(1 for c in captions if c['laugh'] >= 7)}")
print(f"Captions with laugh >= 8s: {sum(1 for c in captions if c['laugh'] >= 8)}")
print(f"Captions with laugh >= 10s: {sum(1 for c in captions if c['laugh'] >= 10)}")

# --- ana_04: Laughter-by-minute (rolling profile of the hour) ---
print("\n=== ana_04 ===")
minute_laugh = [0.0] * 60
for c in captions:
    m = c["timeStart"] // 60
    if m < 60:
        minute_laugh[m] += c["laugh"]
print("Minute, laugh_seconds")
for m, v in enumerate(minute_laugh):
    print(f"  {m:2d}  {v:.1f}")
peak_min = minute_laugh.index(max(minute_laugh))
print(f"\nPeak minute: {peak_min} ({minute_laugh[peak_min]:.1f} s of laughter)")
print(f"Quietest non-zero minute: {min((v for v in minute_laugh if v > 0))}")

# --- ana_05: Topic-group laughter ranking ---
print("\n=== ana_05 ===")
group_laugh = Counter()
group_seconds_on_stage = {}
for c in captions:
    group_laugh[c["group"]] += c["laugh"]
for g in set(c["group"] for c in captions):
    spans = [(c["timeStart"], c["timeStop"]) for c in captions if c["group"] == g]
    if spans:
        group_seconds_on_stage[g] = max(s[1] for s in spans) - min(s[0] for s in spans)
ranked = sorted(group_laugh.items(), key=lambda x: x[1], reverse=True)
print("Top 15 topic groups by total laugh seconds:")
for g, v in ranked[:15]:
    on_stage = group_seconds_on_stage.get(g, 0)
    rate = v / on_stage if on_stage else 0
    print(f"  {v:5.1f}s  [{on_stage:4d}s on stage, {rate:.2f} laugh/s] {g}")
print(f"\nTotal distinct caption-groups: {len(ranked)}")
zero_groups = [g for g, v in group_laugh.items() if v == 0]
print(f"Groups with zero laughter: {len(zero_groups)}")

# --- ana_06: Topic nesting depth ---
print("\n=== ana_06 ===")
level_counts = Counter(t["level"] for t in topics)
for lvl in sorted(level_counts):
    print(f"  Level {lvl}: {level_counts[lvl]} topics")
print(f"\nMax depth: {max(level_counts)}")
print(f"Top-level topics (level 1): {level_counts[1]}")

# --- ana_07: Laugh size by nesting level ---
print("\n=== ana_07 ===")
# Map each topic group → level, then aggregate caption laughs by level
group_to_level = {t["group"]: t["level"] for t in topics}
level_total = Counter()
level_n_caps = Counter()
level_max = {lvl: 0 for lvl in level_counts}
for c in captions:
    lvl = group_to_level.get(c["group"])
    if lvl is None:
        continue
    level_total[lvl] += c["laugh"]
    level_n_caps[lvl] += 1
    if c["laugh"] > level_max[lvl]:
        level_max[lvl] = c["laugh"]
for lvl in sorted(level_total):
    avg = level_total[lvl] / level_n_caps[lvl] if level_n_caps[lvl] else 0
    print(f"  Level {lvl}: total={level_total[lvl]:.1f}s, captions={level_n_caps[lvl]}, "
          f"avg={avg:.2f}s, max={level_max[lvl]}s")

# --- ana_08: The three explicit callbacks ---
print("\n=== ana_08 ===")
callbacks = [t for t in topics if t["callback_seconds"] is not None]
print(f"Number of explicit callbacks in topics CSV: {len(callbacks)}")
for t in callbacks:
    target_secs = t["callback_seconds"]
    target_topic = None
    for prior in topics:
        if prior["timeStart"] is not None and prior["timeStart"] == target_secs:
            target_topic = prior["group"]
            break
    distance = t["timeStart"] - target_secs
    cb_caption_laughs = [c["laugh"] for c in captions
                         if c["timeStart"] >= t["timeStart"] and c["timeStart"] < t["totalStop"]]
    max_laugh_in_cb = max(cb_caption_laughs) if cb_caption_laughs else 0
    print(f"  Callback at {fmt_mmss(t['timeStart'])} ({t['group']}) → "
          f"target topic at {fmt_mmss(target_secs)} ({target_topic}); "
          f"reach back: {distance}s ({distance//60}m {distance%60}s); "
          f"max laugh during callback: {max_laugh_in_cb}s")

# --- ana_09: Laughter bucket near the climax ---
print("\n=== ana_09 ===")
climax_t = top["timeStart"]
window = 60
in_window = [c for c in captions if abs(c["timeStart"] - climax_t) <= window]
print(f"Window: {window}s either side of climax at {fmt_mmss(climax_t)}")
print(f"Captions in window: {len(in_window)}")
print(f"Total laugh seconds in window: {sum(c['laugh'] for c in in_window):.1f}")
print(f"Captions with laugh >= 4s in window:")
for c in in_window:
    if c["laugh"] >= 4:
        print(f"  {c['laugh']:.1f}s @ {fmt_mmss(c['timeStart'])} [{c['group']}]: {c['caption'][:80]}")

# --- ana_10: Top-level topic durations (the seven big chapters) ---
print("\n=== ana_10 ===")
level1 = [t for t in topics if t["level"] == 1]
print("Top-level topics (level 1):")
for t in level1:
    span = t["topicEnd"] - t["timeStart"] if (t["topicEnd"] and t["timeStart"]) else 0
    chap_laugh = sum(c["laugh"] for c in captions
                     if c["timeStart"] >= t["timeStart"] and c["timeStart"] < (t["topicEnd"] or 99999))
    print(f"  {t['group']:30s} start={fmt_mmss(t['timeStart'])}  "
          f"end={fmt_mmss(t['topicEnd'])}  span={span}s  total_laugh={chap_laugh:.1f}s")

# --- ana_11: Talk-vs-laugh share visualised as a stacked bar ---
print("\n=== ana_11 ===")
print(f"Set duration: {TOTAL_DURATION}s")
print(f"Laughter: {total_laugh}s ({total_laugh/TOTAL_DURATION*100:.1f}%)")
print(f"Talk + silence: {TOTAL_DURATION - total_laugh}s ({(TOTAL_DURATION - total_laugh)/TOTAL_DURATION*100:.1f}%)")
