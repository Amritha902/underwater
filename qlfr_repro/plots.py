"""Make figures/*.png and results/summary.md from results/*.csv."""
import csv
import collections
import math
import os
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments import PROTOCOLS, LABELS, NODES

os.makedirs("figures", exist_ok=True)
COLORS = {"dbr": "#6C757D", "vbf": "#E69F00", "qlfr": "#0072B2", "dqevdr": "#009E73"}
MARK = {"dbr": "s", "vbf": "^", "qlfr": "o", "dqevdr": "D"}
T95 = {4: 2.776, 9: 2.262}


def ci(v):
    if len(v) < 2:
        return 0.0
    return T95.get(len(v) - 1, 1.96) * st.stdev(v) / math.sqrt(len(v))


rows = list(csv.DictReader(open("results/density.csv")))
agg = collections.defaultdict(list)
for r in rows:
    agg[(r["protocol"], int(r["nodes"]))].append(r)

METRICS = [("pdr", "Packet delivery ratio"), ("delay_s", "Average end-to-end delay (s)"),
           ("energy_per_pkt_j", "Energy per delivered packet (J)"), ("transmissions_per_pkt", "Transmissions per packet")]
for i, (k, lab) in enumerate(METRICS, 1):
    plt.figure(figsize=(5.2, 3.8))
    for p in PROTOCOLS:
        m = [st.mean(float(x[k]) for x in agg[(p, n)]) for n in NODES]
        e = [ci([float(x[k]) for x in agg[(p, n)]]) for n in NODES]
        plt.errorbar(NODES, m, yerr=e, label=LABELS[p], color=COLORS[p], marker=MARK[p], capsize=3, lw=1.6, ms=5)
    plt.xlabel("Number of sensor nodes")
    plt.ylabel(lab)
    if k in ("energy_per_pkt_j", "transmissions_per_pkt"):
        plt.yscale("log")
    plt.grid(alpha=0.3)
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(f"figures/fig{i}_{k}.png", dpi=160)
    plt.close()

life = collections.defaultdict(list)
for r in csv.DictReader(open("results/lifetime.csv")):
    life[r["protocol"]].append(float(r["packets_before_first_death"]))
plt.figure(figsize=(5.2, 3.8))
plt.bar([LABELS[p] for p in PROTOCOLS], [st.mean(life[p]) for p in PROTOCOLS],
        yerr=[ci(life[p]) for p in PROTOCOLS], color=[COLORS[p] for p in PROTOCOLS], capsize=4)
plt.ylabel("Packets generated before first node death")
plt.xticks(fontsize=8)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig5_lifetime.png", dpi=160)
plt.close()

learn = collections.defaultdict(list)
for r in csv.DictReader(open("results/learning.csv")):
    learn[(r["protocol"], int(r["window_end"]))].append(float(r["pdr"]))
wins = sorted({w for _, w in learn})
plt.figure(figsize=(5.2, 3.8))
for p in ("qlfr", "dqevdr"):
    m = [st.mean(learn[(p, w)]) for w in wins]
    e = [ci(learn[(p, w)]) for w in wins]
    plt.errorbar(wins, m, yerr=e, label=LABELS[p], color=COLORS[p], marker=MARK[p], capsize=3)
plt.xlabel("Packets generated (100-packet windows)")
plt.ylabel("Windowed packet delivery ratio")
plt.ylim(0.85, 1.0)
plt.grid(alpha=0.3)
plt.legend(frameon=False, fontsize=8)
plt.tight_layout()
plt.savefig("figures/fig6_learning.png", dpi=160)
plt.close()

# summary tables
out = ["# Results summary (mean ± 95% CI over 5 seeds)\n"]
for k, lab in METRICS:
    out.append(f"\n## {lab}\n\n| Nodes | " + " | ".join(LABELS[p] for p in PROTOCOLS) + " |")
    out.append("|---|" + "---|" * len(PROTOCOLS))
    for n in NODES:
        cells = []
        for p in PROTOCOLS:
            v = [float(x[k]) for x in agg[(p, n)]]
            cells.append(f"{st.mean(v):.3f} ± {ci(v):.3f}")
        out.append(f"| {n} | " + " | ".join(cells) + " |")
out.append("\n## Lifetime (packets generated before first node death, 300 nodes, 15 J batteries)\n")
out.append("| Protocol | Mean ± 95% CI |\n|---|---|")
for p in PROTOCOLS:
    out.append(f"| {LABELS[p]} | {st.mean(life[p]):.1f} ± {ci(life[p]):.1f} |")

# paired comparison DQ-EVDR vs QLFR (same seeds and topologies)
out.append("\n## Paired difference: DQ-EVDR minus QLFR (same topology/seed), mean ± 95% CI\n")
out.append("| Nodes | ΔPDR | ΔDelay (s) | ΔEnergy/pkt (J) |\n|---|---|---|---|")
for n in NODES:
    by = {p: {int(x["seed"]): x for x in agg[(p, n)]} for p in ("qlfr", "dqevdr")}
    cells = []
    for k in ("pdr", "delay_s", "energy_per_pkt_j"):
        d = [float(by["dqevdr"][s][k]) - float(by["qlfr"][s][k]) for s in by["qlfr"]]
        cells.append(f"{st.mean(d):+.3f} ± {ci(d):.3f}")
    out.append(f"| {n} | " + " | ".join(cells) + " |")
open("results/summary.md", "w").write("\n".join(out) + "\n")
print("ok")
