#!/usr/bin/env python3
"""Relocate heavy UNREFERENCED media masters out of assets/ into provenance/ at finalize.

A run's assets/ accumulates heavy ORIGINAL masters that the shipped page never loads:
the full-res source still a hero clip was animated from, the lossless BGM the page plays
as a _web.mp3, the original JPGs every figure now references as _web.webp, etc. They do
not affect render or mobile load, but they bloat the published folder (~25 MB on disk vs
~5 MB shipped) and they trip validate.py Section 16 once relocate has run.

This script MOVES (shutil.move — auditable + reversible, never copy-then-delete-into-the-
void) each heavy unreferenced asset from PROJECT_DIR/assets/ into PROJECT_DIR/provenance/,
writes provenance/_relocated.json (the manifest of what moved + why), and — as a safety
net — repoints any role-JSON pointer that still named a moved original to its new
provenance/ path (most live pointers already point at the _web copies, so this rarely
fires). It NEVER deletes the masters; they remain under provenance/ for audit.

Determinism + no-crash (matches the skill house style of the other inspector scripts):
no LLM, no network, sorted iteration, missing/invalid JSON skipped silently, a tool/IO
failure prints a warning and is skipped (never an exception). Idempotent: a second run
with nothing left to move still (re)writes _relocated.json and exits 0.

The set of files moved is the SAME set validate.py Section 16 flags as a heavy orphan:
  - a media file ANYWHERE under assets/ (recursively, incl. subdirs like assets/clips/)
    whose reference path is absent from index.html (a top-level file is tested by basename
    as before; a SUBDIR file by its relative path assets/<sub>/<file> — a basename-only
    test is a false-positive trap, e.g. player_pedri.jpg != clips/pedri.jpg)
  - AND not a live pointer in scout.json / designer.json / hero.json (shipped-asset fields)
  - AND whose owning item does not carry keep_in_assets:true
  - AND HEAVY: size >= 256 KB OR an original superseded by a referenced *_web.* copy.
When audit/render_report.json carries performance.unreferencedAssets we PREFER that list
(the real browser already computed it), intersected with the same guards; otherwise we
recompute by listing assets/ recursively + the reference-in-index.html test. Masters are
flattened into the flat provenance/ audit folder by basename.

Usage:
    python relocate_unreferenced.py PROJECT_DIR
"""

import argparse
import json
import os
import re
import shutil
import sys


# Windows/GBK consoles cannot encode non-ASCII diagnostics; force UTF-8 stdout.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


HEAVY_BYTES = 262144  # 256 KB — mirror of validate.py Section 16 _HEAVY16

MEDIA_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tif', '.tiff', '.gif',
             '.mp4', '.mov', '.webm', '.mkv', '.avi', '.m4v',
             '.mp3', '.m4a', '.wav', '.ogg', '.oga', '.opus', '.flac', '.aac', '.aiff')


def _load_json(path):
    """Best-effort JSON load; returns {} on absence/parse error (never raises)."""
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _read_text(path):
    if not os.path.isfile(path):
        return ''
    try:
        with open(path, encoding='utf-8') as fh:
            return fh.read()
    except OSError:
        return ''


# --- live-pointer + keep guards (mirror validate.py Section 16) ----------------

def _gather_guards(proj):
    """Return (live_basenames, keep_basenames): basenames the page legitimately
    depends on (shipped-asset fields of scout/designer/hero.json) or that an owning
    item explicitly pins via keep_in_assets. Hero source masters (render_master/
    input_still) are intentionally NOT live pointers — they are exactly what we move."""
    live = set()
    keep = set()

    def reg(v):
        if isinstance(v, str) and v.strip():
            live.add(os.path.basename(v.strip()))

    scout = _load_json(os.path.join(proj, 'scout.json'))
    for it in (scout.get('items', {}) or {}).values():
        if not isinstance(it, dict):
            continue
        for k in ('filename', 'cover_path', 'poster', 'media_ref'):
            reg(it.get(k))
        if it.get('keep_in_assets') is True and isinstance(it.get('filename'), str):
            keep.add(os.path.basename(it['filename']))

    designer = _load_json(os.path.join(proj, 'designer.json'))
    for it in (designer.get('items', {}) or {}).values():
        if not isinstance(it, dict):
            continue
        c = it.get('content', {}) or {}
        for k in ('filename', 'source_image', 'poster', 'cover_image', 'media_ref',
                  'render_master', 'input_still'):
            reg(c.get(k))
        reg(it.get('media_ref'))
        if it.get('keep_in_assets') is True or c.get('keep_in_assets') is True:
            for k in ('filename', 'source_image', 'poster', 'cover_image'):
                v = c.get(k)
                if isinstance(v, str) and v.strip():
                    keep.add(os.path.basename(v.strip()))

    hero = _load_json(os.path.join(proj, 'hero.json'))
    hero_obj = hero.get('hero', hero) if isinstance(hero, dict) else {}
    if isinstance(hero_obj, dict):
        ha = hero_obj.get('assets', {}) or {}
        for k in ('video_webm', 'video_mp4', 'poster'):
            reg(ha.get(k))
        reg(hero_obj.get('reduced_motion_fallback'))
        if hero_obj.get('keep_in_assets') is True:
            for v in (ha or {}).values():
                if isinstance(v, str) and v.strip():
                    keep.add(os.path.basename(v.strip()))

    return live, keep


def _list_assets(assets):
    """Every media file UNDER assets/ as a relative POSIX path (recursive, so files in
    subdirs like assets/clips/ are covered too). A top-level file's relpath is just its
    basename ('foo.png'); a subdir file's is 'sub/foo.png'. Returns a sorted set of
    relpaths. (os.walk recurse — the non-recursive os.listdir version missed subdir
    orphans, which then had to be relocated by hand.)"""
    out = set()
    for root, _dirs, files in os.walk(assets):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), assets).replace(os.sep, '/')
            out.add(rel)
    return out


def _ref_forms(rel):
    """The strings index.html would use to reference assets/<rel>, against which we test
    membership in the page text. For a top-level file ('foo.png') we keep the historical
    BASENAME test (the page usually writes `assets/foo.png`, but a bare `foo.png` was the
    legacy match — preserved exactly). For a SUBDIR file ('clips/pedri.jpg') we test the
    RELATIVE PATH 'assets/clips/pedri.jpg' (and 'clips/pedri.jpg'); a basename-only test
    is a false-positive trap — `player_pedri.jpg` elsewhere on the page would wrongly
    'reference' clips/pedri.jpg and the orphan would never be swept."""
    if '/' not in rel:
        return (rel,)
    return ('assets/' + rel, rel)


def _heavy_orphans(proj):
    """The list of (relpath, basename, bytes, reason) heavy unreferenced assets to relocate.

    Prefers audit/render_report.json performance.unreferencedAssets (the browser already
    computed the unreferenced set), intersected with the live/keep guards + the HEAVY
    filter; else recomputes by listing assets/ (RECURSIVELY, incl. subdirs) + the
    reference-in-index.html test (relative path for subdir files; see _ref_forms)."""
    assets = os.path.join(proj, 'assets')
    if not os.path.isdir(assets):
        return []
    html = _read_text(os.path.join(proj, 'index.html'))
    live, keep = _gather_guards(proj)

    present = _list_assets(assets)          # relpaths (recursive)
    if not present:
        return []
    present_bn = {os.path.basename(p) for p in present}

    def has_web_sibling(rel):
        # The _web sibling test is keyed on basename within assets/ (a master and its
        # _web copy sit together); reference test uses the page text + live pointers.
        bn = os.path.basename(rel)
        stem, _ = os.path.splitext(bn)
        if stem.endswith('_web'):
            return False
        for cand in present_bn:
            cstem, _ = os.path.splitext(cand)
            if cstem == stem + '_web' and (cand in html or cand in live):
                return True
        return False

    # candidate relpaths: prefer the render_report unreferenced list, else all media.
    # render_report entries may carry a bare basename or an assets/<rel> path; match each
    # to a present relpath (by exact relpath, by assets/-stripped relpath, or by basename).
    candidates = []
    rr = _load_json(os.path.join(proj, 'audit', 'render_report.json'))
    ua = (rr.get('performance', {}) or {}).get('unreferencedAssets') if isinstance(rr, dict) else None
    if isinstance(ua, list) and ua:
        by_bn = {}
        for p in present:
            by_bn.setdefault(os.path.basename(p), p)
        for e in ua:
            if not (isinstance(e, dict) and e.get('file')):
                continue
            f = str(e['file']).replace(os.sep, '/').lstrip('/')
            cand = None
            if f in present:
                cand = f
            elif f.startswith('assets/') and f[len('assets/'):] in present:
                cand = f[len('assets/'):]
            elif os.path.basename(f) in by_bn:
                cand = by_bn[os.path.basename(f)]
            if cand:
                candidates.append(cand)
        candidates = sorted(set(candidates))
    if not candidates:
        candidates = sorted(present)

    out = []
    for rel in candidates:
        bn = os.path.basename(rel)
        ext = os.path.splitext(bn)[1].lower()
        if ext not in MEDIA_EXT:
            continue
        if any(form in html for form in _ref_forms(rel)):   # referenced on the page
            continue
        if bn in live or bn in keep:   # live pointer / pinned (guards are basename-keyed)
            continue
        try:
            sz = os.path.getsize(os.path.join(assets, rel))
        except OSError:
            sz = 0
        superseded = has_web_sibling(rel)
        if sz < HEAVY_BYTES and not superseded:
            continue
        reason = 'superseded_by_web_copy' if superseded else 'heavy_unreferenced'
        if superseded and sz >= HEAVY_BYTES:
            reason = 'heavy_and_superseded'
        out.append((rel, bn, sz, reason))
    return out


# --- dangling-pointer repointing (reuse of optimize_assets _rewrite logic) -----
# We extend the optimize_assets.py _rewrite_filename_in_json helper: that one rewrites
# item-level / content-level `filename`; here we also repoint hero.json's nested
# source.render_master / source.input_still + the content media fields, since a moved
# original would otherwise leave those pointing at a now-empty assets/ path.

def _rewrite_one(holder, key, old_base, new_path):
    """If holder[key] basename == old_base, set it to new_path. Returns True if changed."""
    fn = holder.get(key)
    if not isinstance(fn, str) or not fn or os.path.basename(fn) != old_base:
        return False
    holder[key] = new_path
    return True


def _repoint_in_json(json_path, moved):
    """Repoint any role-JSON pointer that still names a moved original to its new
    provenance/<basename> path. `moved` is {old_basename: new_relpath}. Best-effort:
    absent/invalid JSON or write failure is skipped. Returns the count of fields rewritten.

    Handles: top-level items[*].filename, items[*].content.{filename,source_image,poster,
    cover_image,render_master,input_still}, AND hero.json's nested hero.source.{render_master,
    input_still} + hero.assets.{...} + hero.reduced_motion_fallback."""
    if not os.path.isfile(json_path) or not moved:
        return 0
    try:
        with open(json_path, encoding='utf-8') as fh:
            doc = json.load(fh)
    except (OSError, ValueError):
        return 0
    n = 0

    def try_keys(holder, keys):
        c = 0
        if not isinstance(holder, dict):
            return c
        for k in keys:
            v = holder.get(k)
            if isinstance(v, str) and v:
                ob = os.path.basename(v)
                if ob in moved and _rewrite_one(holder, k, ob, moved[ob]):
                    c += 1
        return c

    CONTENT_KEYS = ('filename', 'source_image', 'poster', 'cover_image',
                    'render_master', 'input_still', 'media_ref')
    ITEM_KEYS = ('filename', 'cover_path', 'poster', 'media_ref')

    # {"items": {id: {...}}} docs (scout.json / designer.json)
    items = doc.get('items')
    if isinstance(items, dict):
        for item in items.values():
            if not isinstance(item, dict):
                continue
            n += try_keys(item, ITEM_KEYS)
            n += try_keys(item.get('content'), CONTENT_KEYS)

    # hero.json (nested under hero.hero)
    hero_obj = doc.get('hero') if isinstance(doc.get('hero'), dict) else None
    if isinstance(hero_obj, dict):
        n += try_keys(hero_obj, ('reduced_motion_fallback',))
        n += try_keys(hero_obj.get('source'), ('render_master', 'input_still'))
        n += try_keys(hero_obj.get('assets'), ('video_webm', 'video_mp4', 'poster'))

    if n:
        try:
            with open(json_path, 'w', encoding='utf-8') as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=2)
                fh.write('\n')
        except OSError:
            return 0
    return n


# --- main ----------------------------------------------------------------------

def main(project_dir=None):
    """Relocate heavy unreferenced masters. Callable as a function (Stage 7 wiring) or
    via the CLI. Returns the path to provenance/_relocated.json. Always exits/returns 0
    on a normal run (including the idempotent nothing-to-move case)."""
    if project_dir is None:
        ap = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
        ap.add_argument('project_dir', help='the run folder (contains assets/ + index.html)')
        args = ap.parse_args()
        project_dir = args.project_dir
    proj = str(project_dir).rstrip('/\\')

    assets = os.path.join(proj, 'assets')
    prov = os.path.join(proj, 'provenance')
    sentinel = os.path.join(prov, '_relocated.json')

    orphans = _heavy_orphans(proj)

    os.makedirs(prov, exist_ok=True)

    moved = {}        # old_basename -> "provenance/<basename>"  (new relpath, POSIX-style)
    manifest_items = []
    # `rel` is the path RELATIVE to assets/ (basename for a top-level file, 'sub/file' for
    # a subdir file); `fn` is its basename. Masters are flattened into the flat provenance/
    # audit folder by basename (and _repoint_in_json keys repointing on that basename). The
    # manifest 'from' records the true assets/<rel> source.
    for rel, fn, sz, reason in orphans:
        src = os.path.join(assets, rel)
        dst = os.path.join(prov, fn)
        src_from = 'assets/' + rel
        if not os.path.isfile(src):
            continue
        # if a same-named file already sits in provenance/, don't clobber — skip the move
        # but still record it as relocated (idempotent re-run safety).
        if os.path.exists(dst) and os.path.abspath(src) != os.path.abspath(dst):
            try:
                if os.path.getsize(dst) == sz and fn not in moved:
                    # dst predates this run (genuine prior-run dup) and matches by size;
                    # the assets/ copy is a stray dup — safe to drop.
                    try:
                        os.remove(src)
                    except OSError:
                        pass
                    moved[fn] = 'provenance/' + fn
                    manifest_items.append({'file': fn, 'bytes': sz, 'reason': reason,
                                           'from': src_from, 'to': 'provenance/' + fn,
                                           'note': 'duplicate in assets/ removed (already in provenance/)'})
                    continue
            except OSError:
                pass
            # different size, OR a within-run basename collision (a same-named orphan from
            # another subdir was already moved this run): keep both, suffix to avoid data loss.
            base, ext = os.path.splitext(fn)
            alt = base + '_dup' + ext
            dst = os.path.join(prov, alt)
            try:
                shutil.move(src, dst)
                moved[fn] = 'provenance/' + alt
                manifest_items.append({'file': fn, 'bytes': sz, 'reason': reason,
                                       'from': src_from, 'to': 'provenance/' + alt})
            except (OSError, shutil.Error) as e:
                print(f'  [warn] could not move {fn}: {e}', file=sys.stderr)
            continue
        try:
            shutil.move(src, dst)
            moved[fn] = 'provenance/' + fn
            manifest_items.append({'file': fn, 'bytes': sz, 'reason': reason,
                                   'from': src_from, 'to': 'provenance/' + fn})
        except (OSError, shutil.Error) as e:
            print(f'  [warn] could not move {fn}: {e}', file=sys.stderr)

    # repoint any dangling JSON pointer that still names a moved original (safety net).
    repointed = {}
    for jname in ('scout.json', 'designer.json', 'hero.json'):
        c = _repoint_in_json(os.path.join(proj, jname), moved)
        if c:
            repointed[jname] = c

    # write the auditable, reversible manifest (idempotent: always rewritten).
    manifest = {
        'generated_by': 'relocate_unreferenced.py',
        'project': os.path.basename(proj),
        'assets_dir': 'assets/',
        'provenance_dir': 'provenance/',
        'moved_count': len(manifest_items),
        'moved': manifest_items,
        'repointed_pointers': repointed,
        'note': 'Heavy unreferenced media masters moved out of assets/ (reversible: move '
                'each back from provenance/ to assets/ to restore). The shipped page does '
                'not load any of these.',
    }
    try:
        with open(sentinel, 'w', encoding='utf-8') as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
    except OSError as e:
        print(f'  [warn] could not write {sentinel}: {e}', file=sys.stderr)

    rp = (' | repointed ' + ', '.join(f'{k}:{v}' for k, v in repointed.items())) if repointed else ''
    print(f'relocate_unreferenced: moved {len(manifest_items)} heavy unreferenced asset(s) '
          f'to provenance/{rp} -> {sentinel}')
    return sentinel


if __name__ == '__main__':
    main()
