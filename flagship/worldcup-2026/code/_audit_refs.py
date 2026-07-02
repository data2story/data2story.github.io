#!/usr/bin/env python3
# Verification: every local asset/code reference in index.html must resolve to a
# file on disk; confirm teaser orphans are unreferenced and the ratings
# placeholder is gone. Read-only audit.
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # this blog root
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()

refs = set()
refs |= set(re.findall(r'(?:src|href|poster)\s*=\s*["\']([^"\']+)["\']', html))
refs |= set(re.findall(r'url\(\s*["\']?([^)"\']+)["\']?\s*\)', html))
refs |= set(re.findall(r'["\']((?:assets|code)/[^"\']+)["\']', html))  # JS string paths

local = sorted({r.split('?')[0].split('#')[0] for r in refs
                if r.startswith(('assets/', 'code/'))})
missing = [r for r in local if not os.path.exists(os.path.join(BASE, r))]

print(f"local asset/code refs: {len(local)}  | missing: {len(missing)}")
for m in missing:
    print("   MISSING ->", m)

# external CDNs still present?
for lib in ("vega@5", "vega-lite@5", "d3@7", "leaflet@1.9"):
    print(f"CDN {lib:14}: {'yes' if lib in html else 'NO'}")

print("teaser_* references in HTML:", len(re.findall(r'teaser_(?:motion|hero)', html)),
      "(0 => safe to delete the orphan files)")
print("ratings placeholder still empty:", "player-ratings cards injected in a later pass" in html)
print("ratings module heading present:", "scored from scratch" in html.lower() or "ratings-module" in html)

# count the showcase modules + key new ids
for marker in ('edt_predictor', 'id="ratings-module"', 'edt_oddsmkt', 'hero_stadium',
               '0808 8020 133', '1-800-GAMBLER', 'StatsBomb'):
    print(f"  marker {marker:22}: {'present' if marker in html else 'MISSING'}")
