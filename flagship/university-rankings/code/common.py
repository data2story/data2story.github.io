"""
common.py — shared loaders + institution-name normalizer for the
university-rankings-disagree analysis.

Run every sibling script from DATA_DIR (the dataset root), e.g.:
    cd "<DATA_DIR>"
    PYTHONUTF8=1 py "<PROJECT_DIR>/code/03_pairwise.py"

The normalizer is the load-bearing join key: it reduces each system's
institution string to a comparable token set so the SAME university lines up
across THE / ARWU / CWUR / QS / OpenAlex. It is deliberately fuzzy (name-only,
no ROR for the commercial tables), so a small number of edge cases can mis-join
— that unmatched/mis-join count is reported honestly in the alignment finding.
"""
import os
import re
import unicodedata
import pandas as pd

# Resolve DATA_DIR = current working directory (scripts are launched from there).
DATA_DIR = os.getcwd()

# Stopwords stripped before comparing names. We drop the generic "university"
# tokens and grammatical glue, but KEEP discriminating words like
# "institute", "technology", "college", "state", "national", city names.
_STOP = {
    "university", "universities", "the", "of", "at", "a", "and", "for",
    "in", "de", "der", "des", "und",
}

# A few explicit aliases where the same school is named too differently for the
# token normalizer to unify (abbreviations / translated names). Keyed by the
# normalized form we want them ALL to collapse to.
_ALIAS = {
    # ETH Zurich appears translated ("Swiss Federal Institute of Technology")
    "eth zurich swiss federal institute technology zurich": "eth zurich",
    "eth zurich swiss federal institute technology": "eth zurich",
    "swiss federal institute technology zurich": "eth zurich",
    "swiss federal institute technology in zurich": "eth zurich",
    "eth zurich": "eth zurich",
    "swiss federal institute technology lausanne epfl": "epfl lausanne",
    "ecole polytechnique federale lausanne": "epfl lausanne",
    # University of Michigan: THE/OpenAlex say "University of Michigan" while
    # ARWU/CWUR/QS append "Ann Arbor". Collapse them (this is the flagship
    # OpenAlex #1 raw-output subject, so the mis-join matters).
    "michigan ann arbor": "michigan",
    # Munich technical university variants
    "technical munich": "technische munchen",
    "technische munchen": "technische munchen",
    # Paris-Saclay / Pierre & Marie Curie etc. left to the token normalizer.
    # Peking / Tsinghua are already stable.
}


def normalize_name(name: str) -> str:
    """Reduce an institution name to a comparable token string."""
    if not isinstance(name, str):
        return ""
    s = name.strip()
    # strip parenthetical content e.g. "(MIT)", "(UCB)"
    s = re.sub(r"\([^)]*\)", " ", s)
    # unify ampersand
    s = s.replace("&", " and ")
    # drop accents -> ascii
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    # non-alphanumeric -> space
    s = re.sub(r"[^a-z0-9]+", " ", s)
    tokens = [t for t in s.split() if t and t not in _STOP]
    key = " ".join(tokens)
    key = re.sub(r"\s+", " ", key).strip()
    return _ALIAS.get(key, key)


# ---- loaders (return per-system 2015 / current tables, one row per school) ----

def load_the(year=2015):
    df = pd.read_csv(os.path.join(DATA_DIR, "the", "timesData.csv"))
    df = df[df.year == year].copy()
    df["rank_num"] = df["world_rank"].apply(_first_rank)
    df["key"] = df["university_name"].apply(normalize_name)
    df = df.drop_duplicates("key", keep="first")
    return df


def load_arwu(year=2015):
    df = pd.read_csv(os.path.join(DATA_DIR, "arwu", "shanghaiData.csv"))
    df = df[df.year == year].copy()
    df["rank_num"] = df["world_rank"].apply(_first_rank)
    df["key"] = df["university_name"].apply(normalize_name)
    df = df.drop_duplicates("key", keep="first")
    return df


def load_cwur(year=2015):
    df = pd.read_csv(os.path.join(DATA_DIR, "cwur", "cwurData.csv"))
    df = df[df.year == year].copy()
    df["rank_num"] = pd.to_numeric(df["world_rank"], errors="coerce")
    df["key"] = df["institution"].apply(normalize_name)
    df = df.drop_duplicates("key", keep="first")
    return df


def load_qs():
    df = pd.read_csv(os.path.join(DATA_DIR, "qs", "QS_2023_Dataset.csv"))
    df["rank_num"] = df["rank display"].apply(_first_rank)
    df["score_num"] = pd.to_numeric(df["score scaled"], errors="coerce")
    df["key"] = df["institution"].apply(normalize_name)
    df = df.drop_duplicates("key", keep="first")
    return df


def load_openalex():
    df = pd.read_csv(
        os.path.join(DATA_DIR, "openalex", "openalex_institutions_research_output.csv")
    )
    df["key"] = df["institution"].apply(normalize_name)
    df = df.drop_duplicates("key", keep="first")
    # OpenAlex "world rank" by raw output volume (1 = most works)
    df = df.sort_values("works_count", ascending=False).reset_index(drop=True)
    df["oa_rank_works"] = df["works_count"].rank(ascending=False, method="min").astype(int)
    df["oa_rank_cites"] = df["cited_by_count"].rank(ascending=False, method="min").astype(int)
    df["oa_rank_hindex"] = df["h_index"].rank(ascending=False, method="min").astype(int)
    return df


def _first_rank(v):
    """Turn a rank cell into a numeric rank.
    Handles ints, '6=' ties, and banded ranks like '201-225' (uses the band's
    lower bound as the representative rank).
    """
    if pd.isna(v):
        return None
    s = str(v).strip().replace("=", "")
    m = re.match(r"^\s*(\d+)", s)
    return int(m.group(1)) if m else None
