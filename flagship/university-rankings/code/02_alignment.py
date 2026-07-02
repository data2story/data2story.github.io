"""
02_alignment.py — cross-system name join sizes (pairwise, 4-commercial, 5-way, trio).
Run from DATA_DIR:  PYTHONUTF8=1 py "<PROJECT_DIR>/code/02_alignment.py"
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c  # noqa: E402

the = c.load_the()
arwu = c.load_arwu()
cwur = c.load_cwur()
qs = c.load_qs()
oa = c.load_openalex()
kt, ka, kc, kq, ko = (set(the.key), set(arwu.key), set(cwur.key), set(qs.key), set(oa.key))

# --- ana_03: join sizes — pairwise, 4-commercial, 5-way core, 2015 trio ---
print("=== ana_03 ===")
print("Per-system distinct normalized institutions after dedup:",
      dict(THE=len(kt), ARWU=len(ka), CWUR=len(kc), QS=len(kq), OpenAlex=len(ko)))
pairs = {
    ("THE", "ARWU"): kt & ka, ("THE", "CWUR"): kt & kc, ("THE", "QS"): kt & kq,
    ("THE", "OpenAlex"): kt & ko, ("ARWU", "CWUR"): ka & kc, ("ARWU", "QS"): ka & kq,
    ("ARWU", "OpenAlex"): ka & ko, ("CWUR", "QS"): kc & kq, ("CWUR", "OpenAlex"): kc & ko,
    ("QS", "OpenAlex"): kq & ko,
}
print("Pairwise overlap (# universities present in BOTH):")
for (a, b), s in pairs.items():
    print(f"  {a} n {b} = {len(s)}")
trio = kt & ka & kc                    # THE 2015 n ARWU 2015 n CWUR 2015
four_commercial = kt & ka & kc & kq    # + QS 2023
core5 = kt & ka & kc & kq & ko         # + OpenAlex
print("2015 trio (THE n ARWU n CWUR):", len(trio))
print("4-commercial core (+QS):", len(four_commercial))
print("5-WAY COMMON CORE (+OpenAlex):", len(core5))

# how many of each system's own top-100 survive into the 5-way core (join coverage)
def top_cover(df, n=100):
    top = set(df.sort_values("rank_num").head(n).key)
    return len(top & core5)
print("Coverage of the 5-way core among each system's own TOP 100:",
      dict(THE=top_cover(the), ARWU=top_cover(arwu), CWUR=top_cover(cwur), QS=top_cover(qs)))

# save the core key list + a master merged table for downstream scripts
import pandas as pd  # noqa: E402
master = pd.DataFrame({"key": sorted(core5)})
master = (master
          .merge(the[["key", "university_name", "country", "rank_num"]].rename(
              columns={"rank_num": "the_rank", "university_name": "the_name"}), on="key", how="left")
          .merge(arwu[["key", "rank_num"]].rename(columns={"rank_num": "arwu_rank"}), on="key", how="left")
          .merge(cwur[["key", "rank_num"]].rename(columns={"rank_num": "cwur_rank"}), on="key", how="left")
          .merge(qs[["key", "rank_num"]].rename(columns={"rank_num": "qs_rank"}), on="key", how="left")
          .merge(oa[["key", "institution", "country_code", "works_count", "cited_by_count",
                     "h_index", "two_yr_mean_citedness", "oa_rank_works", "oa_rank_cites",
                     "oa_rank_hindex"]], on="key", how="left"))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "core_master.csv")
master.to_csv(out, index=False)
print("Wrote master core table:", out, "shape", master.shape)
