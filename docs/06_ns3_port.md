# ns-3 Port: QLFR and LAQR on the ns-3 UAN Stack

**Date:** 3 Nov 2026.
- **Code:** `ns3_port/scratch/laqr-sim/laqr-sim.cc` (one ns-3 program that runs both protocols); `ns3_port/build_ns3.sh` (fetches and builds ns-3.44 and links the program).
- **Evaluation:** `ns3_port/run_eval.sh`, `ns3_port/report.py`.
- **Results (ALOHA MAC):** `ns3_port/results/ns3_eval.csv` (300 runs), `ns3_summary.md`, `ns3_eval.png`.
- **Results (UanMacCw MAC):** `ns3_port/results/ns3_eval_cw.csv` (300 runs), `ns3_summary_cw.md`, `ns3_eval_cw.png`.

The Python simulator (`qlfr_repro/`) has no MAC: transmissions never collide, and link loss comes only from the paper's Rayleigh/BPSK model. This port re-runs both protocols over ns-3's underwater acoustic stack, which has a real MAC (with collisions), propagation, noise and an energy model. The aim is to check whether the Python-sim conclusions in `05_final_protocol_LAQR.md` hold in ns-3.

## 1. What is modelled

| Layer | ns-3 component | Setting |
|---|---|---|
| Propagation | `UanPropModelThorp` | Thorp absorption, spreading factor 1.5 |
| Noise | `UanNoiseModelDefault` | Default (wind and shipping) |
| PHY | `UanPhyGen`, BPSK, `UanPhyPerCommonModes`, `UanPhyCalcSinrDefault` | 20 kbps, f_c = 40 kHz, B = 20 kHz, source level 114 dB re µPa, RX threshold 10 dB |
| MAC | `UanMacAloha` (Sections 3.1–3.3) | Pure ALOHA: no carrier sense and no ACKs. A send is retried by the routing layer only if the node's own PHY is busy transmitting. |
| MAC | `UanMacCw` (Section 3.4) | Carrier sense plus a random contention-window backoff (ns-3 defaults: CW = 10 slots, slot 20 ms). It has no ACKs and buffers one packet; the routing layer retries a refused send every packet time, up to 400 times. |
| Energy | `AcousticModemEnergyModel` + `BasicEnergySource` | Ψ_t = 2 W, Ψ_r = 0.5 W, idle 0 W, E_ini = 1000 J (paper Table II) |
| Mobility | Reflecting random walk, one step per round | v = 3 m/s, 10 s rounds; sources stay at the bottom layer and sinks stay at the surface |
| Topology | 500 m cube; 100–500 sensors; 5 sources at the bottom; 5 surface sinks | Paper Table II |

**Routing logic** is the same as the Python version (see `01_…` and `05_…`):
- QLFR uses the reward of Eq. (5)–(7), the Q-update of Eq. (8), the holding time τ = k(n − 1), overhearing suppression (Alg. 1), and the global list-length adaptation against P_th.
- LAQR adds the sequence-number link estimator (β = 0.05, prior 0.9), the reward term w_lq(1 − p̂) with w_lq = 0.25, and per-hop lists with ρ = 0.99 (cap 8).
- No LAQR parameter was re-tuned for ns-3.

Routing knowledge is exchanged by one 30-byte beacon per node per round, sent at a random time in the first 5.8 s. Q-values are updated at 6.0 s. Each source then generates one 63-byte packet at a random time in [6.1, 6.1 + J] s.

## 2. ns-3-specific settings and how they were chosen

All settings below were fixed on development seeds 100–101 before the evaluation seeds (0–9) were run.

| Setting | Value | Reason |
|---|---|---|
| Modem | 20 kbps, 40 kHz, 114 dB | The `--calib=1` two-node test (400 packets per distance) gives success 1.0 up to 150 m and 0.0 from 175 m. That matches the paper's R = 150 m. A slower 10 kbps / 10 kHz modem doubled the airtime and the collisions. |
| k (holding-time step) | 0.15 s | The paper's k = 0.05 s is shorter than a packet's airtime plus the propagation-delay spread between candidates (25 ms + up to 0.1 s). Lower-ranked candidates then transmit before they can overhear the first one, and the copies collide. |
| Beacons | Every round; neighbours expire after 1 round | With beacons every 2 rounds, 14% of LAQR's chosen next hops had already moved out of range by the time data was sent. |
| Source jitter J | 3.5 s ("desync"), with 0.5 s ("sync") as a stress case | See Section 4 |

**Hard range cutoff.** ns-3's UAN PHY has no small-scale fading. A link is either essentially perfect (closer than about 150 m, with no collision) or dead. Packet loss therefore comes almost entirely from **collisions** and from **neighbours moving out of range**. The Python model's random per-link losses play no role here.

## 3. Results (evaluation seeds 0–9, 50 rounds, 100–500 nodes; mean ± 95% CI)

### 3.1 Desynchronised sources (J = 3.5 s), the main scenario

| Protocol | PDR | Delay (s) | Lifetime (s) | Network energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.465 ± 0.013 | 1.215 ± 0.015 | 32,416 ± 985 | 3,232 ± 39 | 18.0 ± 0.2 |
| **LAQR** | **0.546 ± 0.010** | **0.780 ± 0.007** | **40,129 ± 1,111** | **2,705 ± 27** | **7.4 ± 0.1** |

**Paired LAQR − QLFR** (same seed and density):
- ΔPDR = **+0.081 ± 0.012**
- ΔDelay = **−0.436 ± 0.016 s**
- Lifetime ratio = **1.24 ± 0.01**
- Energy ratio = 0.82
- Transmission ratio = 0.42

LAQR is better at every density (100–500 nodes; see `ns3_summary.md`), and its delivery gain grows with density (+0.014 at 100 nodes, +0.111 at 500).

### 3.2 Synchronised sources (J = 0.5 s), stress case

| Protocol | PDR | Delay (s) | Lifetime (s) | Network energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | **0.604 ± 0.018** | 1.850 ± 0.027 | 30,657 ± 955 | 3,486 ± 41 | 23.2 ± 0.4 |
| LAQR | 0.264 ± 0.014 | 0.892 ± 0.015 | **47,856 ± 976** | **2,421 ± 26** | 4.7 ± 0.1 |

**Paired:** ΔPDR = **−0.341 ± 0.013**. Lifetime ratio = 1.56. LAQR's delay is averaged over far fewer delivered packets, so it is not comparable here.

### 3.3 QLFR at P_th = 0.97

In every ns-3 run, QLFR's end-to-end PDR stays below 0.90. Its global list length therefore stays at the cap of 8 for both P_th = 0.90 and P_th = 0.97, and the two settings give **identical** results. The P_th = 0.97 row in `ns3_summary.md` is kept only for completeness.

### 3.4 Rerun with a carrier-sense MAC (`UanMacCw`)

This is the same 300-run design: seeds 0–9, 100–500 nodes, both scenarios, and every other setting unchanged. The MAC settings are ns-3's defaults; only the retry limit (400) was set, on development seed 101.

| Scenario | Protocol | PDR | Delay (s) | Lifetime (s) | Network energy (J) | Tx/packet |
|---|---|---|---|---|---|---|
| desync | QLFR (P_th = 0.90) | 0.439 ± 0.007 | 1.348 ± 0.017 | 31,410 ± 861 | 3,324 ± 39 | 18.4 ± 0.2 |
| desync | **LAQR** | **0.544 ± 0.012** | **0.860 ± 0.011** | **38,958 ± 870** | **2,778 ± 28** | **7.5 ± 0.1** |
| sync | QLFR (P_th = 0.90) | **0.574 ± 0.014** | 2.091 ± 0.042 | 28,980 ± 712 | 3,620 ± 47 | 24.4 ± 0.5 |
| sync | LAQR | 0.320 ± 0.011 | 1.101 ± 0.016 | **45,301 ± 943** | **2,552 ± 27** | 5.3 ± 0.1 |

**Paired LAQR − QLFR, by MAC:**

| Scenario | MAC | ΔPDR | ΔDelay (s) | Lifetime ratio | Tx ratio |
|---|---|---|---|---|---|
| desync | ALOHA | +0.081 ± 0.012 | −0.436 ± 0.016 | 1.24 ± 0.01 | 0.42 |
| desync | **UanMacCw** | **+0.106 ± 0.011** | −0.489 ± 0.019 | 1.24 ± 0.01 | 0.42 |
| sync | ALOHA | −0.341 ± 0.013 | (not comparable) | 1.56 ± 0.02 | 0.22 |
| sync | **UanMacCw** | **−0.254 ± 0.010** | (not comparable) | 1.56 ± 0.03 | 0.24 |

What changes with carrier sensing:
- **Conclusions are unchanged.** LAQR wins on every metric in the desync scenario, at every density; its delivery gain widens from +0.081 to +0.106. In the sync scenario it still loses delivery, but the gap narrows from −0.34 to −0.25.
- **Carrier sensing helps LAQR and slightly hurts QLFR.**
  - LAQR in sync: 0.264 → 0.320. LAQR in desync: 0.546 → 0.544, no change.
  - QLFR: 0.465 → 0.439 (desync) and 0.604 → 0.574 (sync), with about 0.1–0.2 s more delay.
  - Backoff delays QLFR's many redundant copies. Those copies then arrive after the holding-time order they were meant to follow, so suppression works less well.
- **Absolute delivery barely improves.** Propagation over 150 m takes up to 0.1 s, about four times the 25 ms packet airtime. A node therefore often senses the channel as idle while another transmission is still on its way: the classic reason carrier sensing works poorly underwater. Collisions remain the main cause of loss, and the beacon-vs-data estimation gap in Section 4 (item 3) still applies.

## 4. What ns-3 shows that the Python simulator could not

1. **Absolute delivery is much lower over an ALOHA MAC** (0.26–0.60 here, against 0.90–0.97 in Python), for both protocols.
   - At 114 dB, a transmission interferes at about 4–5× its decoding range, so a 500 m cube is essentially **one collision domain**.
   - Holding-time anypath forwarding adds intra-flow collisions on top.
   - These numbers are not comparable with the paper's Figs. 6–15, which assume no collisions.
2. **When source traffic is spread out (desync), LAQR's main claims hold:**
   - higher delivery (+8 points);
   - lower delay (−0.44 s);
   - 1.24× lifetime;
   - 58% fewer transmissions.

   QLFR's large lists (up to 8 candidates, 18 transmissions per packet) create collisions that cost it delivery and delay.
3. **When all sources fire within 0.5 s (sync), LAQR loses a third of its delivery.** The cause, diagnosed on the development seeds:
   - LAQR learns p̂ from beacons, which are spread over 6 s and almost never collide, so p̂ stays near 0.9.
   - Data packets, by contrast, meet bursty, correlated collisions: the top-ranked candidate was heard re-forwarding only 30% of the time.
   - Sizing the list on 1 − Π(1 − p̂) ≥ ρ therefore picks about 2 candidates where many more are needed.
   - QLFR's blunt global adaptation (list pinned at 8) brute-forces through the collisions, at 1.4× the energy and twice the delay.
4. **Attempted fix (development seeds only, not adopted).** We tried learning p̂ from data-plane implicit ACKs: overhearing whether the top-ranked candidate, which is never suppressed, forwards the packet. We tried it both per link and as a per-node calibration factor (`--ackMode=1/2`).
   - Per-link samples are too sparse to move p̂.
   - The node-level calibration lengthened lists (about 2 → 3–4 candidates) but did not consistently raise delivery, because the extra copies also collide.
   - It is left in the code, switched off by default.

   A collision-aware MAC (carrier sensing or slotted access) or traffic-aware list sizing is the natural next step. It is listed as future work rather than tuned here.

## 5. Implications for the paper

- The ns-3 results **support** LAQR's efficiency claim (fewer transmissions, longer lifetime, lower delay) in all cases.
- They **support** its delivery claim when collisions are not bursty.
- They show a **limitation**: LAQR's reliability target assumes independent link losses, and beacon-based estimates miss correlated data-time collisions. This should be stated alongside the sparse/shadowing limitation already in `05_…` (Section 3.4).
- The conclusions hold with both a pure-ALOHA MAC and a carrier-sense MAC (`UanMacCw`, Section 3.4). Because carrier sensing is weak at acoustic propagation delays, a handshake or scheduled MAC (e.g. ns-3's `UanMacRc`, or Aqua-Sim FG's protocols) is the remaining check. So is a traffic-aware LAQR list rule for synchronised traffic.

## 6. Reproduce

```bash
bash ns3_port/build_ns3.sh /home/user/ns-3      # clone + build ns-3.44 (about 10 min)
export LD_LIBRARY_PATH=/home/user/ns-3/build/lib
/home/user/ns-3/build/scratch/laqr-sim/ns3.44-laqr-sim --calib=1     # range calibration
/home/user/ns-3/build/scratch/laqr-sim/ns3.44-laqr-sim --protocol=laqr --nodes=100 --seed=0
#   -> laqr,100,0,3,0.532,0.789511,633.958,47812.4,6.84,5250,0  (matches results/ns3_eval.csv)
ns3_port/run_eval.sh /home/user/ns-3 4          # 300 runs, about 45 min on 4 cores
python3 ns3_port/report.py                      # tables + figure
ns3_port/run_eval.sh /home/user/ns-3 4 cw --mac=cw --maxAttempts=400   # UanMacCw rerun -> results/ns3_eval_cw.csv
python3 ns3_port/report.py cw                   # -> results/ns3_summary_cw.md, ns3_eval_cw.png
```

**Output columns:**
- protocol, nodes, seed, speed;
- pdr;
- delay: mean end-to-end delay of delivered packets;
- energy_used: total sensor energy, in J;
- lifetime: projected time until the most-drained sensor is empty, at its observed drain rate;
- tx_per_pkt: data transmissions per generated packet;
- helloTx;
- sendFails.

Diagnostic counters go to stderr.
