"""Run all experiments and write results/*.csv and figures/*.png."""
import csv
import os
import sys
from dataclasses import replace
from multiprocessing import Pool

import numpy as np

from uwsim.config import Config
from uwsim.network import Network

PROTOCOLS = ["dbr", "vbf", "qlfr", "dqevdr"]
LABELS = {"dbr": "DBR", "vbf": "VBF", "qlfr": "QLFR (Q-learning)", "dqevdr": "DQ-EVDR (ours)"}
NODES = [100, 150, 200, 250, 300, 400, 500]
SEEDS = range(5)
N_PACKETS, INTERVAL = 400, 20.0
os.makedirs("results", exist_ok=True)


def run_density(args):
    proto, n, seed = args
    r = Network(Config(), n, proto, seed).run(N_PACKETS, INTERVAL)
    return {"protocol": proto, "nodes": n, "seed": seed, **r}


def run_lifetime(args):
    proto, seed = args
    cfg = replace(Config(), initial_energy_j=15.0)
    net = Network(cfg, 300, proto, seed)
    r = net.run(5000, INTERVAL, stop_on_first_death=True)
    return {"protocol": proto, "seed": seed, "packets_before_first_death": r["first_death_pkt"] or r["generated"],
            "pdr": r["pdr"]}


def run_learning(args):
    proto, seed = args
    net = Network(Config(), 200, proto, seed)
    net.run(1000, INTERVAL)
    gen = net.m.generated
    delivered = np.zeros(gen)
    for p in net.m.delivered:
        delivered[p] = 1
    w = 100
    return [{"protocol": proto, "seed": seed, "window_end": k + w, "pdr": delivered[k:k + w].mean()}
            for k in range(0, gen - w + 1, w)]


def write(name, rows):
    with open(f"results/{name}.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)


if __name__ == "__main__":
    which = sys.argv[1:] or ["density", "lifetime", "learning"]
    with Pool() as pool:
        if "density" in which:
            write("density", pool.map(run_density, [(p, n, s) for p in PROTOCOLS for n in NODES for s in SEEDS]))
        if "lifetime" in which:
            write("lifetime", pool.map(run_lifetime, [(p, s) for p in PROTOCOLS for s in SEEDS]))
        if "learning" in which:
            rows = [r for rs in pool.map(run_learning, [(p, s) for p in ("qlfr", "dqevdr") for s in SEEDS]) for r in rs]
            write("learning", rows)
    print("done")
