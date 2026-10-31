"""Build the high-impact-factor literature survey workbook (literature_survey_IF5plus.xlsx)."""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

OUT = "literature_survey_IF5plus.xlsx"
TOPIC = ("Double Q-learning energy- and void-aware depth-based routing (DQ-EVDR) "
         "for underwater acoustic sensor networks, evaluated in ns-3")

# Impact factors: journalmetrics.org (JCR-based) unless noted; checked 31-Oct-2026.
IF = {
    "IEEE Commun. Surveys & Tutorials": ("46.7", "https://www.journalmetrics.org/journal/ieee-communications-surveys-and-tutorials"),
    "ACM Computing Surveys": ("28.0", "https://www.journalmetrics.org/journal/acm-computing-surveys"),
    "Information Fusion": ("15.5", "https://www.journalmetrics.org/journal/information-fusion"),
    "IEEE J. Sel. Areas Commun.": ("13.081 (JCR 2021, Wikipedia; newer value not confirmed)", "https://en.wikipedia.org/wiki/IEEE_Journal_on_Selected_Areas_in_Communications"),
    "IEEE Trans. Wireless Commun.": ("10.7", "https://www.journalmetrics.org/journal/ieee-transactions-on-wireless-communications-2"),
    "IEEE Trans. Mobile Computing": ("9.2", "https://www.journalmetrics.org/journal/ieee-transactions-on-mobile-computing"),
    "IEEE Internet of Things Journal": ("8.9 (JCR 2024, journal site)", "https://ieee-iotj.org/history/impactfactorsperyear/"),
    "Engineering Applications of AI": ("8.0", "https://www.journalmetrics.org/journal/engineering-applications-of-artificial-intelligence"),
    "J. Network & Computer Applications": ("8.0", "https://www.journalmetrics.org/journal/journal-of-network-and-computer-applications"),
    "IEEE Trans. Network Sci. & Eng.": ("7.9", "https://www.journalmetrics.org/journal/ieee-transactions-on-network-science-and-engineering"),
    "IEEE Trans. Vehicular Technology": ("7.5 (6.1 for 2024 per VTS)", "https://www.journalmetrics.org/journal/ieee-transactions-on-vehicular-technology"),
    "Internet of Things (Elsevier)": ("7.1", "https://www.journalmetrics.org/journal/internet-of-things-3"),
    "Ocean Engineering": ("5.5", "https://www.journalmetrics.org/journal/ocean-engineering"),
}

NO_DS = "None - synthetic simulation scenarios (no external dataset reported)"
NO_CODE = "No - no public code found (searched)"
UNK = "Not stated in abstract/metadata"

# cols: year, title, authors, journal, vol, doi, link, area, model, learning, simulator, dataset, ds_link, code, code_link, score, why, notes
P = [
 # ---------------- 2026 ----------------
 (2026, "A novel underwater target tracking method in UASNs via collaborative deep reinforcement learning",
  "Zheng, Liu, Zhang, Dong", "Information Fusion", "Mar 2026 issue", "10.1016/j.inffus.2025.103797",
  "https://scholar.xjtu.edu.cn/en/publications/a-novel-underwater-target-tracking-method-in-uasns-via-collaborat/",
  "Target tracking / sensor scheduling", "Two cooperating agents trained with PPO; multi-agent architecture with global critic; joint sensor scheduling + data fusion",
  "Multi-agent DRL (PPO)", "Simulation + real-world experiment",
  "Own simulation + own real-world experiment data (not released)", "-", NO_CODE, "-", 2,
  "DRL for energy-efficient decisions in UASNs; different task (tracking, not routing)", "Reports >=15% energy-efficiency gain (abstract)."),
 (2026, "Propagation-Aware Scheduling MAC Protocol for Reliable Underwater Swarmed AUV Communications Networks",
  "Yun, Oh, Lim", "IEEE Internet of Things Journal", "vol. 13, no. 5, pp. 8749-8762", "10.1109/JIOT.2025.3642314",
  "https://doi.org/10.1109/JIOT.2025.3642314", "MAC (AUV swarm)", "Propagation-delay-aware scheduling MAC", "None (protocol design)", UNK,
  NO_DS, "-", NO_CODE, "-", 2, "MAC layer below our routing layer; useful for MAC choice in ns-3",
  "Metadata from ACM DL citation record; abstract not seen."),
 (2026, "Multi-AUV Cooperative Path Planning Based on Plasticity Injection TD3 Framework for IoUT Data Collection",
  "See link", "IEEE Trans. Mobile Computing", "2026, issue 10", "See link",
  "https://www.computer.org/csdl/journal/tm/2026/10/11535179/2gM5JrpWJSo", "AUV data collection",
  "TD3 with plasticity injection for multi-AUV path planning", "DRL (TD3, actor-critic)", UNK,
  NO_DS, "-", NO_CODE, "-", 2, "Learning-based IoUT data collection; AUV mobility rather than multi-hop routing", "Authors/DOI not shown in results."),
 (2026, "Underwater Visual-Inertial-Acoustic-Depth Fusion Localization With DVL Preintegration for Degraded Environments",
  "Ding, Zhang, Jiang, Lei", "IEEE Internet of Things Journal", "vol. 13, no. 20", "10.1109/JIOT.2026.3711172",
  "https://doi.org/10.1109/JIOT.2026.3711172", "Localization (AUV)", "Visual-inertial-acoustic-depth sensor fusion with DVL preintegration",
  "None (estimation/fusion)", UNK, UNK, "-", NO_CODE, "-", 1, "Navigation/localization only; background", "Metadata from citation record."),
 # ---------------- 2025 ----------------
 (2025, "An intelligent Q-learning-based tree routing method in underwater acoustic sensor networks (QTRU)",
  "P. Khoshvaght, A. Haider, A. M. Rahmani, M. Altulyan, et al.", "Engineering Applications of AI", "vol. 152, art. 110753, Jul 2025", "pii S0952197625007535 (DOI: see link)",
  "https://www.sciencedirect.com/science/article/abs/pii/S0952197625007535", "Routing (RL)",
  "Q-learning tree routing; reward = node depth + residual energy + transmission-success probability + candidate-set size; loop-prevention screening",
  "Tabular Q-learning", "NS-2 (vs 3 routing baselines)", NO_DS, "-", NO_CODE, "-", 5,
  "Closest match: Q-learning + depth + residual energy + link success; single-estimator Q-learning in NS-2 (we: Double Q in ns-3)",
  "Confirm DOI on ScienceDirect page."),
 (2025, "Fuzzy-Based Deterministic Routing With Probabilistic Flooding in Underwater Acoustic Sensor Networks",
  "Pang, Guo, Liu", "IEEE Internet of Things Journal", "2025 (online Dec 2025)", "10.1109/JIOT.2025.3612375",
  "https://doi.org/10.1109/JIOT.2025.3612375", "Routing (fuzzy)", "Fuzzy-logic deterministic forwarding + probabilistic flooding",
  "None (fuzzy inference)", UNK, NO_DS, "-", NO_CODE, "-", 4, "Fuzzy routing baseline candidate for our comparison",
  "Found only in reference lists of two citing papers; exact-title search returned no publisher page. VERIFY via DOI."),
 (2025, "Joint Power Control and Multi-Path Routing for Internet of Underwater Things in Varying Environments",
  "C. Xu, S. Song, et al.", "IEEE Internet of Things Journal", "2025", "10.1109/JIOT.2025.3527692",
  "https://doi.org/10.1109/JIOT.2025.3527692", "Routing + power control", "Joint power control and multi-path routing", UNK, UNK,
  NO_DS, "-", NO_CODE, "-", 4, "Energy-aware multi-path routing in time-varying channels; strong related work", "From JLU faculty publication list."),
 (2025, "Aqua-Sim Fourth Generation: Towards General and Intelligent Simulation for Underwater Acoustic Networks",
  "Jilin University group (see arXiv for full list)", "IEEE Internet of Things Journal", "vol. 12, 2025", "arXiv:2410.20698",
  "https://arxiv.org/abs/2410.20698", "Simulator (ns-3)",
  "ns-3-based simulator; MATLAB + C++ + Python package for AI training; Thorp & Bellhop propagation; BPSK/QPSK; AUV/glider mobility",
  "Supports AI/RL models (framework)", "ns-3 (itself); validated against field experiments",
  "Field-experiment measurements used for validation (not released as dataset)", "-",
  "YES", "https://github.com/JLU-smartocean/aqua-sim-fg", 4,
  "Candidate platform for implementing DQ-EVDR in ns-3", "Repo link taken from the paper; README/licence not checked."),
 (2025, "A Digital Twin-Based Intelligent Network Architecture for Underwater Acoustic Sensor Networks (DTNA)",
  "Song, et al.", "IEEE Trans. Mobile Computing", "vol. 24, no. 9, 2025", "arXiv:2410.20151",
  "https://research.buaa.edu.cn/en/publications/a-digital-twin-based-intelligent-network-architecture-for-underwa/",
  "Architecture / digital twin", "Local + global twins; MARL in global twin; task-oriented network slicing", "MARL", UNK,
  "Twin-generated data supplements scarce real data (no public dataset)", "-", NO_CODE, "-", 3,
  "Shows RL training data scarcity problem in UASNs", ""),
 (2025, "Traffic Load-Aware Resource Management Strategy for Underwater Wireless Sensor Networks (TARM)",
  "See link", "IEEE Trans. Mobile Computing", "vol. 24, no. 1, 2025", "arXiv:2508.08555",
  "https://www.computer.org/csdl/journal/tm/2025/01/10679618/20b3iOe0Mrm", "MAC / resource allocation",
  "Dec-POMDP; neighbour-listening traffic-load estimation; action-space pruning; link scheduling + power + rate", "Deep MARL", "Simulation",
  NO_DS, "-", NO_CODE, "-", 3, "RL on noisy local observations in UWSNs; single-hop only (no routing)", "Authors not confirmed in results."),
 (2025, "Multi-AUV Cooperative Underwater Multi-Target Tracking Based on Dynamic-Switching-Enabled Multi-Agent Reinforcement Learning",
  "S. Wang, C. Lin, G. Han, Z. Li, et al.", "IEEE Trans. Mobile Computing", "vol. 24, no. 5, pp. 4296-4311, May 2025", "10.1109/TMC.2024.3521889",
  "https://dl.acm.org/doi/10.1109/TMC.2024.3521889", "AUV tracking", "HSARL hierarchical software-defined multi-AUV RL; dynamic-switching attention; reward reshaping",
  "MARL", "Simulation", NO_DS, "-", NO_CODE, "-", 1, "AUV task, not sensor routing", "arXiv 2404.13654."),
 (2025, "Underwater Target Tracking Based on Interrupted Software-Defined Multi-AUV Reinforcement Learning: A Multi-AUV Time-Saving MARL Approach",
  "See link", "IEEE Trans. Mobile Computing", "vol. 24, no. 3, pp. 2124-2136, Mar 2025", "10.1109/TMC.2024.3490545",
  "https://dl.acm.org/doi/abs/10.1109/TMC.2024.3490545", "AUV tracking", "Software-defined multi-AUV MARL with interruption handling", "MARL", UNK,
  NO_DS, "-", NO_CODE, "-", 1, "AUV task; background on interrupted acoustic links", ""),
 (2025, "Integrated Sensing and Communication for Underwater Acoustic Networks Based on Deep Reinforcement Learning (Deep UWA-ISAC)",
  "X. Ye, Y. Mao, X. Yu, J. Xu, et al.", "IEEE Trans. Wireless Commun.", "Jan 2025", "See link",
  "https://www.researchgate.net/publication/403377178", "ISAC / AUV relay", "DRL controls AUV that relays data to buoy while sensing intruders", "DRL", UNK,
  NO_DS, "-", NO_CODE, "-", 2, "DRL in underwater acoustic networking", "DOI not shown in results."),
 (2025, "Attack Detection and Optimal Deployment for Underwater Constrained Wireless Sensor Networks via Hybrid Trust Evidence",
  "B. Jiang, R. Zhou, F. Luo, X. Cui, H. H. Wang, H. H. Song", "IEEE Trans. Network Sci. & Eng.", "2025", "See link",
  "https://mdsoar.org/items/a0b7a078-5e43-4a5e-9437-bea694bef3e8", "Security / trust", "Trust evidence + TabTransformer attack detection; deployment optimisation",
  "Deep learning (Transformer)", UNK, UNK, "-", NO_CODE, "-", 2, "Trust-aware forwarding is a possible extension", ""),
 (2025, "High-Speed Bio-Inspired Covert Underwater Acoustic Communication Technology for Underwater Internet of Things",
  "See link", "IEEE Internet of Things Journal", "2025", "10.1109/JIOT.2025.3604025",
  "https://doi.org/10.1109/JIOT.2025.3604025", "PHY / covert comm", "Bio-inspired covert signalling", "None", UNK, UNK, "-", NO_CODE, "-", 1,
  "Physical layer only", "Title/metadata only."),
 (2025, "Joint Optimization of Underwater Acoustic ISUDC Waveform Design and Sparse Channel Estimation Algorithms",
  "See link", "IEEE Internet of Things Journal", "2025 (early access)", "10.1109/JIOT.2025.3598477",
  "https://doi.org/10.1109/JIOT.2025.3598477", "PHY / channel estimation", "Waveform design + sparse channel estimation", "None", UNK, UNK, "-", NO_CODE, "-", 1,
  "Channel modelling background for link-quality term", ""),
 (2025, "Integrated Acoustic Frequency Comb Signal for Underwater Inverted Ultrashort Baseline Autonomous Positioning Systems",
  "See link", "IEEE Internet of Things Journal", "Jul 2025", "10.1109/JIOT.2025.3564346",
  "https://doi.org/10.1109/JIOT.2025.3564346", "Positioning (iUSBL)", "Joint comm + positioning signal design", "None", UNK, UNK, "-", NO_CODE, "-", 1, "Background", ""),
 (2025, "Hybrid Underwater Localization Communication Framework for Blockchain-Enabled IoT Underwater Acoustic Sensor Network",
  "See link", "IEEE Internet of Things Journal", "Jan 2025", "10.1109/JIOT.2025.3535375",
  "https://doi.org/10.1109/JIOT.2025.3535375", "Localization + security", "Blockchain-enabled hybrid localization/communication", "None", UNK, UNK, "-", NO_CODE, "-", 2,
  "Depth/position info that routing relies on", ""),
 (2025, "Autonomous Underwater Vehicle Safety Path Planning Method Based on Constraint Reinforcement Learning",
  "See link", "IEEE Trans. Vehicular Technology", "Sep 2025 (vol. 75(3) pp. 3800-3815 as listed)", "See link",
  "https://www.researchgate.net/publication/395681955", "AUV path planning", "Constrained RL", "Constrained RL", UNK, UNK, "-", NO_CODE, "-", 1,
  "AUV task; safe-RL idea only", "Volume/year listing inconsistent; verify."),
 (2025, "Towards the underwater internet of things for subsea oil and gas monitoring (survey)",
  "C. Stewart, M. Ayaz, N. Fough, R. Prabhu", "Internet of Things (Elsevier)", "vol. 30, Jan 2025", "See link",
  "https://rgu-repository.worktribe.com/output/2662977", "Survey (IoUT)", "Survey: communications, networking, sensing, computing", "-", "-", "-", "-", "-", "-", 2,
  "Application context", ""),
 (2025, "A survey on energy efficient medium access control for acoustic wireless communication networks in underwater environments",
  "See link", "J. Network & Computer Applications", "vol. 235, Mar 2025", "pii S108480452400256X",
  "https://www.sciencedirect.com/science/article/pii/S108480452400256X", "Survey (MAC)", "Survey incl. ML-based MAC", "-", "-", "-", "-", "-", "-", 3,
  "Choice of MAC under our routing protocol", ""),
 (2025, "Survey of AI-driven routing protocols in underwater acoustic networks for enhanced communication efficiency",
  "See link", "Ocean Engineering", "vol. 314 (Part 1)", "pii S0029801824029445",
  "https://www.sciencedirect.com/science/article/abs/pii/S0029801824029445", "Survey (AI routing)", "Survey: RL, ML, fuzzy routing", "-", "-", "-", "-", "-", "-", 4,
  "Directly frames AI-based routing; cite in Related Work", "Listed as 2024 online / 2025 issue."),
 # ---------------- 2024 ----------------
 (2024, "Longevity-Oriented and Reliable Forwarding Percolation Routing in Underwater Acoustic Sensor Networks (LRP)",
  "Y. Liu, H. Wang, L. Cai, J. Hu, X. Shen", "IEEE Internet of Things Journal", "vol. 11, no. 6, pp. 11031-11045", "10.1109/JIOT.2023.3329715",
  "https://ece.uvic.ca/~cai/ioj24-perc.pdf", "Routing (energy + void)", "Multipath percolation routing; power control; residual-energy optimisation; recursive void avoidance",
  "None (optimisation)", "Simulation", NO_DS, "-", NO_CODE, "-", 4, "Same goals (lifetime + reliability + voids) with non-learning approach; good baseline", "Author-hosted PDF."),
 (2024, "Achieving Fair-Effective Communications and Robustness in Underwater Acoustic Sensor Networks: A Semi-Cooperative Approach (SECOPA)",
  "Y. Gou, T. Zhang, J. Liu, T. Yang, S. Song, J.-H. Cui", "IEEE Trans. Mobile Computing", "vol. 23, no. 5, pp. 5722-5739", "10.1109/TMC.2023.3310476",
  "https://doi.org/10.1109/TMC.2023.3310476", "Power allocation", "Semi-cooperative power allocation; training with imperfect channels and node failures",
  "Distributed MARL", "Simulation", NO_DS, "-", NO_CODE, "-", 3, "Robust RL under imperfect acoustic channels (our overestimation motivation)", "arXiv 2508.07578."),
 (2024, "Joint Link Scheduling and Power Allocation in Imperfect and Energy-Constrained Underwater Wireless Sensor Networks (ICRL-JSA)",
  "T. Zhang, Y. Gou, J. Liu, S. Song, T. Yang, J.-H. Cui (per library catalog)", "IEEE Trans. Mobile Computing", "vol. 23, no. 10, pp. 9863-9880", "10.1109/TMC.2024.3368425",
  "https://doi.org/10.1109/TMC.2024.3368425", "Scheduling + power", "DQN-based deep MARL optimiser with advanced training mechanism",
  "Deep MARL (DQN)", "Simulation", NO_DS, "-", NO_CODE, "-", 3, "DQN in energy-constrained UWSNs", "Author list differs between DBLP and catalog; verify. arXiv 2508.07679."),
 (2024, "A Federated Deep Reinforcement Learning-Based Trust Model in Underwater Acoustic Sensor Networks",
  "Y. He, et al.", "IEEE Trans. Mobile Computing", "vol. 23, no. 5", "See link",
  "https://oulurepo.oulu.fi/handle/10024/48404", "Security / trust", "Federated DRL trust model", "Federated DRL", UNK, UNK, "-", NO_CODE, "-", 2, "Trust background", ""),
 (2024, "Environment- and Energy-Aware AUV-Assisted Data Collection for the Internet of Underwater Things",
  "Z. Zhang, J. Xu, G. Xie, J. Wang, Z. Han, Y. Ren", "IEEE Internet of Things Journal", "vol. 11, no. 15, pp. 26406-26418", "See link",
  "https://research.buaa.edu.cn/en/publications/environment-and-energy-aware-auv-assisted-data-collection-for-the/",
  "AUV data collection", "Multi-agent independent soft actor-critic (MAISAC); urgency-based target selection", "MARL (SAC)", "Simulation",
  NO_DS, "-", NO_CODE, "-", 2, "Energy-aware learning in IoUT", "Author PDF: https://360zmem.github.io/files/PDF/iout2024.pdf"),
 (2024, "AUV-Assisted Node Repair for IoUT Relying on Multiagent Reinforcement Learning (RANR)",
  "Z. Wang, Z. Zhang, J. Wang, C. Jiang, W. Wei, Y. Ren", "IEEE Internet of Things Journal", "vol. 11, no. 3, pp. 4139-4151", "See link",
  "https://dblp.uni-trier.de/rec/journals/iotj/WangZWJWR24.html", "AUV / fault repair", "Multi-AUV MARL search-and-repair", "MARL", UNK,
  NO_DS, "-", NO_CODE, "-", 2, "Repairs voids caused by failed nodes (our void problem from another angle)", ""),
 (2024, "Energy-Efficient Data Collection Scheme Based on Value of Information in Underwater Acoustic Sensor Networks",
  "Liu, et al.", "IEEE Internet of Things Journal", "2024", "10.1109/JIOT.2024.3361850",
  "https://doi.org/10.1109/JIOT.2024.3361850", "AUV data collection", "VoI model based on data rarity", "None", UNK, NO_DS, "-", NO_CODE, "-", 2, "Energy-efficient collection context", ""),
 (2024, "Efficient AUV-Aided Localization for Large-Scale Underwater Acoustic Sensor Networks",
  "See link", "IEEE Internet of Things Journal", "vol. 11, no. 19", "See link",
  "https://research.buaa.edu.cn/en/publications/efficient-auv-aided-localization-for-large-scale-underwater-acous/", "Localization",
  "AUV-aided localization handling unsynchronised clocks and stratification", "None", "Simulation", NO_DS, "-", NO_CODE, "-", 1, "Background", ""),
 (2024, "Design Guidelines on Trust Management for Underwater Wireless Sensor Networks",
  "R. Zhu, A. Boukerche, L. Long, Q. Yang", "IEEE Commun. Surveys & Tutorials", "online 16 Apr 2024", "10.1109/COMST.2024.3389728",
  "https://doi.org/10.1109/COMST.2024.3389728", "Survey (security/trust)", "Survey", "-", "-", "-", "-", "-", "-", 2, "Security background", ""),
 (2024, "Security and Reliability of Internet of Underwater Things: Architecture, Challenges, and Opportunities",
  "See link", "ACM Computing Surveys", "2024", "10.1145/3700640",
  "https://dl.acm.org/doi/10.1145/3700640", "Survey (IoUT security)", "Survey", "-", "-", "-", "-", "-", "-", 2, "Reliability background", ""),
 (2024, "AUV-aided computing offloading for multi-tier underwater computing: A Stackelberg game learning approach",
  "See link", "Ocean Engineering", "2024", "pii S0029801824004463",
  "https://www.sciencedirect.com/science/article/abs/pii/S0029801824004463", "Edge computing", "Stackelberg game learning (buoys, AUVs, LEO)", "Game-theoretic learning", UNK,
  NO_DS, "-", NO_CODE, "-", 1, "Background", ""),
]

FOUND = [
 (2022, "A Trust Update Mechanism Based on Reinforcement Learning in Underwater Acoustic Sensor Networks (TUMRL)", "Y. He, G. Han, et al.",
  "IEEE Trans. Mobile Computing", "vol. 21, no. 3, pp. 811-821", "10.1109/TMC.2020.3020313", "https://doi.org/10.1109/TMC.2020.3020313", "RL-based trust update", 2),
 (2023, "An SDN-Enabled Framework for a Load-Balanced and QoS-Aware Internet of Underwater Things (CASM + SQAR)", "Y. Shi, Q. Yang, X. Huang, D. Li, X. Huang",
  "IEEE Internet of Things Journal", "vol. 10, no. 9", "10.1109/JIOT.2022.3231329", "https://doi.org/10.1109/JIOT.2022.3231329", "RL-based QoS-aware adaptive routing (SQAR)", 4),
 (2022, "AUV-Aided Hybrid Data Collection Scheme Based on Value of Information for Internet of Underwater Things", "Z. Liu, et al.",
  "IEEE Internet of Things Journal", "2022", "10.1109/JIOT.2021.3115800", "https://doi.org/10.1109/JIOT.2021.3115800", "VoI attenuation + hybrid clustering", 2),
 (2021, "Reinforcement Learning-Based Opportunistic Routing Protocol for Underwater Acoustic Sensor Networks (RLOR)", "Zhang, et al.",
  "IEEE Trans. Vehicular Technology", "vol. 70, no. 3, pp. 2756-2770", "See link",
  "https://scholar.xjtlu.edu.cn/en/publications/reinforcement-learning-based-opportunistic-routing-protocol-for-u/", "RL opportunistic routing", 5),
 (2020, "Routing Protocol Design for Underwater Optical Wireless Sensor Networks: A Multiagent Reinforcement Learning Approach (DMARL)", "X. Li, X. Hu, R. Zhang, L. Yang",
  "IEEE Internet of Things Journal", "vol. 7, no. 10, pp. 9805-9818", "10.1109/JIOT.2020.2989924", "https://doi.org/10.1109/JIOT.2020.2989924", "Distributed MARL routing", 4),
 (2019, "CARMA: Channel-Aware Reinforcement Learning-Based Multi-Path Adaptive Routing for Underwater Wireless Sensor Networks",
  "V. Di Valerio, F. Lo Presti, C. Petrioli, L. Picari, D. Spaccini, S. Basagni", "IEEE J. Sel. Areas Commun.", "vol. 37, no. 11, pp. 2634-2647",
  "10.1109/JSAC.2019.2933968", "https://doi.org/10.1109/JSAC.2019.2933968", "Distributed RL, single/multi-path switching (SUNSET + sea trial)", 5),
 (2010, "QELAR: A Machine-Learning-Based Adaptive Routing Protocol for Energy-Efficient and Lifetime-Extended Underwater Sensor Networks",
  "T. Hu, Y. Fei", "IEEE Trans. Mobile Computing", "vol. 9, no. 6, pp. 796-809", "See link", "https://dblp.org/rec/journals/tmc/HuF10",
  "Q-learning routing (Aqua-Sim); ~20% longer lifetime than VBF", 5),
]

RES = [
 ("Simulator", "Aqua-Sim FG (ns-3 based, AI-ready)", "https://github.com/JLU-smartocean/aqua-sim-fg", "From Aqua-Sim FG paper (IEEE IoTJ 2025)", "Main candidate platform"),
 ("Simulator", "Aqua-Sim NG (ns-3 module; recommends ns-3.40; includes VBF, HH-VBF, VBVA)", "https://github.com/rmartin5/aqua-sim-ng", "GitHub + ns-3-users threads", "DBR not confirmed in repo; may need to implement"),
 ("Simulator", "ns-3 UAN module (built-in acoustic channel, MAC, energy model)", "https://www.nsnam.org/docs/models/html/uan.html", "Official ns-3 docs", "Built into ns-3"),
 ("ML bridge", "ns3-ai (ns-3 <-> Python RL, Gym interface)", "https://github.com/hust-diangroup/ns3-ai", "GitHub / apps.nsnam.org", "Only needed for DQN-style extensions"),
 ("Simulator", "DESERT Underwater (NS-Miracle based)", "https://github.com/signetlabdei/DESERT_Underwater", "Project site", "Alternative (ns-2 lineage)"),
 ("Dataset", "Watermark: measured underwater acoustic channel benchmark (Norway, France, Hawaii; MATLAB)", "https://ffi.no/en/research/watermark", "FFI; IEEE JOE 2017 paper", "Real channel data; could drive link-quality realism"),
 ("Code (related)", "SA-MARL multi-AUV tracking code", "https://github.com/PingshengRen0901/SA-MARL", "arXiv 2603.27194", "Not routing; MARL reference code"),
 ("Code (related)", "MARL-AUV open platform (DI-engine + 6-DoF AUV sim)", "https://github.com/dasjsaj/MARL-AUV", "arXiv 2605.15528", "Not routing"),
]

EXCL = [
 (2025, "Service-aware Q-learning-based routing protocol in the underwater acoustic sensor network (SAQR)", "Computer Networks", "4.6", "https://dl.acm.org/doi/10.1016/j.comnet.2024.110986", 5),
 (2025, "A Q-Learning-Based Link-Aware Routing Protocol for Underwater Wireless Sensor Networks", "J. Mar. Sci. Eng.", "2.8", "https://www.mdpi.com/2077-1312/13/12/2374", 5),
 (2023, "Deep Q-Network-Based Intelligent Routing Protocol for Underwater Acoustic Sensor Network (DQIR)", "IEEE Sensors Journal", "4.5", "https://www.bohrium.com/paper-details/deep-q-network-based-intelligent-routing-protocol-for-underwater-acoustic-sensor-network/832929645174194180-4018", 5),
 (2025, "Adaptive Power-Controlled Energy-Efficient Depth-Based Routing (APC-EEDBR)", "J. Mar. Sci. Eng.", "2.8", "https://mdpi.com/2077-1312/13/8/1418", 4),
 (2025, "A Three-Dimensional Routing Protocol for UASNs Based on Fuzzy Logic Reasoning", "J. Mar. Sci. Eng.", "2.8", "https://mdpi-res.com/d_attachment/jmse/jmse-13-00692/article_deploy/jmse-13-00692.pdf", 4),
 (2025, "Deep Q-Learning Based Adaptive MAC Protocol with Collision Avoidance and Efficient Power Control for UWSNs", "J. Mar. Sci. Eng.", "2.8", "https://doi.org/10.3390/jmse13030616", 3),
]

thin = Side(style="thin", color="BBBBBB")
B = Border(left=thin, right=thin, top=thin, bottom=thin)
HFILL = PatternFill("solid", fgColor="1F3864")
HFONT = Font(bold=True, color="FFFFFF")
SCORE_FILL = {5: "C6EFCE", 4: "E2EFDA", 3: "FFF2CC", 2: "FCE4D6", 1: "F2F2F2"}

def sheet(ws, headers, rows, widths, link_cols=(), score_col=None, table_name=None):
    ws.append(headers)
    for r in rows:
        ws.append(list(r))
    for c in range(1, len(headers) + 1):
        h = ws.cell(row=1, column=c); h.fill = HFILL; h.font = HFONT
        h.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(c)].width = widths[c - 1]
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top"); cell.border = B
            if cell.column in link_cols and isinstance(cell.value, str) and cell.value.startswith("http"):
                cell.hyperlink = cell.value; cell.font = Font(color="0563C1", underline="single")
        if score_col:
            s = row[score_col - 1]
            if s.value in SCORE_FILL:
                s.fill = PatternFill("solid", fgColor=SCORE_FILL[s.value]); s.alignment = Alignment(horizontal="center", vertical="top")
    ws.freeze_panes = "C2"
    if table_name:
        ref = f"A1:{get_column_letter(len(headers))}{len(rows) + 1}"
        t = Table(displayName=table_name, ref=ref)
        t.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=False)
        ws.add_table(t)

wb = Workbook()
ws = wb.active; ws.title = "Papers IF>=5 (2024-26)"
P.sort(key=lambda r: (-r[0], -r[15]))
rows = []
for i, r in enumerate(P, 1):
    (y, t, a, j, v, doi, link, area, model, lt, sim, ds, dsl, code, codel, sc, why, note) = r
    rows.append((i, y, t, a, j, IF[j][0], v, doi, link, area, model, lt, sim, ds, dsl, code, codel, sc, why, note))
H = ["#", "Year", "Title", "Authors", "Journal", "Impact factor", "Vol / issue / pages", "DOI / ID", "Direct link",
     "Topic area", "Model / method", "Learning type", "Simulator / evaluation", "Dataset used", "Dataset link",
     "Code available?", "Code link", "Similarity (1-5)", "Similarity to our topic (why)", "Verification notes"]
sheet(ws, H, rows, [4, 6, 48, 30, 26, 14, 24, 26, 40, 20, 44, 18, 22, 30, 14, 18, 34, 10, 44, 34],
      link_cols=(9, 15, 17), score_col=18, table_name="Papers")

ws2 = wb.create_sheet("Foundational (pre-2024)")
FOUND.sort(key=lambda r: (-r[0]))
rows = [(i, y, t, a, j, IF[j][0], v, d, l, m, s) for i, (y, t, a, j, v, d, l, m, s) in enumerate(FOUND, 1)]
sheet(ws2, ["#", "Year", "Title", "Authors", "Journal", "Impact factor", "Vol / pages", "DOI", "Direct link", "Model / method", "Similarity (1-5)"],
      rows, [4, 6, 52, 34, 26, 14, 26, 26, 42, 40, 10], link_cols=(9,), score_col=11, table_name="Foundational")

ws3 = wb.create_sheet("Code & Datasets")
sheet(ws3, ["Type", "Resource", "Link", "Where found", "Use for our project"], RES, [14, 56, 50, 30, 40], link_cols=(3,), table_name="Resources")

ws4 = wb.create_sheet("Journal IF")
rows = sorted([(j, v[0], v[1]) for j, v in IF.items()], key=lambda r: -float(r[1].split()[0]))
sheet(ws4, ["Journal", "Impact factor used", "Source"], rows, [36, 40, 70], link_cols=(3,), table_name="JournalIF")

ws5 = wb.create_sheet("Excluded IF<5 (relevant)")
EXCL.sort(key=lambda r: (-r[0], -r[5]))
sheet(ws5, ["Year", "Title", "Journal", "IF", "Link", "Similarity (1-5)"], EXCL, [6, 60, 22, 8, 50, 10], link_cols=(5,), score_col=6, table_name="Excluded")

ws6 = wb.create_sheet("Read me")
notes = [
 ["Our topic", TOPIC],
 ["Selection rule", "Journal impact factor >= 5 (journalmetrics.org JCR-based values, checked 31-Oct-2026). Main sheet = 2024-2026; older landmark papers on 'Foundational'."],
 ["Sorting", "Year (latest first), then similarity score (highest first)."],
 ["Similarity score", "5 = RL/Q-learning routing for UASNs with energy/depth/void terms; 4 = UASN routing (non-RL) or ns-3 simulator platform; 3 = RL at MAC / resource-allocation layer; 2 = AUV, security, survey context; 1 = PHY / localization / tracking background."],
 ["Dataset column", "Routing/MAC papers almost never use external datasets; they generate synthetic topologies in a simulator. Where a paper used real data that is not released, this is stated."],
 ["Code column", "'YES' only when a public repository link was found. 'No' means searches found no public code; it does not prove none exists - check the paper's full text."],
 ["How verified", "Every paper, DOI and link came from live web-search results. Publisher pages could not be opened from this environment, so authors/pages marked 'See link' or with notes should be confirmed on the page before citing."],
 ["Count", f"{len(P)} papers (2024-2026, IF>=5) + {len(FOUND)} foundational + {len(EXCL)} relevant-but-excluded."],
]
for r in notes: ws6.append(r)
ws6.column_dimensions["A"].width = 18; ws6.column_dimensions["B"].width = 120
for row in ws6.iter_rows():
    row[0].font = Font(bold=True)
    for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
wb.move_sheet("Read me", offset=-5)
wb.active = 1
wb.save(OUT)
print("saved", OUT, len(P), len(FOUND), len(EXCL))
