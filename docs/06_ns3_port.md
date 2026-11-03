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
| MAC | `UanMacAloha` | Pure ALOHA: no carrier sense and no ACKs. A send is retried by the routing layer only if the node's own PHY is busy transmitting. |
| MAC | `UanMacCw` | Carrier sense plus a random contention-window backoff (ns-3 defaults: CW = 10 slots, slot 20 ms). It has no ACKs and buffers one packet; the routing layer retries a refused send every packet time, up to 400 times. |
| Energy | `AcousticModemEnergyModel` + `BasicEnergySource` | Ψ_t = 2 W, Ψ_r = 0.5 W, idle 0 W, E_ini = 1000 J (paper Table II) |
| Mobility | Reflecting random walk, one step per round | v = 3 m/s, 20 s rounds (60 m per step); sources stay at the bottom layer and sinks stay at the surface |
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
| Source jitter J | 3.5 s ("desync" / spread out) and 0.5 s ("sync" / simultaneous) | Two traffic patterns |
| Round length | 20 s (corrected from 10 s) | Packets must finish inside their round; with 20 s rounds, no pending forward is left at a round boundary (dev seeds 101–102). Results were checked to be stable between 15 s and 20 s. |

**Hard range cutoff.** ns-3's UAN PHY has no small-scale fading. A link is either essentially perfect (closer than about 150 m, with no collision) or dead. Packet loss therefore comes almost entirely from **collisions** and from **neighbours moving out of range**. The Python model's random per-link losses play no role here.

## 3. Results (evaluation seeds 0–9, 50 rounds of 20 s, 100–500 nodes; mean ± 95% CI)

> **Correction (3 Nov 2026 audit, `07_audit_and_novelty.md`).** The first version of this document used 10 s rounds and reported LAQR *ahead* of QLFR on delivery with spread-out traffic (+0.081 ALOHA, +0.106 UanMacCw). That result was an artifact. Packets still in flight at the round boundary ran into the next round's beacon burst and a 30 m mobility jump, and pending forwards were cancelled. This hit QLFR's long-lived copies far harder than LAQR's. With 20 s rounds every packet finishes inside its round, and the conclusion reverses. The old files are in `ns3_port/results/superseded_10s_rounds/`.

### 3.1 Absolute results

| MAC | Traffic | Protocol | PDR | Delay (s) | Lifetime (s) | Network energy (J) | Tx/packet |
|---|---|---|---|---|---|---|---|
| ALOHA | spread out (J = 3.5 s) | QLFR (P_th = 0.90) | **0.800 ± 0.008** | 1.997 ± 0.036 | 46,045 ± 549 | 4,663 ± 39 | 37.5 ± 0.6 |
| ALOHA | spread out | LAQR | 0.572 ± 0.015 | **0.825 ± 0.011** | **83,316 ± 1,307** | **2,808 ± 17** | **8.3 ± 0.1** |
| ALOHA | simultaneous (J = 0.5 s) | QLFR (P_th = 0.90) | **0.703 ± 0.010** | 2.296 ± 0.057 | 53,760 ± 1,069 | 4,294 ± 42 | 33.2 ± 0.5 |
| ALOHA | simultaneous | LAQR | 0.250 ± 0.008 | **0.938 ± 0.011** | **101,465 ± 1,318** | **2,452 ± 14** | **4.9 ± 0.1** |
| UanMacCw | spread out | QLFR (P_th = 0.90) | **0.821 ± 0.007** | 2.466 ± 0.041 | 41,517 ± 644 | 5,168 ± 75 | 43.1 ± 0.8 |
| UanMacCw | spread out | LAQR | 0.589 ± 0.013 | **0.947 ± 0.011** | **80,390 ± 1,557** | **2,922 ± 15** | **8.8 ± 0.1** |
| UanMacCw | simultaneous | QLFR (P_th = 0.90) | **0.747 ± 0.013** | 2.853 ± 0.045 | 47,279 ± 650 | 4,885 ± 41 | 40.3 ± 0.6 |
| UanMacCw | simultaneous | LAQR | 0.310 ± 0.006 | **1.167 ± 0.014** | **96,141 ± 1,353** | **2,599 ± 13** | **5.7 ± 0.1** |

### 3.2 Paired LAQR − QLFR (P_th = 0.90), same seed and density

| MAC | Traffic | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|---|
| ALOHA | spread out | **−0.228 ± 0.014** | −1.172 ± 0.032 | **1.85 ± 0.02** | 0.62 | 0.25 |
| ALOHA | simultaneous | **−0.454 ± 0.009** | −1.358 ± 0.061 | **1.96 ± 0.04** | 0.58 | 0.18 |
| UanMacCw | spread out | **−0.232 ± 0.013** | −1.519 ± 0.039 | **2.00 ± 0.03** | 0.58 | 0.24 |
| UanMacCw | simultaneous | **−0.437 ± 0.011** | −1.686 ± 0.039 | **2.11 ± 0.02** | 0.55 | 0.17 |

The pattern is the same at every density (per-density tables in `ns3_summary.md` and `ns3_summary_cw.md`). QLFR's delivery rises with density, from 0.64–0.66 at 100 nodes to 0.86–0.88 at 500 with spread-out traffic. LAQR's stays at 0.52–0.62. Delay is averaged over delivered packets only, so LAQR's lower delay partly reflects which packets got through.

**QLFR at P_th = 0.97.** QLFR's cumulative PDR stays below 0.90 in nearly every run, so its list stays at the cap of 8 under both thresholds. The two settings differ by at most 0.007 PDR. The 0.97 rows are in the summary files.

### 3.3 Carrier sensing (`UanMacCw`) vs ALOHA

- Carrier sensing raises delivery slightly for both protocols: +0.02–0.04 for QLFR and +0.02–0.06 for LAQR. It also adds 0.1–0.6 s of delay through backoff.
- It does not change any conclusion. Propagation over 150 m takes up to 0.1 s, about four times the 25 ms packet airtime, so a node often senses the channel as idle while another packet is still on its way.

### 3.4 `UanMacRc` cannot be used

`UanMacRc` is ns-3's reservation (RTS/CTS) MAC, and it cannot carry these protocols:
- It is built for **one gateway and one hop**: it unicasts every data packet to its associated `UanMacRcGw` gateway, and passes up only packets addressed to the node itself. Broadcast beacons and candidate overhearing, which both protocols need, are impossible.
- With our 5 surface sinks as gateways, ns-3 aborts with "Received CTS at GW. Currently only support single GW network!".
- With a single sink, only that gateway receives anything (35 beacons over 10 rounds), no neighbour tables form, and both protocols deliver **0%**.
- `--mac=rc` is in the code only to reproduce this.

## 4. What ns-3 shows that the Python simulator could not

1. **The delivery ranking flips once there is a real MAC.** In Python (no collisions) LAQR beats QLFR on delivery and lifetime together. In ns-3, QLFR delivers 23–45 points more, and LAQR lasts about twice as long with about one quarter of the transmissions.
2. **Why LAQR under-delivers.**
   - LAQR learns p̂ from beacons, which are spread over 6 s and almost never collide, so p̂ stays near 0.9.
   - Sizing the list on 1 − Π(1 − p̂) ≥ ρ = 0.99 then picks about 2 candidates.
   - Data packets meet bursty, correlated collisions that beacons never see. In the diagnostic runs, the top-ranked candidate was heard re-forwarding only 30–65% of the time.
   - QLFR keeps 8 candidates and its redundancy pushes packets through, at twice the energy.
3. **Raising ρ helps but cannot close the gap** (dev seeds 101–102, 300 nodes): ρ = 0.9999 gives PDR 0.75 at 18.7 tx/packet, against QLFR's 0.84 at 38.5. Delivery tops out around 0.75 (see `07_…`, Section 2).
4. **Implicit-ACK link learning was tried and not adopted** (development seeds only). We learned p̂ from overhearing the top-ranked candidate forward, both per link and as a per-node calibration factor (`--ackMode=1/2`). Per-link samples are too sparse to move p̂, and the calibration lengthened lists without consistently raising delivery. It is left in the code, switched off.
5. **Simulation design matters.** A round boundary that cuts packets mid-flight biased the first results by about 30 points of QLFR delivery. Any round-based UASN simulation should check that packets finish within their round.

## 5. Implications for the paper

- LAQR's **efficiency claim survives in ns-3**: about 2× lifetime, ¼ of the transmissions, 1.2–1.7 s lower delay.
- Its **delivery claim does not**: over ALOHA and carrier-sense MACs, it delivers 23–45 points less than QLFR.
- The paper must present LAQR as a low-energy operating point plus a mechanism study, or first fix the estimator. Beacon-based reliability estimates miss correlated data-time collisions, so a collision-aware estimator or traffic-aware sizing is the next design step.
- `UanMacRc` cannot be used. A handshake MAC that supports multi-hop broadcast would have to be implemented, or Aqua-Sim FG's MACs used.

## 6. Reproduce

```bash
bash ns3_port/build_ns3.sh /home/user/ns-3      # clone + build ns-3.44 (about 10 min)
export LD_LIBRARY_PATH=/home/user/ns-3/build/lib
/home/user/ns-3/build/scratch/laqr-sim/ns3.44-laqr-sim --calib=1     # range calibration
/home/user/ns-3/build/scratch/laqr-sim/ns3.44-laqr-sim --protocol=laqr --nodes=100 --seed=0
#   -> laqr,100,0,3,0.488,0.880334,654.626,108983,7.376,5250,0  (matches results/ns3_eval.csv)
ns3_port/run_eval.sh /home/user/ns-3 4          # 300 runs, about 50 min on 4 cores
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
