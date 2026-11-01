"""Tables (results/harsh_summary.md) and figure (figures/harsh_ablation.png) from results/harsh_ablation.csv."""
import collections
import csv
import math
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from harsh_ablation import NODES, SIGMAS, VARIANTS

rows = list(csv.DictReader(open("results/harsh_ablation.csv")))
D = collections.defaultdict(dict)
for r in rows:
    key = r["variant"] if r["w_lq"] == "" else f'{r["variant"]} [w_lq={float(r["w_lq"]):g}]'
    D[(float(r["sigma"]), key, int(r["nodes"]))][int(r["seed"])] = r
SEEDS = range(10)


def ci(x):
    return 2.262 * st.stdev(x) / math.sqrt(len(x))


def per_seed(sd, lab, k):
    return [st.mean(float(D[(sd, lab, n)][s][k]) for n in NODES) for s in SEEDS]


def paired(sd, lab, base, k, op):
    return [st.mean(op(float(D[(sd, lab, n)][s][k]), float(D[(sd, base, n)][s][k])) for n in NODES) for s in SEEDS]


labs = ["QLFR (P_th=0.90)", "QLFR (P_th=0.97)"] + [f"{l} [w_lq={w:g}]" for w in (0.25, 1.0) for l, _ in VARIANTS]
out = ["# Harsh-channel ablation (log-normal shadowing redrawn every round; 10 seeds; 100–500 nodes; mean ± 95% CI)\n"]
for sd in SIGMAS:
    out.append(f"\n## σ = {sd:g} dB: averaged over densities\n")
    out.append("| Variant | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet | V bias |\n|---|---|---|---|---|---|---|")
    for lab in labs:
        c = []
        for k, f in (("pdr", "{:.3f}"), ("delay_s", "{:.3f}"), ("lifetime_s", "{:.0f}"), ("energy_j", "{:.0f}"),
                     ("tx_per_pkt", "{:.1f}"), ("v_bias", "{:+.3f}")):
            v = per_seed(sd, lab, k)
            c.append("—" if any(math.isnan(x) for x in v) else (f + " ± " + f.replace("+", "")).format(st.mean(v), ci(v)))
        out.append(f"| {lab} | " + " | ".join(c) + " |")
    for base in ("QLFR (P_th=0.90)", "QLFR (P_th=0.97)"):
        out.append(f"\n### σ = {sd:g} dB: paired vs {base}\n")
        out.append("| Variant | ΔPDR | ΔDelay (s) | Lifetime ratio | Tx ratio |\n|---|---|---|---|---|")
        for lab in labs[2:]:
            dp = paired(sd, lab, base, "pdr", lambda a, b: a - b)
            dd = paired(sd, lab, base, "delay_s", lambda a, b: a - b)
            lr = paired(sd, lab, base, "lifetime_s", lambda a, b: a / b)
            tr = paired(sd, lab, base, "tx_per_pkt", lambda a, b: a / b)
            out.append(f"| {lab} | {st.mean(dp):+.3f} ± {ci(dp):.3f} | {st.mean(dd):+.3f} ± {ci(dd):.3f} | "
                       f"{st.mean(lr):.2f} ± {ci(lr):.2f} | {st.mean(tr):.2f} ± {ci(tr):.2f} |")
    out.append(f"\n### σ = {sd:g} dB: effect of Double Q (paired, same seeds)\n")
    out.append("| Comparison | ΔPDR | ΔDelay (s) | Lifetime ratio | ΔV bias |\n|---|---|---|---|---|")
    for w in (0.25, 1.0):
        for a, b in (("+LQ+DQ", "+LQ"), ("+LQ+DQ+AL", "+LQ+AL")):
            A, B = f"{a} [w_lq={w:g}]", f"{b} [w_lq={w:g}]"
            dp = paired(sd, A, B, "pdr", lambda x, y: x - y)
            dd = paired(sd, A, B, "delay_s", lambda x, y: x - y)
            lr = paired(sd, A, B, "lifetime_s", lambda x, y: x / y)
            db = paired(sd, A, B, "v_bias", lambda x, y: x - y)
            out.append(f"| {A} vs {B} | {st.mean(dp):+.3f} ± {ci(dp):.3f} | {st.mean(dd):+.3f} ± {ci(dd):.3f} | "
                       f"{st.mean(lr):.2f} ± {ci(lr):.2f} | {st.mean(db):+.3f} ± {ci(db):.3f} |")
open("results/harsh_summary.md", "w").write("\n".join(out) + "\n")

show = ["QLFR (P_th=0.90)", "QLFR (P_th=0.97)", "+LQ+AL [w_lq=0.25]", "+LQ+DQ+AL [w_lq=0.25]", "DQ-EVDR v2 [w_lq=0.25]",
        "+LQ+AL [w_lq=1]", "DQ-EVDR v2 [w_lq=1]"]
COL = ["#6C757D", "#ADB5BD", "#E69F00", "#D55E00", "#009E73", "#56B4E9", "#0072B2"]
fig, axs = plt.subplots(2, 3, figsize=(14, 7))
for i, sd in enumerate(SIGMAS):
    for ax, (k, name) in zip(axs[i], (("pdr", "PDR"), ("delay_s", "Delay (s)"), ("lifetime_s", "Lifetime (s)"))):
        for lab, c in zip(show, COL):
            ax.errorbar(NODES, [st.mean(float(x[k]) for x in D[(sd, lab, n)].values()) for n in NODES],
                        yerr=[ci([float(x[k]) for x in D[(sd, lab, n)].values()]) for n in NODES],
                        label=lab, color=c, marker="o", ms=3, capsize=2, lw=2 if "v2" in lab else 1.2)
        ax.set_title(f"σ = {sd:g} dB: {name}", fontsize=10)
        ax.set_xlabel("Number of nodes")
        ax.grid(alpha=0.3)
axs[0][0].legend(frameon=False, fontsize=7)
fig.tight_layout()
fig.savefig("figures/harsh_ablation.png", dpi=150)
print(open("results/harsh_summary.md").read())
