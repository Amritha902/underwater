"""Control: is Double Q's PDR gain under harsh channels just smoother link estimates?
Compare +LQ+AL with slower EWMA (lq_beta 0.1, 0.05) against +LQ+DQ+AL (beta 0.2), sigma = 8 dB, w_lq = 0.25."""
import csv, math, statistics as st
from multiprocessing import Pool
from uwsim.paper_sim import Sim, PaperConfig
NODES, SEEDS = [100, 200, 300, 400, 500], range(10)
CFG = [("+LQ+AL beta=0.2", "lq_al", 0.2), ("+LQ+AL beta=0.1", "lq_al", 0.1), ("+LQ+AL beta=0.05", "lq_al", 0.05),
       ("+LQ+DQ+AL beta=0.2", "lq_dq_al", 0.2), ("+LQ+DQ+AL beta=0.1", "lq_dq_al", 0.1)]

def job(a):
    lab, p, b, n, s = a
    r = Sim(PaperConfig(n_sensors=n, shadow_db=8.0, w_lq=0.25, lq_beta=b), p, s).run()
    return {"variant": lab, "nodes": n, "seed": s, **r}

if __name__ == "__main__":
    with Pool() as pool:
        rows = pool.map(job, [(l, p, b, n, s) for l, p, b in CFG for n in NODES for s in SEEDS], chunksize=2)
    with open("results/harsh_control.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    ci = lambda x: 2.262 * st.stdev(x) / math.sqrt(len(x))
    out = ["\n## Control (σ = 8 dB, w_lq = 0.25): smoothing vs Double Q\n",
           "| Variant | PDR | Delay (s) | Lifetime (s) | Tx/packet |", "|---|---|---|---|---|"]
    for lab, _, _ in CFG:
        ps = lambda k: [st.mean(float(r[k]) for r in rows if r["variant"] == lab and r["seed"] == s) for s in SEEDS]
        out.append(f"| {lab} | {st.mean(ps('pdr')):.3f} ± {ci(ps('pdr')):.3f} | {st.mean(ps('delay_s')):.3f} | "
                   f"{st.mean(ps('lifetime_s')):.0f} ± {ci(ps('lifetime_s')):.0f} | {st.mean(ps('tx_per_pkt')):.1f} |")
    txt = "\n".join(out) + "\n"
    open("results/harsh_summary.md", "a").write(txt)
    print(txt)
