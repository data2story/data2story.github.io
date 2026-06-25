#!/usr/bin/env python3
"""Download an image URL, resize to target width, recompress to <~400KB JPEG.

Usage:
    py code/dl_resize.py <url> <out_path> [target_width=1920] [max_kb=400] [is_portrait=0]

Prints a small JSON line with final dims + size so the caller can record it.
"""
import sys, json, io, urllib.request, os

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

def fetch(url, retries=6):
    import time, urllib.error
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "https://www.google.com/",
        })
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 503):
                time.sleep(3.0 * (2 ** attempt))  # 3,6,12,24,48,96s
                continue
            raise
    raise last

def main():
    url = sys.argv[1]
    out = sys.argv[2]
    target_w = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
    max_kb = int(sys.argv[4]) if len(sys.argv) > 4 else 400
    raw = fetch(url)
    from PIL import Image
    im = Image.open(io.BytesIO(raw))
    im = im.convert("RGB")
    w, h = im.size
    if w > target_w:
        nh = int(h * target_w / w)
        im = im.resize((target_w, nh), Image.LANCZOS)
    w, h = im.size
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # binary-search JPEG quality to land under max_kb
    q = 88
    data = None
    while q >= 40:
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=q, optimize=True, progressive=True)
        data = buf.getvalue()
        if len(data) <= max_kb * 1024:
            break
        q -= 6
    with open(out, "wb") as f:
        f.write(data)
    print(json.dumps({
        "out": out, "width": w, "height": h,
        "kb": round(len(data)/1024, 1), "quality": q,
        "orig_bytes": len(raw),
    }))

if __name__ == "__main__":
    main()
