"""Confirmation on fresh seeds 200-209 (never used for tuning or evaluation) of the revised choice rho = 0.99,
which was picked after the pre-registered rho = 0.98 violated the PDR constraint on evaluation seeds."""
import csv, math, statistics as st
from multiprocessing import Pool
from uwsim.paper_sim import Sim, PaperConfig
SEEDS, NODES, SIGMAS = range(200, 210), [100, 200, 300, 400, 500], [0.0, 4.0, 8.0]
P = [("QLFR (P_th=0.90)", "qlfr", {}), ("QLFR (P_th=0.97)", "qlfr", {"pdr_th": 0.97}),
     ("LAQR (rho=0.99)", "lq_al", {"lq_beta": 0.05, "rho": 0.99})]

def job(a):
    lab, p, kw, sd, n, s = a
    return {"protocol": lab, "sigma": sd, "nodes": n, "seed": s, **Sim(PaperConfig(n_sensors=n, shadow_db=sd, **kw), p, s).run()}

if __name__ == "__main__":
    with Pool() as pool:
        rows = pool.map(job, [(l, p, kw, sd, n, s) for l, p, kw in P for sd in SIGMAS for n in NODES for s in SEEDS], chunksize=2)
    with open("results/confirm_final.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    D = {(r["protocol"], r["sigma"], r["nodes"], r["seed"]): r for r in rows}
    ci = lambda x: 2.262 * st.stdev(x) / math.sqrt(len(x))
    out = ["\n## Confirmation on fresh seeds 200-209: LAQR (ρ = 0.99) paired vs QLFR\n",
           "| σ (dB) | Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio |", "|---|---|---|---|---|---|"]
    for sd in SIGMAS:
        for b in ("QLFR (P_th=0.90)", "QLFR (P_th=0.97)"):
            f = lambda k, op: [st.mean(op(D[("LAQR (rho=0.99)", sd, n, s)][k], D[(b, sd, n, s)][k]) for n in NODES) for s in SEEDS]
            dp, dd = f("pdr", lambda a, c: a - c), f("delay_s", lambda a, c: a - c)
            lr, er = f("lifetime_s", lambda a, c: a / c), f("energy_j", lambda a, c: a / c)
            out.append(f"| {sd:g} | {b} | {st.mean(dp):+.3f} ± {ci(dp):.3f} | {st.mean(dd):+.3f} ± {ci(dd):.3f} | "
                       f"{st.mean(lr):.2f} ± {ci(lr):.2f} | {st.mean(er):.2f} ± {ci(er):.2f} |")
    t = "\n".join(out) + "\n"
    open("results/final_summary.md", "a").write(t)
    print(t)
