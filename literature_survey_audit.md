# Audit: literature_survey_IF5plus.xlsx (50 rows)

Audit date: 31 Oct 2026. This is the second audit; it covers all 50 rows.

## Method

- Every paper was checked by searching its exact title and/or DOI.
- Title, authors, journal, volume/pages and DOI were cross-checked against bibliographic records: DBLP, OpenAlex, university repositories, library catalogues and publisher pages.
- **Limitation:** publisher sites and doi.org can't be opened from the audit environment, so the links themselves were not click-tested.

## Status legend

- **A**: two or more independent records agree.
- **B**: one record. Very likely correct; click once to confirm.

## Summary

- Rows: 50. Status A: 44. Status B: 6.
- No duplicate titles or links.
- Lowest impact factor: 5.5 (Ocean Engineering). All journals are at or above 5.

## Fixes made during this round

- Ocean Engineering impact factor (5.5) was missing from the lookup table, so it was added.
- The full title of the IEEE TWC 2022 modulation-recognition paper was confirmed on DBLP before keeping the row.
- Leads that were rejected because a field couldn't be confirmed:
  - Distance-vector opportunistic routing (IEEE IoTJ 2019): authors not found.
  - Geng and Zheng (IEEE TNNLS 2023): DOI not confirmed.
  - Underwater MI communications survey (IEEE COMST 2019): DOI not found.
  - Two Ocean Engineering 2024–2025 localization papers: authors not found.
  - "Improved Newton iteration + Kalman filter" localization (IEEE TMC 2024): title not found.
  - Multi-objective offline-RL AUV data collection: only an arXiv version exists.
  - Clustering guiding-network routing: conference paper, not a journal.
  - Optical networking survey (Ad Hoc Networks): impact factor below 5.

## Notes on other columns

- **Impact factor:** journalmetrics.org (JCR-based) values. JSAC uses its JCR 2021 value (13.1); IEEE TVT has 7.5 or 6.1 depending on source.
- **Relevance %, Research Gap, How Our Work Addresses It:** my analysis based on each paper's abstract, not values reported by the papers.

## Rows to click-check first (status B)

- Joint Power Control and Multi-Path Routing for Internet of Underwater Things in Varying Environments (CAMP)
- Attack Detection and Optimal Deployment for Underwater Constrained Wireless Sensor Networks via Hybrid Trust Evidence
- AUV-Assisted Node Repair for IoUT Relying on Multiagent Reinforcement Learning (RANR)
- An Opportunistic Routing Based on Directional Transmission in the Internet of Underwater Things
- Deep Reinforcement Learning Based MAC Protocol for Underwater Acoustic Networks (DR-DLMA)
- QELAR: A Machine-Learning-Based Adaptive Routing Protocol for Energy-Efficient and Lifetime-Extended Underwater Sensor Networks

## Row-by-row results

| # | Year | Paper | Journal | IF | Status | Evidence |
|---|---|---|---|---|---|---|
| 1 | 2026 | A Novel Underwater Target Tracking Method in UASNs via Collaborative Deep Reinforcement Learning | Information Fusion | 15.5 | A | XJTU scholar record + second search confirming Information Fusion vol. 127 and DOI |
| 2 | 2026 | Is FISHER All You Need in the Multi-AUV Underwater Target Tracking Task? | IEEE Transactions on Mobile Computing | 9.2 | A | OpenAlex (DOI, online 9 Sep 2025) + NJIT repository (vol. 25(2) 2091-2106, 2026). Year shown as 2026 (volume year) |
| 3 | 2026 | Propagation-Aware Scheduling MAC Protocol for Reliable Underwater Swarmed AUV Communications Networks | IEEE Internet of Things Journal | 8.9 | A | SKKU ISP Lab list (DOI), SKKU faculty page, ResearchGate, ACM DL citation |
| 4 | 2025 | Security and Reliability of Internet of Underwater Things: Architecture, Challenges, and Opportunities | ACM Computing Surveys | 28 | A | mdsoar, DBLP, Crossref; vol. 57(3) art. 67 |
| 5 | 2025 | A Digital Twin-Based Intelligent Network Architecture for Underwater Acoustic Sensor Networks (DTNA) | IEEE Transactions on Mobile Computing | 9.2 | A | BUAA/Scopus (DOI, vol. 24(9) 8196-8213), author PDF |
| 6 | 2025 | Multi-AUV Cooperative Underwater Multi-Target Tracking Based on Dynamic-Switching-Enabled Multi-Agent Reinforcement Learning | IEEE Transactions on Mobile Computing | 9.2 | A | ACM DL (DOI, vol. 24(5) 4296-4311), arXiv author list |
| 7 | 2025 | Underwater Target Tracking Based on Interrupted Software-Defined Multi-AUV Reinforcement Learning: A Multi-AUV Time-Saving MARL Approach | IEEE Transactions on Mobile Computing | 9.2 | A | ACM DL, DBLP, oa.mg |
| 8 | 2025 | Joint Power Control and Multi-Path Routing for Internet of Underwater Things in Varying Environments (CAMP) | IEEE Internet of Things Journal | 8.9 | B | BUAA + DBLP (title, authors, vol. 12(11)); DOI from JLU faculty list only |
| 9 | 2025 | Aqua-Sim Fourth Generation: Towards General and Intelligent Simulation for Underwater Acoustic Networks | IEEE Internet of Things Journal | 8.9 | A | BUAA/Scopus (DOI, vol. 12(15) 30203-30214), arXiv |
| 10 | 2025 | An Intelligent Q-Learning-Based Tree Routing Method in Underwater Acoustic Sensor Networks (QTRU) | Engineering Applications of Artificial Intelligence | 8 | A | PSAU Elsevier Pure (vol. 152 art. 110753), ScienceDirect page (no DOI link; ScienceDirect URL used) |
| 11 | 2025 | A Survey on Energy Efficient Medium Access Control for Acoustic Wireless Communication Networks in Underwater Environments | Journal of Network and Computer Applications | 8 | A | ECU repository, X-MOL (DOI) |
| 12 | 2025 | Attack Detection and Optimal Deployment for Underwater Constrained Wireless Sensor Networks via Hybrid Trust Evidence | IEEE Transactions on Network Science and Engineering | 7.9 | B | UMBC mdsoar repository only (DOI) |
| 13 | 2025 | Towards the Underwater Internet of Things for Subsea Oil and Gas Monitoring | Internet of Things (Elsevier) | 7.1 | A | Glasgow eprints (DOI), RGU repository |
| 14 | 2024 | Design Guidelines on Trust Management for Underwater Wireless Sensor Networks | IEEE Communications Surveys & Tutorials | 46.7 | A | X-MOL, Bohrium (DOI) |
| 15 | 2024 | Achieving Fair-Effective Communications and Robustness in Underwater Acoustic Sensor Networks: A Semi-Cooperative Approach (SECOPA) | IEEE Transactions on Mobile Computing | 9.2 | A | BUAA portal, Unpaywall (DOI), arXiv |
| 16 | 2024 | Joint Link Scheduling and Power Allocation in Imperfect and Energy-Constrained Underwater Wireless Sensor Networks (ICRL-JSA) | IEEE Transactions on Mobile Computing | 9.2 | A | DBLP ZhangGLSYC24, library catalogue (DOI) |
| 17 | 2024 | A Federated Deep Reinforcement Learning-Based Trust Model in Underwater Acoustic Sensor Networks | IEEE Transactions on Mobile Computing | 9.2 | A | Oulu repository, DBLP (DOI) |
| 18 | 2024 | Longevity-Oriented and Reliable Forwarding Percolation Routing in Underwater Acoustic Sensor Networks (LRP) | IEEE Internet of Things Journal | 8.9 | A | UVic PDF, NWPU portal, DBLP, OpenAlex |
| 19 | 2024 | Dynamic Packet Routing Based on Acoustic Signal Curve Propagation in the AUV-Assisted IoUT | IEEE Internet of Things Journal | 8.9 | A | DBLP WangDJZRH24 (vol. 11(6) 9854-9869), Bohrium (DOI) |
| 20 | 2024 | AUV-Assisted Node Repair for IoUT Relying on Multiagent Reinforcement Learning (RANR) | IEEE Internet of Things Journal | 8.9 | B | DBLP (authors, vol. 11(3)), AMiner; no DOI found, link is AMiner record |
| 21 | 2024 | Environment- and Energy-Aware AUV-Assisted Data Collection for the Internet of Underwater Things | IEEE Internet of Things Journal | 8.9 | A | Researchr, BUAA portal, author PDF (DOI) |
| 22 | 2024 | Toward a Sustainable Internet of Underwater Things Based on AUVs, SWIPT, and Reinforcement Learning | IEEE Internet of Things Journal | 8.9 | A | Glasgow eprints (DOI, vol. 11(5) 7640-7651), Ajman portal, arXiv |
| 23 | 2024 | Energy-Efficient Data Collection Scheme Based on Value of Information in Underwater Acoustic Sensor Networks | IEEE Internet of Things Journal | 8.9 | A | Bohrium, Reviewer.ly, Nile Univ. index (DOI) |
| 24 | 2024 | A Medium Access Control Protocol Based on Parity Group-Graph Coloring for Underwater AUV-Aided Data Collection | IEEE Internet of Things Journal | 8.9 | A | OpenAlex (DOI), DBLP (vol. 11(4) 5967-5979), UTB catalogue |
| 25 | 2024 | Efficient AUV-Aided Localization for Large-Scale Underwater Acoustic Sensor Networks | IEEE Internet of Things Journal | 8.9 | A | BUAA portal, Unpaywall (DOI) |
| 26 | 2024 | Survey of AI-Driven Routing Protocols in Underwater Acoustic Networks for Enhanced Communication Efficiency | Ocean Engineering | 5.5 | A | ScienceDirect page (vol. 314), search record giving DOI and authors |
| 27 | 2024 | End-to-End Multi-Sensor Fusion Method Based on Deep Reinforcement Learning in UASNs | Ocean Engineering | 5.5 | A | NWPU portal, Bohrium (DOI) |
| 28 | 2023 | Environment-Aware AUV Trajectory Design and Resource Management for Multi-Tier Underwater Computing | IEEE Journal on Selected Areas in Communications | 13.1 | A | Southampton eprints, OpenAlex (DOI, vol. 41(2) 474-490), arXiv |
| 29 | 2023 | Underwater Pollution Tracking Based on Software-Defined Multi-Tier Edge Computing in 6G-Based Underwater Wireless Networks | IEEE Journal on Selected Areas in Communications | 13.1 | A | Unpaywall, OpenAlex, Peeref, oa.mg (DOI, vol. 41(2) 491-503) |
| 30 | 2023 | An SDN-Enabled Framework for a Load-Balanced and QoS-Aware Internet of Underwater Things (SQAR) | IEEE Internet of Things Journal | 8.9 | A | DBLP (vol. 10(9) 7824-7834), Bohrium, UTB catalogue |
| 31 | 2023 | An Opportunistic Routing Based on Directional Transmission in the Internet of Underwater Things | IEEE Internet of Things Journal | 8.9 | B | Researchr BibTeX (DOI, vol. 10(18) 16392-16403) + citing reference list |
| 32 | 2022 | Federated Meta-Learning Enhanced Acoustic Radio Cooperative Framework for Ocean of Things | IEEE Journal of Selected Topics in Signal Processing | 13.7 | A | DBLP (vol. 16(3) 474-486), OpenAlex (DOI), AMiner, arXiv |
| 33 | 2022 | Modulation Recognition of Underwater Acoustic Signals Using Deep Hybrid Neural Networks | IEEE Transactions on Wireless Communications | 10.7 | A | DBLP (vol. 21(8) 5977-5988), author-hosted PDF, Bohrium |
| 34 | 2022 | Deep Reinforcement Learning Based MAC Protocol for Underwater Acoustic Networks (DR-DLMA) | IEEE Transactions on Mobile Computing | 9.2 | B | Library catalogue records (DOI, vol. 21(5) 1625-1638) |
| 35 | 2022 | A Trust Update Mechanism Based on Reinforcement Learning in Underwater Acoustic Sensor Networks | IEEE Transactions on Mobile Computing | 9.2 | A | Loughborough repository, Bohrium (DOI, vol. 21(3) 811-821) |
| 36 | 2022 | Energy-Efficient Guiding-Network-Based Routing for Underwater Wireless Sensor Networks (EEGNBR) | IEEE Internet of Things Journal | 8.9 | A | DBLP LiuJYMG22 (vol. 9(21) 21702-21711), Bohrium (DOI) |
| 37 | 2022 | Opportunistic Routing for Opto-Acoustic Internet of Underwater Things (SectOR) | IEEE Internet of Things Journal | 8.9 | A | UAEU portal (vol. 9(3) 2165-2179), Southampton eprints (DOI), arXiv |
| 38 | 2022 | AUV-Aided Hybrid Data Collection Scheme Based on Value of Information for Internet of Underwater Things | IEEE Internet of Things Journal | 8.9 | A | Bohrium, Reviewer.ly (DOI, 2022) |
| 39 | 2022 | Stochastic Optimization-Aided Energy-Efficient Information Collection in Internet of Underwater Things Networks | IEEE Internet of Things Journal | 8.9 | A | BUAA portal, DBLP (vol. 9(3) 1775-1789), OpenAlex (DOI) |
| 40 | 2022 | Coverage Enhancement of Underwater Internet of Things Using Multilevel Acoustic Communication Networks | IEEE Internet of Things Journal | 8.9 | A | Maynooth MURAL (DOI, vol. 9(24) 25373-25385), KAUST page |
| 41 | 2021 | Internet of Underwater Things and Big Marine Data Analytics - A Comprehensive Survey | IEEE Communications Surveys & Tutorials | 46.7 | A | JCU portfolio, Southampton eprints, marineinfo (DOI, vol. 23(2) 904-956) |
| 42 | 2021 | Anypath Routing Protocol Design via Q-Learning for Underwater Sensor Networks (QLFR) | IEEE Internet of Things Journal | 8.9 | A | Peeref (DOI, vol. 8(10) 8173-8190), arXiv with IoTJ header |
| 43 | 2021 | AoI-Inspired Collaborative Information Collection for AUV-Assisted Internet of Underwater Things | IEEE Internet of Things Journal | 8.9 | A | HIT scholar record, citing reference (DOI, vol. 8(19) 14559-14571) |
| 44 | 2021 | Reinforcement Learning-Based Opportunistic Routing Protocol for Underwater Acoustic Sensor Networks (RLOR) | IEEE Transactions on Vehicular Technology | 7.5 | A | XJTLU portal, DBLP (DOI) |
| 45 | 2020 | Routing Protocol Design for Underwater Optical Wireless Sensor Networks: A Multiagent Reinforcement Learning Approach | IEEE Internet of Things Journal | 8.9 | A | OpenAlex (DOI), OUCI |
| 46 | 2020 | AUV-Aided Energy-Efficient Data Collection in Underwater Acoustic Sensor Networks (AEEDCO) | IEEE Internet of Things Journal | 8.9 | A | Library record (vol. 7(10) 10010-10022), Bohrium (DOI) |
| 47 | 2020 | A Software-Defined Opto-Acoustic Network Architecture for Internet of Underwater Things | IEEE Communications Magazine | 8.2 | A | Southampton eprints, Peeref, X-MOL (DOI, vol. 58(4) 88-94) |
| 48 | 2019 | CARMA: Channel-Aware Reinforcement Learning-Based Multi-Path Adaptive Routing for Underwater Wireless Sensor Networks | IEEE Journal on Selected Areas in Communications | 13.1 | A | Sapienza, Tor Vergata, NSF PAR, Northeastern PDF (DOI) |
| 49 | 2013 | VAPR: Void-Aware Pressure Routing for Underwater Sensor Networks | IEEE Transactions on Mobile Computing | 9.2 | A | KAIST repository/PDF, index record (DOI, vol. 12(5) 895-908) |
| 50 | 2010 | QELAR: A Machine-Learning-Based Adaptive Routing Protocol for Energy-Efficient and Lifetime-Extended Underwater Sensor Networks | IEEE Transactions on Mobile Computing | 9.2 | B | DBLP (vol. 9(6) 796-809); DOI from one citation record |
