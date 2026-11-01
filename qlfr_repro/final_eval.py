"""Final evaluation of the selected protocol on evaluation seeds 0-9 (never used in tuning).
Reads the selected configuration from results/final_config.json."""
import csv
import json
from multiprocessing import Pool

from uwsim.paper_sim import Sim, PaperConfig

FINAL = json.load(open("results/final_config.json"))
SEEDS = range(10)
SCEN = [(0.0, [100, 150, 200, 250, 300, 350, 400, 450, 500]), (4.0, [100, 200, 300, 400, 500]),
        (8.0, [100, 200, 300, 400, 500])]
PROTOS = [
    ("QLFR (P_th=0.90)", "qlfr", {}),
    ("QLFR (P_th=0.97)", "qlfr", {"pdr_th": 0.97}),
    ("DQ-EVDR v2", "dqevdr2", {}),
    (FINAL["name"], FINAL["protocol"], {"lq_beta": FINAL["beta"], "rho": FINAL["rho"]}),
]


def job(a):
    lab, p, kw, sd, n, s = a
    r = Sim(PaperConfig(n_sensors=n, shadow_db=sd, **kw), p, s).run()
    return {"protocol": lab, "sigma": sd, "nodes": n, "seed": s, **r}


if __name__ == "__main__":
    J = [(l, p, kw, sd, n, s) for sd, NN in SCEN for l, p, kw in PROTOS for n in NN for s in SEEDS]
    with Pool() as pool:
        rows = pool.map(job, J, chunksize=2)
    with open("results/final_eval.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "runs")
