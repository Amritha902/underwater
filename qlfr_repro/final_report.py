"""Tables (results/final_summary.md) and figure (figures/final_protocol.png) from results/final_eval.csv."""
import collections, csv, json, math, statistics as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from final_eval import SCEN, PROTOS, FINAL

rows = list(csv.DictReader(open("results/final_eval.csv")))
D = collections.defaultdict(dict)
for r in rows:
    D[(float(r["sigma"]), r["protocol"], int(r["nodes"]))][int(r["seed"])] = r
LABS = [p[0] for p in PROTOS]
ci = lambda x: 2.262 * st.stdev(x) / math.sqrt(len(x))


def ps(sd, NN, lab, k):
    return [st.mean(float(D[(sd, lab, n)][s][k]) for n in NN) for s in range(10)]


def pair(sd, NN, a, b, k, op):
    return [st.mean(op(float(D[(sd, a, n)][s][k]), float(D[(sd, b, n)][s][k])) for n in NN) for s in range(10)]


out = [f"# Final protocol evaluation: {FINAL['name']} (evaluation seeds 0-9; mean ± 95% CI)\n",
       f"Configuration: protocol variant `{FINAL['protocol']}`, β = {FINAL['beta']}, ρ = {FINAL['rho']} "
       "(selected on tuning seeds 100-104; see results/tune_final.md).\n"]
for sd, NN in SCEN:
    out.append(f"\n## σ = {sd:g} dB ({NN[0]}–{NN[-1]} nodes)\n")
    out.append("| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |\n|---|---|---|---|---|---|")
    for lab in LABS:
        c = [f"{st.mean(v):.3f} ± {ci(v):.3f}" if k in ("pdr", "delay_s") else f"{st.mean(v):.0f} ± {ci(v):.0f}"
             if k != "tx_per_pkt" else f"{st.mean(v):.1f}" for k in ("pdr", "delay_s", "lifetime_s", "energy_j", "tx_per_pkt")
             for v in [ps(sd, NN, lab, k)]]
        out.append(f"| {lab} | " + " | ".join(c) + " |")
    out.append(f"\n**{FINAL['name']} paired vs each baseline (σ = {sd:g} dB)**\n")
    out.append("| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio |\n|---|---|---|---|---|")
    for b in LABS[:-1]:
        dp = pair(sd, NN, FINAL["name"], b, "pdr", lambda x, y: x - y)
        dd = pair(sd, NN, FINAL["name"], b, "delay_s", lambda x, y: x - y)
        lr = pair(sd, NN, FINAL["name"], b, "lifetime_s", lambda x, y: x / y)
        er = pair(sd, NN, FINAL["name"], b, "energy_j", lambda x, y: x / y)
        out.append(f"| {b} | {st.mean(dp):+.3f} ± {ci(dp):.3f} | {st.mean(dd):+.3f} ± {ci(dd):.3f} | "
                   f"{st.mean(lr):.2f} ± {ci(lr):.2f} | {st.mean(er):.2f} ± {ci(er):.2f} |")
open("results/final_summary.md", "w").write("\n".join(out) + "\n")

COL = {LABS[0]: "#6C757D", LABS[1]: "#ADB5BD", LABS[2]: "#0072B2", LABS[3]: "#E69F00", LABS[4]: "#009E73"}
fig, axs = plt.subplots(3, 3, figsize=(14, 10))
for i, (sd, NN) in enumerate(SCEN):
    for ax, (k, name) in zip(axs[i], (("pdr", "PDR"), ("delay_s", "Delay (s)"), ("lifetime_s", "Lifetime (s)"))):
        for lab in LABS:
            v = [[float(x[k]) for x in D[(sd, lab, n)].values()] for n in NN]
            ax.errorbar(NN, [st.mean(x) for x in v], yerr=[ci(x) for x in v], label=lab, color=COL[lab],
                        marker="o", ms=3, capsize=2, lw=2.4 if lab.startswith("LAQR") else 1.2)
        ax.set_title(f"σ = {sd:g} dB: {name}", fontsize=10)
        ax.set_xlabel("Number of nodes")
        ax.grid(alpha=0.3)
axs[0][0].legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig("figures/final_protocol.png", dpi=150)
print(open("results/final_summary.md").read())
