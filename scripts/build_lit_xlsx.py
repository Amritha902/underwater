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
    "IEEE Journal on Selected Areas in Communications": 13.1,
    "IEEE Transactions on Mobile Computing": 9.2,
    "IEEE Internet of Things Journal": 8.9,
    "Engineering Applications of Artificial Intelligence": 8.0,
    "Journal of Network and Computer Applications": 8.0,
    "IEEE Transactions on Network Science and Engineering": 7.9,
    "IEEE Transactions on Vehicular Technology": 7.5,
    "Internet of Things (Elsevier)": 7.1,
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
     "Single-estimator Q-learning (prone to overestimation on noisy acoustic links); tree topology; evaluated in NS-2.",
     "We replace Q-learning with Double Q-learning to remove overestimation bias, add a learned void penalty, and evaluate in ns-3.",
     "https://www.sciencedirect.com/science/article/abs/pii/S0952197625007535"),
    (2025, "Joint Power Control and Multi-Path Routing for Internet of Underwater Things in Varying Environments (CAMP)",
     "Xu, Song, Liu, Pan, Xu, Cui", "IEEE Internet of Things Journal", 80,
     "Model-based reliability optimisation with multipath at the source; nodes do not learn from experience as channel conditions change.",
     "Our nodes learn link quality online through Double Q-learning, adapting next-hop choice without an explicit channel model.",
     "https://doi.org/10.1109/JIOT.2025.3527692"),
    (2025, "Aqua-Sim Fourth Generation: Towards General and Intelligent Simulation for Underwater Acoustic Networks",
     "Guo, Song, Chen, Huangfu, Liu, Cui", "IEEE Internet of Things Journal", 70,
     "Provides an ns-3 based simulation platform; does not propose or benchmark a learning-based routing protocol.",
     "We use ns-3 underwater modules to implement DQ-EVDR and benchmark it against DBR, VBF and Q-learning baselines.",
     "https://doi.org/10.1109/JIOT.2025.3571022"),
    (2025, "A Digital Twin-Based Intelligent Network Architecture for Underwater Acoustic Sensor Networks (DTNA)",
     "Song, Huangfu, Guo, Liu, Cui, Shen", "IEEE Transactions on Mobile Computing", 50,
     "Architecture-level framework relying on digital twins and MARL to compensate for scarce training data; heavy for individual sensor nodes.",
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
    (2025, "Attack Detection and Optimal Deployment for Underwater Constrained Wireless Sensor Networks via Hybrid Trust Evidence",
     "Jiang, Zhou, Luo, Cui, Wang, Song", "IEEE Transactions on Network Science and Engineering", 25,
     "Security and deployment focus; routing energy and void handling are not the objective.",
     "Our reward function can later include a trust term; the core work targets energy and void-aware forwarding.",
     "https://doi.org/10.1109/TNSE.2025.3539320"),
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
     "Relies on AUVs (multi-agent SAC) to collect data; costly mobile infrastructure, no multi-hop sensor routing.",
     "We deliver data through multi-hop routing among static nodes, without requiring AUVs.",
     "https://doi.org/10.1109/JIOT.2024.3395568"),
    (2024, "AUV-Assisted Node Repair for IoUT Relying on Multiagent Reinforcement Learning (RANR)",
     "Wang, Zhang, Wang, Jiang, Wei, Ren", "IEEE Internet of Things Journal", 40,
     "Repairs failed nodes (which cause routing voids) using AUVs; routing itself does not adapt around voids.",
     "We let routing adapt around voids immediately through a learned void penalty, without waiting for repair.",
     "https://aminer.cn/pub/6565d23a349c5a0001538abc/auv-assisted-node-repair-for-iout-relying-on-multiagent-reinforcement-learning"),
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
     "RL-based QoS routing depends on SDN controllers; centralised control is costly over acoustic links.",
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
     "Single-estimator RL opportunistic routing; overestimation under noisy links not addressed.",
     "We extend the RL opportunistic routing idea with Double Q-learning and an explicit void penalty, evaluated in ns-3.",
     "https://doi.org/10.1109/TVT.2021.3058282"),
    (2020, "Routing Protocol Design for Underwater Optical Wireless Sensor Networks: A Multiagent Reinforcement Learning Approach",
     "Li, Hu, Zhang, Yang", "IEEE Internet of Things Journal", 70,
     "Designed for optical links, which are short-range; acoustic delay and energy constraints differ.",
     "We target acoustic sensor networks, the dominant long-range underwater technology.",
     "https://doi.org/10.1109/JIOT.2020.2989924"),
    (2019, "CARMA: Channel-Aware Reinforcement Learning-Based Multi-Path Adaptive Routing for Underwater Wireless Sensor Networks",
     "Di Valerio, Lo Presti, Petrioli, Picari, Spaccini, Basagni", "IEEE Journal on Selected Areas in Communications", 85,
     "Distributed RL routing with standard value estimates; evaluated in SUNSET, not ns-3.",
     "We add Double Q-learning to reduce estimation bias and provide an open ns-3 evaluation.",
     "https://doi.org/10.1109/JSAC.2019.2933968"),
    (2010, "QELAR: A Machine-Learning-Based Adaptive Routing Protocol for Energy-Efficient and Lifetime-Extended Underwater Sensor Networks",
     "Hu, Fei", "IEEE Transactions on Mobile Computing", 90,
     "Early Q-learning UASN routing protocol; later work reports slow convergence with many nodes or high node mobility.",
     "We build on QELAR's energy-aware Q-learning, adding Double Q-learning, depth progress and a learned void penalty.",
     "https://doi.org/10.1109/TMC.2010.28"),
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
