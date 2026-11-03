# ns-3 evaluation: QLFR vs LAQR

Runs: 300 (10 seeds x 5 densities x 3 protocols x 2 scenarios). Mean +/- 95% CI over seeds.

## Scenario: desync

### Averaged over densities

| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.465 ± 0.013 | 1.215 ± 0.015 | 32,416 ± 985 | 3,232 ± 39 | 18.0 ± 0.2 |
| QLFR (P_th = 0.97) | 0.465 ± 0.013 | 1.215 ± 0.015 | 32,416 ± 985 | 3,232 ± 39 | 18.0 ± 0.2 |
| LAQR | 0.546 ± 0.010 | 0.780 ± 0.007 | 40,129 ± 1,111 | 2,705 ± 27 | 7.4 ± 0.1 |

### Per density (mean PDR / delay / lifetime)

| Nodes | QLFR (P_th = 0.90) | QLFR (P_th = 0.97) | LAQR |
|---|---|---|---|
| 100 | 0.506 / 1.07 s / 36,435 s | 0.506 / 1.07 s / 36,435 s | 0.520 / 0.77 s / 47,823 s |
| 200 | 0.478 / 1.21 s / 34,671 s | 0.478 / 1.21 s / 34,671 s | 0.564 / 0.76 s / 43,556 s |
| 300 | 0.489 / 1.25 s / 30,997 s | 0.489 / 1.25 s / 30,997 s | 0.576 / 0.76 s / 37,815 s |
| 400 | 0.445 / 1.26 s / 30,690 s | 0.445 / 1.26 s / 30,690 s | 0.552 / 0.77 s / 36,648 s |
| 500 | 0.409 / 1.28 s / 29,288 s | 0.409 / 1.28 s / 29,288 s | 0.520 / 0.82 s / 34,804 s |

### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)

| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | +0.081 ± 0.012 | -0.436 ± 0.016 | 1.24 ± 0.01 | 0.82 ± 0.00 | 0.42 ± 0.01 |
| QLFR (P_th = 0.97) | +0.081 ± 0.012 | -0.436 ± 0.016 | 1.24 ± 0.01 | 0.82 ± 0.00 | 0.42 ± 0.01 |

## Scenario: sync

### Averaged over densities

| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.604 ± 0.018 | 1.850 ± 0.027 | 30,657 ± 955 | 3,486 ± 41 | 23.2 ± 0.4 |
| QLFR (P_th = 0.97) | 0.604 ± 0.018 | 1.850 ± 0.027 | 30,657 ± 955 | 3,486 ± 41 | 23.2 ± 0.4 |
| LAQR | 0.264 ± 0.014 | 0.892 ± 0.015 | 47,856 ± 976 | 2,421 ± 26 | 4.7 ± 0.1 |

### Per density (mean PDR / delay / lifetime)

| Nodes | QLFR (P_th = 0.90) | QLFR (P_th = 0.97) | LAQR |
|---|---|---|---|
| 100 | 0.457 / 1.52 s / 38,842 s | 0.457 / 1.52 s / 38,842 s | 0.233 / 0.89 s / 59,687 s |
| 200 | 0.653 / 1.85 s / 31,025 s | 0.653 / 1.85 s / 31,025 s | 0.274 / 0.88 s / 52,403 s |
| 300 | 0.663 / 1.93 s / 28,550 s | 0.663 / 1.93 s / 28,550 s | 0.268 / 0.88 s / 44,795 s |
| 400 | 0.653 / 1.95 s / 28,027 s | 0.653 / 1.95 s / 28,027 s | 0.278 / 0.89 s / 42,306 s |
| 500 | 0.596 / 2.00 s / 26,841 s | 0.596 / 2.00 s / 26,841 s | 0.264 / 0.93 s / 40,092 s |

### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)

| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | -0.341 ± 0.013 | -0.957 ± 0.030 | 1.56 ± 0.02 | 0.68 ± 0.00 | 0.22 ± 0.01 |
| QLFR (P_th = 0.97) | -0.341 ± 0.013 | -0.957 ± 0.030 | 1.56 ± 0.02 | 0.68 ± 0.00 | 0.22 ± 0.01 |

