#!/usr/bin/env python3
"""Print license/author/url metadata for one or more Commons files + the
Special:FilePath direct URL at a chosen width.

Usage:
    py code/commons_meta.py <width> "File Name.jpg" ["Another.jpg" ...]
"""
import sys, json, re, urllib.parse, urllib.request

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UA = "Data2Story-WikimediaFetch/1.0 (academic research; contact: qinghong.lin@eng.ox.ac.uk)"

def get_json(params):
    params = dict(params, format="json")
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def main():
    width = sys.argv[1]
    files = sys.argv[2:]
    titles = ["File:" + f for f in files]
    data = get_json({
        "action": "query", "titles": "|".join(titles),
        "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
        "iiurlwidth": width,
    })
    out = []
    for page in data.get("query", {}).get("pages", {}).values():
        title = page.get("title", "")
        fn = title[len("File:"):] if title.startswith("File:") else title
        missing = "missing" in page
        ii = (page.get("imageinfo") or [{}])[0]
        ext = ii.get("extmetadata", {}) or {}
        def g(k):
            v = ext.get(k, {})
            val = v.get("value", "") if isinstance(v, dict) else ""
            return re.sub(r"<[^>]+>", "", val).strip()
        filepath = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
                    + urllib.parse.quote(fn.replace(" ", "_")) + "?width=" + width)
        out.append({
            "file": fn,
            "missing": missing,
            "thumburl": ii.get("thumburl", ""),
            "filepath_url": filepath,
            "descriptionurl": ii.get("descriptionurl", ""),
            "mime": ii.get("mime", ""),
            "width": ii.get("width"), "height": ii.get("height"),
            "license_short": g("LicenseShortName"),
            "license": g("License"),
            "artist": g("Artist"),
            "credit": g("Credit"),
            "usage_terms": g("UsageTerms"),
        })
    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
