# II. Related Work

> **Draft v1 (31 Oct 2026).** Working title of the paper: *Double Q-Learning Based Energy- and Void-Aware Depth Routing for Underwater Acoustic Sensor Networks: An ns-3 Evaluation.*
> Reference numbers below are local to this section and map to `literature_survey.md` (the "Survey #" column in the reference list). Every factual claim is taken from the paper's abstract or metadata as returned by search. Items tagged **[TBC]** still need the exact title or author list checked against the publisher page before submission.

Routing in underwater acoustic sensor networks (UASNs) is hard for three reasons. Acoustic links have low bandwidth and long propagation delay, nodes run on batteries that are difficult to recharge, and ocean currents keep moving nodes, so the topology changes all the time. This section reviews the five lines of work our protocol builds on: (A) classic geographic and depth-based routing, (B) energy-aware and void-aware extensions of those schemes, (C) fuzzy-logic and metaheuristic clustering approaches, (D) reinforcement-learning (RL) based routing, and (E) simulation tools and evaluation practice. It ends with (F) the research gap this paper addresses.

## A. Classic Geographic and Depth-Based Routing

The two baselines most used in the UASN routing literature are Vector-Based Forwarding (VBF) and Depth-Based Routing (DBR). In VBF [2], only nodes close to the virtual vector from the source to the destination forward a packet. This means only a small share of the nodes take part in routing. VBF also includes a self-adaptation step that lets nodes drop low-benefit packets to save energy. VBF works well in dense networks with low or moderate mobility, which led to a hop-by-hop variant (HH-VBF) for sparse deployments [2].

DBR [1] removes the need for full 3-D location information: each node forwards using only its local depth, which a pressure sensor can measure cheaply. Neither protocol needs the periodic routing-table refresh that land-based protocols depend on, and that refresh is expensive when the topology keeps changing [1]. Both are greedy, though, and greedy forwarding fails when a packet reaches a node with no neighbour shallower than itself (a *routing void*). Neither protocol considers residual energy either. Most of the work reviewed below sets out to fix one or both of these weaknesses.

## B. Energy-Aware and Void-Aware Extensions (2024–2026)

Recent depth-based protocols add power control and energy awareness. Chu *et al.* [9] proposed APC-EEDBR (Adaptive Power-Controlled Energy-Efficient Depth-Based Routing), which picks relay nodes using neighbour tables and adjusts transmit power. Xu, Song *et al.* [15] combined power control with multi-path routing for the Internet of Underwater Things (IoUT) in varying environments. Homaei *et al.* [14] adapted the terrestrial RPL protocol to the IoUT (RPLUW/M), with network lifetime and node mobility as their main concerns.

Several 2024–2025 papers target routing voids directly. Hussain *et al.* [16] extended adaptive hop-by-hop VBF with three hop-by-hop forwarding checks and relay/sink mobility optimisation, and reported gains in lifetime, throughput, residual energy and packet delivery ratio (PDR). A 2024 trust-model routing scheme [17] uses a two-hop availability check to find void nodes before forwarding. Such schemes find voids with *fixed* rules, such as hop-count look-ahead or geometric checks. They do not *learn* from experience which neighbours tend to lead into voids.

## C. Fuzzy-Logic and Metaheuristic Approaches

A second group of work combines several routing metrics using fuzzy inference. Sun *et al.* [10] proposed a three-dimensional UASN routing protocol based on fuzzy-logic reasoning for adaptive, energy-efficient forwarding. A 2025 preprint [28] built a fuzzy-logic decision from residual energy, hop count, link quality and depth, and evaluated it in **ns-3**. Its reported lifetime improvement has not yet been peer-reviewed.

Clustering protocols use bio-inspired metaheuristics to choose cluster heads. Examples are the Hunger-Driven Lion Clustering Algorithm (HDLCA) [21], an artificial-fish-swarm clustering protocol [22], and HECRA [23], which extends LEACH-style cluster-head election with residual energy and node degree for AUV-assisted networks. Shwetha *et al.* [24] paired a metaheuristic optimiser with Gaussian-mixture clustering. These methods work well, but their rules or optimiser settings are fixed at design time. They do not adapt online when channel conditions change.

## D. Reinforcement-Learning-Based Routing

RL lets each node learn a forwarding policy from local feedback, so it needs no global knowledge of the network. That makes it a good match for UASNs.

**Early work.** QELAR [3] was the first widely cited Q-learning routing protocol for underwater sensor networks. It uses Q-learning to spread residual energy evenly across nodes, and in Aqua-Sim simulations it achieved about 20 % longer network lifetime than VBF. Later work has noted that its convergence can be slow when there are many nodes or mobility is high [3]. CARMA [4] introduced channel-aware RL that switches between single-path and multi-path routing to jointly optimise route energy and PDR. In SUNSET simulations and at-sea experiments, it achieved up to 40 % higher PDR than CARP, QELAR and EFlood.

**Recent work (2025–2026).** RL-based routing has picked up pace in the last two years:

- Li *et al.* [11] proposed a Q-learning-based *link-aware* routing protocol for UWSNs.
- The SAQR protocol [12] makes Q-learning routing *service-aware*, so different traffic classes receive different treatment.
- Prasad [13] combined energy-aware clustering with Q-learning next-hop selection, and reported lower average energy consumption than VBF.
- Karami Benmaran and Taheri Javan [33] used a generative adversarial network (GAN) to store and generate good paths for an RL router.
- A telematic RL routing protocol for the IoUT [19] and a multi-agent RL (MARL) router with multi-head attention for software-defined UASNs [18] go further, toward deep and multi-agent learning.
- In 2026, Q-learning-style opportunistic routing was combined with network coding in a cross-layer design [20].

Two recent surveys [8], [30] confirm that learning-based protocols are now a main research direction in UASN routing.

**Learning at other layers.** RL is also being applied to MAC design. Examples are a deep-Q-learning MAC with power control [25] and a field study of whether deep-RL MAC protocols work in real sea trials [26]. Song *et al.* [27] proposed a digital-twin network architecture in which MARL helps make up for scarce real-world training data. These works suggest that complex deep models are hard to run on resource-limited acoustic nodes, which makes lightweight tabular learners attractive for per-node routing decisions.

**The overestimation problem.** Every Q-learning router listed above updates its values with the *maximum* estimated value of the next state. Van Hasselt [5] showed that this max operator introduces a *positive bias* (overestimation) when rewards and transitions are stochastic. He proposed *Double Q-learning*, which keeps two estimators and separates choosing the action from evaluating it, and which still converges to the optimal policy. Underwater acoustic link quality changes a great deal over time because of multipath and Doppler effects [35]. A single Q-learning router can therefore become over-optimistic about a neighbour whose link has recently degraded, or that leads into a void. None of the UASN routing abstracts we reviewed report using a double estimator.

## E. Simulation Tools and Evaluation Practice

The Aqua-Sim family is the most common tool for UASN routing research. Aqua-Sim NG [6] ported the original ns-2 Aqua-Sim to **ns-3**, adding 3-D and mobile network support and fixing memory-management problems. Aqua-Sim Fourth Generation (FG) [7], published in 2025, builds on ns-3 and adds MATLAB/Python interfaces for AI models and hardware-in-the-loop simulation. Its authors argue that earlier ns-2/ns-3 simulators simulate either the communication side or the AI side well, but not both. The built-in ns-3 UAN module also provides an acoustic channel model, MAC protocols and an energy model.

Even so, evaluation practice varies widely. Of the RL routers above, QELAR used Aqua-Sim [3], CARMA used SUNSET plus sea trials [4], and RL-RPL-UA released Aqua-Sim code [34]. For most 2025–2026 RL routing papers ([11]–[13], [18], [19], [33]), the abstracts we reviewed do not name an ns-3-based simulator. Comparing reported numbers across these papers is therefore unreliable, because channel model, MAC layer and energy model all differ.

## F. Research Gap and Contributions

**Table I.** Summary of representative routing protocols (as described in their abstracts or metadata).

| Ref. | Protocol / year | Decision method | Energy-aware | Void handling | Reported simulator |
|---|---|---|---|---|---|
| [2] | VBF (2006) | Geometric vector pipe | Partial (self-adaptation) | No | — |
| [1] | DBR (2008) | Greedy depth | No | No | — |
| [3] | QELAR (2010) | Q-learning | Yes | Implicit | Aqua-Sim (ns-2) |
| [4] | CARMA (2019) | Distributed RL, multi-path | Yes | Via multi-path | SUNSET + sea trial |
| [16] | IM-RM-AHH-VBF (2025) | Rule-based, 3-hop verification | Yes | Yes (fixed rules) | Not stated |
| [9] | APC-EEDBR (2025) | Depth + power control | Yes | Not stated | Not stated |
| [10] | 3-D fuzzy routing (2025) | Fuzzy inference | Yes | Not stated | Not stated |
| [28] | Fuzzy adaptive routing (2025, preprint) | Fuzzy inference | Yes | Not stated | **ns-3** |
| [11] | Q-learning link-aware (2025) | Q-learning | Not stated | Not stated | Not stated |
| [13] | DRL energy-efficient (2026) | Q-learning + clustering | Yes | Claimed | Not stated |
| **Ours** | **DQ-EVDR** | **Double Q-learning** | **Yes** | **Learned void penalty** | **ns-3 (UAN / Aqua-Sim NG)** |

"Not stated" means the abstract or metadata we could access did not say. The full texts must be checked before submission.

From this survey we identify three gaps:

1. **Estimation bias.** Existing Q-learning UASN routers use single-estimator Q-learning, which tends to overestimate values when link quality is noisy [5]. As far as our survey found, no UASN routing protocol uses a double estimator.
2. **Learned void avoidance.** Void handling in recent work relies on fixed geometric or hop-count rules [16], [17]. It is not part of what the router learns.
3. **Reproducible ns-3 evaluation.** Recent RL routers are seldom evaluated in a common, open ns-3 setup alongside the classic DBR and VBF baselines, even though such tools exist [6], [7].

**Contributions.** To address these gaps, this paper:
(i) proposes **DQ-EVDR**, a distributed Double Q-learning routing protocol whose reward combines depth progress, residual energy, link quality and a learned void penalty;
(ii) uses Q-value-based holding times so that the best-ranked forwarder transmits first and lower-ranked copies are suppressed;
(iii) implements the protocol in ns-3 and benchmarks it against DBR, VBF, a fuzzy-logic scheme and single-estimator Q-learning. The metrics are PDR, end-to-end delay, energy per delivered packet, network lifetime and void-encounter rate, measured under varying node density and mobility.

---

## References (this section)

| Ref | Survey # | Citation (IEEE style) |
|---|---|---|
| [1] | — | H. Yan, Z. J. Shi, and J.-H. Cui, "DBR: Depth-based routing for underwater sensor networks," in *Proc. IFIP NETWORKING 2008*, LNCS vol. 4982, Springer, 2008, pp. 72–86. |
| [2] | — | P. Xie, J.-H. Cui, and L. Lao, "VBF: Vector-based forwarding protocol for underwater sensor networks," in *Proc. IFIP NETWORKING 2006*, LNCS vol. 3976, Springer, 2006. doi: 10.1007/11753810_111 |
| [3] | — | T. Hu and Y. Fei, "QELAR: A machine-learning-based adaptive routing protocol for energy-efficient and lifetime-extended underwater sensor networks," *IEEE Trans. Mobile Comput.*, vol. 9, no. 6, pp. 796–809, Jun. 2010. |
| [4] | — | V. Di Valerio, F. Lo Presti, C. Petrioli, L. Picari, D. Spaccini, and S. Basagni, "CARMA: Channel-aware reinforcement learning-based multi-path adaptive routing for underwater wireless sensor networks," *IEEE J. Sel. Areas Commun.*, vol. 37, no. 11, pp. 2634–2647, Nov. 2019. doi: 10.1109/JSAC.2019.2933968 |
| [5] | — | H. van Hasselt, "Double Q-learning," in *Advances in Neural Information Processing Systems 23 (NIPS 2010)*, 2010, pp. 2613–2621. |
| [6] | — | R. Martin, Z. Peng, S. Rajasekaran *et al.*, "Aqua-Sim Next Generation: An NS-3 based underwater sensor network simulator," in *Proc. ACM WUWNet*, 2015. **[TBC: DBLP lists 2015, another index lists 2017; confirm year and full author list]** |
| [7] | 1 | "Aqua-Sim Fourth Generation: Towards general and intelligent simulation for underwater acoustic networks," *IEEE Internet Things J.*, vol. 12, 2025. arXiv:2410.20698. **[TBC: authors]** |
| [8] | 155 | "Survey of AI-driven routing protocols in underwater acoustic networks for enhanced communication efficiency," *Ocean Eng.*, vol. 314, 2024. **[TBC: authors]** |
| [9] | 13 | Chu, Wang, Fang, and Liu, "Adaptive power-controlled energy-efficient depth-based routing protocol for underwater wireless sensor networks," *J. Mar. Sci. Eng.*, vol. 13, no. 8, art. 1418, 2025. **[TBC: initials]** |
| [10] | 12 | Sun, Liu, Dong, and Wang, "A three-dimensional routing protocol for underwater acoustic sensor networks based on fuzzy logic reasoning," *J. Mar. Sci. Eng.*, vol. 13, art. 692, 2025. **[TBC: initials]** |
| [11] | 37 | Li, Wu, Zhu, and Ren, "A Q-learning-based link-aware routing protocol for underwater wireless sensor networks," *J. Mar. Sci. Eng.*, vol. 13, no. 12, art. 2374, 2025. **[TBC: initials]** |
| [12] | 38 | "Service-aware Q-learning-based routing protocol in the underwater acoustic sensor network," *Comput. Netw.*, vol. 257, Feb. 2025. **[TBC: authors]** |
| [13] | 43 | M. Prasad, "Deep reinforcement learning-enabled energy-efficient routing protocol for underwater wireless sensor networks," *Int. J. Electron. Telecommun.*, 2026. doi: 10.24425/ijet.2026.157924 |
| [14] | 15 | Homaei *et al.*, "Enabling RPL on the Internet of Underwater Things," *J. Netw. Syst. Manage.*, vol. 33, art. 55, May 2025. doi: 10.1007/s10922-025-09925-0 |
| [15] | 14 | C. Xu, S. Song *et al.*, "Joint power control and multi-path routing for Internet of Underwater Things in varying environments," *IEEE Internet Things J.*, 2025. doi: 10.1109/JIOT.2025.3527692 |
| [16] | 16 | Hussain *et al.*, "Improved relay mobility-adaptive hop-by-hop vector-based forwarding (IM-RM-AHH-VBF)," *Telecommun. Syst.*, vol. 88, 2025. doi: 10.1007/s11235-025-01260-8 **[TBC: exact title]** |
| [17] | 32 | Trust-model-based routing with two-hop void avoidance for UWSNs, *Sensors*, vol. 24, no. 23, art. 7614, 2024. **[TBC: title, authors]** |
| [18] | 42 | "Smart interrupted routing based on multi-head attention mask mechanism-driven MARL in software-defined UASNs," arXiv:2509.15856, 2025. **[TBC: authors]** |
| [19] | 40 | "A reinforcement learning-based telematic routing protocol for the Internet of Underwater Things," arXiv:2506.00133, 2025. **[TBC: authors]** |
| [20] | 44 | "Cross-layer cooperative design of network coding and distributed opportunistic routing for underwater acoustic sensor networks," *IEEE Sensors J.*, vol. 26, 2026. doi: 10.1109/JSEN.2025.3633275 **[TBC: authors]** |
| [21] | 74 | Raghu, Shyamsundar, and T. Shankar, "HDLCA: Hunger driven lion clustering algorithm, a novel energy efficient and scalable clustering approach for underwater wireless sensor nodes," *Sci. Rep.*, vol. 15, art. 33292, 2025. |
| [22] | 75 | "Energy-efficient artificial fish swarm-based clustering protocol for enhancing network lifetime in underwater wireless sensor networks," *EURASIP J. Wireless Commun. Netw.*, 2024. doi: 10.1186/s13638-024-02422-z **[TBC: authors]** |
| [23] | 70 | "High-efficiency clustering routing protocol in AUV-assisted underwater sensor networks," *Sensors*, vol. 24, no. 20, art. 6661, 2024. **[TBC: authors]** |
| [24] | 18 | Shwetha *et al.*, "Optimizing energy efficient routing protocol performance in underwater wireless sensor networks with machine learning algorithms," *Trans. Emerg. Telecommun. Technol.*, vol. 36, no. 3, 2025. doi: 10.1002/ett.70073 |
| [25] | 46 | "Deep Q-learning based adaptive MAC protocol with collision avoidance and efficient power control for UWSNs," *J. Mar. Sci. Eng.*, vol. 13, no. 3, art. 616, 2025. doi: 10.3390/jmse13030616 **[TBC: authors]** |
| [26] | 56 | "Is DRL-based MAC ready for underwater acoustic networks? Exploring its practicality in real field experiments," arXiv:2605.10144, 2026. **[TBC: authors]** |
| [27] | 105 | Song *et al.*, "A digital twin-based intelligent network architecture for underwater acoustic sensor networks," *IEEE Trans. Mobile Comput.*, vol. 24, no. 9, 2025. arXiv:2410.20151 |
| [28] | 3 | "Intelligent fuzzy-based adaptive routing protocol for underwater wireless sensor networks in marine environmental monitoring applications," Preprints.org, 202510.0666, 2025 (not peer-reviewed). |
| [29] | 21 | "Advanced routing protocols for underwater wireless sensor networks: Energy optimization and quality of service enhancement," Preprints.org, 202508.0998, 2025 (not peer-reviewed). |
| [30] | 154 | "A review of energy-efficient routing protocols for underwater acoustic wireless sensor networks," *Informatics*, vol. 13, no. 10, art. 168, 2026. **[TBC: authors]** |
| [31] | 62 | Cao, Chen, and Cheng, "Joint AoI and energy optimization for multi-AUV data collection in UASNs," *Front. Mar. Sci.*, 2025. doi: 10.3389/fmars.2025.1580751 **[TBC: exact title]** |
| [32] | 153 | Omeke *et al.*, "Machine learning for the Internet of Underwater Things: From fundamentals to implementation," arXiv:2603.07413, 2026. |
| [33] | 39 | Karami Benmaran and Taheri Javan, RL- and GAN-based routing for UWSNs, *Soft Comput. J.*, 2025. **[TBC: exact title]** |
| [34] | 41 | Homaei *et al.*, "RL-RPL-UA," arXiv / JITEL, 2025 (Aqua-Sim implementation). **[TBC: exact title]** |
| [35] | 116 | "Toward intelligent underwater acoustic systems: Systematic insights into channel estimation and modulation methods," *Electronics*, vol. 14, no. 15, art. 2953, 2025. doi: 10.3390/electronics14152953 **[TBC: authors]** |

References [1]–[6] (the classic baselines and Double Q-learning) were checked separately by title search on 31 Oct 2026. [29], [31] and [32] are in the list for use in the Introduction and are not cited above.
