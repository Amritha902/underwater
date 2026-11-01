"""DQ-EVDR v2 ablation in the QLFR paper setting (Table II). Evaluation seeds 0-9 (tuning used 100-102)."""
import csv
import os
from multiprocessing import Pool

from uwsim.paper_sim import Sim, PaperConfig

NODES = [100, 150, 200, 250, 300, 350, 400, 450, 500]
SEEDS = range(10)
VARIANTS = [  # (label, protocol, extra config)
    ("QLFR (P_th=0.90)", "qlfr", {}),
    ("QLFR (P_th=0.97)", "qlfr", {"pdr_th": 0.97}),
    ("+LQ", "lq", {}),
    ("+LQ+DQ", "lq_dq", {}),
    ("+LQ+AL", "lq_al", {}),
    ("+LQ+DQ+AL", "lq_dq_al", {}),
    ("DQ-EVDR v2 (+LQ+DQ+AL+Trap)", "dqevdr2", {}),
]
os.makedirs("results", exist_ok=True)


def job(a):
    lab, proto, kw, n, s = a
    r = Sim(PaperConfig(n_sensors=n, **kw), proto, s).run()
    return {"variant": lab, "protocol": proto, "nodes": n, "seed": s, **r}


if __name__ == "__main__":
    J = [(lab, p, kw, n, s) for lab, p, kw in VARIANTS for n in NODES for s in SEEDS]
    with Pool() as pool:
        rows = pool.map(job, J, chunksize=2)
    with open("results/ablation.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "runs")
