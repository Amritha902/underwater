# Base-Paper Re-implementation Report: QLFR

**Date:** 31 Oct 2026. **Code:** `qlfr_repro/` (Python; `python3 experiments.py && python3 plots.py` regenerates everything).

## 1. Base paper chosen

Y. Zhou, T. Cao, W. Xiang, "Anypath Routing Protocol Design via Q-Learning for Underwater Sensor Networks," *IEEE Internet of Things Journal*, vol. 8, no. 10, pp. 8173–8190, 2021. doi:10.1109/JIOT.2020.3042901. Preprint: arXiv:2002.09623.

**Why this paper:**
- It has the highest relevance score (95%) in our 50-paper survey, tied with QTRU (EAAI 2025).
- It uses depth- and energy-related rewards, a ranked forwarding-candidate set and priority-based holding times: exactly the building blocks of our DQ-EVDR.
- Its full text is open on arXiv, so its equations and figures can be matched. QTRU is more recent but paywalled.
- None of the 50 surveyed papers publishes Python code, so a re-implementation from the paper's description was required in every case.

## 2. What could and could not be verified

| Item | Status |
|---|---|
| Protocol design elements (from the abstract): Q-learning; depth- and energy-related rewards; anypath candidate set; holding time set by candidate priority; overhearing suppression; localization-free (depth only) | Implemented |
| Exact reward equations, weights, holding-time formula constants | **Not available.** arxiv.org is blocked in this environment, and web search returns only the abstract and section headings. Our own documented choices were used (Section 4). |
| Paper's simulation parameters (area, node counts, range, energy, packet size) | **Not available.** Documented assumptions were used (Section 4). |
| Paper's figures and numerical results | **Not available.** No paper numbers are reproduced or invented here. Section 7 is a ready table to fill in. |
| Paper's qualitative claims: QLFR "reduces end-to-end delay" and "extends network lifetime" against baselines | **Checked against our results** (Section 6) |

To finish the numeric match, allow `arxiv.org` in the environment's network settings or upload the PDF. Then:
1. Copy the paper's parameters into `uwsim/config.py`.
2. Replace the reward and holding-time functions with the paper's equations (`_reward`, `_q`, `_holding_time` in `uwsim/network.py`).
3. Re-run the two scripts and fill in Section 7.

## 3. What was implemented

| Module | Contents |
|---|---|
| `uwsim/channel.py` | Thorp absorption (dB/km), spreading loss with k = 1.5, sound speed 1500 m/s. Hand-checked: 1.187 dB/km at 10 kHz and 6.105 dB/km at 25 kHz. |
| `uwsim/phy.py` | SNR = SL − TL − NL; BPSK bit error rate; packet success = (1 − BER)^bits |
| `uwsim/energy.py`, `topology.py`, `engine.py`, `metrics.py` | Battery model, random 3-D deployment with sinks on the surface, discrete-event engine, metrics |
| `uwsim/network.py` | The four protocols below |

| Protocol | Implementation |
|---|---|
| **DBR** (Yan et al., 2008) | A receiver forwards if it is shallower than the sender. Holding time = (2τ/δ)(R − Δd), with τ = R/c and δ = R. A held copy is cancelled when a shallower forwarder is overheard. |
| **VBF** (Xie et al., 2006) | Forward only inside a pipe of radius W = 150 m around the source-to-sink vector. Desirableness α = p/W + (R − d·cosθ)/R. Holding time = √α·T + (R − d)/c. |
| **QLFR** (base paper, abstract-level) | **Reward:** r = −1 + w_d·Δdepth/R + w_e·(E_res/E_0 − 1), i.e. a depth term plus an energy term. **Q-value:** Q_s(j) = r + γ[P̂_sj·V_j + (1 − P̂_sj)(V_s − c_fail)]. **Advertised value:** V_s = max_j Q_s(j). **Candidates:** the top-3 by Q, with holding time = rank × slot; lower-ranked copies are suppressed on overhearing. **Learning:** link success P̂ and neighbour values V are learned from implicit acknowledgements (overhearing the next hop). |
| **DQ-EVDR** (ours) | The same machinery, plus two changes: **(i) Double Q-learning:** two independent estimators; each sample updates one at random; V_s = ½[Q^B(argmax Q^A) + Q^A(argmax Q^B)]. **(ii) Void penalty:** a candidate with no shallower neighbour is penalised in the reward. |

**Simplifications** (applied equally to all protocols):
- No MAC collisions.
- Idle energy is ignored.
- Sinks acknowledge receptions reliably.
- Up to 2 retransmissions for the Q-learning protocols.

**Tests:** 8 unit tests pass (`python3 -m pytest -q tests`). They cover the channel values, battery, topology symmetry, event order, delivery for every protocol, and determinism given a seed.

## 4. Simulation parameters (documented assumptions)

| Parameter | Value |
|---|---|
| Area | 1000 × 1000 × 1000 m |
| Sinks | 9 (random, at the surface) |
| Sensors | 100, 150, 200, 250, 300, 400, 500 |
| Communication range R | 250 m |
| Frequency | 25 kHz |
| Source level / noise level | 95 dB / 50 dB (link success: 0.98 at 200 m, 0.73 at 250 m) |
| Packet | 800 bits at 16 kbit/s (0.05 s) |
| Tx / Rx power | 2 W / 0.1 W |
| Initial energy | 100 J (15 J in the lifetime test) |
| Traffic | 400 packets, one every 20 s from a random sensor |
| Q-learning | α = 0.5, γ = 0.9, w_d = w_e = 1, hop cost = 1, failure penalty = 2, sink value = 5, 3 candidates |
| DQ-EVDR void penalty | 3 |
| Seeds | 5 per point; error bars are 95% confidence intervals (t-distribution) |

## 5. Figures (produced by our code)

| Figure | Content |
|---|---|
| `qlfr_repro/figures/fig1_pdr.png` | Packet delivery ratio vs node count |
| `qlfr_repro/figures/fig2_delay_s.png` | Average end-to-end delay vs node count |
| `qlfr_repro/figures/fig3_energy_per_pkt_j.png` | Energy per delivered packet (log scale) |
| `qlfr_repro/figures/fig4_transmissions_per_pkt.png` | Transmissions per generated packet (log scale) |
| `qlfr_repro/figures/fig5_lifetime.png` | Packets generated before the first node dies (300 nodes, 15 J) |
| `qlfr_repro/figures/fig6_learning.png` | Learning curve: windowed delivery ratio, QLFR vs DQ-EVDR |

## 6. Results and check against QLFR's claims

### 6.1 Packet delivery ratio (mean ± 95% CI)

| Nodes | DBR | VBF | QLFR | DQ-EVDR |
|---|---|---|---|---|
| 100 | 0.745 ± 0.180 | 0.326 ± 0.104 | 0.766 ± 0.187 | 0.747 ± 0.186 |
| 150 | 0.880 ± 0.040 | 0.531 ± 0.110 | 0.901 ± 0.039 | 0.883 ± 0.039 |
| 200 | 0.957 ± 0.031 | 0.620 ± 0.109 | 0.960 ± 0.040 | 0.959 ± 0.036 |
| 300 | 0.982 ± 0.021 | 0.847 ± 0.038 | 0.981 ± 0.026 | 0.974 ± 0.033 |
| 500 | 0.992 | 0.962 | 0.986 | 0.990 |

The full tables for all densities and metrics are in `qlfr_repro/results/summary.md`.

### 6.2 Delay, energy and transmissions (means; see summary.md for CIs)

| Nodes | Delay (s): DBR / QLFR | Energy per packet (J): DBR / QLFR | Transmissions per packet: DBR / QLFR |
|---|---|---|---|
| 100 | 1.095 / 0.885 | 2.64 / 1.53 | 15.6 / 9.2 |
| 300 | 0.826 / 0.789 | 14.20 / 2.71 | 80.5 / 15.7 |
| 500 | 0.752 / 0.742 | 27.89 / 2.46 | 128.0 / 11.7 |

### 6.3 Lifetime (300 nodes, 15 J batteries)

| Protocol | Packets before first node death |
|---|---|
| DBR | 103.2 ± 6.7 |
| VBF | 536.4 ± 166.1 |
| QLFR | 191.8 ± 52.6 |
| DQ-EVDR | 189.6 ± 68.6 |

### 6.4 Trend check against the paper's stated claims

| QLFR claim (from abstract) | Our re-implementation | Consistent? |
|---|---|---|
| Reduces end-to-end delay compared with baseline routing | QLFR's delay is lower than DBR's at all 7 densities (e.g. 0.885 vs 1.095 s at 100 nodes) | Yes vs DBR. VBF has lower delay only at 100 nodes, where it delivers just 33% of packets. |
| Extends network lifetime | QLFR survives 1.86× longer than DBR (191.8 vs 103.2 packets); it uses 5–11× less energy per packet at 300–500 nodes | Yes vs DBR. VBF lasts longer because it forwards far less, but at a much lower delivery ratio (0.33–0.96). |
| Keeps delivery high with only depth information | QLFR's delivery ratio is within the confidence interval of DBR (flooding-like) at every density | Yes |

**Conclusion:**
- Our Python re-implementation reproduces the *qualitative* behaviour QLFR claims.
- *Numeric* agreement with the paper's figures cannot be shown until the full text is accessible (Section 7).

### 6.5 First result for our proposal (DQ-EVDR vs QLFR, paired by seed)

| Nodes | ΔPDR | ΔDelay (s) | ΔEnergy per packet (J) |
|---|---|---|---|
| 100 | −0.019 ± 0.034 | −0.006 ± 0.072 | −0.013 ± 0.191 |
| 150 | −0.018 ± 0.016 | −0.033 ± 0.061 | −0.085 ± 0.227 |
| 250 | +0.004 ± 0.010 | −0.031 ± 0.034 | −0.043 ± 0.455 |
| 500 | +0.004 ± 0.014 | −0.014 ± 0.031 | −0.136 ± 0.412 |

**Reading this table:**
- In this first setting, DQ-EVDR is **not significantly different** from QLFR: every confidence interval contains 0.
- The one exception is a small, significant PDR loss at 150 nodes (−0.018 ± 0.016).
- Delay is lower in 6 of 7 densities, but never significantly.
- This is an honest negative first result. The brainstorming document explains why it happens and what to change.

## 7. Numeric comparison with the paper (fill in when the full text is available)

| Paper figure / table | Metric | Paper value | Our value (same parameters) | Difference |
|---|---|---|---|---|
| (paper Fig. ?) | End-to-end delay vs nodes | — | — | — |
| (paper Fig. ?) | Network lifetime | — | — | — |
| (paper Fig. ?) | Energy consumption | — | — | — |
| (paper Fig. ?) | Packet delivery ratio | — | — | — |

## 8. Reproduce

```bash
cd qlfr_repro
pip install numpy matplotlib pytest
python3 -m pytest -q tests
python3 experiments.py
python3 plots.py
```

The density sweep takes about 1 minute on 4 cores; the lifetime and learning runs take about 15 s.
