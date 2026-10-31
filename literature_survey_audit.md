# Audit: literature_survey_IF5plus.xlsx

Audit date: 31 Oct 2026. Rows audited: 29 (28 after fixes).

## Method

- Each paper was re-checked by searching its exact title and/or DOI. Title, authors, journal, volume/pages and DOI were cross-checked against bibliographic records: DBLP, university research portals, publisher repositories and library catalogues.
- **Limitation:** publisher pages (IEEE Xplore, ScienceDirect, doi.org) could not be opened from the audit environment, so I couldn't click-test whether each DOI link resolves. "Confirmed" means a bibliographic record pairs that DOI with that title.

## Status legend

- **A**: confirmed by 2 or more independent records.
- **B**: confirmed by 1 record. Very likely correct, but open the link once to check.
- **Fixed**: an error was found and corrected.
- **Removed**: couldn't be confirmed.

## Results

| # | Paper (short) | Year / Journal | Status | Evidence | Action |
|---|---|---|---|---|---|
| 1 | Target tracking via collaborative DRL | 2026 Information Fusion | B | XJTU scholar record pairs title, authors and DOI 10.1016/j.inffus.2025.103797 | — |
| 2 | Propagation-aware scheduling MAC (AUV swarm) | 2026 IEEE IoTJ | A | SKKU ISP Lab publication list (DOI), SKKU faculty page, ResearchGate, ACM DL citation | — |
| 3 | Security & reliability of IoUT (survey) | 2025 ACM CSUR | A | mdsoar, DBLP, Crossref; vol 57(3), art. 67 | — |
| 4 | DTNA digital twin architecture | 2025 IEEE TMC | A | BUAA/Scopus record (DOI, vol 24(9) 8196–8213), author PDF | — |
| 5 | Multi-AUV tracking, Dynamic-Switching MARL | 2025 IEEE TMC | A | ACM DL page (DOI, vol 24(5) 4296–4311), arXiv 2404.13654 | **Fixed** authors: was "Wang, Lin, Han, Li, et al."; now "Wang, Lin, Han, Zhu, Li, Wang, Ma" |
| 6 | Interrupted SD multi-AUV RL tracking | 2025 IEEE TMC | A | ACM DL page, DBLP, oa.mg (DOI) | — |
| 7 | CAMP: joint power control + multipath routing | 2025 IEEE IoTJ | B | Title, authors, vol 12(11) 15197–15210 confirmed by BUAA and DBLP; DOI from JLU faculty list only | Check DOI link |
| 8 | Aqua-Sim FG simulator | 2025 IEEE IoTJ | A | BUAA/Scopus record (DOI, vol 12(15) 30203–30214), arXiv 2410.20698 | — |
| 9 | QTRU Q-learning tree routing | 2025 EAAI | A | PSAU Elsevier Pure record (vol 152, art. 110753), ScienceDirect page | Link goes to the ScienceDirect article page (no DOI found) |
| 10 | Energy-efficient MAC survey | 2025 JNCA | A | ECU repository (vol 235, Mar 2025), X-MOL (DOI) | — |
| 11 | Attack detection via hybrid trust evidence | 2025 IEEE TNSE | B | UMBC mdsoar repository (DOI 10.1109/TNSE.2025.3539320) | — |
| 12 | Underwater IoT for subsea oil & gas | 2025 Internet of Things | A | Univ. of Glasgow eprints (DOI, vol 30, art. 101510), RGU repository | — |
| 13 | Trust management design guidelines | 2024 IEEE COMST | A | X-MOL, Bohrium (DOI, online 16 Apr 2024) | — |
| 14 | SECOPA semi-cooperative power allocation | 2024 IEEE TMC | A | BUAA portal (vol 23(5) 5722–5739), Unpaywall (DOI), arXiv 2508.07578 | — |
| 15 | ICRL-JSA link scheduling + power | 2024 IEEE TMC | A | DBLP ZhangGLSYC24, library catalogue (DOI, vol 23(10) 9863–9880) | Author conflict from earlier search resolved: DBLP confirms the listed authors |
| 16 | Federated DRL trust model | 2024 IEEE TMC | A | Oulu repository, DBLP HeHLTWY24 (DOI, vol 23(5) 5150–5161) | — |
| 17 | LRP percolation routing | 2024 IEEE IoTJ | A | Author PDF (UVic), NWPU portal, DBLP, OpenAlex (DOI) | — |
| 18 | RANR AUV node repair | 2024 IEEE IoTJ | B | DBLP (authors, vol 11(3) 4139–4151), AMiner (title/abstract) | No DOI found; link goes to the AMiner record, **not** the publisher |
| 19 | Environment- & energy-aware AUV data collection | 2024 IEEE IoTJ | A | Researchr, BUAA portal, author PDF; DOI 10.1109/JIOT.2024.3395568 | **Fixed** link: was the BUAA record; now the DOI |
| 20 | VoI-based energy-efficient data collection | 2024 IEEE IoTJ | A | Bohrium, Reviewer.ly, Nile Univ. index (DOI, vol 11(10) 18255–18265) | **Fixed** authors: was "Liu, et al."; now "Liu, Liang, Yuan, Chan, Guan" |
| 21 | EAL AUV-aided localization | 2024 IEEE IoTJ | A | BUAA portal, Unpaywall (DOI, vol 11(19) 31776–31790) | — |
| 22 | SDN load-balanced QoS IoUT (SQAR) | 2023 IEEE IoTJ | A | DBLP (vol 10(9) 7824–7834), Bohrium, UTB catalogue (DOI) | — |
| 23 | TUMRL RL trust update | 2022 IEEE TMC | A | Loughborough repository, Bohrium (vol 21(3) 811–821, DOI) | **Fixed** authors: was "He, Han, et al."; now "He, Han, Jiang, Wang, Martinez-Garcia" |
| 24 | AUV-aided hybrid VoI data collection | 2022 IEEE IoTJ | A | Bohrium, Reviewer.ly (DOI, 2022) | **Fixed** authors: was "Liu, et al."; now "Liu, Meng, Liu, Yang, Wang" |
| 25 | RLOR RL opportunistic routing | 2021 IEEE TVT | A | XJTLU portal, DBLP (DOI, vol 70(3) 2756–2770) | — |
| 26 | DMARL optical routing | 2020 IEEE IoTJ | A | OpenAlex (DOI), OUCI, MARL survey citation | — |
| 27 | CARMA | 2019 IEEE JSAC | A | Sapienza, Tor Vergata, NSF PAR, Northeastern PDF (DOI) | — |
| 28 | QELAR | 2010 IEEE TMC | B | Title, authors, vol 9(6) 796–809 confirmed by DBLP; DOI 10.1109/TMC.2010.28 from one citation record only | Check DOI link |
| — | Visual-inertial-acoustic-depth fusion localization | 2026 IEEE IoTJ | **Removed** | Exact title not found. The same authors' arXiv paper (2510.21215) has a different title ("…SLAM with DVL Preintegration…"), so the journal record couldn't be matched | Deleted row |

## Other columns

- **Impact Factor:** values come from journalmetrics.org (JCR-based), but the JCR year isn't the same for every journal:
  - IEEE IoTJ: 8.9 is the JCR 2024 value, from the journal's own site.
  - IEEE TVT: 7.5 is the newest release; the IEEE VTS page gives 6.1 for 2024.
  - IEEE JSAC: 13.1 is the JCR 2021 value, because no newer one was found.

  Every journal is still above 5 under any of these values.
- **Relevance (%):** my judgement of how close each paper is to DQ-EVDR. It is not a measured value.
- **Research Gap / How Our Work Addresses It:** my analysis based on each paper's abstract. One statement went beyond the evidence and was corrected: QELAR's "no void handling" was replaced with the documented limitation (slow convergence with many nodes or high mobility, as reported by later work).

## Rows to click-check first

These have single-source DOIs or non-publisher links:

- #7 (CAMP)
- #11 (TNSE trust)
- #18 (RANR, AMiner link)
- #28 (QELAR)
