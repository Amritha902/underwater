# Brainstorming: What We Build on Top of QLFR

**Date:** 31 Oct 2026. It builds on `docs/01_base_paper_reimplementation.md`.

## 1. Where we stand

- QLFR has been re-implemented in Python together with DBR, VBF and our DQ-EVDR. Its qualitative claims hold against DBR: lower delay at every density and 1.86× longer lifetime.
- **First DQ-EVDR result:** no significant gain over QLFR. All paired confidence intervals contain 0, except a small PDR loss at 150 nodes.
- **Why there's no gain yet:**
  1. **Little estimation noise.** The links are mostly near-perfect below 200 m (P ≥ 0.98). Double Q-learning only helps when the max operator is applied to noisy estimates, and here there is little noise for it to fix.
  2. **Too few voids.** Only 1–8 void nodes per topology (see `void_nodes` in `results/density.csv`), so the void penalty rarely triggers.
  3. **Halved data.** Splitting samples across two estimators halves the data each estimator sees. That costs learning speed in a 400-packet run, which may explain the 150-node PDR dip.
  4. **Static environment.** Topology and channel never change, so learned values stay valid and adaptivity has nothing to adapt to.

All four point to the same conclusion: our proposal should be evaluated, and made stronger, in **harsh, time-varying** conditions. Those are exactly the conditions underwater deployments face, and the ones the literature says existing Q-routers handle poorly.

## 2. Ideas, ranked by expected impact and effort

| # | Idea | Why it should help | Effort | Priority |
|---|---|---|---|---|
| 1 | **Time-varying channel:** log-normal shadowing plus Doppler/mobility drift on top of Thorp | Creates the noisy rewards where Q-learning's max operator overestimates. This is the core motivation for Double Q-learning (van Hasselt, 2010). | Low: change `phy.py` | **Must do** |
| 2 | **Node mobility from ocean currents** (meandering-current or random-walk model) | Neighbour sets and link quality change during learning, so stale, overestimated Q-values hurt QLFR more | Medium | **Must do** |
| 3 | **Sparse, void-rich scenarios** (100–200 nodes, or deliberately created holes) | The void penalty needs voids to matter. VAPR, LRP and RLOR all evaluate void handling explicitly. | Low | **Must do** |
| 4 | **Learned void detection** in place of the static "no shallower neighbour" flag: count consecutive failed forwards through a neighbour (trap nodes, two-hop voids) | Catches trap nodes that are not local minima but lead into voids, and moves the void penalty from a hand-set rule to a learned one | Medium | High |
| 5 | **Measure overestimation directly:** log each node's advertised V against the realised return of delivered packets | Shows that Double Q-learning reduces bias, which is the paper's main argument, independent of delivery ratio | Low | High |
| 6 | **Separate learning rates per estimator, or "Weighted Double Q"** (blending single and double estimators) | Fixes the sample-halving slowdown (reason 3 above) | Low | Medium |
| 7 | **MAC collisions** (ALOHA/CSMA-like) | DBR's 80–128 transmissions per packet would collide heavily, which matters for a fair comparison. QLFR and DQ-EVDR send about 12–16. | Medium | Medium |
| 8 | **Adaptive candidate-set size** (K = 1–4, learned from link quality) | Trades duplicate transmissions against reliability per hop | Medium | Medium |
| 9 | **Port to ns-3** (UAN module or Aqua-Sim FG) | Required for the paper's "ns-3 evaluation" contribution and a credible channel/MAC model | High | **Must do** (later phase) |
| 10 | **Add QELAR and RLOR as extra baselines** | Both are high-relevance learning-based baselines from the survey (90% each) | Medium | Medium |
| 11 | **Trust term in the reward** | Links to the trust literature (COMST 2024, TMC 2022/2024 trust papers) | Medium | Optional / future work |
| 12 | **Age-of-information metric** | Links to AoI-focused AUV work (IoTJ 2021) | Low | Optional |

## 3. Proposed experiment plan (next steps)

1. **Scenario A, harsh channel:** 200 nodes, shadowing σ ∈ {0, 2, 4, 6} dB.
   - Plot PDR, delay, energy and value-estimation bias against σ.
   - Hypothesis: the gap between DQ-EVDR and QLFR grows with σ.
2. **Scenario B, mobility:** current speed 0–1.5 m/s.
   - Same metrics.
   - Hypothesis: DQ-EVDR degrades less as speed increases.
3. **Scenario C, voids:** 100–150 nodes, plus topologies with an artificial void region.
   - Metrics: void-encounter rate, PDR, retransmissions.
4. **Ablation:** QLFR, then + Double Q, then + void penalty, then + both (DQ-EVDR). This isolates each contribution.
5. **Statistics:** 10–20 seeds per point; paired tests per seed (same topology for every protocol); report 95% confidence intervals.
6. **Then port the winning configuration to ns-3** and repeat Scenarios A–C there.

## 4. What the paper would claim (if the experiments confirm it)

- Single-estimator Q-routing in underwater acoustic networks overestimates route values when link quality fluctuates. We would show this directly with the bias measurement (idea 5).
- DQ-EVDR removes that bias and learns to avoid voids, improving delivery and energy efficiency in harsh or mobile conditions, at no extra message cost.
- The protocol is localization-free (depth only), fully distributed and tabular, so it can run on sensor nodes.
- It comes with an open, reproducible implementation (Python, then ns-3).

## 5. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Double Q still shows no gain under harsh channels | Report the bias reduction (idea 5) as the contribution. Combine with the learned void detector (idea 4), which can help on its own. |
| Exact QLFR equations differ from our abstract-level version | As soon as the full text is accessible, swap in the paper's reward and holding-time equations, then re-run everything (scripts are ready). |
| Python results differ in ns-3 | Keep the same parameters and metrics; treat Python as a fast prototype and ns-3 as the final evaluation. |
| Reviewers ask for newer baselines | Add QTRU (EAAI 2025) once its PDF is obtained. It is the most recent Q-learning routing paper in our survey. |

## 6. Immediate to-do list

- [ ] Get QLFR's full text (allow `arxiv.org` or upload the PDF), match its parameters, and fill Section 7 of the re-implementation report.
- [ ] Implement shadowing and mobility (ideas 1 and 2) and the bias logger (idea 5).
- [ ] Run Scenarios A–C plus the ablation with 10+ seeds.
- [ ] Decide the final DQ-EVDR design from those results, then start the ns-3 port.
