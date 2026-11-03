# Base Paper Re-implementation: QLFR (Paper vs Ours)

**Date:** 1 Nov 2026. **Code:** `qlfr_repro/` (Python).

**Note:** the "paper" values in every comparison table were read by eye from the published plots (`qlfr_repro/paper_digitized.py`), with about ±2–5% of each axis range of reading error.

**Base paper:** Y. Zhou, T. Cao, W. Xiang, "Anypath Routing Protocol Design via Q-Learning for Underwater Sensor Networks," *IEEE Internet of Things Journal*, 8(10), 8173–8190, 2021. doi:10.1109/JIOT.2020.3042901. The re-implementation follows the arXiv:2002.09623v1 full text (16 pages, read in full).

## 1. Summary

| Paper figure | What it shows | Match |
|---|---|---|
| Fig. 6: end-to-end delay vs nodes | QLFR lowest; DBR falls with density | **Strong for QLFR's own values:** within 0.005–0.022 s of the paper at all 9 densities; DBR within 0.06 s. **The ordering does not match:** our DVOR approximation (0.40–0.51 s) is *below* QLFR at every density, so "QLFR lowest" is not reproduced. Our DVOR is approximate (Section 3) and EEDBR is 0.06–0.12 s off. *(Corrected in the 3 Nov audit, `07_audit_and_novelty.md`.)* |
| Fig. 10: delay vs k | Larger k gives longer delay | **Strong.** Same ordering; ours is within 0.005–0.04 s. |
| Fig. 14: delay vs node speed | Speed has little impact | **Good.** Within 0.05 s everywhere. v = 1 m/s is within 0.01 s at 200–500 nodes; v = 5 m/s runs 0.03–0.04 s higher. |
| Fig. 7: lifetime vs nodes | QLFR rises with density; DBR, EEDBR and DVOR fall | **Partial.** Same direction for QLFR, DBR and EEDBR. QLFR rises 1.36× (paper 2.36×). Our DVOR stays above QLFR up to 150 nodes. |
| Fig. 12: energy vs k | Smaller k uses more energy; energy grows with N | **Qualitative.** Same ordering and growth; our growth is steeper. |
| Fig. 15: energy vs speed | Energy rises slightly with speed | **Qualitative.** Same ordering; our rise is steeper. |
| Fig. 8: PDR vs nodes | QLFR about 2–3% below DBR, EEDBR and DVOR | **Partial.** QLFR is below DBR and EEDBR, but at 0.90 rather than 0.97. Section 6 explains why. |
| Fig. 11 / Fig. 13: PDR vs k and vs speed | Small differences | **Partial.** Ours is held at about 0.90 by the threshold parameter. |
| Fig. 9: QLFR vs QELAR | QLFR delay ≈ 0.73–0.78 × QELAR | **Delay matches** (0.73 vs paper 0.73–0.78). **Lifetime does not** (0.28–0.32 vs paper 0.80–0.92); our QELAR is an approximation. |

**Bottom line:** the core protocol (Q-values, priority list, holding time) reproduces the paper's delay results almost exactly, and the main lifetime trend. Remaining gaps trace to parameters the paper does not report (Section 4) and to baselines that could only be approximated without their own papers.

## 2. Implemented exactly as specified in the paper

| Component | Paper source | Implementation (`uwsim/paper_sim.py`) |
|---|---|---|
| Reward | Eq. (5)–(7): r = −c_e(s_i) − c_e(s_j) − c_d(s_i,s_j); c_e = 1 − e_res/e_ini; c_d = ½(1 − d(s_i,s_j)/\|d\|max) | `_qlfr_reward` (\|d\|max = R) |
| Q-update | Eq. (8): Q ← α[r + γV(s_j)] + (1 − α)Q, V = max Q, γ = 0.8 | `_update_q`, once per packet round for all neighbours (Alg. 1, line 10) |
| Priority list | Sec. IV-A, V-C: shallower neighbours sorted by descending Q, length L | `_priority_list` |
| Holding time | Eq. (15): τ(n) = k(n − 1), k ∈ {0.01, 0.05, 0.1} s | `_hold` |
| Overhearing suppression | Alg. 1, lines 4–13 | `_recv` / `_fire` |
| Multipath suppression | Sec. IV-D, Fig. 4: shorten L if sink PDR > P_th, otherwise lengthen | end of each round in `run` |
| Channel | Eq. (16)–(22): Urick A = l^κ a(f)^l, Thorp a(f), Rayleigh-averaged BPSK, p = (1 − p_e)^M | `link_success` |
| Energy and lifetime | Eq. (33)–(40): tx = Ψ_t·M/μ; every neighbour pays Ψ_r·M/μ per overheard packet; Γ_net = min_i e_ini·T_run/E_i | `_transmit`, `result` |
| Delay | Eq. (30): holding time + propagation (D/v0) | event times |
| Topology | Sec. VII-A, Table II: 500 m³ cube; 100–500 sensors; 5 sources at the bottom layer; 5 static sinks on the surface; random-walk mobility at v = 1–5 m/s; R = 150 m; v0 = 1500 m/s; Ψ_t = 2 W; Ψ_r = 0.5 W | `Sim.__init__`, `_move` |

## 3. Baselines

| Baseline | How implemented | Fidelity |
|---|---|---|
| DBR | Depth-greedy; holding time (2τ/δ)(R − Δd); suppression on overhearing (Yan et al., 2008) | Good |
| EEDBR | Shallower forwarders; holding time increases as residual energy falls, plus a propagation term | **Approximate:** EEDBR paper not available, built from QLFR's description |
| DVOR | Hop counts to the nearest sink by query flooding; forward if hop count decreases; hop-based holding time | **Approximate:** DVOR paper not available |
| QELAR | Q-learning with r = −g − a1[c(s)+c(s_j)] + a2[d(s)+d(s_j)], link-aware Q, single next hop, up to 3 retransmissions | **Approximate:** QELAR paper not available; constants assumed |

## 4. Parameters the paper does not report (assumed or calibrated)

| Parameter | Value used | How chosen |
|---|---|---|
| Learning rate α | 0.5 | Assumed |
| Packet size M, data rate μ | 500 bits, 10 kbit/s | Assumed |
| Frequency f, spreading factor κ, Eb/N0 | 10 kHz, 1.5, 63 dB | Chosen so link success is 0.98 at 50 m, 0.94 at 100 m and 0.89 at 150 m |
| Initial energy e_ini | 1000 J | Assumed. The paper's lifetime formula (Eq. 39–40) is used, so no node dies mid-run. |
| Traffic | 100 rounds × 5 sources (500 packets), 10 s per round | Assumed |
| Initial list length L, cap | 3, 8 | Assumed |
| P_th (multipath suppression threshold) | 0.90 | **Calibrated:** best match of the lifetime trend (Section 6) |

## 5. Figures (paper vs ours)

All in `qlfr_repro/figures/`. Each figure shows the paper on the left (values read by eye from the PDF) and ours on the right (mean ± 95% CI over 5 seeds).

| Figure file | Reproduces |
|---|---|
| `paper_fig6_delay.png` | Fig. 6 |
| `paper_fig7_lifetime.png` | Fig. 7 (normalised to QLFR at 100 nodes, because absolute units depend on unreported energy/traffic) |
| `paper_fig8_pdr.png` | Fig. 8 |
| `paper_fig9_qelar.png` | Fig. 9 |
| `paper_fig10_delay_k.png` | Fig. 10 |
| `paper_fig11_pdr_k.png` | Fig. 11 |
| `paper_fig12_energy_k.png` | Fig. 12 (normalised) |
| `paper_fig13_pdr_v.png` | Fig. 13 |
| `paper_fig14_delay_v.png` | Fig. 14 |
| `paper_fig15_energy_v.png` | Fig. 15 (normalised) |
| `paper_dqevdr_vs_qlfr.png` | Our extension vs QLFR |

## 6. Numbers

The full paper-vs-ours tables for every figure are in `qlfr_repro/results/paper_comparison.md`. Key rows follow.

### Fig. 6: delay (s), k = 0.05 s, v = 3 m/s

| Nodes | DBR paper | DBR ours | QLFR paper | QLFR ours | Diff (QLFR) |
|---|---|---|---|---|---|
| 100 | 0.720 | 0.779 | 0.510 | 0.515 | +0.005 |
| 200 | 0.620 | 0.610 | 0.455 | 0.472 | +0.017 |
| 300 | 0.560 | 0.565 | 0.445 | 0.463 | +0.018 |
| 400 | 0.540 | 0.525 | 0.445 | 0.452 | +0.007 |
| 500 | 0.510 | 0.497 | 0.440 | 0.461 | +0.021 |

### Fig. 10: QLFR delay (s) vs k

| Nodes | k=0.01 paper | ours | k=0.05 paper | ours | k=0.1 paper | ours |
|---|---|---|---|---|---|---|
| 100 | 0.450 | 0.455 | 0.510 | 0.515 | 0.530 | 0.538 |
| 300 | 0.405 | 0.424 | 0.440 | 0.463 | 0.475 | 0.491 |
| 500 | 0.400 | 0.418 | 0.440 | 0.461 | 0.475 | 0.497 |

### Fig. 7: lifetime normalised to QLFR at 100 nodes

| Nodes | DBR paper | DBR ours | QLFR paper | QLFR ours | QLFR/DBR paper | QLFR/DBR ours |
|---|---|---|---|---|---|---|
| 100 | 0.86 | 0.76 | 1.00 | 1.00 | 1.16 | 1.32 |
| 300 | 0.32 | 0.21 | 2.11 | 1.17 | 6.7 | 5.7 |
| 500 | 0.20 | 0.13 | 2.36 | 1.36 | 11.8 | 10.1 |

Absolute values (ours): QLFR rises from 11,308 s to 15,394 s; DBR falls from 8,550 s to 1,526 s (100 → 500 nodes).

### Fig. 8: PDR

| Nodes | DBR paper | DBR ours | QLFR paper | QLFR ours |
|---|---|---|---|---|
| 100 | 0.885 | 0.912 | 0.905 | 0.898 |
| 300 | 1.000 | 1.000 | 0.973 | 0.901 |
| 500 | 1.000 | 1.000 | 0.970 | 0.902 |

### Why QLFR's PDR is 0.90, not 0.97 (P_th sensitivity, `results/paper_pth_sensitivity.md`)

| P_th | Nodes | PDR | Delay (s) | Lifetime (s) |
|---|---|---|---|---|
| 0.90 | 100 / 300 / 500 | 0.897 / 0.901 / 0.900 | 0.504 / 0.455 / 0.466 | 10,614 / 13,827 / 15,786 |
| 0.97 | 100 / 300 / 500 | 0.931 / 0.967 / 0.970 | 0.498 / 0.459 / 0.472 | 9,299 / 6,985 / 5,985 |

- QLFR's multipath suppression drives the delivery ratio towards P_th. With P_th = 0.97, our PDR **matches the paper's 0.97** and delay is unchanged, but lifetime then falls with density.
- No single P_th reproduces both the paper's PDR and its rising lifetime. This points to other unreported settings that change the energy balance: traffic load, packet duration, battery size and the initial list length.
- We chose P_th = 0.90 to reproduce the paper's central lifetime claim.

### Fig. 9: QLFR / QELAR (v = 1 m/s)

| Nodes | Lifetime paper | Lifetime ours | Delay paper | Delay ours |
|---|---|---|---|---|
| 200 | 0.80 | 0.28 | 0.78 | 0.73 |
| 250 | 0.85 | 0.32 | 0.74 | 0.73 |
| 300 | 0.92 | 0.31 | 0.73 | 0.73 |

## 7. Our extension in the paper's setting (DQ-EVDR vs QLFR)

DQ-EVDR adds three things to QLFR:
1. A link-quality cost learned from noisy hello receptions.
2. A void-node cost.
3. Double Q-learning.

| Nodes | PDR QLFR | PDR DQ-EVDR | Delay QLFR (s) | Delay DQ-EVDR (s) | Lifetime QLFR (s) | Lifetime DQ-EVDR (s) |
|---|---|---|---|---|---|---|
| 100 | 0.898 ± 0.007 | 0.894 ± 0.021 | 0.515 | 0.542 | 11,308 | 10,626 |
| 300 | 0.901 ± 0.004 | 0.902 ± 0.004 | 0.463 | 0.523 | 13,244 | 8,941 |
| 500 | 0.902 ± 0.004 | 0.900 ± 0.001 | 0.461 | 0.526 | 15,394 | 8,880 |

In this setting DQ-EVDR is **worse** than QLFR: delay is about 0.06 s higher, and lifetime is up to 42% lower at high density, while PDR is the same. This is an honest negative result for the first design. `02_brainstorming.md` analyses the causes and the redesign.

## 8. Reproduce

```bash
cd qlfr_repro
pip install numpy matplotlib pytest
python3 -m pytest -q tests          # 9 tests
python3 paper_experiments.py        # 435 runs, about 8 min on 4 cores
python3 paper_plots.py              # figures/paper_*.png and results/paper_comparison.md
python3 paper_sensitivity.py        # P_th sensitivity
```

The earlier abstract-only prototype (`uwsim/network.py`, `experiments.py`, `plots.py`; 1000 m³ setting) is kept for reference but has been superseded by this report.
