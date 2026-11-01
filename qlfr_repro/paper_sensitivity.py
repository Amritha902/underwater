"""Sensitivity of QLFR to the unspecified PDR threshold P_th (multipath suppression)."""
import csv
from multiprocessing import Pool
from uwsim.paper_sim import Sim, PaperConfig

NODES = [100, 200, 300, 400, 500]


def job(a):
    th, n, s = a
    r = Sim(PaperConfig(n_sensors=n, pdr_th=th), "qlfr", s).run()
    return {"pdr_th": th, "nodes": n, "seed": s, **r}


if __name__ == "__main__":
    J = [(th, n, s) for th in (0.90, 0.97) for n in NODES for s in range(3)]
    with Pool() as p:
        rows = p.map(job, J)
    with open("results/paper_pth_sensitivity.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    import collections, statistics as st
    a = collections.defaultdict(list)
    for r in rows:
        a[(r["pdr_th"], r["nodes"])].append(r)
    print("| P_th | Nodes | PDR | Delay (s) | Lifetime (s) |\n|---|---|---|---|---|")
    for th in (0.90, 0.97):
        for n in NODES:
            x = a[(th, n)]
            print(f"| {th} | {n} | {st.mean(y['pdr'] for y in x):.3f} | {st.mean(y['delay_s'] for y in x):.3f} | {st.mean(y['lifetime_s'] for y in x):.0f} |")
