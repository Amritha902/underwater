"""Tables (results/ablation_summary.md) and figure (figures/ablation.png) from results/ablation.csv."""
import collections
import csv
import math
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ablation import VARIANTS, NODES

rows = list(csv.DictReader(open("results/ablation.csv")))
D = collections.defaultdict(dict)
for r in rows:
    D[(r["variant"], int(r["nodes"]))][int(r["seed"])] = r
LABS = [v[0] for v in VARIANTS]
METRICS = [("pdr", "PDR", "{:.3f}"), ("delay_s", "Delay (s)", "{:.3f}"), ("lifetime_s", "Lifetime (s)", "{:.0f}"),
           ("energy_j", "Total energy (J)", "{:.0f}"), ("tx_per_pkt", "Tx / packet", "{:.1f}"), ("v_bias", "V bias", "{:+.3f}")]


def vals(lab, n, k):
    return [float(x[k]) for x in D[(lab, n)].values()]


def ci(x):
    return 2.262 * st.stdev(x) / math.sqrt(len(x)) if len(x) > 1 else 0.0


out = ["# DQ-EVDR v2 ablation (QLFR paper setting, Table II; 10 evaluation seeds, mean ± 95% CI)\n"]
# averaged over all densities
out.append("## Averaged over 100–500 nodes\n")
out.append("| Variant | " + " | ".join(m[1] for m in METRICS) + " |")
out.append("|---|" + "---|" * len(METRICS))
for lab in LABS:
    cells = []
    for k, _, fmt in METRICS:
        per_seed = [st.mean(float(D[(lab, n)][s][k]) for n in NODES) for s in range(10)]
        cells.append((fmt + " ± " + fmt.replace("+", "")).format(st.mean(per_seed), ci(per_seed)) if not any(map(math.isnan, per_seed)) else "—")
    out.append(f"| {lab} | " + " | ".join(cells) + " |")
for k, name, fmt in METRICS[:5]:
    out.append(f"\n## {name} by number of nodes\n")
    out.append("| Nodes | " + " | ".join(LABS) + " |")
    out.append("|---|" + "---|" * len(LABS))
    for n in NODES:
        out.append(f"| {n} | " + " | ".join(fmt.format(st.mean(vals(l, n, k))) for l in LABS) + " |")
# paired tests vs QLFR(0.90)
out.append("\n## Paired difference vs QLFR (P_th=0.90), averaged over densities (same seeds/topologies)\n")
out.append("| Variant | ΔPDR | ΔDelay (s) | Lifetime ratio | Tx/packet ratio |\n|---|---|---|---|---|")
base = LABS[0]
for lab in LABS[1:]:
    dp, dd, lr, tr = [], [], [], []
    for s in range(10):
        dp.append(st.mean(float(D[(lab, n)][s]["pdr"]) - float(D[(base, n)][s]["pdr"]) for n in NODES))
        dd.append(st.mean(float(D[(lab, n)][s]["delay_s"]) - float(D[(base, n)][s]["delay_s"]) for n in NODES))
        lr.append(st.mean(float(D[(lab, n)][s]["lifetime_s"]) / float(D[(base, n)][s]["lifetime_s"]) for n in NODES))
        tr.append(st.mean(float(D[(lab, n)][s]["tx_per_pkt"]) / float(D[(base, n)][s]["tx_per_pkt"]) for n in NODES))
    out.append(f"| {lab} | {st.mean(dp):+.3f} ± {ci(dp):.3f} | {st.mean(dd):+.3f} ± {ci(dd):.3f} | "
               f"{st.mean(lr):.2f} ± {ci(lr):.2f} | {st.mean(tr):.2f} ± {ci(tr):.2f} |")
open("results/ablation_summary.md", "w").write("\n".join(out) + "\n")

COL = ["#6C757D", "#ADB5BD", "#56B4E9", "#0072B2", "#E69F00", "#D55E00", "#009E73"]
fig, axs = plt.subplots(1, 4, figsize=(16, 3.8))
for ax, (k, name, _) in zip(axs, METRICS[:3] + [METRICS[4]]):
    for lab, c in zip(LABS, COL):
        ax.errorbar(NODES, [st.mean(vals(lab, n, k)) for n in NODES], yerr=[ci(vals(lab, n, k)) for n in NODES],
                    label=lab, color=c, marker="o", ms=3, capsize=2, lw=2.2 if lab.startswith("DQ") else 1.2)
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel(name)
    ax.grid(alpha=0.3)
axs[0].legend(frameon=False, fontsize=7)
fig.tight_layout()
fig.savefig("figures/ablation.png", dpi=150)
print(open("results/ablation_summary.md").read())
