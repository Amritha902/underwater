"""Tune the final protocol (single estimator + link quality + adaptive list, trap optional) on tuning seeds
100-104 across sigma = 0, 4, 8 dB. One setting must work on all channels."""
import csv, itertools, math, statistics as st
from multiprocessing import Pool
from uwsim.paper_sim import Sim, PaperConfig

NODES, SEEDS, SIGMAS = (150, 300, 500), range(100, 105), (0.0, 4.0, 8.0)
GRID = list(itertools.product((0.03, 0.05, 0.1, 0.2), (0.98, 0.99, 0.995), ("lq_al", "lq_al_trap")))


def job(a):
    proto, beta, rho, sd, n, s = a
    kw = dict(n_sensors=n, shadow_db=sd)
    if proto != "qlfr":
        kw.update(lq_beta=beta, rho=rho)
    r = Sim(PaperConfig(**kw), proto, s).run()
    return a, r


if __name__ == "__main__":
    J = [("qlfr", 0, 0, sd, n, s) for sd in SIGMAS for n in NODES for s in SEEDS]
    J += [(p, b, rho, sd, n, s) for b, rho, p in GRID for sd in SIGMAS for n in NODES for s in SEEDS]
    with Pool() as pool:
        res = pool.map(job, J, chunksize=2)
    with open("results/tune_final.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protocol", "beta", "rho", "sigma", "nodes", "seed", "pdr", "delay_s", "lifetime_s", "tx_per_pkt"])
        for a, r in res:
            w.writerow(list(a) + [r["pdr"], r["delay_s"], r["lifetime_s"], r["tx_per_pkt"]])
    base = {}
    for a, r in res:
        if a[0] == "qlfr":
            base[(a[3], a[4], a[5])] = r
    cand = {}
    for a, r in res:
        if a[0] != "qlfr":
            cand.setdefault((a[0], a[1], a[2]), []).append((a, r))
    lines = ["| Protocol | beta | rho | min over σ of ΔPDR | ΔPDR σ=0/4/8 | lifetime ratio σ=0/4/8 | ΔDelay σ=0/4/8 (s) | feasible |",
             "|---|---|---|---|---|---|---|---|"]
    scored = []
    for key, lst in cand.items():
        per = {}
        for sd in SIGMAS:
            sub = [(a, r) for a, r in lst if a[3] == sd]
            dp = st.mean(r["pdr"] - base[(sd, a[4], a[5])]["pdr"] for a, r in sub)
            lr = st.mean(r["lifetime_s"] / base[(sd, a[4], a[5])]["lifetime_s"] for a, r in sub)
            dd = st.mean(r["delay_s"] - base[(sd, a[4], a[5])]["delay_s"] for a, r in sub)
            per[sd] = (dp, lr, dd)
        mindp = min(v[0] for v in per.values())
        feasible = mindp >= -0.005                          # never worse than QLFR on PDR (tolerance 0.5 pt)
        score = (feasible, st.mean(v[1] for v in per.values()), -st.mean(v[2] for v in per.values()))
        scored.append((score, key, per, mindp, feasible))
    scored.sort(key=lambda x: x[0], reverse=True)
    for score, key, per, mindp, feasible in scored:
        lines.append(f"| {key[0]} | {key[1]} | {key[2]} | {mindp:+.3f} | " + "/".join(f"{per[s][0]:+.3f}" for s in SIGMAS)
                     + " | " + "/".join(f"{per[s][1]:.2f}" for s in SIGMAS) + " | "
                     + "/".join(f"{per[s][2]:+.3f}" for s in SIGMAS) + f" | {'yes' if feasible else 'no'} |")
    txt = ("# Final-protocol tuning (tuning seeds 100-104; differences vs QLFR P_th=0.90 on the same seeds)\n\n"
           "Selection: feasible = ΔPDR ≥ −0.005 on every channel; then maximise mean lifetime ratio; tie-break lower delay.\n\n"
           + "\n".join(lines) + "\n")
    open("results/tune_final.md", "w").write(txt)
    print(txt)
