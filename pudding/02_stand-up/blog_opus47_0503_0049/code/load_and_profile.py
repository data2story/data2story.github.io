"""Load Ali Wong Baby Cobra dataset (captions + topics) and report the basic profile."""

import csv
from pathlib import Path

DATA = Path("/Users/forrest/Desktop/data2blog/data_preprint/pudding/02_stand-up")


def load_captions():
    rows = []
    with open(DATA / "ali-wong--captions.csv") as f:
        for r in csv.DictReader(f):
            r["laugh"] = float(r["laugh"]) if r["laugh"] else 0.0
            r["timeStart"] = int(r["timeStart"])
            r["timeStop"] = int(r["timeStop"])
            rows.append(r)
    return rows


def hms_to_seconds(s):
    """Convert 'h:mm:ss' or 'm:ss' string to seconds, or None if blank."""
    if not s:
        return None
    parts = [int(p) for p in s.split(":")]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return int(s)


def load_topics():
    rows = []
    with open(DATA / "ali-wong--topics.csv") as f:
        for r in csv.DictReader(f):
            r["level"] = int(r["level"]) if r["level"] else None
            r["timeStart"] = int(r["timeStart"]) if r["timeStart"] else None
            r["totalStop"] = int(r["totalStop"]) if r["totalStop"] else None
            r["index"] = int(r["index"]) if r["index"] else None
            r["topicEnd"] = int(r["topicEnd"]) if r["topicEnd"] else None
            # callback is a HH:MM:SS timestamp pointing at the start of a callback target
            r["callback_seconds"] = hms_to_seconds(r["callback"]) if r["callback"] else None
            # end is an integer (level number that closes) or blank
            r["end"] = int(r["end"]) if r["end"] else None
            rows.append(r)
    return rows


if __name__ == "__main__":
    captions = load_captions()
    topics = load_topics()

    # --- ana_00: Basic dataset profile ---
    print("=== ana_00 ===")
    last_caption_stop = max(c["timeStop"] for c in captions)
    print(f"Caption rows: {len(captions)}")
    print(f"Topic rows: {len(topics)}")
    print(f"First caption start: {min(c['timeStart'] for c in captions)} s")
    print(f"Last caption stop: {last_caption_stop} s ({last_caption_stop // 60} min {last_caption_stop % 60} s)")
    n_groups = len(set(c["group"] for c in captions))
    print(f"Distinct topic groups in captions: {n_groups}")
    n_groups_topics = len(topics)
    print(f"Distinct topic rows in topics CSV: {n_groups_topics}")
