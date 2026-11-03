# Full Audit and Novelty Assessment

**Date:** 3 Nov 2026. This document records a full recheck of everything in the repository, the errors found, how each was fixed, and an honest assessment of novelty. Where it disagrees with an earlier document, this one is correct; the earlier documents have been updated to match.

## 1. Summary of findings

| # | Area | Finding | Severity | Fix |
|---|---|---|---|---|
| 1 | ns-3 port | **The first ns-3 results were biased against QLFR.** With 10 s rounds and sources spread over 3.5 s, packets were still in flight when the next round began. Every node then beaconed and moved 30 m, and pending forwards were cancelled. QLFR's copies live for seconds (delay about 2 s), so it lost far more than LAQR: on dev seed 101, 541 pending forwards were cut for QLFR against 18 for LAQR. | **Critical**: it reversed the main ns-3 conclusion | Rounds are now 20 s, so every packet finishes before the round boundary (0 forwards cut on the dev seeds), and forwards are no longer cancelled at round end. Both evaluations (ALOHA and UanMacCw) were rerun. The old results are kept in `ns3_port/results/superseded_10s_rounds/`. |
| 2 | ns-3 port | **UanMacRc cannot run these protocols.** It is a single-gateway, single-hop reservation MAC. It sends all data by unicast to its gateway, passes up only packets addressed to the node itself, and `UanMacRcGw` aborts with "Currently only support single GW network!" when two of our 5 sinks hear each other. With one sink, only the gateway receives anything (35 beacons in total), so both protocols deliver 0%. | A requested experiment is impossible | `--mac=rc` was added (with the dual PHY it requires) only to demonstrate this. No UanMacRc results are reported. |
| 3 | Doc 01 | The Fig. 6 row said "Strong" and quoted the paper's "QLFR lowest", but our DVOR approximation has *lower* delay than QLFR at all 9 densities. The ordering is not reproduced. | Moderate (an overstated claim) | Row corrected. Added the note that paper values were read from plots by eye (±2–5% of the axis range). |
| 4 | Survey spreadsheet | The title row and 20 "How Our Work Addresses It" entries still described the dropped design (DQ-EVDR, Double Q-learning, learned void penalty). | Moderate (inconsistent positioning) | All rewritten to describe LAQR. Three void-focused papers had their relevance lowered (VAPR 85→65, Percolation 80→70, AUV repair 40→30), because LAQR does not handle voids. Rebuilt from `scripts/build_lit_xlsx.py`. |
| 5 | `paper/02_related_work.md` | The draft pitched DQ-EVDR with a "no double estimator yet" gap. It also **omitted QLFR, our own base paper**, and did not cite prior work on sizing candidate sets by reliability. | Major for the paper | Gap and contributions rewritten for LAQR. Added QLFR [39], path-diversity opportunistic routing [36], PRO [37] and ETX [38]; entries not opened in full are tagged **[TBC]**. |
| 6 | Doc 02 | The brainstorm describes DQ-EVDR v2 as the plan. | Minor | Marked as superseded (kept as a record). |
| 7 | Python simulator | It also cuts in-flight events at round end, so I checked whether this matters there. QLFR's delivery is unchanged between 10 s and 20 s rounds (0.89–0.91), because Python packets finish in about 0.5 s. LAQR at σ = 8 dB, 100 nodes falls from 0.868 to 0.772 with 20 s rounds, but that is a *mobility* effect: nodes move 60 m per round instead of 30 m. | Not a bug; one sensitivity to note | Documented here. The Python results in docs 03–05 stand. |

**Checked and correct:**
- All 11 unit tests pass.
- Every number in doc 05 (Tables 3.1 and 3.2, 18 cells plus CIs), doc 03 (ablation table) and doc 04 (harsh-channel and control tables) was recomputed independently from the raw CSVs. All match.
- The QLFR delay agreement in doc 01 (0.005–0.022 s) is correct.
- The survey sheet holds 50 rows, all with IF ≥ 5.5; it is correctly sorted (year, then IF), with no duplicate titles or links, and every link is an http(s) URL.
- The links themselves could not be re-opened in this session, because the network policy blocks publisher sites. They were verified twice in earlier sessions.

## 2. Corrected ns-3 results (20 s rounds; seeds 0–9; 100–500 nodes)

See `06_ns3_port.md` for full tables. Paired LAQR − QLFR (P_th = 0.90):

| MAC | Traffic | ΔPDR | ΔDelay (s) | Lifetime ratio | Tx ratio |
|---|---|---|---|---|---|
| ALOHA | spread out (J = 3.5 s) | **−0.228 ± 0.014** | −1.17 | **1.85** | 0.25 |
| ALOHA | simultaneous (J = 0.5 s) | **−0.454 ± 0.009** | −1.36 | **1.96** | 0.18 |
| UanMacCw | spread out | **−0.232 ± 0.013** | −1.52 | **2.00** | 0.24 |
| UanMacCw | simultaneous | **−0.437 ± 0.011** | −1.69 | **2.11** | 0.17 |

**In ns-3, LAQR does not beat QLFR on delivery.** It is a much cheaper operating point: 1.85–2.11× lifetime, 17–25% of the transmissions and 1.2–1.7 s less delay, at 23–45 points lower delivery. The two MACs give the same picture. This matches the Python result against QLFR at P_th = 0.97 under heavy shadowing: there, too, LAQR gives up some delivery for 3× lifetime. The Python claim "LAQR beats QLFR on delivery *and* lifetime" holds only in the MAC-less simulator.

**Why.** LAQR sizes each list so that 1 − Π(1 − p̂) ≥ ρ. It learns p̂ from beacons, which are spread out and rarely collide, so p̂ ≈ 0.9 and lists hold about 2 candidates. Data packets meet correlated collisions that beacons never see; in the diagnostic runs (dev seeds), the top-ranked candidate was heard re-forwarding only 30–65% of the time. QLFR's list sits at the cap of 8 and its redundancy pushes packets through.

**Can LAQR be tuned to match?** On dev seeds 101–102 (300 nodes; not the evaluation seeds), raising ρ trades energy for delivery:

| ρ | Mean list length | PDR | Tx/packet | Delay (s) |
|---|---|---|---|---|
| 0.99 (final) | 1.9 | 0.61 | 8.1 | 0.81 |
| 0.999 | 2.8 | 0.71 | 13.2 | 1.02 |
| 0.9999 | 3.5 | 0.75 | 18.7 | 1.28 |
| 0.99999 | 4.2 | 0.73 | 24.2 | 1.46 |
| QLFR | 5.4 | 0.84 | 38.5 | 2.07 |

Delivery tops out around 0.75. So a fixed ρ cannot reach QLFR's delivery in ns-3, though it can sit anywhere on a cheaper trade-off curve. A link estimator that sees data-time collisions, or traffic-aware sizing, is needed. That is future work.

## 3. Is LAQR novel?

**Short answer: it is incremental. The components are known; the combination and the evaluation are the contribution.**

| Component | Prior art | Status |
|---|---|---|
| Q-learning anypath routing with depth/energy reward and holding time | QLFR (Zhou, Cao, Xiang, IEEE IoTJ 2021); QELAR (2010) | Not ours; LAQR builds on QLFR |
| Link quality from sequence-number gaps (ETX-style) | De Couto et al., MobiCom 2003; standard in WSN link estimators | Not new |
| Link quality in the Q-learning reward | Several UASN Q-routers use SNR or link terms (e.g. a 2026 *Entropy* Q-learning UASN router with a receiver-SNR reward term, doi:10.3390/e28030346) | Not new as an idea |
| Candidate set sized for reliability | EPA-based UASN opportunistic routing (forwarder sets chosen for advancement × delivery probability); a 2018 *Sensors* study of candidate-set size vs path reliability; **PRO (IEEE/ACM ToN 2018) picks the minimum number of candidates that meets a delivery-ratio requirement**, in VANETs | The core rule has a close precedent in another domain |
| **Per-hop, learned-link-quality candidate sizing inside a Q-learning anypath UASN router, replacing QLFR's global PDR feedback** | Not found in our search | **Plausibly new, but incremental** |
| Negative result: Double Q-learning's gain under noise equals estimator smoothing | Not found | Useful, modest |
| Cross-simulator evaluation (MAC-less Python vs ns-3 with ALOHA and carrier sense), showing the conclusion depends on the MAC | Not found for QLFR-family routers | Useful, honest |

**Limits of this search.**
- It used web search only; publisher pages could not be opened in this session.
- One close-sounding 2025 paper, "A Q-Learning-Based Link-Aware Routing Protocol for Underwater Wireless Sensor Networks" (*JMSE* 13, 2374), could only be checked from its abstract. It is about predicting link expiry from node mobility to set how often neighbour information is refreshed, not about sizing candidate sets. Its full text must still be read before any novelty claim.
- PRO's exact sizing formula was confirmed only from its abstract and search snippets.

**What a paper can honestly claim:**
1. LAQR, a simple and overhead-free change to QLFR (per-hop link-aware candidate sets).
2. Its trade-off: in a MAC-less channel it improves delivery and lifetime together. Over a real ns-3 MAC it is a low-energy, low-delay operating point that gives up delivery.
3. The Double Q negative result.
4. The finding that beacon-based link estimation misses correlated data-time collisions, which matters for any reliability-targeted anypath scheme.

This is suitable for a mid-tier journal or a conference. It is **not** strong enough for an IF ≥ 8 venue without a stronger mechanism, such as a collision-aware estimator that closes the ns-3 delivery gap.

Sources used for the novelty check (titles and metadata from search results):
- QLFR: arXiv:2002.09623 and IEEE IoTJ 8(10), 2021, doi:10.1109/JIOT.2020.3042901.
- PRO: arXiv:1709.08199 and IEEE/ACM ToN 26(4), 2018, doi:10.1109/TNET.2018.2852220.
- Path-diversity opportunistic routing: *Sensors* 18(4) 1293, 2018, doi:10.3390/s18041293.
- Q-learning link-aware routing: *JMSE* 13 2374, 2025, doi:10.3390/jmse13122374.
- EDORQ: *Sensors* 20(4) 1025, 2020, doi:10.3390/s20041025.
- ETX: De Couto et al., MobiCom 2003.
