# Harsh-Channel Ablation: Does Double Q-Learning Help When Links Are Noisy?

**Date:** 1 Nov 2026. **Code:** `qlfr_repro/harsh_ablation.py`, `harsh_report.py`, `harsh_control.py`. **Full tables:** `qlfr_repro/results/harsh_summary.md`. **Figure:** `qlfr_repro/figures/harsh_ablation.png`.

## 1. Setup

- **Channel:** the QLFR paper's Rayleigh/BPSK channel (Eq. 16–22), plus **log-normal shadowing** redrawn every round and symmetric per link. This is not in the QLFR paper; it is our stress test.
  - σ = 0 dB (the paper's channel): mean link success 0.93.
  - σ = 4 dB: 0.90, with 0.9% of links below 50% success.
  - σ = 8 dB: 0.83, with 10.9% of links below 50% success.
- **Everything else:** the paper's Table II setting (5 sources, 5 sinks, R = 150 m, k = 0.05 s, v = 3 m/s).
- **Variants:** QLFR (P_th = 0.90 and 0.97), plus LQ, DQ, AL and Trap combinations, each at w_lq = 0.25 (tuned) and w_lq = 1.0 (a stronger link term, more noise for Double Q to act on).
- **Runs:** 5 densities (100–500) × 10 evaluation seeds = 1,200 runs, plus a 250-run control.
- ρ = 0.99 and w_trap = 1.0 are kept from the tuning in `03_dqevdr_v2_ablation.md`; they were not re-tuned for this channel.

## 2. Main results (averaged over densities, w_lq = 0.25, mean ± 95% CI)

| Variant | PDR σ=4 | Lifetime σ=4 (s) | PDR σ=8 | Lifetime σ=8 (s) | Delay σ=8 (s) |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.896 ± 0.004 | 12,148 | 0.895 ± 0.005 | 10,298 | 0.510 |
| QLFR (P_th = 0.97) | 0.958 ± 0.008 | 7,012 | 0.958 ± 0.007 | 6,758 | 0.514 |
| + LQ | 0.894 ± 0.005 | 11,846 | 0.898 ± 0.003 | 10,075 | 0.514 |
| + LQ + DQ | 0.897 ± 0.007 | 11,668 | 0.897 ± 0.004 | 9,624 | 0.525 |
| + LQ + AL | 0.921 ± 0.009 | **23,642** | 0.868 ± 0.009 | **26,560** | 0.506 |
| + LQ + DQ + AL | 0.944 ± 0.010 | 19,684 | 0.889 ± 0.009 | 22,431 | 0.519 |
| **DQ-EVDR v2** | **0.947 ± 0.012** | 19,030 | **0.904 ± 0.007** | 20,854 | 0.531 |

### Paired against QLFR (P_th = 0.90)

| Variant | ΔPDR σ=4 | Lifetime ratio σ=4 | ΔPDR σ=8 | Lifetime ratio σ=8 | ΔDelay σ=8 (s) |
|---|---|---|---|---|---|
| + LQ + AL | +0.025 ± 0.008 | 2.00 | **−0.027 ± 0.009** | 2.62 | −0.004 |
| + LQ + DQ + AL | +0.048 ± 0.009 | 1.66 | −0.006 ± 0.008 | 2.20 | +0.010 |
| DQ-EVDR v2 | **+0.051 ± 0.010** | 1.61 | **+0.009 ± 0.010** | **2.05** | +0.021 |

At w_lq = 1.0 the picture is the same, with slightly more delay. A stronger link term does not give Double Q extra benefit.

### Effect of adding Double Q (paired, same seeds)

| Comparison | ΔPDR σ=4 | ΔPDR σ=8 | Lifetime ratio σ=8 | ΔV bias σ=8 |
|---|---|---|---|---|
| + LQ + DQ vs + LQ | +0.002 ± 0.007 | −0.001 ± 0.006 | 0.96 | +0.089 |
| + LQ + DQ + AL vs + LQ + AL | **+0.024 ± 0.011** | **+0.022 ± 0.010** | 0.85 | +0.068 |

## 3. Control: is the Double Q gain just smoother link estimates?

Double Q splits link samples across two estimators and averages them. That effectively lengthens the estimator's memory. To test whether that alone explains the gain, we ran single-estimator + LQ + AL with slower EWMA rates (β; the default is 0.2) at σ = 8 dB:

| Variant (σ = 8 dB) | PDR | Delay (s) | Lifetime (s) | Tx / packet |
|---|---|---|---|---|
| + LQ + AL, β = 0.2 | 0.868 ± 0.009 | 0.506 | 26,560 ± 840 | 13.1 |
| **+ LQ + AL, β = 0.1** | 0.894 ± 0.012 | 0.508 | **24,075 ± 1,283** | 14.5 |
| **+ LQ + AL, β = 0.05** | **0.899 ± 0.010** | 0.510 | 22,979 ± 1,133 | 15.0 |
| + LQ + DQ + AL, β = 0.2 | 0.889 ± 0.009 | 0.519 | 22,431 ± 1,004 | 14.9 |
| + LQ + DQ + AL, β = 0.1 | 0.896 ± 0.009 | 0.519 | 21,631 ± 793 | 15.3 |

**A single estimator with slower smoothing matches or beats Double Q** on every metric:
- Delivery: equal or higher.
- Lifetime: higher.
- Delay: about 0.01 s lower.

Caveat: these β values were explored on the evaluation seeds as a diagnostic. A final β must be chosen on tuning seeds.

## 4. Conclusions

1. **Harsh channels expose a weakness of adaptive lists with fast estimators.** With β = 0.2, noisy p̂ sometimes overstates link quality, so lists are cut too short. Delivery then falls below QLFR at σ = 8 dB (−0.027), even though lifetime is 2.6× longer.
2. **Double Q-learning does recover that delivery (+0.022 to +0.032), but not through reduced overestimation.** Our oracle-twin bias measure is *higher* with Double Q at every σ and w_lq. The gain comes from smoother averaged link estimates, and a single estimator with β = 0.05–0.1 achieves the same at lower cost.
3. **Across the paper's channel (σ = 0) and both harsh channels**, the evidence says the protocol's value comes from **link-quality-aware adaptive candidate lists with a properly smoothed estimator**, not from Double Q-learning.
4. **The trap penalty gives a small, borderline gain** at σ = 8 dB: DQ-EVDR v2 at 0.904 against 0.889 without it (CIs about ±0.009). It needs the sparse/void scenario for a fair test.

## 5. Recommendation for the final protocol

**Final design:** QLFR's Q-learning and holding time, plus a learned link-quality term (single estimator, β tuned for the channel), plus adaptive per-hop list length (ρ), plus, optionally, the trap penalty.

Present Double Q-learning as an evaluated design choice that did not reduce estimation bias. Its gain under noise is fully explained by estimator smoothing. This is an honest and useful finding for the paper.

**Next steps:**
1. Tune β (and ρ) jointly on tuning seeds for σ ∈ {0, 4, 8}. Consider an adaptive β that depends on the observed variance of p̂.
2. Run the sparse/void scenario for the trap penalty.
3. Fix the final protocol and run the paper's full figure set (Figs. 6–15) against QLFR, DBR, EEDBR, DVOR and QELAR.
4. Port to ns-3.
