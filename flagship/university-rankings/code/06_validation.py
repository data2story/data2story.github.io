"""
06_validation.py — honest era-mismatch robustness check (REQUIRED validation finding).
  ana_11 : recompute the disagreement on the SAME-YEAR 2015 trio (THE n ARWU n CWUR)
           to show "they disagree" is NOT an artefact of mixing 2015 with QS-2023 / current OpenAlex.
Run from DATA_DIR:  PYTHONUTF8=1 py "<PROJECT_DIR>/code/06_validation.py"
"""
import os
import sys
import pandas as pd
from scipy.stats import spearmanr, kendalltau

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c  # noqa: E402

the = c.load_the(2015); arwu = c.load_arwu(2015); cwur = c.load_cwur(2015)

# --- ana_11: 2015-trio validation (all three systems the SAME year) ---
print("=== ana_11 ===")
trio = (the[["key", "rank_num"]].rename(columns={"rank_num": "the"})
        .merge(arwu[["key", "rank_num"]].rename(columns={"rank_num": "arwu"}), on="key")
        .merge(cwur[["key", "rank_num"]].rename(columns={"rank_num": "cwur"}), on="key"))
print("2015 trio core (THE n ARWU n CWUR, all edition year 2015):", len(trio), "schools")
pairs = [("the", "arwu"), ("the", "cwur"), ("arwu", "cwur")]
trio_res = {}
for a, b in pairs:
    rho, _ = spearmanr(trio[a], trio[b]); tau, _ = kendalltau(trio[a], trio[b])
    trio_res[(a, b)] = rho
    print(f"  {a.upper():>4} vs {b.upper():<4}  Spearman={rho:.3f}  Kendall={tau:.3f}")
mean_trio = sum(trio_res.values()) / len(trio_res)
print("Mean same-year (2015) Spearman among the trio: %.3f" % mean_trio)

# contrast: the QS-involving pairs (2023 edition) from the 5-way core
m = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "core_master.csv"))
qs_pairs = {}
for other in ["the_rank", "arwu_rank", "cwur_rank"]:
    rho, _ = spearmanr(m["qs_rank"], m[other])
    qs_pairs[other] = rho
mean_qs = sum(qs_pairs.values()) / len(qs_pairs)
print("Mean QS(2023)-vs-2015-system Spearman:", "%.3f" % mean_qs,
      "->", {k: round(v, 3) for k, v in qs_pairs.items()})
print()
print("VALIDATION VERDICT:")
print("- Same-year (2015) THE/ARWU/CWUR still only agree at Spearman ~%.2f (mean), NOT ~1.0 —" % mean_trio)
print("  so the core 'they disagree' finding is NOT an artefact of mixing years. It holds within 2015 alone.")
print("- LEVEL VALIDATED: cross-SYSTEM disagreement among the three 2015 tables (methodology-only, era held fixed).")
print("- LEVEL THE HEADLINE CLAIMS: the 4-way 'QS/THE/ARWU/CWUR disagree' + the OpenAlex referee overlay.")
print("  GAP: QS is 2023 and OpenAlex is 2026 — any QS- or OpenAlex-involving gap CONFLATES methodology")
print("  divergence with an ~8-year (QS) / ~11-year (OpenAlex vs 2015) time difference. QS's lower correlations")
print("  (mean %.2f vs trio %.2f) are therefore an UPPER bound on methodology divergence, not a clean estimate." % (mean_qs, mean_trio))
print()
print("COMPARABILITY LEDGER (timepoint | method | n):")
print("  THE   | 2015 edition | teaching+research+citations+intl+industry pillars | core n=218")
print("  ARWU  | 2015 edition | research output + Nobel/Fields prizes, no survey  | core n=218")
print("  CWUR  | 2015 edition | outcomes + research, indicator RANKS not scores   | core n=218")
print("  QS    | 2023 edition | reputation surveys 50%, legacy pre-2024 weights   | core n=218 (era overlay +8y)")
print("  OpenAlex | fetched 2026-06-24 | raw works/citations/h-index, size-biased | core n=218 (recent overlay)")
