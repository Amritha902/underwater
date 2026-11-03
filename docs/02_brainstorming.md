# Brainstorming: What We Build on Top of QLFR

> **Superseded (3 Nov 2026):** this brainstorm led to DQ-EVDR v2, which the experiments in `03_…` and `04_…` replaced with LAQR (`05_…`). Kept as a record of the reasoning.

**Date:** 1 Nov 2026. It builds on `01_base_paper_reimplementation.md` (faithful QLFR reproduction).

## 1. What the reproduction taught us

1. **QLFR's delay advantage comes almost entirely from the holding time τ(n) = k(n − 1).** Our delay matches the paper within 0.005–0.022 s using only the paper's equations, so the propagation-plus-holding model is right. Delay depends mostly on k and hop count, not on learning.
2. **QLFR's Q-learning is deterministic.** Its reward (Eq. 5–7) uses only depth and residual energy, which nodes know exactly. Q-values therefore never see noisy samples, and there is nothing for Double Q-learning to correct. *This is why our first DQ-EVDR design gives no gain in the paper's setting.*
3. **QLFR ignores link quality.** Candidates are ranked by depth and energy only, even though the paper's own channel model (Eq. 16–22) makes a 150 m link fail about 11% of the time against about 2% at 50 m. A far candidate ranked first wastes its slot whenever its link fails, and the next candidate has to wait an extra k.
4. **The multipath-suppression threshold P_th decides the delivery-vs-lifetime trade-off.** With P_th = 0.97, PDR matches the paper (0.97) but lifetime falls with density (9,299 → 5,985 s). With P_th = 0.90, lifetime rises (10,614 → 15,786 s) but PDR is 0.90. QLFR adapts the list length with a single global threshold that has to be hand-tuned.
5. **Our first DQ-EVDR is worse in this setting.** Delay is +0.06 s and lifetime is up to 42% lower at 500 nodes, with the same PDR. The noisy one-shot hello sample (w_link = 1) reshuffles the priority list every round. Unstable rankings break the energy balancing, and more transmissions follow.

## 2. Redesigned contribution (keeping the Double Q-learning idea where it is actually needed)

| # | Idea | Why it addresses a QLFR weakness | Effort | Priority |
|---|---|---|---|---|
| 1 | **Learned link quality from implicit acknowledgements.** Estimate p_ij with Double Q-style split estimators from actual forward successes, not one-shot hello samples. Put the expected cost (1 − p_ij)·k into the reward. | Weakness 3: ranks reliable candidates first, cuts wasted holding slots. Double Q now has real noise to correct (weakness 2), and averaging many samples avoids the reshuffling seen in weakness 5. | Medium | **Must do** |
| 2 | **Adaptive per-node list length in place of the global P_th.** Each sender sets L so that the probability that at least one candidate receives, 1 − Π(1 − p_ij), stays above a target. | Weakness 4: removes the hand-tuned global trade-off and adapts to local density and link quality. | Medium | **Must do** |
| 3 | **Learned void/trap penalty.** Learn which candidates often fail to make onward progress (trap nodes); use it as a cost, not a static flag. | QLFR has no void handling; voids grow when sources sit at the bottom of sparse networks (100–150 nodes, where QLFR's PDR is lowest at 0.90). | Medium | High |
| 4 | **Overestimation diagnostic:** log each node's V against the realised return of delivered packets, for single vs Double Q | Gives direct evidence for or against the Double Q claim, independent of PDR | Low | High |
| 5 | **Stability term:** add hysteresis to ranking changes, or smooth Q across rounds | Fixes the reshuffling problem (weakness 5) | Low | High |
| 6 | **Harsher channels:** log-normal shadowing on top of Rayleigh fading; weaker Eb/N0 | The regime where link-aware learning should matter most | Low | Medium |
| 7 | **MAC collisions** | DBR sends 1.3–13.6× and EEDBR 2.0–19.7× more transmissions per packet than QLFR (100–500 nodes); collisions would penalise them, a fairer comparison | Medium | Medium |
| 8 | **Port to ns-3** (UAN module / Aqua-Sim FG) | Our planned contribution: open, reproducible ns-3 evaluation | High | **Must do** (after the Python design is fixed) |
| 9 | **Newer baselines:** QTRU (EAAI 2025), RLOR (TVT 2021) | Reviewers will expect 2024–2026 comparisons; QLFR is from 2021 | Medium | High (needs the PDFs) |

## 3. Revised protocol sketch: DQ-EVDR v2

- **Reward:** r = −c_e(s_i) − c_e(s_j) − c_d(s_i,s_j) − w_l·(1 − p̂_ij) − w_v·trap̂_j
  - The first three terms are QLFR's own (Eq. 5–7).
  - p̂_ij and trap̂_j are learned from implicit acknowledgements, each with two estimators (Double Q-learning).
- **Q-update:** Double Q-learning. One estimator selects the best next-hop value and the other evaluates it, which removes the max-operator bias caused by the noisy p̂ and trap̂.
- **Priority list:** sorted by Q. Length L_i is the smallest value such that 1 − Π_{n ≤ L}(1 − p̂_{i,n}) ≥ ρ, with ρ a reliability target.
- **Holding time:** QLFR's τ(n) = k(n − 1), unchanged, so the delay advantage is preserved.

## 4. Experiment plan

1. **Baseline lock-in:** our faithful QLFR (done), plus DBR, EEDBR, DVOR and QELAR. Keep the paper's Table II setting.
2. **Ablation:** QLFR → + link term (single Q) → + link term (Double Q) → + adaptive L → + trap penalty = DQ-EVDR v2.
3. **Scenarios:**
   - The paper's setting (100–500 nodes, v = 1/3/5 m/s, k = 0.05 s).
   - Harsh channel (shadowing σ = 4–8 dB).
   - Sparse, void-rich networks (100–150 nodes).
4. **Metrics:** the paper's four (delay, PDR, total energy, lifetime), plus overestimation bias and transmissions per packet. Use 10 seeds and 95% confidence intervals.
5. **Success criterion:** at equal or better delay, DQ-EVDR v2 should deliver more packets than QLFR (at P_th = 0.90, without QLFR's lifetime loss) or last longer at the same PDR.

## 5. Risks

| Risk | Mitigation |
|---|---|
| Double Q still adds little | The link-quality term and adaptive L can carry the contribution alone; report the bias measurement either way. |
| Baselines are approximations (EEDBR, DVOR, QELAR) | Get those papers' PDFs and implement them exactly (`papers/DOWNLOAD_LIST.md`). |
| Absolute lifetime and energy units differ from the paper | Compare normalised trends, as in the report, and state the assumptions. |
| QLFR is from 2021 | Add QTRU (2025) as a second, recent baseline once its PDF is available. |

## 6. Immediate next steps

- [ ] Implement DQ-EVDR v2 (ideas 1, 2, 3, 5) in `uwsim/paper_sim.py` and run the ablation.
- [ ] Add the overestimation diagnostic (idea 4).
- [ ] Get the EEDBR, DVOR, QELAR and QTRU PDFs so the baselines can be implemented exactly.
- [ ] Port the final design to ns-3.
