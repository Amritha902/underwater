# Literature Survey: Underwater Sensor Networks (UWSN / UASN / IoUT), ns-3 Simulation Focus

Compiled: 31 Oct 2026 · 155 papers · 121 from 2025–2026, 34 from 2024

## How these were verified

- Every paper below came up in live web-search results (search-engine index), and every link is the URL the search returned. No title, DOI or link was written from memory.
- The sandbox could not open publisher pages directly (mdpi.com, arxiv.org, doi.org and ieeexplore were blocked), so I have **not** read the full texts. Before citing, open each link once to confirm the exact title, authors and pages.
- **Status** column: `Journal` / `Conf.` = peer-reviewed venue, `arXiv` / `Preprint` = not peer-reviewed yet.
- Some Title cells are short descriptions (marked with `~`) because the search results described the paper but didn't show its exact title. Get the exact title from the link.
- Papers I couldn't confirm (no year, no working link, or no title) were **removed**.

---

## 1. Simulation tools and ns-3 (most relevant to our project)

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 1 | 2025 | Aqua-Sim Fourth Generation: Towards General and Intelligent Simulation for Underwater Acoustic Networks (ns-3 based) | IEEE Internet of Things Journal, vol. 12 (arXiv 2410.20698) | Journal | https://arxiv.org/abs/2410.20698 |
| 2 | 2025 | ~ NS-3 for underwater acoustic networks (UAN module overview) | IJCESR vol. 12, iss. 6, pp. 70–77 | Journal | http://troindia.in/journal/ijcesr/vol12iss6/70-77.pdf |
| 3 | 2025 | ~ Fuzzy-logic adaptive routing (residual energy, hop count, link quality, depth), evaluated in **NS-3** | Preprints.org 202510.0666 | Preprint | https://www.preprints.org/manuscript/202510.0666 |
| 4 | 2026 | Sea Trial Validation of the ROS-DESERT Middleware with Autonomous Underwater Vehicles | arXiv 2605.23553 | arXiv | https://arxiv.org/abs/2605.23553 |
| 5 | 2024 | ~ UW-ALOHA-Q RL-based MAC evaluated under unreliable channels with the DESERT simulator | Zenodo record 10850803 (conference paper) | Conf. | https://zenodo.org/records/10850803 |
| 6 | 2025 | Li & Chitre – StableUASim: pre-trained conditional latent-diffusion surrogate for UWA channel simulation | arXiv 2511.18078 | arXiv | https://arxiv.org/abs/2511.18078 |
| 7 | 2026 | Underwater Acoustic Channel Library | arXiv 2609.03207 | arXiv | https://arxiv.org/abs/2609.03207 |
| 8 | 2025 | Traspadini, Zorzi, Giordani – Performance Evaluation of LoRa for IoT Applications in Non-Terrestrial Networks via **ns-3** (terrestrial WSN reference) | arXiv 2509.02811 | arXiv | https://arxiv.org/abs/2509.02811 |
| 9 | 2025 | FAST-LoRa: An Efficient Simulation Framework for Evaluating LoRaWAN Networks and Transmission Parameter Strategies (terrestrial WSN reference) | arXiv 2507.23342 | arXiv | https://arxiv.org/abs/2507.23342 |
| 10 | 2025 | Evaluating the Performance of LoRa Networks: A Study on Disaster Monitoring Scenarios (terrestrial WSN reference) | IoT (MDPI) 6(1), 14 | Journal | https://doi.org/10.3390/iot6010014 |
| 11 | 2026 | Towards Realistic Waveform-Level IoT Network Simulation via IQ Mixing (terrestrial WSN reference) | arXiv 2604.06408 | arXiv | https://arxiv.org/abs/2604.06408 |

## 2. Routing protocols (energy, depth-based, fuzzy, clustering-based)

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 12 | 2025 | Sun, Liu, Dong, Wang – A Three-Dimensional Routing Protocol for UASNs Based on Fuzzy Logic Reasoning | J. Mar. Sci. Eng. 13, 692 | Journal | https://mdpi-res.com/d_attachment/jmse/jmse-13-00692/article_deploy/jmse-13-00692.pdf |
| 13 | 2025 | Chu, Wang, Fang, Liu – Adaptive Power-Controlled Energy-Efficient Depth-Based Routing Protocol (APC-EEDBR) for UWSNs | J. Mar. Sci. Eng. 13(8), 1418 | Journal | https://mdpi.com/2077-1312/13/8/1418 |
| 14 | 2025 | Xu, Song et al. – Joint Power Control and Multi-Path Routing for Internet of Underwater Things in Varying Environments (doi 10.1109/JIOT.2025.3527692) | IEEE Internet of Things Journal | Journal | https://ccst.jlu.edu.cn/info/1028/19119.htm |
| 15 | 2025 | Homaei et al. – Enabling RPL on the Internet of Underwater Things (RPLUW/M) | J. Network and Systems Management 33, art. 55 | Journal | https://link.springer.com/article/10.1007/s10922-025-09925-0 |
| 16 | 2025 | Hussain et al. – Improved Relay Mobility-Adaptive Hop-by-Hop VBF (IM-RM-AHH-VBF) | Telecommunication Systems 88 | Journal | https://ideas.repec.org/a/spr/telsys/v88y2025i1d10.1007_s11235-025-01260-8.html |
| 17 | 2025 | Khan, Rauf, Jamil – Hybrid CT-DEWCA energy-efficient routing for data and storage nodes in UASNs | IEEE Access | Journal | https://library.kab.ac.ug/Record/doaj-art-ea96ac656c5a4c58b73d4f2fa03d8f9d/Description |
| 18 | 2025 | Shwetha et al. – Optimizing Energy Efficient Routing Protocol Performance in UWSNs With Machine Learning Algorithms | Trans. Emerging Telecommunications Technologies 36(3) | Journal | https://onlinelibrary.wiley.com/doi/10.1002/ett.70073 |
| 19 | 2025 | ~ RL-SRP: A secure routing protocol for UASNs using reinforcement learning (doi 10.1109/ETECOM66111.2025.11319130) | IEEE ETECOM 2025 | Conf. | https://research-portal.uws.ac.uk/en/publications/a-secure-routing-protocol-for-underwater-acoustic-sensor-networks/ |
| 20 | 2025 | ~ DTEAR: Digital-twin-synchronised energy-aware depth-based routing for UANs | Preprints.org 202511.0328 | Preprint | https://www.preprints.org/manuscript/202511.0328 |
| 21 | 2025 | Advanced Routing Protocols for UWSNs: Energy Optimization and QoS Enhancement (review 2018–2025) | Preprints.org 202508.0998 | Preprint | https://www.preprints.org/manuscript/202508.0998 |
| 22 | 2026 | ~ Hybrid message encoding based routing protocol (HMERP) for UASNs | Telecommunication Systems | Journal | https://link.springer.com/article/10.1007/s11235-026-01411-5 |
| 23 | 2026 | ~ Dynamic cluster-head routing protocol for intra- and inter-cluster UAWSNs | Wireless Networks | Journal | https://link.springer.com/article/10.1007/s11276-026-04119-1 |
| 24 | 2026 | ~ Metaheuristic-enhanced cluster-based routing for energy efficiency in UWSNs | J. Ambient Intelligence & Humanized Computing | Journal | https://link.springer.com/article/10.1007/s12652-026-05077-4 |
| 25 | 2026 | ~ Energy-efficient routing protocols for UWSNs with Improved Hermit Crab Optimization | Springer book chapter | Conf. | https://link.springer.com/chapter/10.1007/978-981-96-7991-1_23 |
| 26 | 2026 | ~ EERPUWSN: Innovative scheme for energy efficiency in underwater heterogeneous WSNs | ICISN 2025 (Springer, 2026) | Conf. | https://link.springer.com/chapter/10.1007/978-981-95-1746-6_11 |
| 27 | 2026 | ~ Energy-Aware Fuzzy Clustering and Multi-Hop Relay Optimization for UWSNs (EAFC) | Engineering Proceedings (MDPI) 163(1), 1 | Conf. | https://www.mdpi.com/2673-4591/163/1/1 |
| 28 | 2026 | ~ Hybrid cluster-based energy-efficient routing framework for UWSNs | Turkish Journal of Engineering | Journal | https://dergipark.org.tr/en/pub/tuje/article/1809878 |
| 29 | 2026 | ~ Adaptive clustering + secure cross-layer routing + AUV-assisted collection for marine environmental monitoring | Frontiers in Marine Science (10.3389/fmars.2026.1767826) | Journal | https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1767826/full |
| 30 | 2024 | Khan, Luque-Nieto, Siddique – Underwater Efficient Data Routing: Clustering-Travel Salesman Protocol (CTSP) | IEEE Access (10.1109/ACCESS.2024.3367012) | Journal | https://www.bohrium.com/paper-details/underwater-efficient-data-routing-clustering-travel-salesman-protocol-ctsp/970862687980355784-2649 |
| 31 | 2024 | Khan, Aamir, Otero – REOVA routing for mobile UASNs | J. Mar. Sci. Eng. 12(12), 2215 | Journal | https://portaldelainvestigacion.uma.es/documentos/678c2a0543f60728deb98e4a |
| 32 | 2024 | ~ Trust-model routing with two-hop void-node detection | Sensors 24(23), 7614 | Journal | https://mdpi.com/1424-8220/24/23/7614 |
| 33 | 2024 | ~ Multicast routing + hybrid clustering + fuzzy logic for UASNs | Wireless Networks 30 | Journal | https://link.springer.com/content/pdf/10.1007/s11276-023-03555-7.pdf |
| 34 | 2024 | ~ Energy-efficient routing for UWSNs based on improved ACO | Procedia Computer Science 247 | Conf. | https://www.sciencedirect.com/science/article/pii/S1877050924029533 |
| 35 | 2024 | Energy-Aware Depth-Based Routing Protocol for Enhanced Data Transmission in UWSNs | J. Science Technology & Research 5(1) 631–639 | Journal | https://philarchive.org/rec/MANEDR-3 |
| 36 | 2024 | Improved Depth-Based Routing for Prolonged Network Lifetime in Underwater Wireless Sensor Systems | J. Science Technology & Research 5(1) 625–630 | Journal | https://philarchive.org/versions/SENIDR |

## 3. AI / Reinforcement-learning based routing

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 37 | 2025 | Li, Wu, Zhu, Ren – A Q-Learning-Based Link-Aware Routing Protocol for UWSNs | J. Mar. Sci. Eng. 13(12), 2374 | Journal | https://www.mdpi.com/2077-1312/13/12/2374 |
| 38 | 2025 | Service-aware Q-learning-based routing protocol (SAQR) in UASNs | Computer Networks 257 | Journal | https://www.sciencedirect.com/science/article/pii/S1389128624008181 |
| 39 | 2025 | Karami Benmaran & Taheri Javan – RL + GAN based routing for UWSNs | Soft Computing Journal | Journal | https://scj.kashanu.ac.ir/article_114876.html |
| 40 | 2025 | A Reinforcement Learning-Based Telematic Routing Protocol for the Internet of Underwater Things | arXiv 2506.00133 | arXiv | https://arxiv.org/abs/2506.00133 |
| 41 | 2025 | Homaei et al. – RL-RPL-UA: RL-enhanced RPL for underwater IoT (open-source Aqua-Sim code) | arXiv / JITEL 2025 | arXiv | https://awesome.ecosyste.ms/projects/github.com%2Fhomaei%2Frl-rpl-ua |
| 42 | 2025 | Smart Interrupted Routing Based on Multi-head Attention Mask Mechanism-Driven MARL in Software-defined UASNs | arXiv 2509.15856 | arXiv | https://arxiv.org/abs/2509.15856 |
| 43 | 2026 | Prasad M. – Deep Reinforcement Learning-Enabled Energy-Efficient Routing Protocol for UWSNs | Int. J. Electronics & Telecommunications (10.24425/ijet.2026.157924) | Journal | https://ijet.pl/index.php/ijet/article/view/10.24425-ijet.2026.157924 |
| 44 | 2026 | Cross-Layer Cooperative Design of Network Coding and Distributed Opportunistic Routing for UASNs (10.1109/JSEN.2025.3633275) | IEEE Sensors Journal 26 | Journal | https://ui.adsabs.harvard.edu/abs/2026ISenJ..26.1329R/abstract |

## 4. MAC protocols and resource allocation

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 45 | 2025 | A Collision Avoidance MAC Protocol with Power Control for Adaptive Clustering Underwater Sensor Networks (APCC-MAC) | J. Mar. Sci. Eng. 13(1), 76 | Journal | https://doi.org/10.3390/jmse13010076 |
| 46 | 2025 | Deep Q-Learning Based Adaptive MAC Protocol with Collision Avoidance and Efficient Power Control for UWSNs | J. Mar. Sci. Eng. 13(3), 616 | Journal | https://doi.org/10.3390/jmse13030616 |
| 47 | 2025 | ~ Hybrid CSMA/CA–TDMA MAC with actor-critic RL for energy efficiency | Acoustics (MDPI) 7(3), 39 | Journal | https://www.mdpi.com/2624-599X/7/3/39 |
| 48 | 2025 | ~ MOMA-MAC: Multi-objective UWA MAC based on multi-agent RL | Drones 9(2), 123 | Journal | https://mdpi.com/2504-446X/9/2/123 |
| 49 | 2025 | Feng et al. – A Fair MAC Protocol Based on Dual Bandwidth Allocation Iterations in UASNs (FBA-MAC) | Int. J. Communication Systems (10.1002/dac.6017) | Journal | https://onlinelibrary.wiley.com/doi/abs/10.1002/dac.6017 |
| 50 | 2025 | ~ Survey of energy-efficient MAC protocols for underwater acoustic networks | J. Network and Computer Applications 235 | Journal | https://ro.ecu.edu.au/ecuworks2022-2026/5266/ |
| 51 | 2025 | ~ Multi-node acoustic MAC for tsunami/earthquake monitoring (closed-form utilization & energy analysis) | J. Mar. Sci. Eng. 14(1), 21 | Journal | https://www.mdpi.com/2077-1312/14/1/21 |
| 52 | 2025 | Joint Link Scheduling and Power Allocation in Imperfect and Energy-Constrained UWSNs (ICRL-JSA, deep MARL) | arXiv 2508.07679 | arXiv | https://arxiv.org/abs/2508.07679 |
| 53 | 2025 | Traffic Load-Aware Resource Management Strategy for UWSNs | arXiv 2508.08555 | arXiv | https://arxiv.org/abs/2508.08555 |
| 54 | 2025 | ~ MARL-TS: Cross-layer transmission scheduling for time-varying UWA channels | J. Unmanned Undersea Systems 33(2) 261–271 | Journal | https://sxwrxtxb.xml-journal.net/en/article/doi/10.11993/j.issn.2096-3920.2025-0015 |
| 55 | 2025 | ~ Two-level multi-armed-bandit RL link adaptation (modulation, power, feedback) for UANs | IEEE Globecom 2025 (arXiv 2602.20105) | Conf. | https://arxiv.org/abs/2602.20105 |
| 56 | 2026 | Is DRL-based MAC Ready for Underwater Acoustic Networks? Exploring Its Practicality in Real Field Experiments | arXiv 2605.10144 | arXiv | https://arxiv.org/abs/2605.10144 |
| 57 | 2026 | An Asynchronous Triggered MAC Protocol for Underwater Acoustic Networks (AT-MAC) | arXiv 2608.10533 | arXiv | https://arxiv.org/abs/2608.10533 |
| 58 | 2026 | Achieving Rate-Concurrency Balance for Underwater Concurrent Random Access | arXiv 2608.01254 | arXiv | https://arxiv.org/abs/2608.01254 |
| 59 | 2026 | A Deep Reinforcement Learning Approach for Joint Resource Allocation in Time-Varying Underwater Acoustic Cooperative Networks | J. Mar. Sci. Eng. 14(7), 616 | Journal | https://www.mdpi.com/2077-1312/14/7/616 |
| 60 | 2024 | ~ Q-learning energy-efficient MAC for UWSNs (collision avoidance, lifetime) | Electronics 13(22), 4388 | Journal | https://mdpi.com/2079-9292/13/22/4388 |
| 61 | 2024 | ~ Multi-agent RL medium-access policy for energy-harvesting UASNs | Sensors 24(17), 5791 | Journal | https://mdpi.com/1424-8220/24/17/5791 |

## 5. AUV-assisted data collection, AoI and mobility

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 62 | 2025 | Cao, Chen, Cheng – Joint AoI and energy optimization for multi-AUV data collection in UASNs | Frontiers in Marine Science (10.3389/fmars.2025.1580751) | Journal | https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2025.1580751/full |
| 63 | 2025 | Almuzaini & Savkin – AUV Trajectory Planning for Optimized Sensor Data Collection in IoUT | MDPI (DOAJ-indexed) | Journal | https://library.kab.ac.ug/Record/doaj-art-c2ec51f030d2470f892a8de9f825c87a/Description |
| 64 | 2025 | Xu et al. – Encoder-Decoder Based Deep RL for Multi-AUV Assisted Data Collection in UWSNs | Univ. of Essex repository (venue not shown) | Repository | https://repository.essex.ac.uk/42346/ |
| 65 | 2025 | Wei et al. – A Channel-Aware AUV-Aided Data Collection Scheme Based on Deep RL | MDPI (AGRIS-indexed) | Journal | https://agris.fao.org/search/en/records/68d2839db3b40a20d617fe3e |
| 66 | 2025 | SafeDiver: Cooperative AUV-USV Assisted Diver Communication via Multi-agent RL | arXiv 2509.11508 | arXiv | https://arxiv.org/abs/2509.11508 |
| 67 | 2026 | Multi-AUV Trajectory Learning for Sustainable Underwater IoT with Acoustic Energy Transfer | arXiv 2604.04079 | arXiv | https://arxiv.org/abs/2604.04079 |
| 68 | 2026 | ~ Review of 56 AUV-assisted data-gathering protocols (2011–2025), six-class taxonomy | Preprints.org 202605.1576 | Preprint | https://www.preprints.org/manuscript/202605.1576 |
| 69 | 2026 | Learning to Stay Fresh: A Self-Learning Semantic Framework for Underwater IoT | arXiv 2607.16902 | arXiv | https://arxiv.org/abs/2607.16902 |
| 70 | 2024 | High-Efficiency Clustering Routing Protocol in AUV-Assisted Underwater Sensor Networks (HECRA) | Sensors 24(20), 6661 | Journal | https://www.mdpi.com/1424-8220/24/20/6661 |
| 71 | 2024 | VoI and Energy-Aware AUV-Assisted Data Collection for Internet of Underwater Things | (ResearchGate record; venue not shown) | Unconfirmed venue | https://www.researchgate.net/publication/377075271 |
| 72 | 2024 | Environment and Energy-Aware AUV-Assisted Data Collection for the Internet of Underwater Things | (ResearchGate record; venue not shown) | Unconfirmed venue | https://www.researchgate.net/publication/380167340 |
| 73 | 2024 | Boundary Control Behaviors of Multiple Low-cost AUVs Using Acoustic Communication | arXiv 2412.00118 | arXiv | https://arxiv.org/abs/2412.00118 |

## 6. Clustering and metaheuristics

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 74 | 2025 | HDLCA: Hunger Driven Lion Clustering Algorithm, energy-efficient & scalable clustering for underwater nodes | Scientific Reports 15, 33292 | Journal | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12475414/ |
| 75 | 2024 | Energy-efficient artificial fish swarm-based clustering protocol for enhancing network lifetime in UWSNs | EURASIP J. Wireless Commun. & Networking (10.1186/s13638-024-02422-z) | Journal | https://link.springer.com/article/10.1186/s13638-024-02422-z |

## 7. Localization, positioning, time synchronization

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 76 | 2025 | Wang, Guo, Li, Chen, Wei – An Underwater Localization Algorithm Based on the Internet of Vessels | J. Mar. Sci. Eng. 13(3), 535 | Journal | https://doi.org/10.3390/jmse13030535 |
| 77 | 2025 | Exploration of contemporary modernization in UWSNs in the context of localization incl. ML/DL opportunities | Scientific Reports (10.1038/s41598-025-89916-y) | Journal | https://www.nature.com/articles/s41598-025-89916-y |
| 78 | 2025 | ~ Range-Based Localization in UWSNs Using an Optimization Algorithm (recursive position estimation) | Ad Hoc & Sensor Wireless Networks 60 | Journal | https://search.napstic.cn/literature/periodical/0220250400201286 |
| 79 | 2025 | Unified Underwater Communication, Positioning, Navigation and Timing Network System Design and Application | J. Mar. Sci. Eng. 13(6), 1094 | Journal | https://www.mdpi.com/2077-1312/13/6/1094 |
| 80 | 2025 | ~ LT-Sync: Lightweight time synchronization for high-speed mobile UASNs | MDPI (DOAJ-indexed) | Journal | https://library.kab.ac.ug/Record/doaj-art-53815c4ef37b46cd8c2c2290a6f159d7/Description |
| 81 | 2025 | A Comprehensive Survey on Underwater Acoustic Target Positioning and Tracking | arXiv 2506.14165 | arXiv | https://arxiv.org/abs/2506.14165 |
| 82 | 2025 | Robust Underwater Localization of Buoyancy-Driven microFloats Using Acoustic Time-of-Flight (field trials, TDMA modems) | arXiv 2512.12233 | arXiv | https://arxiv.org/abs/2512.12233 |
| 83 | 2026 | Low-Complexity RSS-based Underwater Localization with Unknown Transmit Power | arXiv 2601.12278 | arXiv | https://arxiv.org/abs/2601.12278 |
| 84 | 2026 | Resource-Aware Topology Management for ISAC-Enabled TDOA Localization in IoUT Networks | arXiv 2607.24028 | arXiv | https://arxiv.org/abs/2607.24028 |
| 85 | 2026 | ~ MARL-based AUV beacon selection for localization (TD3/SAC/MADDPG) | J. Mar. Sci. Eng. 14, 262 | Journal | https://mdpi-res.com/d_attachment/jmse/jmse-14-00262/article_deploy/jmse-14-00262.pdf |
| 86 | 2026 | Multi-Source Sensor Fusion Localization Method for AUVs Based on Deep Learning | J. Mar. Sci. Eng. 14(11), 1064 | Journal | https://doi.org/10.3390/jmse14111064 |
| 87 | 2026 | ~ Novel underwater target-tracking method in UASNs via collaborative DRL | Information Fusion | Journal | https://scholar.xjtu.edu.cn/en/publications/a-novel-underwater-target-tracking-method-in-uasns-via-collaborat/ |
| 88 | 2024 | Efficient AUV-Aided Localization for Large-Scale Underwater Acoustic Sensor Networks | IEEE Internet of Things Journal 11(19) | Journal | https://research.buaa.edu.cn/en/publications/efficient-auv-aided-localization-for-large-scale-underwater-acous/ |
| 89 | 2024 | Ouyang et al. – Underwater Network Time Synchronization Method Based on Probabilistic Graphical Models | J. Mar. Sci. Eng. 12(11), 2079 | Journal | https://www.mdpi.com/2077-1312/12/11/2079 |
| 90 | 2024 | Sun, Ouyang, Han – DC-Sync: time synchronization for mobile UASNs | IEEE Access | Journal | https://doaj.org/article/00129ebd13084ecab53bff95b2d0ad20 |
| 91 | 2024 | Bhardwaj & Kush – Review on Localization Algorithm in Underwater Sensor Network | IC3Com 2024 (SciTePress) | Conf. | https://www.scitepress.org/PublishedPapers/2024/133431 |

## 8. Security, trust, intrusion detection

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 92 | 2025 | Jiang, Zhou, Luo, Cui, Wang, Song – Attack Detection and Optimal Deployment for Underwater Constrained WSNs via Hybrid Trust Evidence | IEEE Trans. Network Science & Engineering | Journal | https://mdsoar.org/items/a0b7a078-5e43-4a5e-9437-bea694bef3e8 |
| 93 | 2025 | Shah et al. – A flexible and lightweight signcryption scheme for UWSNs | Scientific Reports (10.1038/s41598-025-95836-8) | Journal | https://library.kab.ac.ug/Record/doaj-art-d44485404fd146609fd4677380dbf520/Description |
| 94 | 2025 | Zhang et al. – Trust Model for UWSNs Based on Variational Autoencoders | J. Underwater Unmanned Systems | Journal | https://library.kab.ac.ug/Record/doaj-art-7dfbd5e7662d4ceba1e541091f429b2a |
| 95 | 2025 | Histogram Gradient Boosting Classifier Based UWSN Cyber Attack Detection | IJACSA 16(12) | Journal | https://thesai.org/Downloads/Volume16No12/Paper_17-Histogram_Gradient_Boosting_Classifier_Based_UWSN_Cyber_Attack_Detection.pdf |
| 96 | 2025 | ~ Random-Forest attack detection for UWSNs | J. Européen des Systèmes Automatisés (IIETA) | Journal | https://www.iieta.org/download/file/fid/176575 |
| 97 | 2025 | Enhancing Sybil Attack Detection and Prevention in UWSNs through a Hybrid Model (blockchain + anomaly detection) | Zenodo record 16741992 | Preprint | https://zenodo.org/records/16741992 |
| 98 | 2025 | ~ High-speed bio-inspired covert underwater acoustic communication for Underwater IoT (10.1109/JIOT.2025.3604025) | IEEE Internet of Things Journal | Journal | https://api.openalex.org/works/doi:10.1109%2FJIOT.2025.3604025 |
| 99 | 2026 | ~ Systematic review of intrusion detection for the Internet of Underwater Things | Recent Progress in Science & Engineering 2(4), 022 | Journal | https://www.lidsen.com/journals/rpse/rpse-02-04-022 |
| 100 | 2026 | A blockchain-enabled framework for secure and efficient data transmission in underwater sensor networks using advanced cryptographic techniques | PMC-indexed journal article | Journal | https://pmc.ncbi.nlm.nih.gov/articles/PMC13187329/ |
| 101 | 2024 | Securing Underwater Wireless Sensor Networks: A Review of Attacks and Mitigation Techniques | IEEE Access 12, 161096–161133 | Journal | https://portaldelainvestigacion.uma.es/documentos/673a637b10dcc339fb2b4695?lang=en |
| 102 | 2024 | Das et al. – AIDPS: Adaptive Intrusion Detection and Prevention System for UASNs | IEEE/ACM Trans. Networking (arXiv 2309.07730) | Journal | https://eprints.whiterose.ac.uk/id/eprint/209244 |
| 103 | 2024 | ~ DRFTM: Dynamic trust model (random forest + DRL) for UASNs | Applied Sciences 14(8), 3374 | Journal | https://mdpi.com/2076-3417/14/8/3374 |
| 104 | 2024 | Security and Reliability of Internet of Underwater Things: Architecture, Challenges, and Opportunities | ACM Computing Surveys (10.1145/3700640) | Journal | https://dl.acm.org/doi/10.1145/3700640 |

## 9. Architecture: digital twin, SDN, edge/federated learning, space-air-ground-sea

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 105 | 2025 | Song et al. – A Digital Twin-based Intelligent Network Architecture for UASNs (DTNA) | IEEE Trans. Mobile Computing 24(9) (arXiv 2410.20151) | Journal | https://arxiv.org/abs/2410.20151 |
| 106 | 2025 | Multicast reliable traffic engineering technique for SDN-Fog based IoUT | Scientific Reports 15, 9069 | Journal | https://www.nature.com/articles/s41598-025-93383-w |
| 107 | 2025 | Federated learning-based privacy-preserving IoUT: vision, architecture, computing, taxonomy, and future directions | J. Supercomputing (10.1007/s11227-025-07322-7) | Journal | https://link.springer.com/article/10.1007/s11227-025-07322-7 |
| 108 | 2025 | Unified Design of Space-Air-Ground-Sea Integrated Maritime Communications | arXiv 2508.09817 | arXiv | https://arxiv.org/abs/2508.09817 |
| 109 | 2025 | ~ Underwater digital-twin sensor networks for maritime monitoring (EHC-ANFIS) | Preprints.org | Preprint | https://www.preprints.org/frontend/manuscript/0ec75ec093aa6fc33289933df548d5a3/download_pub |
| 110 | 2026 | TFL-IoUT: Transfer federated learning for privacy-preserving coral classification on the IoUT | Multimedia Tools & Applications | Journal | https://link.springer.com/article/10.1007/s11042-026-21678-9 |
| 111 | 2026 | Multi-Level Multi-Technology Underwater Networks: Challenges and Opportunities for Marine Monitoring | Network (MDPI) 6(1), 2 | Journal | https://doi.org/10.3390/network6010002 |
| 112 | 2026 | Advancements of Topology Control in Internet of Underwater Things | ICIT '25 (ACM, 2026) | Conf. | https://dl.acm.org/doi/full/10.1145/3787330.3787340 |
| 113 | 2024 | AUV-aided computing offloading for multi-tier underwater computing: A Stackelberg game learning approach | Ocean Engineering | Journal | https://www.sciencedirect.com/science/article/abs/pii/S0029801824004463 |
| 114 | 2024 | Design and Performance Evaluation of SEANet, a Software-defined Networking Platform for the IoUT | arXiv 2403.01009 | arXiv | https://arxiv.org/abs/2403.01009 |
| 115 | 2024 | A Survey on Resource Management in Joint Communication and Computing-Embedded SAGIN | arXiv 2403.17400 | arXiv | https://arxiv.org/abs/2403.17400 |

## 10. Physical layer: channel, modulation, modems, AI for signals

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 116 | 2025 | Toward Intelligent Underwater Acoustic Systems: Systematic Insights into Channel Estimation and Modulation Methods | Electronics 14(15), 2953 | Journal | https://doi.org/10.3390/electronics14152953 |
| 117 | 2025 | ~ ML framework for UWA channel estimation exploiting delay-Doppler sparsity (10.1109/SYMPOL68153.2025.11395920) | IEEE SYMPOL 2025 | Conf. | https://iro.uiowa.edu/esploro/outputs/conferenceProceeding/Underwater-Acoustic-Channel-Estimation-Using-Sparse/9985139488202771 |
| 118 | 2025 | ~ Convolution-recurrent neural network channel estimation for underwater OFDM | Frontiers in Marine Science (10.3389/fmars.2025.1671853) | Journal | https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2025.1671853/full |
| 119 | 2025 | ~ Underwater acoustic communications (review article; title taken from PDF file name) | Nature Reviews Electrical Engineering (NUS ARL copy) | Journal | https://arl.nus.edu.sg/wp-content/uploads/2025/03/Underwater-acoustic-communications.pdf |
| 120 | 2025 | ~ Low-cost underwater acoustic array testbed | J. Acoust. Soc. Am. 157(4_Suppl) A351 | Conf. | https://pubs.aip.org/asa/jasa/article/157/4_Supplement/A351/3354266/Low-cost-underwater-acoustic-array-testbed |
| 121 | 2026 | ~ Open-set modulation recognition for UWA communication based on Multi-Path ResNet (10.1121/10.0043867) | J. Acoust. Soc. Am. | Journal | https://pubmed.ncbi.nlm.nih.gov/42133458/ |
| 122 | 2026 | Heterogeneous 2D/1D Signal Representation Fusion for UWA Modulation Recognition Under Distribution Shift | arXiv 2606.23702 | arXiv | https://arxiv.org/abs/2606.23702 |
| 123 | 2026 | ~ Temporal deep-learning architectures for predicting UWA channel variability | Springer book chapter | Conf. | https://link.springer.com/chapter/10.1007/978-3-032-17846-6_12 |
| 124 | 2026 | Modulation Feature Enhancement with a Multi-Stage Attention Network for Underwater Acoustic Target Recognition | arXiv 2605.16304 | arXiv | https://arxiv.org/abs/2605.16304 |
| 125 | 2026 | From Signals to Evidence: Interpretable Underwater Acoustic Target Sensing with LLMs – Part I | arXiv 2610.22064 | arXiv | https://arxiv.org/abs/2610.22064 |
| 126 | 2026 | Underwater Acoustic Data Transmission in the Presence of Challenging Multipath Conditions and Shadow Zones: Sea Trial Analysis and Lessons Learned | Electronics 15(2), 358 | Journal | https://www.mdpi.com/2079-9292/15/2/358 |
| 127 | 2026 | ~ Construction of an experimental platform for UASNs and analysis of experimental results | Wireless Networks (10.1007/s11276-026-04174-8) | Journal | https://link.springer.com/article/10.1007/s11276-026-04174-8 |
| 128 | 2025 | ~ EPASNet: experimental platform for acoustic sensor networks at sea (doi 10.16300/j.cnki.1000-3630.24012701) | Technical Acoustics (Chinese journal) | Journal | https://files.sciengine.com/pdfs/1000-3630/5EC59442DF6B4C2C8C042DBD0F3472C4.pdf |
| 129 | 2024 | ~ Modulation recognition of UWA communication signals based on deep learning | EURASIP J. Adv. Signal Process. (10.1186/s13634-024-01200-9) | Journal | https://link.springer.com/article/10.1186/s13634-024-01200-9 |
| 130 | 2024 | ~ Software-defined underwater modem: first sea-trial campaign (Padova / SubSeaPulse) | Univ. Padova research record | Conf. | https://research.unipd.it/handle/11577/3549085 |

## 11. Optical, hybrid optical–acoustic, magnetic-induction links

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 131 | 2025 | Armghan et al. – Hybrid underwater optical + UWB link for sensor networks | Frontiers in Physics (10.3389/fphy.2025.1650284) | Journal | https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2025.1650284/full |
| 132 | 2025 | Arya – Comprehensive review of underwater optical wireless communication systems | J. Optical Communications (10.1515/joc-2025-0106) | Journal | https://www.degruyterbrill.com/document/doi/10.1515/joc-2025-0106/pdf |
| 133 | 2025 | Sarkar & Barua – UOWC performance analysis in clear oceanic water | J. Optical Communications (10.1515/joc-2025-0211) | Journal | https://www.degruyterbrill.com/document/doi/10.1515/joc-2025-0211/pdf |
| 134 | 2025 | ~ Progress and trends in underwater wireless optical communication (invited review) | Acta Optica Sinica 45(13), 1306016 | Journal | https://m.researching.cn/articles/OJ4b6cc3438c439316 |
| 135 | 2025 | ~ Range extension for underwater MI communication via parametric analysis of MI coils in IoUT | Electronics 14(22), 4543 | Journal | https://doi.org/10.3390/electronics14224543 |
| 136 | 2025 | Through-the-Earth Magnetic Induction Communication and Networking: A Comprehensive Survey | arXiv 2510.14854 | arXiv | https://arxiv.org/abs/2510.14854 |
| 137 | 2026 | Machine Learning for Underwater Optical Wireless Communication Systems: A Comprehensive Survey | arXiv 2609.22294 | arXiv | https://arxiv.org/abs/2609.22294 |
| 138 | 2026 | Joseph & Anandan – Hybrid optical–acoustic underwater communication with joint modulation and bio-inspired power optimization | Int. J. Electronics & Telecommunications | Journal | https://wydawnictwo.pan.pl/index.php/ijet/article/view/1115 |
| 139 | 2024 | ~ Optical/acoustic hybrid underwater modem prototype (sea test) | Shimadzu Review 81 | Journal | https://www.shimadzu.com/about/magazine/tec_news/srv81_12/report04.html |
| 140 | 2024 | Rodionov – Application of multi-frequency underwater communication systems based on magnetic induction | Underwater Investigations and Robotics | Journal | https://www.researchgate.net/publication/388174401 |
| 141 | 2024 | ~ A New Methodology for the Development of Underwater Magnetic Pulse Wireless Communication | J. Supercond. Nov. Magn. (10.1007/s10948-024-06870-y) | Journal | https://link.springer.com/article/10.1007/s10948-024-06870-y |
| 142 | 2024 | Bamhdi – Underwater Magnetic Induction Communication Range Enhancement: Survey and Comprehensive Evaluation | IJASCA | Journal | https://www.researchgate.net/publication/383214213 |

## 12. Energy harvesting, deployment, coverage

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 143 | 2025 | Nordfjord, Thorsteinsson, Andersen – Powering underwater robotic sensor networks: systematic review (energy harvesting & WPT) | J. Mar. Sci. Eng. 13(9), 1728 | Journal | https://doi.org/10.3390/jmse13091728 |
| 144 | 2025 | Vignesh & Sukumaran – Underwater energy harvesting model for agricultural applications using stochastic network calculus | IJECE 15(2) 2031–2041 | Journal | https://ijece.iaescore.com/index.php/IJECE/article/view/36907 |
| 145 | 2025 | ~ Long-range underwater energy-harvesting power bank system for UWSNs | ICRAMET 2025 | Conf. | https://researcher.manipal.edu/en/publications/long-range-underwater-energy-harvesting-power-bank-system-for-mul/ |
| 146 | 2025 | Tyagi, Shah, Srivastava – Greedy bathymetry & transmission-loss aware sensor deployment for UASNs | PeerJ Computer Science cs-3321 | Journal | https://peerj.com/articles/cs-3321 |
| 147 | 2024 | ~ Energy-efficient mobile-sink data collection in WSNs with non-uniform data (terrestrial WSN reference) | Scientific Reports (10.1038/s41598-024-79825-x) | Journal | https://www.nature.com/articles/s41598-024-79825-x |

## 13. Surveys and editorials (2024–2026)

| # | Year | Title | Venue | Status | Link |
|---|---|---|---|---|---|
| 148 | 2025 | Stewart, Ayaz, Fough, Prabhu – Towards the underwater internet of things for subsea oil and gas monitoring (survey) | Internet of Things (Elsevier) 30 | Journal | https://rgu-repository.worktribe.com/output/2662977 |
| 149 | 2025 | Underwater communication technologies: a review | Telecommunication Systems (10.1007/s11235-025-01279-x) | Journal | https://link.springer.com/article/10.1007/s11235-025-01279-x |
| 150 | 2025 | Integrating Environmental Awareness in Underwater Acoustic Networks: A Comprehensive Review | Acoustics Australia (10.1007/s40857-025-00374-y) | Journal | https://link.springer.com/article/10.1007/s40857-025-00374-y |
| 151 | 2025 | Underwater Sensor Networks for Communication, Navigation, and Localization (editorial) | Sensors 25(3), 593 | Journal | https://www.mdpi.com/1424-8220/25/3/593 |
| 152 | 2026 | Semantic Communication for the Internet of Underwater Things: Architectures, Applications, Challenges, and Future Directions | arXiv 2601.13289 | arXiv | https://arxiv.org/abs/2601.13289 |
| 153 | 2026 | Omeke et al. – Machine Learning for the Internet of Underwater Things: From Fundamentals to Implementation | arXiv 2603.07413 | arXiv | https://arxiv.org/abs/2603.07413 |
| 154 | 2026 | ~ A Review of Energy-Efficient Routing Protocols for Underwater Acoustic Wireless Sensor Networks | Informatics (MDPI) 13(10), 168 | Journal | https://www.mdpi.com/2227-9709/13/10/168 |
| 155 | 2024 | Survey of AI-driven routing protocols in underwater acoustic networks for enhanced communication efficiency | Ocean Engineering 314 | Journal | https://www.sciencedirect.com/science/article/abs/pii/S0029801824029445 |

---

## Year distribution

| Year | Count |
|---|---|
| 2026 | 42 |
| 2025 | 79 |
| 2024 | 34 |
| **Total** | **155** |

## Removed during verification

Removed because the search couldn't confirm the year, the title or a working link: duplicate RPLUW/M preprint, EEDCCR (ICDCOT 2024, no link), the void-repair survey (no year), the ocean-current void-avoidance protocol (no year), an "Energy and Path-Aware Reliable Routing" record (no year), a semi-cooperative MARL MAC record (no year), the Cluster-Dragonfly routing paper (no year), a Scientific Reports 2026 in-press article (title not visible), a JoWUA 2026 paper (title not visible), and an IEEE IoTJ fuzzy-flooding paper (title search returned nothing).
