"""
04_referee.py — the neutral referee (OpenAlex research output).
  ana_07 : correlate each commercial system's rank against the OpenAlex output order
           (which table tracks measured output; which leans most on reputation)
  ana_08 : the referee crowns YET ANOTHER order (works vs citations vs h-index all differ,
           and none matches any single commercial #1)
Run from DATA_DIR:  PYTHONUTF8=1 py "<PROJECT_DIR>/code/04_referee.py"
"""
import os
import sys
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c  # noqa: E402

m = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "core_master.csv"))
SYS = {"the_rank": "THE", "arwu_rank": "ARWU", "cwur_rank": "CWUR", "qs_rank": "QS"}

# --- ana_07: each system's rank vs the OpenAlex output/impact order ---
print("=== ana_07 ===")
print("Spearman of each commercial rank against OpenAlex (n=%d core schools):" % len(m))
print(f"{'system':<6}{'vs works_count':>16}{'vs cited_by':>14}{'vs h_index':>13}")
res = {}
for col, lab in SYS.items():
    rw, _ = spearmanr(m[col], m["oa_rank_works"])
    rc, _ = spearmanr(m[col], m["oa_rank_cites"])
    rh, _ = spearmanr(m[col], m["oa_rank_hindex"])
    res[lab] = (rw, rc, rh)
    print(f"{lab:<6}{rw:>16.3f}{rc:>14.3f}{rh:>13.3f}")
by_works = sorted(res.items(), key=lambda kv: kv[1][0], reverse=True)
print("Tracks raw OUTPUT (works_count) most closely:", by_works[0][0], "%.3f" % by_works[0][1][0])
print("Tracks raw OUTPUT least closely (most reputation-driven):", by_works[-1][0], "%.3f" % by_works[-1][1][0])
by_h = sorted(res.items(), key=lambda kv: kv[1][2], reverse=True)
print("Tracks IMPACT (h_index) most closely:", by_h[0][0], "%.3f" % by_h[0][1][2])
print("NOTE even the best correlation (%.2f) leaves the tables far from the output order — "
      "none is 'just measuring output'." % by_works[0][1][0])

# --- ana_08: the referee crowns another order (works vs cites vs h-index) ---
print("=== ana_08 ===")
oa = c.load_openalex()
def topn(metric, n=10):
    return oa.sort_values(metric, ascending=False).head(n)[["institution", metric]].reset_index(drop=True)
w = topn("works_count"); ci = topn("cited_by_count"); h = topn("h_index")
tbl = pd.DataFrame({
    "by works_count": w["institution"], "by cited_by_count": ci["institution"], "by h_index": h["institution"],
})
tbl.index = range(1, 11)
print(tbl.to_string())
print("\nOpenAlex #1 by each lens:",
      dict(works=w.institution[0], cited_by=ci.institution[0], h_index=h.institution[0]))
# do these three neutral orders even agree at the top?
rw_c, _ = spearmanr(oa["works_count"].rank(ascending=False), oa["cited_by_count"].rank(ascending=False))
rw_h, _ = spearmanr(oa["works_count"].rank(ascending=False), oa["h_index"].rank(ascending=False))
print("Spearman among the neutral lenses themselves: works vs cited_by=%.3f, works vs h_index=%.3f "
      "(the referee disagrees with ITSELF depending on volume vs impact)." % (rw_c, rw_h))
# Michigan crown vs commercial best rank
mi = m[m.key == "michigan"].iloc[0]
print("Michigan: OpenAlex works rank #%d, but best commercial rank is #%d (THE) — the raw-output giant no table crowns."
      % (mi.oa_rank_works, min(mi.the_rank, mi.arwu_rank, mi.cwur_rank, mi.qs_rank)))
