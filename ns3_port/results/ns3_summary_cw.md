# ns-3 evaluation: QLFR vs LAQR (MAC: UanMacCw)

Runs: 300 (10 seeds x 5 densities x 3 protocols x 2 scenarios). Mean +/- 95% CI over seeds.

## Scenario: desync

### Averaged over densities

| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.821 ± 0.007 | 2.466 ± 0.041 | 41,517 ± 644 | 5,168 ± 75 | 43.1 ± 0.8 |
| QLFR (P_th = 0.97) | 0.821 ± 0.007 | 2.491 ± 0.039 | 41,264 ± 628 | 5,218 ± 42 | 43.8 ± 0.5 |
| LAQR | 0.589 ± 0.013 | 0.947 ± 0.011 | 80,390 ± 1,557 | 2,922 ± 15 | 8.8 ± 0.1 |

### Per density (mean PDR / delay / lifetime)

| Nodes | QLFR (P_th = 0.90) | QLFR (P_th = 0.97) | LAQR |
|---|---|---|---|
| 100 | 0.663 / 1.53 s / 64,194 s | 0.663 / 1.53 s / 64,194 s | 0.552 / 0.92 s / 101,169 s |
| 200 | 0.826 / 2.29 s / 40,816 s | 0.826 / 2.29 s / 40,816 s | 0.600 / 0.93 s / 86,065 s |
| 300 | 0.868 / 2.61 s / 35,725 s | 0.868 / 2.62 s / 35,525 s | 0.621 / 0.92 s / 75,661 s |
| 400 | 0.872 / 2.83 s / 34,018 s | 0.867 / 2.86 s / 33,541 s | 0.597 / 0.96 s / 71,141 s |
| 500 | 0.876 / 3.06 s / 32,831 s | 0.883 / 3.15 s / 32,243 s | 0.577 / 1.00 s / 67,912 s |

### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)

| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | -0.232 ± 0.013 | -1.519 ± 0.039 | 2.00 ± 0.03 | 0.58 ± 0.01 | 0.24 ± 0.00 |
| QLFR (P_th = 0.97) | -0.232 ± 0.013 | -1.544 ± 0.036 | 2.01 ± 0.03 | 0.58 ± 0.00 | 0.23 ± 0.00 |

## Scenario: sync

### Averaged over densities

| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.747 ± 0.013 | 2.853 ± 0.045 | 47,279 ± 650 | 4,885 ± 41 | 40.3 ± 0.6 |
| QLFR (P_th = 0.97) | 0.747 ± 0.014 | 2.855 ± 0.045 | 47,292 ± 628 | 4,892 ± 42 | 40.4 ± 0.6 |
| LAQR | 0.310 ± 0.006 | 1.167 ± 0.014 | 96,141 ± 1,353 | 2,599 ± 13 | 5.7 ± 0.1 |

### Per density (mean PDR / delay / lifetime)

| Nodes | QLFR (P_th = 0.90) | QLFR (P_th = 0.97) | LAQR |
|---|---|---|---|
| 100 | 0.514 / 1.97 s / 75,652 s | 0.514 / 1.97 s / 75,652 s | 0.278 / 1.12 s / 122,510 s |
| 200 | 0.727 / 2.61 s / 48,076 s | 0.727 / 2.61 s / 48,076 s | 0.321 / 1.13 s / 105,047 s |
| 300 | 0.821 / 2.89 s / 40,079 s | 0.821 / 2.89 s / 40,079 s | 0.342 / 1.14 s / 90,168 s |
| 400 | 0.831 / 3.19 s / 37,107 s | 0.831 / 3.19 s / 37,107 s | 0.314 / 1.18 s / 83,175 s |
| 500 | 0.842 / 3.60 s / 35,483 s | 0.842 / 3.61 s / 35,547 s | 0.295 / 1.27 s / 79,803 s |

### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)

| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | -0.437 ± 0.011 | -1.686 ± 0.039 | 2.11 ± 0.02 | 0.55 ± 0.00 | 0.17 ± 0.00 |
| QLFR (P_th = 0.97) | -0.437 ± 0.011 | -1.687 ± 0.040 | 2.11 ± 0.02 | 0.55 ± 0.00 | 0.17 ± 0.00 |

