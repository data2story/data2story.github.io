"""
_corpus.py — resolve the OPTIONAL local dataset corpus root for find-data.

find-data is local-first: when a corpus of already-cloned datasets is present
it searches there before going online, and it degrades cleanly to remote
fetch / WebSearch when no corpus is configured. This module is the single
place the corpus location is decided, so no tool hard-codes a workspace layout.

Resolution order (first hit wins):

  (a) $DATA2STORY_DATASETS — if set and pointing at an existing directory;
  (b) the nearest `datasets/` directory found by walking up from the current
      working directory;
  (c) a non-existent sentinel under the skill dir ("<find-data>/.no_local_corpora").

In case (c) the returned path never exists on disk, so every is_dir()/exists()
guard in the callers returns empty and discovery falls through to remote fetch
/ WebSearch without crashing.
"""
from __future__ import annotations

import os
from pathlib import Path

# Generic corpus directory name searched for while walking up from cwd.
CORPUS_DIRNAME = "datasets"
# Sentinel used when no corpus is configured — chosen so it never exists on disk.
NO_CORPUS_SENTINEL = ".no_local_corpora"
# Environment override pointing directly at a corpus root.
ENV_VAR = "DATA2STORY_DATASETS"


def resolve_datasets_root() -> Path:
    """Return the local dataset corpus root (see module docstring for order).

    The result is NOT guaranteed to exist: with no corpus configured it is a
    sentinel path that never exists, which is what makes the callers' local
    scans no-op and degrade to remote fetch / WebSearch.
    """
    # (a) explicit override
    override = os.environ.get(ENV_VAR)
    if override:
        p = Path(override).expanduser()
        if p.is_dir():
            return p

    # (b) nearest generic datasets/ dir, walking up from the working directory
    cwd = Path.cwd().resolve()
    for parent in (cwd, *cwd.parents):
        candidate = parent / CORPUS_DIRNAME
        if candidate.is_dir():
            return candidate

    # (c) no corpus configured: sentinel under the skill dir (never exists)
    skill_dir = Path(__file__).resolve().parent.parent  # tools/ -> find-data/
    return skill_dir / NO_CORPUS_SENTINEL
