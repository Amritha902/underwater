"""Summarise ns3_port/results/ns3_eval.csv: per-scenario means and paired LAQR - QLFR differences."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        19: 2.093, 29: 2.045, 49: 2.010}
HERE = Path(__file__).resolve().parent
TAG = sys.argv[1] if len(sys.argv) > 1 else ""
SUF = f"_{TAG}" if TAG else ""
df = pd.read_csv(HERE / "results" / f"ns3_eval{SUF}.csv")
METRICS = ["pdr", "delay", "lifetime", "energy_used", "tx_per_pkt"]
NAMES = {"qlfr": "QLFR (P_th = 0.90)", "qlfr97": "QLFR (P_th = 0.97)", "laqr": "LAQR"}


def ci(x):
    x = np.asarray(x, float)
    if len(x) < 2:
        return float("nan")
    return T975.get(len(x) - 1, 1.96) * x.std(ddof=1) / np.sqrt(len(x))


out = [f"# ns-3 evaluation: QLFR vs LAQR (MAC: {'UanMacCw' if TAG == 'cw' else 'UanMacAloha'})", "",
       f"Runs: {len(df)} ({df.seed.nunique()} seeds x {df.nodes.nunique()} densities x "
       f"{df.protocol.nunique()} protocols x {df.scenario.nunique()} scenarios). Mean +/- 95% CI over seeds.", ""]
for sc, g in df.groupby("scenario", sort=False):
    out += [f"## Scenario: {sc}", "", "### Averaged over densities", "",
            "| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |", "|---|---|---|---|---|---|"]
    for p in ["qlfr", "qlfr97", "laqr"]:
        s = g[g.protocol == p].groupby("seed")[METRICS].mean()
        out.append(f"| {NAMES[p]} | " + " | ".join(
            f"{s[m].mean():.3f} ± {ci(s[m]):.3f}" if m in ("pdr", "delay") else f"{s[m].mean():,.0f} ± {ci(s[m]):,.0f}"
            if m != "tx_per_pkt" else f"{s[m].mean():.1f} ± {ci(s[m]):.1f}" for m in METRICS) + " |")
    out += ["", "### Per density (mean PDR / delay / lifetime)", "",
            "| Nodes | " + " | ".join(NAMES[p] for p in ["qlfr", "qlfr97", "laqr"]) + " |", "|---|---|---|---|"]
    for n, h in g.groupby("nodes"):
        cells = []
        for p in ["qlfr", "qlfr97", "laqr"]:
            s = h[h.protocol == p]
            cells.append(f"{s.pdr.mean():.3f} / {s.delay.mean():.2f} s / {s.lifetime.mean():,.0f} s")
        out.append(f"| {n} | " + " | ".join(cells) + " |")
    out += ["", "### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)", "",
            "| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |", "|---|---|---|---|---|---|"]
    L = g[g.protocol == "laqr"].set_index(["nodes", "seed"])
    for b in ["qlfr", "qlfr97"]:
        B = g[g.protocol == b].set_index(["nodes", "seed"])
        j = L.join(B, lsuffix="_l", rsuffix="_b", how="inner")
        per = j.groupby(level="seed").apply(lambda x: pd.Series({
            "dpdr": (x.pdr_l - x.pdr_b).mean(), "dd": (x.delay_l - x.delay_b).mean(),
            "lr": (x.lifetime_l / x.lifetime_b).mean(), "er": (x.energy_used_l / x.energy_used_b).mean(),
            "tr": (x.tx_per_pkt_l / x.tx_per_pkt_b).mean()}))
        out.append(f"| {NAMES[b]} | {per.dpdr.mean():+.3f} ± {ci(per.dpdr):.3f} | {per.dd.mean():+.3f} ± {ci(per.dd):.3f} | "
                   f"{per.lr.mean():.2f} ± {ci(per.lr):.2f} | {per.er.mean():.2f} ± {ci(per.er):.2f} | "
                   f"{per.tr.mean():.2f} ± {ci(per.tr):.2f} |")
    out.append("")
text = "\n".join(out)
(HERE / "results" / f"ns3_summary{SUF}.md").write_text(text + "\n")
print(text)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 3, figsize=(13, 7), sharex=True)
    for r, sc in enumerate(df.scenario.unique()):
        g = df[df.scenario == sc]
        for c, (m, lab) in enumerate([("pdr", "PDR"), ("delay", "Delay (s)"), ("lifetime", "Lifetime (s)")]):
            for p, mk in [("qlfr", "o-"), ("qlfr97", "s--"), ("laqr", "^-")]:
                s = g[g.protocol == p].groupby("nodes")[m]
                mu, e = s.mean(), s.apply(ci)
                ax[r, c].errorbar(mu.index, mu.values, yerr=e.values, fmt=mk, capsize=3, label=NAMES[p])
            ax[r, c].set_title(f"{lab} ({sc} sources)")
            ax[r, c].grid(alpha=0.3)
            if r == 1:
                ax[r, c].set_xlabel("Number of nodes")
    ax[0, 0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "results" / f"ns3_eval{SUF}.png", dpi=130)
except Exception as e:  # plotting is optional
    print("plot skipped:", e, file=sys.stderr)
