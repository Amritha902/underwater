"""Paper-vs-reimplementation figures (figures/paper_*.png) and tables (results/paper_comparison.md)."""
import collections
import csv
import math
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import paper_digitized as P

N = P.N
COL = {"dbr": "#6C757D", "eedbr": "#D55E00", "dvor": "#E69F00", "qlfr": "#0072B2", "dqevdr": "#009E73", "qelar": "#CC79A7"}
LAB = {"dbr": "DBR", "eedbr": "EEDBR", "dvor": "DVOR", "qlfr": "QLFR", "dqevdr": "DQ-EVDR (ours)", "qelar": "QELAR"}
rows = list(csv.DictReader(open("results/paper_runs.csv")))
D = collections.defaultdict(list)
for r in rows:
    D[(r["exp"] if r["exp"] != "fig6_8" else "base", r["protocol"], int(r["nodes"]), float(r["k"]), float(r["speed"]))].append(r)


def get(proto, n, metric, k=0.05, v=3.0, exp=None):
    keys = [exp] if exp else ["base", "fig10_12", "fig13_15"]
    for e in keys:
        if (e, proto, n, k, v) in D:
            return [float(x[metric]) for x in D[(e, proto, n, k, v)]]
    raise KeyError((proto, n, k, v))


def m(x):
    return st.mean(x)


def ci(x):
    return 2.776 * st.stdev(x) / math.sqrt(len(x)) if len(x) > 1 else 0


def panel(ax, title, ylabel):
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)


def sweep_fig(fname, title, metric, ylabel, paper, series, norm=None):
    """series: list of (label, color, proto, k, v, paper_key). norm: callable(paper/ours) normalization."""
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    for lab, col, proto, k, v, pk in series:
        pv = paper[pk]
        ours = [m(get(proto, n, metric, k, v)) for n in N]
        err = [ci(get(proto, n, metric, k, v)) for n in N]
        if norm:
            pb, ob = norm(paper, pk), norm("ours", (proto, k, v))
            pv = [x / pb for x in pv]
            ours, err = [x / ob for x in ours], [e / ob for e in err]
        axs[0].plot(N, pv, marker="o", color=col, label=lab)
        axs[1].errorbar(N, ours, yerr=err, marker="o", color=col, label=lab, capsize=2)
    panel(axs[0], f"Paper (digitised): {title}", ylabel)
    panel(axs[1], f"Ours: {title}", ylabel)
    for a in axs:
        a.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(f"figures/{fname}.png", dpi=150)
    plt.close(fig)


base_series = [(LAB[p], COL[p], p, 0.05, 3.0, p) for p in ("dbr", "eedbr", "dvor", "qlfr")]
sweep_fig("paper_fig6_delay", "average end-to-end delay (s)", "delay_s", "Delay (s)", P.FIG6_DELAY, base_series)
sweep_fig("paper_fig8_pdr", "packet delivery ratio", "pdr", "PDR", P.FIG8_PDR, base_series)
q100 = m(get("qlfr", 100, "lifetime_s"))
sweep_fig("paper_fig7_lifetime", "lifetime / QLFR at 100 nodes", "lifetime_s", "Lifetime / QLFR@100",
          P.FIG7_LIFETIME, base_series,
          norm=lambda src, key: P.FIG7_LIFETIME["qlfr"][0] if src is P.FIG7_LIFETIME else q100)
ks = [("k=0.01 s", "#0072B2", "qlfr", 0.01, 3.0, 0.01), ("k=0.05 s", "#D55E00", "qlfr", 0.05, 3.0, 0.05),
      ("k=0.1 s", "#E69F00", "qlfr", 0.1, 3.0, 0.1)]
sweep_fig("paper_fig10_delay_k", "delay vs k (s)", "delay_s", "Delay (s)", P.FIG10_DELAY_K, ks)
sweep_fig("paper_fig11_pdr_k", "PDR vs k", "pdr", "PDR", P.FIG11_PDR_K, ks)
e005 = m(get("qlfr", 100, "energy_j", 0.05, 3.0))
sweep_fig("paper_fig12_energy_k", "energy vs k (rel. to k=0.05, 100 nodes)", "energy_j", "Energy / ref",
          P.FIG12_ENERGY_K, ks, norm=lambda src, key: P.FIG12_ENERGY_K[0.05][0] if src is P.FIG12_ENERGY_K else e005)
vs = [("v=1 m/s", "#0072B2", "qlfr", 0.05, 1.0, 1.0), ("v=3 m/s", "#D55E00", "qlfr", 0.05, 3.0, 3.0),
      ("v=5 m/s", "#E69F00", "qlfr", 0.05, 5.0, 5.0)]
sweep_fig("paper_fig13_pdr_v", "PDR vs node speed", "pdr", "PDR", P.FIG13_PDR_V, vs)
sweep_fig("paper_fig14_delay_v", "delay vs node speed (s)", "delay_s", "Delay (s)", P.FIG14_DELAY_V, vs)
e_v3 = m(get("qlfr", 100, "energy_j", 0.05, 3.0))
sweep_fig("paper_fig15_energy_v", "energy vs speed (rel. to v=3, 100 nodes)", "energy_j", "Energy / ref",
          P.FIG15_ENERGY_V, vs, norm=lambda src, key: P.FIG15_ENERGY_V[3.0][0] if src is P.FIG15_ENERGY_V else e_v3)

# Fig. 9: QLFR / QELAR ratios
q9 = {met: [m(get("qlfr", n, met, 0.05, 1.0, "fig9")) / m(get("qelar", n, met, 0.05, 1.0, "fig9")) for n in (200, 250, 300)]
      for met in ("lifetime_s", "delay_s")}
fig, ax = plt.subplots(figsize=(6, 3.6))
xs = range(3)
ax.bar([x - 0.3 for x in xs], P.FIG9_QLFR_OVER_QELAR["lifetime"], 0.2, label="Paper: lifetime", color="#9ACD32")
ax.bar([x - 0.1 for x in xs], q9["lifetime_s"], 0.2, label="Ours: lifetime", color="#556B2F")
ax.bar([x + 0.1 for x in xs], P.FIG9_QLFR_OVER_QELAR["delay"], 0.2, label="Paper: delay", color="#87CEEB")
ax.bar([x + 0.3 for x in xs], q9["delay_s"], 0.2, label="Ours: delay", color="#1F4E79")
ax.axhline(1, color="k", lw=0.8)
ax.set_xticks(list(xs), ["200", "250", "300"])
ax.set_xlabel("Number of nodes")
ax.set_ylabel("QLFR / QELAR")
ax.legend(frameon=False, fontsize=8, ncol=2)
ax.set_title("Fig. 9: QLFR relative to QELAR (v = 1 m/s)", fontsize=10)
fig.tight_layout()
fig.savefig("figures/paper_fig9_qelar.png", dpi=150)
plt.close(fig)

# DQ-EVDR vs QLFR (paper setting)
fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
for ax, (met, lab) in zip(axs, [("pdr", "PDR"), ("delay_s", "Delay (s)"), ("lifetime_s", "Lifetime (s)")]):
    for p in ("qlfr", "dqevdr"):
        ax.errorbar(N, [m(get(p, n, met)) for n in N], yerr=[ci(get(p, n, met)) for n in N], marker="o",
                    color=COL[p], label=LAB[p], capsize=2)
    panel(ax, lab, lab)
    ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig("figures/paper_dqevdr_vs_qlfr.png", dpi=150)
plt.close(fig)

# ---- tables ----
out = ["# QLFR paper vs our re-implementation (numbers)\n",
       "Paper values are read by eye from the paper's figures (about ±2–5% of the axis range). Ours are means of 5 seeds.\n"]


def table(title, paper, series, metric, fmt="{:.3f}", scale=None):
    out.append(f"\n## {title}\n\n| Nodes | " + " | ".join(f"{s[0]} paper | {s[0]} ours" for s in series) + " |")
    out.append("|---|" + "---|---|" * len(series))
    for i, n in enumerate(N):
        cells = []
        for lab, _, proto, k, v, pk in series:
            pv = paper[pk][i]
            ov = m(get(proto, n, metric, k, v))
            if scale:
                pv, ov = pv / scale[0](pk), ov / scale[1](proto, k, v)
            cells += [fmt.format(pv), fmt.format(ov)]
        out.append(f"| {n} | " + " | ".join(cells) + " |")


table("Fig. 6: average end-to-end delay (s)", P.FIG6_DELAY, base_series, "delay_s")
table("Fig. 8: packet delivery ratio", P.FIG8_PDR, base_series, "pdr")
table("Fig. 7: network lifetime normalised to QLFR at 100 nodes", P.FIG7_LIFETIME, base_series, "lifetime_s", "{:.2f}",
      (lambda pk: P.FIG7_LIFETIME["qlfr"][0], lambda p, k, v: q100))
table("Fig. 10: delay vs k (s)", P.FIG10_DELAY_K, ks, "delay_s")
table("Fig. 11: PDR vs k", P.FIG11_PDR_K, ks, "pdr")
table("Fig. 12: total energy vs k, normalised to k=0.05 s at 100 nodes", P.FIG12_ENERGY_K, ks, "energy_j", "{:.2f}",
      (lambda pk: P.FIG12_ENERGY_K[0.05][0], lambda p, k, v: e005))
table("Fig. 13: PDR vs node speed", P.FIG13_PDR_V, vs, "pdr")
table("Fig. 14: delay vs node speed (s)", P.FIG14_DELAY_V, vs, "delay_s")
table("Fig. 15: total energy vs node speed, normalised to v=3 at 100 nodes", P.FIG15_ENERGY_V, vs, "energy_j", "{:.2f}",
      (lambda pk: P.FIG15_ENERGY_V[3.0][0], lambda p, k, v: e_v3))
out.append("\n## Fig. 9: QLFR / QELAR (v = 1 m/s)\n\n| Nodes | Lifetime paper | Lifetime ours | Delay paper | Delay ours |\n|---|---|---|---|---|")
for i, n in enumerate((200, 250, 300)):
    out.append(f"| {n} | {P.FIG9_QLFR_OVER_QELAR['lifetime'][i]:.2f} | {q9['lifetime_s'][i]:.2f} | "
               f"{P.FIG9_QLFR_OVER_QELAR['delay'][i]:.2f} | {q9['delay_s'][i]:.2f} |")
out.append("\n## Absolute values (ours, mean ± 95% CI): lifetime (s) and total energy (J), k=0.05 s, v=3 m/s\n")
out.append("| Nodes | " + " | ".join(f"{LAB[p]} lifetime" for p in ("dbr", "eedbr", "dvor", "qlfr", "dqevdr")) + " | QLFR energy |")
out.append("|---|" + "---|" * 6)
for n in N:
    out.append(f"| {n} | " + " | ".join(f"{m(get(p, n, 'lifetime_s')):.0f} ± {ci(get(p, n, 'lifetime_s')):.0f}"
                                        for p in ("dbr", "eedbr", "dvor", "qlfr", "dqevdr"))
               + f" | {m(get('qlfr', n, 'energy_j')):.0f} |")
out.append("\n## DQ-EVDR vs QLFR (paper setting), mean ± 95% CI\n\n| Nodes | PDR QLFR | PDR DQ-EVDR | Delay QLFR | Delay DQ-EVDR |\n|---|---|---|---|---|")
for n in N:
    out.append(f"| {n} | {m(get('qlfr', n, 'pdr')):.3f} ± {ci(get('qlfr', n, 'pdr')):.3f} | "
               f"{m(get('dqevdr', n, 'pdr')):.3f} ± {ci(get('dqevdr', n, 'pdr')):.3f} | "
               f"{m(get('qlfr', n, 'delay_s')):.3f} | {m(get('dqevdr', n, 'delay_s')):.3f} |")
open("results/paper_comparison.md", "w").write("\n".join(out) + "\n")
print("ok")
