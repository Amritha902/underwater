"""Build literature_survey_IF5plus.xlsx: one clean, sortable, colour-graded sheet."""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

OUT = "literature_survey_IF5plus.xlsx"
OUR_WORK = ("Our Work: DQ-EVDR - Double Q-Learning based Energy- and Void-Aware Depth Routing "
            "for Underwater Acoustic Sensor Networks, implemented and evaluated in ns-3")

IF = {
    "IEEE Communications Surveys & Tutorials": 46.7,
    "ACM Computing Surveys": 28.0,
    "Information Fusion": 15.5,
    "IEEE Journal of Selected Topics in Signal Processing": 13.7,
    "IEEE Journal on Selected Areas in Communications": 13.1,
    "IEEE Transactions on Wireless Communications": 10.7,
    "IEEE Communications Magazine": 8.2,
    "IEEE Transactions on Mobile Computing": 9.2,
    "IEEE Internet of Things Journal": 8.9,
    "Engineering Applications of Artificial Intelligence": 8.0,
    "Journal of Network and Computer Applications": 8.0,
    "IEEE Transactions on Network Science and Engineering": 7.9,
    "IEEE Transactions on Vehicular Technology": 7.5,
    "Internet of Things (Elsevier)": 7.1,
    "Ocean Engineering": 5.5,
}

# (year, title, authors, journal, relevance %, research gap, how our work addresses it, link)
ROWS = [
    (2026, "A Novel Underwater Target Tracking Method in UASNs via Collaborative Deep Reinforcement Learning",
     "Zheng, Liu, Zhang, Dong", "Information Fusion", 15,
     "Applies multi-agent PPO to sensor scheduling and data fusion for target tracking; does not address multi-hop packet routing or routing voids.",
     "We apply reinforcement learning to the routing layer, where each node learns its next hop from depth, energy and link quality.",
     "https://doi.org/10.1016/j.inffus.2025.103797"),
    (2026, "Propagation-Aware Scheduling MAC Protocol for Reliable Underwater Swarmed AUV Communications Networks",
     "Yun, Oh, Lim", "IEEE Internet of Things Journal", 35,
     "Handles long propagation delay at the MAC layer for AUV swarms; routing decisions above the MAC are outside its scope.",
     "We work at the network layer on top of a standard ns-3 UAN MAC, using delay-aware holding times to suppress duplicate forwarding.",
     "https://doi.org/10.1109/JIOT.2025.3642314"),
    (2025, "An Intelligent Q-Learning-Based Tree Routing Method in Underwater Acoustic Sensor Networks (QTRU)",
     "Khoshvaght, Haider, Rahmani, Altulyan, et al.", "Engineering Applications of Artificial Intelligence", 95,
     "Uses standard single-estimator Q-learning, which is known to overestimate values under noisy rewards; tree topology; evaluated in NS-2.",
     "We replace Q-learning with Double Q-learning to remove overestimation bias, add a learned void penalty, and evaluate in ns-3.",
     "https://www.sciencedirect.com/science/article/abs/pii/S0952197625007535"),
    (2025, "Joint Power Control and Multi-Path Routing for Internet of Underwater Things in Varying Environments (CAMP)",
     "Xu, Song, Liu, Pan, Xu, Cui", "IEEE Internet of Things Journal", 80,
     "Uses analytical reliability models with multipath at the source and power control; no learning component is described.",
     "Our nodes learn link quality online through Double Q-learning, adapting next-hop choice without an explicit channel model.",
     "https://doi.org/10.1109/JIOT.2025.3527692"),
    (2025, "Aqua-Sim Fourth Generation: Towards General and Intelligent Simulation for Underwater Acoustic Networks",
     "Guo, Song, Chen, Huangfu, Liu, Cui", "IEEE Internet of Things Journal", 70,
     "Provides an ns-3 based simulation platform; does not propose or benchmark a learning-based routing protocol.",
     "We use ns-3 underwater modules to implement DQ-EVDR and benchmark it against DBR, VBF and Q-learning baselines.",
     "https://doi.org/10.1109/JIOT.2025.3571022"),
    (2025, "A Digital Twin-Based Intelligent Network Architecture for Underwater Acoustic Sensor Networks (DTNA)",
     "Song, Huangfu, Guo, Liu, Cui, Shen", "IEEE Transactions on Mobile Computing", 50,
     "Architecture-level framework relying on digital twins and MARL to compensate for scarce training data; not a per-node routing protocol.",
     "We use lightweight tabular Double Q-learning that runs on each node with only local information.",
     "https://doi.org/10.1109/TMC.2025.3555640"),
    (2025, "Multi-AUV Cooperative Underwater Multi-Target Tracking Based on Dynamic-Switching-Enabled Multi-Agent Reinforcement Learning",
     "Wang, Lin, Han, Zhu, Li, Wang, Ma", "IEEE Transactions on Mobile Computing", 10,
     "Targets AUV swarm tracking; not concerned with energy-constrained static sensor routing.",
     "We focus on multi-hop data delivery from battery-powered sensor nodes to surface sinks.",
     "https://doi.org/10.1109/TMC.2024.3521889"),
    (2025, "Underwater Target Tracking Based on Interrupted Software-Defined Multi-AUV Reinforcement Learning: A Multi-AUV Time-Saving MARL Approach",
     "Zhu, Han, Lin, Zhang", "IEEE Transactions on Mobile Computing", 10,
     "Handles interrupted links for AUV tracking; routing in sensor networks is not addressed.",
     "We address link disruption in routing through learned void and link-quality penalties.",
     "https://doi.org/10.1109/TMC.2024.3490545"),
    (2025, "Security and Reliability of Internet of Underwater Things: Architecture, Challenges, and Opportunities",
     "Jiang, Feng, Cui, Wang, Liu, Song", "ACM Computing Surveys", 25,
     "Survey; identifies reliability challenges but proposes no routing protocol.",
     "We contribute a concrete reliable routing protocol with reproducible ns-3 evaluation.",
     "https://doi.org/10.1145/3700640"),
    (2025, "A Survey on Energy Efficient Medium Access Control for Acoustic Wireless Communication Networks in Underwater Environments",
     "Hasan, Ahmad, Habibi, Phung, Al-Fawa'reh, Islam, Zaheer, Khaled", "Journal of Network and Computer Applications", 45,
     "Survey of energy-efficient MAC including ML-based MAC; network-layer learning is outside its scope.",
     "We bring learning-based energy efficiency to the routing layer, complementing the MAC techniques it reviews.",
     "https://doi.org/10.1016/j.jnca.2024.104079"),
    (2025, "Towards the Underwater Internet of Things for Subsea Oil and Gas Monitoring",
     "Stewart, Ayaz, Fough, Prabhu", "Internet of Things (Elsevier)", 20,
     "Application-level survey of communication technologies; no routing protocol design.",
     "We provide an energy-aware routing protocol suitable for long-lived subsea monitoring deployments.",
     "https://doi.org/10.1016/j.iot.2025.101510"),
    (2024, "Design Guidelines on Trust Management for Underwater Wireless Sensor Networks",
     "Zhu, Boukerche, Long, Yang", "IEEE Communications Surveys & Tutorials", 25,
     "Survey of trust management; does not address energy or void-aware routing.",
     "Our protocol's modular reward allows trust to be added as future work.",
     "https://doi.org/10.1109/COMST.2024.3389728"),
    (2024, "Longevity-Oriented and Reliable Forwarding Percolation Routing in Underwater Acoustic Sensor Networks (LRP)",
     "Liu, Wang, Cai, Hu, Shen", "IEEE Internet of Things Journal", 80,
     "Non-learning percolation routing; voids avoided by a fixed recursive rule rather than learned from experience.",
     "We learn which neighbours lead to voids through a void penalty in the Double Q-learning reward.",
     "https://doi.org/10.1109/JIOT.2023.3329715"),
    (2024, "Achieving Fair-Effective Communications and Robustness in Underwater Acoustic Sensor Networks: A Semi-Cooperative Approach (SECOPA)",
     "Gou, Zhang, Liu, Yang, Song, Cui", "IEEE Transactions on Mobile Computing", 55,
     "Learns transmit power allocation with MARL; next-hop routing is not learned.",
     "We apply robust learning to next-hop selection, using Double Q-learning to cope with imperfect channels.",
     "https://doi.org/10.1109/TMC.2023.3310476"),
    (2024, "Joint Link Scheduling and Power Allocation in Imperfect and Energy-Constrained Underwater Wireless Sensor Networks (ICRL-JSA)",
     "Zhang, Gou, Liu, Song, Yang, Cui", "IEEE Transactions on Mobile Computing", 55,
     "DQN-based deep MARL for scheduling and power; computationally heavier than tabular learning and does not perform routing.",
     "We keep learning lightweight (tabular Double Q) so it can run on sensor nodes, and apply it to routing.",
     "https://doi.org/10.1109/TMC.2024.3368425"),
    (2024, "A Federated Deep Reinforcement Learning-Based Trust Model in Underwater Acoustic Sensor Networks",
     "He, Han, Li, Taleb, Wang, Yu", "IEEE Transactions on Mobile Computing", 30,
     "Learning applied to trust prediction rather than packet forwarding.",
     "We apply learning directly to forwarding decisions.",
     "https://doi.org/10.1109/TMC.2023.3301825"),
    (2024, "Environment- and Energy-Aware AUV-Assisted Data Collection for the Internet of Underwater Things",
     "Zhang, Xu, Xie, Wang, Han, Ren", "IEEE Internet of Things Journal", 35,
     "Relies on AUVs (multi-agent SAC) to collect data; multi-hop routing among sensor nodes is not addressed.",
     "We deliver data through multi-hop routing among static nodes, without requiring AUVs.",
     "https://doi.org/10.1109/JIOT.2024.3395568"),
    (2024, "AUV-Assisted Node Repair for IoUT Relying on Multiagent Reinforcement Learning (RANR)",
     "Wang, Zhang, Wang, Jiang, Wei, Ren", "IEEE Internet of Things Journal", 40,
     "Addresses voids caused by failed nodes by physically repairing them with AUVs, rather than by adapting the routing.",
     "We let routing adapt around voids immediately through a learned void penalty, without waiting for repair.",
     "https://doi.org/10.1109/JIOT.2023.3298522"),
    (2024, "Energy-Efficient Data Collection Scheme Based on Value of Information in Underwater Acoustic Sensor Networks",
     "Liu, Liang, Yuan, Chan, Guan", "IEEE Internet of Things Journal", 30,
     "Energy efficiency through value-of-information based collection; no learning-based multi-hop routing.",
     "We reduce energy per delivered packet through learned forwarding and duplicate suppression.",
     "https://doi.org/10.1109/JIOT.2024.3361850"),
    (2024, "Efficient AUV-Aided Localization for Large-Scale Underwater Acoustic Sensor Networks",
     "Wang, Song, Liu, Guo, Cui", "IEEE Internet of Things Journal", 15,
     "Localization requires AUVs and handles clock and stratification issues; no routing.",
     "We need only depth information, so no localization infrastructure is required.",
     "https://doi.org/10.1109/JIOT.2024.3420448"),
    (2023, "An SDN-Enabled Framework for a Load-Balanced and QoS-Aware Internet of Underwater Things (SQAR)",
     "Shi, Yang, Huang, Li, Huang", "IEEE Internet of Things Journal", 75,
     "RL-based QoS routing relies on SDN controllers (a centralised control plane).",
     "Our routing is fully distributed; each node learns locally without a controller.",
     "https://doi.org/10.1109/JIOT.2022.3231329"),
    (2022, "A Trust Update Mechanism Based on Reinforcement Learning in Underwater Acoustic Sensor Networks",
     "He, Han, Jiang, Wang, Martinez-Garcia", "IEEE Transactions on Mobile Computing", 30,
     "Uses RL to update trust values, not routes.",
     "We use RL for forwarding decisions.",
     "https://doi.org/10.1109/TMC.2020.3020313"),
    (2022, "AUV-Aided Hybrid Data Collection Scheme Based on Value of Information for Internet of Underwater Things",
     "Liu, Meng, Liu, Yang, Wang", "IEEE Internet of Things Journal", 30,
     "Depends on AUV mobility and clustering for collection.",
     "We provide AUV-free multi-hop delivery.",
     "https://doi.org/10.1109/JIOT.2021.3115800"),
    (2021, "Reinforcement Learning-Based Opportunistic Routing Protocol for Underwater Acoustic Sensor Networks (RLOR)",
     "Zhang, Zhang, Chen, Wang", "IEEE Transactions on Vehicular Technology", 90,
     "RL-based opportunistic routing with standard value estimates; estimation bias under noisy links is not discussed in the abstract.",
     "We extend the RL opportunistic routing idea with Double Q-learning and an explicit void penalty, evaluated in ns-3.",
     "https://doi.org/10.1109/TVT.2021.3058282"),
    (2020, "Routing Protocol Design for Underwater Optical Wireless Sensor Networks: A Multiagent Reinforcement Learning Approach",
     "Li, Hu, Zhang, Yang", "IEEE Internet of Things Journal", 70,
     "Designed for optical links, which are short-range; acoustic delay and energy constraints differ.",
     "We target acoustic sensor networks, the dominant long-range underwater technology.",
     "https://doi.org/10.1109/JIOT.2020.2989924"),
    (2019, "CARMA: Channel-Aware Reinforcement Learning-Based Multi-Path Adaptive Routing for Underwater Wireless Sensor Networks",
     "Di Valerio, Lo Presti, Petrioli, Picari, Spaccini, Basagni", "IEEE Journal on Selected Areas in Communications", 85,
     "Distributed RL routing with standard value estimates; evaluated with SUNSET and sea trials rather than ns-3.",
     "We add Double Q-learning to reduce estimation bias and provide an open ns-3 evaluation.",
     "https://doi.org/10.1109/JSAC.2019.2933968"),
    (2010, "QELAR: A Machine-Learning-Based Adaptive Routing Protocol for Energy-Efficient and Lifetime-Extended Underwater Sensor Networks",
     "Hu, Fei", "IEEE Transactions on Mobile Computing", 90,
     "Early Q-learning UASN routing protocol; later work reports slow convergence with many nodes or high node mobility.",
     "We build on QELAR's energy-aware Q-learning, adding Double Q-learning, depth progress and a learned void penalty.",
     "https://doi.org/10.1109/TMC.2010.28"),
    (2023, "Environment-Aware AUV Trajectory Design and Resource Management for Multi-Tier Underwater Computing",
     "Hou, Wang, Bai, Deng, Ren, Hanzo", "IEEE Journal on Selected Areas in Communications", 20,
     "Optimises AUV trajectories and computing resources with RL; static sensor multi-hop routing is not addressed.",
     "We address energy-aware multi-hop routing among sensor nodes, which feeds data to such computing tiers.",
     "https://doi.org/10.1109/JSAC.2022.3227103"),
    (2021, "Anypath Routing Protocol Design via Q-Learning for Underwater Sensor Networks (QLFR)",
     "Zhou, Cao, Xiang", "IEEE Internet of Things Journal", 95,
     "Q-learning anypath routing with depth and energy rewards and holding times; uses standard single-estimator Q-learning.",
     "We keep the depth/energy rewards and holding-time idea, and replace Q-learning with Double Q-learning plus a learned void penalty, evaluated in ns-3.",
     "https://doi.org/10.1109/JIOT.2020.3042901"),
    (2022, "Deep Reinforcement Learning Based MAC Protocol for Underwater Acoustic Networks (DR-DLMA)",
     "Ye, Yu, Fu", "IEEE Transactions on Mobile Computing", 35,
     "Deep Q-network adapted to propagation delay at the MAC layer; needs neural-network training on each node.",
     "We bring delay-aware learning to the routing layer with lightweight tabular Double Q-learning.",
     "https://doi.org/10.1109/TMC.2020.3029844"),
    (2021, "Internet of Underwater Things and Big Marine Data Analytics - A Comprehensive Survey",
     "Jahanbakht, Xiang, Hanzo, Azghadi", "IEEE Communications Surveys & Tutorials", 25,
     "Broad survey of IoUT communication and machine learning; no specific routing protocol proposed.",
     "We contribute a concrete learning-based routing protocol for the IoUT data-delivery layer.",
     "https://doi.org/10.1109/COMST.2021.3053118"),
    (2020, "A Software-Defined Opto-Acoustic Network Architecture for Internet of Underwater Things",
     "Celik, Saeed, Shihada, Al-Naffouri, Alouini", "IEEE Communications Magazine", 20,
     "Architecture-level vision for hybrid optical-acoustic SDN; no distributed routing algorithm evaluated.",
     "We provide a distributed acoustic routing protocol that needs no central controller.",
     "https://doi.org/10.1109/MCOM.001.1900593"),
    (2020, "AUV-Aided Energy-Efficient Data Collection in Underwater Acoustic Sensor Networks (AEEDCO)",
     "Zhuo, Liu, Wei, Yu, Qu, Sun", "IEEE Internet of Things Journal", 35,
     "Energy efficiency achieved through clustering and AUV path planning (TSP); depends on AUV availability.",
     "We achieve energy efficiency through learned multi-hop forwarding without AUVs.",
     "https://doi.org/10.1109/JIOT.2020.2988697"),
    (2022, "Stochastic Optimization-Aided Energy-Efficient Information Collection in Internet of Underwater Things Networks",
     "Fang, Wang, Du, Hou, Ren, Han", "IEEE Internet of Things Journal", 30,
     "Optimisation-based energy-efficient collection; does not learn forwarding decisions from experience.",
     "Our nodes learn forwarding online, adapting to energy and channel changes.",
     "https://doi.org/10.1109/JIOT.2021.3088279"),
    (2013, "VAPR: Void-Aware Pressure Routing for Underwater Sensor Networks",
     "Noh, Lee, Wang, Choi, Gerla", "IEEE Transactions on Mobile Computing", 85,
     "Handles voids with beacon-based directional trails using depth (pressure) information; rule-based rather than learning-based.",
     "We also use only depth, but learn void avoidance and add residual-energy balancing through Double Q-learning.",
     "https://doi.org/10.1109/TMC.2012.53"),
    (2024, "End-to-End Multi-Sensor Fusion Method Based on Deep Reinforcement Learning in UASNs",
     "Zheng, Liu, Zhang, Liu, Dong", "Ocean Engineering", 15,
     "Uses DRL for sensor data fusion; packet routing is not addressed.",
     "We apply RL to routing decisions.",
     "https://doi.org/10.1016/j.oceaneng.2024.117904"),
    (2022, "Opportunistic Routing for Opto-Acoustic Internet of Underwater Things (SectOR)",
     "Celik, Saeed, Shihada, Al-Naffouri, Alouini", "IEEE Internet of Things Journal", 65,
     "Sector-based opportunistic routing designed for short-range optical links; no learning component is described.",
     "We target acoustic links and learn forwarder priority with Double Q-learning.",
     "https://doi.org/10.1109/JIOT.2021.3090301"),
    (2024, "Toward a Sustainable Internet of Underwater Things Based on AUVs, SWIPT, and Reinforcement Learning",
     "Omeke, Mollel, Shah, Zhang, Abbasi, Imran", "IEEE Internet of Things Journal", 35,
     "Extends lifetime through AUV-based wireless power transfer and RL; requires energy-delivering AUVs.",
     "We extend lifetime through energy-balanced routing alone, which can complement energy transfer.",
     "https://doi.org/10.1109/JIOT.2023.3319250"),
    (2026, "Is FISHER All You Need in the Multi-AUV Underwater Target Tracking Task?",
     "Xie, Xu, Zhang, Hou, Ma, Zhang, Ren, Niyato", "IEEE Transactions on Mobile Computing", 10,
     "Imitation learning and decision transformer for AUV tracking; not about sensor routing.",
     "We focus on multi-hop data delivery among static sensor nodes.",
     "https://doi.org/10.1109/TMC.2025.3607882"),
    (2021, "AoI-Inspired Collaborative Information Collection for AUV-Assisted Internet of Underwater Things",
     "Fang, Wang, Jiang, Zhang, Ren", "IEEE Internet of Things Journal", 30,
     "Optimises information freshness through AUV collection; multi-hop routing among sensors is not learned.",
     "Delay-aware holding times in our routing also reduce delivery latency without AUVs.",
     "https://doi.org/10.1109/JIOT.2021.3049239"),
    (2024, "Survey of AI-Driven Routing Protocols in Underwater Acoustic Networks for Enhanced Communication Efficiency",
     "Saleem, Wang, Bharany", "Ocean Engineering", 85,
     "Survey of AI-based routing; notes inconsistent delay in some learning methods; proposes no protocol.",
     "We propose and evaluate a concrete learning-based protocol that targets estimation bias and voids.",
     "https://doi.org/10.1016/j.oceaneng.2024.119606"),
    (2024, "Dynamic Packet Routing Based on Acoustic Signal Curve Propagation in the AUV-Assisted IoUT",
     "Wang, Du, Jiang, Zhang, Ren, Han", "IEEE Internet of Things Journal", 65,
     "Routing model built around AUV mobility and acoustic curve propagation; static sensor energy and void learning not the focus.",
     "We target static energy-constrained sensor networks with learned void and energy awareness.",
     "https://doi.org/10.1109/JIOT.2023.3324311"),
    (2022, "Coverage Enhancement of Underwater Internet of Things Using Multilevel Acoustic Communication Networks",
     "Xu, Kishk, Alouini", "IEEE Internet of Things Journal", 20,
     "Stochastic-geometry coverage optimisation; does not address packet routing.",
     "We address how packets travel once coverage exists.",
     "https://doi.org/10.1109/JIOT.2022.3196180"),
    (2023, "Underwater Pollution Tracking Based on Software-Defined Multi-Tier Edge Computing in 6G-Based Underwater Wireless Networks",
     "Lin, Han, Jiang, Li, Shah, Liu", "IEEE Journal on Selected Areas in Communications", 15,
     "Application-level AUV pollution tracking with SDN and edge computing; no routing protocol.",
     "Our routing protocol can serve as the data-delivery layer for such monitoring applications.",
     "https://doi.org/10.1109/JSAC.2022.3233625"),
    (2024, "A Medium Access Control Protocol Based on Parity Group-Graph Coloring for Underwater AUV-Aided Data Collection",
     "Jiang, Tian, Han, Zhang", "IEEE Internet of Things Journal", 25,
     "MAC-layer slot assignment for AUV-aided collection; network-layer routing not addressed.",
     "We work at the network layer above the MAC.",
     "https://doi.org/10.1109/JIOT.2023.3309251"),
    (2022, "Modulation Recognition of Underwater Acoustic Signals Using Deep Hybrid Neural Networks",
     "Zhang, Yang, Leng, Wang, Mao", "IEEE Transactions on Wireless Communications", 10,
     "Physical-layer signal recognition; no networking component.",
     "We operate at the network layer, using link quality as one input to routing.",
     "https://doi.org/10.1109/TWC.2022.3144608"),
    (2023, "An Opportunistic Routing Based on Directional Transmission in the Internet of Underwater Things",
     "Jiang, Yan, Han, Wang", "IEEE Internet of Things Journal", 75,
     "Rule-based forwarding-area division and candidate coordination; no learning component is described.",
     "We learn forwarder priority, void avoidance and energy balance with Double Q-learning.",
     "https://doi.org/10.1109/JIOT.2023.3267880"),
    (2022, "Energy-Efficient Guiding-Network-Based Routing for Underwater Wireless Sensor Networks (EEGNBR)",
     "Liu, Jin, Yang, Ma, Guan", "IEEE Internet of Things Journal", 70,
     "Localization-free routing along minimum-hop paths of a guiding network; no learning component is described.",
     "We replace fixed hop-count guidance with learned Q-values combining depth, energy, link quality and void penalty.",
     "https://doi.org/10.1109/JIOT.2022.3183128"),
    (2022, "Federated Meta-Learning Enhanced Acoustic Radio Cooperative Framework for Ocean of Things",
     "Zhao, Ji, Li, Guan, Wang, Wen", "IEEE Journal of Selected Topics in Signal Processing", 10,
     "Learning-based receiver design at the physical layer; no routing.",
     "We apply learning at the routing layer.",
     "https://doi.org/10.1109/JSTSP.2022.3144020"),
    (2019, "Distance-Vector-Based Opportunistic Routing for Underwater Acoustic Sensor Networks",
     "Guan, Ji, Liu, Yu, Chen", "IEEE Internet of Things Journal", 75,
     "Builds hop-count distance vectors via a query mechanism and coordinates forwarding over them; no learning component is described.",
     "We replace the fixed hop-count metric with learned Double Q-values combining depth, energy, link quality and a void penalty.",
     "https://doi.org/10.1109/JIOT.2019.2891910"),
]

ROWS.sort(key=lambda r: (-r[0], -IF[r[3]], -r[4]))


def green(pct):
    """Interpolate from white (0 %) to strong green (100 %)."""
    lo, hi = (255, 255, 255), (99, 190, 123)
    t = max(0, min(100, pct)) / 100
    return "".join(f"{round(a + (b - a) * t):02X}" for a, b in zip(lo, hi))


HEADERS = ["Year", "Title", "Authors", "Journal", "Impact Factor", "Relevance to Our Work (%)",
           "Research Gap", "How Our Work Addresses It", "Link"]
WIDTHS = [7, 52, 30, 30, 9, 12, 52, 52, 44]

wb = Workbook()
ws = wb.active
ws.title = "Literature Survey"

ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HEADERS))
ws.cell(row=1, column=1, value=OUR_WORK)
ws.cell(row=1, column=1).font = Font(bold=True, size=13, color="1B5E20")
ws.cell(row=1, column=1).alignment = Alignment(vertical="center", wrap_text=True)
ws.row_dimensions[1].height = 34

HR = 3
thin = Side(style="thin", color="A5A5A5")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
for c, (h, w) in enumerate(zip(HEADERS, WIDTHS), 1):
    cell = ws.cell(row=HR, column=c, value=h)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1B5E20")
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    cell.border = border
    ws.column_dimensions[get_column_letter(c)].width = w
ws.row_dimensions[HR].height = 32

for i, (year, title, authors, journal, rel, gap, ours, link) in enumerate(ROWS, HR + 1):
    values = [year, title, authors, journal, IF[journal], rel, gap, ours, link]
    fill = PatternFill("solid", fgColor=green(rel))
    for c, v in enumerate(values, 1):
        cell = ws.cell(row=i, column=c, value=v)
        cell.fill = fill
        cell.border = border
        cell.font = Font(color="000000")
        cell.alignment = Alignment(wrap_text=True, vertical="top",
                                   horizontal="center" if c in (1, 5, 6) else "left")
    lc = ws.cell(row=i, column=9)
    lc.hyperlink = link
    lc.font = Font(color="0B3D91", underline="single")
    ws.cell(row=i, column=5).number_format = "0.0"

last = HR + len(ROWS)
table = Table(displayName="LiteratureSurvey", ref=f"A{HR}:{get_column_letter(len(HEADERS))}{last}")
table.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=False)
ws.add_table(table)
ws.freeze_panes = ws.cell(row=HR + 1, column=3)

ws.page_setup.orientation = "landscape"
ws.page_setup.paperSize = ws.PAPERSIZE_A3
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.print_title_rows = f"{HR}:{HR}"

wb.save(OUT)
print("saved", OUT, len(ROWS), "rows")
