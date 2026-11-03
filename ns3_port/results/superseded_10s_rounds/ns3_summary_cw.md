# ns-3 evaluation: QLFR vs LAQR (MAC: UanMacCw)

Runs: 300 (10 seeds x 5 densities x 3 protocols x 2 scenarios). Mean +/- 95% CI over seeds.

## Scenario: desync

### Averaged over densities

| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.439 ± 0.007 | 1.348 ± 0.017 | 31,410 ± 861 | 3,324 ± 39 | 18.4 ± 0.2 |
| QLFR (P_th = 0.97) | 0.439 ± 0.007 | 1.348 ± 0.017 | 31,410 ± 861 | 3,324 ± 39 | 18.4 ± 0.2 |
| LAQR | 0.544 ± 0.012 | 0.860 ± 0.011 | 38,958 ± 870 | 2,778 ± 28 | 7.5 ± 0.1 |

### Per density (mean PDR / delay / lifetime)

| Nodes | QLFR (P_th = 0.90) | QLFR (P_th = 0.97) | LAQR |
|---|---|---|---|
| 100 | 0.476 / 1.17 s / 36,020 s | 0.476 / 1.17 s / 36,020 s | 0.535 / 0.83 s / 46,442 s |
| 200 | 0.454 / 1.36 s / 33,256 s | 0.454 / 1.36 s / 33,256 s | 0.563 / 0.84 s / 42,564 s |
| 300 | 0.452 / 1.37 s / 30,079 s | 0.452 / 1.37 s / 30,079 s | 0.575 / 0.83 s / 36,950 s |
| 400 | 0.416 / 1.39 s / 29,388 s | 0.416 / 1.39 s / 29,388 s | 0.547 / 0.88 s / 35,103 s |
| 500 | 0.395 / 1.44 s / 28,307 s | 0.395 / 1.44 s / 28,307 s | 0.502 / 0.92 s / 33,731 s |

### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)

| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | +0.106 ± 0.011 | -0.489 ± 0.019 | 1.24 ± 0.01 | 0.82 ± 0.00 | 0.42 ± 0.01 |
| QLFR (P_th = 0.97) | +0.106 ± 0.011 | -0.489 ± 0.019 | 1.24 ± 0.01 | 0.82 ± 0.00 | 0.42 ± 0.01 |

## Scenario: sync

### Averaged over densities

| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.574 ± 0.014 | 2.091 ± 0.042 | 28,980 ± 712 | 3,620 ± 47 | 24.4 ± 0.5 |
| QLFR (P_th = 0.97) | 0.574 ± 0.014 | 2.091 ± 0.042 | 28,980 ± 712 | 3,620 ± 47 | 24.4 ± 0.5 |
| LAQR | 0.320 ± 0.011 | 1.101 ± 0.016 | 45,301 ± 943 | 2,552 ± 27 | 5.3 ± 0.1 |

### Per density (mean PDR / delay / lifetime)

| Nodes | QLFR (P_th = 0.90) | QLFR (P_th = 0.97) | LAQR |
|---|---|---|---|
| 100 | 0.501 / 1.76 s / 34,996 s | 0.501 / 1.76 s / 34,996 s | 0.303 / 1.05 s / 56,402 s |
| 200 | 0.622 / 2.08 s / 30,632 s | 0.622 / 2.08 s / 30,632 s | 0.345 / 1.09 s / 49,649 s |
| 300 | 0.626 / 2.15 s / 26,996 s | 0.626 / 2.15 s / 26,996 s | 0.338 / 1.07 s / 42,938 s |
| 400 | 0.592 / 2.18 s / 26,849 s | 0.592 / 2.18 s / 26,849 s | 0.321 / 1.10 s / 40,049 s |
| 500 | 0.530 / 2.28 s / 25,428 s | 0.530 / 2.28 s / 25,428 s | 0.292 / 1.19 s / 37,466 s |

### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)

| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | -0.254 ± 0.010 | -0.990 ± 0.033 | 1.56 ± 0.03 | 0.69 ± 0.01 | 0.24 ± 0.01 |
| QLFR (P_th = 0.97) | -0.254 ± 0.010 | -0.990 ± 0.033 | 1.56 ± 0.03 | 0.69 ± 0.01 | 0.24 ± 0.01 |

