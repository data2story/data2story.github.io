"""Cleaner structural views: chapter-level laughter, callbacks with proper target labels, and the climax window."""

from load_and_profile import load_captions, load_topics, hms_to_seconds


def fmt_mmss(s):
    s = int(s)
    return f"{s // 60}:{s % 60:02d}"


captions = load_captions()
topics = load_topics()
TOTAL = 3535 - 28

# --- ana_12: Chapters of the show (level-1 topics, deduplicated, with cumulative laugh) ---
print("=== ana_12 ===")
# The CSV repeats some level-1 rows because of nesting end markers.
# We treat each (group, timeStart, topicEnd) as one chapter unit.
seen = set()
chapters = []
for t in topics:
    if t["level"] != 1:
        continue
    key = (t["group"], t["timeStart"], t["topicEnd"])
    if key in seen:
        continue
    seen.add(key)
    chapters.append(t)
chapters.sort(key=lambda t: t["timeStart"])
print("Distinct level-1 chapters:")
for t in chapters:
    span = t["topicEnd"] - t["timeStart"]
    chap_laugh = sum(c["laugh"] for c in captions
                     if c["timeStart"] >= t["timeStart"] and c["timeStart"] < t["topicEnd"])
    chap_caps = [c for c in captions
                 if c["timeStart"] >= t["timeStart"] and c["timeStart"] < t["topicEnd"]]
    talk_secs = sum(c["timeStop"] - c["timeStart"] for c in chap_caps)
    print(f"  {t['group']:25s}  {fmt_mmss(t['timeStart'])}–{fmt_mmss(t['topicEnd'])}  "
          f"span={span}s  laugh={chap_laugh:.1f}s  ({chap_laugh/span*100:.1f}% of chapter)")

# --- ana_13: Properly resolved callbacks ---
print("\n=== ana_13 ===")
# Find the topic whose timeStart equals the callback's seconds (some are nested children)
print("Callback resolution (nearest topic at-or-before target time):")
all_t_start = sorted(((t["timeStart"], t["group"]) for t in topics if t["timeStart"] is not None),
                     key=lambda x: x[0])
for t in topics:
    if t["callback_seconds"] is None:
        continue
    target = t["callback_seconds"]
    # find the topic whose timeStart is closest at-or-before target
    best = None
    for ts, g in all_t_start:
        if ts <= target:
            best = (ts, g)
        else:
            break
    distance = t["timeStart"] - target
    # find caption text closest to the target time, for human-readable label
    nearby_target_caps = [c for c in captions if abs(c["timeStart"] - target) < 30]
    target_text = nearby_target_caps[0]["caption"] if nearby_target_caps else ""
    nearby_cb_caps = [c for c in captions
                      if c["timeStart"] >= t["timeStart"] and c["timeStart"] < t["totalStop"]]
    cb_text = nearby_cb_caps[0]["caption"] if nearby_cb_caps else ""
    print(f"\n  CALLBACK: '{cb_text[:80]}'")
    print(f"    fired at  {fmt_mmss(t['timeStart'])}  in topic '{t['group']}'")
    print(f"    target at {fmt_mmss(target)}  in topic '{best[1] if best else '?'}'")
    print(f"    target text: '{target_text[:80]}'")
    print(f"    distance: {distance}s ({distance//60}m {distance%60}s)")
    if nearby_cb_caps:
        max_l = max(c["laugh"] for c in nearby_cb_caps)
        print(f"    max laugh in callback topic: {max_l}s")

# --- ana_14: Climax — the full bit, line by line, with laugh sizes ---
print("\n=== ana_14 ===")
# top-rated single laugh is at 708s (11:48), group 166-hooking up.
# Show the full topic and surrounding context.
climax_caps = [c for c in captions if 670 <= c["timeStart"] <= 760]
print(f"Climax window 11:10–12:40 ({len(climax_caps)} captions):")
for c in climax_caps:
    marker = "*" if c["laugh"] >= 4 else " "
    print(f"  {marker} {fmt_mmss(c['timeStart'])}  laugh={c['laugh']:>4.1f}s  [{c['group']}]  {c['caption'].strip()}")

# --- ana_15: How many times specific motifs (mom, husband, etc.) appear in captions ---
print("\n=== ana_15 ===")
motifs = {
    "husband": ["husband"],
    "mom / mother": ["mom", "mother"],
    "money / dollars": ["money", "dollar", "$"],
    "Asian / asian / korean / Japanese": ["asian", "korean", "japanese", "vietnam"],
    "white guy / colonize": ["white guy", "white man", "colonize", "white men", "white people"],
    "hpv": ["hpv"],
    "feminism / feminist": ["feminism", "feminist", "lean in"],
    "trap": ["trap"],
}
for label, keys in motifs.items():
    n = 0
    for c in captions:
        text = c["caption"].lower()
        if any(k in text for k in keys):
            n += 1
    print(f"  {label:40s}  mentioned in {n} captions")

# --- ana_16: Long laughs (>= 5s) by chapter ---
print("\n=== ana_16 ===")
big_laughs = sorted([c for c in captions if c["laugh"] >= 5], key=lambda c: c["timeStart"])
print(f"Number of laughs >= 5s: {len(big_laughs)}")
for c in big_laughs:
    print(f"  {c['laugh']:.1f}s @ {fmt_mmss(c['timeStart'])} [{c['group']}]: {c['caption'].strip()[:80]}")
