# -*- coding: utf-8 -*-
"""
LOCAL-ONLY best-effort official-style headshot fetcher.
Downloads EA FC face renders from the SoFIFA CDN by numeric player id.
Publish-gated: these renders are copyrighted; swap to Wikimedia before any public release.

URL pattern (game version 26 = EA FC 26, 240px transparent PNG head render):
    https://cdn.sofifa.net/players/{first3}/{last3}/26_240.png
where the numeric EA/SoFIFA id is zero-padded to >=6 digits and split first3/last3.
"""
import json
import os
import re
import sys
import time
import urllib.request

# Windows consoles default to GBK and choke on names like "Ødegaard".
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
LICENSE = ("copyrighted - LOCAL BUILD ONLY, publish-gate: swap to Wikimedia "
           "before public release")
SIZE = 240  # render size; sofifa offers 120/180/240


def slug(name):
    s = name.lower()
    s = s.replace("é", "e").replace("è", "e").replace("í", "i")
    s = s.replace("ú", "u").replace("ó", "o").replace("ñ", "n")
    s = s.replace("á", "a").replace("ü", "u").replace("ø", "o")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def sofifa_url(pid, ver=26, size=SIZE):
    p = str(pid).strip()
    if not p.isdigit():
        return None
    p = p.zfill(6)
    return "https://cdn.sofifa.net/players/%s/%s/%d_%d.png" % (p[:-3], p[-3:], ver, size)


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://sofifa.com/"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    ct = r.headers.get("Content-Type", "")
    if r.status != 200 or "image" not in ct or len(data) < 800:
        return False, r.status, ct, len(data)
    with open(dest, "wb") as f:
        f.write(data)
    return True, r.status, ct, len(data)


def main():
    # players.json: [{ "name": ..., "id": "277643"|null }]
    with open(os.path.join(HERE, "_players.json"), "r", encoding="utf-8") as f:
        players = json.load(f)

    manifest = []
    found = 0
    for pl in players:
        name = pl["name"]
        pid = pl.get("id")
        sl = slug(name)
        rec = {"name": name, "file": None, "source_url": None,
               "license": LICENSE, "found": False}
        if not pid or not str(pid).isdigit():
            rec["note"] = "no id resolved; build falls back to existing Wikimedia photo"
            manifest.append(rec)
            print("SKIP  %-22s (no id)" % name)
            continue
        url = sofifa_url(pid)
        fn = sl + ".png"
        dest = os.path.join(HERE, fn)
        try:
            ok, status, ct, n = fetch(url, dest)
        except Exception as e:
            ok, status, ct, n = False, "ERR", str(e), 0
        if ok:
            rec.update(file=fn, source_url=url, found=True)
            found += 1
            print("OK    %-22s id=%-8s %6db  %s" % (name, pid, n, fn))
        else:
            rec["source_url"] = url
            rec["note"] = ("download failed (%s %s); build falls back to existing "
                           "Wikimedia photo" % (status, ct))
            print("FAIL  %-22s id=%-8s [%s %s]" % (name, pid, status, ct))
        manifest.append(rec)
        time.sleep(0.25)

    with open(os.path.join(HERE, "_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("\n%d/%d found. manifest -> _manifest.json" % (found, len(players)))


if __name__ == "__main__":
    main()
