"""Harsh-channel ablation: log-normal shadowing (sigma = 4, 8 dB, redrawn each round) on top of the paper's
Rayleigh/BPSK channel, with link-term weight w_lq = 0.25 (tuned) and 1.0. Evaluation seeds 0-9."""
import csv
from multiprocessing import Pool

from uwsim.paper_sim import Sim, PaperConfig

NODES = [100, 200, 300, 400, 500]
SEEDS = range(10)
SIGMAS = [4.0, 8.0]
VARIANTS = [("+LQ", "lq"), ("+LQ+DQ", "lq_dq"), ("+LQ+AL", "lq_al"), ("+LQ+DQ+AL", "lq_dq_al"),
            ("DQ-EVDR v2", "dqevdr2")]


def job(a):
    lab, proto, kw, n, s = a
    r = Sim(PaperConfig(n_sensors=n, **kw), proto, s).run()
    return {"variant": lab, "sigma": kw["shadow_db"], "w_lq": kw.get("w_lq", ""), "nodes": n, "seed": s, **r}


def jobs():
    J = []
    for sd in SIGMAS:
        J += [("QLFR (P_th=0.90)", "qlfr", {"shadow_db": sd}, n, s) for n in NODES for s in SEEDS]
        J += [("QLFR (P_th=0.97)", "qlfr", {"shadow_db": sd, "pdr_th": 0.97}, n, s) for n in NODES for s in SEEDS]
        for w in (0.25, 1.0):
            J += [(lab, p, {"shadow_db": sd, "w_lq": w}, n, s) for lab, p in VARIANTS for n in NODES for s in SEEDS]
    return J


if __name__ == "__main__":
    J = jobs()
    with Pool() as pool:
        rows = pool.map(job, J, chunksize=2)
    with open("results/harsh_ablation.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "runs")
