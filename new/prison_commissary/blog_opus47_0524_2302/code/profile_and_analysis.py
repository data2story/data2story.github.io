"""Locked In, Priced Out — full analysis. Runnable from DATA_DIR.
Usage: python3 profile_and_analysis.py
Reads the three CSVs in the same directory (or DATA_DIR via env).
"""
import csv, os, statistics
from collections import defaultdict, Counter

DATA = os.environ.get("DATA_DIR", "/Users/forrest/Desktop/data2blog-skill/data/prison_commissary")
PRICES = os.path.join(DATA, "commissary-prices-20240417.csv")
SUMM   = os.path.join(DATA, "commissary-summaries-20240417.csv")
LISTS  = os.path.join(DATA, "commissary-lists-20240417.csv")

def money(s):
    s = (s or "").strip().replace("$", "").replace(",", "")
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None

# load prices
prices = []
with open(PRICES) as f:
    for r in csv.DictReader(f):
        r["p"] = money(r["price"])
        prices.append(r)

# load summaries
summ = []
with open(SUMM) as f:
    for r in csv.DictReader(f):
        r["cp"] = money(r["cheapest_price"])
        r["lo"] = money(r["common_option_low"])
        r["hi"] = money(r["common_option_high"])
        summ.append(r)

# load lists
lists = []
with open(LISTS) as f:
    for r in csv.DictReader(f):
        lists.append(r)

# ============================================================
print("=== ana_00: dataset profile ===")
print(f"prices rows: {len(prices)}")
print(f"summaries rows: {len(summ)}")
print(f"lists rows: {len(lists)}")
states_priced = sorted({r["state"] for r in prices})
print(f"states with price data: {len(states_priced)}")
provided = sum(1 for r in lists if r["list_provided"] == "TRUE")
print(f"states provided list: {provided} of {len(lists)}")
notprov = [r["state"] for r in lists if r["list_provided"] != "TRUE"]
print(f"states NOT provided: {notprov}")
cats = Counter(r["product_category"] for r in prices)
print(f"price categories: {dict(cats)}")
ptypes = Counter(r["product_type"] for r in prices)
print(f"distinct product types: {len(ptypes)}")

# ============================================================
# --- ana_01: cross-state spread for key food/hygiene products (cheapest price) ---
print("\n=== ana_01 ===")
# use summary cheapest_price per state per product_type for clean cross-state comparison
by_type = defaultdict(dict)  # type -> state -> cheapest price
for r in summ:
    if r["cp"] is not None:
        by_type[r["product_type"]][r["state"]] = r["cp"]

def spread(t):
    d = by_type.get(t, {})
    vals = list(d.values())
    if not vals:
        return None
    lo_s = min(d, key=d.get); hi_s = max(d, key=d.get)
    return dict(t=t, n=len(vals), lo=min(vals), lo_state=lo_s, hi=max(vals),
                hi_state=hi_s, ratio=max(vals)/min(vals) if min(vals) else None,
                median=statistics.median(vals))

for t in ["Ramen", "Toothpaste", "Deodorant", "Soap/Body Wash", "Peanut Butter", "Mac and Cheese"]:
    s = spread(t)
    if s:
        print(f"{t}: n={s['n']} states  low=${s['lo']:.2f} ({s['lo_state']})  "
              f"high=${s['hi']:.2f} ({s['hi_state']})  median=${s['median']:.2f}  "
              f"ratio={s['ratio']:.1f}x")

# ============================================================
# --- ana_02: Ramen detail — every state, cheapest price (the flagship example) ---
print("\n=== ana_02 ===")
ramen = sorted(by_type["Ramen"].items(), key=lambda kv: kv[1])
for st, v in ramen:
    print(f"{st}: ${v:.2f}")
rv = [v for _, v in ramen]
print(f"n={len(rv)} low=${min(rv):.2f} high=${max(rv):.2f} ratio={max(rv)/min(rv):.1f}x median=${statistics.median(rv):.2f}")

# ============================================================
# --- ana_03: Hours of prison labor to buy each product (median cheapest / wage) ---
print("\n=== ana_03 ===")
# wage benchmarks from detective det_02
WAGE_LOW = 0.06   # Louisiana avg
WAGE_TYP = 0.25   # rough typical midpoint
prod_med = {}
for t, d in by_type.items():
    vals = list(d.values())
    if len(vals) >= 5:
        prod_med[t] = statistics.median(vals)
for t in ["Ramen", "Soap/Body Wash", "Deodorant", "Toothpaste", "Lotion",
          "Hair Conditioner", "Peanut Butter", "Beans", "Electric Fan", "Reading Glasses"]:
    if t in prod_med:
        m = prod_med[t]
        print(f"{t}: median=${m:.2f}  hrs@$0.06={m/WAGE_LOW:.0f}  hrs@$0.25={m/WAGE_TYP:.0f}")

# ============================================================
# --- ana_04: Most expensive product types overall (median cheapest across states) ---
print("\n=== ana_04 ===")
ranked = sorted(prod_med.items(), key=lambda kv: kv[1], reverse=True)
for t, m in ranked:
    n = len(by_type[t])
    print(f"{t}: median=${m:.2f} (n={n} states)")

# ============================================================
# --- ana_05: Religious items — price level and dispersion ---
print("\n=== ana_05 ===")
rel = [r for r in prices if r["product_category"] == "Religious" and r["p"] is not None]
rel_by_type = defaultdict(list)
for r in rel:
    rel_by_type[r["product_type"]].append(r["p"])
for t, vals in sorted(rel_by_type.items(), key=lambda kv: statistics.median(kv[1]), reverse=True):
    print(f"{t}: n={len(vals)} median=${statistics.median(vals):.2f} low=${min(vals):.2f} high=${max(vals):.2f}")
# Bible vs Quran direct
bible = [r["p"] for r in rel if r["product_type"] == "Bible"]
quran = [r["p"] for r in rel if r["product_type"] == "Quran"]
print(f"Bible median=${statistics.median(bible):.2f} | Quran median=${statistics.median(quran):.2f}")

# ============================================================
# --- ana_06: Vendor landscape (who runs the commissaries) ---
print("\n=== ana_06 ===")
vend = Counter(r["vendor"] for r in lists if r["list_provided"] == "TRUE")
for v, c in vend.most_common():
    print(f"{v}: {c}")

# ============================================================
# --- ana_07: Electric fan price range (heat / headline item) ---
print("\n=== ana_07 ===")
fans = [r for r in prices if r["product_type"] == "Electric Fan" and r["p"] is not None]
fan_by_state = defaultdict(list)
for r in fans:
    fan_by_state[r["state"]].append(r["p"])
fan_min = {s: min(v) for s, v in fan_by_state.items()}
for s, v in sorted(fan_min.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{s}: ${v:.2f}")
fv = list(fan_min.values())
print(f"n={len(fv)} low=${min(fv):.2f} high=${max(fv):.2f} ratio={max(fv)/min(fv):.1f}x")

# ============================================================
# --- ana_08: Within-state range (common_option_low to high) breadth ---
print("\n=== ana_08 ===")
# average price level per state across all summary cheapest prices -> cheapest vs priciest states
state_levels = defaultdict(list)
for r in summ:
    if r["cp"] is not None:
        state_levels[r["state"]].append(r["cp"])
state_avg = {s: statistics.mean(v) for s, v in state_levels.items() if len(v) >= 8}
ranked_states = sorted(state_avg.items(), key=lambda kv: kv[1], reverse=True)
print("Priciest states (mean of cheapest comparable prices, >=8 products):")
for s, v in ranked_states[:8]:
    print(f"  {s}: ${v:.2f}")
print("Cheapest states:")
for s, v in ranked_states[-8:]:
    print(f"  {s}: ${v:.2f}")
