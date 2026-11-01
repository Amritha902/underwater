# DQ-EVDR v2: Implementation and Ablation

**Date:** 1 Nov 2026. **Code:** `qlfr_repro/uwsim/paper_sim.py` (variants in `V2_VARIANTS`), `ablation.py`, `ablation_report.py`, `tune_v2.py`.
**Setting:** the QLFR paper's own (Table II): 500 m³; 100–500 nodes; 5 sources; 5 sinks; R = 150 m; k = 0.05 s; v = 3 m/s.
**Evaluation:** 10 seeds (0–9) × 9 densities × 7 variants = 630 runs. Mean ± 95% CI; differences are paired on the same seed and topology.

## 1. What v2 adds to QLFR

| Component | Mechanism |
|---|---|
| **LQ: learned link quality** | Every packet carries the sender's transmission sequence number. Neighbours count gaps (ETX-style) to estimate p̂_ij with an EWMA (β = 0.2). History is forgotten when a link drops out of range. The reward becomes QLFR's Eq. (5) − w_lq·(1 − p̂_ij). |
| **DQ: Double Q-learning** | Two estimators; each link sample feeds one at random. Each table's target uses argmax under itself, evaluated with the other table. The advertised value is ½[Q_B(argmax Q_A) + Q_A(argmax Q_B)]. |
| **AL: adaptive list length** | Each sender uses the smallest L with 1 − Π(1 − p̂) ≥ ρ, replacing QLFR's global PDR-threshold scheme. |
| **Trap: learned trap penalty** | A per-node no-progress rate F_j (EWMA of "no candidate heard forwarding") is piggybacked in headers. The reward subtracts w_trap·F_j. |
| Holding time | Unchanged from QLFR: τ(n) = k(n − 1) |

**Tuned values:** w_lq = 0.25, ρ = 0.99, w_trap = 1.0. They were chosen on *separate tuning seeds* (100–102; `results/v2_tuning.txt`) and never on the evaluation seeds.

### Bugs found and fixed during implementation

1. **Implicit-ack link estimates were biased low** (0.63 learned vs 0.86 true). Silent candidates were counted as failures even when they were suppressed by another copy. That made lists longer, which caused more duplicates and more false failures: a feedback loop. Replaced by sequence-gap estimation (0.94 learned vs 0.93 true).
2. **Mobility counted out-of-range time as losses.** Fixed by resetting a link's history when it leaves range.
3. **Adaptive-list bug:** `searchsorted` was used on a descending array, so lists always hit the cap of 8. Fixed and covered by a unit test.
4. **The overestimation diagnostic was confounded** by the optimistic initial Q. It now compares learned V against an **oracle twin**: the same update schedule, but with the true p.

## 2. Results (averaged over 100–500 nodes)

| Variant | PDR | Delay (s) | Lifetime (s) | Total energy (J) | Tx / packet | V bias |
|---|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.900 ± 0.001 | 0.469 ± 0.003 | 13,865 ± 538 | 8,065 ± 307 | 25.0 ± 0.8 | — |
| QLFR (P_th = 0.97) | 0.965 ± 0.003 | 0.473 ± 0.003 | 7,297 ± 365 | 16,122 ± 738 | 48.4 ± 2.0 | — |
| + LQ | 0.898 ± 0.003 | 0.470 ± 0.003 | 13,494 ± 589 | 8,349 ± 187 | 25.7 ± 0.7 | +0.008 |
| + LQ + DQ | 0.899 ± 0.001 | 0.484 ± 0.003 | 12,488 ± 475 | 8,825 ± 353 | 27.2 ± 1.0 | +0.085 |
| + LQ + AL | 0.951 ± 0.003 | 0.471 ± 0.003 | **22,744 ± 838** | **5,253 ± 108** | **14.8 ± 0.3** | +0.007 |
| + LQ + DQ + AL | 0.963 ± 0.003 | 0.483 ± 0.003 | 18,736 ± 394 | 5,980 ± 88 | 17.2 ± 0.1 | +0.073 |
| **DQ-EVDR v2** (all four) | **0.967 ± 0.006** | 0.487 ± 0.003 | 18,156 ± 431 | 6,406 ± 123 | 18.2 ± 0.3 | +0.078 |

### Paired against QLFR at equal delivery ratio (P_th = 0.97)

This is the fair comparison: both protocols are run to deliver about the same share of packets.

| Variant | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| + LQ + AL | −0.013 ± 0.005 | −0.003 ± 0.002 | **3.18 ± 0.16** | 0.33 ± 0.01 | 0.31 ± 0.01 |
| + LQ + DQ + AL | −0.001 ± 0.004 | +0.010 ± 0.002 | 2.62 ± 0.12 | 0.38 ± 0.02 | 0.36 ± 0.01 |
| **DQ-EVDR v2** | +0.002 ± 0.006 | +0.013 ± 0.003 | **2.53 ± 0.09** | 0.40 ± 0.02 | 0.38 ± 0.01 |

### Paired against QLFR at its calibrated setting (P_th = 0.90)

| Variant | ΔPDR | ΔDelay (s) | Lifetime ratio | Tx ratio |
|---|---|---|---|---|
| + LQ | −0.002 ± 0.003 | +0.001 ± 0.003 | 0.99 ± 0.04 | 1.04 ± 0.02 |
| + LQ + DQ | −0.001 ± 0.002 | +0.015 ± 0.003 | 0.92 ± 0.03 | 1.10 ± 0.04 |
| + LQ + AL | +0.051 ± 0.003 | +0.001 ± 0.003 | 1.68 ± 0.09 | 0.61 ± 0.02 |
| + LQ + DQ + AL | +0.063 ± 0.004 | +0.014 ± 0.003 | 1.39 ± 0.05 | 0.71 ± 0.02 |
| **DQ-EVDR v2** | **+0.067 ± 0.006** | +0.018 ± 0.004 | **1.34 ± 0.05** | 0.75 ± 0.02 |

Per-density tables are in `qlfr_repro/results/ablation_summary.md`; the figure is `qlfr_repro/figures/ablation.png`.

## 3. What each component contributes

1. **Adaptive list length (AL) is the main contribution.**
   - Paired with learned link quality, it beats QLFR on every axis: +0.051 PDR, 1.68× lifetime, 39% fewer transmissions, no extra delay.
   - At equal delivery ratio it gives 3.2× QLFR's lifetime at a third of the energy.
   - Why it works: QLFR adapts one global list length from end-to-end PDR feedback. AL sizes each hop's candidate set from that hop's actual link reliability.
2. **The link-quality term alone (LQ) is neutral.** It changes rankings only slightly (w_lq = 0.25). Its value is in feeding AL with accurate p̂.
3. **Double Q-learning (DQ) does not deliver what we hypothesised.**
   - It adds +0.012 PDR on top of LQ + AL, but costs 18% of the lifetime and +0.012 s of delay.
   - It **raises** the measured value bias (+0.073 vs +0.007) instead of lowering it.
   - Reason: the single-estimator bias is already near zero, because EWMA-smoothed link estimates with a small weight give the max operator very little noise. Splitting samples between two estimators only makes each one noisier and slower.
   - Our original motivation (overestimation from noisy rewards) is **not supported** in this setting.
4. **The trap penalty is not significant here:** 0.967 ± 0.006 vs 0.963 ± 0.003 PDR. Voids are rare at these densities, with sources at the bottom and five sinks.

## 4. Implications for the paper

- **The strongest, defensible contribution is link-aware adaptive anypath candidate sets on top of QLFR's Q-learning** (QLFR + LQ + AL).
  - Equal-PDR result: about 3× lifetime, about 0.33× energy, the same delay.
  - Equal-setting result: +5 points PDR and 1.7× lifetime.
- **Double Q-learning should not be claimed as an improvement** on this evidence. Options:
  - (a) drop it and rename the protocol;
  - (b) keep it as a studied design choice with this negative result;
  - (c) test it where reward noise is genuinely high: harsh fading or shadowing, a larger w_lq, or fast-changing links. Section 5 plans this.
- The full DQ-EVDR v2 is still a clear improvement over QLFR (+0.067 PDR, 1.34× lifetime; or 2.5× lifetime at equal PDR), but its simpler + LQ + AL variant is better on lifetime.

## 5. Next steps

1. **Harsh-channel scenario**, the one place DQ might help: shadowing σ = 4–8 dB, lower Eb/N0, w_lq ∈ {0.5, 1}. Run the same ablation on 10 seeds.
2. **Sparse, void-rich scenario** (100–150 nodes, sources spread through the volume) to give the trap penalty a fair test.
3. **Decide the final protocol** from 1–2, then run the paper's full figure set (Figs. 6–15) for it against QLFR, DBR, EEDBR, DVOR and QELAR.
4. **Port to ns-3.**

## 6. Reproduce

```bash
cd qlfr_repro
python3 -m pytest -q tests        # 10 tests
python3 tune_v2.py                # tuning on seeds 100-102 (about 3 min)
python3 ablation.py               # 630 runs (about 8 min on 4 cores)
python3 ablation_report.py        # tables and figure
```
