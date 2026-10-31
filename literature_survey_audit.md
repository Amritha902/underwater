# Audit: literature_survey_IF5plus.xlsx (50 rows)

Final audit, 31 Oct 2026.

## Result

- All **50 of 50** rows have title, authors, journal, volume/pages and DOI confirmed by two or more independent bibliographic records.
- No duplicate titles or links.
- Every journal has an impact factor of at least 5.5.

## Method

- Each paper was searched by exact title and by DOI.
- Bibliographic details were cross-checked against DBLP, OpenAlex, NASA ADS, ACM DL, IEEE Xplore records, university repositories, library catalogues and citing reference lists.

## Changes made in this audit

1. **Five rows upgraded** from one confirming record to two or more: CAMP, RANR, directional opportunistic routing, DR-DLMA and QELAR.
2. **RANR link** now uses its DOI (10.1109/JIOT.2023.3298522) instead of the AMiner page.
3. **TNSE "Attack Detection … Hybrid Trust Evidence" removed.** Its title is confirmed, but the journal and DOI rest on a single repository record. It was replaced by Guan et al., "Distance-Vector-Based Opportunistic Routing for Underwater Acoustic Sensor Networks" (IEEE IoTJ 2019), which has two confirming records and is more relevant.
4. **Research Gap wording tightened** in 13 rows so each statement only claims what the paper's abstract supports. Examples:
   - "VAPR is energy-unaware" became "rule-based rather than learning-based".
   - "fixed rules, no learning of energy" became "no learning component is described".

## Known limits

- **Links not click-tested.** The audit environment blocks doi.org, Crossref, OpenAlex and DBLP, so the links haven't been opened. The DOIs themselves are confirmed by the records above. To machine-check all 50 links, allow `doi.org` and `api.crossref.org` in the environment's network settings.
- **Impact factors** are journalmetrics.org (JCR-based) values. IEEE JSAC uses its JCR 2021 value (13.1); IEEE TVT is 7.5 or 6.1 depending on source.
- **Year:** the volume/issue year is used. Some papers were online a year earlier (for example FISHER: online 2025, volume 2026).
- **Relevance % and the two gap columns** are analysis based on the abstracts, not figures reported by the papers.
- **Authors:** the QTRU row lists four authors plus "et al." because the full list wasn't visible in any record.

## Row-by-row evidence

| # | Year | Paper | Journal | IF | Evidence (2 or more independent records) |
|---|---|---|---|---|---|
| 1 | 2026 | A Novel Underwater Target Tracking Method in UASNs via Collaborative Deep Reinforcement Learning | Information Fusion | 15.5 | XJTU scholar record; second search confirming Information Fusion vol. 127 and DOI |
| 2 | 2026 | Is FISHER All You Need in the Multi-AUV Underwater Target Tracking Task? | IEEE Transactions on Mobile Computing | 9.2 | OpenAlex (DOI, online 9 Sep 2025); NJIT repository (vol. 25(2) 2091-2106, 2026) |
| 3 | 2026 | Propagation-Aware Scheduling MAC Protocol for Reliable Underwater Swarmed AUV Communications Networks | IEEE Internet of Things Journal | 8.9 | SKKU ISP Lab list (DOI); SKKU faculty page; ResearchGate; ACM DL citation |
| 4 | 2025 | Security and Reliability of Internet of Underwater Things: Architecture, Challenges, and Opportunities | ACM Computing Surveys | 28 | mdsoar; DBLP; Crossref (vol. 57(3) art. 67) |
| 5 | 2025 | A Digital Twin-Based Intelligent Network Architecture for Underwater Acoustic Sensor Networks (DTNA) | IEEE Transactions on Mobile Computing | 9.2 | BUAA/Scopus (DOI, vol. 24(9) 8196-8213); author PDF |
| 6 | 2025 | Multi-AUV Cooperative Underwater Multi-Target Tracking Based on Dynamic-Switching-Enabled Multi-Agent Reinforcement Learning | IEEE Transactions on Mobile Computing | 9.2 | ACM DL (DOI, vol. 24(5) 4296-4311); arXiv author list |
| 7 | 2025 | Underwater Target Tracking Based on Interrupted Software-Defined Multi-AUV Reinforcement Learning: A Multi-AUV Time-Saving MARL Approach | IEEE Transactions on Mobile Computing | 9.2 | ACM DL; DBLP; oa.mg |
| 8 | 2025 | Joint Power Control and Multi-Path Routing for Internet of Underwater Things in Varying Environments (CAMP) | IEEE Internet of Things Journal | 8.9 | NASA ADS (DOI, authors); BUAA; DBLP (vol. 12(11) 15197-15210) |
| 9 | 2025 | Aqua-Sim Fourth Generation: Towards General and Intelligent Simulation for Underwater Acoustic Networks | IEEE Internet of Things Journal | 8.9 | BUAA/Scopus (DOI, vol. 12(15) 30203-30214); arXiv |
| 10 | 2025 | An Intelligent Q-Learning-Based Tree Routing Method in Underwater Acoustic Sensor Networks (QTRU) | Engineering Applications of Artificial Intelligence | 8 | PSAU Elsevier Pure (vol. 152 art. 110753); ScienceDirect page |
| 11 | 2025 | A Survey on Energy Efficient Medium Access Control for Acoustic Wireless Communication Networks in Underwater Environments | Journal of Network and Computer Applications | 8 | ECU repository; X-MOL (DOI) |
| 12 | 2025 | Towards the Underwater Internet of Things for Subsea Oil and Gas Monitoring | Internet of Things (Elsevier) | 7.1 | Glasgow eprints (DOI); RGU repository; ScienceDirect page |
| 13 | 2024 | Design Guidelines on Trust Management for Underwater Wireless Sensor Networks | IEEE Communications Surveys & Tutorials | 46.7 | X-MOL; Bohrium (DOI) |
| 14 | 2024 | Achieving Fair-Effective Communications and Robustness in Underwater Acoustic Sensor Networks: A Semi-Cooperative Approach (SECOPA) | IEEE Transactions on Mobile Computing | 9.2 | BUAA portal; Unpaywall (DOI); arXiv |
| 15 | 2024 | Joint Link Scheduling and Power Allocation in Imperfect and Energy-Constrained Underwater Wireless Sensor Networks (ICRL-JSA) | IEEE Transactions on Mobile Computing | 9.2 | DBLP; library catalogue (DOI) |
| 16 | 2024 | A Federated Deep Reinforcement Learning-Based Trust Model in Underwater Acoustic Sensor Networks | IEEE Transactions on Mobile Computing | 9.2 | Oulu repository; DBLP (DOI) |
| 17 | 2024 | Longevity-Oriented and Reliable Forwarding Percolation Routing in Underwater Acoustic Sensor Networks (LRP) | IEEE Internet of Things Journal | 8.9 | UVic PDF; NWPU portal; DBLP; OpenAlex |
| 18 | 2024 | Dynamic Packet Routing Based on Acoustic Signal Curve Propagation in the AUV-Assisted IoUT | IEEE Internet of Things Journal | 8.9 | DBLP (vol. 11(6) 9854-9869); Bohrium (DOI) |
| 19 | 2024 | AUV-Assisted Node Repair for IoUT Relying on Multiagent Reinforcement Learning (RANR) | IEEE Internet of Things Journal | 8.9 | DBLP (DOI 10.1109/JIOT.2023.3298522, vol. 11(3) 4139-4151); AMiner; ResearchGate |
| 20 | 2024 | Environment- and Energy-Aware AUV-Assisted Data Collection for the Internet of Underwater Things | IEEE Internet of Things Journal | 8.9 | Researchr; BUAA portal; author PDF (DOI) |
| 21 | 2024 | Toward a Sustainable Internet of Underwater Things Based on AUVs, SWIPT, and Reinforcement Learning | IEEE Internet of Things Journal | 8.9 | Glasgow eprints (DOI, vol. 11(5) 7640-7651); Ajman portal; arXiv |
| 22 | 2024 | Energy-Efficient Data Collection Scheme Based on Value of Information in Underwater Acoustic Sensor Networks | IEEE Internet of Things Journal | 8.9 | Bohrium; Reviewer.ly; Nile Univ. index (DOI) |
| 23 | 2024 | A Medium Access Control Protocol Based on Parity Group-Graph Coloring for Underwater AUV-Aided Data Collection | IEEE Internet of Things Journal | 8.9 | OpenAlex (DOI); DBLP (vol. 11(4) 5967-5979); UTB catalogue |
| 24 | 2024 | Efficient AUV-Aided Localization for Large-Scale Underwater Acoustic Sensor Networks | IEEE Internet of Things Journal | 8.9 | BUAA portal; Unpaywall (DOI) |
| 25 | 2024 | Survey of AI-Driven Routing Protocols in Underwater Acoustic Networks for Enhanced Communication Efficiency | Ocean Engineering | 5.5 | ScienceDirect page (vol. 314); search record with DOI and authors |
| 26 | 2024 | End-to-End Multi-Sensor Fusion Method Based on Deep Reinforcement Learning in UASNs | Ocean Engineering | 5.5 | NWPU portal; Bohrium (DOI) |
| 27 | 2023 | Environment-Aware AUV Trajectory Design and Resource Management for Multi-Tier Underwater Computing | IEEE Journal on Selected Areas in Communications | 13.1 | Southampton eprints; OpenAlex (DOI, vol. 41(2) 474-490); arXiv |
| 28 | 2023 | Underwater Pollution Tracking Based on Software-Defined Multi-Tier Edge Computing in 6G-Based Underwater Wireless Networks | IEEE Journal on Selected Areas in Communications | 13.1 | Unpaywall; OpenAlex; Peeref; oa.mg (DOI, vol. 41(2) 491-503) |
| 29 | 2023 | An SDN-Enabled Framework for a Load-Balanced and QoS-Aware Internet of Underwater Things (SQAR) | IEEE Internet of Things Journal | 8.9 | DBLP (vol. 10(9) 7824-7834); Bohrium; UTB catalogue |
| 30 | 2023 | An Opportunistic Routing Based on Directional Transmission in the Internet of Underwater Things | IEEE Internet of Things Journal | 8.9 | IEEE Xplore document 10104092; Researchr BibTeX (DOI, vol. 10(18) 16392-16403); Springer reference list |
| 31 | 2022 | Federated Meta-Learning Enhanced Acoustic Radio Cooperative Framework for Ocean of Things | IEEE Journal of Selected Topics in Signal Processing | 13.7 | DBLP (vol. 16(3) 474-486); OpenAlex (DOI); AMiner; arXiv |
| 32 | 2022 | Modulation Recognition of Underwater Acoustic Signals Using Deep Hybrid Neural Networks | IEEE Transactions on Wireless Communications | 10.7 | DBLP (vol. 21(8) 5977-5988); author-hosted PDF; Bohrium |
| 33 | 2022 | Deep Reinforcement Learning Based MAC Protocol for Underwater Acoustic Networks (DR-DLMA) | IEEE Transactions on Mobile Computing | 9.2 | Library catalogue; ACM reference list; OUCI reference list (DOI, vol. 21(5) 1625-1638) |
| 34 | 2022 | A Trust Update Mechanism Based on Reinforcement Learning in Underwater Acoustic Sensor Networks | IEEE Transactions on Mobile Computing | 9.2 | Loughborough repository; Bohrium (DOI, vol. 21(3) 811-821) |
| 35 | 2022 | Energy-Efficient Guiding-Network-Based Routing for Underwater Wireless Sensor Networks (EEGNBR) | IEEE Internet of Things Journal | 8.9 | DBLP (vol. 9(21) 21702-21711); Bohrium (DOI) |
| 36 | 2022 | Opportunistic Routing for Opto-Acoustic Internet of Underwater Things (SectOR) | IEEE Internet of Things Journal | 8.9 | UAEU portal (vol. 9(3) 2165-2179); Southampton eprints (DOI); arXiv |
| 37 | 2022 | AUV-Aided Hybrid Data Collection Scheme Based on Value of Information for Internet of Underwater Things | IEEE Internet of Things Journal | 8.9 | Bohrium; Reviewer.ly (DOI, 2022) |
| 38 | 2022 | Stochastic Optimization-Aided Energy-Efficient Information Collection in Internet of Underwater Things Networks | IEEE Internet of Things Journal | 8.9 | BUAA portal; DBLP (vol. 9(3) 1775-1789); OpenAlex (DOI) |
| 39 | 2022 | Coverage Enhancement of Underwater Internet of Things Using Multilevel Acoustic Communication Networks | IEEE Internet of Things Journal | 8.9 | Maynooth MURAL (DOI, vol. 9(24) 25373-25385); KAUST page |
| 40 | 2021 | Internet of Underwater Things and Big Marine Data Analytics - A Comprehensive Survey | IEEE Communications Surveys & Tutorials | 46.7 | JCU portfolio; Southampton eprints; marineinfo (DOI, vol. 23(2) 904-956) |
| 41 | 2021 | Anypath Routing Protocol Design via Q-Learning for Underwater Sensor Networks (QLFR) | IEEE Internet of Things Journal | 8.9 | Peeref (DOI, vol. 8(10) 8173-8190); arXiv with IoTJ header |
| 42 | 2021 | AoI-Inspired Collaborative Information Collection for AUV-Assisted Internet of Underwater Things | IEEE Internet of Things Journal | 8.9 | HIT scholar record; citing reference (DOI, vol. 8(19) 14559-14571) |
| 43 | 2021 | Reinforcement Learning-Based Opportunistic Routing Protocol for Underwater Acoustic Sensor Networks (RLOR) | IEEE Transactions on Vehicular Technology | 7.5 | XJTLU portal; DBLP (DOI) |
| 44 | 2020 | Routing Protocol Design for Underwater Optical Wireless Sensor Networks: A Multiagent Reinforcement Learning Approach | IEEE Internet of Things Journal | 8.9 | OpenAlex (DOI); OUCI |
| 45 | 2020 | AUV-Aided Energy-Efficient Data Collection in Underwater Acoustic Sensor Networks (AEEDCO) | IEEE Internet of Things Journal | 8.9 | Library record (vol. 7(10) 10010-10022); Bohrium (DOI) |
| 46 | 2020 | A Software-Defined Opto-Acoustic Network Architecture for Internet of Underwater Things | IEEE Communications Magazine | 8.2 | Southampton eprints; Peeref; X-MOL (DOI, vol. 58(4) 88-94) |
| 47 | 2019 | CARMA: Channel-Aware Reinforcement Learning-Based Multi-Path Adaptive Routing for Underwater Wireless Sensor Networks | IEEE Journal on Selected Areas in Communications | 13.1 | Sapienza; Tor Vergata; NSF PAR; Northeastern PDF (DOI) |
| 48 | 2019 | Distance-Vector-Based Opportunistic Routing for Underwater Acoustic Sensor Networks | IEEE Internet of Things Journal | 8.9 | IEEE Xplore record via Unpaywall (DOI, vol. 6(2)); multiple reference lists (authors, pp. 3831-3839) |
| 49 | 2013 | VAPR: Void-Aware Pressure Routing for Underwater Sensor Networks | IEEE Transactions on Mobile Computing | 9.2 | KAIST repository/PDF; index record (DOI, vol. 12(5) 895-908) |
| 50 | 2010 | QELAR: A Machine-Learning-Based Adaptive Routing Protocol for Energy-Efficient and Lifetime-Extended Underwater Sensor Networks | IEEE Transactions on Mobile Computing | 9.2 | ACM DL page (DOI 10.1109/TMC.2010.28); IEEE Xplore document 5408367; DBLP (vol. 9(6) 796-809) |
