"""Reproduce QLFR paper Figs. 6-15 (arXiv:2002.09623v1) and add DQ-EVDR. Writes results/paper_*.csv."""
import csv
import os
import sys
from multiprocessing import Pool

from uwsim.paper_sim import Sim, PaperConfig

NODES = [100, 150, 200, 250, 300, 350, 400, 450, 500]
SEEDS = range(5)
os.makedirs("results", exist_ok=True)


def job(a):
    exp, proto, n, k, v, seed = a
    r = Sim(PaperConfig(n_sensors=n, k=k, speed=v), proto, seed).run()
    return {"exp": exp, "protocol": proto, "nodes": n, "k": k, "speed": v, "seed": seed, **r}


def jobs():
    J = []
    for p in ("dbr", "eedbr", "dvor", "qlfr", "dqevdr"):                 # Figs. 6-8 (k=0.05 s, v=3 m/s)
        J += [("fig6_8", p, n, 0.05, 3.0, s) for n in NODES for s in SEEDS]
    for p in ("qlfr", "qelar"):                                           # Fig. 9 (v=1 m/s)
        J += [("fig9", p, n, 0.05, 1.0, s) for n in (200, 250, 300) for s in SEEDS]
    for k in (0.01, 0.1):                                                 # Figs. 10-12 (k=0.05 reused)
        J += [("fig10_12", "qlfr", n, k, 3.0, s) for n in NODES for s in SEEDS]
    for v in (1.0, 5.0):                                                  # Figs. 13-15 (v=3 reused)
        J += [("fig13_15", "qlfr", n, 0.05, v, s) for n in NODES for s in SEEDS]
    return J


if __name__ == "__main__":
    J = jobs()
    with Pool() as pool:
        rows = pool.map(job, J, chunksize=1)
    with open("results/paper_runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "runs")
