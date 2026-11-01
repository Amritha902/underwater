"""Tune DQ-EVDR v2 weights on held-out tuning seeds (100-102); evaluation uses seeds 0-9."""
import itertools, statistics as st
from multiprocessing import Pool
from uwsim.paper_sim import Sim, PaperConfig
NODES, SEEDS = (150, 300, 500), (100, 101, 102)
GRID = list(itertools.product((0.25, 0.5, 1.0), (0.98, 0.99, 0.995), (0.5, 1.0)))   # w_lq, rho, w_trap

def job(a):
    proto, w, rho, wt, n, s = a
    r = Sim(PaperConfig(n_sensors=n, w_lq=w, rho=rho, w_trap=wt), proto, s).run()
    return a, r

if __name__ == "__main__":
    J = [("qlfr", 0, 0, 0, n, s) for n in NODES for s in SEEDS]
    J += [("dqevdr2", w, rho, wt, n, s) for (w, rho, wt) in GRID for n in NODES for s in SEEDS]
    with Pool() as p:
        res = p.map(job, J)
    base = {}
    for a, r in res:
        if a[0] == "qlfr":
            base.setdefault(a[4], []).append(r)
    B = {n: {k: st.mean(x[k] for x in base[n]) for k in ("pdr", "delay_s", "lifetime_s", "tx_per_pkt")} for n in NODES}
    print("QLFR", B)
    cand = {}
    for a, r in res:
        if a[0] == "dqevdr2":
            cand.setdefault(a[1:4], {}).setdefault(a[4], []).append(r)
    rows = []
    for g, d in cand.items():
        M = {n: {k: st.mean(x[k] for x in d[n]) for k in ("pdr", "delay_s", "lifetime_s", "tx_per_pkt")} for n in NODES}
        dpdr = st.mean(M[n]["pdr"] - B[n]["pdr"] for n in NODES)
        ddel = st.mean(M[n]["delay_s"] - B[n]["delay_s"] for n in NODES)
        life = st.mean(M[n]["lifetime_s"] / B[n]["lifetime_s"] for n in NODES)
        rows.append((g, dpdr, ddel, life))
    rows.sort(key=lambda x: -(x[1] * 10 + (x[3] - 1) - 2 * max(x[2], 0)))
    print("w_lq rho w_trap | dPDR | dDelay | lifetime ratio")
    for g, a, b, c in rows:
        print(g, f"{a:+.3f} {b:+.3f} {c:.2f}")
