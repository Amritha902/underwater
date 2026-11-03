# Final Protocol: LAQR (Link-Aware Adaptive-List Q-Learning Routing)

**Date:** 1 Nov 2026. **Code:** `qlfr_repro/uwsim/paper_sim.py`, protocol variant `lq_al` with `lq_beta = 0.05`, `rho = 0.99`. **Evaluation:** `final_eval.py`, `final_report.py`, `confirm_final.py`. **Tables:** `qlfr_repro/results/final_summary.md`. **Figure:** `qlfr_repro/figures/final_protocol.png`.

## 1. Protocol specification

LAQR keeps QLFR's Q-learning and holding-time machinery (Zhou, Cao, Xiang, IEEE IoTJ 2021) and replaces its global multipath-suppression scheme with link-aware, per-hop candidate sets.

| Step | QLFR (base paper) | LAQR (ours) |
|---|---|---|
| Routing knowledge in each header | V, depth, residual energy, sender ID | Same, **plus a per-node transmission sequence number** |
| Link-quality estimate | none | Receiver-side, ETX-style: p̂_ij ← p̂_ij + β(x − p̂_ij) for each heard packet (x = 1) and each gap in j's sequence numbers (x = 0, at most 5 per gap). β = 0.05, prior 0.9; links assumed symmetric; reset when j leaves range. |
| Reward | r = −c_e(s_i) − c_e(s_j) − c_d(s_i,s_j) (Eq. 5–7) | r = −c_e(s_i) − c_e(s_j) − c_d(s_i,s_j) − w_lq·(1 − p̂_ij), w_lq = 0.25 |
| Q-update | Eq. (8): Q ← α[r + γV] + (1 − α)Q, V = max Q | Same (single estimator); α = 0.5, γ = 0.8 |
| Candidate set | Shallower neighbours by descending Q; global length L adapted from end-to-end PDR vs P_th | Shallower neighbours by descending Q; **per-hop length L_i = smallest L with 1 − Π_{n≤L}(1 − p̂_{i,n}) ≥ ρ**, ρ = 0.99, capped at 8 |
| Holding time | τ(n) = k(n − 1) (Eq. 15) | Same |
| Overhearing suppression | Alg. 1 | Same |

**Overhead:** one sequence number per header. There are no extra control packets and no global feedback loop.

### Pseudocode (per sender s_i, per packet)

```
neighbours  <- shallower neighbours of s_i
for each s_j in neighbours:
    Q(s_i,s_j) <- alpha*[ -c_e(i) - c_e(j) - c_d(i,j) - w_lq*(1 - p_hat(i,j)) + gamma*V(j) ] + (1-alpha)*Q(s_i,s_j)
list <- neighbours sorted by Q, descending
L    <- smallest L such that 1 - prod_{n<=L} (1 - p_hat(i, list[n])) >= rho
broadcast packet with header {V(i), depth, e_res, id, seq_i++, list[1..L]}
on receiving any packet from s_j: update p_hat(i,j) from s_j's sequence-number gap
```

## 2. How the final design was reached

| Step | Evidence | Decision |
|---|---|---|
| Base-paper reproduction | QLFR delay matches the paper within 0.005–0.022 s (`01_base_paper_reimplementation.md`) | Use the faithful QLFR as the base |
| DQ-EVDR v2 ablation, paper channel (`03_…`) | Adaptive lists (AL) give the main gain. Double Q (DQ) adds delay and cuts lifetime. The trap penalty is not significant. | Keep LQ + AL |
| Harsh-channel ablation (`04_…`) | DQ's gain under noise equals the gain from slower estimator smoothing. A single estimator with lower β matches or beats it. | Drop DQ; tune β |
| Tuning on seeds 100–104 (`results/tune_final.md`) | Pre-registered rule: ΔPDR ≥ −0.005 vs QLFR on σ = 0/4/8 dB, then maximise lifetime. Selected β = 0.05, ρ = 0.98; the trap penalty was not selected. | Candidate ρ = 0.98 |
| Evaluation on seeds 0–9 | **ρ = 0.98 violated the PDR rule at σ = 8 dB** (−0.020 ± 0.010) | Revised to the runner-up, ρ = 0.99 |
| Confirmation on fresh seeds 200–209 | ρ = 0.99 meets the rule on all channels | **Final: β = 0.05, ρ = 0.99** |

The revision is reported openly. ρ = 0.99 was chosen after seeing the evaluation-seed results, so it was re-tested on seeds 200–209, which no earlier step had used.

## 3. Results

### 3.1 Confirmation on fresh seeds 200–209 (100–500 nodes, paired, mean ± 95% CI)

| σ (dB) | Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio |
|---|---|---|---|---|---|
| 0 | QLFR (P_th = 0.90) | **+0.069 ± 0.009** | +0.001 ± 0.002 | **1.47 ± 0.06** | 0.71 ± 0.03 |
| 0 | QLFR (P_th = 0.97) | +0.010 ± 0.011 | −0.001 ± 0.003 | **2.68 ± 0.09** | 0.39 ± 0.01 |
| 4 | QLFR (P_th = 0.90) | **+0.052 ± 0.009** | +0.003 ± 0.004 | **1.70 ± 0.10** | 0.62 ± 0.02 |
| 4 | QLFR (P_th = 0.97) | −0.012 ± 0.012 | −0.001 ± 0.002 | **2.93 ± 0.17** | 0.35 ± 0.01 |
| 8 | QLFR (P_th = 0.90) | +0.009 ± 0.016 | −0.001 ± 0.005 | **2.19 ± 0.08** | 0.48 ± 0.02 |
| 8 | QLFR (P_th = 0.97) | −0.049 ± 0.018 | −0.006 ± 0.006 | **3.51 ± 0.14** | 0.31 ± 0.01 |

### 3.2 Evaluation seeds 0–9 (absolute values; LAQR is the "LAQR-HR (rho=0.99)" row in `final_summary.md`)

| σ (dB) | Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|---|
| 0 | QLFR (P_th = 0.90) | 0.900 | 0.469 | 13,865 | 8,065 | 25.0 |
| 0 | QLFR (P_th = 0.97) | 0.965 | 0.473 | 7,297 | 16,122 | 48.4 |
| 0 | DQ-EVDR v2 | 0.967 | 0.487 | 18,156 | 6,406 | 18.2 |
| 0 | **LAQR** | **0.973** | 0.472 | **19,482** | **5,950** | **17.2** |
| 4 | QLFR (P_th = 0.90) | 0.896 | 0.482 | 12,148 | 9,032 | 28.1 |
| 4 | QLFR (P_th = 0.97) | 0.958 | 0.487 | 7,012 | 16,643 | 49.2 |
| 4 | DQ-EVDR v2 | 0.947 | 0.501 | 19,030 | 6,269 | 17.9 |
| 4 | **LAQR** | **0.953** | 0.483 | **20,505** | **5,689** | **16.5** |
| 8 | QLFR (P_th = 0.90) | 0.895 | 0.510 | 10,298 | 10,779 | 33.0 |
| 8 | QLFR (P_th = 0.97) | 0.958 | 0.514 | 6,758 | 17,834 | 52.1 |
| 8 | DQ-EVDR v2 | 0.904 | 0.531 | 20,854 | 5,758 | 16.7 |
| 8 | **LAQR** | 0.899 | 0.510 | **22,979** | **5,075** | **15.0** |

### 3.3 Supportable claims

1. **Against QLFR at its calibrated setting:** LAQR delivers +5–7 points more packets on normal and moderately shadowed channels and lasts 1.5–1.7× longer. Under heavy shadowing it lasts 2.2× longer at equal delivery. Delay is unchanged on every channel (all |ΔDelay| ≤ 0.006 s).
2. **Against QLFR tuned for high delivery (P_th = 0.97):** LAQR lasts 2.7–3.5× longer on 31–39% of the energy. Delivery is equal on the paper's channel. It is lower under shadowing: −0.012 ± 0.012 (not significant) at σ = 4 dB and −0.049 ± 0.018 at σ = 8 dB.
3. **Against our earlier DQ-EVDR v2:** LAQR is simpler (one estimator, no trap term) and better. It has lower delay (−0.015 to −0.021 s), longer lifetime, and equal or higher delivery at σ = 0 and 4 dB.

### 3.4 Limitations (state these in the paper)

- **Sparse networks under heavy shadowing:** at 100 nodes and σ = 8 dB, LAQR delivers about 0.81 against QLFR's 0.87 (see the figure). Per-hop reliability cannot compensate when few candidates exist. A fallback to a longer list when the candidate set is small is a natural fix and future work.
- Simulation is in Python with no MAC collisions. Several QLFR parameters the paper doesn't report are assumed or calibrated (`01_…`, Section 4). EEDBR, DVOR and QELAR are approximations.
- Shadowing is our own stress model, not part of the QLFR paper.
- **ns-3 validation (done, `06_ns3_port.md`):** over ns-3's UAN stack with an ALOHA MAC, LAQR beats QLFR on delivery (+0.081), delay (−0.44 s) and lifetime (1.24×) when sources are desynchronised. When all sources transmit within 0.5 s, it loses delivery (−0.34): beacon-based p̂ misses correlated data-time collisions. Next: repeat with a collision-avoiding MAC and on Aqua-Sim FG.

## 4. Proposed paper framing

**Title idea:** *Link-Aware Adaptive Candidate Sets for Q-Learning Anypath Routing in Underwater Acoustic Sensor Networks.*

**Contributions:**
1. A faithful, open re-implementation of QLFR that reproduces its delay results.
2. LAQR: ETX-style link learning from sequence numbers, plus per-hop adaptive candidate sets in place of QLFR's global multipath suppression.
3. An ablation showing that Double Q-learning's apparent benefit under noisy links comes from estimator smoothing rather than reduced overestimation, a negative result useful to the community.
4. An evaluation across the paper's channel and log-normal shadowing.
